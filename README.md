# Detector de Personagens Tom e Jerry

Este projeto implementa uma rede neural convolucional (CNN) para detectar se uma imagem contém o personagem Tom, Jerry, ambos, ou nenhum dos personagens.

## Estrutura do Projeto:
- `data/`: Contém as imagens do dataset.
- `models/`: Modelos treinados.
- `scripts/`: Scripts Python para treinamento e predição.
- `notebooks/`: Notebooks Jupyter para experimentação.
- `config.json`: Arquivo de configurações do projeto.
- `requirements.txt`: Lista de dependências.

## Como Executar:
1. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
2. Treine o modelo:
    ```bash
    python scripts/train_model.py
    ```
3. Faça predições em novas imagens:
    ```bash
    python scripts/predict.py
    ```

## Dependências:
- TensorFlow
- NumPy