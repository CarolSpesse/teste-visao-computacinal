# Projeto de Visão Computacional com MediaPipe

Este projeto demonstra o uso do MediaPipe para diferentes tarefas de visão computacional, incluindo detecção de mãos, pose corporal e detecção facial.

## 📋 Requisitos

- Python 3.8 ou superior
- Webcam (para os exemplos em tempo real)

## 🚀 Instalação

1. Clone ou baixe este repositório

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📁 Estrutura do Projeto

```
.
├── README.md
├── requirements.txt
├── detecao_maos.py      # Detecção de mãos em tempo real
├── detecao_pose.py      # Detecção de pose corporal
├── detecao_facial.py    # Detecção facial e landmarks
└── detecao_sorriso.py   # Detecção de sorriso
```

## 🎯 Exemplos

### 1. Detecção de Mãos (`detecao_maos.py`)

Detecta e desenha landmarks das mãos em tempo real usando a webcam.

**Como executar:**
```bash
python detecao_maos.py
```

**Funcionalidades:**
- Detecta até 2 mãos simultaneamente
- Desenha 21 landmarks por mão
- Mostra conexões entre os landmarks

**Controles:**
- Pressione `q` para sair

---

### 2. Detecção de Pose Corporal (`detecao_pose.py`)

Detecta e desenha landmarks da pose corporal completa em tempo real.

**Como executar:**
```bash
python detecao_pose.py
```

**Funcionalidades:**
- Detecta 33 landmarks da pose corporal
- Identifica braços, pernas, tronco e cabeça
- Desenha conexões entre os pontos principais

**Controles:**
- Pressione `q` para sair

---

### 3. Detecção Facial (`detecao_facial.py`)

Detecta faces e desenha landmarks faciais detalhados, incluindo contornos e íris.

**Como executar:**
```bash
python detecao_facial.py
```

**Funcionalidades:**
- Detecção de faces
- 468 landmarks faciais (face mesh)
- Detecção de íris dos olhos
- Contornos faciais detalhados

**Controles:**
- Pressione `q` para sair

---

### 4. Detecção de Sorriso (`detecao_sorriso.py`)

Detecta se a pessoa está sorrindo analisando a distância entre os cantos da boca usando landmarks faciais.

**Como executar:**
```bash
python detecao_sorriso.py
```

**Funcionalidades:**
- Detecta sorriso em tempo real
- Usa landmarks específicos da boca (pontos 61 e 291)
- Calibração automática na primeira detecção
- Mostra visualmente se está sorrindo ou não

**Controles:**
- Pressione `q` ou `ESC` para sair
- Pressione `r` para recalibrar o threshold

**Personalização:**
- Ajuste `SMILE_THRESHOLD` no código para tornar a detecção mais ou menos sensível
- O código detecta automaticamente qual câmera está disponível

## 🔧 Personalização

Você pode ajustar os parâmetros em cada script:

- `min_detection_confidence`: Confiança mínima para detecção (0.0 a 1.0)
- `min_tracking_confidence`: Confiança mínima para rastreamento (0.0 a 1.0)
- `max_num_hands`: Número máximo de mãos a detectar
- `model_complexity`: Complexidade do modelo de pose (0, 1 ou 2)

## 📚 Recursos do MediaPipe

O MediaPipe oferece várias soluções de visão computacional:

- **Hands**: Detecção de mãos e landmarks
- **Pose**: Detecção de pose corporal completa
- **Face Detection**: Detecção de faces
- **Face Mesh**: Landmarks faciais detalhados
- **Holistic**: Combinação de mãos, pose e face

## 🐛 Solução de Problemas

**Problema**: A webcam não abre
- Verifique se a webcam está conectada e funcionando
- Tente alterar o índice da câmera: `cv2.VideoCapture(1)` em vez de `cv2.VideoCapture(0)`

**Problema**: Erro ao importar MediaPipe
- Certifique-se de ter instalado todas as dependências: `pip install -r requirements.txt`
- Verifique se está usando Python 3.8 ou superior

**Problema**: Performance baixa
- Reduza a complexidade do modelo (ex: `model_complexity=0` no pose)
- Ajuste a resolução da webcam no código

## 📝 Licença

Este projeto é apenas para fins educacionais e de demonstração.

## 🤝 Contribuições

Sinta-se à vontade para expandir este projeto com mais exemplos e funcionalidades!
