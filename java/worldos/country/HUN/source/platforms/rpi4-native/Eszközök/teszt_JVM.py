#!/usr/bin/env python3
"""OpenJDK와 saját ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from végrehajt_parancs import teendő_gyök


def Futtatás():
    kimenet = teendő_gyök / 'build/verification/jvm'
    tanóra_útvonal = kimenet / 'classes'; tanóra_útvonal.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = teendő_gyök / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((teendő_gyök / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(tanóra_útvonal)] + [str(sztring_adat) for sztring_adat in 원문목록])
    teszt_Lista = [('객체시험', ['Háttér_ÉRTÉK', 'ág_ÉRTÉK', '계산가능']), ('예외시험', []), ('sokaság_teszt', []),
             ('가닥시험', ['számláló_ÉRTÉK', 'teendő_Action', 'szál_ÉRTÉK']), ('한글시험', []), ('teszt_hálózat', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('ellenőriz.teszt_köteg', []), ('bejegyzés_kompatibilitás_teszt', [])]
    ellenőrzés_jelent = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((teendő_gyök / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Név, 포함인수 in teszt_Lista:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(tanóra_útvonal) + ':' + str(자바꾸러미), Név], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(teendő_gyök / 'Eszközök/végrehajt_Fájl.py'), str(tanóra_útvonal / (Név.replace('.', '/') + '.class'))]
            if '.' in Név: 명령인수 += ['--class-name', Név]
            for tartalmaz in 포함인수: 명령인수 += ['--include', str(tanóra_útvonal / (tartalmaz + '.class'))]
            if Név == '한글소스': 명령인수[2] = str(teendő_gyök / '시험/자바/한글소스.java')
            Kész_összeg = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            tényleges_KR = Kész_összeg.stdout.decode('utf-8').replace('\r\n', '\n')
            (kimenet / (Név + '.log')).write_text(tényleges_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", tényleges_KR, re.S)
            assert Kész_összeg.returncode == 0 and 일치, (Név, tényleges_KR)
            KR = next(sztring_adat for sztring_adat in 일치.groups() if sztring_adat is not None) + '\n'
            assert KR == 예상결과, (Név, 예상결과, KR)
            ellenőrzés_jelent['tests'].append({'name': Név, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Név, flush=True)
        # saját JVM에 직접 연결한 magyar szál_ÉRTÉK/진입점은 OpenJDK용 래퍼가 아니다.
        Kész_összeg = subprocess.run(['python3', str(teendő_gyök/'Eszközök/végrehajt_Fájl.py'), str(tanóra_útvonal/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        KR = Kész_összeg.stdout.decode('utf-8').replace('\r\n', '\n')
        (kimenet/'한국어가닥시험.log').write_text(KR)
        assert Kész_összeg.returncode == 0 and 'magyar 직접 szál_ÉRTÉK továbbít_ÉRTÉK\n' in KR and '\nexit 0\n' in KR, KR
        ellenőrzés_jelent['direct_korean_thread_and_entry'] = True
        print('PASS: magyar 직접 szál_ÉRTÉK·Végrehajtás·Futtatás belépési_pont', flush=True)
        érvényes = (tanóra_útvonal / '객체시험.class').read_bytes()
        teszt_eset = [('판거부', érvényes[:6] + b'\x00\x35' + érvényes[8:], 'supported class versions'),
                 ('잘린클래스', érvényes[:24], 'truncated class file')]
        ellenőrzés_jelent['rejection_tests'] = []
        for Név, teher_adat, alapelv_SMS in teszt_eset:
            teszt_adat = kimenet / (Név + '.class'); teszt_adat.write_bytes(teher_adat)
            Kész_összeg = subprocess.run(['python3', str(teendő_gyök / 'Eszközök/végrehajt_Fájl.py'), str(teszt_adat)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Szöveg = Kész_összeg.stdout.decode('utf-8').replace('\r\n', '\n')
            (kimenet / (Név + '.log')).write_text(Szöveg, encoding='utf-8')
            assert Kész_összeg.returncode == 1 and alapelv_SMS in Szöveg and 'exit 1\n' in Szöveg, (Név, Szöveg)
            ellenőrzés_jelent['rejection_tests'].append({'name': Név, 'passed': True})
            print('PASS (rejected):', Név, flush=True)
        ellenőrzés_jelent['passed'] = True
    finally:
        (kimenet / 'report.json').write_text(json.dumps(ellenőrzés_jelent, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Futtatás()
