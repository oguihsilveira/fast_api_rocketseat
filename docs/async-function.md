# Assincronismo e Funções Assíncronas no FastAPI

## 1. Contexto da aula

A aula apresenta um dos conceitos mais importantes para entender o funcionamento do **FastAPI**: o **assincronismo**.

O FastAPI se destaca no ecossistema Python por ter ótimo desempenho e por trabalhar muito bem com recursos assíncronos da linguagem, como:

```python
async def
await
```

Esses recursos permitem que a aplicação lide melhor com tarefas que precisam aguardar algum retorno externo, como banco de dados, APIs externas ou outros serviços.

---

## 2. Antes de entender o assíncrono: o que é sincronismo?

A programação síncrona é o modelo mais tradicional de execução.

Nesse modelo, as tarefas são executadas **uma depois da outra**, em sequência.

Exemplo conceitual:

```text
Tarefa 1 → Tarefa 2 → Tarefa 3 → Tarefa 4
```

A próxima tarefa só começa depois que a tarefa anterior termina.

---

## 3. Exemplo de execução síncrona

Imagine uma aplicação que precisa executar três etapas:

1. validar dados;
2. buscar informações no banco de dados;
3. formatar a resposta.

Em um fluxo síncrono, a execução acontece assim:

```text
Valida os dados
↓
Busca no banco de dados
↓
Espera o banco responder
↓
Formata a resposta
↓
Finaliza
```

Se a busca no banco demorar, o programa fica parado esperando aquela resposta antes de continuar.

Esse comportamento é simples e previsível, mas pode ser menos eficiente em aplicações web que recebem várias requisições ao mesmo tempo.

---

## 4. O que é assincronismo?

O assincronismo permite que uma tarefa seja pausada enquanto espera uma resposta externa, sem bloquear totalmente a execução de outras tarefas.

Ou seja, a aplicação não precisa ficar parada enquanto aguarda uma resposta do banco de dados, de uma API externa ou de outro sistema.

Exemplo conceitual:

```text
Tarefa 1 inicia
Tarefa 1 aguarda resposta externa
Enquanto isso, Tarefa 2 pode iniciar
Tarefa 2 aguarda resposta externa
Tarefa 1 recebe resposta e continua
Tarefa 2 recebe resposta e continua
```

A ideia principal é:

```text
Não é necessário finalizar uma tarefa para começar outra.
```

---

## 5. Por que isso importa em APIs?

Em uma API, várias requisições podem chegar ao mesmo tempo.

Exemplo:

```text
Usuário 1 faz uma requisição
Usuário 2 faz uma requisição
Usuário 3 faz uma requisição
```

Se cada requisição precisar acessar um banco de dados, chamar uma API externa ou consultar outro serviço, haverá momentos de espera.

O assincronismo permite que a aplicação aproveite esses momentos de espera para processar outras tarefas.

Isso melhora o aproveitamento da aplicação e pode aumentar a performance em cenários com muitas operações de entrada e saída.

---

## 6. Operações que se beneficiam do assincronismo

O assincronismo é especialmente útil quando a aplicação precisa aguardar respostas de recursos externos.

Exemplos:

- consultas em banco de dados;
- chamadas para APIs externas;
- comunicação com sistemas em nuvem;
- leitura e escrita de arquivos;
- envio de requisições HTTP;
- comunicação com outros serviços.

Essas operações são chamadas, de forma geral, de operações de **I/O**.

I/O significa entrada e saída de dados.

---

## 7. Loop de eventos

Um dos elementos principais do assincronismo é o **loop de eventos**.

O loop de eventos é o mecanismo responsável por organizar a execução das tarefas assíncronas.

Ele funciona como um gerenciador que decide:

- qual tarefa será executada;
- qual tarefa deve aguardar;
- qual tarefa pode continuar;
- quando uma tarefa retornou da espera;
- quando uma nova tarefa pode entrar em execução.

De forma simplificada:

```text
O loop de eventos orquestra as tarefas assíncronas.
```

---

## 8. Fila de tarefas

No funcionamento assíncrono, as tarefas entram em uma espécie de fila.

Quando uma tarefa precisa esperar uma resposta externa, ela não bloqueia todo o programa. Ela é colocada em espera, e o loop de eventos pode continuar executando outras tarefas.

Exemplo:

```text
Tarefa 1 entra no loop de eventos
Tarefa 1 chama o banco de dados
Tarefa 1 fica aguardando resposta

Enquanto isso:

Tarefa 2 entra no loop de eventos
Tarefa 2 chama uma API externa
Tarefa 2 fica aguardando resposta

Quando a resposta da Tarefa 1 chega:
Tarefa 1 volta para o loop e continua
```

Esse comportamento permite concorrência.

---

## 9. Concorrência não é necessariamente paralelismo

É importante entender que assincronismo não significa obrigatoriamente que várias tarefas estão sendo executadas ao mesmo tempo em diferentes núcleos do processador.

O conceito principal é a **concorrência**.

Na concorrência, várias tarefas podem estar em andamento, mas alternando momentos de execução e espera.

Exemplo:

```text
Tarefa 1 começa
Tarefa 1 espera
Tarefa 2 começa
Tarefa 2 espera
Tarefa 1 continua
Tarefa 2 continua
```

O ganho acontece principalmente porque o programa não fica parado durante os períodos de espera.

---

## 10. Funções assíncronas com `async def`

Em Python, uma função assíncrona é criada com:

```python
async def
```

Exemplo:

```python
async def saudar(nome: str):
    return {"mensagem": f"Olá, {nome}"}
```

No FastAPI, é comum criar rotas assíncronas dessa forma:

```python
@app.get("/saudar/{nome}")
async def saudar(nome: str):
    return {"mensagem": f"Olá, {nome}"}
```

Nesse caso, a função `saudar` é uma função assíncrona.

---

## 11. O que significa `async def`?

Quando uma função é declarada com `async def`, ela passa a ser uma **corrotina**.

Uma corrotina é uma função especial que pode ser pausada e retomada depois.

Isso permite que o Python interrompa temporariamente aquela função em pontos específicos, geralmente marcados com `await`, e use esse tempo para executar outras tarefas.

---

## 12. A palavra-chave `await`

A palavra `await` é usada dentro de funções assíncronas.

Ela indica que o código deve aguardar o resultado de uma operação assíncrona antes de continuar.

Exemplo:

```python
await asyncio.sleep(3)
```

Esse comando significa:

```text
Aguarde 3 segundos sem bloquear completamente o loop de eventos.
```

Enquanto essa espera acontece, outras tarefas assíncronas podem ser executadas.

---

## 13. Diferença entre espera síncrona e espera assíncrona

### Espera síncrona

```python
import time

time.sleep(3)
```

Esse tipo de espera bloqueia a execução.

O programa fica parado durante os 3 segundos.

### Espera assíncrona

```python
import asyncio

await asyncio.sleep(3)
```

Esse tipo de espera permite que o loop de eventos execute outras tarefas enquanto aguarda.

---

## 14. Exemplo prático com `asyncio`

Na aula, foi criado um arquivo chamado:

```text
async.py
```

Esse arquivo serve para demonstrar o funcionamento do assincronismo em Python.

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

    await tarefa(3, 4)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 15. Explicação do código

### Importação

```python
import asyncio
```

O módulo `asyncio` é a biblioteca padrão do Python usada para trabalhar com programação assíncrona.

---

### Função assíncrona `tarefa`

```python
async def tarefa(nome, duracao):
```

Essa função representa uma tarefa assíncrona.

Ela recebe dois parâmetros:

```python
nome
duracao
```

O parâmetro `nome` identifica a tarefa.

O parâmetro `duracao` indica quanto tempo ela irá esperar.

---

### Início da tarefa

```python
print(f"tarefa [{nome}] iniciando...")
```

Essa linha apenas mostra no terminal que a tarefa começou.

---

### Pausa assíncrona

```python
await asyncio.sleep(duracao)
```

Aqui acontece o ponto principal da aula.

A função entra em espera, mas essa espera não trava todo o programa.

Enquanto essa tarefa aguarda, o loop de eventos pode executar outra tarefa.

---

### Final da tarefa

```python
print(f"tarefa [{nome}] terminou...")
```

Essa linha mostra quando a tarefa terminou.

---

## 16. Função `main`

```python
async def main():
```

A função `main` também é assíncrona.

Ela organiza quais tarefas serão executadas.

---

## 17. Executando tarefas juntas com `asyncio.gather`

```python
await asyncio.gather(
    tarefa(1, 3),
    tarefa(2, 6)
)
```

O `asyncio.gather` executa mais de uma tarefa assíncrona de forma concorrente.

Nesse exemplo:

```python
tarefa(1, 3)
tarefa(2, 6)
```

as duas tarefas começam praticamente juntas.

A tarefa 1 espera 3 segundos.

A tarefa 2 espera 6 segundos.

Como elas são executadas de forma concorrente, o tempo total dessa parte tende a ser próximo de 6 segundos, e não 9 segundos.

Em uma execução puramente síncrona, seria:

```text
3 segundos + 6 segundos = 9 segundos
```

Com assincronismo, fica aproximadamente:

```text
máximo entre 3 e 6 segundos = 6 segundos
```

---

## 18. Executando uma tarefa depois das outras

Depois do `gather`, o código executa:

```python
await tarefa(3, 4)
```

Essa tarefa só começa depois que as tarefas 1 e 2 terminam.

Isso acontece porque o código usou `await` no `asyncio.gather`.

Ou seja, a função `main` espera o grupo de tarefas terminar antes de continuar.

Fluxo:

```text
Tarefa 1 e Tarefa 2 iniciam juntas
↓
Espera as duas terminarem
↓
Tarefa 3 inicia
↓
Tarefa 3 termina
```

---

## 19. Executando o loop de eventos

```python
if __name__ == "__main__":
    asyncio.run(main())
```

Esse trecho faz com que a função `main` seja executada quando o arquivo for rodado diretamente.

O comando:

```python
asyncio.run(main())
```

inicia o loop de eventos e executa a função assíncrona `main`.

Sem isso, a função assíncrona seria apenas definida, mas não executada.

---

## 20. Resultado esperado no terminal

Ao executar:

```bash
python async.py
```

a saída será parecida com:

```text
tarefa [1] iniciando...
tarefa [2] iniciando...
tarefa [1] terminou...
tarefa [2] terminou...
tarefa [3] iniciando...
tarefa [3] terminou...
```

Esse resultado demonstra que as tarefas 1 e 2 começaram antes de uma esperar a outra terminar.

---

## 21. Relação com FastAPI

No FastAPI, as rotas podem ser escritas com `async def`.

Exemplo:

```python
@app.get("/saudar/{nome}")
async def saudar(nome: str):
    return {"mensagem": f"Olá, {nome}"}
```

Quando uma rota é assíncrona, ela pode usar `await` internamente para operações assíncronas.

Exemplo conceitual:

```python
@app.get("/usuarios/{id}")
async def buscar_usuario(id: int):
    usuario = await buscar_no_banco(id)
    return usuario
```

Nesse caso, enquanto a aplicação aguarda o banco de dados responder, o servidor pode lidar com outras requisições.

---

## 22. Quando usar `async def` no FastAPI?

Use `async def` quando a rota precisar aguardar operações assíncronas, como:

- consulta assíncrona a banco de dados;
- chamada a API externa com biblioteca assíncrona;
- leitura assíncrona de arquivos;
- comunicação com serviços externos;
- tarefas que usam `await`.

Exemplo:

```python
@app.get("/dados")
async def obter_dados():
    resposta = await consultar_api_externa()
    return resposta
```

---

## 23. Quando `def` comum pode ser suficiente?

Nem toda rota precisa ser assíncrona.

Se a função executa apenas processamento simples, direto e rápido, uma função comum pode ser suficiente.

Exemplo:

```python
@app.get("/status")
def status():
    return {"status": "ok"}
```

Esse tipo de função não precisa necessariamente ser `async`.

---

## 24. Cuidado importante

Usar `async def` não torna automaticamente todo o código mais rápido.

Para obter benefício real, as operações internas também precisam ser compatíveis com assincronismo.

Por exemplo, dentro de uma função assíncrona, faz mais sentido usar bibliotecas assíncronas quando a operação envolve espera externa.

Exemplo de ideia correta:

```python
await consultar_banco_assincrono()
```

Se uma operação bloqueante for usada dentro de uma função assíncrona, ela pode prejudicar o funcionamento do loop de eventos.

---

## 25. Resumo visual

### Síncrono

```text
Tarefa 1 inicia
Tarefa 1 termina
Tarefa 2 inicia
Tarefa 2 termina
Tarefa 3 inicia
Tarefa 3 termina
```

### Assíncrono

```text
Tarefa 1 inicia
Tarefa 1 espera resposta externa

Tarefa 2 inicia
Tarefa 2 espera resposta externa

Tarefa 1 recebe resposta e termina
Tarefa 2 recebe resposta e termina
```

---

## 26. Principais conceitos da aula

A aula apresentou os seguintes conceitos:

- o FastAPI tem forte relação com assincronismo;
- programação síncrona executa tarefas uma a uma;
- programação assíncrona permite alternar entre tarefas durante momentos de espera;
- o loop de eventos gerencia a execução das tarefas;
- tarefas podem entrar em uma fila de espera;
- `async def` declara funções assíncronas;
- `await` aguarda uma operação assíncrona;
- `asyncio` permite testar assincronismo em Python;
- `asyncio.gather` executa tarefas concorrentes;
- `asyncio.run` inicia o loop de eventos em um script Python;
- no FastAPI, rotas podem ser criadas com `async def`.

---

## 27. Conclusão

O assincronismo é um dos conceitos mais importantes para entender o FastAPI.

Ele permite que a aplicação aproveite melhor o tempo de espera em operações externas, como banco de dados, APIs e serviços em nuvem.

Em vez de bloquear toda a execução enquanto uma tarefa aguarda resposta, o loop de eventos pode continuar trabalhando em outras tarefas.

Por isso, o FastAPI consegue oferecer bom desempenho em aplicações web modernas, especialmente quando combinado com servidores assíncronos e bibliotecas compatíveis com `async` e `await`.
