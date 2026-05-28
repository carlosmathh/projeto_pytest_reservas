# Sistema de Reservas de Sala — Python + Testes Unitários

## Sobre o projeto

Este projeto foi desenvolvido com o objetivo de praticar conceitos de arquitetura backend e testes unitários utilizando Python.

A aplicação simula um sistema simples de reservas de salas, contendo regras de negócio como:

- criação de reservas
- cancelamento de reservas
- alteração de data e horário
- validação de conflitos de horário
- validação de datas passadas
- notificação de eventos
- controle de status da reserva

O foco principal do projeto não foi a interface ou persistência real em banco de dados, mas sim a construção de uma arquitetura organizada e a escrita de testes automatizados bem estruturados.

---

## Objetivos do projeto

Durante o desenvolvimento, os principais objetivos foram:

- praticar testes unitários com pytest
- aprender isolamento de dependências
- utilizar Mock para substituir serviços externos
- trabalhar com fixtures
- utilizar factory fixtures
- estruturar regras de negócio em camadas
- praticar tratamento de exceções
- trabalhar com dataclass
- praticar uso de datetime e timezone
- melhorar organização e legibilidade do código

---

## Estrutura do projeto

```
project/
├── config.py
├── models/
├── repositories/
├── services/
├── tests/
├── conftest.py
```

### models/

Responsável pelas entidades, exceções e mensagens do sistema.

Exemplos:

- Reservation
- ReservationStatus
- CreateReservationDTO
- exceções personalizadas

### repositories/

Responsável pelo acesso e manipulação de dados.

O repository contém métodos como:

- salvar reservas
- buscar reservas
- atualizar status
- alterar data e horário

### services/

Contém as regras de negócio da aplicação.

Exemplo:

- criação de reservas
- validação de conflitos
- cancelamento
- notificações

### tests/

Contém todos os testes unitários do projeto.

Os testes foram organizados por funcionalidade:

- criação de reservas
- cancelamento
- alteração de horário
- cenários de erro
- validações

### conftest.py

Arquivo responsável pelas fixtures compartilhadas entre os testes.

Nele foram centralizados:

- mocks
- factories
- objetos reutilizáveis
- congelamento de tempo para testes com datetime

---

## Regras de negócio implementadas

### Criar reserva

Ao criar uma reserva, o sistema:

1. valida se a data é válida
2. verifica conflito de sala e horário
3. gera um identificador
4. salva a reserva
5. envia notificação
6. retorna a reserva criada

### Cancelar reserva

Ao cancelar uma reserva, o sistema:

1. verifica se ela existe
2. altera o status para cancelado
3. envia notificação
4. retorna a reserva atualizada

### Alterar data e horário

Ao alterar uma reserva, o sistema:

1. verifica se a reserva existe
2. valida a nova data
3. verifica conflito de horário
4. atualiza a reserva
5. envia notificação

---

## Testes automatizados

Os testes foram desenvolvidos utilizando pytest.

Principais conceitos utilizados:

- fixtures
- factory fixtures
- mocks
- side effects
- isolamento de dependências
- testes de exceção
- verificação de chamadas
- testes de fluxo

Exemplos de cenários testados:

- reserva criada com sucesso
- sala já ocupada
- data inválida
- reserva inexistente
- alteração de horário
- cancelamento
- notificações enviadas corretamente

---

## Tecnologias utilizadas

- Python
- Pytest
- unittest.mock
- dataclasses
- datetime
- zoneinfo

---

## Aprendizados

Esse projeto foi importante para consolidar conhecimentos relacionados a:

- arquitetura backend
- testes unitários
- separação de responsabilidades
- escrita de código testável
- organização de projeto
- validação de regras de negócio
- boas práticas com pytest

---

## Como executar os testes

Instale as dependências:

```bash
pip install pytest pytest-mock
```

Execute os testes:

```bash
pytest
```

---

## Considerações finais

O projeto foi desenvolvido com foco em aprendizado e evolução técnica.

Apesar de simples, ele busca seguir práticas comuns utilizadas em projetos reais, principalmente na parte de testes automatizados e organização de código.