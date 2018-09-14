# -*- coding: utf-8 -*-


###################### Net ######################

from Petri_Net import petri_net ## Importa a classe petri_net do arquivo Petri_Net.py ##

############################################

net = petri_net()

with open('CIM_Timed_Model.ndr', mode = 'r') as rede:
	for line in rede:
	
		if 't ' in line[:2]: # Transições
			l = line.split(' ')
			net.addTransition([l[3], l[8], int(l[5])])
			
		if 'p ' in line[:2]: # Lugares
			l = line.split(' ')
			net.addPlace([l[3], l[6], int(l[4])])
			
		if 'e ' in line[:2]:
			l = line.split(' ')
			
			if 'p' in l[1][:2]: # Pre
				c=net.getPrePosts()
				net.addPre(l[2], l[1], int(l[3]))
			
			if 't' in l[1][:2]: # Post
				net.addPost(l[1], l[2], int(l[3]))	

############################################