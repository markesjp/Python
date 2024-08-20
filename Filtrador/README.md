
# Filtrador

## Descrição

O **Filtrador** é um aplicativo simples desenvolvido em Python que utiliza as bibliotecas `OpenCV`, `tkinter`, `PIL`, e `numpy` para aplicar uma série de filtros em imagens. Ele permite que o usuário carregue imagens ou pastas contendo imagens e aplique diferentes filtros definidos por um arquivo de texto, além de realizar operações bitwise entre a imagem original e a filtrada.

## Funcionalidades

- Carregamento de uma imagem individual ou uma pasta com várias imagens.
- Aplicação de filtros especificados por um arquivo de texto.
- Aplicação de operações bitwise (`Not`, `And`, `Or`, `Xor`) entre a imagem original e a imagem filtrada.
- Salvamento das imagens processadas em um diretório escolhido pelo usuário.

## Uso

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/Filtrador.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd Filtrador
   ```
3. Execute o programa:
   ```bash
   python Filtrador.py
   ```

## Dependências

Para executar este programa, você precisará instalar as seguintes bibliotecas Python:

- `opencv-python`
- `Pillow`
- `numpy`
- `tkinter`

Você pode instalar essas dependências usando o `pip`:

```bash
pip install opencv-python Pillow numpy
```

## Como Contribuir

Se você encontrar problemas ou tiver sugestões para melhorias, fique à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
