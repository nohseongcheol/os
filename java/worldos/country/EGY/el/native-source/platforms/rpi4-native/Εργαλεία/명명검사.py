#!/usr/bin/env python3
"""명명 απόσπασμα·εξαίρεση·경로를 검사한다. --시언어는 libclang δήλωση 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

έργο_ρίζα = Path(__file__).resolve().parents[1]
αποθετήριο_ρίζα = έργο_ρίζα.parents[1]

def Εκτέλεση_2():
    ανάλυση_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ανάλυση_48ee4b1b.add_argument('--Ταχυδρομικός_κώδικας_Γλώσσα', action='store_true')
    Παράμετροι = ανάλυση_48ee4b1b.parse_args()
    실패들 = []
    εργασία_τιμή = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    παράμετρος_πίνακας = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [αποθετήριο_ρίζα/'compiler/πρόγραμμα_μεταγλώττισης.py', αποθετήριο_ρίζα/'compiler/기계어미리번역.py']
    for ΔΙΑΔΡΟΜΗ in list((έργο_ρίζα/'Εργαλεία').glob('*.py')) + list((έργο_ρίζα/'예제').rglob('*.py')) + 공용번역기들:
        if ΔΙΑΔΡΟΜΗ.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(ΔΙΑΔΡΟΜΗ.read_text()); 나무들[ΔΙΑΔΡΟΜΗ] = 나무
        for καταχώρηση_τιμή in ast.walk(나무):
            if isinstance(καταχώρηση_τιμή, ast.FunctionDef):
                παράμετρος_πίνακας.setdefault(καταχώρηση_τιμή.name, set()).update(παράμετρος_όρισμα.arg for παράμετρος_όρισμα in καταχώρηση_τιμή.args.args + καταχώρηση_τιμή.args.kwonlyargs)
                if καταχώρηση_τιμή.args.kwarg: 가변매개함수.add(καταχώρηση_τιμή.name)
            if isinstance(καταχώρηση_τιμή, ast.ClassDef):
                for συνάρτηση_τιμή in καταχώρηση_τιμή.body:
                    if isinstance(συνάρτηση_τιμή, ast.FunctionDef) and συνάρτηση_τιμή.name == '__init__':
                        παράμετρος_πίνακας.setdefault(καταχώρηση_τιμή.name, set()).update(παράμετρος_όρισμα.arg for παράμετρος_όρισμα in συνάρτηση_τιμή.args.args + συνάρτηση_τιμή.args.kwonlyargs)
            Όνομα = ''
            if isinstance(καταχώρηση_τιμή, (ast.FunctionDef, ast.ClassDef)): Όνομα = καταχώρηση_τιμή.name
            elif isinstance(καταχώρηση_τιμή, ast.Name) and isinstance(καταχώρηση_τιμή.ctx, ast.Store): Όνομα = καταχώρηση_τιμή.id
            elif isinstance(καταχώρηση_τιμή, ast.arg): Όνομα = καταχώρηση_τιμή.arg
            if Όνομα and Όνομα not in εργασία_τιμή and all(ord(χαρακτήρας_τιμή)<128 for χαρακτήρας_τιμή in Όνομα):
                실패들.append('{}:{}: {}'.format(ΔΙΑΔΡΟΜΗ.relative_to(αποθετήριο_ρίζα), καταχώρηση_τιμή.lineno, Όνομα))
    for ΔΙΑΔΡΟΜΗ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Όνομα = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Όνομα not in παράμετρος_πίνακας or Όνομα in 가변매개함수 or not any(ord(χαρακτήρας_τιμή)>127 for χαρακτήρας_τιμή in Όνομα): continue
            for παράμετρος_όρισμα in 호출.keywords:
                if παράμετρος_όρισμα.arg and παράμετρος_όρισμα.arg not in παράμετρος_πίνακας[Όνομα]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(ΔΙΑΔΡΟΜΗ.relative_to(αποθετήριο_ρίζα), 호출.lineno, Όνομα, παράμετρος_όρισμα.arg))
    for Γραμμή in (έργο_ρίζα/'명명/όνομα_αρχείου_αντιστοίχιση.tsv').read_text().splitlines()[1:]:
        이전, τρέχων_στοιχείο, διεργασία_τιμή_καταχώρηση = Γραμμή.split('\t')
        if not (έργο_ρίζα/τρέχων_στοιχείο).is_file(): 실패들.append('μετακινώ_τιμή_83b651b8 Αρχείο 없음: '+τρέχων_στοιχείο)
        if διεργασία_τιμή_καταχώρηση == '호환진입점유지' and not (έργο_ρίζα/이전).is_file(): 실패들.append('호환 σημείο_εισόδου 없음: '+이전)
    예제 = (έργο_ρίζα.parents[1]/'example/java/ΠαράδειγμαΔικτύου.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ΔΙΑΔΡΟΜΗ in sorted((έργο_ρίζα.parents[1]/'example/java').glob('*.java')):
        ΠΗΓΗ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ΔΙΑΔΡΟΜΗ.read_text())
        for Όνομα in re.findall(r'\b[^\W\d]\w*\b', ΠΗΓΗ, re.UNICODE):
            if Όνομα not in 예약어 and all(ord(χαρακτήρας_τιμή)<128 for χαρακτήρας_τιμή in Όνομα):
                실패들.append('{}: 예제의 영어 αναγνωριστικό_τιμή {}'.format(ΔΙΑΔΡΟΜΗ.name, Όνομα))
    for Όνομα in ('Παράθυρο', 'κουμπί', 'Ετικέτα', 'πεδίο_κειμένου', '화면구성요소', 'συμβάν_ουρά', '작업가닥', '실행할일', '동작받이', 'έργο_γνωστοποίηση', '작업'):
        ΠΗΓΗ = (έργο_ρίζα/'한국어자바/ελληνικά/ίδιο'/(Όνομα+'.java')).read_text()
        ΠΗΓΗ = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ΠΗΓΗ)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ΠΗΓΗ):
            실패들.append(Όνομα+': ελληνικά 직접 구현에 표준 αντικείμενο_τιμή 래퍼가 남았습니다.')
    시언어예제 = (έργο_ρίζα.parents[1]/'example/c/ΠαράδειγμαΔικτύου.c').read_text()
    for Όνομα in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Όνομα in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Όνομα: '+Όνομα)
    파이썬예제 = (έργο_ρίζα.parents[1]/'example/python/ΠαράδειγμαΔικτύου.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 εξαίρεση 직접 χρήση_τιμή')
    머리 = (έργο_ρίζα.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Όνομα in ('πλέγμα_παιδικά', 'υποδοχή_αυτοδύναμου_πακέτου', 'αυτοδύναμο_πακέτο_πρωτόκολλο', 'υποδοχή_διεύθυνση', 'πλέγμα_υποδοχή_διεύθυνση', 'ανοίγω_τελικό_σημείο', 'στέλνω_αυτοδύναμο_πακέτο_δεδομένα'):
        if re.search(r'^#define\s+'+Όνομα+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 μακροεντολή_τιμή χρήση_τιμή: '+Όνομα)
    자바파일수 = 0
    for ρίζα_τιμή in ('ΠΗΓΗ', 'χρήστης/자바', '한국어자바'):
        for ΔΙΑΔΡΟΜΗ in (έργο_ρίζα/ρίζα_τιμή).rglob('*.java'):
            자바파일수 += 1
            ΠΗΓΗ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ΔΙΑΔΡΟΜΗ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ΠΗΓΗ):
                실패들.append('{}: 한국어화되지 않은 δήλωση {}'.format(ΔΙΑΔΡΟΜΗ.relative_to(έργο_ρίζα), 맞음[1]))
            if ρίζα_τιμή == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ΠΗΓΗ):
                실패들.append('{}: 공개 εξαίρεση δήλωση'.format(ΔΙΑΔΡΟΜΗ.relative_to(έργο_ρίζα)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for ΔΙΑΔΡΟΜΗ in sorted((αποθετήριο_ρίζα/'os/ΠΗΓΗ').glob('*.java')):
        x86자바파일수 += 1
        ΠΗΓΗ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ΔΙΑΔΡΟΜΗ.read_text())
        for Όνομα in re.findall(r'\b[^\W\d]\w*\b', ΠΗΓΗ, re.UNICODE):
            if Όνομα not in 예약어 | 표준자바이름 and all(ord(χαρακτήρας_τιμή)<128 for χαρακτήρας_τιμή in Όνομα):
                실패들.append('{}: ίδιο 영어 αναγνωριστικό_τιμή {}'.format(ΔΙΑΔΡΟΜΗ.relative_to(αποθετήριο_ρίζα), Όνομα))
    καταγράφω_ρεκόρ = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Παράμετροι.Ταχυδρομικός_κώδικας_Γλώσσα:
        subprocess.check_call(['python3', str(έργο_ρίζα/'Εργαλεία/시언어이름분석.py')])
        Ανάλυσε_τιμή = json.loads((έργο_ρίζα/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ΣΦΑΛΜΑ) for ΣΦΑΛΜΑ in Ανάλυσε_τιμή['ΣΦΑΛΜΑ'])
        공개규약 = set(json.loads((έργο_ρίζα/'명명/규격이름.json').read_text()))
        for καταχώρηση_τιμή in Ανάλυσε_τιμή['δήλωση'].values():
            Όνομα = καταχώρηση_τιμή['Όνομα']; ΔΙΑΔΡΟΜΗ = Path(καταχώρηση_τιμή['Αρχείο'])
            ΠΗΓΗ = ΔΙΑΔΡΟΜΗ.read_bytes()
            # ελληνικά 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ΠΗΓΗ[καταχώρηση_τιμή['Υπέρθεση_τιμή']:καταχώρηση_τιμή['Υπέρθεση_τιμή']+len(Όνομα)] == Όνομα.encode() and Όνομα not in 공개규약:
                실패들.append('{}:{}: {}'.format(ΔΙΑΔΡΟΜΗ.relative_to(έργο_ρίζα), καταχώρηση_τιμή['Γραμμή'], Όνομα))
        καταγράφω_ρεκόρ['c_semantic_checked'] = True
        καταγράφω_ρεκόρ['c_source_sha256'] = {str(Path(Αρχείο).relative_to(έργο_ρίζα)):κατακερματισμός_Αρχείο for Αρχείο,κατακερματισμός_Αρχείο in Ανάλυσε_τιμή['원문해시'].items()}
    καταγράφω_ρεκόρ['passed'] = not 실패들; καταγράφω_ρεκόρ['failures'] = 실패들
    προορισμός_τιμή = έργο_ρίζα/'build/verification/naming'; προορισμός_τιμή.mkdir(parents=True, exist_ok=True)
    (προορισμός_τιμή/'report.json').write_text(json.dumps(καταγράφω_ρεκόρ, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: ελληνικά δήλωση·Αρχείο ΔΙΑΔΡΟΜΗ·호환 σημείο_εισόδου·통신 예제')

if __name__ == '__main__': Εκτέλεση_2()
