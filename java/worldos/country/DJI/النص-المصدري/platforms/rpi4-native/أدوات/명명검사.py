#!/usr/bin/env python3
"""명명 يقص·استثناء·경로를 검사한다. --시언어는 libclang إعلان 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

يعرض_جذر = Path(__file__).resolve().parents[1]
مستودع_جذر = يعرض_جذر.parents[1]

def تشغيل():
    المحلل_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    المحلل_48ee4b1b.add_argument('--الرمز_البريدي_لغة', action='store_true')
    وسائط = المحلل_48ee4b1b.parse_args()
    실패들 = []
    قيمة_العقد = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    معلمة_جدول = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [مستودع_جذر/'compiler/محول_برمجي.py', مستودع_جذر/'compiler/مترجممسبق.py']
    for مسار in list((يعرض_جذر/'أدوات').glob('*.py')) + list((يعرض_جذر/'예제').rglob('*.py')) + 공용번역기들:
        if مسار.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(مسار.read_text()); 나무들[مسار] = 나무
        for إدخال_قيمة_962f286b in ast.walk(나무):
            if isinstance(إدخال_قيمة_962f286b, ast.FunctionDef):
                معلمة_جدول.setdefault(إدخال_قيمة_962f286b.name, set()).update(معلمة_وسيطة.arg for معلمة_وسيطة in إدخال_قيمة_962f286b.args.args + إدخال_قيمة_962f286b.args.kwonlyargs)
                if إدخال_قيمة_962f286b.args.kwarg: 가변매개함수.add(إدخال_قيمة_962f286b.name)
            if isinstance(إدخال_قيمة_962f286b, ast.ClassDef):
                for دالة_قيمة in إدخال_قيمة_962f286b.body:
                    if isinstance(دالة_قيمة, ast.FunctionDef) and دالة_قيمة.name == '__init__':
                        معلمة_جدول.setdefault(إدخال_قيمة_962f286b.name, set()).update(معلمة_وسيطة.arg for معلمة_وسيطة in دالة_قيمة.args.args + دالة_قيمة.args.kwonlyargs)
            اسم = ''
            if isinstance(إدخال_قيمة_962f286b, (ast.FunctionDef, ast.ClassDef)): اسم = إدخال_قيمة_962f286b.name
            elif isinstance(إدخال_قيمة_962f286b, ast.Name) and isinstance(إدخال_قيمة_962f286b.ctx, ast.Store): اسم = إدخال_قيمة_962f286b.id
            elif isinstance(إدخال_قيمة_962f286b, ast.arg): اسم = إدخال_قيمة_962f286b.arg
            if اسم and اسم not in قيمة_العقد and all(ord(حرف_قيمة)<128 for حرف_قيمة in اسم):
                실패들.append('{}:{}: {}'.format(مسار.relative_to(مستودع_جذر), إدخال_قيمة_962f286b.lineno, اسم))
    for مسار, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            اسم = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if اسم not in معلمة_جدول or اسم in 가변매개함수 or not any(ord(حرف_قيمة)>127 for حرف_قيمة in اسم): continue
            for معلمة_وسيطة in 호출.keywords:
                if معلمة_وسيطة.arg and معلمة_وسيطة.arg not in معلمة_جدول[اسم]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(مسار.relative_to(مستودع_جذر), 호출.lineno, اسم, معلمة_وسيطة.arg))
    for سطر in (يعرض_جذر/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, حديث_عنصر, عملية_قيمة_إدخال = سطر.split('\t')
        if not (يعرض_جذر/حديث_عنصر).is_file(): 실패들.append('نقل_قيمة ملف 없음: '+حديث_عنصر)
        if عملية_قيمة_إدخال == '호환진입점유지' and not (يعرض_جذر/이전).is_file(): 실패들.append('호환 نقطة_الإدخال 없음: '+이전)
    예제 = (يعرض_جذر.parents[1]/'example/java/مثالشبكة.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for مسار in sorted((يعرض_جذر.parents[1]/'example/java').glob('*.java')):
        مصدر = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', مسار.read_text())
        for اسم in re.findall(r'\b[^\W\d]\w*\b', مصدر, re.UNICODE):
            if اسم not in 예약어 and all(ord(حرف_قيمة)<128 for حرف_قيمة in اسم):
                실패들.append('{}: 예제의 영어 معرف_قيمة {}'.format(مسار.name, اسم))
    for اسم in ('نافذة', 'زر', 'تسمية', 'حقل_نصي', '화면구성요소', 'حدث_يدرج', 'خيطالعمل', '실행할일', '동작받이', 'إجراء_إشعار', '작업'):
        مصدر = (يعرض_جذر/'한국어자바/العربية/ذاتي'/(اسم+'.java')).read_text()
        مصدر = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', مصدر)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', مصدر):
            실패들.append(اسم+': العربية 직접 구현에 표준 عنصر_قيمة_2ed200e9 래퍼가 남았습니다.')
    시언어예제 = (يعرض_جذر.parents[1]/'example/c/مثالشبكة.c').read_text()
    for اسم in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if اسم in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 اسم: '+اسم)
    파이썬예제 = (يعرض_جذر.parents[1]/'example/python/مثالشبكة.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 استثناء 직접 يستخدم_قيمة')
    رأس_قيمة = (يعرض_جذر.parents[1]/'posix-kor/arm64-native/تصريحات/통신규약.h').read_text()
    for اسم in ('سحابة_عائلة', 'مأخذ_مخطط_البيانات', 'مخطط_بيانات_بروتوكول', 'مأخذ_التوصيل_عنوان', 'سحابة_مأخذ_التوصيل_عنوان', 'فتح_المشارك', 'يرسل_مخطط_بيانات_بيانات'):
        if re.search(r'^#define\s+'+اسم+r'\b', رأس_قيمة, re.M): 실패들.append('C 직접 구현 대신 ماكرو_قيمة يستخدم_قيمة: '+اسم)
    자바파일수 = 0
    for جذر_قيمة in ('مصدر', 'فضاء_المستخدم/자바', '한국어자바'):
        for مسار in (يعرض_جذر/جذر_قيمة).rglob('*.java'):
            자바파일수 += 1
            مصدر = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', مسار.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', مصدر):
                실패들.append('{}: 한국어화되지 않은 إعلان {}'.format(مسار.relative_to(يعرض_جذر), 맞음[1]))
            if جذر_قيمة == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', مصدر):
                실패들.append('{}: 공개 استثناء إعلان'.format(مسار.relative_to(يعرض_جذر)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for مسار in sorted((مستودع_جذر/'os/مصدر').glob('*.java')):
        x86자바파일수 += 1
        مصدر = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', مسار.read_text())
        for اسم in re.findall(r'\b[^\W\d]\w*\b', مصدر, re.UNICODE):
            if اسم not in 예약어 | 표준자바이름 and all(ord(حرف_قيمة)<128 for حرف_قيمة in اسم):
                실패들.append('{}: ذاتي 영어 معرف_قيمة {}'.format(مسار.relative_to(مستودع_جذر), اسم))
    سجل_سجل = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if وسائط.الرمز_البريدي_لغة:
        subprocess.check_call(['python3', str(يعرض_جذر/'أدوات/시언어이름분석.py')])
        تحليل_قيمة = json.loads((يعرض_جذر/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(خطأ) for خطأ in تحليل_قيمة['خطأ'])
        공개규약 = set(json.loads((يعرض_جذر/'명명/규격이름.json').read_text()))
        for إدخال_قيمة_962f286b in تحليل_قيمة['إعلان'].values():
            اسم = إدخال_قيمة_962f286b['اسم']; مسار = Path(إدخال_قيمة_962f286b['ملف'])
            مصدر = مسار.read_bytes()
            # العربية 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if مصدر[إدخال_قيمة_962f286b['إزاحة_قيمة']:إدخال_قيمة_962f286b['إزاحة_قيمة']+len(اسم)] == اسم.encode() and اسم not in 공개규약:
                실패들.append('{}:{}: {}'.format(مسار.relative_to(يعرض_جذر), إدخال_قيمة_962f286b['سطر'], اسم))
        سجل_سجل['c_semantic_checked'] = True
        سجل_سجل['c_source_sha256'] = {str(Path(ملف).relative_to(يعرض_جذر)):تجزئة_ملف for ملف,تجزئة_ملف in تحليل_قيمة['원문해시'].items()}
    سجل_سجل['passed'] = not 실패들; سجل_سجل['failures'] = 실패들
    وجهة_قيمة = يعرض_جذر/'build/verification/naming'; وجهة_قيمة.mkdir(parents=True, exist_ok=True)
    (وجهة_قيمة/'report.json').write_text(json.dumps(سجل_سجل, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: العربية إعلان·ملف مسار·호환 نقطة_الإدخال·통신 예제')

if __name__ == '__main__': تشغيل()
