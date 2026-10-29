#!/usr/bin/env python3
"""명명 ဖြတ်နယ်ပယ်·ခြွင်းချက်·경로를 검사한다. --시언어는 libclang ကြေညာချက် 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

စီမံကိန်းအမြစ် = Path(__file__).resolve().parents[1]
저장소 = စီမံကိန်းအမြစ်.parents[1]

def လုပ်ဆောင်():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--Cဘာသာစကား', action='store_true')
    အချက်များ = 해석기.parse_args()
    실패들 = []
    သဘောတူစည်းမျဉ်းတန်ဖိုး = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    ဖိုင်အရေအတွက် = 0
    သတ်မှတ်အချက်ဇယား = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/ဘာသာပြန်စက်.py', 저장소/'compiler/ကြိုတင်ဘာသာပြန်.py']
    for လမ်း in list((စီမံကိန်းအမြစ်/'ကိရိယာစု').glob('*.py')) + list((စီမံကိန်းအမြစ်/'ဥပမာ').rglob('*.py')) + 공용번역기들:
        if လမ်း.name.endswith(('이름반영.py', '이름분석.py')): continue
        ဖိုင်အရေအတွက် += 1
        나무 = ast.parse(လမ်း.read_text()); 나무들[လမ်း] = 나무
        for အချက်တန်ဖိုး in ast.walk(나무):
            if isinstance(အချက်တန်ဖိုး, ast.FunctionDef):
                သတ်မှတ်အချက်ဇယား.setdefault(အချက်တန်ဖိုး.name, set()).update(သတ်မှတ်အချက်ပေးအချက်.arg for သတ်မှတ်အချက်ပေးအချက် in အချက်တန်ဖိုး.args.args + အချက်တန်ဖိုး.args.kwonlyargs)
                if အချက်တန်ဖိုး.args.kwarg: 가변매개함수.add(အချက်တန်ဖိုး.name)
            if isinstance(အချက်တန်ဖိုး, ast.ClassDef):
                for လုပ်ဆောင်ချက် in အချက်တန်ဖိုး.body:
                    if isinstance(လုပ်ဆောင်ချက်, ast.FunctionDef) and လုပ်ဆောင်ချက်.name == '__init__':
                        သတ်မှတ်အချက်ဇယား.setdefault(အချက်တန်ဖိုး.name, set()).update(သတ်မှတ်အချက်ပေးအချက်.arg for သတ်မှတ်အချက်ပေးအချက် in လုပ်ဆောင်ချက်.args.args + လုပ်ဆောင်ချက်.args.kwonlyargs)
            အမည် = ''
            if isinstance(အချက်တန်ဖိုး, (ast.FunctionDef, ast.ClassDef)): အမည် = အချက်တန်ဖိုး.name
            elif isinstance(အချက်တန်ဖိုး, ast.Name) and isinstance(အချက်တန်ဖိုး.ctx, ast.Store): အမည် = အချက်တန်ဖိုး.id
            elif isinstance(အချက်တန်ဖိုး, ast.arg): အမည် = အချက်တန်ဖိုး.arg
            if အမည် and အမည် not in သဘောတူစည်းမျဉ်းတန်ဖိုး and all(ord(အက္ခရာတန်ဖိုး)<128 for အက္ခရာတန်ဖိုး in အမည်):
                실패들.append('{}:{}: {}'.format(လမ်း.relative_to(저장소), အချက်တန်ဖိုး.lineno, အမည်))
    for လမ်း, 나무 in 나무들.items():
        for ခေါ်လုပ် in ast.walk(나무):
            if not isinstance(ခေါ်လုပ်, ast.Call): continue
            အမည် = ခေါ်လုပ်.func.id if isinstance(ခေါ်လုပ်.func, ast.Name) else ခေါ်လုပ်.func.attr if isinstance(ခေါ်လုပ်.func, ast.Attribute) else ''
            if အမည် not in သတ်မှတ်အချက်ဇယား or အမည် in 가변매개함수 or not any(ord(အက္ခရာတန်ဖိုး)>127 for အက္ခရာတန်ဖိုး in အမည်): continue
            for သတ်မှတ်အချက်ပေးအချက် in ခေါ်လုပ်.keywords:
                if သတ်မှတ်အချက်ပေးအချက်.arg and သတ်မှတ်အချက်ပေးအချက်.arg not in သတ်မှတ်အချက်ဇယား[အမည်]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(လမ်း.relative_to(저장소), ခေါ်လုပ်.lineno, အမည်, သတ်မှတ်အချက်ပေးအချက်.arg))
    for စာကြောင်း in (စီမံကိန်းအမြစ်/'명명/ဖိုင်အမည်ချိတ်ဆက်ပုံ.tsv').read_text().splitlines()[1:]:
        ယခင်အချက်အလက်တစ်ခု, လက်ရှိအချက်အလက်တစ်ခု, လုပ်ငန်းစဉ်တန်ဖိုးအချက် = စာကြောင်း.split('\t')
        if not (စီမံကိန်းအမြစ်/လက်ရှိအချက်အလက်တစ်ခု).is_file(): 실패들.append('ရွှေ့တန်ဖိုး ဖိုင် 없음: '+လက်ရှိအချက်အလက်တစ်ခု)
        if လုပ်ငန်းစဉ်တန်ဖိုးအချက် == '호환진입점유지' and not (စီမံကိန်းအမြစ်/ယခင်အချက်အလက်တစ်ခု).is_file(): 실패들.append('호환 အချက်အမှတ်တစ်ခု 없음: '+ယခင်အချက်အလက်တစ်ခု)
    ဥပမာ = (စီမံကိန်းအမြစ်.parents[1]/'example/java/ကွန်ရက်ဥပမာ.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in ဥပမာ: 실패들.append('ကွန်ရက်ဆက် 예제에 남은 표준 직접 ခေါ်လုပ်: '+금지호출)
    # 사용자가 읽는 Java 예제는 သီးသန့်စကားလုံးများ/리터럴을 제외한 식별자도 အားလုံးတည်ဆောက် 한국어다.
    သီးသန့်စကားလုံးများ = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for လမ်း in sorted((စီမံကိန်းအမြစ်.parents[1]/'example/java').glob('*.java')):
        မူရင်းကုဒ် = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', လမ်း.read_text())
        for အမည် in re.findall(r'\b[^\W\d]\w*\b', မူရင်းကုဒ်, re.UNICODE):
            if အမည် not in သီးသန့်စကားလုံးများ and all(ord(အက္ခရာတန်ဖိုး)<128 for အက္ခရာတန်ဖိုး in အမည်):
                실패들.append('{}: 예제의 영어 သတ်မှတ်နံပါတ်တန်ဖိုး {}'.format(လမ်း.name, အမည်))
    for အမည် in ('창', 'ခလုတ်', 'အညွှန်းစာ', 'စာသားအကွက်', 'မျက်နှာပြင်အင်္ဂါရပ်', 'ဖြစ်ရပ်တန်းစီရာ', 'အလုပ်သမား', 'လုပ်ဆောင်ရန်အလုပ်', 'လှုပ်ရှားမှုလက်ခံသူ', 'လှုပ်ရှားမှုအသိပေးချက်', 'အလုပ်'):
        မူရင်းကုဒ် = (စီမံကိန်းအမြစ်/'မြန်မာJava/မြန်မာ/ကိုယ်ပိုင်'/(အမည်+'.java')).read_text()
        မူရင်းကုဒ် = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', မူရင်းကုဒ်)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', မူရင်းကုဒ်):
            실패들.append(အမည်+': မြန်မာ 직접 구현에 표준 အရာဝတ္ထုတန်ဖိုး 래퍼가 남았습니다.')
    Cဥပမာ = (စီမံကိန်းအမြစ်.parents[1]/'example/c/ကွန်ရက်ဥပမာ.c').read_text()
    for အမည် in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if အမည် in Cဥပမာ: 실패들.append('C ဆက်သွယ်မှု 예제에 남은 표준 အမည်: '+အမည်)
    Pythonဥပမာ = (စီမံကိန်းအမြစ်.parents[1]/'example/python/ကွန်ရက်ဥပမာ.py').read_text()
    if 'OSError' in Pythonဥပမာ or '.args' in Pythonဥပမာ: 실패들.append('Python ဆက်သွယ်မှု 예제에 남은 표준 ခြွင်းချက် 직접 သုံးစွဲမှု')
    ဦးခေါင်းတန်ဖိုး = (စီမံကိန်းအမြစ်.parents[1]/'posix-kor/arm64-native/ခေါင်းစီးဖိုင်/통신규약.h').read_text()
    for အမည် in ('အင်တာနက်မျိုးစု', 'ဒေတာစာကွန်ရက်ပေါက်', 'ဒေတာစာဆက်သွယ်စည်းမျဉ်း', 'ကွန်ရက်ပေါက်လိပ်စာ', 'အင်တာနက်ကွန်ရက်ပေါက်လိပ်စာ', 'အဆုံးမှတ်ဖန်တီး', 'ဒေတာစာဒေတာပို့'):
        if re.search(r'^#define\s+'+အမည်+r'\b', ဦးခေါင်းတန်ဖိုး, re.M): 실패들.append('C 직접 အကောင်အထည်ဖော်မှု 대신 매크로 သုံးစွဲမှု: '+အမည်)
    Javaဖိုင်အရေအတွက် = 0
    for အမြစ်တန်ဖိုး in ('မူရင်းကုဒ်', 'သုံးစွဲသူ/Java', 'မြန်မာJava'):
        for လမ်း in (စီမံကိန်းအမြစ်/အမြစ်တန်ဖိုး).rglob('*.java'):
            Javaဖိုင်အရေအတွက် += 1
            မူရင်းကုဒ် = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', လမ်း.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', မူရင်းကုဒ်):
                실패들.append('{}: 한국어화되지 않은 ကြေညာချက် {}'.format(လမ်း.relative_to(စီမံကိန်းအမြစ်), 맞음[1]))
            if အမြစ်တန်ဖိုး == 'မြန်မာJava' and re.search(r'\bthrows\s+[A-Za-z]', မူရင်းကုဒ်):
                실패들.append('{}: 공개 ခြွင်းချက် ကြေညာချက်'.format(လမ်း.relative_to(စီမံကိန်းအမြစ်)))
    x86Javaဖိုင်အရေအတွက် = 0
    စံJavaအမည်များ = {'String', 'length', 'charAt'}
    for လမ်း in sorted((저장소/'os/မူရင်းကုဒ်').glob('*.java')):
        x86Javaဖိုင်အရေအတွက် += 1
        မူရင်းကုဒ် = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', လမ်း.read_text())
        for အမည် in re.findall(r'\b[^\W\d]\w*\b', မူရင်းကုဒ်, re.UNICODE):
            if အမည် not in သီးသန့်စကားလုံးများ | စံJavaအမည်များ and all(ord(အက္ခရာတန်ဖိုး)<128 for အက္ခရာတန်ဖိုး in အမည်):
                실패들.append('{}: ကိုယ်ပိုင် 영어 သတ်မှတ်နံပါတ်တန်ဖိုး {}'.format(လမ်း.relative_to(저장소), အမည်))
    မှတ်တမ်းမှတ်တမ်းတစ်ခု = {'passed': False, 'python_files': ဖိုင်အရေအတွက်, 'java_files': Javaဖိုင်အရေအတွက်,
          'x86_java_files': x86Javaဖိုင်အရေအတွက်, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if အချက်များ.Cဘာသာစကား:
        subprocess.check_call(['python3', str(စီမံကိန်းအမြစ်/'ကိရိယာစု/Cအမည်များခွဲခြမ်းစိတ်ဖြာ.py')])
        တန်ဖိုးခွဲခြမ်းစိတ်ဖြာ = json.loads((စီမံကိန်းအမြစ်/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(အမှား) for အမှား in တန်ဖိုးခွဲခြမ်းစိတ်ဖြာ['အမှား'])
        공개규약 = set(json.loads((စီမံကိန်းအမြစ်/'명명/စံအမည်များ.json').read_text()))
        for အချက်တန်ဖိုး in တန်ဖိုးခွဲခြမ်းစိတ်ဖြာ['ကြေညာချက်'].values():
            အမည် = အချက်တန်ဖိုး['အမည်']; လမ်း = Path(အချက်တန်ဖိုး['ဖိုင်'])
            မူရင်းကုဒ် = လမ်း.read_bytes()
            # မြန်မာ 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if မူရင်းကုဒ်[အချက်တန်ဖိုး['အရွေ့တန်ဖိုး']:အချက်တန်ဖိုး['အရွေ့တန်ဖိုး']+len(အမည်)] == အမည်.encode() and အမည် not in 공개규약:
                실패들.append('{}:{}: {}'.format(လမ်း.relative_to(စီမံကိန်းအမြစ်), အချက်တန်ဖိုး['줄'], အမည်))
        မှတ်တမ်းမှတ်တမ်းတစ်ခု['c_semantic_checked'] = True
        မှတ်တမ်းမှတ်တမ်းတစ်ခု['c_source_sha256'] = {str(Path(ဖိုင်).relative_to(စီမံကိန်းအမြစ်)):ဖိုင်ဟက်ရှ်တွက် for ဖိုင်,ဖိုင်ဟက်ရှ်တွက် in တန်ဖိုးခွဲခြမ်းစိတ်ဖြာ['원문해시'].items()}
    မှတ်တမ်းမှတ်တမ်းတစ်ခု['passed'] = not 실패들; မှတ်တမ်းမှတ်တမ်းတစ်ခု['failures'] = 실패들
    ဦးတည်ရာတန်ဖိုး = စီမံကိန်းအမြစ်/'build/verification/naming'; ဦးတည်ရာတန်ဖိုး.mkdir(parents=True, exist_ok=True)
    (ဦးတည်ရာတန်ဖိုး/'report.json').write_text(json.dumps(မှတ်တမ်းမှတ်တမ်းတစ်ခု, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: မြန်မာ ကြေညာချက်·ဖိုင် လမ်း·호환 အချက်အမှတ်တစ်ခု·ဆက်သွယ်မှု ဥပမာ')

if __name__ == '__main__': လုပ်ဆောင်()
