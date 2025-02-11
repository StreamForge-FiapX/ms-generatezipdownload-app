![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=POSTECH-SOAT-SALA11_application-avalanches-pedido-ms&metric=alert_status)
![Bugs](https://sonarcloud.io/api/project_badges/measure?project=POSTECH-SOAT-SALA11_application-avalanches-pedido-ms&metric=bugs)
![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=POSTECH-SOAT-SALA11_application-avalanches-pedido-ms&metric=code_smells)
![Coverage](https://sonarcloud.io/api/project_badges/measure?project=POSTECH-SOAT-SALA11_application-avalanches-pedido-ms&metric=coverage)

# **Documentação do Microserviço de Compactação e Download de Arquivos: ms-generatezipdownload-app-app**
Este documento descreve o fluxo de funcionamento do microserviço responsável por acessar diretórios no bucket S3, compactar arquivos em um único `.zip`, e fornecer uma URL auto-assinada para download. Ele aborda as etapas de desenvolvimento, integrações, papéis no sistema e detalhamento técnico.

---

### **Visão Geral do Sistema**
O sistema gerencia diretórios no S3 indicados por registros no banco Elasticache for Redis. Após a identificação de um diretório, os arquivos e subdiretórios são compactados em um único `.zip`, que é disponibilizado para download através de uma URL auto-assinada, gerada pelo próprio S3.

---

### **Objetivo do Microserviço**
O microserviço é responsável por:

1. **Identificar Diretórios no S3**:
   Consultar informações de diretórios no banco de dados Redis.

2. **Compactar Arquivos**:
   Acessar todos os arquivos e subdiretórios listados no diretório especificado no S3 e gerar um único arquivo `.zip`.

3. **Gerar URL Auto-assinada**:
   Criar uma URL auto-assinada para o cliente acessar e baixar o arquivo `.zip`.

4. **Atualizar Metadados no Redis**:
   Registrar informações do `.zip` gerado, como nome, tamanho e URL gerada.

---

### **Fluxo de Funcionamento**

#### **Recepção de Requisição**
1. O microserviço recebe uma solicitação, seja via fila de mensagens (ex.: RabbitMQ) ou requisição HTTP.
2. A solicitação contém:
   - **Identificador do diretório**: Obtido no banco Redis, que aponta para o caminho no S3.

#### **Processamento do Diretório**
Após identificar o diretório:
1. O microserviço usa o Redis para recuperar o caminho do diretório no S3.
2. Ele acessa o bucket S3 e lista os arquivos e subdiretórios do diretório especificado.
3. Todos os itens são baixados e compactados em um único arquivo `.zip`.

#### **Upload e Geração de URL**
1. O arquivo `.zip` é enviado ao bucket S3 em um caminho específico (ex.: `compressed/zips/`).
2. Uma URL auto-assinada é gerada pelo S3 para permitir o download público temporário do arquivo.

#### **Atualização do Banco e Notificação**
1. O Redis é atualizado com os seguintes metadados do `.zip`:
   - Caminho no S3
   - URL auto-assinada
   - Tamanho do arquivo
   - Data e hora de geração
2. Uma mensagem é enviada para a fila ou serviço correspondente, indicando que o arquivo `.zip` está pronto para download.

---

### **Integrações e Dependências**

1. **Amazon S3**
   - Listagem de arquivos e subdiretórios.
   - Upload do `.zip` gerado.
   - Geração de URL auto-assinada.

2. **Banco Redis (AWS Elasticache)**
   - Armazenamento de metadados de diretórios e `.zip` gerados.
   - Recuperação de informações sobre diretórios a processar.

3. **Mensageria (opcional)**
   - RabbitMQ ou similar para notificação de que o `.zip` está pronto.

---

### **Tecnologias e Ferramentas Utilizadas**
- **Linguagem**: Python ou .NET Core
- **Orquestração**: Kubernetes (AWS EKS)
- **Banco de Dados**: Redis (AWS Elasticache)
- **Armazenamento**: Amazon S3
- **Mensageria (opcional)**: RabbitMQ

---

### **Regras de Negócio e Pontos Críticos**

1. **Integridade do Arquivo `.zip`**
   Garantir que todos os arquivos sejam compactados antes do upload.

2. **Ordem das Operações**
   A geração da URL, atualização no Redis e envio da notificação devem ser realizadas em sequência ou com mecanismos de rollback.

3. **URLs Temporárias**
   A URL auto-assinada deve ter validade configurável (ex.: 24 horas).

4. **Gerenciamento de Erros**
   Implementar lógica de tolerância a falhas para:
   - Operações de download e upload no S3.
   - Conexão com Redis e fila de mensagens.

5. **Escalabilidade**
   O microserviço deve suportar múltiplas requisições simultâneas, com processamento paralelo dos diretórios.

---

### **Estrutura do Projeto**

#### **Estrutura de Diretórios**
```plaintext
ms-generatezipdownload-app-app/
├── Dockerfile
├── README.md
├── requirements.txt
├── src
│   ├── domain
│   │   ├── repositories.py
│   │   └── use_cases.py
│   ├── infrastructure
│   │   ├── redis_repository.py
│   │   └── s3_event_parser.py
│   └── main.py
└── tests
    ├── test_lambda_handler.py
    ├── test_redis_repository.py
    ├── test_repositories.py
    ├── test_s3_event_parser.py
    └── test_use_cases.py
```

---

### **Detalhamento do Fluxo de Trabalho**

1. **Recepção de Requisição**:
   O caso de uso `ProcessDirectoryUseCase` é acionado para iniciar o processamento.

2. **Processamento do Diretório**:
   - `StoragePort` acessa o bucket S3 e lista os arquivos.
   - `ZipGenerationService` compacta os itens.

3. **Upload e Geração de URL**:
   - `StoragePort` faz o upload do `.zip`.
   - `GenerateDownloadLinkUseCase` cria a URL auto-assinada.

4. **Atualização e Notificação**:
   - `CachePort` atualiza o Redis com as informações do `.zip`.
   - `MessagePublisherPort` notifica que o arquivo está disponível.

---

Esta estrutura assegura modularidade, facilidade de manutenção e escalabilidade para o microserviço.
