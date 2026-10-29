#!/usr/bin/env python3
"""OpenJDK와 nativo ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Executar_comando import ação_raiz


def iniciar():
    saída = ação_raiz / 'build/verification/jvm'
    aula_caminho = saída / 'classes'; aula_caminho.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = ação_raiz / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((ação_raiz / 'testes/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(aula_caminho)] + [str(cadeia_dados) for cadeia_dados in 원문목록])
    lista_de_testes = [('객체시험', ['Tela_de_fundo_VALOR', 'branch_VALOR', '계산가능']), ('예외시험', []), ('Coleção_teste', []),
             ('가닥시험', ['contador_VALOR', 'Tarefa_Ação', 'thread_VALOR']), ('한글시험', []), ('teste_Rede', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('validar.teste_grupo', []), ('entrada_compatibilidade_teste', [])]
    validação_relatar = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((ação_raiz / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Nome, 포함인수 in lista_de_testes:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(aula_caminho) + ':' + str(자바꾸러미), Nome], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(ação_raiz / 'ferramentas/Executar_Arquivo.py'), str(aula_caminho / (Nome.replace('.', '/') + '.class'))]
            if '.' in Nome: 명령인수 += ['--class-name', Nome]
            for incluir in 포함인수: 명령인수 += ['--include', str(aula_caminho / (incluir + '.class'))]
            if Nome == '한글소스': 명령인수[2] = str(ação_raiz / 'testes/자바/한글소스.java')
            concluído_valor = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            real_RC = concluído_valor.stdout.decode('utf-8').replace('\r\n', '\n')
            (saída / (Nome + '.log')).write_text(real_RC, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", real_RC, re.S)
            assert concluído_valor.returncode == 0 and 일치, (Nome, real_RC)
            resultado = next(cadeia_dados for cadeia_dados in 일치.groups() if cadeia_dados is not None) + '\n'
            assert resultado == 예상결과, (Nome, 예상결과, resultado)
            validação_relatar['tests'].append({'name': Nome, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Nome, flush=True)
        # nativo JVM에 직접 연결한 Português thread_VALOR/진입점은 OpenJDK용 래퍼가 아니다.
        concluído_valor = subprocess.run(['python3', str(ação_raiz/'ferramentas/Executar_Arquivo.py'), str(aula_caminho/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        resultado = concluído_valor.stdout.decode('utf-8').replace('\r\n', '\n')
        (saída/'한국어가닥시험.log').write_text(resultado)
        assert concluído_valor.returncode == 0 and 'Português 직접 thread_VALOR 통과\n' in resultado and '\nexit 0\n' in resultado, resultado
        validação_relatar['direct_korean_thread_and_entry'] = True
        print('PASS: Português 직접 thread_VALOR·Executar·iniciar ponto_de_entrada', flush=True)
        válido = (aula_caminho / '객체시험.class').read_bytes()
        caso_de_teste = [('판거부', válido[:6] + b'\x00\x35' + válido[8:], 'supported class versions'),
                 ('잘린클래스', válido[:24], 'truncated class file')]
        validação_relatar['rejection_tests'] = []
        for Nome, carga_dados, aviso_SMS in caso_de_teste:
            teste_dados = saída / (Nome + '.class'); teste_dados.write_bytes(carga_dados)
            concluído_valor = subprocess.run(['python3', str(ação_raiz / 'ferramentas/Executar_Arquivo.py'), str(teste_dados)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            texto = concluído_valor.stdout.decode('utf-8').replace('\r\n', '\n')
            (saída / (Nome + '.log')).write_text(texto, encoding='utf-8')
            assert concluído_valor.returncode == 1 and aviso_SMS in texto and 'exit 1\n' in texto, (Nome, texto)
            validação_relatar['rejection_tests'].append({'name': Nome, 'passed': True})
            print('PASS (rejected):', Nome, flush=True)
        validação_relatar['passed'] = True
    finally:
        (saída / 'report.json').write_text(json.dumps(validação_relatar, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    iniciar()
