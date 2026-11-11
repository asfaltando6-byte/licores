# Licores por Encomenda

Projeto completo da página de vendas, com todas as seções, imagens, fonte local, dois carrosséis, perguntas frequentes e seleção dos planos Básico e Premium.

## Executar localmente

Requer Node.js 20 ou superior. Não precisa instalar dependências.

```sh
npm run dev
```

Abra http://localhost:4173. Para conferir arquivos e JavaScript:

```sh
npm run build
```

## Publicar na Vercel

Importe este repositório. O arquivo `vercel.json` configura a saída `dist` e o comando `npm run build`. Framework: Other. A pasta raiz do projeto é a raiz do repositório. Não são necessárias variáveis de ambiente.

Também é possível publicar o conteúdo de `dist/` em qualquer hospedagem estática. Não envie apenas o HTML: a pasta `assets/` deve acompanhá-lo.

## Arquivos

- `dist/index.html`: página completa e editável; inclui HTML, CSS e JavaScript.
- `dist/assets/`: todas as imagens originais, versões responsivas otimizadas e fonte Montserrat local.
- `scripts/serve.mjs`: servidor estático para desenvolvimento.
- `scripts/verify.mjs`: valida arquivos referenciados, sintaxe do JavaScript e conteúdo essencial.
- `scripts/optimize-images.py`: geração das versões WebP responsivas (requer Pillow).
- `outputs/image-optimization.json`: dimensões e pesos das imagens otimizadas.
- `.openai/hosting.json`: configuração da publicação original no ChatGPT Sites.
- `vercel.json`: configuração da Vercel e cache com revalidação.

## Otimizações de carregamento

A estrutura e os textos da página foram preservados. As imagens têm versões WebP menores para cada tela, seleção automática por `srcset` e `sizes`, carregamento tardio abaixo da primeira tela e decodificação assíncrona. O mockup principal tem prioridade alta e pré-carregamento responsivo. O fundo da primeira seção tem uma versão específica para celular. A fonte está no próprio projeto e usa `font-display: swap`. A página não depende de frameworks nem bibliotecas externas.

O ganho efetivo de velocidade depende do dispositivo, da conexão e da hospedagem. Os arquivos originais continuam disponíveis para futuras edições.

## Estado comercial preservado

O plano Básico mostra R$ 6,90 e 20 receitas. O Premium mostra R$ 17,00, 60 receitas e três bônus. Os botões de compra levam diretamente ao checkout Cakto de cada plano: Básico em https://pay.cakto.com.br/f3icmzr_1307247 e Premium em https://pay.cakto.com.br/34vc5pu. Este projeto contém o site e as imagens; os PDFs comerciais das receitas e bônus não fazem parte dos arquivos existentes.

## Carregamento e medição

O pixel Meta é inicializado no começo do head e envia apenas PageView, uma vez por carregamento. O mockup usa AVIF com fallback WebP, pré-carregamento compatível e tamanhos próximos da largura exibida. As novas imagens têm nomes próprios para evitar cache antigo. Os assets podem ser reutilizados pelo navegador por 24 horas; o HTML continua sendo revalidado.

O rastreador de visitas e cliques no checkout mantém os UTMs e funciona mesmo quando randomUUID, armazenamento de sessão ou sendBeacon não estão disponíveis. Os dados de visita desse rastreador não são equivalentes à atribuição de PageView do Meta.
