import os
import csv
import re

from bs4 import BeautifulSoup

def parseXML(file):
    with open(file, 'r') as f:
        data = f.read()
    
    # Passa os dados para o BS 
    bs_data = BeautifulSoup(data, 'xml')
    
    # Busca as tags   
    try:
        valor_produtos = bs_data.find_all('vProd')
        nota_fiscal = bs_data.find('nNF')
        data_emissao = bs_data.find('dhEmi')
        obs_pedido = bs_data.find('infCpl')
        nat_operacao = bs_data.find('natOp')

    except Exception as e:
            print(e)
            return

    try:
        obs = obs_pedido.get_text()
        pedido = re.findall(r"(?<=PEDIDO ORIGEM:).*", obs)

        if not pedido:
          pedido = re.findall(r"(?<=PEDIDO ADM:).*", obs)

    except:
      pedido = "0"
  
    if not pedido:
      pedido = "0"  

    valor = valor_produtos[-1].get_text()

    natOp = nat_operacao.get_text()
    if not natOp:
      natOp = "0"

    return [nota_fiscal.get_text(), data_emissao.get_text(), valor, *pedido, natOp]

def main():
    # define diretorio
    directory = 'xml'

    # loop no diretorio
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        
        print(filename)

      # check se é arquivo
        if os.path.isfile(f):
            nf = parseXML(f)

            with open('faturados.csv', mode='a') as devolucoes:
              devolucoes_writer = csv.writer(devolucoes, delimiter=';', lineterminator = '\n')    
              devolucoes_writer.writerow(nf)

if __name__ == '__main__':
    main()
