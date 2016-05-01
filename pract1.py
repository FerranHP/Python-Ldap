#! /usr/bin/python
#-*- coding: utf-8-*-

#Exercici 1: client ldap
# Escola del treball de Barcelona 
# ASIX Hisi2 M06­ASO UF2NF1­Scripts 
# @edt Curs 20152016  abril 2016
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
		if groupLine[-1] == '\n':
			groupLine = groupLine[:-1]
		groupFields=groupLine.split(':')
		self.gname=groupFields[0]
		self.password=groupFields[1]
		self.gid=groupFields[2]
		# Comprovar si hi ha usuaris amb el grup secundari
		if groupFields[3]=='':
			# si no en te, deixem la llista buida
			self.userList=[]
		# Sino, inserim els usuaris
		else:
			# Treure \n del final de linia
			if groupFields[3][-1] == '\n':
				groupFields[3] = groupFields[3][:-1]
			self.userList=groupFields[3].split(',') 
	def __str__(self):
		return "%15s:%5d:%s" % \
		(self.gname,int(self.gid),self.userList)

# UnixUser
class UnixUser():
	"Classe que defixeix un usuari POSIX Unix"
	def __init__(self,userLine):
		userFields=userLine.split(':')
		self.login=userFields[0]
		self.password=userFields[1]
		self.uid=userFields[2]
		self.gid=userFields[3]
		self.gecos=userFields[4]
		self.homeDirectory=userFields[5]
		self.shell=userFields[6]
		# Comprobar que existeixi el grup del usuari
		if dicGroups.has_key(self.gid):
			self.gname=dicGroups[self.gid].gname
		else:
			print 'Grup inexistent: %s' % (self.gid)
	def __str__(self):
		return "{%s:%s:%s:%s:%s:%s:%s}" % \
		(self.login,self.uid,self.gid,self.gname,self.gecos,self.homeDirectory,self.shell)


if __name__ == '__main__':
	
	# if Eduard not feliç:
	#	sys.stderr.write('mala suerte')
	#	sys.exit(nananianonanianonaniano)
	
	fitxer = 'etc.ldif'
	# Comprobem que poguem crear el fitxer per guardar les dades
	try:
		ff = open(fitxer, 'wb')
	except:
		sys.stderr.write("Error al crear el fitxer\n")
		sys.exit(2)
	
	# Carregar grups
	# Crear diccionari grups
	dicGroups={}
	for line in args.fileGroups:
		oneGroup=UnixGroup(line[:-1])
		dicGroups[oneGroup.gid]=oneGroup 
	args.fileGroups.close()
	
	
	# Carregar usuaris
	# Crear diccionari usuaris
	# Escriure usuaris al fitxer ldif
	dicUsers={}
	for line in args.fileUsers:
		oneUser=UnixUser(line[:-1])
		dicUsers[oneUser.login]=oneUser
		# Comprovar que existeixi el grup principal del usuari
		if oneUser.gid in dicGroups:
			# Afegir a la llista d'usuaris, aquells que el tinguin com a principal	
			if oneUser.login not in dicGroups[oneUser.gid].userList
				# Afegir a la llista d'usuaris del grup principal el login de l'usuari
				oneUser.gid.userList.append(oneUser.login)
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
		memberin = ''
		for login in dicGroups[group].userList:
			memberin += 'memberUid: %s\n' % (login)
		group = plantilles.ADDGROUP % (dicGroups[group].gname,
								dicGroups[group].gname, 
								dicGroups[group].gid,
								dicGroups[group].gname,
								memberin)
		ff.write(group)
	ff.write('\n')
	ff.close()
	try:
		# Popen per inserir les dades al servidor LDAP
		LDAPADD = ["ldapadd", "-x","-h","localhost", "-D", "cn=Manager,dc=edt,dc=org", "-w", "jupiter", "-f", fitxer]
		pipeData = Popen(LDAPADD, stdout=PIPE, stderr=PIPE)
	except:
		sys.exit(3)
	sys.exit(0)
	
# Comentaris del professor
'''
'''
