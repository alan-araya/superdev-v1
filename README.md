
# Super DEV - AI Tests

Repo para testes e experiências da palestra Super DEV.

Nesta edição estamos testando 3 implementações "iguais", feitas pelos modelos de IA: o3-mini, Qwen 2.5 Max, Deepseek-R1.

Para cada modelo de IA foi criado uma pasta com os arquivos de mesmo nome e objetivo, mas cada um contendo a implementação gerada pelo respectivo modelo de IA.

  

# Setup do Ambiente:
  
### 1. Suba o container docker:
    docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=mypass postgres

### 2. Crie as tabelas no banco
    cat create-tables.sql | docker exec -i database psql -U postgres -d postgres
### 3. Execute o arquivo "populate.py" de algum dos modelos
Por exemplo, executando o arquivo do o3-mini para gerar dados na base:

    python openai-o3/populate.py
    
### 4. Extensão para "servir" o HTML (opcional)
Caso você esteja executando o projeto no Github Codespaces ou similar, recomendamos a extensão Live Server do VS Code:
https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer
Caso você esteja executando na sua própria máquina, basta abrir o arquivo HTML em um navegador.

# Rodando o exemplo
Para rodar o exemplo de algum dos modelos, basta subir a API executando o arquivo "app.py" de alguma das pastas, como por exemplo do o3-mini:

    python openai-o3/app.py

Depois basta abrir o arquivo index.html (abrindo em sua máquina no navegador ou servindo ele via Live Server).
Na sequência, basta executar o arquivo "consumer.py" enquanto você observa o HTML aberto. Você notará as poltronas sendo "resevados" pelos consumidores.
Para reiniciar o exemplo, basta rodar os passos 2 e 3 do setup. Eventualmente, subindo a API de outro modelo e testando com outro consumer.

     python openai-o3/consumer.py
