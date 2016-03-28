#! /usr/bin/python
#-*- coding: utf-8-*-

#Exercici 1: client ldap
# Escola del treball de Barcelona 
# ASIX Hisi2 M06­ASO UF2NF1­Scripts 
# @edt Curs 20152016  gener 2016
# Ferran Homet Puigbo
# isx47167139

#Activitat 1.­

__all__ = ["imports_objectes_parser"]

import sys
import argparse
import plantilles
from subprocess import Popen, PIPE 

# Processar els arguments amb argparse
# try/except per controlar que el fitxer existeix/es accessible
try:
	parser = argparse.ArgumentParser(description='mostrar linies d\'un fitxer')
	parser.add_argument('-f', '--file-passwd', dest='fileUsers', help='fitxer de usuaris', type=file, default='/etc/passwd')
	parser.add_argument('-g', '--file-group', dest='fileGroups', help='fitxer de grups', type=file, default='/etc/group')
	args=parser.parse_args()
except:
	sys.stderr.write("Error de lectura\n")
	sys.exit(1)

# UnixGroup
class UnixGroup():
	"Classe que defixeix un POSIX group Unix"
	def __init__(self,groupLine):
		"Constructor de grup donada una línia"
		groupFields=groupLine.split(':')
		self.gname=groupFields[0]
		self.password=groupFields[1]
		self.gid=groupFields[2]
		if groupFields[3]=='':
			self.userList=[]
		else:
			self.userList=groupFields[3].split(',') 
	def __str__(self):
		return "%15s:%5d:%s" % \
		(self.gname,int(self.gid),self.userList)

# UnixUser
class UnixUser():
	"Classe que defixeix un usuari POSIX Unix"
	def __init__(self,userLine):
		"Constructor d'usuaris donada una línia"
		userFields=userLine.split(':')
		if dicGroups.has_key(self.gid):
			self.login=userFields[0]
			self.password=userFields[1]
			self.uid=userFields[2]
			self.gid=userFields[3]
			self.gecos=userFields[4]
			self.homeDirectory=userFields[5]
			self.shell=userFields[6]
			self.gname=dicGroups[self.gid].gname
		else:
			sys.stdout.write("El usuari %s No pertany a cap grup! .. ERROR!\n" % login)
			pass
			#b) sys.stderror,info user i gname ERROR, and pass
	def __str__(self):
		return "{%s:%s:%s:%s:%s:%s:%s}" % \
		(self.login,self.uid,self.gid,self.gname,self.gecos,self.homeDirectory,self.shell)


if __name__ == '__main__':
	
	# if Eduard not feliç:
	#	sys.stderr.write('mala suerte')
	#	sys.exit(nananianonanianonaniano)
	
	# Carregar grups
	# Crear diccionari grups
	dicGroups={}
	for line in args.fileGroups:
		oneGroup=UnixGroup(line[:-1])
		dicGroups[oneGroup.gid]=oneGroup 
	args.fileGroups.close()
	
	
	fitxer = 'etc.ldif'
	# Comprobem que poguem crear el fitxer per guardar les dades
	try:
		ff = open(fitxer, 'wb')
	except:
		sys.stderr.write("Error al crear el fitxer\n")
		sys.exit(2)
	
	# Carregar usuaris
	# Crear diccionari usuaris
	# Escriure usuaris al fitxer ldif
	dicUsers={}
	for line in args.fileUsers:
		oneUser=UnixUser(line[:-1])
		dicUsers[oneUser.login]=oneUser
		user = plantilles.ADDUSER % (oneUser.login,
						  oneUser.login, 
						  oneUser.login,
						  oneUser.uid,
						  oneUser.gid,
						  oneUser.homeDirectory)
		ff.write(user)
	args.fileUsers.close()

	# Recorrem el diccionari de groups
	# Creem una llista amb els usuaris amb grup secundari
	# Guardem els groups en format ldif al fitxer
	for group in dicGroups:
		ll_membres=[]
		for login in dicGroups[group].userList:
			ll_membres.append('memberUid: %s' % (dicUsers[login].uid +'\n'))
		group = plantilles.ADDGROUP % (dicGroups[group].gname,
								dicGroups[group].gname, 
								dicGroups[group].gid,
								dicGroups[group].gname)
		ff.write(group)
	if len(ll_membres) > 0:
		for membre in ll_membres:
			ff.write(membre)
	ff.write('\n')
	ff.close()
	
	# Popen per inserir les dades al servidor LDAP
	LDAPADD = ["ldapadd", "-x","-h","localhost", "-D", "cn=Manager,dc=edt,dc=org", "-w", "jupiter", "-f", fitxer]
	pipeData = Popen(LDAPADD, stdout=PIPE, stderr=PIPE)
	sys.exit(0)

# Comentaris del professor
'''
'''
