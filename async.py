import asyncio

async def tarefa(nome, duracao):
    print(f"tarefa [{nome}] iniciando...")
    await asyncio.sleep(duracao)
    print(f"tarefa [{nome}] terminou...")

# Corrotina (Função assíncrona pode ser chamada de corrotina)
async def main():
    await asyncio.gather(
     tarefa(1, 3),
     tarefa(2, 6)
    )
    await tarefa(3, 4)

if __name__ == "__main__":
    asyncio.run(main()) # Ligar loop de eventos da função assíncrona

