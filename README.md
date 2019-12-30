# Hardmobber
Hardmobber é um script desenvolvido para Windows (W10) em Python (3.5+).
Consiste em obter atualizações dos dados do [fórum de promoções do hardmob](https://www.hardmob.com.br/forums/407-Promocoes), notificando o usuário quando aparecerem promoções novas.

### Pré-requisitos
- [Python 3.5+](https://www.python.org/downloads/)

### Instalação
- Extraia o conteúdo do repositório para uma pasta de sua preferência;
- Abra o prompt de comando na pasta especificada;
- Execute o comando ```pip install -r requirements.txt``` e aguarde;
- Execute o script principal: ```python main.py```

Após a execução desses passos, as notificações serão exibidas de acordo com a configuração do seu Windows.

### Flags
São utilizadas flags para controle do script nas primeiras linhas do arquivo `main.py`:

- #### quiet_update: 
Flag para atualizar todos os posts, útil para quando você já visualizou os posts manualmente. Basta alterar o seu valor para `True` e executar o script para a atualização, e depois voltar para `False`.

- #### debug: 
Flag para exibir os comandos `print` que se encontram ao longo do script.