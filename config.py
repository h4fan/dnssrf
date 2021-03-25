# -*- coding: utf-8 -*-


ACME_challenge_DOMAIN = ""
ACME_challenge_TXT_Record = ""

SERVER_IP = ""
API_TOKEN = ""


API_DOMAIN_PREFIX = ""

DNSLOG_Root_Domain = ""

REBIND_DOMAIN = "reb"+DNSLOG_Root_Domain+"."

REBIND_DOMAIN_VALUE = (SERVER_IP, "127.0.0.1")

REDIRECT_30x_Check = "/302_redirect_here"

REDIRECT_30x_Code = 302
REDIRECT_30x_Value = "http://127.0.0.1/"

