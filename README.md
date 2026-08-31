# Sistema de Reconhecimento Facial para Controle de Acesso - IFMS Corumbá

Este projeto é parte de uma Iniciação Científica desenvolvida no Instituto Federal de Mato Grosso do Sul (IFMS) – Campus Corumbá, com foco na construção de um **protótipo funcional de sistema de reconhecimento facial** voltado para o **controle de acesso a ambientes restritos**, como laboratórios.

## 🎯 Objetivo

Desenvolver um sistema seguro, gratuito e de fácil manutenção para autenticação facial, integrando:

* Captura de imagem via webcam.
* Comparação facial com banco de dados local.
* Registro de tentativas de acesso em banco PostgreSQL.
* Avaliação do desempenho em ambiente simulado.

## 🔧 Tecnologias Utilizadas

* **Python** – linguagem principal
* **OpenCV** – captura e tratamento de imagens
* **face\_recognition** – extração e comparação facial
* **PostgreSQL** – armazenamento local de registros
* **dlib** – base da biblioteca `face_recognition`

## 📌 Funcionalidades

* Cadastro de imagens autorizadas.
* Captura de imagem em tempo real.
* Autenticação facial automática.
* Registro de acesso (usuário, data/hora, status).
* Testes com diferentes condições de iluminação e ângulos.
* Geração de relatório técnico com resultados e recomendações.

## 📁 Estrutura do Projeto

```
📂 projeto-reconhecimento-facial
├── 📁 imagens_autorizadas/
├── 📁 src/
│   ├── captura.py
│   ├── reconhecimento.py
│   └── banco_dados.py
├── 📁 docs/
│   └── manual_uso.pdf
├── requirements.txt
└── README.md
```

> A estrutura poderá ser atualizada com base na evolução do protótipo.

## 🧪 Metodologia

1. **Planejamento** dos requisitos e arquitetura do sistema.
2. **Desenvolvimento** do protótipo funcional.
3. **Integração** com banco de dados local.
4. **Validação** em ambiente simulado.
5. **Documentação** técnica e recomendações futuras.

## 📈 Resultados Esperados

* Protótipo funcional validado.
* Manual de operação completo.
* Base para implementação física futura com hardware (ex: travas eletromagnéticas).
* Inclusão de recursos de acessibilidade.

## 👥 Equipe

* **Coordenadora:** Patricia Fernanda da Silva Freitas
  `patricia.freitas@ifms.edu.br`

* **Bolsistas:**

  * Gabriel dos Santos Gonçalves
  * Guilherme Beckman Oliveira Aguero

## 🗓 Cronograma

* **Set 2025 - Abr 2026:** Desenvolvimento do sistema e funcionalidades básicas.
* **Mai - Jul 2026:** Integração com banco de dados e testes.
* **Jul - Ago 2026:** Validação, documentação e propostas de melhoria.

## 📚 Referências

Algumas das obras e estudos utilizados:

* ZELLE, John M. *Python: programação para todos*.
* GONZALEZ, Rafael C.; WOODS, Richard E. *Processamento Digital de Imagens*.
* FERREIRA, L. F.; ALMEIDA, R. S. *Banco de dados locais para sistemas embarcados*.
* SANTOS, João P. et al. *Sistema de controle de acesso com ferramentas livres*.

> Consulte o relatório técnico completo para a lista completa de referências e fundamentações teóricas.

