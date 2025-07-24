from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from datetime import datetime
import pandas as pd
import os
import json




# Subclasse de SimpleDocTemplate para adicionar o cabeçalho com imagem
class PropostaComImagem(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        super(PropostaComImagem, self).__init__(*args, **kwargs)

    def beforePage(self):
        altura, largura = letter
        # Cabeçalho (imagem) - usaremos self.canv para acessar o canvas corretamente
        self.canv.drawImage('Logo.jpg', 5, altura +95, width=600, height=80)
        espacamento = 20  # Ajuste esse valor conforme necessário, em pontos
        self.canv.translate(0, -espacamento) 
    

# Mapeamento das chaves
mapeamento_chaves = {
    '{{VIG}}':'DATA VIG',
    '{{MATRICULA}}':'MATRÍCULA',
    '{{NOME}}':'NOME COMPLETO',
    '{{NOMEMAE}}':'NOME DA MÃE',
    '{{TELEFONE}}':'DDD CELULAR',
    '{{EMAIL}}':'E-MAIL',
    '{{SEXO}}':'SEXO',
    '{{DTNASC}}':'DATA DE NASCIMENTO',
    '{{ESTCIVTIT}}':'ESTADO CIVIL',
    '{{CPF}}':'CPF',
    '{{END}}':'ENDEREÇO',
    '{{NUM}}':'NÚMERO',
    '{{BAIRRO}}':'BAIRRO',
    '{{CIDADE}}':'CIDADE',
    '{{CEP}}':'CEP',
    '{{UF}}':'UF',
    '{{NOMEDEP1}}':'NOME DEP 1',
    '{{NasDep1}}':'DATA NASC DEP 1',
    '{{SEXDEP1}}' :'SEXO DEP 1',
    '{{NOMAEDEP1}}':'NOME DA MÃE DEP 1',
    '{{CPFDEP1}}':'CPF DEP 1',
    '{{PARENDEP1}}':'PARENTESCO DEP 1',
    '{{ESTCIVDEP1}}':'ESTADO CIVIL DEP 1',
    '{{NOMEDEP2}}':'NOME DEP 2',
    '{{NasDep2}}':'DATA NASC DEP 2',
    '{{SEXDEP2}}':'SEXO DEP 2',
    '{{NOMAEDEP2}}':'NOME DA MÃE DEP 2',
    '{{PARENDEP2}}':'PARENTESCO DEP 2',
    '{{CPFDEP2}}':"CPF DEP 2",
    '{{ESTCIVDEP2}}':'ESTADO CIVIL DEP 2',
    '{{NOMEDEP3}}':'NOME DEP 3',
    '{{NasDep3}}':'DATA NASC DEP 3',
    '{{SEXDEP3}}':'SEXO DEP 3',
    '{{NOMAEDEP3}}':'NOME DA MÃE DEP 3',
    '{{CPFDEP3}}':'CPF DEP 3',
    '{{PARENDEP3}}':'PARENTESCO DEP 3',
    '{{ESTCIVDEP3}}':'ESTADO CIVIL DEP 3',
    '{{NOMEDEP4}}':'NOME DEP 4',
    '{{NasDep4}}':'DATA NASC DEP 4',
    '{{SEXDEP4}}':'SEXO DEP 4',
    '{{NOMAEDEP4}}':'NOME DA MÃE DEP 4',
    '{{CPFDEP4}}':'CPF DEP 4',
    '{{PARENDEP4}}':'PARENTESCO DEP 4',
    '{{ESTCIVDEP4}}':'ESTADO CIVIL DEP 4',
    '{{NOMEDEP5}}':'NOME DEP 5',
    '{{NasDep5}}':'DATA NASC DEP 5',
    '{{SEXDEP5}}':'SEXO DEP 5',
    '{{NOMAEDEP5}}':'NOME DA MÃE DEP 5',
    '{{CPFDEP5}}':'CPF DEP 5',
    '{{PARENDEP5}}':'PARENTESCO DEP 5',
    '{{ESTCIVDEP5}}':'ESTADO CIVIL DEP 5',
    '{{mosEnf}}':11226,
    '{{mosAp}}':11239,
    '{{natEnf}}':11227,
    '{{natAp}}':11240,
    '{{odonto}}':'Odonto PREMIUM',
    '{{idadeTit}}':'Titular IDADE',
    '{{valorSautit}}':'Titular VALOR',
    '{{valorOdotit}}':'Odonto VALOR',
    '{{idadedep1}}':'Dep 1 IDADE',
    '{{valorSaudep1}}':'Dep 1 VALOR',
    '{{valorOdodep1}}':'Dep 1 Odonto VALOR',
    '{{idadedep2}}':'Dep 2 IDADE',
    '{{valorSaudep2}}':'Dep 2 VALOR',
    '{{valorOdodep2}}':'Dep 2 Odonto VALOR',
    '{{idadedep3}}':'Dep 3 IDADE',
    '{{valorSaudep3}}':'Dep 3 VALOR',
    '{{valorOdodep3}}':'Dep 3 Odonto VALOR',
    '{{idadedep4}}':'Dep 4 IDADE',
    '{{valorSaudep4}}':'Dep 4 VALOR',
    '{{valorOdodep4}}':'Dep 4 Odonto VALOR',
    '{{idadedep5}}':'Dep 5 IDADE',
    '{{valorSaudep5}}':'Dep 5 VALOR',
    '{{valorOdodep5}}':'Dep 5 Odonto VALOR',
    '{{TotalSau}}':'VALOR Plano',
    '{{Totalodo}}':'VALOR Total Odonto',
    '{{LOCAL}}':'LOCAL',
    '{{DATA}}': 'DATA'
}

def preencher_chaves(linha_cliente):
    """
    Preenche as chaves do documento com os valores correspondentes da linha do cliente.
    """
    # Substitui valores vazios, NaN ou None por uma string vazia
    proposta_dados = {}
    for chave, coluna in mapeamento_chaves.items():  # mapeamento_chaves é o seu dicionário
        valor = linha_cliente.get(coluna, None)  # Pega o valor da coluna correspondente
        
        # Verificar se o valor é NaN, None ou vazio
        if pd.isna(valor) or valor is None or valor == '':
            proposta_dados[chave] = ''  # Substitui por string vazia
        else:
            proposta_dados[chave] = str(valor)  # Converte valor para string
    
    return proposta_dados

def criar_proposta(arquivo,diretorio,linha_inicio,linha_fim):
    df = pd.read_excel(arquivo, dtype={
    'Dep 5 IDADE': str, 
    'Dep 4 IDADE': str, 
    'Dep 3 IDADE': str, 
    'Dep 2 IDADE': str, 
    'Dep 1 IDADE': str, 
    'Titular IDADE': str, 
    'NÚMERO': str, 
    'DDD CELULAR': str
})
    # Substituindo NaN por string vazia em todo o DataFrame
    df = df.fillna('')
    if linha_inicio is not None and linha_fim is not None:
        df = df.iloc[linha_inicio:linha_fim+1]
    log_contratos = []
    for _, linha_cliente in df.iterrows():
        if linha_cliente['NOME COMPLETO']:
        # Preencher as chaves com os dados da linha atual
            proposta_dados = preencher_chaves(linha_cliente)
            nome_arquivo = f"Proposta SINSP {proposta_dados.get('{{NOME}}','')}.pdf"
            caminho_arquivo = os.path.join(diretorio, nome_arquivo)
            # Usando a subclasse para permitir inserção de cabeçalho com imagem
            doc = PropostaComImagem(caminho_arquivo, pagesize=letter)


            # Lista para adicionar elementos no PDF
            elementos = []
            
            # Função para garantir que o texto caiba na célula
            def adjust_text_for_table(text, max_width):
                # Calcula a largura do texto para garantir que ele se ajusta à célula
                words = text.split(" ")
                lines = []
                current_line = ""

                for word in words:
                    # Verifica se a linha atual mais a nova palavra excede a largura da célula
                    if len(current_line + word) * 6 <= max_width:
                        current_line += word + " "
                    else:
                        lines.append(current_line.strip())
                        current_line = word + " "
                
                if current_line:
                    lines.append(current_line.strip())
                
                return "\n".join(lines)  # Retorna texto simples
            

            # Função para criar um Paragraph com texto ajustado
            def create_paragraph(text, max_width):
                styles = getSampleStyleSheet()
                style = styles['Normal']  # Estilo básico
                style.fontName = 'Helvetica'
                style.fontSize = 11
                style.leading = 10
                style.spaceBefore = 2
                style.spaceAfter = 2
                
                # Configura a largura do parágrafo
                paragraph = Paragraph(text, style)
                return paragraph
           

            # Obtendo a data de hoje
            hoje = datetime.today()

            # Verificando o dia
            if hoje.day <= 21:
                # Se o dia for até 21, o mês seguinte é o mês de vigência
                mes_vigencia = hoje.month + 1 if hoje.month < 12 else 1
                ano_vigencia = hoje.year if hoje.month < 12 else hoje.year + 1
            else:
                # Se o dia for a partir de 22, o mês após o próximo mês é o mês de vigência
                mes_vigencia = hoje.month + 2 if hoje.month < 11 else (hoje.month - 10)
                ano_vigencia = hoje.year if hoje.month < 11 else hoje.year + 1

            # Montando a data no formato DD/MM/AAAA
            data_vig = f"01/{mes_vigencia:02d}/{ano_vigencia}"    
            # Informações iniciais
            data_vigencia = [
                ['Data Vigência', 'Entidade', 'Matrícula'],  # Cabeçalho
                [data_vig, 'SINSP/RN', proposta_dados.get('{{MATRICULA}}','')]  # Valores e campo vazio
            ]

            # Criando a tabela
            tabela_1 = Table(data_vigencia, colWidths=[200, 200, 200])
            
            # Estilizando a tabela
            tabela_1.setStyle(TableStyle([ 
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            # Adicionando a tabela à lista de elementos
            elementos.append(tabela_1)

            espacador = Spacer(1, 50)  # 50 é o espaço em pontos (ajuste conforme necessário)
            elementos.append(espacador)

        # Criando o formulário com chaves para preenchimento
            formulario = [
                ['Proponente Titular', '', '',''],  # Título mesclado
                ['Nome:', proposta_dados.get('{{NOME}}',''), '', ''],  # Chave para substituir depois
                ['Email:', proposta_dados.get('{{EMAIL}}'),'Telefone:', proposta_dados['{{TELEFONE}}']],
                ['CPF:', proposta_dados.get('{{CPF}}',''), '', ''],  # Chave para substituir depois
                ['Data de Nascimento:',proposta_dados.get('{{DTNASC}}',''),'SEXO:', proposta_dados['{{SEXO}}']],
                ['Estado Civil:',proposta_dados.get('{{ESTCIVTIT}}',''), '', ''],
                ['RG:',proposta_dados.get('{{RG}}',''),'ORG:',proposta_dados.get('{{ORG}}','')],
                ['Endereço:',proposta_dados.get('{{END}}',''),"Número:",proposta_dados.get('{{NUM}}','')],
                ['Complemento:',proposta_dados.get('{{COMPL}}',''),'Bairro',proposta_dados.get('{{BAIRRO}}','')],
                ['Cidade:',proposta_dados.get('{{CIDADE}}',''),'UF',proposta_dados.get('{{UF}}','')],
                ['Nome da mãe:',proposta_dados.get('{{NOMEMAE}}','')]
                #['','{{}}','','{{}}'],
                #['','{{}}','','{{}}'],
                ]
            col_widths = [110, 260,110,120]

            for row in formulario:
                if len(row[1]) > 0:  # Se houver texto
                    row[1] = adjust_text_for_table(row[1], col_widths[1])
            # Criando a tabela para o formulário
            tabela_formulario = Table(formulario, col_widths)

            # Estilizando a tabela
            tabela_formulario.setStyle(TableStyle([ 
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),  # Alinhando os campos à esquerda
                ('SPAN', (0, 0), (3, 0)), 
                ('SPAN', (1, 1), (3, 1)),  
                ('SPAN', (1, 3), (3, 3)),  # Mesclando a célula de "CPF"
                ('SPAN', (1, 5), (3, 5)),  
                ('SPAN',(1,10), (3,10)),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold')
                
            ]))

            # Adicionando a tabela do formulário à lista de elementos
            elementos.append(tabela_formulario)


            #EMPRESA/ENTIDADE
            entidade = [
                ['EMPRESA/ENTIDADE DE CLASSE',''],
                ['Razão Social:','SINDICATO DOS TRABALHADORES DO SERVICO PUBLICO DA ADMINISTRACAO DIRETA DO ESTADO DO RN'],
                ['CNPJ:','17.572.030/0001-75'],
                ['Sindicato:','SINSP/RN']
            ]

            
            
                # Criando a tabela com colunas de tamanhos ajustados
            col_widths = [200, 400]

            # Ajustando o texto da segunda coluna para garantir que quebre corretamente
            for row in entidade:
                if len(row[1]) > 0:  # Se houver texto
                    row[1] = create_paragraph(row[1], col_widths[1])
            
            #tabela_entidade = Table(entidade,colWidths=[100, 400])
            tabela_entidade = Table(entidade, colWidths=col_widths)

            tabela_entidade.setStyle(TableStyle([ 
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),  # Alinhando os campos à esquerda
                ('SPAN', (0, 0), (1, 0)),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                
            ]))

            

            espacador = Spacer(1, 50)  # 50 é o espaço em pontos (ajuste conforme necessário)
            elementos.append(espacador)
            elementos.append(tabela_entidade)


            #DEPENDENTES

            depen = [
            ['1. DEPENDENTE','','',''],
            ['Nome:', proposta_dados.get('{{NOMEDEP1}}', ''), 'Data Nascimento:', proposta_dados.get('{{NasDep1}}', '')],
            ['CPF:', proposta_dados.get('{{CPFDEP1}}', ''), 'Sexo:', proposta_dados.get('{{SEXDEP1}}', '')],
            ['Estado Civil:', proposta_dados.get('{{ESTCIVDEP1}}', ''), 'Parentesco:', proposta_dados.get('{{PARENDEP1}}', '')],
            ['Nome da Mãe:', proposta_dados.get('{{NOMAEDEP1}}', ''), '', ''],
            
            # Dependente 2
            ['2. DEPENDENTE','','',''],
            ['Nome:', proposta_dados.get('{{NOMEDEP2}}', ''), 'Data Nascimento:', proposta_dados.get('{{NasDep2}}', '')],
            ['CPF:', proposta_dados.get('{{CPFDEP2}}', ''), 'Sexo:', proposta_dados.get('{{SEXDEP2}}', '')],
            ['Estado Civil:', proposta_dados.get('{{ESTCIVDEP2}}', ''), 'Parentesco:', proposta_dados.get('{{PARENDEP2}}', '')],
            ['Nome da Mãe:', proposta_dados.get('{{NOMAEDEP2}}', ''), '', ''],
            
            # Dependente 3
            ['3. DEPENDENTE','','',''],
            ['Nome:', proposta_dados.get('{{NOMEDEP3}}', ''), 'Data Nascimento:', proposta_dados.get('{{NasDep3}}', '')],
            ['CPF:', proposta_dados.get('{{CPFDEP3}}', ''), 'Sexo:', proposta_dados.get('{{SEXDEP3}}', '')],
            ['Estado Civil:', proposta_dados.get('{{ESTCIVDEP3}}', ''), 'Parentesco:', proposta_dados.get('{{PARENDEP3}}', '')],
            ['Nome da Mãe:', proposta_dados.get('{{NOMAEDEP3}}', ''), '', ''],
            
            # Dependente 4
            ['4. DEPENDENTE','','',''],
            ['Nome:', proposta_dados.get('{{NOMEDEP4}}', ''), 'Data Nascimento:', proposta_dados.get('{{NasDep4}}', '')],
            ['CPF:', proposta_dados.get('{{CPFDEP4}}', ''), 'Sexo:', proposta_dados.get('{{SEXDEP4}}', '')],
            ['Estado Civil:', proposta_dados.get('{{ESTCIVDEP4}}', ''), 'Parentesco:', proposta_dados.get('{{PARENDEP4}}', '')],
            ['Nome da Mãe:', proposta_dados.get('{{NOMAEDEP4}}', ''), '', ''],
            
            # Dependente 5
            ['5. DEPENDENTE','','',''],
            ['Nome:', proposta_dados.get('{{NOMEDEP5}}', ''), 'Data Nascimento:', proposta_dados.get('{{NasDep5}}', '')],
            ['CPF:', proposta_dados.get('{{CPFDEP5}}', ''), 'Sexo:', proposta_dados.get('{{SEXDEP5}}', '')],
            ['Estado Civil:', proposta_dados.get('{{ESTCIVDEP5}}', ''), 'Parentesco:', proposta_dados.get('{{PARENDEP5}}', '')],
            ['Nome da Mãe:', proposta_dados.get('{{NOMAEDEP5}}', ''), '', ''],
        ]
            col_widths = [110, 260,110,120]

            for row in depen:
                if len(row[1]) > 0:  # Se houver texto
                    row[1] = adjust_text_for_table(row[1], col_widths[1])

            tabela_depen = Table(depen,col_widths)

            tabela_depen.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),  # Alinhando os campos à esquerda
                ('SPAN', (0, 0), (3, 0)), 
                ('SPAN',(1, 4), (3, 4)),
                ('SPAN',(0, 5), (3, 5)),
                #dependente 2
                ('BACKGROUND', (0, 5), (3, 5), colors.lightgrey),
                ('TEXTCOLOR', (0, 5), (3, 5), colors.black),
                ('FONTNAME', (0, 5), (3, 5), 'Helvetica-Bold'),
                ('ALIGN', (0, 5), (3, 5), 'CENTER'),
                ('ALIGN', (1, 9), (1, 9), 'LEFT'),
                ('SPAN',(1, 9), (3, 9)),
                #dependente 3
                ('BACKGROUND', (0, 10), (3, 10), colors.lightgrey),
                ('TEXTCOLOR', (0, 10), (3, 10), colors.black),
                ('FONTNAME', (0, 10), (3, 10), 'Helvetica-Bold'),
                ('ALIGN', (0, 10), (3, 10), 'CENTER'),
                ('ALIGN', (1, 10), (1, 10), 'LEFT'),
                ('SPAN',(0, 10), (3, 10)),
                ('SPAN',(1, 14), (3, 14)),
                #dependnete 4
                ('BACKGROUND', (0, 15), (3, 15), colors.lightgrey),
                ('TEXTCOLOR', (0, 15), (3, 15), colors.black),
                ('FONTNAME', (0, 15), (3, 15), 'Helvetica-Bold'),
                ('ALIGN', (0, 15), (3, 15), 'CENTER'),
                ('ALIGN', (1, 15), (1, 15), 'LEFT'),
                ('SPAN',(0, 15), (3, 15)),
                ('SPAN',(1, 19), (3, 19)),
                #DEPENDENTE 5
                ('BACKGROUND', (0, 20), (3, 20), colors.lightgrey),
                ('TEXTCOLOR', (0, 20), (3, 20), colors.black),
                ('FONTNAME', (0, 20), (3, 20), 'Helvetica-Bold'),
                ('ALIGN', (0, 20), (3, 20), 'CENTER'),
                ('ALIGN', (1, 20), (1, 20), 'LEFT'),
                ('SPAN',(0, 20), (3, 20)),
                ('SPAN',(1, 24), (3, 24)),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold')



            ]))

            espacador = Spacer(1, 50)  # 50 é o espaço em pontos (ajuste conforme necessário)
            elementos.append(espacador)
            elementos.append(tabela_depen)
            elementos.append(PageBreak()) #pular para proxima pagina
        

                # Dados da tabela
            produto = [
            ['Praça: MOSSORÓ','','','','','','',''],
            [create_paragraph('Assinale abaixo, com um “X”, o plano pretendido. ATENÇÃO: verifique a disponibilidade do plano de saúde pretendido conforme a entidade indicada na página 1. Todos os dependentes serão cadastrados obrigatoriamente na mesma categoria de plano do proponente titular. ÁREA DE COMERCIALIZAÇÃO Mossoró/RN: Mossoró/RN, Tibau/RN e Baraúna/RN.',100), '','','','','','',''],
            ['Assinale o plano contratado','Planos','Mecanismo de regulação','Código ANS','Abrangência Geográfica','Segmentação Assistencial','Acomodação em internação',''],
            [proposta_dados.get('{{mosEnf}}', ''), 'NOSSO PLANO AHO CA MUN ENF QC 162', 'Sem coparticipação', '485.681/20-3', 'Municipal', 'Ambulatorial + Hospitalar com Obstetrícia', 'Coletiva (Enfermaria)','11226'],
            [proposta_dados.get('{{mosAp}}', ''), 'NOSSO PLANO AHO CA MUN APT QC 184', 'Sem coparticipação', '485.694/20-5', 'Municipal', 'Ambulatorial + Hospitalar com Obstetrícia', 'Individual (Apartamento)','11239'],
            
        ]
            # Largura das colunas
            col_widths = [60, 150, 68, 66, 66, 100,70,20]
            # Agora, ajustando o texto para todas as células, após mesclagem das células
            for row_index, row in enumerate(produto):
                # A partir da linha de índice 2 (ou seja, terceira linha)
                if row_index >= 2:
                    for i, cell in enumerate(row):
                        if len(cell) > 0:  # Se houver texto na célula
                            # Verificando se o texto é longo e precisa ser ajustado
                            row[i] = adjust_text_for_table(cell, col_widths[i])

            # Criando a tabela
            tabela_produto = Table(produto, col_widths)

            # Definindo o estilo da tabela
            tabela_produto.setStyle([
                # Primeira linha: negrito e mesclada
                ('FONTNAME', (0, 0), (6, 0), 'Helvetica-Bold'),  # Aplica negrito na primeira linha inteira
                ('SPAN', (0, 0), (7, 0)),  # Mescla a primeira linha
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),

                # Segunda linha: mesclada
                ('SPAN', (0, 1), (7, 1)),  # Mescla a segunda linha inteira

                # Terceira linha: negrito e cor cinza
                ('FONTNAME', (0, 2), (7, 2), 'Helvetica-Bold'),  # Negrito na terceira linha
                ('BACKGROUND', (0, 2), (7, 2), colors.lightgrey),

                # Ajustes gerais para alinhamento e bordas
                ('SPAN',(6,2),(7,2)),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinha todas as células ao centro
                ('GRID', (0, 0), (-1, 4), 1, colors.black),  # Borda para todas as 
                ('LINEBEFORE', (7, 3), (7, 4), 1, colors.white),
                ('ALIGN', (0, 0), (-1, 4), 'CENTER'),  # Centralizando horizontalmente
                ('VALIGN', (0, 0), (-1, 4), 'MIDDLE'),  # Centralizando verticalmente
                ('ALIGN', (7, 3), (7, 4), 'LEFT'),
                ('VALIGN', (7, 3), (7, 4), 'BOTTOM'), 
                ('TEXTCOLOR', (7, 3), (7, 4), colors.white),
            ])

            
            # Adicionando a tabela aos elementos
            elementos.append(tabela_produto)
        # Seu código atualizado
            produto_Natal = [
            ['Praça: NATAL','','','','','','',''],
            [create_paragraph('Assinale abaixo, com um “X”, o plano pretendido. ATENÇÃO: verifique a disponibilidade do plano de saúde pretendido conforme a entidade indicada na página 1. Todos os dependentes serão cadastrados obrigatoriamente na mesma categoria de plano do proponente titular. ÁREA DE COMERCIALIZAÇÃO Natal/RN, Macaíba/RN, Extremoz/RN,São Gonçalo do Amarante/RN',100),'','','','','','',''],
            ['Assinale o plano contratado','Planos','Mecanismo de regulação','Código ANS','Abrangência Geográfica','Segmentação Assistencial','Acomodação em internação',''],
            [proposta_dados.get('{{natEnf}}', ''), 'NOSSO PLANO AHO \n CA MUN ENF QC 163', 'Sem coparticipação', '485.682/20-1', 'Municipal', 'Ambulatorial + Hospitalar com Obstetrícia', 'Coletiva (Enfermaria)','11227'],
            [proposta_dados.get('{{natAp}}', ''), 'NOSSO PLANO AHO \n CA MUN APT QC 185', 'Sem coparticipação', '485.695/20-3', 'Municipal', 'Ambulatorial + Hospitalar com Obstetrícia', 'Individual (Apartamento)','11240'],

        ]



            # Ajustando o texto para cada célula da tabela
            # Agora, ajustando o texto para todas as células, após mesclagem das células
            for row_index, row in enumerate(produto_Natal):
                # A partir da linha de índice 2 (ou seja, terceira linha)
                if row_index >= 2:
                    for i, cell in enumerate(row):
                        if len(cell) > 0:  # Se houver texto na célula
                            # Verificando se o texto é longo e precisa ser ajustado
                            row[i] = adjust_text_for_table(cell, col_widths[i])

            # Criando a tabela
            tabela_produto_Natal = Table(produto_Natal, col_widths)

            # Definindo o estilo da tabela
            tabela_produto_Natal.setStyle([
                # Primeira linha: negrito e mesclada
                ('FONTNAME', (0, 0), (7, 0), 'Helvetica-Bold'),  # Aplica negrito na primeira linha inteira
                ('SPAN', (0, 0), (7, 0)),  # Mescla a primeira linha
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),

                # Segunda linha: mesclada
                ('SPAN', (0, 1), (7, 1)),  # Mescla a segunda linha inteira

                # Terceira linha: negrito e cor cinza
                ('FONTNAME', (0, 2), (7, 2), 'Helvetica-Bold'),  # Negrito na terceira linha
                ('BACKGROUND', (0, 2), (7, 2), colors.lightgrey),

                # Ajustes gerais para alinhamento e bordas
                ('SPAN',(6,2),(7,2)),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinha todas as células ao centro
                ('GRID', (0, 0), (-1, 4), 1, colors.black),  # Borda para todas as células
                ('LINEBEFORE', (7, 3), (7, 4), 1, colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centralizando horizontalmente
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centralizando verticalmente
                ('ALIGN', (7, 3), (7, 4), 'LEFT'),
                ('VALIGN', (7, 3), (7, 4), 'BOTTOM'), 
                ('TEXTCOLOR', (7, 3), (7, 4), colors.white),
            ])

            # Adicionando a tabela aos elementos
            espacador = Spacer(1,15)
            elementos.append(espacador)
            elementos.append(tabela_produto_Natal)

            



            #BENEFICIO OPCIONAL
            odonto = [
            ['Benefício opcional','','','',''],
            ['Assinale abaixo o plano pretendido','Plano','Código ANS','Abrangência Geográfica','Segmentação Assistencial'],
            [proposta_dados.get('{{odonto}}', ''), '+ ODONTO PREMIUM ADESÃO', '476.835/16-3', 'NACIONAL', 'ODONTOLÓGICO']
        ]
            col_widths=[120,120,120,120,120]
            for row_index, row in enumerate(odonto):
                if row_index >= 1:  # A partir da segunda linha (índice 1)
                    for i, cell in enumerate(row):
                        if len(cell) > 0:  # Se houver texto na célula
                            # Verificando se o texto é longo e precisa ser ajustado
                            row[i] = adjust_text_for_table(cell, col_widths[i])

            tabela_odonto = Table(odonto,col_widths)

            tabela_odonto.setStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Aplica negrito a toda a primeira linha
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Fundo cinza para a primeira linha (cabeçalho)
                ('SPAN', (0, 0), (4, 0)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Cor do texto no cabeçalho
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Padding inferior
                ('TOPPADDING', (0, 0), (-1, -1), 6),  # Padding superior
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),  # Aplica negrito a toda a primeira linha
                ('BACKGROUND', (0, 0), (-1, 1), colors.lightgrey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centralizando horizontalmente
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centralizando verticalmente
            ])
            elementos.append(PageBreak()) #pular para proxima pagina
            elementos.append(tabela_odonto)


            #Local e data
            local_data = [
            ['Local e data', 'Assinatura do titular/representante legal'],
            [f"{proposta_dados.get('{{LOCAL}}', '')}, {proposta_dados.get('{{DATA}}', '')}", ''],
            ['','ASSBENEF']
        ]

            col_widths=[300,300]
            # Ajustando o texto para todas as células a partir da segunda linha (índice 1)
            for row_index, row in enumerate(local_data):
                if row_index >= 1:  # A partir da segunda linha (índice 1)
                    for i, cell in enumerate(row):
                        if len(cell) > 0:  # Se houver texto na célula
                            # Verificando se o texto é longo e precisa ser ajustado
                            row[i] = adjust_text_for_table(cell, col_widths[i])

            tabela_localData = Table(local_data,col_widths)
            tabela_localData.setStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Aplica negrito a toda a primeira linha
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Fundo cinza para a primeira linha (cabeçalho)
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Cor do texto no cabeçalho
                ('GRID', (0, 0), (-1, 1), 1, colors.black),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Padding inferior
                ('TOPPADDING', (0, 0), (-1, -1), 6),  # Padding superior
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 2), (-1, 2), 'LEFT'),
                ('VALIGN', (0, 2), (-1, 2), 'TOP'),
                ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
                

            ])

            elementos.append(espacador)
            elementos.append(tabela_localData)


            #TABELA COM TOTAIS
            totais = [
            ['Valor por proponente', '', '', ''],
            ['Proponente', 'Idade', 'Plano assistência à SAÚDE', 'Plano assistência à SAÚDE \n com opcional ODONTOLÓGICO'],
            ['Titular', proposta_dados.get('{{idadeTit}}', ''), proposta_dados.get('{{valorSautit}}', ''), proposta_dados.get('{{valorOdotit}}', '')],
            ['Dependente 1', proposta_dados.get('{{idadedep1}}', ''), proposta_dados.get('{{valorSaudep1}}', ''), proposta_dados.get('{{valorOdodep1}}', '')],
            ['Dependente 2', proposta_dados.get('{{idadedep2}}', ''), proposta_dados.get('{{valorSaudep2}}', ''), proposta_dados.get('{{valorOdodep2}}', '')],
            ['Dependente 3', proposta_dados.get('{{idadedep3}}', ''), proposta_dados.get('{{valorSaudep3}}', ''), proposta_dados.get('{{valorOdodep3}}', '')],
            ['Dependente 4', proposta_dados.get('{{idadedep4}}', ''), proposta_dados.get('{{valorSaudep4}}', ''), proposta_dados.get('{{valorOdodep4}}', '')],
            ['Dependente 5', proposta_dados.get('{{idadedep5}}', ''), proposta_dados.get('{{valorSaudep5}}', ''), proposta_dados.get('{{valorOdodep5}}', '')],
            ['Valor Total:', '', proposta_dados.get('{{TotalSau}}', ''), proposta_dados.get('{{Totalodo}}', '')]
        ]
            col_widths=[150,150,150,150]
            for row_index, row in enumerate(totais):
                if row_index >= 1:  # A partir da segunda linha (índice 1)
                    for i, cell in enumerate(row):
                        if len(cell) > 0:  # Se houver texto na célula
                            # Verificando se o texto é longo e precisa ser ajustado
                            row[i] = adjust_text_for_table(cell, col_widths[i])

            tabela_totais = Table(totais,col_widths)

            tabela_totais.setStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Aplica negrito a toda a primeira linha
                ('SPAN', (0, 0), (-1, 0)), #mesclar primeira linha
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Fundo cinza para a primeira linha (cabeçalho)
                ('BACKGROUND', (0, 1), (-1, 1), colors.silver),
                ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Cor do texto no cabeçalho
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Padding inferior
                ('TOPPADDING', (0, 0), (-1, -1), 6),  # Padding superior
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BACKGROUND', (0, 2), (0, 7), colors.silver),
                ('FONTNAME', (0, 2), (0, 7), 'Helvetica-Bold'),
                ('SPAN', (0, 8), (1, 8)),
                ('FONTNAME', (0, 8), (-1, 8), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 8), (-1, 8), colors.lightgrey)
            ]

            )
            elementos.append(espacador)
            elementos.append(tabela_totais)

                # TABELA COM ALERTAS E INSTRUÇÕES
            alertas = [
                ['Atenção: Alteração dos valores', '', '', ''],
                [create_paragraph('Os valores indicados acima sofrerão alteração caso haja reajuste anual do contrato coletivo ou mudança de faixa etária entre a data de assinatura desta Proposta e a data da sua 1ª (primeira) cobrança, observado o disposto no item 14 da página 7 desta Proposta. O valor total deverá ser pago mensalmente.',150), '', '',''],
                [create_paragraph('• Caso o beneficiário solicite o cancelamento do plano de assistência à saúde, o plano opcional odontológico também será cancelado.',150), '', '',''],
            ]

            # Definir as larguras das colunas (podem ser ajustadas conforme necessário)
            col_widths_alerta = [150, 150, 150, 150]


            # Criando a tabela de alertas
            tabela_alertas = Table(alertas, col_widths_alerta)


            # Definindo o estilo da tabela
            tabela_alertas.setStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Aplica negrito à primeira linha
                ('SPAN', (0, 0), (-1, 0)), # Mescla a primeira linha
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Fundo cinza para a primeira linha (cabeçalho)
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Cor do texto no cabeçalho
                ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grade ao redor da tabela
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Padding inferior
                ('TOPPADDING', (0, 0), (-1, -1), 6),  # Padding superior
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinha o texto ao centro
                ('SPAN', (0, 1), (-1, 1)),
                ('SPAN', (0, 2), (-1, 2)),
                
            ])
            
            # Adiciona a tabela ao elemento
            elementos.append(espacador)  # Se necessário, adicione um espaçador antes da tabela
            
            elementos.append(tabela_alertas)

            ciencia = [
                ['Pelo presente, declaro expressamente que, CONCORDO E ESTOU CIENTE QUE:'],
                [create_paragraph('1. Este instrumento é meu Contrato de Adesão (a “Proposta”) ao contrato de plano de assistência à saúde, coletivos por adesão (os “benefícios”), celebrados entre o SINSP/RN e a Hapvida Assistência Médica Ltda. (a “Operadora”) e destinados à população que mantenha vínculo com a minha “Entidade”, que é a Pessoa Jurídica indicada na página 1 desta Proposta. Estou ciente de que o plano de assistência odontológica é um benefício opcional e, se ele for contratado, terei cobertura para os procedimentos odontológicos.',150), '', '', ''],
                [create_paragraph('2. Mantenho vínculo com a Entidade indicada na página 1 desta Proposta, sendo que a documentação comprobatória desse vínculo está sendo entregue por mim ao angariador, no ato da assinatura desta, para que seja conferida pela Entidade de classe, podendo esta Proposta ser recusada em razão da falta de minha elegibilidade.',150), '', '', ''],
                [create_paragraph('3. Estou ciente de que, caso eu seja elegível ao Sindicato dos Trabalhadores do Serviço Público da Administração Direta do Estado do Rio Grande do Norte (SINSP/RN), também poderei incluir dependentes no(s) benefício(s), respeitadas as seguintes condições: Somente serão aceitos como dependentes o meu cônjuge ou meu(minha) companheiro(a) e o(a) meu(-minha) filho(a) de até 21 (vinte e um) anos, ou até 23 (vinte e três) anos, se for universitário(a).',150), '', '', ''],
                [create_paragraph('4. Sou o único responsável pelos documentos e informações fornecidos por mim e por meu(s) dependente(s) sobre toda e qualquer circunstância que possa influir na aceitação desta Proposta, na manutenção ou no valor mensal do(s) benefício(s), sabendo que omissões ou dados errôneos acarretarão a perda de todos os meus direitos, bem como os do(s) meu(s) dependente(s), decorrentes do(s) benefício(s).',150), '', '', ''],
                [create_paragraph('5. Analisada a documentação e as informações prestadas nesta Proposta, de acordo com a legislação vigente, ocorrerá a implantação pela Operadora e o(s) benefício(s) terá(ão) início na data indicada no campo “Início da vigência do(s) benefício(s)”, na página 1 da presente, e tanto eu quanto meu(s) dependente(s) passaremos a ser denominados “beneficiários”.',150), '', '', ''],
                [create_paragraph('6. Assim que eu assumir a condição de beneficiário titular, ficam outorgados à Entidade de Classe amplos poderes para me representar, assim como o(s) meu(s) beneficiário(s) dependente(s), perante a Operadora e outros órgãos, em especial a ANS, no cumprimento e/ou nas alterações deste(s) benefício(s), bem como nos reajustes dos seus valores mensais.',150), '', '', ''],
                [create_paragraph('7. O(s) contrato(s) coletivo(s) firmado(s) entre a Entidade de Classe e a Operadora, contrato(s) que passarei a integrar, será(ão) renovado(s), automaticamente, por prazo indeterminado, desde que não ocorra denúncia, por escrito, no prazo de 60 (sessenta) dias, de qualquer das partes, seja pela Entidade de Classe ou pela Operadora. A vigência dos(s) benefício(s) indicada na página 1 desta Proposta não se confunde com a vigência do(s) contrato(s) coletivo(s). O mês base de aniversário do contrato coletivo é janeiro. Em caso de rescisão desse(s) contrato(s) coletivo(s), a Entidade de Classe me fará a comunicação desse fato em prazo não inferior a 30 (trinta) dias.',150), '', '', ''],
                [create_paragraph('8. Poderei, assim como meu(s) beneficiário(s) dependente(s), utilizar o(s) benefício(s) por meio dos prestadores próprios ou credenciados da Operadora para os planos contratados, respeitadas as condições contratuais de cada plano.',150), '', '', ''],
                [create_paragraph('9. O benefício de plano de assistência à saúde cobrirá as despesas com serviços médico-hospitalares, de acordo com o plano contratado, relacionadas ao “Rol de Procedimentos e Eventos em Saúde” e suas diretrizes, instituídos pela ANS, no tratamento das doenças codificadas na versão 10 da Classificação Estatística Internacional de Doenças e Problemas Relacionados à Saúde (CID-10), da Organização Mundial da Saúde (OMS), observadas as condições gerais deste(s) benefício(s).',150), '', '', ''],
                [create_paragraph('10. Os prazos de carência são os períodos nos quais nem eu nem meu(s) beneficiário(s) dependente(s) teremos direito a determinadas coberturas, mesmo que em dia com o pagamento do(s) benefício(s). Haverá prazos de carência para utilização do(s) benefício(s) conforme tabela indicativa abaixo. Para efeitos de isenção de carências, devem-se observar as normas regulamentares da ANS e a legislação em vigor. Se houver redução de carências, deve-se observar o Aditivo de Redução de Carências que acompanha esta Proposta.',150), '', '', '']
        ]
            
                # Definir as larguras das colunas (podem ser ajustadas conforme necessário)
            col_widths = [150, 150, 150, 150]

            # Criando a tabela de alertas
            tabela_ciencia = Table(ciencia, col_widths)

            # Definindo o estilo da tabela
            tabela_ciencia.setStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Aplica negrito à primeira linha
                ('SPAN', (0, 0), (-1, 0)),  # Mescla todas as células da primeira linha
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Fundo cinza para a primeira linha (cabeçalho)
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Cor do texto no cabeçalho
                #('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grade ao redor da tabela
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Padding inferior
                ('TOPPADDING', (0, 0), (-1, -1), 6),  # Padding superior
                ('SPAN', (0, 1), (-1, 1)),
                ('SPAN', (0, 2), (-1, 2)),
                ('SPAN', (0, 3), (-1, 3)),
                ('SPAN', (0, 4), (-1, 4)),
                ('SPAN', (0, 5), (-1, 5)),
                ('SPAN', (0, 6), (-1, 6)),
                ('SPAN', (0, 7), (-1, 7)),
                ('SPAN', (0, 8), (-1, 8)),
                ('SPAN', (0, 9), (-1, 9)),
                ('SPAN', (0, 10), (-1, 10)),

            ])
            elementos.append(PageBreak())
            # Adiciona a tabela ao elemento
            elementos.append(tabela_ciencia)

            carencias = [
                ['Cobertura','Prazos de carências','Prazos de carências \n (Promoção – Junho de 2025)'],
                [create_paragraph('Atendimentos decorrentes de acidentes pessoais, ocorridos comprovadamente a partir do início de vigência do beneficiário no contrato coletivo, sendo que 24 (vinte e quatro) horas 0 (zero) dias as demais condições de atendimento para urgência/emergência estão em conformidade com a Resolução do CONSU nº 13/1998 e detalhadas no Manual do Beneficiário, consultas médicas e exames laboratoriais simples (exceto Imunológicos, Hormonais e PAC*), na definição estabelecida no Rol De Procedimentos e Eventos em Saúde, da ANS',300),'24 (vinte e quatro) horas','0 (zero) dias'],
                [create_paragraph('Raio-X simples (Radiografia não contrastada) e Eletrocardiograma (ECG).',300),'30 (trinta)dias','0 (zero) dias'],
                [create_paragraph('Cobertura dos seguintes exames e procedimentos: Exames Cardiológicos simples como:Teste Ergométrico, Holter, Ecocardiograma Convencional (exceto PAC*);90 (noventa) dias Exames Oftalmológicos simples como: Curva tensional,Tonometria, Campimetria, Mapeamento de retina (exceto PAC*);Exames Otorrinolaringológicos simples como: Audiometrias e Impedanciometria, Pesquisa de Potencial Evocado (BERA), (exceto PAC*);Exames de Raio-X Contrastado (exceto PAC*);Exames de Ultrassonografia (exceto endoscópicos ou PAC*);Mamografia Convencional e Densitometria Óssea. Internação Hospitalar clinica ou cirúrgica (exceto as relacionadas à patologias de CPT**);Internações em leitos de alta complexidade (exceto as relacionadas à patologias de CPT**);Cirurgias ambulatoriais (exceto as relacionadas à patologias de CPT**);Tomografia Computadorizada,Ressonância Magnética, Endoscopias,Colonoscopia, Procedimentos de Medicina Nuclear, Angiografia (cerebral central e/ou periférica), Procedimentos que necessitam de Hemodinâmica (como Cateterismo Cardiológico), Radioterapia e Quimioterapia, exceto as que forem relacionadas à cobertura parcial temporária, e todos os exames não mencionados nos itens anteriores.',300),'90 (noventa) dias','0 (zero) dias'],
                [create_paragraph('Cobertura dos seguintes exames e procedimentos:Consultas/Sessões e Terapias Simples, Especiais, Isoladas e Multidisciplinares, inclusive, com métodos específicos – ABA, BOBATH e outras - (como psicoterapia,fonoaudiologia, nutricionista, fisioterapia, e terapia ocupacional);',300),'180 (cento e oitenta) dias','180 (cento e oitenta) dias'],
                [create_paragraph('Partos a termo',300),'300 (trezento) dias','300 (trezento) dias'],
                ['','11227 11240','11226 11239']
            ]

            col_widths = [300, 150, 150]
            

            tabela_carencias = Table(carencias,col_widths)
            tabela_carencias.setStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Aplica negrito à primeira linha
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinha o texto no centro em toda a tabela
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Fundo cinza para a primeira linha (cabeçalho)
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Cor do texto no cabeçalho
                ('GRID', (0, 0), (-1, 5), 1, colors.black),  # Grade ao redor da tabela
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Padding inferior
                ('TOPPADDING', (0, 0), (-1, -1), 6),  # Padding superior
                ('WORDWRAP', (0, 1), (-1, -1), True),
                ('ALIGN', (0, 0), (-1, 5), 'CENTER'),  # Centralizando horizontalmente
                ('VALIGN', (0, 0), (-1, 5), 'MIDDLE'),  # Centralizando verticalmente,
                ('VALIGN', (0, 6), (-1, 6), 'TOP'),
                ('TEXTCOLOR', (0, 6), (-1, 6), colors.white)
            ])
            
            elementos.append(PageBreak())
            elementos.append(tabela_carencias)

            ciencia2 = [
            [create_paragraph('11. Doença ou lesão preexistente é aquela da qual eu ou meu(s) proponente(s) dependente(s) saiba(mos) ser portador(es) nesta data, seja por diagnóstico feito ou conhecido, devendo declará-la na “Declaração de Saúde” que acompanha esta Proposta. Havendo na “Declaração de Saúde” a informação de doença(s) ou lesão(ões) preexistente(s), poderá ser aplicada pela Operadora a Cobertura Parcial Temporária (CPT), a qual admite, por um período ininterrupto de 24 (vinte e quatro) meses, contados a partir da data de início de vigência do(s) benefício(s), a suspensão da cobertura para Procedimentos de Alta Complexidade (PAC), leitos de alta tecnologia e procedimentos cirúrgicos, desde que relacionados à(s) doença(s) ou lesão(ões) preexistente(s) declarada(s). Este item não se aplica ao benefício de plano de assistência odontológica, independentemente de sua contratação.', 150), '', '', ''],
            [create_paragraph('12. As características do(s) benefício(s) relativas a: (i) segmentação assistencial; (ii) acomodação em internação; e (iii) abrangência geográfica estão definidas na página 3 desta Proposta, assim como a área de atuação.', 150), '', '', ''],
            [create_paragraph('13. A data de vencimento do pagamento do valor mensal do(s) benefício(s), será dia 10 de cada mês, e sua forma será aquela indicada na página 5 desta Proposta, sendo que a falta de pagamento na data do seu vencimento acarretará multa de 2% (dois por cento) sobre o referido valor mensal do(s) benefício(s), além de juros de 1% (um por cento) ao mês (0,033% ao dia) sobre o valor total do(s) benefício(s). No período de inadimplência, poderá ocorrer a suspensão automática do(s) benefício(s), cuja utilização somente será restabelecida a partir da quitação do(s) valor(es) pendente(s), acrescido(s) dos encargos supracitados, observada a possibilidade de cancelamento, conforme disposto no item 16 desta Proposta.', 150), '', '', ''],
            [create_paragraph('14. Independentemente da data da minha Proposta, o valor mensal do(s) benefício(s) poderá(ão) sofrer os seguintes reajustes: (i) reajuste anual (financeiro e/ou por índice de sinistralidade), que ocorre quando há alteração de custos, utilização dos serviços médicos e uso de novas tecnologias, nunca ocorrendo, porém, em periodicidade inferior a 12 (doze) meses, contados da data de aniversário do contrato coletivo ou da última aplicação do reajuste anual, conforme disposto no item 7 desta proposta, o mês de aniversário do contrato coletivo é janeiro; (ii) reajuste por mudança de faixa etária, que ocorre quando o beneficiário completa uma idade que ultrapassa o limite da faixa etária em que se encontrava, sendo aplicado no mês subsequente ao aniversário do beneficiário, conforme tabela a seguir; (iii) reajuste(s) em outra(s) hipótese(s), que venha(m) a ser autorizado(s) pela ANS, contratado(s) entre a Entidade de Classe e a Operadora, além de previamente comunicado(s) ao beneficiário.', 150), '', '', ''],
        ]
            # Definir as larguras das colunas (podem ser ajustadas conforme necessário)
            col_widths = [150, 150, 150, 150]

            # Criando a tabela de alertas
            tabela_ciencia2 = Table(ciencia2, col_widths)

            # Definindo o estilo da tabela
            tabela_ciencia2.setStyle([
                ('SPAN', (0, 0), (-1, 0)),  # Mescla todas as células da primeira linha
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Cor do texto no cabeçalho
                #('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grade ao redor da tabela
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Padding inferior
                ('TOPPADDING', (0, 0), (-1, -1), 6),  # Padding superior
                ('SPAN', (0, 1), (-1, 1)),
                ('SPAN', (0, 2), (-1, 2)),
                ('SPAN', (0, 3), (-1, 3)),

            ])
            elementos.append(PageBreak())
            # Adiciona a tabela ao elemento
            elementos.append(tabela_ciencia2)
            reajuste = [
                ['Faixa etária','NOSSO PLANO AHO \nCA MUN ENF QC 162','NOSSO PLANO AHO \nCA MUN APT QC 184','NOSSO PLANO AHO \nCA MUN ENF QC 163','NOSSO PLANO AHO \nCA MUN APT QC 185'],
                ['De 0 a 18 anos','0,00%','0,00%','0,00%','0,00%'],
                ['De 19 a 23 anos','0,00%','0,00%','0,00%','0,00%'],
                ['De 24 a 28 anos','0,00%','0,00%','0,00%','0,00%'],
                ['De 29 a 33 anos','0,00%','0,00%','0,00%','0,00%'],
                ['De 34 a 38 anos','0,00%','0,00%','0,00%','0,00%'],
                ['De 39 a 43 anos','0,00%','0,00%','0,00%','0,00%'],
                ['De 44 a 48 anos','0,00%','0,00%','0,00%','0,00%'],
                ['De 49 a 53 anos','0,00%','0,00%','0,00%','0,00%'],
                ['De 54 a 58 anos','0,00%','0,00%','0,00%','0,00%'],
                ['De 59 ou mais','80,00%','80,00%','80,00%','80,00%'],

            ]

            col_widths=[120,120,120,120,120]
            for row_index, row in enumerate(reajuste):
                if row_index >= 1:  # A partir da segunda linha (índice 1)
                    for i, cell in enumerate(row):
                        if len(cell) > 0:  # Se houver texto na célula
                            # Verificando se o texto é longo e precisa ser ajustado
                            row[i] = adjust_text_for_table(cell, col_widths[i])

            tabela_reajuste = Table(reajuste,col_widths)
            tabela_reajuste.setStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Negrito na primeira linha
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Cor do texto no cabeçalho
                ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grade ao redor da tabela
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # Cor de fundo da primeira linha
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Alinhamento horizontal da primeira linha (centrado)
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alinhamento horizontal de todas as outras células (à esquerda)
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Fonte para todas as células
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),  # Alinhamento vertical da primeira linha (centrado)
            ])

            

            elementos.append(tabela_reajuste)

            ciencia3 = [
            [create_paragraph('15. Devo solicitar e informar expressamente à Entidade de Classe toda e qualquer alteração cadastral, tal como a eventual perda de elegibilidade.', 150), '', '', ''],
            [create_paragraph('15.1. Declaro, ainda, estar ciente de que a falta de comunicação da alteração do endereço poderá configurar fraude, ocasionando o cancelamento do(s) benefício(s), bem como as sanções previstas em lei.', 150), '', '', ''],
            [create_paragraph('16. Poderei solicitar o cancelamento do(s) benefício(s) à Entidade de Classe, de acordo com os normativos da legislação em vigor. O(s) benefício(s) poderá(ão) ser cancelado(s) pela Entidade de Classe no caso de perda da minha elegibilidade ou pela falta de pagamento do valor mensal do(s) benefício(s) até o dia 18 de cada mês. A vigência do(s) benefício(s) não se confunde com a data de vencimento de seu pagamento, prevalecendo, para efeito de cancelamento, o período máximo para pagamento, até o dia 17 de cada mês. No caso de cancelamento do(s) benefício(s), haverá minha exclusão e a de meu(s) beneficiário(s) dependente(s), sem prejuízo da cobrança do(s) valor(es) não pago(s), incluídos juros e multa. Caso eu solicite o cancelamento do plano de assistência à saúde, tenho ciência que o plano opcional odontológico também será cancelado.', 150), '', '', ''],
            [create_paragraph('17. Declaro, ainda, estar ciente que a cobrança referente a mensalidade do meu plano de saúde, assim como meu(s) beneficiário(s) dependente(s), será realizada pelas empresas intermediárias indicada pela Entidade de Classe; tais como: Assessoria em Contratação de Planos de Saúde para Servidores Públicos LTDA, CNPJ: 50.976.390/0001-08; Assessoria em Contratação de Planos de Saúde para Servidores do SINSPRN LTDA, CNPJ: 51.493.778/0001-10; Intermediação em Contratação de Planos de Saúde Para Servidores do SINSP-RN LTDA, CNPJ: 52.008.209/0001-03 e Administração de Planos de Saúde Para Servidores do SINSP-RN LTDA, CNPJ: 52.339.972/0001-09.', 150), '', '', ''],
            [create_paragraph('18. Poderei postular nova adesão ao(s) benefício(s), após ser feita nova análise e aceitação das condições de minha elegibilidade e após ter quitado eventuais débitos anteriores. A nova adesão poderá estar sujeita ao cumprimento de novos prazos de carência parciais ou totais, de acordo com os normativos da legislação em vigor.', 150), '', '', ''],
            [create_paragraph('19. Poderei desistir desta Proposta, sem nenhum ônus, desde que tal decisão seja comunicada por escrito à Entidade de Classe no prazo máximo de 7 (sete) dias, contados a partir da data da minha assinatura, autorizando a cobrança do valor mensal do(s) benefício(s), caso esse prazo não seja observado.', 150), '', '', ''],
            [create_paragraph('20. A minha manifestação de vontade, ao aceitar esta Proposta, não poderá ser questionada pelo mero fato de ter sido assinada por meio eletrônico e, para todos os fins de direito, esta Proposta equivale a um documento particular. Declaro, ainda, aceitar como válido o meio tecnológico adotado pela Entidade de Classe para a celebração desta Proposta, uma vez que garantidas a autoria e integridade do documento em forma eletrônica, nos termos da legislação em vigor.', 150), '', '', '']
        ]
            # Definir as larguras das colunas (podem ser ajustadas conforme necessário)
            col_widths = [150, 150, 150, 150]

            # Criando a tabela de alertas
            tabela_ciencia3 = Table(ciencia3, col_widths)

            # Definindo o estilo da tabela
            tabela_ciencia3.setStyle([
                ('SPAN', (0, 0), (-1, 0)),  # Mescla todas as células da primeira linha
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Cor do texto no cabeçalho
                #('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grade ao redor da tabela
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Padding inferior
                ('TOPPADDING', (0, 0), (-1, -1), 6),  # Padding superior
                ('SPAN', (0, 1), (-1, 1)),
                ('SPAN', (0, 2), (-1, 2)),
                ('SPAN', (0, 3), (-1, 3)),
                ('SPAN', (0, 4), (-1, 4)),
                ('SPAN', (0, 5), (-1, 5)),
                ('SPAN', (0, 6), (-1, 6)),
            ])
            elementos.append(PageBreak())
            # Adiciona a tabela ao elemento
            elementos.append(tabela_ciencia3)

            espacador = Spacer(1,10)
            elementos.append(espacador)
            elementos.append(tabela_localData)

                # Gerar o PDF com os elementos
            doc.build(elementos)
            log_contratos.append({
                "nome": proposta_dados.get("{{NOME}}", ""),
                "email": proposta_dados.get("{{EMAIL}}", ""),
                "arquivo": caminho_arquivo
            })
    with open(os.path.join(diretorio, "log_contratos.json"), "w", encoding="utf-8") as f:
        json.dump(log_contratos, f, indent=2, ensure_ascii=False)
# Chamar a função para criar o PDF
if __name__ == "__main__":
    criar_proposta()
