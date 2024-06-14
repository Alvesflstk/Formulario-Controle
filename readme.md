# FORMULARIO DE CONTROLE

## Visão Geral

O projeto **FORMULARIO DE CONTROLE** é uma aplicação desktop desenvolvida em Python utilizando a biblioteca `customtkinter` para a interface gráfica e o SQLite para gerenciamento de banco de dados. A aplicação tem como objetivo gerenciar registros de compras, incluindo funcionalidades de inserção, pesquisa, filtragem e atualização de dados de clientes.

## Funcionalidades

### Inserção de Dados
- Formulário para adicionar novas compras com campos como descrição, cliente, quantidade, data, valor, forma de pagamento, etc.
- Opção para calcular valores de parcelas e aplicar descontos.

### Visualização e Pesquisa
- Exibição de registros em uma `Treeview`.
- Função de pesquisa por nome do cliente.
- Filtragem de registros com base no status (Todos, Débito, Pago).

### Atualização de Registros
- Alteração de status dos registros.
- Atualização do número de parcelas.

## Estrutura do Projeto

### `main.py`
Este é o script principal que contém toda a lógica da aplicação.

#### Classe `main`
- `__init__(self)`: Inicializa a janela principal, configurações iniciais, contêineres e componentes.
- `clear(self, window)`: Limpa todos os widgets de um contêiner específico.
- `config(self, width, height)`: Configurações de inicialização da janela (dimensões, posição).
- `call_return(self, choice)`: Calcula o valor das parcelas com base na escolha do número de parcelas.
- `descontar(self)`: Aplica desconto no valor total.
- `inserir_dados(self)`: Insere um novo registro no banco de dados.
- `insert_data(self, tree)`: Insere dados na `Treeview` a partir do banco de dados.
- `combobox_callback(self, choice)`: Controla a ativação/desativação de campos com base na forma de pagamento selecionada.
- `filtros_serch(self, choice)`: Aplica filtros de pesquisa na `Treeview`.
- `pesquisar(self, event)`: Realiza a pesquisa de clientes na `Treeview`.
- `alterar_item(self)`: Altera o status de um registro selecionado.
- `alterar_parcelas(self)`: Altera o número de parcelas de um registro selecionado.

#### Widgets e Layout
- `containers(self)`: Define os contêineres principais da interface.
- `components_nav(self)`: Configura os botões de navegação.
- `form_compra(self)`: Configura o formulário de inserção de dados.
- `ct_clientes(self)`: Configura a interface de visualização e atualização de registros.

## Requisitos

- Python 3.x
- Bibliotecas:
  - `customtkinter`
  - `tkinter`
  - `sqlite3`
  - `PIL (Pillow)`

## Como Executar

1. Certifique-se de ter o Python instalado.
2. Instale as bibliotecas necessárias:
   ```bash
   pip install customtkinter pillow
