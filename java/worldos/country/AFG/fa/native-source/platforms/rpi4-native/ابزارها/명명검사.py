#!/usr/bin/env python3
"""명명 کلیپ·استثنا·경로를 검사한다. --시언어는 libclang اعلامیه 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

نمایش_دادن_جذر = Path(__file__).resolve().parents[1]
مخزن_جذر = نمایش_دادن_جذر.parents[1]

def اجرا_2():
    مفسر_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    مفسر_48ee4b1b.add_argument('--시언어', action='store_true')
    نشانوندها = مفسر_48ee4b1b.parse_args()
    실패들 = []
    شغل_مقدار = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    پارامتر_جدول = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [مخزن_جذر/'compiler/컴파일러.py', مخزن_جذر/'compiler/기계어미리번역.py']
    for مسیر in list((نمایش_دادن_جذر/'ابزارها').glob('*.py')) + list((نمایش_دادن_جذر/'예제').rglob('*.py')) + 공용번역기들:
        if مسیر.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(مسیر.read_text()); 나무들[مسیر] = 나무
        for ورودی_مقدار in ast.walk(나무):
            if isinstance(ورودی_مقدار, ast.FunctionDef):
                پارامتر_جدول.setdefault(ورودی_مقدار.name, set()).update(پارامتر_آرگومان.arg for پارامتر_آرگومان in ورودی_مقدار.args.args + ورودی_مقدار.args.kwonlyargs)
                if ورودی_مقدار.args.kwarg: 가변매개함수.add(ورودی_مقدار.name)
            if isinstance(ورودی_مقدار, ast.ClassDef):
                for عملکرد_مقدار in ورودی_مقدار.body:
                    if isinstance(عملکرد_مقدار, ast.FunctionDef) and عملکرد_مقدار.name == '__init__':
                        پارامتر_جدول.setdefault(ورودی_مقدار.name, set()).update(پارامتر_آرگومان.arg for پارامتر_آرگومان in عملکرد_مقدار.args.args + عملکرد_مقدار.args.kwonlyargs)
            نام = ''
            if isinstance(ورودی_مقدار, (ast.FunctionDef, ast.ClassDef)): نام = ورودی_مقدار.name
            elif isinstance(ورودی_مقدار, ast.Name) and isinstance(ورودی_مقدار.ctx, ast.Store): نام = ورودی_مقدار.id
            elif isinstance(ورودی_مقدار, ast.arg): نام = ورودی_مقدار.arg
            if نام and نام not in شغل_مقدار and all(ord(نویسه_مقدار)<128 for نویسه_مقدار in نام):
                실패들.append('{}:{}: {}'.format(مسیر.relative_to(مخزن_جذر), ورودی_مقدار.lineno, نام))
    for مسیر, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            نام = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if نام not in پارامتر_جدول or نام in 가변매개함수 or not any(ord(نویسه_مقدار)>127 for نویسه_مقدار in نام): continue
            for پارامتر_آرگومان in 호출.keywords:
                if پارامتر_آرگومان.arg and پارامتر_آرگومان.arg not in پارامتر_جدول[نام]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(مسیر.relative_to(مخزن_جذر), 호출.lineno, نام, پارامتر_آرگومان.arg))
    for خط in (نمایش_دادن_جذر/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, فرآیند_مقدار_ورودی = خط.split('\t')
        if not (نمایش_دادن_جذر/현재).is_file(): 실패들.append('انتقال_مقدار پرونده 없음: '+현재)
        if فرآیند_مقدار_ورودی == '호환진입점유지' and not (نمایش_دادن_جذر/이전).is_file(): 실패들.append('호환 ورودی_نقطه 없음: '+이전)
    예제 = (نمایش_دادن_جذر.parents[1]/'example/java/نمونهشبکه.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for مسیر in sorted((نمایش_دادن_جذر.parents[1]/'example/java').glob('*.java')):
        مبداء = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', مسیر.read_text())
        for نام in re.findall(r'\b[^\W\d]\w*\b', مبداء, re.UNICODE):
            if نام not in 예약어 and all(ord(نویسه_مقدار)<128 for نویسه_مقدار in نام):
                실패들.append('{}: 예제의 영어 شناسه_مقدار {}'.format(مسیر.name, نام))
    for نام in ('창', 'دکمه', 'برچسب', 'متن_فیلد', '화면구성요소', 'رویداد_صف', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        مبداء = (نمایش_دادن_جذر/'한국어자바/فارسی/بومی'/(نام+'.java')).read_text()
        مبداء = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', مبداء)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', مبداء):
            실패들.append(نام+': فارسی 직접 구현에 표준 شئ_مقدار 래퍼가 남았습니다.')
    시언어예제 = (نمایش_دادن_جذر.parents[1]/'example/c/نمونهشبکه.c').read_text()
    for نام in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if نام in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 نام: '+نام)
    파이썬예제 = (نمایش_دادن_جذر.parents[1]/'example/python/نمونهشبکه.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 استثنا 직접 사용')
    머리 = (نمایش_دادن_جذر.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for نام in ('ابری_خانواده', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+نام+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 ماکرو_مقدار 사용: '+نام)
    자바파일수 = 0
    for جذر_مقدار in ('مبداء', 'کاربر/자바', '한국어자바'):
        for مسیر in (نمایش_دادن_جذر/جذر_مقدار).rglob('*.java'):
            자바파일수 += 1
            مبداء = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', مسیر.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', مبداء):
                실패들.append('{}: 한국어화되지 않은 اعلامیه {}'.format(مسیر.relative_to(نمایش_دادن_جذر), 맞음[1]))
            if جذر_مقدار == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', مبداء):
                실패들.append('{}: 공개 استثنا اعلامیه'.format(مسیر.relative_to(نمایش_دادن_جذر)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for مسیر in sorted((مخزن_جذر/'os/مبداء').glob('*.java')):
        x86자바파일수 += 1
        مبداء = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', مسیر.read_text())
        for نام in re.findall(r'\b[^\W\d]\w*\b', مبداء, re.UNICODE):
            if نام not in 예약어 | 표준자바이름 and all(ord(نویسه_مقدار)<128 for نویسه_مقدار in نام):
                실패들.append('{}: بومی 영어 شناسه_مقدار {}'.format(مسیر.relative_to(مخزن_جذر), نام))
    واقعه_نگار_ردیف = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if نشانوندها.시언어:
        subprocess.check_call(['python3', str(نمایش_دادن_جذر/'ابزارها/시언어이름분석.py')])
        분석 = json.loads((نمایش_دادن_جذر/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(خطا) for خطا in 분석['خطا'])
        공개규약 = set(json.loads((نمایش_دادن_جذر/'명명/규격이름.json').read_text()))
        for ورودی_مقدار in 분석['اعلامیه'].values():
            نام = ورودی_مقدار['نام']; مسیر = Path(ورودی_مقدار['پرونده'])
            مبداء = مسیر.read_bytes()
            # فارسی 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if مبداء[ورودی_مقدار['جابجایی_لایه_ای_مقدار']:ورودی_مقدار['جابجایی_لایه_ای_مقدار']+len(نام)] == نام.encode() and نام not in 공개규약:
                실패들.append('{}:{}: {}'.format(مسیر.relative_to(نمایش_دادن_جذر), ورودی_مقدار['خط'], نام))
        واقعه_نگار_ردیف['c_semantic_checked'] = True
        واقعه_نگار_ردیف['c_source_sha256'] = {str(Path(پرونده).relative_to(نمایش_دادن_جذر)):هاشور_فایل for پرونده,هاشور_فایل in 분석['원문해시'].items()}
    واقعه_نگار_ردیف['passed'] = not 실패들; واقعه_نگار_ردیف['failures'] = 실패들
    مقصد_مقدار = نمایش_دادن_جذر/'build/verification/naming'; مقصد_مقدار.mkdir(parents=True, exist_ok=True)
    (مقصد_مقدار/'report.json').write_text(json.dumps(واقعه_نگار_ردیف, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: فارسی اعلامیه·پرونده مسیر·호환 ورودی_نقطه·통신 예제')

if __name__ == '__main__': اجرا_2()
