# This code was generated by the "hpcodegen" Django management command.

from typing import Optional, Union, List
from decimal import Decimal
import datetime
from enum import Enum
from dataclasses import dataclass, field
from hpaction.hotdocs import AnswerSet, enum2mc, enum2mc_opt, none2unans, AnswerType


class AccessPersonMC(Enum):
    # Me
    ME = 'Me'
    # Someone else
    SOMEONE_ELSE = 'Someone else'


class ActionTypeMS(Enum):
    # Sue my landlord for repairs
    REPAIRS = 'Repairs'
    # Sue my landlord for harassment
    HARASSMENT = 'Harassment'
    # Ask the court to waive the court fee ($45)
    FEE_WAIVER = 'Fee waiver'


class CourtCountyMC(Enum):
    BRONX = 'Bronx'
    KINGS = 'Kings'
    NEW_YORK = 'New York'
    QUEENS = 'Queens'
    RICHMOND = 'Richmond'


class CourtLocationMC(Enum):
    # Bronx County
    BRONX_COUNTY = 'Bronx County'
    # Harlem Community Justice Center
    HARLEM_COMMUNITY_JUSTICE_CENTER = 'Harlem Community Justice Center'
    # Kings County
    KINGS_COUNTY = 'Kings County'
    # New York County
    NEW_YORK_COUNTY = 'New York County'
    # Queens County
    QUEENS_COUNTY = 'Queens County'
    # Richmond County
    RICHMOND_COUNTY = 'Richmond County'
    # Red Hook Community Justice Center
    RED_HOOK_COMMUNITY_JUSTICE_CENTER = 'Red Hook Community Justice Center'


class HarassmentAllegationsMS(Enum):
    # used force or said they would use force or implied the use of force
    FORCE = 'force'
    # knowingly provided false or misleading information on the current occupancy, or rent
    # stabilization status of a unit on any application or construction document for a permit for
    # work to be performed in said building
    MISLEADING_INFO = 'misleading info'
    # interrupted or stopped essential services repeatedly, or only once where a previous violation
    # in the building occurred
    STOPPED_SERVICE = 'stopped service'
    # failed to timely comply with NYC Admin. Code §27–2140[c] by failing to correct the conditions
    # which made the unit unlivable or unfit for habitation, which are described in the Vacate Order
    # issued by DHPD pursuant to NYC Admin. Code §27–2139[b], and a violation of record was issued
    # for at least one of those conditions
    FAILED_TO_COMPLY = 'failed to comply'
    # repeatedly made false certifications that a violation relating to the unit or unit building
    # has been corrected
    FALSE_CERT_REPAIRS = 'false cert repairs'
    # repeatedly engaged in conduct in the building in violation of NYC Admin. Code §28–105.1
    CONDUCT_IN_VIOLATION = 'conduct in violation'
    # repeatedly brought court cases for no good reasons
    SUED = 'sued'
    # removed tenant possessions from the unit, or removed the unit front door or made the lock to
    # the unit not work, or changed the lock on the unit door without giving a key to the new lock
    # to the tenant/petitioner
    REMOVED_POSSESSIONS = 'removed possessions'
    # offered money or valuables to tenant, or their relatives, to induce tenant to leave, or to
    # surrender or waive their rights, without written disclosure of the tenant’s rights and without
    # written permission to make an offer from court or the tenant; or, while: threatening,
    # intimidating or using obscene language; frequently harassing or communicating abusively;
    # communicating at tenant’s place of employment without prior written consent; or  knowingly
    # falsifying or misrepresenting information to ten
    INDUCED_LEAVING = 'induced leaving'
    # repeatedly contacted or visited tenant without written consent on: weekends, legal holidays,
    # outside of 9am-5pm, or in such a manner that would abuse or harass tenant
    CONTACT = 'contact'
    # threatened tenant based on their age; race; creed; color; national origin; gender; disability;
    # marital or partnership status; caregiver status; uniformed service; sexual orientation;
    # citizenship status; status as a victim of domestic violence, sex offenses, or stalking; lawful
    # source of income; or because they have children as terms are defined in NYC Admin. Codes
    # §8–102 and §8–107.1
    THREATS_RE_STATUS = 'threats re status'
    # requested identifying documentation that would disclose tenant’s citizenship status, when they
    # have already provided government-issued personal identification as such term is defined in NYC
    # Admin. Code §21–908, and when the documentation was neither required by law, nor requested for
    # any unrelated, specific, and limited purpose
    REQUESTED_ID = 'requested id'
    # repeatedly caused or permitted acts or omissions that substantially interfered with or
    # disturbed the comfort, peace, or quiet of the tenant, including requiring them to seek,
    # receive, or refrain from medical treatment in violation of NYC Admin. Code §26–1202[b].  If
    # the acts or omissions involve physical conditions in the unit or the building, a violation of
    # record was issued.
    DISTURBED = 'disturbed'


class IFPWhatOrdersMS(Enum):
    # waive any and all statutory fees for the defense or prosecution of the action
    FEES = 'fees'
    # waive the fee for filing a Notice of Appeal
    APPEAL_FEES = 'appeal fees'
    # Other
    OTHER = 'Other'


class LandlordAddressStateMC(Enum):
    ALABAMA = 'Alabama'
    ALASKA = 'Alaska'
    ARIZONA = 'Arizona'
    ARKANSAS = 'Arkansas'
    CALIFORNIA = 'California'
    COLORADO = 'Colorado'
    CONNECTICUT = 'Connecticut'
    DELAWARE = 'Delaware'
    DISTRICT_OF_COLUMBIA = 'District of Columbia'
    FLORIDA = 'Florida'
    GEORGIA = 'Georgia'
    HAWAII = 'Hawaii'
    IDAHO = 'Idaho'
    ILLINOIS = 'Illinois'
    INDIANA = 'Indiana'
    IOWA = 'Iowa'
    KANSAS = 'Kansas'
    KENTUCKY = 'Kentucky'
    LOUISIANA = 'Louisiana'
    MAINE = 'Maine'
    MARYLAND = 'Maryland'
    MASSACHUSETTS = 'Massachusetts'
    MICHIGAN = 'Michigan'
    MINNESOTA = 'Minnesota'
    MISSISSIPPI = 'Mississippi'
    MISSOURI = 'Missouri'
    MONTANA = 'Montana'
    NEBRASKA = 'Nebraska'
    NEVADA = 'Nevada'
    NEW_HAMPSHIRE = 'New Hampshire'
    NEW_JERSEY = 'New Jersey'
    NEW_MEXICO = 'New Mexico'
    NEW_YORK = 'New York'
    NORTH_CAROLINA = 'North Carolina'
    NORTH_DAKOTA = 'North Dakota'
    OHIO = 'Ohio'
    OKLAHOMA = 'Oklahoma'
    OREGON = 'Oregon'
    PENNSYLVANIA = 'Pennsylvania'
    RHODE_ISLAND = 'Rhode Island'
    SOUTH_CAROLINA = 'South Carolina'
    SOUTH_DAKOTA = 'South Dakota'
    TENNESSEE = 'Tennessee'
    TEXAS = 'Texas'
    UTAH = 'Utah'
    VERMONT = 'Vermont'
    VIRGINIA = 'Virginia'
    WASHINGTON = 'Washington'
    WEST_VIRGINIA = 'West Virginia'
    WISCONSIN = 'Wisconsin'
    WYOMING = 'Wyoming'


class LandlordEntityOrIndividualMC(Enum):
    # Individual
    INDIVIDUAL = 'Individual'
    # Company
    COMPANY = 'Company'


class PayPeriodMC(Enum):
    # week
    WEEK = 'week'
    # 2 weeks
    TWO_WEEKS = '2 weeks'
    # half-month
    HALF_MONTH = 'half-month'
    # month
    MONTH = 'month'
    # other
    OTHER = 'other'


class PriorHarassmentCaseMC(Enum):
    # Yes
    YES = 'Yes'
    # No
    NO = 'No'


class TenantBoroughMC(Enum):
    BRONX = 'Bronx'
    BROOKLYN = 'Brooklyn'
    MANHATTAN = 'Manhattan'
    QUEENS = 'Queens'
    STATEN_ISLAND = 'Staten Island'


class TenantRepairsAllegationsMC(Enum):
    # I filed a complaint with HPD. HPD issued a Notice of Violation. More than 30 days have passed
    # since then. The landlord has not fixed the problem
    NOTICE_ISSUED = 'Notice issued'
    # I filed a complaint with HPD. More than 30 days have passed since then. HPD has not issued a
    # Notice of Violation.
    NO_NOTICE_ISSUED = 'No notice issued'


class AreaComplainedOfMC(Enum):
    # My apartment
    MY_APARTMENT = 'My apartment'
    # Public area
    PUBLIC_AREA = 'Public area'


class WhichRoomMC(Enum):
    # Kitchen
    KITCHEN = 'Kitchen'
    # Bathroom
    BATHROOM = 'Bathroom'
    # Hallway
    HALLWAY = 'Hallway'
    # Living Room
    LIVING_ROOM = 'Living Room'
    # Dining Room
    DINING_ROOM = 'Dining Room'
    # Bedroom 1
    BEDROOM_1 = 'Bedroom 1'
    # Bedroom 2
    BEDROOM_2 = 'Bedroom 2'
    # Bedroom 3
    BEDROOM_3 = 'Bedroom 3'
    # Bedroom 4
    BEDROOM_4 = 'Bedroom 4'
    # Stairway
    STAIRWAY = 'Stairway'
    # Porch/Balcony
    PORCHBALCONY = 'Porch/Balcony'
    # Front Entrance
    FRONT_ENTRANCE = 'Front Entrance'
    # Lobby
    LOBBY = 'Lobby'
    # Mailbox Area
    MAILBOX_AREA = 'Mailbox Area'
    # Laundry Room
    LAUNDRY_ROOM = 'Laundry Room'
    # Yard
    YARD = 'Yard'
    # Parking Area
    PARKING_AREA = 'Parking Area'
    # Storage Room
    STORAGE_ROOM = 'Storage Room'
    # All Rooms
    ALL_ROOMS = 'All Rooms'


ManagementCompanyAddressStateMC = LandlordAddressStateMC

PriorRepairsCaseMC = PriorHarassmentCaseMC

TenantAddressStateMC = LandlordAddressStateMC


@dataclass
class TenantChild:
    # Child's full name
    tenant_child_name_te: Optional[str] = None

    # Birth date (month/date/year)
    tenant_child_dob: Optional[datetime.date] = None

    @staticmethod
    def add_to_answer_set(values: List['TenantChild'], result: AnswerSet) -> None:
        result.add('Tenant child name TE', [
            none2unans(v.tenant_child_name_te, AnswerType.TEXT)
            for v in values
        ])
        result.add('Tenant child DOB', [
            none2unans(v.tenant_child_dob, AnswerType.DATE)
            for v in values
        ])


@dataclass
class TenantComplaints:
    # Location of the problem
    area_complained_of_mc: Optional[AreaComplainedOfMC] = None

    # Which room?
    which_room_mc: Optional[WhichRoomMC] = None

    # Condition(s) -- Be specific
    conditions_complained_of_te: Optional[str] = None

    @staticmethod
    def add_to_answer_set(values: List['TenantComplaints'], result: AnswerSet) -> None:
        result.add('Area complained of MC', [
            enum2mc(none2unans(v.area_complained_of_mc, AnswerType.MC))
            for v in values
        ])
        result.add('Which room MC', [
            enum2mc(none2unans(v.which_room_mc, AnswerType.MC))
            for v in values
        ])
        result.add('Conditions complained of TE', [
            none2unans(v.conditions_complained_of_te, AnswerType.TEXT)
            for v in values
        ])


@dataclass
class HPActionVariables:
    # Full name
    access_person_te: Optional[str] = None

    # Phone
    access_person_phone_te: Optional[str] = None

    # Case/Index number, if known
    case_number_te: Optional[str] = None

    #  First, you have to complete this sentence: «.b»“My case is good and worthwhile
    # because_______”.«.be» «.i» You should fill in something like “my landlord has broken the law
    # by not making repairs to my apartment and I have evidence to show this”  or “my landlord has
    # broken the law by repeatedly harassing me.”  A simple sentence is all you need here.«.ie»
    cause_of_action_description_te: Optional[str] = None

    # Explain how the landlord or someone on the landlord's behalf has harassed you. Be as specific
    # as you can and be sure to give the date these things happened. (If you cannot remember the
    # exact date, give the month and year.)
    harassment_details_te: Optional[str] = None

    # Specify what else you want ordered regarding your application to proceed without paying court
    # fees
    ifp_other_order_te: Optional[str] = None  # noqa: E701

    # City
    landlord_address_city_te: Optional[str] = None

    # Landlord's street address
    landlord_address_street_te: Optional[str] = None

    # Zip
    landlord_address_zip_te: Optional[str] = None

    # Contact person first name
    landlord_contact_person_name_first_te: Optional[str] = None

    # Last name
    landlord_contact_person_name_last_te: Optional[str] = None

    # Name of landlord (you may wish to look this up on the HPD website to make sure you get the
    # name correct)
    landlord_entity_name_te: Optional[str] = None

    # First name
    landlord_name_first_te: Optional[str] = None

    # Last name
    landlord_name_last_te: Optional[str] = None

    # City
    management_company_address_city_te: Optional[str] = None

    # Management company's street address
    management_company_address_street_te: Optional[str] = None

    # Zip
    management_company_address_zip_te: Optional[str] = None

    # Management company name
    management_company_name_te: Optional[str] = None

    # Other pay period
    other_pay_period_te: Optional[str] = None

    # Please provide the court case number (the “index number”) and/or the date(s) of the earlier
    # case(s).«IF Action type MS = "Repairs" AND Prior repairs case MC = "Yes"»  (Please also
    # include the case number and date(s) of any case(s) you have brought in the housing court for
    # repairs.)«END IF»
    prior_relief_sought_case_numbers_and_dates_te: Optional[str] = None

    # Please complete this sentence: «.b» I have applied for a fee waiver before, but I am making
    # this application because _____________.«.be»  «.i»If your earlier application was denied, you
    # can write something like "my circumstances have changed and I cannot afford the filing fee."
    # If your earlier application was granted, you can write "my prior application was granted and I
    # cannot afford the filing fee."«.ie»
    reason_for_further_application_te: Optional[str] = None

    # Apt. No.
    tenant_address_apt_no_te: Optional[str] = None

    # City
    tenant_address_city_te: Optional[str] = None

    # Your street address
    tenant_address_street_te: Optional[str] = None

    # Zip
    tenant_address_zip_te: Optional[str] = None

    # What is the source of your income?«.i» (For example, employment, social security, pension,
    # child support, etc.  You can list more than one source.)«.ie»
    tenant_income_source_te: Optional[str] = None

    # Your first name
    tenant_name_first_te: Optional[str] = None

    # Your last name
    tenant_name_last_te: Optional[str] = None

    # Your middle name (optional)
    tenant_name_middle_te: Optional[str] = None

    # Home/cell phone
    tenant_phone_home_te: Optional[str] = None

    # Business or work phone
    tenant_phone_work_te: Optional[str] = None

    # List any major property that you own, like a car or a valuable item, and the value of that
    # property. (You can list several items in the same answer.)
    tenant_property_owned_te: Optional[str] = None

    # What floor do you live on?
    tenant_address_floor_nu: Optional[Union[int, float, Decimal]] = None

    # How many children under 6 live in the apartment where the problem is? If none, please enter 0.
    tenant_children_under_6_nu: Optional[Union[int, float, Decimal]] = None

    # What is your household income?  You can list the amount by week, 2 weeks, month, etc.  Just be
    # sure to check the box for the period you listed.
    tenant_income_nu: Optional[Union[int, float, Decimal]] = None

    # Amounts withheld from your paycheck
    tenant_monthly_exp_deductions_nu: Optional[Union[int, float, Decimal]] = None

    # School and child care required for employment
    tenant_monthly_exp_employment_nu: Optional[Union[int, float, Decimal]] = None

    # Food and household supplies
    tenant_monthly_exp_food_etc_nu: Optional[Union[int, float, Decimal]] = None

    # Rent/house payment and maintenance
    tenant_monthly_exp_housing_nu: Optional[Union[int, float, Decimal]] = None

    # Insurance (life, health, accident)
    tenant_monthly_exp_insurance_nu: Optional[Union[int, float, Decimal]] = None

    # Laundry and cleaning
    tenant_monthly_exp_laundry_nu: Optional[Union[int, float, Decimal]] = None

    # Medical and dental payments
    tenant_monthly_exp_medical_nu: Optional[Union[int, float, Decimal]] = None

    # Total of other monthly expenses (clothing, housing supplies, hygiene, etc.)
    tenant_monthly_exp_other_nu: Optional[Union[int, float, Decimal]] = None

    # Court-ordered child or spousal support
    tenant_monthly_exp_support_nu: Optional[Union[int, float, Decimal]] = None

    # Transportation and auto expenses (insurance, gas, repairs, etc.)
    tenant_monthly_exp_transportation_nu: Optional[Union[int, float, Decimal]] = None

    # Utilities and telephone
    tenant_monthly_exp_utilities_nu: Optional[Union[int, float, Decimal]] = None

    # Rent
    tenant_monthly_rent_nu: Optional[Union[int, float, Decimal]] = None

    # «.i»The judge could fine your landlord, though they do not always do that.«.ie»«.b» Do you
    # want the judge to fine your landlord?«.be»
    fine_landlord_harassment_tf: Optional[bool] = None

    flag_tf: Optional[bool] = None

    harassment_conduct_in_violation_tf: Optional[bool] = None

    harassment_contact_tf: Optional[bool] = None

    harassment_disturbed_tf: Optional[bool] = None

    harassment_failed_to_comply_tf: Optional[bool] = None

    harassment_false_cert_repairs_tf: Optional[bool] = None

    harassment_force_tf: Optional[bool] = None

    harassment_induced_leaving_tf: Optional[bool] = None

    harassment_misleading_info_tf: Optional[bool] = None

    harassment_removed_possessions_tf: Optional[bool] = None

    harassment_requested_id_tf: Optional[bool] = None

    harassment_stopped_service_tf: Optional[bool] = None

    harassment_sued_tf: Optional[bool] = None

    harassment_threats_re_status_tf: Optional[bool] = None

    # Is there a management company or managing agent for the landlord that you also want to sue?
    management_company_to_be_sued_tf: Optional[bool] = None

    # Are there more than two apartments in your building?
    more_than_2_apartments_in_building_tf: Optional[bool] = None

    # Is there more than one family living in each apartment?
    more_than_one_family_per_apartment_tf: Optional[bool] = None

    # Have you asked the court to waive the court fee before in another case?
    previous_application_tf: Optional[bool] = None

    # «.b»Are the conditions urgent and dangerous?«.be»«.i» If the problems in your apartment are
    # urgent and dangerous to you or your family’s health or safety, you can ask the court to go
    # forward without a city inspection.  This means that the City will not send someone to inspect
    # the apartment. The City inspection report could be useful evidence in your case. Is the
    # problem urgent, and do you want to skip the inspection?«.ie»
    problem_is_urgent_tf: Optional[bool] = None

    # Ask the court to waive the court fee ($45)
    request_fee_waiver_tf: Optional[bool] = None

    # Sue my landlord for harassment
    sue_for_harassment_tf: Optional[bool] = None

    # Sue my landlord for repairs
    sue_for_repairs_tf: Optional[bool] = None

    # Do you receive public assistance benefits, such as cash benefits, rent assistance, food stamps
    # or Medicaid?
    tenant_receives_public_assistance_tf: Optional[bool] = None

    # Do you want to serve the papers yourself?
    tenant_wants_to_serve_tf: Optional[bool] = None

    # not asked - passed from JustFix.nyc
    user_is_nycha_tf: Optional[bool] = None

    # Who will be home to let the City housing inspector in?
    access_person_mc: Optional[AccessPersonMC] = None

    # «.b»What would you like to do?«.be»  (Choose all that apply.)
    action_type_ms: Optional[List[ActionTypeMS]] = None

    # In what jurisdiction/county will you be filing?
    court_county_mc: Optional[CourtCountyMC] = None

    # Which Court will you be filing in?
    court_location_mc: Optional[CourtLocationMC] = None

    # «.i»Choose any of the following that have happened.«.ie» The landlord, or someone acting on
    # the landlord’s behalf, has:
    harassment_allegations_ms: Optional[List[HarassmentAllegationsMS]] = None

    # What do you want the Court to order?
    ifp_what_orders_ms: Optional[List[IFPWhatOrdersMS]] = None  # noqa: E701

    # State
    landlord_address_state_mc: Optional[LandlordAddressStateMC] = None

    # Is your landlord an individual or a company?
    landlord_entity_or_individual_mc: Optional[LandlordEntityOrIndividualMC] = None

    # State
    management_company_address_state_mc: Optional[ManagementCompanyAddressStateMC] = None

    # In what period?
    pay_period_mc: Optional[PayPeriodMC] = None

    # Have you brought a case in housing court against this landlord for harassment before this
    # case?
    prior_harassment_case_mc: Optional[PriorHarassmentCaseMC] = None

    # Have you brought a case in housing court to get repairs to this apartment or building before
    # this case?
    prior_repairs_case_mc: Optional[PriorRepairsCaseMC] = None

    # State
    tenant_address_state_mc: Optional[TenantAddressStateMC] = None

    # Borough
    tenant_borough_mc: Optional[TenantBoroughMC] = None

    # Have you made a complaint to the City’s Department of Housing Preservation and Development
    # (HPD)? «.i» It is not required, but check the box if you have.)«.ie»  To find out whether HPD
    # issued a Notice of Violation, go to HPD's website: «.w
    # "http://www1.nyc.gov/site/hpd/about/hpdonline.page"»HPDONLINE«.we».  If you do not know how to
    # answer this question, you can skip it.
    tenant_repairs_allegations_mc: Optional[TenantRepairsAllegationsMC] = None

    tenant_child_list: List[TenantChild] = field(default_factory=list)

    tenant_complaints_list: List[TenantComplaints] = field(default_factory=list)

    def to_answer_set(self) -> AnswerSet:
        result = AnswerSet()
        result.add_opt('Access person TE',
                       self.access_person_te)
        result.add_opt('Access person phone TE',
                       self.access_person_phone_te)
        result.add_opt('Case number TE',
                       self.case_number_te)
        result.add_opt('Cause of action description TE',
                       self.cause_of_action_description_te)
        result.add_opt('Harassment details TE',
                       self.harassment_details_te)
        result.add_opt('IFP other order TE',
                       self.ifp_other_order_te)
        result.add_opt('Landlord address city TE',
                       self.landlord_address_city_te)
        result.add_opt('Landlord address street TE',
                       self.landlord_address_street_te)
        result.add_opt('Landlord address zip TE',
                       self.landlord_address_zip_te)
        result.add_opt('Landlord contact person name first TE',
                       self.landlord_contact_person_name_first_te)
        result.add_opt('Landlord contact person name last TE',
                       self.landlord_contact_person_name_last_te)
        result.add_opt('Landlord entity name TE',
                       self.landlord_entity_name_te)
        result.add_opt('Landlord name first TE',
                       self.landlord_name_first_te)
        result.add_opt('Landlord name last TE',
                       self.landlord_name_last_te)
        result.add_opt('Management company address city TE',
                       self.management_company_address_city_te)
        result.add_opt('Management company address street TE',
                       self.management_company_address_street_te)
        result.add_opt('Management company address zip TE',
                       self.management_company_address_zip_te)
        result.add_opt('Management company name TE',
                       self.management_company_name_te)
        result.add_opt('Other pay period TE',
                       self.other_pay_period_te)
        result.add_opt('Prior relief sought case numbers and dates TE',
                       self.prior_relief_sought_case_numbers_and_dates_te)
        result.add_opt('Reason for further application TE',
                       self.reason_for_further_application_te)
        result.add_opt('Tenant address apt no TE',
                       self.tenant_address_apt_no_te)
        result.add_opt('Tenant address city TE',
                       self.tenant_address_city_te)
        result.add_opt('Tenant address street TE',
                       self.tenant_address_street_te)
        result.add_opt('Tenant address zip TE',
                       self.tenant_address_zip_te)
        result.add_opt('Tenant income source TE',
                       self.tenant_income_source_te)
        result.add_opt('Tenant name first TE',
                       self.tenant_name_first_te)
        result.add_opt('Tenant name last TE',
                       self.tenant_name_last_te)
        result.add_opt('Tenant name middle TE',
                       self.tenant_name_middle_te)
        result.add_opt('Tenant phone home TE',
                       self.tenant_phone_home_te)
        result.add_opt('Tenant phone work TE',
                       self.tenant_phone_work_te)
        result.add_opt('Tenant property owned TE',
                       self.tenant_property_owned_te)
        result.add_opt('Tenant address floor NU',
                       self.tenant_address_floor_nu)
        result.add_opt('Tenant children under 6 NU',
                       self.tenant_children_under_6_nu)
        result.add_opt('Tenant income NU',
                       self.tenant_income_nu)
        result.add_opt('Tenant monthly exp deductions NU',
                       self.tenant_monthly_exp_deductions_nu)
        result.add_opt('Tenant monthly exp employment NU',
                       self.tenant_monthly_exp_employment_nu)
        result.add_opt('Tenant monthly exp food etc NU',
                       self.tenant_monthly_exp_food_etc_nu)
        result.add_opt('Tenant monthly exp housing NU',
                       self.tenant_monthly_exp_housing_nu)
        result.add_opt('Tenant monthly exp insurance NU',
                       self.tenant_monthly_exp_insurance_nu)
        result.add_opt('Tenant monthly exp laundry NU',
                       self.tenant_monthly_exp_laundry_nu)
        result.add_opt('Tenant monthly exp medical NU',
                       self.tenant_monthly_exp_medical_nu)
        result.add_opt('Tenant monthly exp other NU',
                       self.tenant_monthly_exp_other_nu)
        result.add_opt('Tenant monthly exp support NU',
                       self.tenant_monthly_exp_support_nu)
        result.add_opt('Tenant monthly exp transportation NU',
                       self.tenant_monthly_exp_transportation_nu)
        result.add_opt('Tenant monthly exp utilities NU',
                       self.tenant_monthly_exp_utilities_nu)
        result.add_opt('Tenant monthly rent NU',
                       self.tenant_monthly_rent_nu)
        result.add_opt('Fine landlord harassment TF',
                       self.fine_landlord_harassment_tf)
        result.add_opt('Flag TF',
                       self.flag_tf)
        result.add_opt('Harassment conduct in violation TF',
                       self.harassment_conduct_in_violation_tf)
        result.add_opt('Harassment contact TF',
                       self.harassment_contact_tf)
        result.add_opt('Harassment disturbed TF',
                       self.harassment_disturbed_tf)
        result.add_opt('Harassment failed to comply TF',
                       self.harassment_failed_to_comply_tf)
        result.add_opt('Harassment false cert repairs TF',
                       self.harassment_false_cert_repairs_tf)
        result.add_opt('Harassment force TF',
                       self.harassment_force_tf)
        result.add_opt('Harassment induced leaving TF',
                       self.harassment_induced_leaving_tf)
        result.add_opt('Harassment misleading info TF',
                       self.harassment_misleading_info_tf)
        result.add_opt('Harassment removed possessions TF',
                       self.harassment_removed_possessions_tf)
        result.add_opt('Harassment requested id TF',
                       self.harassment_requested_id_tf)
        result.add_opt('Harassment stopped service TF',
                       self.harassment_stopped_service_tf)
        result.add_opt('Harassment sued TF',
                       self.harassment_sued_tf)
        result.add_opt('Harassment threats re status TF',
                       self.harassment_threats_re_status_tf)
        result.add_opt('Management company to be sued TF',
                       self.management_company_to_be_sued_tf)
        result.add_opt('More than 2 apartments in building TF',
                       self.more_than_2_apartments_in_building_tf)
        result.add_opt('More than one family per apartment TF',
                       self.more_than_one_family_per_apartment_tf)
        result.add_opt('Previous application TF',
                       self.previous_application_tf)
        result.add_opt('Problem is urgent TF',
                       self.problem_is_urgent_tf)
        result.add_opt('Request fee waiver TF',
                       self.request_fee_waiver_tf)
        result.add_opt('Sue for harassment TF',
                       self.sue_for_harassment_tf)
        result.add_opt('Sue for repairs TF',
                       self.sue_for_repairs_tf)
        result.add_opt('Tenant receives public assistance TF',
                       self.tenant_receives_public_assistance_tf)
        result.add_opt('Tenant wants to serve TF',
                       self.tenant_wants_to_serve_tf)
        result.add_opt('user_is_NYCHA_tf',
                       self.user_is_nycha_tf)
        result.add_opt('Access person MC',
                       enum2mc_opt(self.access_person_mc))
        result.add_opt('Action type MS',
                       enum2mc_opt(self.action_type_ms))
        result.add_opt('Court county MC',
                       enum2mc_opt(self.court_county_mc))
        result.add_opt('Court location MC',
                       enum2mc_opt(self.court_location_mc))
        result.add_opt('Harassment allegations MS',
                       enum2mc_opt(self.harassment_allegations_ms))
        result.add_opt('IFP what orders MS',
                       enum2mc_opt(self.ifp_what_orders_ms))
        result.add_opt('Landlord address state MC',
                       enum2mc_opt(self.landlord_address_state_mc))
        result.add_opt('Landlord entity or individual MC',
                       enum2mc_opt(self.landlord_entity_or_individual_mc))
        result.add_opt('Management company address state MC',
                       enum2mc_opt(self.management_company_address_state_mc))
        result.add_opt('Pay period MC',
                       enum2mc_opt(self.pay_period_mc))
        result.add_opt('Prior harassment case MC',
                       enum2mc_opt(self.prior_harassment_case_mc))
        result.add_opt('Prior repairs case MC',
                       enum2mc_opt(self.prior_repairs_case_mc))
        result.add_opt('Tenant address state MC',
                       enum2mc_opt(self.tenant_address_state_mc))
        result.add_opt('Tenant borough MC',
                       enum2mc_opt(self.tenant_borough_mc))
        result.add_opt('Tenant repairs allegations MC',
                       enum2mc_opt(self.tenant_repairs_allegations_mc))
        if self.tenant_child_list:
            TenantChild.add_to_answer_set(self.tenant_child_list, result)
        if self.tenant_complaints_list:
            TenantComplaints.add_to_answer_set(self.tenant_complaints_list, result)
        return result
