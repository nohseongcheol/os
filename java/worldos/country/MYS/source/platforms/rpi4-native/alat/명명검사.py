#!/usr/bin/env python3
"""명명 klip·pengecualian·경로를 검사한다. --시언어는 libclang pengisytiharan_4f4f026b 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

projek_akar = Path(__file__).resolve().parents[1]
repositori_akar = projek_akar.parents[1]

def Jalan():
    penghurai_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    penghurai_48ee4b1b.add_argument('--C_Bahasa', action='store_true')
    인수 = penghurai_48ee4b1b.parse_args()
    실패들 = []
    kes_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    fail_COUNT = 0
    parameter_jadual = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [repositori_akar/'compiler/컴파일러.py', repositori_akar/'compiler/기계어미리번역.py']
    for LALUAN in list((projek_akar/'alat').glob('*.py')) + list((projek_akar/'예제').rglob('*.py')) + 공용번역기들:
        if LALUAN.name.endswith(('이름반영.py', '이름분석.py')): continue
        fail_COUNT += 1
        나무 = ast.parse(LALUAN.read_text()); 나무들[LALUAN] = 나무
        for pemasukan_VALUE in ast.walk(나무):
            if isinstance(pemasukan_VALUE, ast.FunctionDef):
                parameter_jadual.setdefault(pemasukan_VALUE.name, set()).update(parameter_argumen.arg for parameter_argumen in pemasukan_VALUE.args.args + pemasukan_VALUE.args.kwonlyargs)
                if pemasukan_VALUE.args.kwarg: 가변매개함수.add(pemasukan_VALUE.name)
            if isinstance(pemasukan_VALUE, ast.ClassDef):
                for fungsi_VALUE in pemasukan_VALUE.body:
                    if isinstance(fungsi_VALUE, ast.FunctionDef) and fungsi_VALUE.name == '__init__':
                        parameter_jadual.setdefault(pemasukan_VALUE.name, set()).update(parameter_argumen.arg for parameter_argumen in fungsi_VALUE.args.args + fungsi_VALUE.args.kwonlyargs)
            Nama = ''
            if isinstance(pemasukan_VALUE, (ast.FunctionDef, ast.ClassDef)): Nama = pemasukan_VALUE.name
            elif isinstance(pemasukan_VALUE, ast.Name) and isinstance(pemasukan_VALUE.ctx, ast.Store): Nama = pemasukan_VALUE.id
            elif isinstance(pemasukan_VALUE, ast.arg): Nama = pemasukan_VALUE.arg
            if Nama and Nama not in kes_VALUE and all(ord(aksara_VALUE)<128 for aksara_VALUE in Nama):
                실패들.append('{}:{}: {}'.format(LALUAN.relative_to(repositori_akar), pemasukan_VALUE.lineno, Nama))
    for LALUAN, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Nama = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Nama not in parameter_jadual or Nama in 가변매개함수 or not any(ord(aksara_VALUE)>127 for aksara_VALUE in Nama): continue
            for parameter_argumen in 호출.keywords:
                if parameter_argumen.arg and parameter_argumen.arg not in parameter_jadual[Nama]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(LALUAN.relative_to(repositori_akar), 호출.lineno, Nama, parameter_argumen.arg))
    for baris in (projek_akar/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Proses_VALUE_pemasukan = baris.split('\t')
        if not (projek_akar/현재).is_file(): 실패들.append('alih_VALUE Fail 없음: '+현재)
        if Proses_VALUE_pemasukan == '호환진입점유지' and not (projek_akar/이전).is_file(): 실패들.append('호환 titik_permulaan 없음: '+이전)
    예제 = (projek_akar.parents[1]/'example/java/ContohRangkaian.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for LALUAN in sorted((projek_akar.parents[1]/'example/java').glob('*.java')):
        SUMBER = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', LALUAN.read_text())
        for Nama in re.findall(r'\b[^\W\d]\w*\b', SUMBER, re.UNICODE):
            if Nama not in 예약어 and all(ord(aksara_VALUE)<128 for aksara_VALUE in Nama):
                실패들.append('{}: 예제의 영어 식별자 {}'.format(LALUAN.name, Nama))
    for Nama in ('Tetingkap', 'Butang', 'label', 'medan_teks', '화면구성요소', 'acara_baris', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        SUMBER = (projek_akar/'한국어자바/Melayu/Asli'/(Nama+'.java')).read_text()
        SUMBER = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', SUMBER)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', SUMBER):
            실패들.append(Nama+': Melayu 직접 구현에 표준 objek_VALUE 래퍼가 남았습니다.')
    시언어예제 = (projek_akar.parents[1]/'example/c/ContohRangkaian.c').read_text()
    for Nama in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Nama in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Nama: '+Nama)
    파이썬예제 = (projek_akar.parents[1]/'example/python/ContohRangkaian.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 pengecualian 직접 사용')
    머리 = (projek_akar.parents[1]/'posix-kor/arm64-native/pengisytiharan/통신규약.h').read_text()
    for Nama in ('awan_Keluarga', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', 'cipta_peserta', '자료전문보내기'):
        if re.search(r'^#define\s+'+Nama+r'\b', 머리, re.M): 실패들.append('C 직접 pelaksanaan 대신 makro_VALUE 사용: '+Nama)
    자바파일수 = 0
    for akar_VALUE in ('SUMBER', 'ruang_pengguna/자바', '한국어자바'):
        for LALUAN in (projek_akar/akar_VALUE).rglob('*.java'):
            자바파일수 += 1
            SUMBER = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', LALUAN.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', SUMBER):
                실패들.append('{}: 한국어화되지 않은 pengisytiharan_4f4f026b {}'.format(LALUAN.relative_to(projek_akar), 맞음[1]))
            if akar_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', SUMBER):
                실패들.append('{}: 공개 pengecualian pengisytiharan_4f4f026b'.format(LALUAN.relative_to(projek_akar)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for LALUAN in sorted((repositori_akar/'os/SUMBER').glob('*.java')):
        x86자바파일수 += 1
        SUMBER = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', LALUAN.read_text())
        for Nama in re.findall(r'\b[^\W\d]\w*\b', SUMBER, re.UNICODE):
            if Nama not in 예약어 | 표준자바이름 and all(ord(aksara_VALUE)<128 for aksara_VALUE in Nama):
                실패들.append('{}: Asli 영어 식별자 {}'.format(LALUAN.relative_to(repositori_akar), Nama))
    LOG_baris = {'passed': False, 'python_files': fail_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.C_Bahasa:
        subprocess.check_call(['python3', str(projek_akar/'alat/시언어이름분석.py')])
        Analisis_VALUE = json.loads((projek_akar/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(RALAT) for RALAT in Analisis_VALUE['RALAT'])
        공개규약 = set(json.loads((projek_akar/'명명/규격이름.json').read_text()))
        for pemasukan_VALUE in Analisis_VALUE['pengisytiharan_4f4f026b'].values():
            Nama = pemasukan_VALUE['Nama']; LALUAN = Path(pemasukan_VALUE['Fail'])
            SUMBER = LALUAN.read_bytes()
            # Melayu 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if SUMBER[pemasukan_VALUE['Ofset_VALUE']:pemasukan_VALUE['Ofset_VALUE']+len(Nama)] == Nama.encode() and Nama not in 공개규약:
                실패들.append('{}:{}: {}'.format(LALUAN.relative_to(projek_akar), pemasukan_VALUE['줄'], Nama))
        LOG_baris['c_semantic_checked'] = True
        LOG_baris['c_source_sha256'] = {str(Path(Fail).relative_to(projek_akar)):cincangan_fail for Fail,cincangan_fail in Analisis_VALUE['원문해시'].items()}
    LOG_baris['passed'] = not 실패들; LOG_baris['failures'] = 실패들
    destinasi_VALUE = projek_akar/'build/verification/naming'; destinasi_VALUE.mkdir(parents=True, exist_ok=True)
    (destinasi_VALUE/'report.json').write_text(json.dumps(LOG_baris, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Melayu pengisytiharan_4f4f026b·Fail LALUAN·호환 titik_permulaan·통신 예제')

if __name__ == '__main__': Jalan()
