# Assets de Marca — Skolen

Coloque aqui os arquivos de imagem para usar nos slides com foto.

## Estrutura

```
Assets/
├── produto/     → Screenshots e prints do app Skolen
├── pessoas/     → Fotos de diretores, professores, alunos
└── marca/       → Logo, ícones, elementos visuais da marca
```

## Como referenciar no config.json

```json
{
  "tipo": "foto-card",
  "posicao": "esquerda",
  "imagem": "Marketing/Assets/pessoas/diretora.jpg",
  "imagem_tipo": "pessoa",
  "label": "Label do slide",
  "headline": "Headline com <em>destaque</em>",
  "body": "Texto de apoio aqui."
}
```

## Campos de `imagem_tipo`

| Valor | Quando usar | Forma do recorte |
|---|---|---|
| `pessoa` | Foto de diretor, professor, aluno | Círculo com borda colorida |
| `produto` | Screenshot do app | Retângulo com sombra e cantos arredondados |
| `print-anotado` | Print com setas e destaques | Retângulo com badge de destaque |
| `marca` | Logo, ícone | Quadrado limpo, sem borda |

## Sem imagem disponível

Se o campo `"imagem"` for omitido ou o arquivo não existir,
o slide renderiza um placeholder visual de marca (bolinhas coloridas Skolen)
no lugar da foto — o layout não quebra.
