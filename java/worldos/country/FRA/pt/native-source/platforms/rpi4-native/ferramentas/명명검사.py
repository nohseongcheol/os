#!/usr/bin/env python3
"""명명 recortar·exceção·경로를 검사한다. --시언어는 libclang declaração 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ação_raiz = Path(__file__).resolve().parents[1]
repositório_raiz = ação_raiz.parents[1]

def iniciar():
    analisador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analisador_48ee4b1b.add_argument('--C_Idioma', action='store_true')
    argumentos = analisador_48ee4b1b.parse_args()
    실패들 = []
    valor_do_contrato = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Arquivo_CONT_NÚM = 0
    parâmetro_tabela = {}
    variádico_FUNÇÃO = set()
    나무들 = {}
    공용번역기들 = [repositório_raiz/'compiler/compilador.py', repositório_raiz/'compiler/CompiladorAntecipado.py']
    for caminho in list((ação_raiz/'ferramentas').glob('*.py')) + list((ação_raiz/'예제').rglob('*.py')) + 공용번역기들:
        if caminho.name.endswith(('이름반영.py', '이름분석.py')): continue
        Arquivo_CONT_NÚM += 1
        나무 = ast.parse(caminho.read_text()); 나무들[caminho] = 나무
        for entrada_VALOR_962f286b in ast.walk(나무):
            if isinstance(entrada_VALOR_962f286b, ast.FunctionDef):
                parâmetro_tabela.setdefault(entrada_VALOR_962f286b.name, set()).update(parâmetro_argumento.arg for parâmetro_argumento in entrada_VALOR_962f286b.args.args + entrada_VALOR_962f286b.args.kwonlyargs)
                if entrada_VALOR_962f286b.args.kwarg: variádico_FUNÇÃO.add(entrada_VALOR_962f286b.name)
            if isinstance(entrada_VALOR_962f286b, ast.ClassDef):
                for FUNÇÃO_VALOR in entrada_VALOR_962f286b.body:
                    if isinstance(FUNÇÃO_VALOR, ast.FunctionDef) and FUNÇÃO_VALOR.name == '__init__':
                        parâmetro_tabela.setdefault(entrada_VALOR_962f286b.name, set()).update(parâmetro_argumento.arg for parâmetro_argumento in FUNÇÃO_VALOR.args.args + FUNÇÃO_VALOR.args.kwonlyargs)
            Nome = ''
            if isinstance(entrada_VALOR_962f286b, (ast.FunctionDef, ast.ClassDef)): Nome = entrada_VALOR_962f286b.name
            elif isinstance(entrada_VALOR_962f286b, ast.Name) and isinstance(entrada_VALOR_962f286b.ctx, ast.Store): Nome = entrada_VALOR_962f286b.id
            elif isinstance(entrada_VALOR_962f286b, ast.arg): Nome = entrada_VALOR_962f286b.arg
            if Nome and Nome not in valor_do_contrato and all(ord(caractere_VALOR)<128 for caractere_VALOR in Nome):
                실패들.append('{}:{}: {}'.format(caminho.relative_to(repositório_raiz), entrada_VALOR_962f286b.lineno, Nome))
    for caminho, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Nome = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Nome not in parâmetro_tabela or Nome in variádico_FUNÇÃO or not any(ord(caractere_VALOR)>127 for caractere_VALOR in Nome): continue
            for parâmetro_argumento in 호출.keywords:
                if parâmetro_argumento.arg and parâmetro_argumento.arg not in parâmetro_tabela[Nome]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(caminho.relative_to(repositório_raiz), 호출.lineno, Nome, parâmetro_argumento.arg))
    for linha_de_entrada in (ação_raiz/'명명/nome_de_arquivo_mapeamento.tsv').read_text().splitlines()[1:]:
        Anterior_item, em_dia_item, Processo_VALOR_entrada = linha_de_entrada.split('\t')
        if not (ação_raiz/em_dia_item).is_file(): 실패들.append('mover_VALOR ficheiro 없음: '+em_dia_item)
        if Processo_VALOR_entrada == '호환진입점유지' and not (ação_raiz/Anterior_item).is_file(): 실패들.append('호환 ponto_de_entrada 없음: '+Anterior_item)
    예제 = (ação_raiz.parents[1]/'example/java/ExemploRede.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for caminho in sorted((ação_raiz.parents[1]/'example/java').glob('*.java')):
        códigoFonte = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', caminho.read_text())
        for Nome in re.findall(r'\b[^\W\d]\w*\b', códigoFonte, re.UNICODE):
            if Nome not in 예약어 and all(ord(caractere_VALOR)<128 for caractere_VALOR in Nome):
                실패들.append('{}: 예제의 영어 identificador_VALOR {}'.format(caminho.name, Nome))
    for Nome in ('Janela', 'botão', 'Etiqueta', 'campo_de_texto', 'tela_elemento', 'Evento_Fila', 'tarefaSegundoPlano', '실행할일', '동작받이', 'Ação_aviso', '작업'):
        códigoFonte = (ação_raiz/'한국어자바/Português/nativo'/(Nome+'.java')).read_text()
        códigoFonte = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', códigoFonte)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', códigoFonte):
            실패들.append(Nome+': Português 직접 구현에 표준 objeto_VALOR 래퍼가 남았습니다.')
    시언어예제 = (ação_raiz.parents[1]/'example/c/ExemploRede.c').read_text()
    for Nome in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Nome in 시언어예제: 실패들.append('C comunicação 예제에 남은 표준 Nome: '+Nome)
    파이썬예제 = (ação_raiz.parents[1]/'example/python/ExemploRede.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python comunicação 예제에 남은 표준 exceção 직접 uso_VALOR')
    HEAD_VALOR = (ação_raiz.parents[1]/'posix-kor/arm64-native/declarações/rede_ABI.h').read_text()
    for Nome in ('malha_Família', 'datagrama_soquete', 'datagrama_protocolo', 'soquete_email', 'malha_soquete_email', 'Criar_empresa', 'enviar_datagrama_dados'):
        if re.search(r'^#define\s+'+Nome+r'\b', HEAD_VALOR, re.M): 실패들.append('C 직접 implementação 대신 macro_VALOR uso_VALOR: '+Nome)
    자바파일수 = 0
    for raiz_VALOR in ('códigoFonte', 'espaço_do_utilizador/자바', '한국어자바'):
        for caminho in (ação_raiz/raiz_VALOR).rglob('*.java'):
            자바파일수 += 1
            códigoFonte = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', caminho.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', códigoFonte):
                실패들.append('{}: 한국어화되지 않은 declaração {}'.format(caminho.relative_to(ação_raiz), 맞음[1]))
            if raiz_VALOR == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', códigoFonte):
                실패들.append('{}: 공개 exceção declaração'.format(caminho.relative_to(ação_raiz)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for caminho in sorted((repositório_raiz/'os/códigoFonte').glob('*.java')):
        x86자바파일수 += 1
        códigoFonte = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', caminho.read_text())
        for Nome in re.findall(r'\b[^\W\d]\w*\b', códigoFonte, re.UNICODE):
            if Nome not in 예약어 | 표준자바이름 and all(ord(caractere_VALOR)<128 for caractere_VALOR in Nome):
                실패들.append('{}: nativo 영어 identificador_VALOR {}'.format(caminho.relative_to(repositório_raiz), Nome))
    LOG_linha = {'passed': False, 'python_files': Arquivo_CONT_NÚM, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if argumentos.C_Idioma:
        subprocess.check_call(['python3', str(ação_raiz/'ferramentas/시언어이름분석.py')])
        Analisar_VALOR = json.loads((ação_raiz/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(erro) for erro in Analisar_VALOR['erro'])
        exportar_ABI = set(json.loads((ação_raiz/'명명/규격이름.json').read_text()))
        for entrada_VALOR_962f286b in Analisar_VALOR['declaração'].values():
            Nome = entrada_VALOR_962f286b['Nome']; caminho = Path(entrada_VALOR_962f286b['ficheiro'])
            códigoFonte = caminho.read_bytes()
            # Português 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if códigoFonte[entrada_VALOR_962f286b['DESLOC_VALOR']:entrada_VALOR_962f286b['DESLOC_VALOR']+len(Nome)] == Nome.encode() and Nome not in exportar_ABI:
                실패들.append('{}:{}: {}'.format(caminho.relative_to(ação_raiz), entrada_VALOR_962f286b['linha_de_entrada'], Nome))
        LOG_linha['c_semantic_checked'] = True
        LOG_linha['c_source_sha256'] = {str(Path(ficheiro).relative_to(ação_raiz)):hash_Arquivo for ficheiro,hash_Arquivo in Analisar_VALOR['원문해시'].items()}
    LOG_linha['passed'] = not 실패들; LOG_linha['failures'] = 실패들
    destino_VALOR = ação_raiz/'build/verification/naming'; destino_VALOR.mkdir(parents=True, exist_ok=True)
    (destino_VALOR/'report.json').write_text(json.dumps(LOG_linha, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Português declaração·ficheiro caminho·호환 ponto_de_entrada·comunicação 예제')

if __name__ == '__main__': iniciar()
