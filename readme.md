# Floating Translate

Floating Translate é uma ferramenta de tradução em tempo real pensada para jogos e aplicações em tela cheia.  
Ela permite selecionar uma área da tela, reconhecer o texto (OCR) e mostrar a tradução em uma caixinha flutuante discreta.

## Funcionalidades

- Botão flutuante circular sempre visível, arrastável pela tela.
- Overlay para selecionar uma região da tela com o mouse.
- Captura da área selecionada e pré-processamento da imagem para OCR.
- OCR com Tesseract (inglês e português).
- Tradução automática (por exemplo, de inglês para português).
- Bubble de tradução minimalista, sem bordas, com fundo preto translúcido.
- Zona de saída “hotspot”: arraste o botão flutuante até o círculo de saída para encerrar o app.

## Instalação

1. Clonar o repositório:

git clone https://github.com/MarcoCatoi/Floating_Translate

cd Floating_Translate

2. Criar e ativar o ambiente virtual (opcional, mas recomendado):

python -m venv .venv
..venv\Scripts\activate # Windows

3. Instalar as dependências:

pip install -r requirements.txt


4. Instalar o Tesseract OCR no sistema (Windows):

- Baixar o instalador em https://github.com/UB-Mannheim/tesseract/wiki
- Após instalar, garantir que o executável `tesseract.exe` esteja no PATH ou configurar o caminho em `ocr.py`.

## Uso

Executar o aplicativo a partir da raiz do projeto:

python -m app.app


Fluxo básico:

1. O botão flutuante aparecerá no canto da tela.
2. Clique no botão para abrir o overlay.
3. Selecione uma área com texto na tela.
4. A tradução aparecerá na bubble de tradução.
5. Para encerrar o programa, arraste o botão flutuante até a zona de saída (círculo com “X”), no centro inferior da tela (só aparece quando há a "invasão" do botao na zona de saida).

## Empacotar como executável (opcional)

Você pode gerar um `.exe` standalone usando PyInstaller:

pip install pyinstaller
pyinstaller --onefile --windowed -n FloatingTranslate app/app.py

O executável será criado em `dist/FloatingTranslate.exe`.

## Estrutura do projeto

Floating_Translate/
app/
app.py
core/
capture.py
preprocess.py
ocr.py
translate.py
gui/
overlay.py
bubble.py
floating_button.py
exit_zone.py
requirements.txt
README.md

## Licença
MIT License

Copyright (c) 2025 Marco Catoi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

