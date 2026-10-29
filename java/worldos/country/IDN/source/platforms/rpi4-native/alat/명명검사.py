#!/usr/bin/env python3
"""명명 klip·pengecualian·경로를 검사한다. --시언어는 libclang deklarasi_4f4f026b 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Tugas_akar = Path(__file__).resolve().parents[1]
repositori_akar = Tugas_akar.parents[1]

def jalankan():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--시언어', action='store_true')
    argumen = parser_48ee4b1b.parse_args()
    실패들 = []
    kasus_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    file_COUNT = 0
    parameter_tabel = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [repositori_akar/'compiler/컴파일러.py', repositori_akar/'compiler/기계어미리번역.py']
    for jalur in list((Tugas_akar/'alat').glob('*.py')) + list((Tugas_akar/'예제').rglob('*.py')) + 공용번역기들:
        if jalur.name.endswith(('이름반영.py', '이름분석.py')): continue
        file_COUNT += 1
        나무 = ast.parse(jalur.read_text()); 나무들[jalur] = 나무
        for entri_VALUE in ast.walk(나무):
            if isinstance(entri_VALUE, ast.FunctionDef):
                parameter_tabel.setdefault(entri_VALUE.name, set()).update(parameter_argumen.arg for parameter_argumen in entri_VALUE.args.args + entri_VALUE.args.kwonlyargs)
                if entri_VALUE.args.kwarg: 가변매개함수.add(entri_VALUE.name)
            if isinstance(entri_VALUE, ast.ClassDef):
                for fungsi_VALUE in entri_VALUE.body:
                    if isinstance(fungsi_VALUE, ast.FunctionDef) and fungsi_VALUE.name == '__init__':
                        parameter_tabel.setdefault(entri_VALUE.name, set()).update(parameter_argumen.arg for parameter_argumen in fungsi_VALUE.args.args + fungsi_VALUE.args.kwonlyargs)
            Nama_2 = ''
            if isinstance(entri_VALUE, (ast.FunctionDef, ast.ClassDef)): Nama_2 = entri_VALUE.name
            elif isinstance(entri_VALUE, ast.Name) and isinstance(entri_VALUE.ctx, ast.Store): Nama_2 = entri_VALUE.id
            elif isinstance(entri_VALUE, ast.arg): Nama_2 = entri_VALUE.arg
            if Nama_2 and Nama_2 not in kasus_VALUE and all(ord(karakter_VALUE)<128 for karakter_VALUE in Nama_2):
                실패들.append('{}:{}: {}'.format(jalur.relative_to(repositori_akar), entri_VALUE.lineno, Nama_2))
    for jalur, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Nama_2 = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Nama_2 not in parameter_tabel or Nama_2 in 가변매개함수 or not any(ord(karakter_VALUE)>127 for karakter_VALUE in Nama_2): continue
            for parameter_argumen in 호출.keywords:
                if parameter_argumen.arg and parameter_argumen.arg not in parameter_tabel[Nama_2]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(jalur.relative_to(repositori_akar), 호출.lineno, Nama_2, parameter_argumen.arg))
    for baris_masukan in (Tugas_akar/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, saat_ini_item, Proses_VALUE_entri = baris_masukan.split('\t')
        if not (Tugas_akar/saat_ini_item).is_file(): 실패들.append('gerak_VALUE berkas 없음: '+saat_ini_item)
        if Proses_VALUE_entri == '호환진입점유지' and not (Tugas_akar/이전).is_file(): 실패들.append('호환 entri_p 없음: '+이전)
    예제 = (Tugas_akar.parents[1]/'example/java/ContohJaringan.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for jalur in sorted((Tugas_akar.parents[1]/'example/java').glob('*.java')):
        kodeSumber = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', jalur.read_text())
        for Nama_2 in re.findall(r'\b[^\W\d]\w*\b', kodeSumber, re.UNICODE):
            if Nama_2 not in 예약어 and all(ord(karakter_VALUE)<128 for karakter_VALUE in Nama_2):
                실패들.append('{}: 예제의 영어 pengidentifikasi_VALUE {}'.format(jalur.name, Nama_2))
    for Nama_2 in ('Jendela', 'tombol', 'Nama', 'bidang_teks', '화면구성요소', 'acara_antrean', 'tugasLatar', '실행할일', '동작받이', '동작알림', '작업'):
        kodeSumber = (Tugas_akar/'한국어자바/Indonesia/Asli'/(Nama_2+'.java')).read_text()
        kodeSumber = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', kodeSumber)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', kodeSumber):
            실패들.append(Nama_2+': Indonesia 직접 구현에 표준 objek_VALUE 래퍼가 남았습니다.')
    시언어예제 = (Tugas_akar.parents[1]/'example/c/ContohJaringan.c').read_text()
    for Nama_2 in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Nama_2 in 시언어예제: 실패들.append('C komunikasi 예제에 남은 표준 Nama_2: '+Nama_2)
    파이썬예제 = (Tugas_akar.parents[1]/'example/python/ContohJaringan.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python komunikasi 예제에 남은 표준 pengecualian 직접 gunakan_VALUE')
    kepala_VALUE = (Tugas_akar.parents[1]/'posix-kor/arm64-native/deklarasi/통신규약.h').read_text()
    for Nama_2 in ('cloud_famili', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', 'Buat_peserta', '자료전문보내기'):
        if re.search(r'^#define\s+'+Nama_2+r'\b', kepala_VALUE, re.M): 실패들.append('C 직접 implementasi 대신 makro_VALUE gunakan_VALUE: '+Nama_2)
    자바파일수 = 0
    for akar_VALUE in ('kodeSumber', 'ruang_pengguna/자바', '한국어자바'):
        for jalur in (Tugas_akar/akar_VALUE).rglob('*.java'):
            자바파일수 += 1
            kodeSumber = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', jalur.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', kodeSumber):
                실패들.append('{}: 한국어화되지 않은 deklarasi_4f4f026b {}'.format(jalur.relative_to(Tugas_akar), 맞음[1]))
            if akar_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', kodeSumber):
                실패들.append('{}: 공개 pengecualian deklarasi_4f4f026b'.format(jalur.relative_to(Tugas_akar)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for jalur in sorted((repositori_akar/'os/kodeSumber').glob('*.java')):
        x86자바파일수 += 1
        kodeSumber = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', jalur.read_text())
        for Nama_2 in re.findall(r'\b[^\W\d]\w*\b', kodeSumber, re.UNICODE):
            if Nama_2 not in 예약어 | 표준자바이름 and all(ord(karakter_VALUE)<128 for karakter_VALUE in Nama_2):
                실패들.append('{}: Asli 영어 pengidentifikasi_VALUE {}'.format(jalur.relative_to(repositori_akar), Nama_2))
    LOG_baris = {'passed': False, 'python_files': file_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if argumen.시언어:
        subprocess.check_call(['python3', str(Tugas_akar/'alat/시언어이름분석.py')])
        Analisis_VALUE = json.loads((Tugas_akar/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(galat) for galat in Analisis_VALUE['galat'])
        공개규약 = set(json.loads((Tugas_akar/'명명/규격이름.json').read_text()))
        for entri_VALUE in Analisis_VALUE['deklarasi_4f4f026b'].values():
            Nama_2 = entri_VALUE['Nama_2']; jalur = Path(entri_VALUE['berkas'])
            kodeSumber = jalur.read_bytes()
            # Indonesia 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if kodeSumber[entri_VALUE['OFFSET_VALUE']:entri_VALUE['OFFSET_VALUE']+len(Nama_2)] == Nama_2.encode() and Nama_2 not in 공개규약:
                실패들.append('{}:{}: {}'.format(jalur.relative_to(Tugas_akar), entri_VALUE['baris_masukan'], Nama_2))
        LOG_baris['c_semantic_checked'] = True
        LOG_baris['c_source_sha256'] = {str(Path(berkas).relative_to(Tugas_akar)):hash_file for berkas,hash_file in Analisis_VALUE['원문해시'].items()}
    LOG_baris['passed'] = not 실패들; LOG_baris['failures'] = 실패들
    tujuan_VALUE = Tugas_akar/'build/verification/naming'; tujuan_VALUE.mkdir(parents=True, exist_ok=True)
    (tujuan_VALUE/'report.json').write_text(json.dumps(LOG_baris, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Indonesia deklarasi_4f4f026b·berkas jalur·호환 entri_p·komunikasi 예제')

if __name__ == '__main__': jalankan()
