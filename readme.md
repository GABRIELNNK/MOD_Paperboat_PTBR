# MOD_Paperboat_PTBR: Paper Mario (N64) - Tradução Português do Brasil (.o2r)

Este repositório contém os arquivos de tradução e o script em Python para compilar e gerar mods de texto no formato `.o2r` (compatíveis com o ecossistema Paperboat / Shipwright / decompilações do Paper Mario 64).

## 📌 Créditos e Agradecimentos

Este projeto é fruto do trabalho da comunidade de modding e engenharia reversa de Paper Mario:

* [**Star Rod**](https://github.com/z64a/star-rod): Pela ferramenta essencial de extração e descompilação dos textos, **bem como pela base do arquivo de definição de fontes (`fonts.xml`) e mapeamento do charset do jogo**.

* [**Paperboat**](https://github.com/HarbourMasters/PaperBoat): Pelos arquivos de referência e mapeamento da estrutura de mensagens e recursos.

A alocação de textos deste projeto foi extraída utilizando o **Star Rod** e alinhada com as referências do **Paperboat**.

---

## 🌍 Uso para Outros Idiomas

Este script e a estrutura em formato `JSON` **podem ser reutilizados para criar traduções do Paper Mario para qualquer outro idioma não oficial**. 

> ⚠️ **Importante:** O script **não altera o mapa de caracteres (charset) ou fontes pré-renderizadas do jogo**. Ele codifica os textos com base na tabela de fontes já existente (`fonts.xml` do jogo original). Portanto, caracteres não cadastrados no charset padrão dispararão erros de compilação.

---

## 🚧 Status do Projeto

* **Status:** Em andamento (WIP).

* **Pendências:** Restam aproximadamente **5.000 linhas** para serem adaptadas e ajustadas.

* **Revisão:** A tradução **ainda não passou por uma etapa formal de revisão** de contexto em jogo.

### 🤝 Quer ajudar?

Toda contribuição é bem-vinda! Se você deseja ajudar traduzindo mensagens, adequando comandos de formatação, revisando textos ou testando no jogo, sinta-se à vontade para abrir uma *Issue* ou enviar um *Pull Request*.

---

## 📂 Estrutura de Pastas e Pré-requisitos

Para executar a compilação localmente ou contribuir com o projeto, siga a estrutura necessária de arquivos:

```text
MOD_Paperboat_PTBR/
├── MPB_translate_messages_o2r.py
├── messages_ptbr.json
└── translate/
    └── messages/          <-- Extrair arquivos originais aqui
```

### 📥 Configuração Inicial das Mensagens de Referência (`PM64.o2r`)

Para compilar os arquivos traduzidos, o script precisa validar e alinhar os textos com as mensagens originais em inglês.

1. Localize o arquivo `PM64.o2r` do seu jogo/instalação.
2. Abra ou descompacte o arquivo `PM64.o2r` (ele utiliza formato ZIP).
3. Extraia a pasta `messages` para dentro da diretório `translate/` do repositório, resultando no caminho: `translate/messages/`.

---

## ⚙️ Estrutura do Arquivo de Mensagens (`JSON`)

A tradução é mantida em um arquivo JSON centralizado que mapeia cada mensagem do jogo. Exemplo do formato utilizado:

```json
{
    "format": "paperboat-star-rod-messages-v1",
    "source": "translate/messages",
    "messages": [
        {
            "group": 0,
            "id": "00:0001",
            "index": 1,
            "original_text": "[CenterX 159]Today...[End]",
            "resource": "MSG_Intro_0001",
            "source": "tools/traducao/src/00 Introduction.str",
            "text": "[CenterX 159]Hoje...[End]"
        }
    ]
}
```

### Campos do JSON:

* `format`: Especificação de compatibilidade (`paperboat-star-rod-messages-v1`).
* `resource`: Nome do recurso/arquivo da mensagem no jogo (ex: `MSG_Intro_0001`).
* `original_text`: Texto original em inglês incluindo as tags de controle.
* `text`: Texto traduzido para o português (mantendo as tags de controle como `[CenterX ...]`, `[BR]`, `[End]`, etc.).

---

## 🔍 Tipos de Erros Detectados pelo Compilador

O script de compilação `MPB_translate_messages_o2r.py` executa validações nos textos traduzidos antes do empacotamento no arquivo `.o2r`. Quando ocorrem falhas, elas são exibidas no console e gravadas no arquivo `errors.csv`.

Principais tipos de erros:

1. **`missing reference MSG_...`**
   * **Causa:** O arquivo binário de referência original (`translate/messages/MSG_...`) não foi localizado. Verifique se extraiu corretamente a pasta `messages` do `PM64.o2r`.

2. **`Character is not present in charset: 'X'`**
   * **Causa:** A tradução contém um caractere que não está cadastrado na tabela de fontes (`fonts.xml` / charset normal) do jogo.

3. **`Unsupported Star Rod command: [NomeDoComando]`**
   * **Causa:** Tag de comando entre colchetes `[...]` desconhecida ou com erro de digitação.

4. **`effect commands were changed; keep existing [effects] unchanged`**
   * **Causa:** As tags de efeitos gráficos (como `[Wave]`, `[Shake]`, `[PrintRising]`, `[/fx]`) do texto traduzido diferem da versão original. Os efeitos de texto devem ser mantidos sem alteração na tradução.

5. **`could not align original text with reference payload` / `could not locate effect`**
   * **Causa:** O compilador não conseguiu alinhar os bytes do texto traduzido aos comandos e cabeçalhos de referência.

6. **`encoded size 0xXX exceeds 0xYY`**
   * **Causa:** O tamanho codificado em bytes ultrapassa o limite de memória reservado no ponteiro original. A diferença em bytes excedentes é gravada no relatório (ex: `- 14` para 14 bytes excedidos).

---

## 🚀 Como Executar

### Pré-requisitos

* **Python 3.8** ou superior instalado.
* A pasta `translate/messages/` preenchida com as mensagens de referência extraídas do `PM64.o2r`.

### Execução Básica

Para compilar o JSON traduzido e gerar o arquivo `.o2r`:

```bash
python MPB_translate_messages_o2r.py messages_ptbr.json
```

O arquivo final será gerado no mesmo diretório com a extensão `.o2r` (ex: `messages_ptbr.o2r`).

### Opções de Linha de Comando

```text
Uso: MPB_translate_messages_o2r.py [-h] [-o OUTPUT] [--csv-errors CSV_ERRORS] [-y] messages

Positional arguments:
  messages              Caminho para o JSON de mensagens traduzidas.

Options:
  -h, --help            Exibe a mensagem de ajuda.
  -o, --output OUTPUT   Caminho de saída personalizado do arquivo .o2r.
  --csv-errors FILE     Caminho onde os erros serão salvos (padrão: errors.csv).
  -y, --ignore-errors   Gera o arquivo .o2r ignorando mensagens com erro, sem solicitar confirmação.
```

#### Exemplo com parâmetros avançados:

```bash
python MPB_translate_messages_o2r.py messages_ptbr.json -o MOD_Paperboat_PTBR.o2r --csv-errors relatorio_erros.csv -y
```

---

## 📄 Licença e Uso

Este projeto é feito por fãs, sem fins lucrativos e com fins exclusivamente educacionais e de preservação. Todos os direitos relativos a *Paper Mario* pertencem à Nintendo.