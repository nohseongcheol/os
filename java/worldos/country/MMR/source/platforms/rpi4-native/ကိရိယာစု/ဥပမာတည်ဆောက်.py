"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from Javaစာကြည့်တိုက်တည်ဆောက် import Javaစာကြည့်တိုက်ဖန်တီး


def ဥပမာများဖန်တီး(အမြစ်လမ်းကြောင်း, 저장소경로, စက်မောင်း):
    မူရင်းဒေတာ=저장소경로/'example';ရလဒ်ဒေတာ=အမြစ်လမ်းကြောင်း/'build/examples';ရလဒ်ဒေတာ.mkdir(parents=True,exist_ok=True)
    အတန်းလမ်းကြောင်း=ရလဒ်ဒေတာ/'classes';အတန်းလမ်းကြောင်း.mkdir(exist_ok=True)
    Javaစာကြည့်တိုက်ဖန်တီး(အမြစ်လမ်းကြောင်း,စက်မောင်း)
    ip_settings = read_config(အမြစ်လမ်းကြောင်း)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = ရလဒ်ဒေတာ/'java-source'; java_sources.mkdir(exist_ok=True)
    Javaလုပ်ဆောင်=[]
    for path in sorted((မူရင်းဒေတာ/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); Javaလုပ်ဆောင်.append(target)
    စက်မောင်း(['javac','--release','8','-encoding','UTF-8','-cp',အမြစ်လမ်းကြောင်း/'build/java-library/classes','-d',အတန်းလမ်းကြောင်း]+Javaလုပ်ဆောင်)
    စက်ညွှန်ကြားချက်အစဉ်လိုက်=['public final class ဥပမာအထုပ် { public static int တန်ဖိုးတပ်ဆင်(int ဘာသာစကား) { int ကိုင်တွယ်ပြီးတန်ဖိုး;',
          'ကိုင်တွယ်ပြီးတန်ဖိုး=အမိန့်အဓိပ္ပာယ်ဖော်.ဥပမာဖိုင်တွဲ("/example"); if(ကိုင်တွယ်ပြီးတန်ဖိုး<0)return ကိုင်တွယ်ပြီးတန်ဖိုး;']
    꾸러미명세={}
    안내자료=guest_bytes(မူရင်းဒေတာ/'README.md')
    if len(안내자료)>16384: raise ValueError('example README exceeds native VFS limit')
    စက်ညွှန်ကြားချက်အစဉ်လိုက်.append('ကိုင်တွယ်ပြီးတန်ဖိုး=အမိန့်အဓိပ္ပာယ်ဖော်.ဥပမာဖိုင်("/example/README.md","%s"); if(ကိုင်တွယ်ပြီးတန်ဖိုး<0)return ကိုင်တွယ်ပြီးတန်ဖိုး;'%안내자료.hex())
    꾸러미명세['/example/README.md']={'bytes':len(안내자료),'sha256':hashlib.sha256(안내자료).hexdigest()}
    စက်ညွှန်ကြားချက်အစဉ်လိုက်.append('if(ဘာသာစကား==0){ကိုင်တွယ်ပြီးတန်ဖိုး=အမိန့်အဓိပ္ပာယ်ဖော်.ဥပမာဖိုင်တွဲ("/lib"); if(ကိုင်တွယ်ပြီးတန်ဖိုး<0)return ကိုင်တွယ်ပြီးတန်ဖိုး;')
    for လမ်း in [မူရင်းဒေတာ/'python/မြန်မာ.py'] + sorted((အမြစ်လမ်းကြောင်း/'Pythonတံတား/စာကြည့်တိုက်').glob('*.py')):
        အကြောင်းအရာတန်ဖိုး=guest_bytes(လမ်း);ဦးတည်ချက်တန်ဖိုး='/lib/'+လမ်း.name
        if len(အကြောင်းအရာတန်ဖိုး)>16384 or len(ဦးတည်ချက်တန်ဖိုး.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+ဦးတည်ချက်တန်ဖိုး)
        စက်ညွှန်ကြားချက်အစဉ်လိုက်.append('ကိုင်တွယ်ပြီးတန်ဖိုး=အမိန့်အဓိပ္ပာယ်ဖော်.ဥပမာဖိုင်(%s,"%s"); if(ကိုင်တွယ်ပြီးတန်ဖိုး<0)return ကိုင်တွယ်ပြီးတန်ဖိုး;'%(json.dumps(ဦးတည်ချက်တန်ဖိုး,ensure_ascii=True),အကြောင်းအရာတန်ဖိုး.hex()))
        꾸러미명세[ဦးတည်ချက်တန်ဖိုး]={'bytes':len(အကြောင်းအရာတန်ဖိုး),'sha256':hashlib.sha256(အကြောင်းအရာတန်ဖိုး).hexdigest()}
    စက်ညွှန်ကြားချက်အစဉ်လိုက်.append('}')
    for ရှာကြည့်အညွှန်းကိန်း,ဘာသာစကား in enumerate(('java','c','python')):
        ဖိုင်စာရင်း=[(ဒေတာနေရာ.name,ဒေတာနေရာ) for ဒေတာနေရာ in sorted((မူရင်းဒေတာ/ဘာသာစကား).iterdir()) if ဒေတာနေရာ.is_file()]
        if ဘာသာစကား=='java':ဖိုင်စာရင်း += [(ဒေတာနေရာ.stem+'.class',အတန်းလမ်းကြောင်း/(ဒေတာနေရာ.stem+'.class')) for ဒေတာနေရာ in Javaလုပ်ဆောင်]
        စက်ညွှန်ကြားချက်အစဉ်လိုက် += ['if(ဘာသာစကား==%d){'%ရှာကြည့်အညွှန်းကိန်း,'ကိုင်တွယ်ပြီးတန်ဖိုး=အမိန့်အဓိပ္ပာယ်ဖော်.ဥပမာဖိုင်တွဲ("/example/%s"); if(ကိုင်တွယ်ပြီးတန်ဖိုး<0)return ကိုင်တွယ်ပြီးတန်ဖိုး;'%ဘာသာစကား]
        for အမည်,လမ်း in ဖိုင်စာရင်း:
            အကြောင်းအရာတန်ဖိုး=guest_bytes(လမ်း);ဦးတည်ချက်တန်ဖိုး='/example/'+ဘာသာစကား+'/'+အမည်
            if len(အကြောင်းအရာတန်ဖိုး)>16384 or len(ဦးတည်ချက်တန်ဖိုး.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+ဦးတည်ချက်တန်ဖိုး)
            စက်ညွှန်ကြားချက်အစဉ်လိုက်.append('ကိုင်တွယ်ပြီးတန်ဖိုး=အမိန့်အဓိပ္ပာယ်ဖော်.ဥပမာဖိုင်(%s,"%s"); if(ကိုင်တွယ်ပြီးတန်ဖိုး<0)return ကိုင်တွယ်ပြီးတန်ဖိုး;'%(json.dumps(ဦးတည်ချက်တန်ဖိုး,ensure_ascii=True),အကြောင်းအရာတန်ဖိုး.hex()))
            꾸러미명세[ဦးတည်ချက်တန်ဖိုး]={'bytes':len(အကြောင်းအရာတန်ဖိုး),'sha256':hashlib.sha256(အကြောင်းအရာတန်ဖိုး).hexdigest()}
        စက်ညွှန်ကြားချက်အစဉ်လိုက် += ['return 0;}']
    စက်ညွှန်ကြားချက်အစဉ်လိုက် += ['return -22;}}']
    (အမြစ်လမ်းကြောင်း/'build/ဥပမာအထုပ်.java').write_text('\n'.join(စက်ညွှန်ကြားချက်အစဉ်လိုက်)+'\n')
    (ရလဒ်ဒေတာ/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
