from Modulos import *
from ValidEntry import *
from Funcao_BD import *
from Relatorio import *

root = Tk()     #criação da janela principal usando as bibliotecas gráficas 

class GradientFrame(Canvas):         
#efeito gradiente no frame que herda do widget canvas
#parent: o widget "pai" (normalmente uma janela ou frame).
#**kwargs: permite passar parâmetros adicionais para o Canvas (como largura, altura, borda etc).
    def __init__(self, parent, color1="#C6CCFF", color2="gray35", **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1       #passando parametros
        self._color2 = color2
#Sempre que o Canvas for redimensionado (evento <Configure>), a função _draw_gradient será chamada. 
# Isso garante que o gradiente sempre ocupe todo o espaço do canvas.        
        self.bind("<Configure>", self._draw_gradient)  
    def _draw_gradient(self, event= None):  #função que desenha o gradiente no widget
        self.delete("gradient")             #Remove todas as linhas desenhadas anteriormente com a tag "gradient", para evitar sobreposição.
        width = self.winfo_width()          #Obtém a largura e altura atual do Canvas
        height = self.winfo_height()
        limit = width
        (r1, g1, b1) = self.winfo_rgb(self._color1) #converte cores de string para rgb
        (r2, g2, b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1)/limit                #Calcula a "velocidade" com que os componentes de cor (R, G, B) deve mudar por pixel horizontal para gerar o gradiente.
        g_ratio = float(g2-g1)/limit
        b_ratio = float(b2-b1)/limit

        for i in range(limit):  #Para cada pixel horizontal i, calcula os valores RGB intermediários da cor naquele ponto.
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)   #Formata os valores de cor em hexadecimal no padrão esperado por tkinter
    #Desenha uma linha vertical (do topo até a base do canvas) na posição i, com a cor calculada. A tag "gradient" permite identificá-la depois        
            self.create_line(i, 0, i, height, tags=("gradient",), fill=color)
        self.lower("gradient")   

class EntPlaceHold(Entry):  #classe para manipular frases de auxílio para o usuário
    def __init__(self, master=None, placeholder='PLACEHOLDER', color='gray'):
        super().__init__(master)

        self.placeholder = placeholder       #instanciamento do placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind('<FocusIn>' , self.foc_in)   #quando o mouse passar por cima da entry, irá realizar uma função usando o bind
        self.bind('<FocusOut>', self.foc_out)
        self.put_placeholder()               #função para inserir um texto como padrão

    def put_placeholder(self):              
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):       #função do bind quando o mouse passar dentro do entry
        if self['fg']==self.placeholder_color:
            self.delete('0', 'end')       #apaga a informação
            self['fg']=self.default_fg_color

    def foc_out(self, *args):      #função do bind quando o mouse passar fora do entry
        if not self.get():   #se caso não tiver a informação chamará a função put_placeholder       
            self.put_placeholder()    

class Aplication(Funcao, Relatorios, Validadores):   #informar que a classe aplication pode usar a classe Funcao
    def __init__(self):
        self.root = root        #equivalência para a classe root, é preciso nomeá-la
        self.tela()             #chamando a função tela
        self.validaEntradas()   #chamando função de validar entradas do código digitado pelo usuário
        self.frameTela()        #chamando a função frame
        self.janelaFrame1()     #chamando as funções do frame1
        self.janelaFrame2()     #chamando as funções do frame2
        self.tabelas()          #irá criar a tabela caso não exista
        self.select_lista()     #exibe a lista atualizada ao abrir o sistema        
        self.Menus()            #tela de menu
        root.mainloop()         #responsável por abrir a janela             

    def tela(self):         #configuração de tela    
        self.root.title("Cadastro de Clientes")
        self.root.configure(background='#1e3743')
        self.root.geometry("788x588")    #dimensão da janela horizontal x vertical
        self.root.resizable(True, False)              #aumenta ou diminua, horizontal x vertical
        self.root.maxsize(width=900, height=700)      #tamanho máximo da tela
        self.root.minsize(width=500, height=300)      #tamanho mínimo da tela

    def validaEntradas(self):
        self.vcmd2 = (self.root.register(self.validate_entry2), "%P")   #abstração para usar a função dentro da entry 
    #validate="key", validatecommand="self.vcmd2" são introduzidos no Entry.       

#posicionamento do frame dentro da tela horizontal x vertical. Valor entre 0 a 1. 
#relx é o valor da esquerda para a direita e rely é valor de cima para baixo       
#relwidth é Largura da direita para esquerda e relheight é o valor de baixo para cima.
#place faz com que o tamanho se torne relativo dentro da tela    
    def frameTela(self):
        self.frame_1 = Frame(self.root, bd=4, bg="#a4a8aa", highlightbackground='green', highlightthickness=4)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)          

        self.frame_2 = Frame(self.root, bd=4, bg='#a4a8aa', highlightbackground='green', highlightthickness=4)  
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def janelaFrame1(self):    #botão dentro do frame_1. bd é uma sombra para o botão 
    #Adicionando abas no frame1
        self.abas = ttk.Notebook(self.frame_1)        
        self.aba1 = Frame(self.abas)
        self.aba2 = GradientFrame(self.abas)
        self.aba1.configure(background='#a4a8aa')
        self.aba2.configure(background="lightgray")
        self.abas.add(self.aba1, text="Aba 1")
        self.abas.add(self.aba2, text="Aba 2")
        self.abas.place(relx=0, rely=0, relheight=0.96, relwidth=0.98)          
    #molduras nos botões
        self.canvas_bt = Canvas(self.aba1, bd=0, bg='black', highlightbackground='gray', highlightthickness=3) 
        self.canvas_bt.place(relx=0.19, rely=0.08, relheight=0.14, relwidth=0.23)  
    #efeito do botão é activeforeground e activeforeground        
        self.btnLimpar = Button(self.aba1, text='Limpar', bd=3, bg="#6d6e9c", activebackground='#108ecb', activeforeground="white", fg='white', font=('verdana', 8, 'bold'), command=self.limpa_tela )
        self.btnLimpar.place(relx=0.2 ,rely=0.1, relheight=0.1, relwidth=0.1) 
        self.btnBuscar = Button(self.aba1, text='Buscar', bd=3, bg="#6d6e9c", activebackground='#108ecb', activeforeground="white", fg='white', font=('verdana', 8, 'bold'), command=self.busca_cliente)
        self.btnBuscar.place(relx=0.31 ,rely=0.1, relheight=0.1, relwidth=0.1)   
        self.btnNovo = Button(self.aba1, text='Cadastrar', bd=3, bg="#6d6e9c",fg='white', font=('verdana', 8, 'bold'), command=self.insert)
        self.btnNovo.place(relx=0.62 ,rely=0.1, relheight=0.1, relwidth=0.1) 
        self.btnAlterar = Button(self.aba1, text='Alterar', bd=3, bg="#6d6e9c",fg='white', font=('verdana', 8, 'bold'), command=self.altera_cliente)
        self.btnAlterar.place(relx=0.73 ,rely=0.1, relheight=0.1, relwidth=0.1) 
        self.btnApagar = Button(self.aba1, text='Apagar', bd=3, bg="#6d6e9c",fg='white', font=('verdana', 8, 'bold'), command=self.deleta_cliente)
        self.btnApagar.place(relx=0.84 ,rely=0.1, relheight=0.1, relwidth=0.1) 
    #label e entrada do código
        self.lblCodigo = Label(self.aba1, text='Código', bg='#a4a8aa', font=('verdana', 8, 'bold'))
        self.lblCodigo.place(relx=0.05, rely=0.02)
        self.codigoEntry = Entry(self.aba1, validate="key", validatecommand=self.vcmd2, bg="#84878b", font=('verdana', 8, 'bold'))      #Chamando o txt para o usuário digitar
        self.codigoEntry.place(relx=0.05, rely=0.1, relheight=0.1, relwidth=0.08)                #relwidth determina o tamanho do label
        #self.codigoEntry.config(state="disabled")                                                # Desabilita o campo (o usuário não pode digitar)
    #label e entrada do nome
        self.lblNome = Label(self.aba1, text='Nome', bg='#a4a8aa', font=('verdana', 8, 'bold'))
        self.lblNome.place(relx=0.05, rely=0.30)
        self.nomeEntry = EntPlaceHold(self.aba1, 'Digite o nome do cliente')
        self.nomeEntry.place(relx=0.05, rely=0.38, relheight=0.1, relwidth=0.89)
    #label e entrada do telefone
        self.lblTelefone = Label(self.aba1, text='Telefone', bg='#a4a8aa', font=('verdana', 8, 'bold'))
        self.lblTelefone.place(relx=0.05, rely=0.60)
        self.telefoneEntry = EntPlaceHold(self.aba1, 'Digite um telefone')
        self.telefoneEntry.place(relx=0.05, rely=0.68, relheight=0.1, relwidth=0.30)    
    #label e entrada do nome de cidade
        self.lblCidade = Label(self.aba1, text='Cidade', bg='#a4a8aa', font=('verdana', 8, 'bold'))
        self.lblCidade.place(relx=0.36, rely=0.60)
        self.cidadeEntry = Entry(self.aba1, font=('verdana', 8, 'bold'))
        self.cidadeEntry.place(relx=0.36, rely=0.68, relheight=0.1, relwidth=0.58)
     #dropdown
        self.Tipvar = StringVar(self.aba2)
        self.TipV = ("Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)")
        self.Tipvar.set("Solteiro(a)")    #Opção padrão que sempre aparece na caixa
        self.popupMenu = OptionMenu(self.aba2, self.Tipvar, *self.TipV) #variável para option menu em que chama a lista
        self.popupMenu.place(relx=0.1, rely=0.2, relheight=0.2, relwidth=0.2)
        self.estado_civil = self.Tipvar.get()   #Coletando a informação que o usuário escolheu  

        self.btnJanela2 = Button(self.aba2,text="Janela 2", bd=3, bg="#6d6e9c", activebackground='#108ecb', activeforeground="white", fg='white', font=('verdana', 8, 'bold'), command=self.janela2)        
        self.btnJanela2.place(relx=0.1 ,rely=0.5)

    #calendário
        self.bt_calendario = Button(self.aba2, text="Data", command=self.calendario)    
        self.bt_calendario.place(relx=0.5, rely=0.02)
        self.dataEntry = Entry(self.aba2, width=10)
        self.dataEntry.place(relx=0.5,rely=0.17)

    def janelaFrame2(self): 
    #criando tabela. Height configura a posição verticalmente e columns especifica as colunas        
        self.listaCli = ttk.Treeview(self.frame_2, columns=("col1", "col2", "col3","col4"), show='headings')
    #especificando o cabeçalho de cada coluna criada. É iniciada com valor Zero    
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Código")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Telefone")
        self.listaCli.heading("#4", text="Cidade")
    #especificando o tamanho em relação das colunas
        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)    
        self.listaCli.place(relx=0.01, rely=0.01, relheight=0.95, relwidth=0.95)  
        
    #barra de rolagem    
        self.scroolList = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolList.set)    #barra de rolagem (yscroll) pertence a scroolList
        self.scroolList.place(relx=0.95, rely=0.01, relheight=0.95, relwidth=0.04) 
    #chamando a função double click. Bind é a interação com a lista. Double-1 significa double click    
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)     

    def Menus(self):    #menu de opções
        menubar = Menu(self.root)           
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)    #Variável para cada Menubar
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()     #função para fechar o sistema

        menubar.add_cascade(label= "Opções", menu= filemenu)    #Criando nomes para cada menu
        menubar.add_cascade(label= "Relatórios", menu= filemenu2)

        filemenu.add_command(label="Sair", command=Quit)    #chamando a função que fecha a janela
        filemenu.add_command(label="Limpa Cliente", command= self.limpa_tela)
        filemenu2.add_command(label="Ficha do cliente", command= self.gerarRelatorioCliente)

    def janela2(self): 
        self.root2 = Toplevel() #Toplevel é uma classe do Tkinter que cria uma nova janela (uma "janela filha") independente da janela principal.
        self.root2.title("Javela 2")
        self.root2.configure(background="lightblue")
        self.root2.geometry("400x200")
        self.root2.resizable(False, False)   #janela estática, tamanho fixo
        self.root2.transient(self.root)      #janela 2 está dentro da janela principal
        self.root2.focus_force               #forçando o foco para que a janela 2 fique a frente
        self.root2.grab_set()                #impede que seja digitando algo na primeira janela
                       
Aplication()    #chamando a classe para exibir a janela