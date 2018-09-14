# -*- coding: utf-8 -*-


###################### Análises ######################

from Net import net ## Importa a rede do arquivo Net.py ##
from Control import producao_pecas ## Importa a função que produz as peças do arquivo Dynamic.py ##
from Control_Improved import producao_pecas_melhorada ## Importa a função que produz as peças do arquivo Dynamic_Improved.py ##

import timeit ## Só para medir o tempo de execução de partes do código ##

############################################


## Somente para printar o tempo gasto pelo Python e pelas redes ##

def tempo(p = False):
	
	quantidade_pecas_produzidas = []
	
	tempo_total_producao = []
	tempo_total_producao_melhorado = []
	
	tempo_medio_producao = []
	tempo_medio_producao_melhorado = []
	
	
	for i in range(1, 7): # Para produzir as peças e mostrar o tempo de execução no Python e na rede

		quantidade_producao = i # Quantidade de peças que serão produzidas em sequência
	
		start = timeit.default_timer() # Tempo inicial para a execução do código
		tempo = producao_pecas(net, quantidade_producao) # Produz as peças
		stop = timeit.default_timer() # Tempo final para a execução do código
		
		net.resetDynamic() # Reseta a dinâmica da rede
		
		start_melhorado = timeit.default_timer() # Tempo inicial para a execução do código
		tempo_melhorado = producao_pecas_melhorada(net, quantidade_producao) # Produz as peças de forma otimizada
		stop_melhorado = timeit.default_timer() # Tempo final para a execução do código
		
		net.resetDynamic() # Reseta a dinâmica da rede
		
		quantidade_pecas_produzidas.append(i)
		
		tempo_total_producao.append(tempo)
		tempo_total_producao_melhorado.append(tempo_melhorado)
		
		tempo_medio_producao.append(tempo/float(i))
		tempo_medio_producao_melhorado.append(tempo_melhorado/float(i))
		
		
		if p == True:
			if i == 1:
				print ('\n#############################'
					   '##############################\n')
				print 'Order to Manufacture', i, 'Piece' # Quantidade de peças feitas por pedido de produção
			
			else:
				print 'Order to Manufacture', i, 'Pieces in a Row' # Quantidade de peças feitas por pedido de produção
				
			print '\n\nExecution Time:', stop - start, 's' # Printa o tempo gasto para executar o código
			print 'Execution Time (Improved):', stop_melhorado - start_melhorado, 's' # Printa o tempo gasto para executar o código melhorado
			print '\nElapsed Time (net):', tempo, 's' # Printa o tempo gasto para produzir as peças
			print 'Elapsed Time (net) (Improved):', tempo_melhorado, 's' # Printa o tempo gasto para produzir as peças melhorado
			print '\nTime for Piece (arithmetic mean):', round(tempo/float(i), 3), 's' # Printa o tempo médio para produzir uma peça
			print 'Time for Piece (arithmetic mean) (Improved):', round(tempo_melhorado/float(i), 3), 's' # Printa o tempo melhorado médio para produzir uma peça
			print ('\n#############################'
				   '##############################\n')
	
	producao = [quantidade_pecas_produzidas, tempo_total_producao, tempo_total_producao_melhorado, tempo_medio_producao, tempo_medio_producao_melhorado]
	
	return producao
	
# tempo(p = True)	
############################################