#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from exekutatu_komando import Project_erro


def Exekutatu_2():
    출력결과 = Project_erro / 'build/verification/jvm'
    Gela_bide_izen = 출력결과 / 'classes'; Gela_bide_izen.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Project_erro / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Project_erro / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Gela_bide_izen)] + [str(kate_datuak) for kate_datuak in 원문목록])
    시험목록 = [('객체시험', ['horma_paper_balio', 'adar_balio', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['셈통', 'ataza_ekintza', 'hari_balio']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('baliozkotu.꾸러미시험', []), ('진입호환시험', [])]
    balidazio_txosten = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Project_erro / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Izena, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Gela_bide_izen) + ':' + str(자바꾸러미), Izena], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Project_erro / 'Tresnak/exekutatu_fitxategi.py'), str(Gela_bide_izen / (Izena.replace('.', '/') + '.class'))]
            if '.' in Izena: 명령인수 += ['--class-name', Izena]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(Gela_bide_izen / (포함항목 + '.class'))]
            if Izena == '한글소스': 명령인수[2] = str(Project_erro / '시험/자바/한글소스.java')
            Osatutakoak_kopuru = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            benetako_neurria = Osatutakoak_kopuru.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Izena + '.log')).write_text(benetako_neurria, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", benetako_neurria, re.S)
            assert Osatutakoak_kopuru.returncode == 0 and 일치, (Izena, benetako_neurria)
            EMAITZA = next(kate_datuak for kate_datuak in 일치.groups() if kate_datuak is not None) + '\n'
            assert EMAITZA == 예상결과, (Izena, 예상결과, EMAITZA)
            balidazio_txosten['tests'].append({'name': Izena, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Izena, flush=True)
        # 자체 JVM에 직접 연결한 Euskara hari_balio/진입점은 OpenJDK용 래퍼가 아니다.
        Osatutakoak_kopuru = subprocess.run(['python3', str(Project_erro/'Tresnak/exekutatu_fitxategi.py'), str(Gela_bide_izen/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        EMAITZA = Osatutakoak_kopuru.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(EMAITZA)
        assert Osatutakoak_kopuru.returncode == 0 and 'Euskara 직접 hari_balio pasatu_balio\n' in EMAITZA and '\nexit 0\n' in EMAITZA, EMAITZA
        balidazio_txosten['direct_korean_thread_and_entry'] = True
        print('PASS: Euskara 직접 hari_balio·Exekutatu·Exekutatu_2 sarrera_p', flush=True)
        유효함 = (Gela_bide_izen / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        balidazio_txosten['rejection_tests'] = []
        for Izena, karga_datuak, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Izena + '.class'); 시험자료.write_bytes(karga_datuak)
            Osatutakoak_kopuru = subprocess.run(['python3', str(Project_erro / 'Tresnak/exekutatu_fitxategi.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Testua = Osatutakoak_kopuru.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Izena + '.log')).write_text(Testua, encoding='utf-8')
            assert Osatutakoak_kopuru.returncode == 1 and 알림문 in Testua and 'exit 1\n' in Testua, (Izena, Testua)
            balidazio_txosten['rejection_tests'].append({'name': Izena, 'passed': True})
            print('PASS (rejected):', Izena, flush=True)
        balidazio_txosten['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(balidazio_txosten, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Exekutatu_2()
