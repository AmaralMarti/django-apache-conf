# django-apache-conf
Script que cria o arquivo ".conf" da sua aplicação Django para ser colocado na configuração do Apache.

Eu não sei se já existe alguma ferramenta que faz isso, se existir eu acredito que ela será mais robusta do que essa minha. Eu fiz 
esse script pra atender uma necessidade minha, talvez você precise adaptá-lo a sua necessidade se quiser usar também.

##Motivo para criá-lo

Eu li esse [post do Guilherme Louro] (http://pythonclub.com.br/configurando-ambiente-django-com-apache-e-mod-wsgi.html) sobre 
como fazer deploy de aplicações django no Apache, testei e funciona muito bem. A parte chata era ter que ficar criando o arquivo
".conf" do Apache na mão, as vezes eu cometia algum erro de digitação e ficava dando erro. Pra resolver isso eu fiz esse script
bem simples para gerar o arquivo pra mim.

##Importante

Para que esse script funcione é preciso observar algumas condições:

  * Você deve estar desenvolvendo um projeto Django
  * Você deve estar usando VirtualEnvWrapper
  * Você deve estar pretendendo fazer deploy da sua aplicação Django no Apache
  * Você deve estar usando Python 2.7
  
## Como funciona

Você deve colocar esse script no diretório do seu projeto Django e executá-lo passando como parâmentro a URL que deseja usar para 
acessar o projeto.

Exemplo:

```
python make_apache_conf.py teste.marti.com.br
```

Fazendo isso o script criará no próprio diretório o arquivo ".conf" que você deve copiar para o diretório do apache:
`/etc/apache2/sites-available/`.
O nome do arquivo ".conf" criado ficará `<nome do projeto>.conf`.

Se eu estivesse trabalhando no projeto chamado `meu_projeto_django` e executasse esse script no seu diretório dessa forma:

```
python make_apache_conf.py teste.marti.com.br
```

O resultado seria a criação do arquivo `meu_projeto_django.conf` com o conteúdo abaixo:

```
WSGIDaemonProcess teste.marti.com.br python-path=/home/henrique/www/meu_projeto_django:/home/henrique/.env/meu_projeto_django/lib/python2.7/site-packages
WSGIProcessGroup teste.marti.com.br

<VirtualHost *:80>
	ServerName teste.marti.com.br
	WSGIScriptAlias / /home/henrique/www/meu_projeto_django/meu_projeto_django/wsgi.py

	<Directory /home/henrique/www/meu_projeto_django>
		<Files wsgi.py>
			Require all granted
			Order allow,deny
			Allow from all
		</Files>
	</Directory>

	Alias /media/ /home/henrique/www/meu_projeto_django/media/
	Alias /static/ /home/henrique/www/meu_projeto_django/static/

	<Directory /home/henrique/www/meu_projeto_django/media>
		Require all granted
		Order allow,deny
		Allow from all
	</Directory>

	<Directory /home/henrique/www/meu_projeto_django/static>
		Require all granted
		Order allow,deny
		Allow from all
	</Directory>

</VirtualHost>
```

## Detalhes sobre o funcionamento

É importante reparar que o script pega automaticamente todos os dados necessários sobre seu projeto e sobre o VirtualEnvWrapper
para poder montar o arquivo adequadamente.

Veja os dados que ele obtém:

  * Nome do seu projeto
  * Caminho do seu projeto
  * Caminho do VirtualEnv que seu projeto usa
  * Caminho onde está o arquivo `wsgi.py` do seu projeto
