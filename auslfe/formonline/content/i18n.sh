#!/bin/sh

DOMAIN='auslfe.formonline.content'

i18ndude rebuild-pot --pot locales/${DOMAIN}.pot --create ${DOMAIN} .
i18ndude sync --pot locales/${DOMAIN}.pot locales/*/LC_MESSAGES/${DOMAIN}.po

DOMAIN='plone'
i18ndude rebuild-pot --pot i18n/${DOMAIN}.pot --create ${DOMAIN} profiles/default/workflows
i18ndude sync --pot i18n/${DOMAIN}.pot i18n/${DOMAIN}-??.po
