from flask import Flask, redirect, render_template, request, session, url_for

from tarefa import models
from tarefa.models import buscar_livro, buscar_livros, resenhas_do_livro, usuarios


app = Flask(__name__, template_folder="template")
app.secret_key = "chave-da-biblioteca"


@app.get("/")
def index():
	return render_template("principal.html", livros=buscar_livros())


@app.route("/login", methods=["GET", "POST"])
def login():
	mensagem = None

	if request.method == "POST":
		nome = request.form.get("nome", "")
		senha = request.form.get("senha", "")

		for usuario in usuarios:
			if usuario["nome"] == nome and usuario["senha"] == senha:
				session["usuario"] = nome
				return redirect(url_for("index"))

		mensagem = "Nome ou senha incorretos."

	return render_template("login.html", mensagem=mensagem)


@app.get("/logout")
def logout():
	session.clear()
	return redirect(url_for("index"))


@app.get("/livro/<int:livro_id>")
def detalhe_livro(livro_id):
	livro = buscar_livro(livro_id)
	if livro is None:
		return "Livro não encontrado", 404

	return render_template(
		"livro.html",
		livro=livro,
		resenhas=resenhas_do_livro(livro_id),
	)


@app.route("/livro/<int:livro_id>/resenhar", methods=["POST"])
def resenhar(livro_id):
	if "usuario" not in session:
		return redirect(url_for("login"))

	livro = buscar_livro(livro_id)
	if livro is None:
		return "Livro não encontrado", 404

	texto = request.form.get("texto", "")
	nota = request.form.get("nota", "1")

	if texto.strip() == "":
		return redirect(url_for("detalhe_livro", livro_id=livro_id))

	nova_resenha = {
		"id": models.proximo_id_resenha,
		"livro_id": livro_id,
		"usuario": session["usuario"],
		"texto": texto,
		"nota": int(nota),
	}
	models.resenhas.append(nova_resenha)
	models.proximo_id_resenha += 1

	return redirect(url_for("detalhe_livro", livro_id=livro_id))


if __name__ == "__main__":
	app.run(debug=True)
