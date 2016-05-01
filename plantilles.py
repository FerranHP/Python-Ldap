#! /usr/bin/python
#-*- coding: utf-8-*-

ADDUSER = """dn: cn=%s,ou=usuaris,dc=edt,dc=org
objectclass: posixAccount
objectclass: inetOrgPerson
cn: %s
sn: usuari
ou: usuaris
uid: %s
uidNumber: %s
gidNumber: %s
homeDirectory: %s

"""

ADDGROUP="""dn: cn=%s,ou=groups,dc=edt,dc=org
objectclass: posixGroup
objectclass: top
cn: %s
gidNumber: %s
description: Container per al grup unix %s
%s
"""


PASSWD = """%s:x:%s:%s:%s
"""
GROUP = """%s:x:%s:%s
"""
