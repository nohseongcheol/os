#!/usr/bin/env python3
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
filesystem=ROOT/'build/rootfs'
languages=json.loads((ROOT/'naming/terms.json').read_text())
iso=json.loads(Path('/usr/share/iso-codes/json/iso_639-3.json').read_text())['639-3']
short={x['alpha_3']:x.get('alpha_2',x['alpha_3']) for x in iso}
layouts={}
for layout in ET.parse(str(filesystem/'usr/share/X11/xkb/rules/base.xml')).findall('.//layoutList/layout'):
    config=layout.find('configItem');name=config.findtext('name')
    for code in config.findall('languageList/iso639Id'):
        language=short.get(code.text,code.text);layouts.setdefault(language,[]).append(name)
m17n={}
for path in (filesystem/'usr/share/m17n').glob('*.mim'):
    match=re.search(r'^\(input-method\s+([^\s()]+)\s+([^\s()]+)',path.read_text(errors='replace'),re.M)
    if match and match.group(2) not in ['kbd','anthy','han2','romaja']:
        m17n.setdefault(match.group(1),[]).append(match.group(2))
preferred={'en':'keyboard-us','ko':'hangul','ja':'anthy','zh':'pinyin','zh_Hant':'rime','vi':'unikey','hi':'m17n_hi_itrans','bn':'m17n_bn_inscript','ta':'m17n_ta_tamil99','te':'m17n_te_inscript'}
output={}
for lang in languages:
    base=lang.split('_')[0];choices=layouts.get(base,[])
    if lang in preferred:engine=preferred[lang];source='Explicit installed input engine'
    elif base in m17n and '_' not in lang:
        names=m17n[base];name=next((x for x in ['inscript','itrans','phonetic','rom'] if x in names),sorted(names)[0]);engine='m17n_'+base+'_'+name;source='Installed m17n input-method definition'
    elif choices:
        layout=base if base in choices else ('us' if 'us' in choices else choices[0]);engine='keyboard-'+layout;source='XKeyboardConfig language association; script variant needs review'
    else:engine='keyboard-us';source='Fallback keyboard; use Unicode entry or configure another installed engine'
    output[lang]={'engine':engine,'source':source,'review':'pending'}
(ROOT/'naming/input-methods.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print('Input profiles',len(output))
