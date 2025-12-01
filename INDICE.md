# 📑 Índice Geral do Projeto

## 🎯 Por Onde Começar?

### 👨‍🎓 Se você é INICIANTE:
1. 📄 [QUICK_START.md](QUICK_START.md) - **Comece aqui!** Guia rápido em 5 passos
2. 📄 [README.md](README.md) - Documentação completa do projeto
3. 📄 [EXEMPLOS.md](EXEMPLOS.md) - Exemplos práticos de uso

### 👨‍💻 Se você é DESENVOLVEDOR:
1. 📄 [ARQUITETURA.md](ARQUITETURA.md) - Diagramas e explicações técnicas
2. 📄 [SUMARIO_EXECUTIVO.md](SUMARIO_EXECUTIVO.md) - Visão geral do projeto
3. 💻 [pc/line_follower.py](pc/line_follower.py) - Código principal
4. 🤖 [esp32/main.py](esp32/main.py) - Código do carrinho

### 🔧 Se você está com PROBLEMAS:
1. 📄 [EXEMPLOS.md](EXEMPLOS.md) - Seção "Troubleshooting"
2. 📄 [README.md](README.md) - Seção "Troubleshooting"
3. 💻 [pc/test_connection.py](pc/test_connection.py) - Script de diagnóstico

---

## 📚 Documentação Completa

### Guias Principais
| Arquivo | Descrição | Para quem? |
|---------|-----------|------------|
| [README.md](README.md) | Documentação completa do projeto (8.6KB) | Todos |
| [QUICK_START.md](QUICK_START.md) | Início rápido em 5 passos (2.7KB) | Iniciantes |
| [ARQUITETURA.md](ARQUITETURA.md) | Diagramas e arquitetura técnica (18KB) | Técnicos |
| [EXEMPLOS.md](EXEMPLOS.md) | 11 exemplos práticos de uso (11KB) | Usuários |
| [SUMARIO_EXECUTIVO.md](SUMARIO_EXECUTIVO.md) | Visão geral executiva (11KB) | Professores/Gestores |
| [ESTRUTURA_PROJETO.txt](ESTRUTURA_PROJETO.txt) | Estrutura de arquivos (8.2KB) | Referência |
| [INDICE.md](INDICE.md) | Este arquivo - índice geral | Navegação |

### Documentação Específica
| Arquivo | Descrição |
|---------|-----------|
| [esp32/README.md](esp32/README.md) | Documentação do código ESP32 (3.0KB) |
| [pc/README.md](pc/README.md) | Documentação do código PC (5.9KB) |

---

## 💻 Código Fonte

### ESP32 (MicroPython)
| Arquivo | Linhas | Descrição |
|---------|--------|-----------|
| [esp32/main.py](esp32/main.py) | ~380 | Servidor WebSocket + controle de motores |
| [esp32/config.py](esp32/config.py) | ~30 | Configurações WiFi e pinos |

**Características:**
- ✅ Servidor WebSocket completo
- ✅ Controle PWM dos motores
- ✅ Suporte a comandos JSON
- ✅ Handshake WebSocket implementado
- ✅ Controle diferencial

### PC (Python + OpenCV)
| Arquivo | Linhas | Descrição |
|---------|--------|-----------|
| [pc/line_follower.py](pc/line_follower.py) | ~450 | Script principal do seguidor de linha |
| [pc/calibrate_hsv.py](pc/calibrate_hsv.py) | ~120 | Ferramenta de calibração visual |
| [pc/test_connection.py](pc/test_connection.py) | ~140 | Testes de conexão automáticos |
| [pc/config.py](pc/config.py) | ~50 | Parâmetros configuráveis |

**Características:**
- ✅ Processamento em tempo real
- ✅ Interface gráfica com OpenCV
- ✅ Cliente WebSocket assíncrono
- ✅ Controle PD-like inteligente
- ✅ Modo debug completo

---

## 🛠️ Utilitários

### Scripts de Instalação
| Arquivo | Plataforma | Uso |
|---------|------------|-----|
| [install.sh](install.sh) | Linux/Mac | `bash install.sh` |
| [install.bat](install.bat) | Windows | `install.bat` |

### Configuração
| Arquivo | Descrição |
|---------|-----------|
| [pc/requirements.txt](pc/requirements.txt) | Dependências Python |
| [.gitignore](.gitignore) | Arquivos ignorados pelo Git |

---

## 🗺️ Mapa de Navegação

### Fluxo de Leitura Recomendado

```
INÍCIO
  │
  ├─ Nunca usou o projeto?
  │  └─▶ QUICK_START.md → README.md → EXEMPLOS.md
  │
  ├─ Quer entender a arquitetura?
  │  └─▶ ARQUITETURA.md → esp32/main.py → pc/line_follower.py
  │
  ├─ Vai configurar agora?
  │  └─▶ QUICK_START.md → esp32/README.md → pc/README.md
  │
  ├─ Tem dúvidas específicas?
  │  └─▶ EXEMPLOS.md → README.md (Troubleshooting)
  │
  └─ Quer apresentar o projeto?
     └─▶ SUMARIO_EXECUTIVO.md → ARQUITETURA.md
```

---

## 📖 Conteúdo Detalhado por Documento

### README.md
- Descrição completa do projeto
- Hardware necessário
- Configuração passo a passo
- Como usar (comandos)
- Como funciona (explicação técnica)
- Dicas de performance
- Troubleshooting completo
- Critérios de avaliação
- Conceitos utilizados

### QUICK_START.md
- Início rápido em 5 passos
- Comandos essenciais
- Controles do sistema
- Ajustes importantes
- Problemas comuns
- Checklist pré-competição
- Dicas para ganhar

### ARQUITETURA.md
- Diagrama de componentes
- Fluxo de dados completo
- Algoritmo de detecção
- Lógica de controle
- Protocolo WebSocket
- Controle de motores L298N
- Processamento de imagem
- Diagrama de hardware
- Timing diagram
- Métricas de performance

### EXEMPLOS.md
- 11 exemplos práticos:
  1. Configuração inicial
  2. Configurar câmera
  3. Calibrar detecção
  4. Primeiro teste
  5. Executar seguidor
  6. Modo debug
  7. Cenários reais
  8. Config competição
  9. Troubleshooting
  10. Controle manual
  11. Logs e estatísticas

### SUMARIO_EXECUTIVO.md
- Objetivo do projeto
- Arquitetura resumida
- Tecnologias utilizadas
- Deliverables (entregáveis)
- Algoritmo de detecção
- Funcionalidades
- Métricas de performance
- Como usar (resumo)
- Diferenciais do projeto
- Conceitos aprendidos
- Resultados esperados

### ESTRUTURA_PROJETO.txt
- Árvore de arquivos
- Resumo de arquivos
- Fluxo de uso
- Qual arquivo ler primeiro
- Arquivos mais importantes
- Tecnologias utilizadas
- Checklist de completude

### esp32/README.md
- Configuração dos pinos
- Conexões L298N
- Upload para ESP32
- Instalar MicroPython
- Debug e testes
- Protocolo WebSocket
- Troubleshooting

### pc/README.md
- Instalação de dependências
- Uso dos scripts
- Configuração detalhada
- Calibração HSV
- Como funciona (pipeline)
- Configurar câmera
- Controles
- Otimizações
- Debug
- Parâmetros ajustáveis

---

## 🔍 Busca Rápida de Tópicos

### Por Tópico

#### Instalação e Setup
- 📄 QUICK_START.md - Passos 1-2
- 📄 README.md - Seção "Instalação"
- 📄 esp32/README.md - "Instalar MicroPython"
- 📄 pc/README.md - "Instalação"
- 🛠️ install.sh / install.bat

#### Configuração
- 📄 QUICK_START.md - "Ajustes Importantes"
- 📄 EXEMPLOS.md - "Exemplo 1: Configuração Inicial"
- 💻 esp32/config.py
- 💻 pc/config.py

#### Calibração
- 📄 EXEMPLOS.md - "Exemplo 3: Calibrar Detecção"
- 📄 pc/README.md - "Calibração HSV"
- 💻 pc/calibrate_hsv.py

#### Uso e Execução
- 📄 QUICK_START.md - Passo 5
- 📄 README.md - "Como Usar"
- 📄 EXEMPLOS.md - "Exemplo 5: Executar Seguidor"
- 💻 pc/line_follower.py

#### Troubleshooting
- 📄 EXEMPLOS.md - "Exemplo 9: Troubleshooting"
- 📄 README.md - Seção "Troubleshooting"
- 📄 QUICK_START.md - "Problemas Comuns"
- 💻 pc/test_connection.py

#### Arquitetura e Funcionamento
- 📄 ARQUITETURA.md - Todos os diagramas
- 📄 SUMARIO_EXECUTIVO.md - "Algoritmo de Detecção"
- 📄 README.md - "Como Funciona"

#### Competição
- 📄 QUICK_START.md - "Checklist Pré-Competição"
- 📄 EXEMPLOS.md - "Exemplo 8: Config Competição"
- 📄 README.md - "Dicas para Melhor Desempenho"
- 📄 SUMARIO_EXECUTIVO.md - "Resultados Esperados"

---

## 📊 Estatísticas do Projeto

### Código
- **Total de linhas de código**: ~1.200 linhas
- **Arquivos de código**: 6 arquivos
- **Linguagens**: Python, MicroPython

### Documentação
- **Total de documentação**: ~60 KB (texto)
- **Arquivos de documentação**: 8 arquivos
- **Páginas impressas equivalentes**: ~80 páginas

### Funcionalidades
- **Funcionalidades principais**: 5
- **Funcionalidades avançadas**: 5
- **Funcionalidades extra**: 4
- **Total**: 14 funcionalidades

### Ferramentas
- **Scripts de instalação**: 2
- **Scripts de teste**: 1
- **Scripts de calibração**: 1
- **Scripts principais**: 1
- **Total**: 5 ferramentas

---

## ✅ Checklist de Uso do Projeto

### Primeira Vez
- [ ] Ler QUICK_START.md
- [ ] Executar install.sh / install.bat
- [ ] Configurar esp32/config.py
- [ ] Upload código para ESP32
- [ ] Configurar câmera do celular
- [ ] Executar test_connection.py
- [ ] Executar calibrate_hsv.py
- [ ] Executar line_follower.py

### Antes de Cada Uso
- [ ] ESP32 ligado e conectado ao WiFi
- [ ] Câmera do celular ativa
- [ ] Linha preparada no chão
- [ ] Bateria carregada

### Para Competição
- [ ] Calibrar no local da competição
- [ ] Testar em linha similar
- [ ] Otimizar velocidade
- [ ] Fazer backup de configs
- [ ] Testar múltiplas vezes

---

## 🎓 Recursos de Aprendizado

### Para Entender Visão Computacional
1. 📄 ARQUITETURA.md - "Processamento de Imagem"
2. 📄 pc/README.md - "Pipeline de Processamento"
3. 💻 pc/line_follower.py - Métodos de processamento

### Para Entender WebSocket
1. 📄 ARQUITETURA.md - "Protocolo de Comunicação"
2. 📄 esp32/README.md - "Protocolo WebSocket"
3. 🤖 esp32/main.py - Implementação do servidor

### Para Entender Controle de Motores
1. 📄 ARQUITETURA.md - "Controle de Motores"
2. 📄 esp32/README.md - "Conexões L298N"
3. 🤖 esp32/main.py - Classe MotorControl

---

## 📞 Precisa de Ajuda?

### Ordem de Consulta

1. **Problema específico?** → EXEMPLOS.md (Troubleshooting)
2. **Não sabe como usar?** → QUICK_START.md
3. **Quer entender melhor?** → README.md
4. **Dúvida técnica?** → ARQUITETURA.md
5. **Erro no código?** → Comentários nos arquivos .py

### Diagnóstico Automático

```bash
# Execute para diagnosticar problemas
python pc/test_connection.py IP_ESP32 URL_CAMERA
```

---

## 🚀 Próximos Passos Recomendados

1. ✅ Leia QUICK_START.md (10 minutos)
2. ✅ Execute install.sh (5 minutos)
3. ✅ Configure ESP32 (15 minutos)
4. ✅ Teste conexões (5 minutos)
5. ✅ Calibre detecção (10 minutos)
6. ✅ Primeiro teste (5 minutos)
7. ✅ Otimize para competição (∞)

---

**Tempo total estimado**: ~1 hora para setup inicial  
**Tempo de calibração/otimização**: variável

---

**BOA SORTE NO PROJETO! 🏆🚗💨**

