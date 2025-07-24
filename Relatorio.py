from Funcao_BD import *
from Modulos import *
from ValidEntry import*

class Relatorios():
    def printClient(self):      #função que chama o navegador para abrir o pdf
        webbrowser.open("cliente.pdf")      #cria um arquivo PDF

    def gerarRelatorioCliente(self):    #função que gera o relatório de acordo com a digitação do usuário. 
        self.c = canvas.Canvas("cliente.pdf")   
        self.codigoRel   = self.codigoEntry.get()
        self.nomeRel     = self.nomeEntry.get()
        self.telefoneRel = self.telefoneEntry.get()
        self.cidadeRel   = self.cidadeEntry.get()
    #desenhando string na tela largura de espaçamento da esquerda para a direita, cima para baixo
        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha de cliente')
    #corpo do relatório
        self.c.setFont("Helvetica-Bold", 16)
        #self.c.drawString(50, 700, 'Código: '   + self.codigoRel)    Essa forma concatena a informação do cliente mas é puxado em negrito
        self.c.drawString(50, 700, 'Código: ')    
        self.c.drawString(50, 670, 'Nome: '  )    
        self.c.drawString(50, 640, 'Telefone: ')    
        self.c.drawString(50, 610, 'Cidade: ' )
        self.c.setFont("Helvetica", 16)     #Trazendo as informações do cliente sem o negrito        
        self.c.drawString(150, 700, self.codigoRel)    
        self.c.drawString(150, 670, self.nomeRel)    
        self.c.drawString(150, 640, self.telefoneRel)    
        self.c.drawString(150, 610, self.cidadeRel)
    #rect cria linhas, espaços, molduras
    #Largura esquerda para direita, abaixo da informação de cidade, comprimento, espeçura da linha, fill é o preenchimento, strock é para aparecer
        self.c.rect(20, 550, 550, 200, fill=False, stroke=True)  
        self.c.showPage()
        self.c.save()
        self.printClient()