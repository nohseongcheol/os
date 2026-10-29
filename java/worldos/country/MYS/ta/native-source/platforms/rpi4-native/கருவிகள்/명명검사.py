#!/usr/bin/env python3
"""명명 கிளிப்·விதிவிலக்கு·경로를 검사한다. --시언어는 libclang அறிவிப்பு 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

திட்டப்பணி_மூலம் = Path(__file__).resolve().parents[1]
தொகுபதிவகம்_மூலம் = திட்டப்பணி_மூலம்.parents[1]

def செயல்படுத்துக():
    பார்சர்_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    பார்சர்_48ee4b1b.add_argument('--시언어', action='store_true')
    செயலுருபுகள் = பார்சர்_48ee4b1b.parse_args()
    실패들 = []
    வேலை_மதிப்பு_102996da = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    அளவுரு_அட்டவணை = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [தொகுபதிவகம்_மூலம்/'compiler/컴파일러.py', தொகுபதிவகம்_மூலம்/'compiler/기계어미리번역.py']
    for பாதை_2 in list((திட்டப்பணி_மூலம்/'கருவிகள்').glob('*.py')) + list((திட்டப்பணி_மூலம்/'예제').rglob('*.py')) + 공용번역기들:
        if பாதை_2.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(பாதை_2.read_text()); 나무들[பாதை_2] = 나무
        for உள்ளீடு_மதிப்பு in ast.walk(나무):
            if isinstance(உள்ளீடு_மதிப்பு, ast.FunctionDef):
                அளவுரு_அட்டவணை.setdefault(உள்ளீடு_மதிப்பு.name, set()).update(அளவுரு_மதிப்புரு.arg for அளவுரு_மதிப்புரு in உள்ளீடு_மதிப்பு.args.args + உள்ளீடு_மதிப்பு.args.kwonlyargs)
                if உள்ளீடு_மதிப்பு.args.kwarg: 가변매개함수.add(உள்ளீடு_மதிப்பு.name)
            if isinstance(உள்ளீடு_மதிப்பு, ast.ClassDef):
                for செயல்பாடு_மதிப்பு in உள்ளீடு_மதிப்பு.body:
                    if isinstance(செயல்பாடு_மதிப்பு, ast.FunctionDef) and செயல்பாடு_மதிப்பு.name == '__init__':
                        அளவுரு_அட்டவணை.setdefault(உள்ளீடு_மதிப்பு.name, set()).update(அளவுரு_மதிப்புரு.arg for அளவுரு_மதிப்புரு in செயல்பாடு_மதிப்பு.args.args + செயல்பாடு_மதிப்பு.args.kwonlyargs)
            பெயர் = ''
            if isinstance(உள்ளீடு_மதிப்பு, (ast.FunctionDef, ast.ClassDef)): பெயர் = உள்ளீடு_மதிப்பு.name
            elif isinstance(உள்ளீடு_மதிப்பு, ast.Name) and isinstance(உள்ளீடு_மதிப்பு.ctx, ast.Store): பெயர் = உள்ளீடு_மதிப்பு.id
            elif isinstance(உள்ளீடு_மதிப்பு, ast.arg): பெயர் = உள்ளீடு_மதிப்பு.arg
            if பெயர் and பெயர் not in வேலை_மதிப்பு_102996da and all(ord(எழுத்துக்குறி_மதிப்பு)<128 for எழுத்துக்குறி_மதிப்பு in பெயர்):
                실패들.append('{}:{}: {}'.format(பாதை_2.relative_to(தொகுபதிவகம்_மூலம்), உள்ளீடு_மதிப்பு.lineno, பெயர்))
    for பாதை_2, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            பெயர் = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if பெயர் not in அளவுரு_அட்டவணை or பெயர் in 가변매개함수 or not any(ord(எழுத்துக்குறி_மதிப்பு)>127 for எழுத்துக்குறி_மதிப்பு in பெயர்): continue
            for அளவுரு_மதிப்புரு in 호출.keywords:
                if அளவுரு_மதிப்புரு.arg and அளவுரு_மதிப்புரு.arg not in அளவுரு_அட்டவணை[பெயர்]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(பாதை_2.relative_to(தொகுபதிவகம்_மூலம்), 호출.lineno, பெயர், அளவுரு_மதிப்புரு.arg))
    for உள்ளீட்டு_வரி in (திட்டப்பணி_மூலம்/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, செயலகம்_மதிப்பு_உள்ளீடு = உள்ளீட்டு_வரி.split('\t')
        if not (திட்டப்பணி_மூலம்/현재).is_file(): 실패들.append('நகர்த்து_மதிப்பு கோப்பின்_பெயர் 없음: '+현재)
        if செயலகம்_மதிப்பு_உள்ளீடு == '호환진입점유지' and not (திட்டப்பணி_மூலம்/이전).is_file(): 실패들.append('호환 நுழைவுப்_புள்ளி 없음: '+이전)
    예제 = (திட்டப்பணி_மூலம்.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for பாதை_2 in sorted((திட்டப்பணி_மூலம்.parents[1]/'example/java').glob('*.java')):
        மூலக்_கோப்பு = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', பாதை_2.read_text())
        for பெயர் in re.findall(r'\b[^\W\d]\w*\b', மூலக்_கோப்பு, re.UNICODE):
            if பெயர் not in 예약어 and all(ord(எழுத்துக்குறி_மதிப்பு)<128 for எழுத்துக்குறி_மதிப்பு in பெயர்):
                실패들.append('{}: 예제의 영어 அடையாளங்காட்டி_மதிப்பு {}'.format(பாதை_2.name, பெயர்))
    for பெயர் in ('창', 'பொத்தான்', 'விளக்கச்சீட்டு', 'உரைப்_புலம்', '화면구성요소', 'நிகழ்வு_சாரை', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        மூலக்_கோப்பு = (திட்டப்பணி_மூலம்/'한국어자바/தமிழ்/자체'/(பெயர்+'.java')).read_text()
        மூலக்_கோப்பு = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', மூலக்_கோப்பு)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', மூலக்_கோப்பு):
            실패들.append(பெயர்+': தமிழ் 직접 구현에 표준 பொருள்_மதிப்பு 래퍼가 남았습니다.')
    시언어예제 = (திட்டப்பணி_மூலம்.parents[1]/'example/c/네트워크예제.c').read_text()
    for பெயர் in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if பெயர் in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 பெயர்: '+பெயர்)
    파이썬예제 = (திட்டப்பணி_மூலம்.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 விதிவிலக்கு 직접 사용')
    머리 = (திட்டப்பணி_மூலம்.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for பெயர் in ('இணையம்_குடும்பம்', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', 'உருவாக்கு_முடிவுப்_புள்ளி', '자료전문보내기'):
        if re.search(r'^#define\s+'+பெயர்+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 மேக்ரோ_மதிப்பு 사용: '+பெயர்)
    자바파일수 = 0
    for மூலம்_மதிப்பு in ('மூலக்_கோப்பு', 'பயனர்/자바', '한국어자바'):
        for பாதை_2 in (திட்டப்பணி_மூலம்/மூலம்_மதிப்பு).rglob('*.java'):
            자바파일수 += 1
            மூலக்_கோப்பு = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', பாதை_2.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', மூலக்_கோப்பு):
                실패들.append('{}: 한국어화되지 않은 அறிவிப்பு {}'.format(பாதை_2.relative_to(திட்டப்பணி_மூலம்), 맞음[1]))
            if மூலம்_மதிப்பு == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', மூலக்_கோப்பு):
                실패들.append('{}: 공개 விதிவிலக்கு அறிவிப்பு'.format(பாதை_2.relative_to(திட்டப்பணி_மூலம்)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for பாதை_2 in sorted((தொகுபதிவகம்_மூலம்/'os/மூலக்_கோப்பு').glob('*.java')):
        x86자바파일수 += 1
        மூலக்_கோப்பு = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', பாதை_2.read_text())
        for பெயர் in re.findall(r'\b[^\W\d]\w*\b', மூலக்_கோப்பு, re.UNICODE):
            if பெயர் not in 예약어 | 표준자바이름 and all(ord(எழுத்துக்குறி_மதிப்பு)<128 for எழுத்துக்குறி_மதிப்பு in பெயர்):
                실패들.append('{}: 자체 영어 அடையாளங்காட்டி_மதிப்பு {}'.format(பாதை_2.relative_to(தொகுபதிவகம்_மூலம்), பெயர்))
    பதிவு_பதிவு = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if செயலுருபுகள்.시언어:
        subprocess.check_call(['python3', str(திட்டப்பணி_மூலம்/'கருவிகள்/시언어이름분석.py')])
        분석 = json.loads((திட்டப்பணி_மூலம்/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(பிழை) for பிழை in 분석['பிழை'])
        공개규약 = set(json.loads((திட்டப்பணி_மூலம்/'명명/규격이름.json').read_text()))
        for உள்ளீடு_மதிப்பு in 분석['அறிவிப்பு'].values():
            பெயர் = உள்ளீடு_மதிப்பு['பெயர்']; பாதை_2 = Path(உள்ளீடு_மதிப்பு['கோப்பின்_பெயர்'])
            மூலக்_கோப்பு = பாதை_2.read_bytes()
            # தமிழ் 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if மூலக்_கோப்பு[உள்ளீடு_மதிப்பு['ஆஃப்செட்_மதிப்பு']:உள்ளீடு_மதிப்பு['ஆஃப்செட்_மதிப்பு']+len(பெயர்)] == பெயர்.encode() and பெயர் not in 공개규약:
                실패들.append('{}:{}: {}'.format(பாதை_2.relative_to(திட்டப்பணி_மூலம்), உள்ளீடு_மதிப்பு['உள்ளீட்டு_வரி'], பெயர்))
        பதிவு_பதிவு['c_semantic_checked'] = True
        பதிவு_பதிவு['c_source_sha256'] = {str(Path(கோப்பின்_பெயர்).relative_to(திட்டப்பணி_மூலம்)):ஹாஷ்_கோப்பு for கோப்பின்_பெயர்,ஹாஷ்_கோப்பு in 분석['원문해시'].items()}
    பதிவு_பதிவு['passed'] = not 실패들; பதிவு_பதிவு['failures'] = 실패들
    இலக்கு_மதிப்பு = திட்டப்பணி_மூலம்/'build/verification/naming'; இலக்கு_மதிப்பு.mkdir(parents=True, exist_ok=True)
    (இலக்கு_மதிப்பு/'report.json').write_text(json.dumps(பதிவு_பதிவு, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: தமிழ் அறிவிப்பு·கோப்பின்_பெயர் பாதை_2·호환 நுழைவுப்_புள்ளி·통신 예제')

if __name__ == '__main__': செயல்படுத்துக()
