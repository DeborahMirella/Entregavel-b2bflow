# Desafio b2bflow: Integração Python, Supabase e Z-API ⚡

## Visão Geral Arquitetural
Este repositório contém a prova de conceito (PoC) desenvolvida para a 1ª etapa do processo seletivo de Estágio em Desenvolvimento Python da b2bflow. O sistema implementa um pipeline de orquestração automatizada que extrai tuplas de contatos de um banco de dados relacional e efetua o disparo dinâmico de mensagens via protocolo HTTP utilizando uma API.

---

## 1. Modelagem Relacional e Setup da Tabela (Supabase)
A persistência de dados foi estruturada em um SGBD PostgreSQL (via Supabase). Para instanciar a tabela de contatos e popular os dados iniciais de teste, a seguinte DDL (*Data Definition Language*) deve ser executada no SQL Editor da plataforma:

```sql
CREATE TABLE contatos (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  nome TEXT NOT NULL,
  telefone TEXT NOT NULL,
  criado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Inserção das tuplas de teste
INSERT INTO contatos (nome, telefone) VALUES
('Deborah', '5531987743302');
```

---

## 2. Topologia de Variáveis de Ambiente (.env)
Em conformidade com as diretrizes de segurança da informação, credenciais e chaves não são versionadas neste repositório. O arquivo `.env.example` serve como contrato de configuração. Crie um arquivo `.env` na raiz do diretório e insira as seguintes chaves de integração:

```text
# Credenciais - Camada de Persistência (Supabase)
SUPABASE_URL=[https://seu-projeto.supabase.co](https://seu-projeto.supabase.co)
SUPABASE_KEY=sua_chave_publica_anon_jwt

# Credenciais - Camada de Mensageria (Z-API)
ZAPI_INSTANCE_ID=seu_id_da_instancia
ZAPI_TOKEN=seu_token_da_instancia
ZAPI_CLIENT_TOKEN=seu_token_de_seguranca_da_conta
```

---

## 3. Guia de Execução
Para garantir o isolamento topológico das dependências da aplicação, exige-se a execução do fluxo no interior de um ambiente virtual. 

**Procedimentos via terminal:**

1. **Instanciação e ativação do ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Injeção do manifesto de dependências:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Invocação do script principal:**
   ```bash
   python3 main.py
   ```

---

## 4. Qualidade de Código e Boas Práticas
O orquestrador `main.py` foi codificado priorizando a robustez do fluxo. Implementou-se o rigoroso tratamento de exceções (blocos `try-except`) na camada de rede (via biblioteca `requests`), com mapeamento de *status code* HTTP. O sistema expõe logs estruturados de execução no *stdout* do terminal, garantindo a rastreabilidade total de falhas na extração de dados do Supabase ou na submissão de *payloads* para a Z-API.
