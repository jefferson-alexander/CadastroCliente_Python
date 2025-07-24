from ValidEntry import *
from Modulos import *
from Relatorio import *

class Funcao():
    def variaveis(self):
        self.codigo   = self.codigoEntry.get()
        self.nome     = self.nomeEntry.get()
        self.telefone = self.telefoneEntry.get()
        self.cidade   = self.cidadeEntry.get()

    def limpa_tela(self):       #irá limpar as informações de entrada do usuário
        self.codigoEntry.delete(0, END)
        self.nomeEntry.delete(0, END)
        self.telefoneEntry.delete(0, END)
        self.cidadeEntry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.db")  #criando e conectando ao banco clientes.bd
        self.cursor = self.conn.cursor()            #cursor faz a execução da query e os parametros

    def desconecta_bd(self):
        self.conn.close()    

    def tabelas(self):
        self.conecta_bd()        #funçao que conecta ao BD e cria a tabela clientes   
        print("Conectando ao Banco de Dados")
    #função para executar o SQL  
    # para funcionar o autoincrement INTEGER e AUTOINCREMENT deve ser exatamente descrito dessa forma      
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS clientes
                             (cod INTEGER PRIMARY KEY AUTOINCREMENT, nome_cliente varchar(40) not null, telefone int(12), cidade varchar(40));""")
        self.conn.commit()   #salvando e validando a criação da tabela
        print("Banco de dados criado com sucesso")    

    def insert(self):
        self.variaveis()     #chamando a função de variáveis  
    #tratando condição se caso o usuário não digitar
        if self.nomeEntry.get()  == "": #caso o campo esteja vazio
            messagebox.showinfo("Aviso", "Para cadastrar um novo cliente é preciso digitar o nome!" )
        elif self.telefoneEntry.get() == "":
            messagebox.showinfo("Aviso", "Para cadastrar um novo cliente é preciso digitar o telefone!" )
        elif self.cidadeEntry.get() == "":  
            messagebox.showinfo("Aviso", "Para cadastrar um novo cliente é preciso digitar a cidade!" )
        else:              
            self.conecta_bd()    #chamando a função conecta_db para conectar ao BD
            self.cursor.execute("""INSERT INTO clientes (nome_cliente, telefone, cidade)
                                VALUES(?, ?, ?)""", (self.nome, self.telefone, self.cidade))
            self.conn.commit()
            self.desconecta_bd()           
            self.select_lista()  #depois de inserir um novo registro irá realizar o select da lista
            self.limpa_tela()    #limpa os dados digitados

    def select_lista(self): 
    #Caso tenha algo na lista vai deletar, depois *self get irá exibir novamente
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()          
        lista = self.cursor.execute("SELECT * FROM clientes ORDER BY cod;")    
        for i in lista:
            self.listaCli.insert("", END, values=i)
            
        self.desconecta_bd()    #A conexão é fechada depois de realizar o for loop

    def OnDoubleClick(self, event):  #função para coletar as informações do Treeview usando o duplo clique. Realiza o evento de doubleclick
        self.limpa_tela()
        self.listaCli.selection()   #selecionando as informações da lista
        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')    #seleciona os itens que receberem o dublo clique
            self.codigoEntry.insert(END, col1)                          #pega as informações que o Entry receberá
            self.nomeEntry.insert(END, col2)
            self.telefoneEntry.insert(END, col3)
            self.cidadeEntry.insert(END, col4)

    def deleta_cliente(self):
        self.variaveis()     #chamando a função de variáveis   
        self.conecta_bd()
        self.cursor.execute("DELETE FROM clientes WHERE cod = ?", (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista() 

    def altera_cliente(self):
        self.variaveis()    #chamando função de variáveis
        self.conecta_bd()
        self.cursor.execute("""UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade =? 
                            WHERE cod = ? """, (self.nome, self.telefone, self.cidade, self.codigo,))   #codigo deve ficar por último
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())      #limpando a lista    
        self.nomeEntry.insert(END, '%')  #porcentagem busca tudo que estiver digitado, como se fosse um complemento
        nome = self.nomeEntry.get()
    #Like faz a pesquisa onde tem a informação no cliente ordenado ascedente por nome
    #porcentagem é o código usado para não precisar digitar toda informação a ser buscada
        self.cursor.execute("SELECT * FROM clientes WHERE nome_cliente LIKE '%s' ORDER BY  nome_cliente ASC" % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:  #insere a busca dentro da lista
            self.listaCli.insert("", END, values=i)
        self.limpa_tela()    
        self.desconecta_bd()

    def calendario(self):
        self.calendario1 = Calendar(self.aba2, fg="gray75", bg="blue", font=("Times", '9', 'bold'), locale='pt_br') #locale configura a data pela regiao
        self.calendario1.place(relx=0.5, rely=0.15)
        self.calData = Button(self.aba2, text="Inserir Data", command=self.print_cal)
        self.calData.place(relx=0.56, rely=0.02, height=25, width=100) 

    def print_cal(self): #inserindo a data na entry
        dataIni = self.calendario1.get_date()
        self.calendario1.destroy()              #fecha a janela
        self.dataEntry.delete(0, END)           #deleta o que tiver escrito para não sobrescrever
        self.dataEntry.insert(END, dataIni)     #insert, joga a informação do calendario1 para o dataIni
        self.calData.destroy()                  #destroi o botão que insere a data
