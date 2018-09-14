# -*- coding: utf-8 -*-


###################### Petri Net ######################

from collections import OrderedDict ## Para criar o dicionário ordenado ##
import copy ## Para copiar lista com dicionários ##

############################################

## Classe que define os lugares da Rede de Petri ##

class places():
	def __init__ (self):
		self._places = []
	
	
	def addPlace(self, lista):
		try:
			if type(lista) != list:
				raise
			
			else:
				if ((len(lista) < 2) or (len(lista) > 3)):
					raise
					
				else:
					if ((type(lista[0]) != str) or (type(lista[1]) != str)):
						raise
				
					if len(lista) == 2:
						self._places.append({'place': lista[0], 'label': lista[1], 'tokens': 0})
					
					if len(lista) == 3:
						if type(lista[2]) == int:
							self._places.append({'place': lista[0], 'label': lista[1], 'tokens': lista[2]})
						
						else:
							raise
						
		except:
			pass
			
			
	def removePlace(self, place_or_label):
		try:
			if type(place_or_label) != str:
				raise
			
			else:
				for i in self._places:
					if ((i['place'] == place_or_label) or (i['label'] == place_or_label)):
						self._places.remove(i)
						
						for j in self._pre_post:
							for k in j['pre']:							
								if i['place'] in k:
									j['pre'].remove(k)
									
							for k in j['post']:							
								if i['place'] in k:
									j['post'].remove(k)
								
						break
						
		except:
			pass
	
	
	def getPlaces(self):
		return self._places
		
	
	def sortPlaces(self):
		self._places.sort(key=lambda x: (int(x['place'][1:]))) ## Só funciona quando o nome do lugar só tem uma letra no início ##
		
		
	def orderPlaces(self):
		places.sortPlaces(self)
		
		pTemp = []
		order = ['place', 'label', 'tokens']
		
		for i in range(len(self._places)):
			pTemp.append(OrderedDict((k, self._places[i][k]) for k in order))
		
		self._places = pTemp
		
############################################

## Classe que define as transições da Rede de Petri ##
		
class transitions():
	def __init__ (self):
		self._transitions = []
	
	
	def addTransition(self, lista):
		try:
			if type(lista) != list:
				raise
			
			else:
				if ((len(lista) < 2) or (len(lista) > 3)):
					raise
					
				else:
					if ((type(lista[0]) != str) or (type(lista[1]) != str)):
						raise
				
					if len(lista) == 2:
						self._transitions.append({'transition': lista[0], 'label': lista[1], 'time': 0, 'time elapsed': 0})
					
					if len(lista) == 3:
						if ((type(lista[2]) == int) or (type(lista[2]) == float)):
							self._transitions.append({'transition': lista[0], 'label': lista[1], 'time': lista[2], 'time elapsed': 0})
						
						else:
							raise
		
		except:
			pass
	
	
	def removeTransition(self, transition_or_label):
		try:
			if type(transition_or_label) != str:
				raise
			
			else:
				for i in self._transitions:
					if ((i['transition'] == transition_or_label) or (i['label'] == transition_or_label)):
						self._transitions.remove(i)
						
						for j in self._pre_post:
							if j['transition'] == transition_or_label:
								self._pre_post.remove(j)
								
						break
							
		except:
			pass
		
		
	def getTransitions(self):
		return self._transitions	
		
		
	def sortTransitions(self):
		self._transitions.sort(key=lambda x: (int(x['transition'][1:]))) ## Só funciona quando o nome da transição só tem uma letra no início ##
		
		
	def orderTransitions(self):
		transitions.sortTransitions(self)
		
		tTemp = []
		order = ['transition', 'label', 'time', 'time elapsed']
		
		for i in range(len(self._transitions)):
			tTemp.append(OrderedDict((k, self._transitions[i][k]) for k in order))
		
		self._transitions = tTemp
	
############################################

## Classe que define o Pre e o Post da Rede de Petri ##
	
class conditions():
	def __init__ (self):
		self._pre_post = []		
		
		
	def addPre(self, transition, pre, weight):		
		try:
			if ((type(transition) != str) or (type(pre) != str) or (type(weight) != int)):
				raise
			
			else:
				find = False
				for i in self._pre_post:
					if i['transition'] == transition:
						find = True
						
						if 'pre' in i.keys():
							i['pre'].append(pre + '*' + str(weight))
						
						else:
							i['pre'] = [pre + '*' + str(weight)]
						
						break
						
				if find == False:
					self._pre_post.append({'transition': transition, 'pre': [pre + '*' + str(weight)]})
		
		except:
			pass

	
	def removePre(self, transition, pre, weight):
		try:
			if ((type(transition) != str) or (type(pre) != str) or (type(weight) != int)):
				raise
			
			else:
				for i in self._pre_post:
					if ((i['transition'] == transition) and (pre + '*' + str(weight) in i['pre'])):
						if len(i['pre']) == 1:
							i.pop('pre')
							
						else:
							i['pre'].remove(pre + '*' + str(weight))
						
						break
						
		except:
			pass
	
			
	def addPost(self, transition, post, weight):		
		try:
			if ((type(transition) != str) or (type(post) != str) or (type(weight) != int)):
				raise
			
			else:
				find = False
				for i in self._pre_post:
					if i['transition'] == transition:
						find = True
						
						if 'post' in i.keys():
							i['post'].append(post + '*' + str(weight))
						
						else:
							i['post'] = [post + '*' + str(weight)]
						
						break
						
				if find == False:
					self._pre_post.append({'transition': transition, 'post': [post + '*' + str(weight)]})
		
		except:
			pass

	
	def removePost(self, transition, post, weight):
		try:
			if ((type(transition) != str) or (type(post) != str) or (type(weight) != int)):
				raise
			
			else:
				for i in self._pre_post:
					if ((i['transition'] == transition) and (post + '*' + str(weight) in i['post'])):
						if len(i['post']) == 1:
							i.pop('post')
							
						else:
							i['post'].remove(post + '*' + str(weight))
						
						break
						
		except:
			pass
			
			
	def getPrePosts(self):
		return self._pre_post
		
		
	def sortPrePosts(self):
		for i in self._pre_post:
			if 'pre' in i.keys():
				i['pre'].sort()
				
			if 'post' in i.keys():
				i['post'].sort()
				
		self._pre_post.sort(key=lambda x: (int(x['transition'][1:]))) ## Só funciona quando o nome da transição só tem uma letra no início ##
		
		
	def orderPrePosts(self):
		conditions.sortPrePosts(self)
		
		cTemp = []
		order = ['transition', 'pre', 'post']
		
		for i in range(len(self._transitions)):
			cTemp.append(OrderedDict((k, self._pre_post[i][k]) for k in order))
		
		self._pre_post = cTemp
		
############################################

## Classe que define a dinâmica da Rede de Petri ##

class dynamic(places, transitions, conditions):
	def __init__ (self):
		self._total_time_elapsed = 0
		self.__start = True
		self._untimed_enabled_transitions = []
		self._dynamic_places = []
		self._dynamic_transitions = []
		

	def getTotalTimeElapsed(self):
		return self._total_time_elapsed	
	
	
	def avanceTimeElapsed(self):
	
		self._total_time_elapsed += 1
		
		for i in self._untimed_enabled_transitions:
			for j in self._dynamic_transitions:
				if i == j['transition']:
					j['time elapsed'] += 1
		
		self.enabledTransitions()
		
		
	def resetTotalTimeElapsed(self):
		self._total_time_elapsed = 0
	
	
	def resetDynamic(self):
		self._total_time_elapsed = 0
		self._dynamic_places = copy.deepcopy(self._places)
		self._dynamic_transitions = copy.deepcopy(self._transitions)
		self._stop = False
		
		
	def enabledTransitions(self):
		self._enabled_transitions = []
		self._untimed_enabled_transitions = []
	
		for t in self._pre_post:
			if 'pre' not in t.keys():
				self._enabled_transitions.append(t['transition'])
				
			else:
				enabled = True
			
				for pre in t['pre']: 					
					if self.__start == True:
						self.resetDynamic()
						self.__start = False
					
					for p in self._dynamic_places:					
						if p['place'] == pre[:pre.find('*')]:
							if p['tokens'] < int(pre[pre.find('*') + 1:]):
								enabled = False
								break
								
				if enabled == True:
					self._untimed_enabled_transitions.append(t['transition'])
					
					for j in self._dynamic_transitions:
						if t['transition'] == j['transition'] and j['time elapsed'] >= j['time']:
							self._enabled_transitions.append(t['transition'])
				
			
	def getEnabledTransitions(self):
		return self._enabled_transitions

	
	def sortEnabledTransitions(self):
		self._enabled_transitions.sort()
		
	
	def dynamic(self, transition):
		try:
			if transition not in self._enabled_transitions:
				print 'Transition ' + transition + ' could not be fired.'
				raise
				
			else:
				for t in self._dynamic_transitions: 
					if ((t['time elapsed'] > 0 and t['transition'] not in self._untimed_enabled_transitions) or (t['transition'] == transition)):
						t['time elapsed'] = 0

				for pp in self._pre_post:
					pp_keys = pp.keys()
					
					if pp['transition'] == transition:
						if 'pre' in pp_keys:
							for p in pp['pre']:
								for i in self._dynamic_places:
									if i['place'] == p[:p.find('*')]:
										i['tokens'] -= int(p[p.find('*') + 1:])
										break
						
						if 'post' in pp_keys:
							for p in pp['post']:
								for i in self._dynamic_places:
									if i['place'] == p[:p.find('*')]:
										i['tokens'] += int(p[p.find('*') + 1:])
										break	
				
				self.enabledTransitions()
				
		except:
			self._stop = True
			
			
	def getDynamic(self):
		return self._dynamic_places, self._dynamic_transitions
	
	
	def firingSequence(self, transitions, test = False):
		if test == True:
			
			try:
				if type(transitions) != list:
					raise
				
				self.enabledTransitions()
				
				for transition in transitions:
					
					if type(transition) != str:
						raise
					
					if self._stop == False:
						self.dynamic(transition)
					
					else:
						break	

				r.avanceTimeElapsed()
			
			except:
				pass
				
		else:
		
			for transition in transitions:
					self.enabledTransitions()
					
					if self._stop == False:
						self.dynamic(transition)
					
					else:
						break
		
			
############################################

## Classe que define a Rede de Petri ##
	
class petri_net(places, transitions, conditions, dynamic):
	def __init__ (self):
		places.__init__(self)
		transitions.__init__(self)
		conditions.__init__(self)
		dynamic.__init__(self)

	
	def addPlace(self, lista):
		places.addPlace(self, lista)
		
	
	def removePlace(self, lista):
		places.removePlace(self, lista)
	
	
	def getPlaces(self):
		return self._places
		
	
	def sortPlaces(self):
		places.sortPlaces(self)
		
	
	def orderPlaces(self):
		places.orderPlaces(self)

	
	def addTransition(self, lista):
		transitions.addTransition(self, lista)
	
	
	def removeTransition(self, lista):
		transitions.removeTransition(self, lista)
		
		
	def getTransitions(self):
		return self._transitions
	
	
	def sortTransitions(self):
		transitions.sortTransitions(self)
		
		
	def orderTransitions(self):
		transitions.orderTransitions(self)
	
	
	def addPre(self, transition, pre, weight):
		conditions.addPre(self, transition, pre, weight)
		
		
	def removePre(self, transition, pre, weight):
		conditions.removePre(self, transition, pre, weight)
		
	
	def addPost(self, transition, post, weight):
		conditions.addPost(self, transition, post, weight)	
	
	
	def removePost(self, transition, post, weight):
		conditions.removePost(self, transition, post, weight)
		
	
	def getPrePosts(self):
		return self._pre_post
		
	
	def sortPrePosts(self):
		conditions.sortPrePosts(self)
		
		
	def orderPrePosts(self):
		conditions.orderPrePosts(self)
		
		
	def getNet(self):		
		return [self._places, self._transitions, self._pre_post]
		
		
	def sortNet(self):
		petri_net.sortPlaces(self)
		petri_net.sortTransitions(self)
		petri_net.sortPrePosts(self)
		
		
	def orderNet(self):
		petri_net.orderPlaces(self)
		petri_net.orderTransitions(self)
		petri_net.orderPrePosts(self)
	
	
	def getTotalTimeElapsed(self):
		return self._total_time_elapsed
	
	
	def avanceTimeElapsed(self):
		dynamic.avanceTimeElapsed(self)	
	
	
	def resetTotalTimeElapsed(self):
		dynamic.resetTotalTimeElapsed(self)

	
	def resetDynamic(self):
		dynamic.resetDynamic(self)
	
	
	def enabledTransitions(self):
		dynamic.enabledTransitions(self)
		
		
	def getEnabledTransitions(self):
		return self._enabled_transitions
		
	
	def sortEnabledTransitions(self):
		self._enabled_transitions.sort()
		
		
	def dynamic(self, transition):
		dynamic.dynamic(self, transition)
		
		
	def getDynamic(self):
		return self._dynamic_places, self._dynamic_transitions
		
	
	def firingSequence(self, transitions):
		dynamic.firingSequence(self, transitions)
		
############################################