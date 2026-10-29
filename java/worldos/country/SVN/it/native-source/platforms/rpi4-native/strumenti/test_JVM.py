#!/usr/bin/env python3
"""OpenJDK와 nativo ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Esegui_comando import azione_radice


def avvia():
    output = azione_radice / 'build/verification/jvm'
    Corso_percorso = output / 'classes'; Corso_percorso.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = azione_radice / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((azione_radice / 'prove/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Corso_percorso)] + [str(stringa_dati) for stringa_dati in 원문목록])
    elenco_dei_test = [('객체시험', ['sfondo_VALORE', 'ramo_VALORE', '계산가능']), ('예외시험', []), ('album_test', []),
             ('가닥시험', ['contatore_VALORE', 'task_Action', 'thread_VALORE']), ('한글시험', []), ('test_Rete', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('convalidare.test_aggregare', []), ('voce_compatibilità_test', [])]
    convalida_Report = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((azione_radice / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Nome, 포함인수 in elenco_dei_test:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Corso_percorso) + ':' + str(자바꾸러미), Nome], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(azione_radice / 'strumenti/Esegui_File.py'), str(Corso_percorso / (Nome.replace('.', '/') + '.class'))]
            if '.' in Nome: 명령인수 += ['--class-name', Nome]
            for includere in 포함인수: 명령인수 += ['--include', str(Corso_percorso / (includere + '.class'))]
            if Nome == '한글소스': 명령인수[2] = str(azione_radice / 'prove/자바/한글소스.java')
            Completate_importo = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            effettivo_KR = Completate_importo.stdout.decode('utf-8').replace('\r\n', '\n')
            (output / (Nome + '.log')).write_text(effettivo_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", effettivo_KR, re.S)
            assert Completate_importo.returncode == 0 and 일치, (Nome, effettivo_KR)
            risultato = next(stringa_dati for stringa_dati in 일치.groups() if stringa_dati is not None) + '\n'
            assert risultato == 예상결과, (Nome, 예상결과, risultato)
            convalida_Report['tests'].append({'name': Nome, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Nome, flush=True)
        # nativo JVM에 직접 연결한 Italiano thread_VALORE/진입점은 OpenJDK용 래퍼가 아니다.
        Completate_importo = subprocess.run(['python3', str(azione_radice/'strumenti/Esegui_File.py'), str(Corso_percorso/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        risultato = Completate_importo.stdout.decode('utf-8').replace('\r\n', '\n')
        (output/'한국어가닥시험.log').write_text(risultato)
        assert Completate_importo.returncode == 0 and 'Italiano 직접 thread_VALORE passare_VALORE\n' in risultato and '\nexit 0\n' in risultato, risultato
        convalida_Report['direct_korean_thread_and_entry'] = True
        print('PASS: Italiano 직접 thread_VALORE·Esegui·avvia punto_di_ingresso', flush=True)
        valido = (Corso_percorso / '객체시험.class').read_bytes()
        test_case = [('판거부', valido[:6] + b'\x00\x35' + valido[8:], 'supported class versions'),
                 ('잘린클래스', valido[:24], 'truncated class file')]
        convalida_Report['rejection_tests'] = []
        for Nome, payload_dati, informativa_SMS in test_case:
            test_dati = output / (Nome + '.class'); test_dati.write_bytes(payload_dati)
            Completate_importo = subprocess.run(['python3', str(azione_radice / 'strumenti/Esegui_File.py'), str(test_dati)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            testo = Completate_importo.stdout.decode('utf-8').replace('\r\n', '\n')
            (output / (Nome + '.log')).write_text(testo, encoding='utf-8')
            assert Completate_importo.returncode == 1 and informativa_SMS in testo and 'exit 1\n' in testo, (Nome, testo)
            convalida_Report['rejection_tests'].append({'name': Nome, 'passed': True})
            print('PASS (rejected):', Nome, flush=True)
        convalida_Report['passed'] = True
    finally:
        (output / 'report.json').write_text(json.dumps(convalida_Report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    avvia()
