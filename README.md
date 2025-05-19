# project-test-flask-crud

Este projeto é uma API RESTful de CRUD de usuários desenvolvida com Flask e SQLite.

## Funcionalidades

- Criar usuário (`POST /users`)
- Listar todos os usuários (`GET /users`)
- Buscar usuário por ID (`GET /users/<id>`)
- Atualizar usuário (`PUT /users/<id>`)
- Deletar usuário (`DELETE /users/<id>`)

## Estrutura do Projeto

```
app/
  routes.py
  models.py
  user_repository.py
  database.py
tests/
  routes_test.py
run.py
requirements.txt
```

## Como executar

1. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Inicie o servidor:**
   ```sh
   python run.py
   ```

   O servidor estará disponível em `http://127.0.0.1:5000/`.

## Como rodar os testes

Execute no terminal:

```sh
python -m unittest -v tests/routes_test.py
```

## Exemplo de requisição

### Criar usuário

```http
POST /users
Content-Type: application/json

{
  "name": "Lucas"
}
```

### Resposta esperada

```json
{
  "id": 1,
  "name": "Lucas"
}
```

## Observações

- O nome do usuário deve ter entre 2 e 50 caracteres e conter apenas letras e espaços.
- O projeto utiliza SQLite para persistência dos dados.
- Os testes unitários cobrem todos os endpoints principais.

---