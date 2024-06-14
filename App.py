import customtkinter as i           
import tkinter as t
from tkinter import messagebox , filedialog , ttk ,PhotoImage
import sqlite3
from PIL import Image

i.set_appearance_mode('light')

class main:
    def __init__(self):
        self.window = i.CTk()
        self.window.title('FABIANO-CLIENTES')
        self.config(1335,580)
        self.containers()
        self.components_nav()
        self.form_compra()
        self.window.mainloop()

    def clear(self,window):
        for i in window.winfo_children():
            i.destroy()

    # Configuração Iniciais
            
    def config(self,width,height):
        self.window.resizable(False,False)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    # configs de precificação 
        
    def call_return(self,choice):
        if float(self.entry_valor_real.get()):
            valor_real = float(self.entry_valor_real.get())
            tranf = int(choice)
            divisor = valor_real / tranf
            result = '{:.2f}'.format(divisor)
            self.entry_valorparcelas.delete(0,t.END)
            self.entry_valorparcelas.insert(0,f'{result}')

    def descontar(self):
        try:
            valor_real = float(self.entry_valor_real.get())
            valor_desconto = float(self.entry_descontos.get())             
            result = valor_real - valor_desconto
            self.entry_valor_real.delete(0,t.END)
            self.entry_valor_real.insert(0,f'{float(result)}')
        except ValueError:
            messagebox.showerror(title="ERRO",message='Algum campo NÃO está preenchido')


    def inserir_dados(self):
        conversao_nparcelas = int(self.entry_nparcelas.get())
        descricao = self.entry_descricao.get()
        cliente = self.entry_cliente.get()
        quantidade = int(self.entry_quantidade.get())
        data = self.entry_data.get()
        valor = float(self.entry_valor_real.get())
        pg = self.forma_de_pagamento.get()
        nparcelas = conversao_nparcelas
        valorparcelas = float(self.entry_valorparcelas.get())
        valor_desconto = float(self.entry_descontos.get())
        valor_entrada = float(self.entry_entrada.get())
        status_atual = '❌ DEBITO'


        
        if descricao and cliente and quantidade and data and valor and pg and valorparcelas:
            self.conn = sqlite3.connect('dados.db')
            self.cursor1 = self.conn.cursor()
            try:
                self.cursor1.execute("INSERT INTO metadados (Descricao,Cliente,Quantidade,Data,Forma_pg,Q_Parcelas,Valor_parcelas,Desconto,Entrada,Total,Status) VALUES (?,?,?,?,?,?,?,?,?,?,?)",(descricao,cliente,quantidade,data,pg,nparcelas,valorparcelas,valor_desconto,valor_entrada,valor,status_atual))
                    

                self.entry_descricao.delete(0,t.END)
                self.entry_cliente.delete(0,t.END)
                self.entry_quantidade.delete(0,t.END)
                self.entry_data.delete(0,t.END)
                self.entry_valor_real.delete(0,t.END)          
                self.entry_valorparcelas.delete(0,t.END)
                self.entry_descontos.delete(0,t.END)
                self.entry_entrada.delete(0,t.END)
                self.entry_valorparcelas.delete(0,t.END)
                self.entry_nparcelas.set('0')
                self.forma_de_pagamento.set('FORMA DE PAGAMENTO')

                messagebox.showinfo('PARABENS','Novo Registro')
            except:
                messagebox.showerror(title='ERROR',message="Ocorreu um erro no cadastro ")
            self.conn.commit()


    def insert_data(self,tree):
        conexao = sqlite3.connect('dados.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM metadados')
        for idx, row in enumerate(cursor.fetchall()):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            tree.insert('', 'end', values=row, tags=tag)

        
    
    def combobox_callback(self,choice):
        if choice == "CARD CREDITO" or choice == 'PIX':
            self.entry_nparcelas.configure(state="normal")
            self.entry_valorparcelas.configure(state="normal")
            
        else:
            self.entry_valorparcelas.delete(0,t.END)
            self.entry_nparcelas.configure(state="disabled")
            self.entry_valorparcelas.configure(state="disabled") 

    def filtros_serch(self,choice):
        filtro = self.filtros.get()
        conexao = sqlite3.connect('dados.db')
        cursor = conexao.cursor()

        if filtro == '❌ DEBITO':
            for item in self.frame_pessoas.get_children():
                self.frame_pessoas.delete(item)

            cursor.execute('SELECT * FROM metadados WHERE Status LIKE ?', ('%' + filtro + '%',))
                           
            for idx, row in enumerate(cursor.fetchall()):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.frame_pessoas.insert('', 'end', values=row, tags=tag)

        elif filtro == '✅ PAGO':
            for item in self.frame_pessoas.get_children():
                self.frame_pessoas.delete(item)

            cursor.execute('SELECT * FROM metadados WHERE Status LIKE ?', ('%' + filtro + '%',))
                           
            for idx, row in enumerate(cursor.fetchall()):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.frame_pessoas.insert('', 'end', values=row, tags=tag)

        else:
            for item in self.frame_pessoas.get_children():
                self.frame_pessoas.delete(item)
            self.insert_data(self.frame_pessoas)

    def pesquisar(self,event):
        # Limpar a Treeview
        for item in self.frame_pessoas.get_children():
            self.frame_pessoas.delete(item)

        conexao = sqlite3.connect('dados.db')
        cursor = conexao.cursor()

        termo_pesquisa = self.seach_name.get()

        cursor.execute('SELECT * FROM metadados WHERE Cliente LIKE ?', ('%' + termo_pesquisa + '%',))

        for idx, row in enumerate(cursor.fetchall()):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.frame_pessoas.insert('', 'end', values=row, tags=tag)

        
        conexao.commit()   

    def alterar_item(self):
        new_value = self.mudar_etiqueta.get()
        item_selecionado = self.frame_pessoas.selection()

        if item_selecionado:
            valores_atuais = self.frame_pessoas.item(item_selecionado,'values')   
            conexao = sqlite3.connect('dados.db')
            cursor = conexao.cursor()     
            cursor.execute('UPDATE metadados SET Status=? WHERE id=?', (new_value, valores_atuais[0]))

            conexao.commit()

            for item in self.frame_pessoas.get_children():
                self.frame_pessoas.delete(item)

            self.insert_data(self.frame_pessoas)

    def alterar_parcelas(self):
        new_value = self.atualizar_parcelas.get()
        item_selecionado = self.frame_pessoas.selection()

        if item_selecionado:
            valores_atuais = self.frame_pessoas.item(item_selecionado,'values')
            conexao = sqlite3.connect('dados.db')
            cursor = conexao.cursor()
            cursor.execute('UPDATE metadados SET Q_Parcelas=? WHERE id=?',(new_value,valores_atuais[0]))

            conexao.commit()

            for item in self.frame_pessoas.get_children():
                self.frame_pessoas.delete(item)

            self.insert_data(self.frame_pessoas)

    # Widgets
    def containers(self):
        path = i.CTkImage(light_image=Image.open('dll/path/template.png'),size=(222,580))
        self.nav_bar = i.CTkLabel(self.window,image=path,text='')
        self.nav_bar.place(relheight=1,x=0,y=0)

        self.container = t.Frame(self.window,width=1115,bg='#edf6f9')
        self.container.place(x=223,y=0,relheight=1)

    def components_nav(self):
        self.button_new = i.CTkButton(self.nav_bar,width=140,height=29,text='Nova Compra',fg_color='#000000',font=('Inria Sans',24,'bold'),command=self.form_compra,bg_color='#000000')
        self.clientes = i.CTkButton(self.nav_bar,width=140,height=29,text='Clientes',fg_color='#000000',font=('Inria Sans',24,'bold'),command=self.ct_clientes,border_width=0,border_spacing=0,bg_color='#000000')

        self.button_new.place(x=26,y=30)
        self.clientes.place(x=10,y=70)
    
    def form_compra(self):
        self.clear(self.container)
        self.label_titulo_add = i.CTkLabel(self.container,text='Formulário de Controle',font=('Inria Sans',32,'bold'))
        self.entry_descricao = i.CTkEntry(self.container,placeholder_text='Descrição:',width=457,height=46,corner_radius=8)

        self.entry_cliente = i.CTkEntry(self.container,placeholder_text='Cliente:',width=457,height=46,corner_radius=8)

        self.entry_valor_real = i.CTkEntry(self.container,placeholder_text='Valor Real:',width=275,height=46,corner_radius=8)

        self.entry_quantidade = i.CTkEntry(self.container,placeholder_text='Quantidade:',width=172,height=46,corner_radius=8)

        self.entry_data = i.CTkEntry(self.container,placeholder_text='Data:',width=172,height=46,corner_radius=8)

        
        self.entry_nparcelas = i.CTkComboBox(self.container,width=134,height=46,corner_radius=8,values=['0','1','2','3','4','5','6'],command=self.call_return)

        self.entry_valorparcelas = i.CTkEntry(self.container,placeholder_text='Valor Parcelas:',width=187,height=46,corner_radius=8)

        self.entry_descontos = i.CTkEntry(self.container,placeholder_text='Desconto:',width=383,height=46,corner_radius=8)

        self.entry_entrada = i.CTkEntry(self.container,placeholder_text='Entrada:', width=343,height=46)

        
        self.forma_de_pagamento = i.CTkComboBox(self.container,values=['PIX','A VISTA','CARD CREDITO','CARD DEBITO'],width=383,height=46,command=self.combobox_callback)

        self.forma_de_pagamento.set('FORMA DE PAGAMENTO')

        self.button_inserir = i.CTkButton(self.container,text='Inserir Compra',fg_color='#00B4D8',corner_radius=8,text_color='#FFFFFF',width=228,height=43,font=('Inria Sans',14,'bold'),command=self.inserir_dados)


        self.button_aplicar = i.CTkButton(self.container,text='Aplicar Desconto',fg_color='#00B4D8',corner_radius=8,text_color='#FFFFFF',width=228,height=43,font=('Inria Sans',14,'bold'),command=self.descontar)

        self.label_titulo_add.place(x=30,y=45)
        self.entry_descricao.place(x=30,y=130)
        self.entry_cliente.place(x=30,y=207)
        self.entry_valor_real.place(x=520,y=130)
        self.entry_quantidade.place(x=30,y=290)
        self.entry_data.place(x=215,y=290)
        self.entry_nparcelas.place(y=207,x=520)
        self.entry_valorparcelas.place(x=670,y=207)
        self.forma_de_pagamento.place(x=30,y=378)
        self.button_inserir.place(x=600,y=501)
        self.entry_descontos.place(x=30,y=455)
        self.entry_entrada.place(x=520,y=284)
        self.button_aplicar.place(x=600, y=450)

        self.entry_nparcelas.configure(state="disabled")
        self.entry_valorparcelas.configure(state="disabled")

       

    def ct_clientes(self):
        self.clear(self.container)

        self.buton_editar_data = i.CTkButton(self.container,text='Editar data Pagamento', width=233,height=43,fg_color='#90E0EF')

        self.mudar_etiqueta = i.CTkComboBox(self.container,values=['MUDAR ETIQUETA','❌ DEBITO','✅ PAGO'],width=233,height=48)

        self.seach_name = i.CTkEntry(self.container,width=319,height=48,placeholder_text='Pesquisar por Nome:')

        self.filtros = i.CTkComboBox(self.container,values=['📃 TODOS','❌ DEBITO','✅ PAGO'],width=233,height=48,command=self.filtros_serch)

        self.atualizar_parcelas = i.CTkComboBox(self.container,values=['ATUALIZAR PARCELAS','1','2','3','4','5','6'],width=233,height=48)

        self.gerarNota = i.CTkButton(self.container,text='Gerar Relatório Cliente',width=150,height=30)

        self.button_alterar = i.CTkButton(self.container,text='ALTERAR ETIQUETA', fg_color='#0077B6',corner_radius=8,command=self.alterar_item,width=200,height=40,font=('Inria Sans',16,'bold'))
        self.button_alterar_parcelas = i.CTkButton(self.container,text='ALTERAR PARCELAS', fg_color='#0077B6',corner_radius=8,command=self.alterar_parcelas,width=100,height=40,font=('Inria Sans',16,'bold'))

        self.frame_pessoas = ttk.Treeview(self.container,columns=('Id','Descrição','Cliente','Quantidade','Data','FgPag','Q.Parcelas','R$ PAR','Desconto','Entrada','Total','Status'),show='headings')

        # headings is frame pessoas
        self.frame_pessoas.heading('Id',text='Id')
        self.frame_pessoas.heading('Descrição',text='Descrição')
        self.frame_pessoas.heading('Cliente',text='Cliente')
        self.frame_pessoas.heading('Quantidade',text='Quantidade')
        self.frame_pessoas.heading('Data',text='Data')
        self.frame_pessoas.heading('FgPag',text='FgPag')
        self.frame_pessoas.heading('Q.Parcelas',text='Q.Parcelas')
        self.frame_pessoas.heading('R$ PAR',text='R$ PAR')
        self.frame_pessoas.heading('Desconto',text='Desconto')
        self.frame_pessoas.heading('Entrada',text='Entrada')
        self.frame_pessoas.heading('Total',text='Total')
        self.frame_pessoas.heading('Status',text='Status')

        # configurations in columns frame person
        self.frame_pessoas.column('Id',width=40)
        self.frame_pessoas.column('Descrição',width=150)
        self.frame_pessoas.column('Cliente',width=150)
        self.frame_pessoas.column('Quantidade',width=40)
        self.frame_pessoas.column('Data',width=100)
        self.frame_pessoas.column('FgPag',width=100)
        self.frame_pessoas.column('Q.Parcelas',width=40)
        self.frame_pessoas.column('R$ PAR',width=80)
        self.frame_pessoas.column('Desconto',width=80)
        self.frame_pessoas.column('Entrada',width=80)
        self.frame_pessoas.column('Total',width=60)
        self.frame_pessoas.column('Status',width=80)

        self.seach_name.place(x=20,y=10)
        self.filtros.place(x=340,y=10)
        self.mudar_etiqueta.place(x=20,y=60)
        self.atualizar_parcelas.place(x=260,y=60)
        self.frame_pessoas.place(x=10,y=120,width=1100,height=416)
        self.gerarNota.place(x=20,y=540)
        self.button_alterar.place(x=600,y=10)
        self.button_alterar_parcelas.place(x=820,y=10)

        # configurações de frame Treeview
        self.frame_pessoas.tag_configure('evenrow', background='#cddafd')  
        self.frame_pessoas.tag_configure('oddrow', background='#FFFFFF')  
        self.insert_data(self.frame_pessoas)
        self.seach_name.bind('<KeyRelease>',self.pesquisar)
        
        

if __name__ == '__main__':
    main() 