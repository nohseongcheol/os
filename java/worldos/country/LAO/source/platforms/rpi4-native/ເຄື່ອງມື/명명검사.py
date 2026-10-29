#!/usr/bin/env python3
"""명명 ຄ_ລິບ·ຂໍ້ຍົກເວັ້ນ·경로를 검사한다. --시언어는 libclang ການປະກາດ 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parents[1]
ຣີໂພຊິທໍຣີ_ເລກຮາກ = ໂຄງ_ການ_ເລກຮາກ.parents[1]

def ແລ່ນ():
    ຕົວແຍກວິເຄາະ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--시언어', action='store_true')
    인수 = ຕົວແຍກວິເຄາະ_48ee4b1b.parse_args()
    실패들 = []
    ສັນຍາ_ຄ່າ = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    ພາຣາມິເຕີ_ຕາຕະລາງ = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [ຣີໂພຊິທໍຣີ_ເລກຮາກ/'compiler/컴파일러.py', ຣີໂພຊິທໍຣີ_ເລກຮາກ/'compiler/기계어미리번역.py']
    for ທາງໂຄຈອນ in list((ໂຄງ_ການ_ເລກຮາກ/'ເຄື່ອງມື').glob('*.py')) + list((ໂຄງ_ການ_ເລກຮາກ/'예제').rglob('*.py')) + 공용번역기들:
        if ທາງໂຄຈອນ.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(ທາງໂຄຈອນ.read_text()); 나무들[ທາງໂຄຈອນ] = 나무
        for ເຂົ້າໃນ_ຄ່າ in ast.walk(나무):
            if isinstance(ເຂົ້າໃນ_ຄ່າ, ast.FunctionDef):
                ພາຣາມິເຕີ_ຕາຕະລາງ.setdefault(ເຂົ້າໃນ_ຄ່າ.name, set()).update(ພາຣາມິເຕີ_ຂໍ້ພິສູດ.arg for ພາຣາມິເຕີ_ຂໍ້ພິສູດ in ເຂົ້າໃນ_ຄ່າ.args.args + ເຂົ້າໃນ_ຄ່າ.args.kwonlyargs)
                if ເຂົ້າໃນ_ຄ່າ.args.kwarg: 가변매개함수.add(ເຂົ້າໃນ_ຄ່າ.name)
            if isinstance(ເຂົ້າໃນ_ຄ່າ, ast.ClassDef):
                for ຟັງ_ຄ໌_ຊັນ_ຄ່າ in ເຂົ້າໃນ_ຄ່າ.body:
                    if isinstance(ຟັງ_ຄ໌_ຊັນ_ຄ່າ, ast.FunctionDef) and ຟັງ_ຄ໌_ຊັນ_ຄ່າ.name == '__init__':
                        ພາຣາມິເຕີ_ຕາຕະລາງ.setdefault(ເຂົ້າໃນ_ຄ່າ.name, set()).update(ພາຣາມິເຕີ_ຂໍ້ພິສູດ.arg for ພາຣາມິເຕີ_ຂໍ້ພິສູດ in ຟັງ_ຄ໌_ຊັນ_ຄ່າ.args.args + ຟັງ_ຄ໌_ຊັນ_ຄ່າ.args.kwonlyargs)
            ຊື່ = ''
            if isinstance(ເຂົ້າໃນ_ຄ່າ, (ast.FunctionDef, ast.ClassDef)): ຊື່ = ເຂົ້າໃນ_ຄ່າ.name
            elif isinstance(ເຂົ້າໃນ_ຄ່າ, ast.Name) and isinstance(ເຂົ້າໃນ_ຄ່າ.ctx, ast.Store): ຊື່ = ເຂົ້າໃນ_ຄ່າ.id
            elif isinstance(ເຂົ້າໃນ_ຄ່າ, ast.arg): ຊື່ = ເຂົ້າໃນ_ຄ່າ.arg
            if ຊື່ and ຊື່ not in ສັນຍາ_ຄ່າ and all(ord(ຕົວອັກສອນ_ຄ່າ)<128 for ຕົວອັກສອນ_ຄ່າ in ຊື່):
                실패들.append('{}:{}: {}'.format(ທາງໂຄຈອນ.relative_to(ຣີໂພຊິທໍຣີ_ເລກຮາກ), ເຂົ້າໃນ_ຄ່າ.lineno, ຊື່))
    for ທາງໂຄຈອນ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            ຊື່ = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if ຊື່ not in ພາຣາມິເຕີ_ຕາຕະລາງ or ຊື່ in 가변매개함수 or not any(ord(ຕົວອັກສອນ_ຄ່າ)>127 for ຕົວອັກສອນ_ຄ່າ in ຊື່): continue
            for ພາຣາມິເຕີ_ຂໍ້ພິສູດ in 호출.keywords:
                if ພາຣາມິເຕີ_ຂໍ້ພິສູດ.arg and ພາຣາມິເຕີ_ຂໍ້ພິສູດ.arg not in ພາຣາມິເຕີ_ຕາຕະລາງ[ຊື່]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(ທາງໂຄຈອນ.relative_to(ຣີໂພຊິທໍຣີ_ເລກຮາກ), 호출.lineno, ຊື່, ພາຣາມິເຕີ_ຂໍ້ພິສູດ.arg))
    for ສາຍ in (ໂຄງ_ການ_ເລກຮາກ/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, ຂະ_ບວນ_ການ_ຄ່າ_ເຂົ້າໃນ = ສາຍ.split('\t')
        if not (ໂຄງ_ການ_ເລກຮາກ/현재).is_file(): 실패들.append('이동 ຟາຍ 없음: '+현재)
        if ຂະ_ບວນ_ການ_ຄ່າ_ເຂົ້າໃນ == '호환진입점유지' and not (ໂຄງ_ການ_ເລກຮາກ/이전).is_file(): 실패들.append('호환 ເຂົ້າໃນ_ຈຸດ 없음: '+이전)
    예제 = (ໂຄງ_ການ_ເລກຮາກ.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ທາງໂຄຈອນ in sorted((ໂຄງ_ການ_ເລກຮາກ.parents[1]/'example/java').glob('*.java')):
        ແຫຼ່ງທີ່ມາ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ທາງໂຄຈອນ.read_text())
        for ຊື່ in re.findall(r'\b[^\W\d]\w*\b', ແຫຼ່ງທີ່ມາ, re.UNICODE):
            if ຊື່ not in 예약어 and all(ord(ຕົວອັກສອນ_ຄ່າ)<128 for ຕົວອັກສອນ_ຄ່າ in ຊື່):
                실패들.append('{}: 예제의 영어 ຕົວ_ກໍາ_ນົດ_ຄ່າ {}'.format(ທາງໂຄຈອນ.name, ຊື່))
    for ຊື່ in ('창', 'ປຸ່ມ', 'ປ້າຍ', 'ຂໍ້ຄວາມ_ຊ່ອງຂໍ້ມູນ', '화면구성요소', 'ງານ_ຄິວ', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        ແຫຼ່ງທີ່ມາ = (ໂຄງ_ການ_ເລກຮາກ/'한국어자바/한국어/자체'/(ຊື່+'.java')).read_text()
        ແຫຼ່ງທີ່ມາ = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ແຫຼ່ງທີ່ມາ)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ແຫຼ່ງທີ່ມາ):
            실패들.append(ຊື່+': 한국어 직접 구현에 표준 ວັດ_ຖຸ_ຄ່າ 래퍼가 남았습니다.')
    시언어예제 = (ໂຄງ_ການ_ເລກຮາກ.parents[1]/'example/c/네트워크예제.c').read_text()
    for ຊື່ in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if ຊື່ in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 ຊື່: '+ຊື່)
    파이썬예제 = (ໂຄງ_ການ_ເລກຮາກ.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 ຂໍ້ຍົກເວັ້ນ 직접 사용')
    머리 = (ໂຄງ_ການ_ເລກຮາກ.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for ຊື່ in ('ຄລາວ_ຄອບຄົວ', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+ຊື່+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 ມາກໂຄຣ_ຄ່າ 사용: '+ຊື່)
    자바파일수 = 0
    for ເລກຮາກ_ຄ່າ in ('ແຫຼ່ງທີ່ມາ', 'ຜູ້ໃຊ້/자바', '한국어자바'):
        for ທາງໂຄຈອນ in (ໂຄງ_ການ_ເລກຮາກ/ເລກຮາກ_ຄ່າ).rglob('*.java'):
            자바파일수 += 1
            ແຫຼ່ງທີ່ມາ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ທາງໂຄຈອນ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ແຫຼ່ງທີ່ມາ):
                실패들.append('{}: 한국어화되지 않은 ການປະກາດ {}'.format(ທາງໂຄຈອນ.relative_to(ໂຄງ_ການ_ເລກຮາກ), 맞음[1]))
            if ເລກຮາກ_ຄ່າ == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ແຫຼ່ງທີ່ມາ):
                실패들.append('{}: 공개 ຂໍ້ຍົກເວັ້ນ ການປະກາດ'.format(ທາງໂຄຈອນ.relative_to(ໂຄງ_ການ_ເລກຮາກ)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for ທາງໂຄຈອນ in sorted((ຣີໂພຊິທໍຣີ_ເລກຮາກ/'os/ແຫຼ່ງທີ່ມາ').glob('*.java')):
        x86자바파일수 += 1
        ແຫຼ່ງທີ່ມາ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ທາງໂຄຈອນ.read_text())
        for ຊື່ in re.findall(r'\b[^\W\d]\w*\b', ແຫຼ່ງທີ່ມາ, re.UNICODE):
            if ຊື່ not in 예약어 | 표준자바이름 and all(ord(ຕົວອັກສອນ_ຄ່າ)<128 for ຕົວອັກສອນ_ຄ່າ in ຊື່):
                실패들.append('{}: 자체 영어 ຕົວ_ກໍາ_ນົດ_ຄ່າ {}'.format(ທາງໂຄຈອນ.relative_to(ຣີໂພຊິທໍຣີ_ເລກຮາກ), ຊື່))
    ບັນທຶກ_ແຖວ = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(ໂຄງ_ການ_ເລກຮາກ/'ເຄື່ອງມື/시언어이름분석.py')])
        분석 = json.loads((ໂຄງ_ການ_ເລກຮາກ/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ຂໍ້ຜິດພາດ) for ຂໍ້ຜິດພາດ in 분석['ຂໍ້ຜິດພາດ'])
        공개규약 = set(json.loads((ໂຄງ_ການ_ເລກຮາກ/'명명/규격이름.json').read_text()))
        for ເຂົ້າໃນ_ຄ່າ in 분석['ການປະກາດ'].values():
            ຊື່ = ເຂົ້າໃນ_ຄ່າ['ຊື່']; ທາງໂຄຈອນ = Path(ເຂົ້າໃນ_ຄ່າ['ຟາຍ'])
            ແຫຼ່ງທີ່ມາ = ທາງໂຄຈອນ.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ແຫຼ່ງທີ່ມາ[ເຂົ້າໃນ_ຄ່າ['ອອບເຊັດ_ຄ່າ']:ເຂົ້າໃນ_ຄ່າ['ອອບເຊັດ_ຄ່າ']+len(ຊື່)] == ຊື່.encode() and ຊື່ not in 공개규약:
                실패들.append('{}:{}: {}'.format(ທາງໂຄຈອນ.relative_to(ໂຄງ_ການ_ເລກຮາກ), ເຂົ້າໃນ_ຄ່າ['줄'], ຊື່))
        ບັນທຶກ_ແຖວ['c_semantic_checked'] = True
        ບັນທຶກ_ແຖວ['c_source_sha256'] = {str(Path(ຟາຍ).relative_to(ໂຄງ_ການ_ເລກຮາກ)):ແຮຊ_ຟາຍ for ຟາຍ,ແຮຊ_ຟາຍ in 분석['원문해시'].items()}
    ບັນທຶກ_ແຖວ['passed'] = not 실패들; ບັນທຶກ_ແຖວ['failures'] = 실패들
    ປາຍທາງ_ຄ່າ = ໂຄງ_ການ_ເລກຮາກ/'build/verification/naming'; ປາຍທາງ_ຄ່າ.mkdir(parents=True, exist_ok=True)
    (ປາຍທາງ_ຄ່າ/'report.json').write_text(json.dumps(ບັນທຶກ_ແຖວ, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 ການປະກາດ·ຟາຍ ທາງໂຄຈອນ·호환 ເຂົ້າໃນ_ຈຸດ·통신 예제')

if __name__ == '__main__': ແລ່ນ()
