#!/usr/bin/python
# coding: utf-8
#
#-------------------------------------------------------------------------------
# projet  : annu.py
# date    : le 11/07/2018
# version : 1.0
# Depends : modules python-ldap python-unidecode
# license : GPL-3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License
#
#-------------------------------------------------------------------------------

import argparse
import ldap
import sys
import unidecode

def printf(format, *args):
    sys.stdout.write(format % args)

#default value
ldapsrv="ldaps://ldap.domaine.fr"
ldapversion=ldap.VERSION3
ldapbase="ou=people,dc=domaine,dc=fr"

parser = argparse.ArgumentParser(description="search in directory server",epilog="le 11/07/2018")
parser.add_argument("val", help="search val in name or surname or mail")
parser.add_argument("-g", dest='group', action='store_true', help="list members in val group")
parser.add_argument("-o", help="only this ou")
args = parser.parse_args()
#initialisation
val=unicode(args.val.lower(), "utf-8")
val=unidecode.unidecode(val)
filter="cn=*"+val+"*"
if args.group:
  filter="businesscategory="+val
if args.o is not None:
  filter="(&(ou="+args.o+")("+filter+"))"
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
l=ldap.initialize(ldapsrv)
l.protocol_version = ldap.VERSION3        
try:
  users=l.search_s(ldapbase,ldap.SCOPE_SUBTREE,filter,['cn','mail','telephonenumber'])
except ldap.LDAPError, e:
  print e
  exit(1)
l.unbind_s()
try:
  for u in users:
    cn=u[1]["cn"][0]
    mail=u[1]["mail"][0]
    tel=u[1]["telephoneNumber"][0]
    printf ("%-25s %-25s %s\n",cn,tel,mail)
except Exception:
  pass
