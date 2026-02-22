# VisionBased_DrawingSystem

Sistema de desenho em tempo real baseado em Visão Computacional, utilizando rastreamento de mãos para interação gestual sem contato físico.

## 🚀 Funcionalidades

- Detecção e rastreamento de mãos com MediaPipe
- Desenho em tempo real utilizando o dedo indicador
- Seleção de cores por gestos
- Função borracha
- HUD interativa com painel superior
- Processamento de imagem com OpenCV

## 🛠 Tecnologias Utilizadas

- Python 3.x
- OpenCV
- MediaPipe
- NumPy

## 📦 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seuusuario/VisionBased_DrawingSystem.git
cd VisionBased_DrawingSystem

python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Instale as dependências

```bash
pip install opencv-python mediapipe numpy
```

---

## ▶️ Como Executar

Execute o arquivo principal:

```bash
python main.py
```

A aplicação iniciará utilizando a câmera padrão do sistema.

Pressione **Q** para encerrar.

---

## 🎮 Como Utilizar

* 1 dedo (indicador) → Desenhar
* 2, 3 ou 4 dedos → Selecionar cores
* 5 dedos → Ativar borracha

---

## ⚙️ Configuração da Fonte de Vídeo

Para webcam padrão:

```python
cap = cv2.VideoCapture(0)
```

Caso a câmera não abra, tente:

```python
cap = cv2.VideoCapture(1)
```
## 📌 Observações

* Utilize o sistema em ambiente bem iluminado.
* Evite fundos com cores semelhantes à pele.
* O desempenho pode variar conforme o hardware.
* Caso ocorram erros relacionados ao MediaPipe ou OpenCV, recomenda-se utilizar Python 3.9 ou 3.10, pois versões mais recentes podem apresentar incompatibilidades com algumas dependências.



