# NEAT-Python AI - Jogo Mais Difícil do Mundo (World's Hardest Game)




## Descrição
Jogo Mais Díficil do Mundo recriado em Python com a biblioteca *pygame* e algoritmo NEAT (NeuroEvolution of Augmenting Topologies) implementado através da biblioteca *neat-python*

Fases 1 a 4 disponíveis, no entanto, não vence a Fase 3 (trabalhando para que vença)

## Exemplo da execução
### Fase 1
![image](https://user-images.githubusercontent.com/103335009/217912371-83dce0fd-8b93-469d-a981-0e95e45b88a6.png)

### Fase 2
![image](https://user-images.githubusercontent.com/103335009/217910995-3006c28b-23b8-46ff-a2bb-1993ef36fa82.png)

### Fase 3
![image](https://user-images.githubusercontent.com/103335009/217911546-9b7e7130-e9fc-4911-bf58-d34fce6ed734.png)

### Fase 4
![image](https://user-images.githubusercontent.com/103335009/217911702-a1783248-8d80-4566-887a-d74701c6eadf.png)

Outros exemplos da execução podem ser vistos em https://twitch.tv/cuccalouto

## Setup
Clone o repositório para sua máquina
```
git clone https://github.com/luccacb16/WorldHardestGame-AI.git
```

Acesse a raiz do projeto
```
cd WorldHardestGame-AI
```

Instale as dependências
```
pip install -r requirements.txt
```

## Uso
Acesse o diretório da fase que deseja executar
```
cd "Fase 1"
```

Execute o comando
```
python -u main.py
```

Informações sobre a população, geração e fitness serão constantemente exibidas no terminal em que foi executado o arquivo.

É possível customizar os parâmetros do algoritmo genético e das redes neurais. Basta abrir o arquivo *config_feedforward.txt*. 

Para mais informações sobre a biblioteca neat-python, acesse a documentação em https://neat-python.readthedocs.io/en/latest/ 

É possível remover as linhas e as distâncias. Para isso, abra o arquivo main.py em um editor de texto e na função draw_window procure por "targetInfo"

Em seguida, altere os valores de *lines* e *dist* como desejar. Por default, ambas são False.