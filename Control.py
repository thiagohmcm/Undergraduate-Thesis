# -*- coding: utf-8 -*-


###################### Controle ######################

## Seleciona as transições que devem disparar para produzir as peças simulando uma produção real ##

def producao_pecas(net, quantidade_producao): # Para a rede do CIM modelada, essa função faz a produção das peças
	
	r = net	# Define a rede a ser trabalhada
	r.sortNet() # Ordena a rede	
	
	places = r.getPlaces()
	transitions = r.getTransitions()

	r.enabledTransitions() # Verifica as transições habilitadas na condição inicial da rede 
	transicoes_habilitadas = r.getEnabledTransitions() # Transições que estão habilitadas no início

	quantidade_pecas_a_serem_produzidas = quantidade_producao # Decido quantas peças quero produzir
	quantidade_de_pecas_produzidas = places[42]['tokens'] # Quantidade de peças produzidas, porque agora vou supor sem falha
	# Mas com falha seria só somar todos os lugares possíveis peças prontas (sejam com falha ou não)

	situacao_pallets = []

	for i in range(1, 15):
		d = {}
		d['pallet'] = i
		d['localizacao'] = 'E2E1' # Do Torno para o ASRS
		d['template'] = 0 # Sem template nenhum, ou seja, vazio
		d['situacao do template'] = 0 # Sem template nenhum, ou seja, vazio
		situacao_pallets.append(d)
		
	pallet_E1 = 0 # E1 começa sem pallet 
	pallet_E2 = 0 # E2 começa sem pallet

	pallet_E1E2 = 0 # Pallet que acabou de sair da E1 para a E2
	pallet_E2E1 = 0 # Pallet que acabou de sair da E1 para a E2

	template_buffer_torno = [] # Template que está no buffer do torno
	
	fila_pecas_producao = [i for i in range(1, quantidade_producao + 1)] # Fila de peças a serem produzidas
	fila_pecas_armazenar = [i for i in range(1, quantidade_producao + 1)] # Fila de peças a serem armazenadas
	
	
	while quantidade_de_pecas_produzidas < quantidade_pecas_a_serem_produzidas: # Enquanto todas as peças não forem produzidas...
		
		## Estação 1 - ASRS ##
		
		if 't1' in transicoes_habilitadas or 't3' in transicoes_habilitadas or 't5' in transicoes_habilitadas or 't44' in transicoes_habilitadas: # Quando E1 recebe um pallet

			if pallet_E1 < 14:
				pallet_E1 += 1 # A numeração é sempre em sequência, visto que os pallets começam alinhados e essa ordem não é alterada em nenhuma configuração do sistema
				
			else: # Caso o pallet seja o 14, é necessário voltar para o pallet 1, uma vez que só há 14 pallets
				pallet_E1 = 1

			situacao_pallets[pallet_E1 - 1]['localizacao'] = 'E1' # O pallet está na E1

			if situacao_pallets[pallet_E1 - 1]['template'] == 0: # Chegou um pallet vazio
			
				if 't1' in transicoes_habilitadas:
					transicoes_habilitadas.remove('t1') # Template com peça bruta
					
				if 't5' in transicoes_habilitadas:
					transicoes_habilitadas.remove('t5') # Template com peça pronta
			
			elif situacao_pallets[pallet_E1 - 1]['situacao do template'] == 'peca bruta': # Chegou um pallet com peça bruta
				
				if 't5' in transicoes_habilitadas:
					transicoes_habilitadas.remove('t5') # Template com peça pronta
					
				if 't44' in transicoes_habilitadas:
					transicoes_habilitadas.remove('t44') # Pallet vazio
					
			elif situacao_pallets[pallet_E1 - 1]['situacao do template'] == 'peca pronta': # Chegou um pallet com peça pronta
			
				if 't1' in transicoes_habilitadas:
					transicoes_habilitadas.remove('t1') # Template com peça bruta
					
				if 't44' in transicoes_habilitadas:
					transicoes_habilitadas.remove('t44') # Pallet vazio
			
			if 't3' in transicoes_habilitadas: # Não tem template vazio chegando
				transicoes_habilitadas.remove('t3') # Template vazio
		

		quantidade_de_pecas_brutas_utilizadas = 6 - (places[45]['tokens'] + places[53]['tokens'] + places[61]['tokens'] + places[69]['tokens'] + places[77]['tokens'] + places[85]['tokens'])

		if 't46' in transicoes_habilitadas: # Peça bruta do template 1

			if quantidade_de_pecas_brutas_utilizadas < quantidade_pecas_a_serem_produzidas:
				transicoes_habilitadas.remove('t45') # Se tem peça bruta para ser entregue, o pallet nunca é dispensado

			else:		
				transicoes_habilitadas.remove('t46') # Se não tem peça bruta para ser entregue, então liberar o pallet

		elif 't52' in transicoes_habilitadas: # Peça bruta do template 2. Só ocorre se a peça bruta do template 1 já estiver na esteira.

			if quantidade_de_pecas_brutas_utilizadas < quantidade_pecas_a_serem_produzidas:
				transicoes_habilitadas.remove('t45') # Se tem peça bruta para ser entregue, o pallet nunca é dispensado

			else:		
				transicoes_habilitadas.remove('t52') # Se não tem peça bruta para ser entregue, então liberar o pallet
				
		elif 't58' in transicoes_habilitadas: # Peça bruta do template 3. Só ocorre se a peça bruta do template 1 e 2 já estiverem na esteira.

			if quantidade_de_pecas_brutas_utilizadas < quantidade_pecas_a_serem_produzidas:
				transicoes_habilitadas.remove('t45') # Se tem peça bruta para ser entregue, o pallet nunca é dispensado

			else:		
				transicoes_habilitadas.remove('t58') # Se não tem peça bruta para ser entregue, então liberar o pallet
				
		elif 't64' in transicoes_habilitadas: # Peça bruta do template 4. Só ocorre se a peça bruta do template 1, 2 e 3 já estiverem na esteira.

			if quantidade_de_pecas_brutas_utilizadas < quantidade_pecas_a_serem_produzidas:
				transicoes_habilitadas.remove('t45') # Se tem peça bruta para ser entregue, o pallet nunca é dispensado

			else:		
				transicoes_habilitadas.remove('t64') # Se não tem peça bruta para ser entregue, então liberar o pallet
				
		elif 't70' in transicoes_habilitadas: # Peça bruta do template 5. Só ocorre se a peça bruta do template 1, 2, 3 e 4 já estiverem na esteira.

			if quantidade_de_pecas_brutas_utilizadas < quantidade_pecas_a_serem_produzidas:
				transicoes_habilitadas.remove('t45') # Se tem peça bruta para ser entregue, o pallet nunca é dispensado

			else:		
				transicoes_habilitadas.remove('t70') # Se não tem peça bruta para ser entregue, então liberar o pallet
				
		elif 't76' in transicoes_habilitadas: # Peça bruta do template 6. Só ocorre se a peça bruta do template 1, 2, 3, 4 e 5 já estiverem na esteira.

			if quantidade_de_pecas_brutas_utilizadas < quantidade_pecas_a_serem_produzidas:
				transicoes_habilitadas.remove('t45') # Se tem peça bruta para ser entregue, o pallet nunca é dispensado

			else:		
				transicoes_habilitadas.remove('t76') # Se não tem peça bruta para ser entregue, então liberar o pallet


		if 't48' in transicoes_habilitadas: # A peça bruta 1 sempre é correta e nunca é rejeitada
		
			transicoes_habilitadas.remove('t48')
			situacao_pallets[pallet_E1 - 1]['template'] = 1 # Aqui a transição t48 será a habilitada e assim o pallet terá o template 1 
			situacao_pallets[pallet_E1 - 1]['situacao do template'] = 'peca bruta' # Como a peça bruta será retirada do ASRS, a configuração do pallet deve ser atualizada	
			
		if 't54' in transicoes_habilitadas: # A peça bruta 2 sempre é correta e nunca é rejeitada
		
			transicoes_habilitadas.remove('t54')
			situacao_pallets[pallet_E1 - 1]['template'] = 2 # Aqui a transição t54 será a habilitada e assim o pallet terá o template 2
			situacao_pallets[pallet_E1 - 1]['situacao do template'] = 'peca bruta' # Como a peça bruta será retirada do ASRS, a configuração do pallet deve ser atualizada	

		if 't60' in transicoes_habilitadas: # A peça bruta 3 sempre é correta e nunca é rejeitada
		
			transicoes_habilitadas.remove('t60')
			situacao_pallets[pallet_E1 - 1]['template'] = 3 # Aqui a transição t60 será a habilitada e assim o pallet terá o template 3
			situacao_pallets[pallet_E1 - 1]['situacao do template'] = 'peca bruta' # Como a peça bruta será retirada do ASRS, a configuração do pallet deve ser atualizada	
			
		if 't66' in transicoes_habilitadas: # A peça bruta 4 sempre é correta e nunca é rejeitada
		
			transicoes_habilitadas.remove('t66')
			situacao_pallets[pallet_E1 - 1]['template'] = 4 # Aqui a transição t66 será a habilitada e assim o pallet terá o template 4
			situacao_pallets[pallet_E1 - 1]['situacao do template'] = 'peca bruta' # Como a peça bruta será retirada do ASRS, a configuração do pallet deve ser atualizada	
			
		if 't72' in transicoes_habilitadas: # A peça bruta 5 sempre é correta e nunca é rejeitada
		
			transicoes_habilitadas.remove('t72')
			situacao_pallets[pallet_E1 - 1]['template'] = 5 # Aqui a transição t72 será a habilitada e assim o pallet terá o template 5
			situacao_pallets[pallet_E1 - 1]['situacao do template'] = 'peca bruta' # Como a peça bruta será retirada do ASRS, a configuração do pallet deve ser atualizada	
			
		if 't78' in transicoes_habilitadas: # A peça bruta 6 sempre é correta e nunca é rejeitada
		
			transicoes_habilitadas.remove('t78')	
			situacao_pallets[pallet_E1 - 1]['template'] = 6 # Aqui a transição t78 será a habilitada e assim o pallet terá o template 6
			situacao_pallets[pallet_E1 - 1]['situacao do template'] = 'peca bruta' # Como a peça bruta será retirada do ASRS, a configuração do pallet deve ser atualizada	
		
		
		if places[3]['tokens'] == 1: # Se p4 tem uma ficha, ou seja, se chegou um pallet na E1 para ter o seu template devolvido

			if 't8' in transicoes_habilitadas and situacao_pallets[pallet_E1 - 1]['template'] != 1 and fila_pecas_armazenar[0] != 1: # Se não for o template 1
				transicoes_habilitadas.remove('t8')
			
			if 't14' in transicoes_habilitadas and situacao_pallets[pallet_E1 - 1]['template'] != 2 and fila_pecas_armazenar[0] != 2: # Se não for o template 2
				transicoes_habilitadas.remove('t14')
			
			if 't20' in transicoes_habilitadas and situacao_pallets[pallet_E1 - 1]['template'] != 3 and fila_pecas_armazenar[0] != 3: # Se não for o template 3
				transicoes_habilitadas.remove('t20')
			
			if 't26' in transicoes_habilitadas and situacao_pallets[pallet_E1 - 1]['template'] != 4 and fila_pecas_armazenar[0] != 4: # Se não for o template 4
				transicoes_habilitadas.remove('t26')
			
			if 't32' in transicoes_habilitadas and situacao_pallets[pallet_E1 - 1]['template'] != 5 and fila_pecas_armazenar[0] != 5: # Se não for o template 5
				transicoes_habilitadas.remove('t32')
			
			if 't38' in transicoes_habilitadas and situacao_pallets[pallet_E1 - 1]['template'] != 6 and fila_pecas_armazenar[0] != 6: # Se não for o template 6
				transicoes_habilitadas.remove('t38')
		
		
		if 't12' in transicoes_habilitadas: # Não tem falha no sistema, logo não tem peça com falha para ser armazenada
			transicoes_habilitadas.remove('t12')
		
		if 't18' in transicoes_habilitadas: # Não tem falha no sistema, logo não tem peça com falha para ser armazenada
			transicoes_habilitadas.remove('t18')
			
		if 't24' in transicoes_habilitadas: # Não tem falha no sistema, logo não tem peça com falha para ser armazenada
			transicoes_habilitadas.remove('t24')
			
		if 't30' in transicoes_habilitadas: # Não tem falha no sistema, logo não tem peça com falha para ser armazenada
			transicoes_habilitadas.remove('t30')
			
		if 't36' in transicoes_habilitadas: # Não tem falha no sistema, logo não tem peça com falha para ser armazenada
			transicoes_habilitadas.remove('t36')
			
		if 't42' in transicoes_habilitadas: # Não tem falha no sistema, logo não tem peça com falha para ser armazenada
			transicoes_habilitadas.remove('t42')
		
		
		if 't11' in transicoes_habilitadas or 't17' in transicoes_habilitadas or 't23' in transicoes_habilitadas or 't29' in transicoes_habilitadas or 't35' in transicoes_habilitadas or 't41' in transicoes_habilitadas: # Uma peça pronta acaba de ser armazenada

			fila_pecas_armazenar = fila_pecas_armazenar[1: ] # A peça já foi armazenada, então remover da fila


		if ('t6' in transicoes_habilitadas) and ('t8' in transicoes_habilitadas or 't14' in transicoes_habilitadas or 't20' in transicoes_habilitadas or 't26' in transicoes_habilitadas or 't32' in transicoes_habilitadas or 't38' in transicoes_habilitadas): # A peça pronta só é liberada se não for a vez dela na fila
			transicoes_habilitadas.remove('t6')
		
		
		if 't2' in transicoes_habilitadas or 't4' in transicoes_habilitadas or 't6' in transicoes_habilitadas or 't45' in transicoes_habilitadas: # O pallet está sendo devolvido para a esteira, saindo da E1 e indo para a E2
		
			if pallet_E1E2 < 14:
				pallet_E1E2 += 1 # A numeração é sempre em sequência, visto que os pallets começam alinhados e essa ordem não é alterada em nenhuma configuração do sistema
				
			else:
				pallet_E1E2 = 1 # Caso o pallet seja o 14, é necessário voltar para o pallet 1, uma vez que só há 14 pallets

			situacao_pallets[pallet_E1 - 1]['localizacao'] = 'E1E2' # O pallet está sendo transportado da E1 para a E2
			
		
		if 't7' in transicoes_habilitadas: # O pallet está sendo devolvido para a esteira, saindo da E1 e indo para a E2

			if pallet_E1E2 < 14:
				pallet_E1E2 += 1 # A numeração é sempre em sequência, visto que os pallets começam alinhados e essa ordem não é alterada em nenhuma configuração do sistema
				
			else:
				pallet_E1E2 = 1 # Caso o pallet seja o 14, é necessário voltar para o pallet 1, uma vez que só há 14 pallets
	
			situacao_pallets[pallet_E1 - 1]['localizacao'] = 'E1E2' # O pallet está sendo transportado da E1 para a E2
			situacao_pallets[pallet_E1 - 1]['template'] = 0 # O template foi armazenado, ou seja, o pallet ficou vazio
			situacao_pallets[pallet_E1 - 1]['situacao do template'] = 0	# O template foi armazenado, logo, sem peça

			
		## Estação 8 - Transporte da Estação 1 para a Estação 2 ##
		
		if 't82' in transicoes_habilitadas and pallet_E1E2 != 1: # Se não for o pallet 1
			transicoes_habilitadas.remove('t82')
			
		if 't84' in transicoes_habilitadas and pallet_E1E2 != 2: # Se não for o pallet 2
			transicoes_habilitadas.remove('t84')
		
		if 't86' in transicoes_habilitadas and pallet_E1E2 != 3: # Se não for o pallet 3
			transicoes_habilitadas.remove('t86')
			
		if 't88' in transicoes_habilitadas and pallet_E1E2 != 4: # Se não for o pallet 4
			transicoes_habilitadas.remove('t88')
			
		if 't90' in transicoes_habilitadas and pallet_E1E2 != 5: # Se não for o pallet 5
			transicoes_habilitadas.remove('t90')
			
		if 't92' in transicoes_habilitadas and pallet_E1E2 != 6: # Se não for o pallet 6
			transicoes_habilitadas.remove('t92')
			
		if 't94' in transicoes_habilitadas and pallet_E1E2 != 7: # Se não for o pallet 7
			transicoes_habilitadas.remove('t94')
			
		if 't96' in transicoes_habilitadas and pallet_E1E2 != 8: # Se não for o pallet 8
			transicoes_habilitadas.remove('t96')
			
		if 't98' in transicoes_habilitadas and pallet_E1E2 != 9: # Se não for o pallet 9
			transicoes_habilitadas.remove('t98')
			
		if 't100' in transicoes_habilitadas and pallet_E1E2 != 10: # Se não for o pallet 10
			transicoes_habilitadas.remove('t100')
			
		if 't102' in transicoes_habilitadas and pallet_E1E2 != 11: # Se não for o pallet 11
			transicoes_habilitadas.remove('t102')
			
		if 't104' in transicoes_habilitadas and pallet_E1E2 != 12: # Se não for o pallet 12
			transicoes_habilitadas.remove('t104')
			
		if 't106' in transicoes_habilitadas and pallet_E1E2 != 13: # Se não for o pallet 13
			transicoes_habilitadas.remove('t106')
			
		if 't108' in transicoes_habilitadas and pallet_E1E2 != 14: # Se não for o pallet 14
			transicoes_habilitadas.remove('t108')

			
		## Estação 2 - Torno ##

		if 't138' in transicoes_habilitadas or 't140' in transicoes_habilitadas or 't142' in transicoes_habilitadas or 't144' in transicoes_habilitadas or 't168' in transicoes_habilitadas: # Se p94 tem uma ficha, ou seja, se chegou um pallet na E2
			
			if pallet_E2 < 14:
				pallet_E2 += 1 # A numeração é sempre em sequência, visto que os pallets começam alinhados e essa ordem não é alterada em nenhuma configuração do sistema
				
			else:
				pallet_E2 = 1 # Caso o pallet seja o 14, é necessário voltar para o pallet 1, uma vez que só há 14 pallets

			situacao_pallets[pallet_E2 - 1]['localizacao'] = 'E2' # O pallet está na E2

			if situacao_pallets[pallet_E2 - 1]['template'] == 0: # Chegou um pallet vazio
			
				if 't142' in transicoes_habilitadas:
					transicoes_habilitadas.remove('t142') # Template com peça bruta diferente
					
				if 't144' in transicoes_habilitadas:
					transicoes_habilitadas.remove('t144') # Template com peça bruta

				if 't168' in transicoes_habilitadas:
					transicoes_habilitadas.remove('t168') # Template com peça pronta diferente
			
			elif situacao_pallets[pallet_E2 - 1]['situacao do template'] == 'peca bruta': # Chegou um pallet com peça bruta

				if 't138' in transicoes_habilitadas:
					transicoes_habilitadas.remove('t138') # Pallet vazio
					
				if 't142' in transicoes_habilitadas:
					transicoes_habilitadas.remove('t142') # Template com peça bruta diferente
				
				if 't168' in transicoes_habilitadas:
					transicoes_habilitadas.remove('t168') # Template com peça pronta diferente
					
			elif situacao_pallets[pallet_E2 - 1]['situacao do template'] == 'peca pronta': # Chegou um pallet com peça pronta
			
				if 't138' in transicoes_habilitadas:
					transicoes_habilitadas.remove('t138') # Pallet vazio
					
				if 't142' in transicoes_habilitadas:
					transicoes_habilitadas.remove('t142') # Template com peça bruta diferente
					
				if 't144' in transicoes_habilitadas:
					transicoes_habilitadas.remove('t144') # Template com peça bruta	
			
			if 't140' in transicoes_habilitadas: # Não tem template vazio chegando
				transicoes_habilitadas.remove('t140') # Template vazio
				
			
		if 't139' in transicoes_habilitadas or 't141' in transicoes_habilitadas or 't143' in transicoes_habilitadas or 't145' in transicoes_habilitadas or 't169' in transicoes_habilitadas: # O pallet está sendo devolvido para a esteira, saindo da E1 e indo para a E2

			if pallet_E2E1 < 14:
				pallet_E2E1 += 1 # A numeração é sempre em sequência, visto que os pallets começam alinhados e essa ordem não é alterada em nenhuma configuração do sistema
				
			else:
				pallet_E2E1 = 1 # Caso o pallet seja o 14, é necessário voltar para o pallet 1, uma vez que só há 14 pallets

			situacao_pallets[pallet_E2 - 1]['localizacao'] = 'E2E1' # O pallet está sendo transportado da E1 para a E2
		
		
		if 't146' in transicoes_habilitadas: # O pallet está sendo devolvido para a esteira, saindo da E2 e indo para a E1

			if pallet_E2E1 < 14:
				pallet_E2E1 += 1 # A numeração é sempre em sequência, visto que os pallets começam alinhados e essa ordem não é alterada em nenhuma configuração do sistema

			else:
				pallet_E2E1 = 1 # Caso o pallet seja o 14, é necessário voltar para o pallet 1, uma vez que só há 14 pallets

			situacao_pallets[pallet_E2 - 1]['localizacao'] = 'E2E1' # O pallet está sendo transportado da E1 para a E2
			situacao_pallets[pallet_E2 - 1]['template'] = 0 # O número do template que o pallet recebeu
			situacao_pallets[pallet_E2 - 1]['situacao do template'] = 0	# A situação da peça que o pallet recebeu


		if places[161]['tokens'] == 0:

			if 't147' in transicoes_habilitadas: # Se o buffer 1 pode receber uma peça bruta
			
				if situacao_pallets[pallet_E2 - 1]['template'] == fila_pecas_producao[0]: # Se a peça que chegou é a da ordem de produção
					if 't157' in transicoes_habilitadas: # Se o buffer 2 pode receber uma peça bruta
					
						template_buffer_torno.append({'template': situacao_pallets[pallet_E2 - 1]['template'], 'buffer': 1}) # Armazenando os números dos templates que estão com as peças sendo trabalhadas
						
						transicoes_habilitadas.remove('t145') # A peça bruta nunca volta, sempre é trabalhada

						transicoes_habilitadas.remove('t157') # Prioridade do buffer 1. Não armazenar a peça bruta no buffer 2
						
						if 't170' in transicoes_habilitadas: # É para levar a peça para o torno e não para movimentar o LSB
							transicoes_habilitadas.remove('t170') # Não permite que o LSB se desloque da esteira para o torno enquanto armazena a peça pronta
							
						fila_pecas_producao = fila_pecas_producao[1 : ] # A primeira peça da fila já esta sendo feita, então tirar da fila
						
					else:
					
						if places[149]['tokens'] != 1: # O buffer 2 não pode receber uma peça bruta... O buffer 1 só pode receber uma peça bruta se o buffer 2 estiver com a sua peça bruta em produção, ou seja, p150 com ficha (assim que está implementado)
							transicoes_habilitadas.remove('t147') # Sendo assim o que resta é deixar o pallet seguir
							
						else:
						
							template_buffer_torno.append({'template': situacao_pallets[pallet_E2 - 1]['template'], 'buffer': 1}) # Armazenando os números dos templates que estão com as peças sendo trabalhadas
						
							transicoes_habilitadas.remove('t145') # Nesse caso, a peça irá para o buffer 1
							
							fila_pecas_producao = fila_pecas_producao[1 : ] # A primeira peça da fila já esta sendo feita, então tirar da fila

				else: # Não é a peça da fila, deixar o pallet seguir

					transicoes_habilitadas.remove('t147') # Não armazenar a peça bruta no buffer 1
					
					transicoes_habilitadas.remove('t157') # Não armazenar a peça bruta no buffer 2

			elif 't157' in transicoes_habilitadas: # Se o buffer 1 não pode receber uma peça bruta mas o buffer 2 pode

				if situacao_pallets[pallet_E2 - 1]['template'] == fila_pecas_producao[0]: # Se a peça que chegou é a da ordem de produção
				
					if places[139]['tokens'] != 1: # O buffer 1 não pode receber uma peça bruta... O buffer 2 só pode receber uma peça bruta se o buffer 1 estiver com a sua peça bruta em produção, ou seja, p103 com ficha (assim que está implementado)
						transicoes_habilitadas.remove('t157')

					else:
						
						template_buffer_torno.append({'template': situacao_pallets[pallet_E2 - 1]['template'], 'buffer': 2}) # Armazenando os números dos templates que estão com as peças sendo trabalhadas
						
						transicoes_habilitadas.remove('t145') # A peça bruta nunca volta, sempre é trabalhada
						
						if 't170' in transicoes_habilitadas: # É para levar a peça para o torno e não para movimentar o LSB
							transicoes_habilitadas.remove('t170') # Não permite que o LSB se desloque da esteira para o torno enquanto armazena a peça pronta
							
						fila_pecas_producao = fila_pecas_producao[1 : ] # A primeira peça da fila já esta sendo feita, então tirar da fila
							
				else: # Não é a peça da fila, deixar o pallet seguir				
					transicoes_habilitadas.remove('t157') # Não armazenar a peça bruta no buffer 2

			else: # O pallet está sendo devolvido para a esteira, saindo da E1 e indo para a E2
				
				if 't145' in transicoes_habilitadas:
					if pallet_E2E1 < 14: 
						pallet_E2E1 += 1 # A numeração é sempre em sequência, visto que os pallets começam alinhados e essa ordem não é alterada em nenhuma configuração do sistema
						
					else:
						pallet_E2E1 = 1 # Caso o pallet seja o 14, é necessário voltar para o pallet 1, uma vez que só há 14 pallets

					situacao_pallets[pallet_E2 - 1]['localizacao'] = 'E2E1' # O pallet está sendo transportado da E1 para a E2
					
			
		if 't172' in transicoes_habilitadas or places[161]['tokens'] == 1: 
		
			if 't151' in transicoes_habilitadas: # Do jeito que está implementado o torno só começa a trabalhar a peça quando o LSB volta para a estação
				transicoes_habilitadas.remove('t151') # Torno não pode começar a trabalhar a peça do buffer 1
				
			if 't161' in transicoes_habilitadas: # Do jeito que está implementado o torno só começa a trabalhar a peça quando o LSB volta para a estação
				transicoes_habilitadas.remove('t161') # Torno não pode começar a trabalhar a peça do buffer 2
		
			if 't153' in transicoes_habilitadas: # Devolver a peça ao template, ao invés de mover o robô pelo LSB
				transicoes_habilitadas.remove('t172') # Não permite que o LSB se desloque do torno para a esteira enquanto armazena a peça pronta
				
			if 't163' in transicoes_habilitadas: # Devolver a peça ao template, ao invés de mover o robô pelo LSB
				transicoes_habilitadas.remove('t172') # Não permite que o LSB se desloque do torno para a esteira enquanto armazena a peça pronta
	
		
		if 't155' in transicoes_habilitadas: # Se o processo de armazenar peça no buffer 1 pode começar
		
			if 't139' in transicoes_habilitadas:
				transicoes_habilitadas.remove('t139') # Sempre devolver a peça feita para o pallet
		
			if 't159' in transicoes_habilitadas:
				transicoes_habilitadas.remove('t159') # Não pode começar o processo de levar peça do buffer 2 para o torno
				
			if 't165' in transicoes_habilitadas: # Do jeito que está implementado ele devolve para esteira o que veio primeiro

				if template_buffer_torno[0]['buffer'] == 1:
					transicoes_habilitadas.remove('t165') # Não começar o processo de armazenar peça no buffer 2
				
				elif template_buffer_torno[0]['buffer'] == 2: # Poderia utilizar o else, mas por segurança estou utilizando o elif
					transicoes_habilitadas.remove('t155') # Não começar o processo de armazenar peça no buffer 1
					
			if 't170' in transicoes_habilitadas:
				transicoes_habilitadas.remove('t170') # Não permite que o LSB se desloque da esteira para o torno enquanto armazena a peça pronta
					
		elif 't165' in transicoes_habilitadas: # Funciona como um 't155' in transicoes_habilitadas or 't165' in transicoes_habilitadas, visto que se 't155' estiver contido, ele executará no código acima, e não depende do 't165', mas caso 't155' não esteja contido, mas 't165' esteja, ele executa abaixo. Funciona como or porque ele só executa esse elif se o primeiro ir for falso
			
			if 't139' in transicoes_habilitadas:
				transicoes_habilitadas.remove('t139') # Sempre devolver a peça feita para o pallet
			
			if 't170' in transicoes_habilitadas:
				transicoes_habilitadas.remove('t170') # Não permite que o LSB se desloque da esteira para o torno enquanto armazena a peça pronta
		
		
		if 't149' in transicoes_habilitadas and 't165' in transicoes_habilitadas: # A prioridade é entregar a peça (jeito que está implementado)
			transicoes_habilitadas.remove('t149') # Não pode começar o processo de levar peça do buffer 1 para o torno
			
		if 't155' in transicoes_habilitadas and 't159' in transicoes_habilitadas: # A prioridade é entregar a peça (jeito que está implementado)
			transicoes_habilitadas.remove('t149') # Não pode começar o processo de levar peça do buffer 1 para o torno
		
		
		if (places[140]['tokens'] == 0 and places[150]['tokens'] == 0) and ('t170' in transicoes_habilitadas): # O LSB precisa estar no torno para pegar a peça produzida
			transicoes_habilitadas.remove('t170') # Não permite que o LSB se desloque da esteira para o torno enquanto armazena a peça pronta
			
			
		if 't167' in transicoes_habilitadas: # O pallet está sendo devolvido para a esteira, saindo da E2 e indo para a E1
			
			situacao_pallets[pallet_E2 - 1]['localizacao'] = 'E2E1' # O pallet está sendo transportado da E1 para a E2

			situacao_pallets[pallet_E2 - 1]['template'] = template_buffer_torno[0]['template'] # O número do template que o pallet recebeu. A preferência para devolver é pela ordem que ele mandou fazer (assim que está implementado).
			situacao_pallets[pallet_E2 - 1]['situacao do template'] = 'peca pronta'	# A situação da peça que o pallet recebeu
			
			template_buffer_torno = template_buffer_torno[1 : ] # Removo o número do template, pois já foi devolvido

			
		## Estação 8 - Transporte da Estação 2 para a Estação 1 ##
		
		if 't110' in transicoes_habilitadas and pallet_E2E1 != 1: # Se não for o pallet 1
			transicoes_habilitadas.remove('t110')
			
		if 't112' in transicoes_habilitadas and pallet_E2E1 != 2: # Se não for o pallet 2
			transicoes_habilitadas.remove('t112')
		
		if 't114' in transicoes_habilitadas and pallet_E2E1 != 3: # Se não for o pallet 3
			transicoes_habilitadas.remove('t114')
			
		if 't116' in transicoes_habilitadas and pallet_E2E1 != 4: # Se não for o pallet 4
			transicoes_habilitadas.remove('t116')
			
		if 't118' in transicoes_habilitadas and pallet_E2E1 != 5: # Se não for o pallet 5
			transicoes_habilitadas.remove('t118')
			
		if 't120' in transicoes_habilitadas and pallet_E2E1 != 6: # Se não for o pallet 6
			transicoes_habilitadas.remove('t120')
			
		if 't122' in transicoes_habilitadas and pallet_E2E1 != 7: # Se não for o pallet 7
			transicoes_habilitadas.remove('t122')
			
		if 't124' in transicoes_habilitadas and pallet_E2E1 != 8: # Se não for o pallet 8
			transicoes_habilitadas.remove('t124')
			
		if 't126' in transicoes_habilitadas and pallet_E2E1 != 9: # Se não for o pallet 9
			transicoes_habilitadas.remove('t126')
			
		if 't128' in transicoes_habilitadas and pallet_E2E1 != 10: # Se não for o pallet 10
			transicoes_habilitadas.remove('t128')
			
		if 't130' in transicoes_habilitadas and pallet_E2E1 != 11: # Se não for o pallet 11
			transicoes_habilitadas.remove('t130')
			
		if 't132' in transicoes_habilitadas and pallet_E2E1 != 12: # Se não for o pallet 12
			transicoes_habilitadas.remove('t132')
			
		if 't134' in transicoes_habilitadas and pallet_E2E1 != 13: # Se não for o pallet 13
			transicoes_habilitadas.remove('t134')
			
		if 't136' in transicoes_habilitadas and pallet_E2E1 != 14: # Se não for o pallet 14
			transicoes_habilitadas.remove('t136')
		
		
		## print 'Tempo Gasto:', r.getTotalTimeElapsed()		
		## print transicoes_habilitadas # Para acompanhar as transições habilitadas após cada evolução no tempo
		## print
		## raw_input() # Para só mostrar as próximas transições quando eu der "Enter"
		
		
		## Dinâmica da Rede ##

		for i in transicoes_habilitadas: # Irá realizar o disparo para cada transição habilitada
			r.dynamic(i)

		r.avanceTimeElapsed() # Após os disparos a rede avança no tempo
		
		transicoes_habilitadas = r.getEnabledTransitions() # As novas transições habilitadas após avançar no tempo

		places, transitions = r.getDynamic()
		
		quantidade_de_pecas_produzidas = places[42]['tokens']

	
	return r.getTotalTimeElapsed() # O tempo gasto para produzir as peças (na rede)

############################################