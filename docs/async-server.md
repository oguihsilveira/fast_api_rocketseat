# Servidores Assíncronos no FastAPI

## 1. Contexto da aula

Depois de entender o conceito de **assincronismo em Python**, o próximo passo é compreender como esse conceito aparece na execução de uma API.

No FastAPI, não basta apenas escrever funções com `async def`. Para que a aplicação consiga lidar com requisições de forma assíncrona, ela também precisa ser executada por um **servidor compatível com assincronismo**.

É nesse ponto que entram servidores como o **Uvicorn** e o **Hypercorn**.

---

## 2. O que é um servidor em uma aplicação FastAPI?

O servidor é o componente responsável por **rodar a aplicação web** e receber as requisições feitas pelos usuários ou sistemas externos.

Por exemplo, quando acessamos uma rota como:

```text
http://localhost:3001/saudar/Guilherme
```

quem recebe essa requisição primeiro é o servidor. Depois, ele encaminha a requisição para a aplicação FastAPI executar a rota correspondente.

No projeto estudado, o servidor usado é o **Uvicorn**:

```python
import uvicorn

uvicorn.run(
    "app:app",
    host="0.0.0.0",
    port=3001,
    reload=True
)
```

---

## 3. Tipos de servidores em Python

Em Python, existem dois tipos principais de servidores para aplicações web:

1. **WSGI**
2. **ASGI**

A diferença principal entre eles está na forma como lidam com as requisições.

---

## 4. WSGI

WSGI significa:

```text
Web Server Gateway Interface
```

Servidores WSGI são servidores **síncronos**.

Isso significa que eles trabalham de forma mais tradicional: uma tarefa tende a ser processada de cada vez dentro daquele fluxo de execução. Se uma operação demora, como uma consulta externa ou leitura de arquivo, aquele fluxo pode ficar aguardando até a tarefa terminar.

Isso não significa que WSGI seja ruim. Ele é muito usado em aplicações Python e funciona bem em vários contextos.

Um exemplo de servidor WSGI citado na aula é o **Waitress**.

O Waitress é bastante utilizado com aplicações feitas em **Flask**, que é outro framework web em Python.

Exemplo conceitual:

```text
Flask + Waitress
```

Nesse caso, o servidor Waitress executa a aplicação Flask usando o padrão WSGI.

---

## 5. ASGI

ASGI significa:

```text
Asynchronous Server Gateway Interface
```

Servidores ASGI são servidores preparados para trabalhar com **assincronismo**.

Eles permitem que a aplicação aproveite recursos como:

- funções assíncronas;
- `async def`;
- `await`;
- execução concorrente;
- loop de eventos;
- melhor tratamento de múltiplas requisições.

No contexto do FastAPI, o ASGI é especialmente importante porque o framework foi pensado para funcionar muito bem com o assincronismo do Python.

Exemplos de servidores ASGI:

```text
Uvicorn
Hypercorn
```

---

## 6. Uvicorn

O **Uvicorn** é um dos servidores ASGI mais utilizados para executar aplicações FastAPI.

Ele é o servidor usado no projeto da aula.

Exemplo:

```python
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/saudar/{nome}")
async def saudar(nome: str):
    return {"mensagem": f"Olá, {nome}"}


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=3001,
        reload=True
    )
```

Nesse exemplo, o Uvicorn é responsável por iniciar o servidor e executar a aplicação FastAPI.

---

## 7. Entendendo o `"app:app"`

No trecho:

```python
uvicorn.run("app:app")
```

a string `"app:app"` possui dois significados:

```text
app:app
```

O primeiro `app` representa o nome do arquivo Python:

```text
app.py
```

O segundo `app` representa a variável criada dentro do arquivo:

```python
app = FastAPI()
```

Portanto:

```python
"app:app"
```

significa:

```text
No arquivo app.py, procure a variável app.
```

---

## 8. Loop de eventos

Nas aulas anteriores, o assincronismo foi demonstrado com `asyncio`.

Exemplo:

```python
import asyncio


async def tarefa(nome, duracao):
    print(f"tarefa [{nome}] iniciando...")
    await asyncio.sleep(duracao)
    print(f"tarefa [{nome}] terminou...")


async def main():
    await asyncio.gather(
        tarefa(1, 3),
        tarefa(2, 6)
    )


if __name__ == "__main__":
    asyncio.run(main())
```

Nesse exemplo, foi necessário chamar:

```python
asyncio.run(main())
```

Esse comando inicia o **loop de eventos** do Python.

O loop de eventos é o mecanismo que organiza e executa funções assíncronas. Ele permite que uma tarefa seja pausada em um `await`, enquanto outra tarefa continua sendo executada.

---

## 9. O papel do servidor ASGI no loop de eventos

Em uma aplicação FastAPI, normalmente não precisamos criar manualmente o loop de eventos com `asyncio.run()`.

Isso acontece porque o servidor ASGI, como o Uvicorn, já cuida dessa parte para a aplicação.

Ou seja, quando usamos FastAPI com Uvicorn, o servidor já fornece a estrutura necessária para executar rotas assíncronas.

Exemplo:

```python
@app.get("/saudar/{nome}")
async def saudar(nome: str):
    return {"mensagem": f"Olá, {nome}"}
```

A função acima é assíncrona, mas não precisamos fazer:

```python
asyncio.run(saudar())
```

O servidor ASGI gerencia essa execução internamente.

---

## 10. Relação entre FastAPI e assincronismo

O FastAPI foi desenvolvido com suporte nativo ao assincronismo do Python.

Isso significa que ele foi pensado para trabalhar bem com:

```python
async def
await
```

Por isso, ele combina naturalmente com servidores ASGI, como o Uvicorn.

Essa é uma diferença importante em relação a frameworks mais tradicionais, que podem ter sido criados inicialmente com foco em execução síncrona.

---

## 11. Diferença prática entre WSGI e ASGI

| Tipo | Nome completo | Modelo | Exemplo de servidor | Uso comum |
|---|---|---|---|---|
| WSGI | Web Server Gateway Interface | Síncrono | Waitress | Flask |
| ASGI | Asynchronous Server Gateway Interface | Assíncrono | Uvicorn, Hypercorn | FastAPI |

De forma simplificada:

```text
WSGI → servidor síncrono
ASGI → servidor assíncrono
```

---

## 12. Hypercorn

Além do Uvicorn, outro exemplo de servidor ASGI é o **Hypercorn**.

Ele também pode executar aplicações FastAPI, pois trabalha com o padrão ASGI.

Exemplo conceitual:

```text
FastAPI + Hypercorn
```

Na aula, o Hypercorn foi citado mais como curiosidade, porque o foco do estudo continua sendo o Uvicorn.

---

## 13. Por que usar Uvicorn no FastAPI?

O Uvicorn é muito utilizado com FastAPI porque:

- é um servidor ASGI;
- suporta assincronismo;
- integra bem com o FastAPI;
- é simples de usar em desenvolvimento;
- permite recarregamento automático com `reload=True`;
- é amplamente adotado em projetos FastAPI.

Durante os estudos, usar Uvicorn é uma escolha adequada porque ele entrega o que o FastAPI precisa para executar rotas assíncronas corretamente.

---

## 14. Explicando os parâmetros do `uvicorn.run`

Código:

```python
uvicorn.run(
    "app:app",
    host="0.0.0.0",
    port=3001,
    reload=True
)
```

### `"app:app"`

Indica qual aplicação será executada.

O primeiro `app` é o arquivo `app.py`.

O segundo `app` é a variável:

```python
app = FastAPI()
```

### `host="0.0.0.0"`

Define que o servidor aceitará conexões vindas de qualquer endereço de rede disponível na máquina.

Em desenvolvimento local, também é comum usar:

```python
host="127.0.0.1"
```

### `port=3001`

Define a porta em que a aplicação será executada.

Nesse caso, a API ficará disponível em:

```text
http://localhost:3001
```

### `reload=True`

Faz o servidor reiniciar automaticamente quando houver alteração no código.

Esse recurso é útil durante o desenvolvimento.

---

## 15. Exemplo de execução

Para rodar a aplicação:

```bash
python app.py
```

Ou diretamente pelo Uvicorn:

```bash
uvicorn app:app --reload --port 3001
```

Depois, é possível acessar a rota:

```text
http://localhost:3001/saudar/Guilherme
```

Resposta esperada:

```json
{
  "mensagem": "Olá, Guilherme"
}
```

Também é possível acessar a documentação automática do FastAPI:

```text
http://localhost:3001/docs
```

---

## 16. Resumo da aula

A aula apresentou a diferença entre servidores síncronos e assíncronos no ecossistema Python.

O ponto central é que o FastAPI trabalha muito bem com assincronismo, mas para isso precisa ser executado por um servidor compatível com ASGI.

Os principais conceitos foram:

- servidores Python podem seguir o padrão WSGI ou ASGI;
- WSGI é associado a servidores síncronos;
- ASGI é associado a servidores assíncronos;
- Waitress é um exemplo de servidor WSGI;
- Uvicorn é um exemplo de servidor ASGI;
- Hypercorn também é um servidor ASGI;
- o FastAPI é nativo ao assincronismo do Python;
- o servidor ASGI gerencia o loop de eventos necessário para executar funções assíncronas;
- no projeto, o Uvicorn é usado para rodar a aplicação FastAPI.

---

## 17. Conclusão

Servidores assíncronos são uma parte fundamental para entender por que o FastAPI consegue lidar bem com múltiplas requisições e funções `async`.

Enquanto em um script Python comum precisamos iniciar manualmente o loop de eventos com `asyncio.run()`, em uma aplicação FastAPI essa responsabilidade é assumida pelo servidor ASGI.

Por isso, ao usar FastAPI, é comum utilizar servidores como:

```text
Uvicorn
Hypercorn
```

No projeto estudado, o Uvicorn será o servidor principal, porque ele é simples, eficiente e adequado para aplicações FastAPI.
