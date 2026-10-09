# Mini Biblioteca

Projeto Django de uma biblioteca com livros, autores e categorias.

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Lista de livros: http://127.0.0.1:8000/
- Página do autor: http://127.0.0.1:8000/autores/1/
- Admin: http://127.0.0.1:8000/admin/

## Modelo de dados

| Model    | Campos                                                                  |
|----------|-------------------------------------------------------------------------|
| Author   | `name` (obrigatório), `nationality` (opcional)                          |
| Category | `name` (único)                                                          |
| Book     | `title`, `author` (FK), `categories` (M2M, opcional), `year_of_publication`, `available` |

Relacionamentos:

- **Author 1 — N Book** (`related_name="books"`): `author.books.all()`.
- **Book N — N Category** (`related_name="books"`): um livro pode ter várias
  categorias ou nenhuma (`blank=True`).

## Decisão: `on_delete=models.PROTECT` em `Book.author`

**O que acontece se alguém tentar apagar um autor que tem livros?**
O Django **bloqueia** a exclusão e lança `ProtectedError`. No admin, aparece uma
mensagem explicando quais livros impedem a remoção.

**Por que PROTECT e não as outras opções?**

- `CASCADE` apagaria todos os livros do autor junto com ele. Em uma biblioteca,
  um clique errado destruiria o acervo (e o histórico) de uma vez. É perigoso demais.
- `SET_NULL` deixaria livros sem autor, mas o autor é obrigatório (`null=False`),
  então isso quebraria a regra de negócio e deixaria dados incompletos.
- `SET_DEFAULT` / `SET_*` exigiriam inventar um autor "padrão" (ex.: "Desconhecido"),
  o que esconde o problema em vez de resolvê-lo.
- `PROTECT` obriga a decisão consciente: antes de apagar o autor, é preciso
  apagar os livros dele ou passá-los para outro autor. Os dados nunca ficam
  inconsistentes nem são perdidos por acidente.

## Migrações (como os dados antigos foram preservados)

Antes, `Book.author` era um texto. Trocar direto para ForeignKey perderia os
dados, então a mudança foi feita em 3 etapas:

1. `0002` — cria `Author`, `Category` e um campo temporário `author_new` (FK, aceita nulo).
2. `0003` — migração de dados: para cada nome de autor em texto, cria **um**
   `Author` (sem duplicar) e liga os livros a ele.
3. `0004` — remove o campo de texto, renomeia `author_new` para `author` e o torna obrigatório.

## Admin

- **Book**: lista com título, autor, ano e disponibilidade; busca por título e
  nome do autor (`author__name`); filtros por disponibilidade e categoria;
  seletor `filter_horizontal` para categorias.
- **Author**: os livros do autor são editados na própria página dele (inline).
- **Category**: cadastro simples com busca por nome.

## Views e URLs

| URL                  | View            | Descrição                                           |
|----------------------|-----------------|-----------------------------------------------------|
| `/`                  | `book_list`     | Lista de livros; o autor é link para a página dele  |
| `/autores/<id>/`     | `author_detail` | Autor e todos os seus livros; 404 se não existir    |

## Testes

```bash
python manage.py test
```
