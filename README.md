1-  Model esta no arquivo models.py, Controller esta no app.py, View esta nos arquivos HTML.Se a logica de acesso aos dados fosse escrita diretamente nas rotas, o app.py ficaria mais complicado e misturaria responsabilidades.

2-  Usamos url_for porque ele gera o endereço da rota a partir do nome da função

3-  A session representa os dados do usuario que esta logado durante a navegação no sistema.A rota de resenhar precisa verificar a session antes de gravar porque é necessario saber qual usuario esta fazendo a resenha e impedir que alguem sem permissão registre uma opinião.