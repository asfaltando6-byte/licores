"""Requer Pillow. Gera imagens responsivas sem alterar as imagens de origem."""
from pathlib import Path
from PIL import Image
import re, json
root=Path(__file__).resolve().parents[1]
assets=root/'dist/assets'
page=root/'dist/index.html'
html=page.read_text()
if 'imagesrcset=' in html:
    print('As versões responsivas já foram geradas. Restaure o HTML de origem para regenerar.')
    raise SystemExit(0)
used=sorted(set(re.findall(r'src="assets/([^"/]+)\.webp"',html)))
stats=[]
for stem in used:
    image=Image.open(assets/(stem+'.webp')).convert('RGB')
    widths=[480,800,1200] if stem=='mockup' else [400,640,1000]
    widths=[w for w in widths if w<=image.width]
    if not widths or widths[-1]<min(image.width,1000): widths.append(min(image.width,1000))
    variants=[]
    for width in widths:
        resized=image.resize((width,round(image.height*width/image.width)),Image.Resampling.LANCZOS)
        target=assets/f'{stem}-{width}w.webp'
        resized.save(target,'WEBP',quality=79,method=6)
        variants.append((width,target.name,target.stat().st_size))
    stats.append({'image':stem,'original_bytes':(assets/(stem+'.webp')).stat().st_size,'variants':variants})
# Background uses the same composition and dimensions, with a mobile alternative.
im=Image.open(assets/'hero-bg.webp').convert('RGB')
for width in [800,1500]:
    im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS).save(assets/f'hero-bg-{width}w.webp','WEBP',quality=78,method=6)
# srcset lets each display download the appropriate file for its width and density.
def responsive(match):
    tag=match.group(0)
    stem=re.search(r'src="assets/([^"/]+)\.webp"',tag).group(1)
    stat=next(x for x in stats if x['image']==stem)
    ishero='class="hero-img"' in tag
    isplan='class="plan-img"' in tag
    sizes='(max-width: 856px) calc(100vw - 56px), 800px' if ishero else ('(max-width: 760px) calc(100vw - 56px), 410px' if isplan else ('(max-width: 760px) calc((100vw - 40px)*0.78), 340px' if stem.startswith('licor-') else '(max-width: 760px) calc(100vw - 56px), 350px'))
    default=stat['variants'][1 if len(stat['variants'])>1 else 0][1]
    tag=tag.replace(f'src="assets/{stem}.webp"',f'src="assets/{default}"')
    srcset=', '.join(f'assets/{name} {w}w' for w,name,_ in stat['variants'])
    tag=tag[:-1]+f' srcset="{srcset}" sizes="{sizes}" decoding="async">'
    return tag
html=re.sub(r'<img\b[^>]*src="assets/[^"/]+\.webp"[^>]*>',responsive,html)
html=html.replace("url('assets/hero-bg.webp')", "url('assets/hero-bg-1500w.webp')")
html=html.replace('</style>',"@media(max-width:760px){.hero{background-image:url('assets/hero-bg-800w.webp')}}"+'</style>')
hero=next(x for x in stats if x['image']=='mockup')
hero_srcset=', '.join(f'assets/{name} {w}w' for w,name,_ in hero['variants'])
preload=f'<link rel="preload" as="image" href="assets/mockup-800w.webp" imagesrcset="{hero_srcset}" imagesizes="(max-width: 856px) calc(100vw - 56px), 800px" fetchpriority="high">'
html=html.replace('</head>',preload+'</head>')
page.write_text(html)
(root/'outputs/image-optimization.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2))
print(json.dumps({'original_referenced_images_bytes':sum(x['original_bytes'] for x in stats),'desktop_640w_bytes':sum(min(x['variants'],key=lambda v:abs(v[0]-640))[2] for x in stats),'mobile_400w_bytes':sum(x['variants'][0][2] for x in stats)},indent=2))
