# This Dockerfile is common to both production and development.

FROM python:3.7.0

ENV NODE_VERSION=10

RUN curl -sL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash - \
  && curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash - \
  && curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
  && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
  && apt-get update \
  && apt-get install -y \
    nodejs \
    yarn \
    # Install the CLIs for databases so we can use 'manage.py dbshell'.
    postgresql-client \
    # Add support for GeoDjango.
    binutils \
    libproj-dev \
    gdal-bin \
    # This is for CircleCI.
    ca-certificates \
    git-lfs \
    # These are for WeasyPrint.
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info \
  && rm -rf /var/lib/apt/lists/* \
  && pip install pipenv

ENV PATH /tenants2/node_modules/.bin:/node_modules/.bin:$PATH
