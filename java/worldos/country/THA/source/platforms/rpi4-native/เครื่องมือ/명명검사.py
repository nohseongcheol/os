#!/usr/bin/env python3
"""명명 คลิป·ข้อยกเว้น·경로를 검사한다. --시언어는 libclang การประกาศ 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

แสดง_ราก = Path(__file__).resolve().parents[1]
ที่เก็บ_ราก = แสดง_ราก.parents[1]

def เรียกใช้งาน():
    ตัวแยกวิเคราะห์_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--시언어', action='store_true')
    อาร์กิวเมนต์ = ตัวแยกวิเคราะห์_48ee4b1b.parse_args()
    실패들 = []
    มูลค่าตามสัญญา = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    พารามิเตอร์_ตาราง = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [ที่เก็บ_ราก/'compiler/คอมไพเลอร์.py', ที่เก็บ_ราก/'compiler/기계어미리번역.py']
    for เส้นทาง in list((แสดง_ราก/'เครื่องมือ').glob('*.py')) + list((แสดง_ราก/'예제').rglob('*.py')) + 공용번역기들:
        if เส้นทาง.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(เส้นทาง.read_text()); 나무들[เส้นทาง] = 나무
        for รายการ_ค่า in ast.walk(나무):
            if isinstance(รายการ_ค่า, ast.FunctionDef):
                พารามิเตอร์_ตาราง.setdefault(รายการ_ค่า.name, set()).update(พารามิเตอร์_อาร์กิวเมนต์.arg for พารามิเตอร์_อาร์กิวเมนต์ in รายการ_ค่า.args.args + รายการ_ค่า.args.kwonlyargs)
                if รายการ_ค่า.args.kwarg: 가변매개함수.add(รายการ_ค่า.name)
            if isinstance(รายการ_ค่า, ast.ClassDef):
                for ฟังก์ชัน_ค่า in รายการ_ค่า.body:
                    if isinstance(ฟังก์ชัน_ค่า, ast.FunctionDef) and ฟังก์ชัน_ค่า.name == '__init__':
                        พารามิเตอร์_ตาราง.setdefault(รายการ_ค่า.name, set()).update(พารามิเตอร์_อาร์กิวเมนต์.arg for พารามิเตอร์_อาร์กิวเมนต์ in ฟังก์ชัน_ค่า.args.args + ฟังก์ชัน_ค่า.args.kwonlyargs)
            ชื่อ = ''
            if isinstance(รายการ_ค่า, (ast.FunctionDef, ast.ClassDef)): ชื่อ = รายการ_ค่า.name
            elif isinstance(รายการ_ค่า, ast.Name) and isinstance(รายการ_ค่า.ctx, ast.Store): ชื่อ = รายการ_ค่า.id
            elif isinstance(รายการ_ค่า, ast.arg): ชื่อ = รายการ_ค่า.arg
            if ชื่อ and ชื่อ not in มูลค่าตามสัญญา and all(ord(อักขระ_ค่า)<128 for อักขระ_ค่า in ชื่อ):
                실패들.append('{}:{}: {}'.format(เส้นทาง.relative_to(ที่เก็บ_ราก), รายการ_ค่า.lineno, ชื่อ))
    for เส้นทาง, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            ชื่อ = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if ชื่อ not in พารามิเตอร์_ตาราง or ชื่อ in 가변매개함수 or not any(ord(อักขระ_ค่า)>127 for อักขระ_ค่า in ชื่อ): continue
            for พารามิเตอร์_อาร์กิวเมนต์ in 호출.keywords:
                if พารามิเตอร์_อาร์กิวเมนต์.arg and พารามิเตอร์_อาร์กิวเมนต์.arg not in พารามิเตอร์_ตาราง[ชื่อ]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(เส้นทาง.relative_to(ที่เก็บ_ราก), 호출.lineno, ชื่อ, พารามิเตอร์_อาร์กิวเมนต์.arg))
    for บรรทัด in (แสดง_ราก/'명명/ชื่อแฟ้ม_การแมป.tsv').read_text().splitlines()[1:]:
        이전, ปัจจุบัน_รายการ, กระบวนการ_ค่า_รายการ = บรรทัด.split('\t')
        if not (แสดง_ราก/ปัจจุบัน_รายการ).is_file(): 실패들.append('ขยับ_ค่า แฟ้ม 없음: '+ปัจจุบัน_รายการ)
        if กระบวนการ_ค่า_รายการ == '호환진입점유지' and not (แสดง_ราก/이전).is_file(): 실패들.append('호환 จุดเข้าใช้งาน 없음: '+이전)
    예제 = (แสดง_ราก.parents[1]/'example/java/เครือข่าย.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for เส้นทาง in sorted((แสดง_ราก.parents[1]/'example/java').glob('*.java')):
        รหัสต้นฉบับ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', เส้นทาง.read_text())
        for ชื่อ in re.findall(r'\b[^\W\d]\w*\b', รหัสต้นฉบับ, re.UNICODE):
            if ชื่อ not in 예약어 and all(ord(อักขระ_ค่า)<128 for อักขระ_ค่า in ชื่อ):
                실패들.append('{}: 예제의 영어 ตัวระบุ_ค่า {}'.format(เส้นทาง.name, ชื่อ))
    for ชื่อ in ('หน้าต่าง', 'ปุ่ม', 'ฉลาก', 'เขตข้อมูลข้อความ', '화면구성요소', 'กิจกรรม_คิว', 'งานเบื้องหลัง', '실행할일', '동작받이', 'แอคชัน_ข้อสังเกต', '작업'):
        รหัสต้นฉบับ = (แสดง_ราก/'한국어자바/ไทย/เอง'/(ชื่อ+'.java')).read_text()
        รหัสต้นฉบับ = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', รหัสต้นฉบับ)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', รหัสต้นฉบับ):
            실패들.append(ชื่อ+': ไทย 직접 구현에 표준 วัตถุ_ค่า 래퍼가 남았습니다.')
    시언어예제 = (แสดง_ราก.parents[1]/'example/c/เครือข่าย.c').read_text()
    for ชื่อ in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if ชื่อ in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 ชื่อ: '+ชื่อ)
    파이썬예제 = (แสดง_ราก.parents[1]/'example/python/เครือข่าย.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 ข้อยกเว้น 직접 ใช้_ค่า')
    머리 = (แสดง_ราก.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for ชื่อ in ('คลาวด์_กลุ่ม', 'เดตาแกรมซ็อกเก็ต', 'เดตาแกรม_โพรโทคอล', '통신주소', '인터넷통신주소', 'เปิด_ปลายทาง', 'ส่ง_เดตาแกรม_ข้อมูล'):
        if re.search(r'^#define\s+'+ชื่อ+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 แมโคร_ค่า ใช้_ค่า: '+ชื่อ)
    자바파일수 = 0
    for ราก_ค่า in ('รหัสต้นฉบับ', 'ผู้ใช้/자바', '한국어자바'):
        for เส้นทาง in (แสดง_ราก/ราก_ค่า).rglob('*.java'):
            자바파일수 += 1
            รหัสต้นฉบับ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', เส้นทาง.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', รหัสต้นฉบับ):
                실패들.append('{}: 한국어화되지 않은 การประกาศ {}'.format(เส้นทาง.relative_to(แสดง_ราก), 맞음[1]))
            if ราก_ค่า == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', รหัสต้นฉบับ):
                실패들.append('{}: 공개 ข้อยกเว้น การประกาศ'.format(เส้นทาง.relative_to(แสดง_ราก)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for เส้นทาง in sorted((ที่เก็บ_ราก/'os/รหัสต้นฉบับ').glob('*.java')):
        x86자바파일수 += 1
        รหัสต้นฉบับ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', เส้นทาง.read_text())
        for ชื่อ in re.findall(r'\b[^\W\d]\w*\b', รหัสต้นฉบับ, re.UNICODE):
            if ชื่อ not in 예약어 | 표준자바이름 and all(ord(อักขระ_ค่า)<128 for อักขระ_ค่า in ชื่อ):
                실패들.append('{}: เอง 영어 ตัวระบุ_ค่า {}'.format(เส้นทาง.relative_to(ที่เก็บ_ราก), ชื่อ))
    บันทึก_สถิติ = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if อาร์กิวเมนต์.시언어:
        subprocess.check_call(['python3', str(แสดง_ราก/'เครื่องมือ/시언어이름분석.py')])
        วิเคราะห์_ค่า = json.loads((แสดง_ราก/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ข้อผิดพลาด) for ข้อผิดพลาด in วิเคราะห์_ค่า['ข้อผิดพลาด'])
        공개규약 = set(json.loads((แสดง_ราก/'명명/규격이름.json').read_text()))
        for รายการ_ค่า in วิเคราะห์_ค่า['การประกาศ'].values():
            ชื่อ = รายการ_ค่า['ชื่อ']; เส้นทาง = Path(รายการ_ค่า['แฟ้ม'])
            รหัสต้นฉบับ = เส้นทาง.read_bytes()
            # ไทย 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if รหัสต้นฉบับ[รายการ_ค่า['ออฟเซต_ค่า']:รายการ_ค่า['ออฟเซต_ค่า']+len(ชื่อ)] == ชื่อ.encode() and ชื่อ not in 공개규약:
                실패들.append('{}:{}: {}'.format(เส้นทาง.relative_to(แสดง_ราก), รายการ_ค่า['บรรทัด'], ชื่อ))
        บันทึก_สถิติ['c_semantic_checked'] = True
        บันทึก_สถิติ['c_source_sha256'] = {str(Path(แฟ้ม).relative_to(แสดง_ราก)):แฮช_แฟ้ม for แฟ้ม,แฮช_แฟ้ม in วิเคราะห์_ค่า['원문해시'].items()}
    บันทึก_สถิติ['passed'] = not 실패들; บันทึก_สถิติ['failures'] = 실패들
    ปลายทาง_ค่า_a0fbc067 = แสดง_ราก/'build/verification/naming'; ปลายทาง_ค่า_a0fbc067.mkdir(parents=True, exist_ok=True)
    (ปลายทาง_ค่า_a0fbc067/'report.json').write_text(json.dumps(บันทึก_สถิติ, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: ไทย การประกาศ·แฟ้ม เส้นทาง·호환 จุดเข้าใช้งาน·통신 예제')

if __name__ == '__main__': เรียกใช้งาน()
