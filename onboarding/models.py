from typing import List
from django.db import models

from project.common_data import Choices
from project import geocoding
from project.util.nyc import PAD_BBL_DIGITS, PAD_BIN_DIGITS
from project.util.instance_change_tracker import InstanceChangeTracker
from project.util.hyperlink import Hyperlink
from project.util.admin_util import admin_field
from users.models import JustfixUser


BOROUGH_CHOICES = Choices.from_file('borough-choices.json')

LEASE_CHOICES = Choices.from_file('lease-choices.json')

SIGNUP_INTENT_CHOICES = Choices.from_file('signup-intent-choices.json')

ADDR_META_HELP = (
    "This field is automatically updated when you change the address or "
    "borough, so you generally shouldn't have to change it manually."
)

ADDRESS_MAX_LENGTH = 200


class AddressWithoutBoroughDiagnostic(models.Model):
    '''
    Information about submitted onboarding forms that contained
    address information without borough information. For more
    details on the rationale behind this, see:

        https://github.com/JustFixNYC/tenants2/issues/533

    We're not storing this information in Google Analytics
    or Rollbar because those services make it very hard
    or impossible to delete sensitive data, and a user's
    address can be PII.
    '''

    address = models.CharField(max_length=ADDRESS_MAX_LENGTH)

    created_at = models.DateTimeField(auto_now_add=True)


class OnboardingInfo(models.Model):
    '''
    The details a user filled out when they joined the site.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # This keeps track of the fields that comprise our address.
        self.__addr = InstanceChangeTracker(self, ['address', 'borough'])

        # This keeps track of fields that comprise metadata about our address,
        # which can be determined from the fields comprising our address.
        self.__addr_meta = InstanceChangeTracker(self, ['zipcode', 'pad_bbl', 'pad_bin'])

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(
        JustfixUser, on_delete=models.CASCADE, related_name='onboarding_info')

    signup_intent = models.CharField(
        max_length=30,
        choices=SIGNUP_INTENT_CHOICES.choices,
        help_text="The reason the user originally signed up with us."
    )

    address = models.CharField(
        max_length=ADDRESS_MAX_LENGTH,
        help_text="The user's address. Only street name and number are required."
    )

    address_verified = models.BooleanField(
        help_text=(
            "Whether we've verified, on the server-side, that the user's "
            "address is valid."
        )
    )

    borough = models.CharField(
        max_length=20, choices=BOROUGH_CHOICES.choices,
        help_text="The New York City borough the user's address is in."
    )

    zipcode = models.CharField(
        # https://stackoverflow.com/q/325041/2422398
        max_length=12,
        blank=True,
        help_text=f"The user's ZIP code. {ADDR_META_HELP}"
    )

    pad_bbl: str = models.CharField(
        max_length=PAD_BBL_DIGITS,
        blank=True,
        help_text=f"The user's Boro, Block, and Lot number. {ADDR_META_HELP}"
    )

    pad_bin: str = models.CharField(
        max_length=PAD_BIN_DIGITS,
        blank=True,
        help_text=f"The user's building identification number (BIN). {ADDR_META_HELP}"
    )

    apt_number = models.CharField(max_length=10)

    floor_number = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="The floor number the user's apartment is on."
    )

    is_in_eviction = models.BooleanField(
        help_text="Has the user received an eviction notice?")

    needs_repairs = models.BooleanField(
        help_text="Does the user need repairs in their apartment?")

    has_no_services = models.BooleanField(
        help_text="Is the user missing essential services like water?")

    has_pests = models.BooleanField(
        help_text="Does the user have pests like rodents or bed bugs?")

    has_called_311 = models.BooleanField(
        help_text="Has the user called 311 before?")

    lease_type = models.CharField(
        max_length=30, choices=LEASE_CHOICES.choices,
        help_text="The type of lease the user has on their dwelling.")

    receives_public_assistance = models.BooleanField(
        help_text="Does the user receive public assistance, e.g. Section 8?")

    can_we_sms = models.BooleanField(
        help_text="Whether we can contact the user via SMS to follow up.")

    @property
    def borough_label(self) -> str:
        if not self.borough:
            return ''
        return BOROUGH_CHOICES.get_label(self.borough)

    @property
    def city(self) -> str:
        '''
        The city of the user. This will be the same as the borough name,
        except we use "New York" instead of "Manhattan".
        '''

        if not self.borough:
            return ''
        if self.borough == BOROUGH_CHOICES.MANHATTAN:
            return 'New York'
        return self.borough_label

    @property
    def full_address(self) -> str:
        '''Return the full address for purposes of geolocation, etc.'''

        if not (self.borough and self.address):
            return ''
        return f"{self.address}, {self.borough_label}"

    @property
    def state(self) -> str:
        '''The two-letter abbreviation for the user's state.'''

        # For now we'll just hard-code this to New York.
        return 'NY'

    @property
    def apartment_address_line(self) -> str:
        '''The address line that specifies the user's apartment number.'''

        if self.apt_number:
            return f"Apartment {self.apt_number}"
        return ''

    @property
    def address_lines_for_mailing(self) -> List[str]:
        '''Return the full mailing address as a list of lines.'''

        result: List[str] = []
        if self.address:
            result.append(self.address)
        if self.apt_number:
            result.append(self.apartment_address_line)
        if self.borough:
            result.append(f"{self.city}, {self.state} {self.zipcode}".strip())

        return result

    @property
    def address_for_mailing(self) -> str:
        '''Return the full mailing address as a string.'''

        return '\n'.join(self.address_lines_for_mailing)

    def __str__(self):
        if not (self.created_at and self.user and self.user.full_name):
            return super().__str__()
        return (
            f"{self.user.full_name}'s onboarding info from "
            f"{self.created_at.strftime('%A, %B %d %Y')}"
        )

    def __should_lookup_new_addr_metadata(self) -> bool:
        if self.__addr.are_any_fields_blank():
            # We can't even look up address metadata without a
            # full address.
            return False

        if self.__addr_meta.are_any_fields_blank():
            # We have full address information but no
            # address metadata, so let's look it up!
            return True

        if self.__addr.has_changed() and not self.__addr_meta.has_changed():
            # The address information has changed but our address
            # metadata has not, so let's look it up again.
            return True

        return False

    def lookup_addr_metadata(self):
        features = geocoding.search(self.full_address)
        if features:
            props = features[0].properties
            self.zipcode = props.postalcode
            self.pad_bbl = props.pad_bbl
            self.pad_bin = props.pad_bin
        elif self.__addr.has_changed():
            # If the address has changed, we really don't want the existing
            # metadata to be there, because it will represent information
            # about their old address.
            self.zipcode = ''
            self.pad_bbl = ''
            self.pad_bin = ''
        self.__addr.set_to_unchanged()
        self.__addr_meta.set_to_unchanged()

    def maybe_lookup_new_addr_metadata(self) -> bool:
        if self.__should_lookup_new_addr_metadata():
            self.lookup_addr_metadata()
            return True
        return False

    def save(self, *args, **kwargs):
        self.maybe_lookup_new_addr_metadata()
        return super().save(*args, **kwargs)

    @property
    def building_links(self) -> List[Hyperlink]:
        links: List[Hyperlink] = []
        if self.pad_bbl:
            links.append(Hyperlink(
                name="Who Owns What",
                url=f"https://whoownswhat.justfix.nyc/bbl/{self.pad_bbl}"
            ))
        if self.pad_bin:
            links.append(Hyperlink(
                name="NYC DOB BIS",
                url=(f"http://a810-bisweb.nyc.gov/bisweb/PropertyProfileOverviewServlet?"
                     f"bin={self.pad_bin}&go4=+GO+&requestid=0")
            ))
        return links

    @admin_field(short_description="Building links", allow_tags=True)
    def get_building_links_html(self) -> str:
        return Hyperlink.join_admin_buttons(self.building_links)
