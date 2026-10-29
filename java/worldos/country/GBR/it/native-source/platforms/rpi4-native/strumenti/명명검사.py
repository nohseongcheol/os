#!/usr/bin/env python3
"""명명 ritagliare·eccezione·경로를 검사한다. --시언어는 libclang dichiarazione 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

azione_radice = Path(__file__).resolve().parents[1]
radice_del_repository = azione_radice.parents[1]

def avvia():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--C_Lingua', action='store_true')
    argomenti = parser_48ee4b1b.parse_args()
    실패들 = []
    valore_di_contratto = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    File_CONTA_NUMERI = 0
    parametro_tabella = {}
    variadic_FUNZIONE = set()
    나무들 = {}
    공용번역기들 = [radice_del_repository/'compiler/compilatore.py', radice_del_repository/'compiler/기계어미리번역.py']
    for percorso in list((azione_radice/'strumenti').glob('*.py')) + list((azione_radice/'예제').rglob('*.py')) + 공용번역기들:
        if percorso.name.endswith(('이름반영.py', '이름분석.py')): continue
        File_CONTA_NUMERI += 1
        나무 = ast.parse(percorso.read_text()); 나무들[percorso] = 나무
        for voce_VALORE in ast.walk(나무):
            if isinstance(voce_VALORE, ast.FunctionDef):
                parametro_tabella.setdefault(voce_VALORE.name, set()).update(parametro_argomento.arg for parametro_argomento in voce_VALORE.args.args + voce_VALORE.args.kwonlyargs)
                if voce_VALORE.args.kwarg: variadic_FUNZIONE.add(voce_VALORE.name)
            if isinstance(voce_VALORE, ast.ClassDef):
                for FUNZIONE_VALORE in voce_VALORE.body:
                    if isinstance(FUNZIONE_VALORE, ast.FunctionDef) and FUNZIONE_VALORE.name == '__init__':
                        parametro_tabella.setdefault(voce_VALORE.name, set()).update(parametro_argomento.arg for parametro_argomento in FUNZIONE_VALORE.args.args + FUNZIONE_VALORE.args.kwonlyargs)
            Nome = ''
            if isinstance(voce_VALORE, (ast.FunctionDef, ast.ClassDef)): Nome = voce_VALORE.name
            elif isinstance(voce_VALORE, ast.Name) and isinstance(voce_VALORE.ctx, ast.Store): Nome = voce_VALORE.id
            elif isinstance(voce_VALORE, ast.arg): Nome = voce_VALORE.arg
            if Nome and Nome not in valore_di_contratto and all(ord(carattere_VALORE)<128 for carattere_VALORE in Nome):
                실패들.append('{}:{}: {}'.format(percorso.relative_to(radice_del_repository), voce_VALORE.lineno, Nome))
    for percorso, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Nome = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Nome not in parametro_tabella or Nome in variadic_FUNZIONE or not any(ord(carattere_VALORE)>127 for carattere_VALORE in Nome): continue
            for parametro_argomento in 호출.keywords:
                if parametro_argomento.arg and parametro_argomento.arg not in parametro_tabella[Nome]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(percorso.relative_to(radice_del_repository), 호출.lineno, Nome, parametro_argomento.arg))
    for riga_di_ingresso in (azione_radice/'명명/nome_file_mapping.tsv').read_text().splitlines()[1:]:
        Indietro_articolo, Regolari_articolo, Processi_VALORE_voce = riga_di_ingresso.split('\t')
        if not (azione_radice/Regolari_articolo).is_file(): 실패들.append('spostare_VALORE file 없음: '+Regolari_articolo)
        if Processi_VALORE_voce == '호환진입점유지' and not (azione_radice/Indietro_articolo).is_file(): 실패들.append('호환 punto_di_ingresso 없음: '+Indietro_articolo)
    예제 = (azione_radice.parents[1]/'example/java/EsempioRete.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for percorso in sorted((azione_radice.parents[1]/'example/java').glob('*.java')):
        codiceSorgente = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', percorso.read_text())
        for Nome in re.findall(r'\b[^\W\d]\w*\b', codiceSorgente, re.UNICODE):
            if Nome not in 예약어 and all(ord(carattere_VALORE)<128 for carattere_VALORE in Nome):
                실패들.append('{}: 예제의 영어 identificatore_VALORE {}'.format(percorso.name, Nome))
    for Nome in ('Finestra', 'pulsante', 'Etichetta', 'campo_di_testo', 'schermata_elemento', 'evento_coda', 'esecutoreAsincrono', '실행할일', '동작받이', 'Action_informativa', '작업'):
        codiceSorgente = (azione_radice/'한국어자바/Italiano/nativo'/(Nome+'.java')).read_text()
        codiceSorgente = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', codiceSorgente)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', codiceSorgente):
            실패들.append(Nome+': Italiano 직접 구현에 표준 oggetto_VALORE 래퍼가 남았습니다.')
    시언어예제 = (azione_radice.parents[1]/'example/c/EsempioRete.c').read_text()
    for Nome in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Nome in 시언어예제: 실패들.append('C comunicazione 예제에 남은 표준 Nome: '+Nome)
    파이썬예제 = (azione_radice.parents[1]/'example/python/EsempioRete.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python comunicazione 예제에 남은 표준 eccezione 직접 usare_VALORE')
    intestazione_VALORE = (azione_radice.parents[1]/'posix-kor/arm64-native/dichiarazioni/rete_ABI.h').read_text()
    for Nome in ('cloud_serie', 'socket_di_datagramma', 'datagramma_protocollo', 'socket_e_mail', 'cloud_socket_e_mail', 'Crea_endpoint', 'inviare_datagramma_dati'):
        if re.search(r'^#define\s+'+Nome+r'\b', intestazione_VALORE, re.M): 실패들.append('C 직접 implementazione 대신 macro_VALORE usare_VALORE: '+Nome)
    자바파일수 = 0
    for radice_VALORE in ('codiceSorgente', 'spazio_utente/자바', '한국어자바'):
        for percorso in (azione_radice/radice_VALORE).rglob('*.java'):
            자바파일수 += 1
            codiceSorgente = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', percorso.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', codiceSorgente):
                실패들.append('{}: 한국어화되지 않은 dichiarazione {}'.format(percorso.relative_to(azione_radice), 맞음[1]))
            if radice_VALORE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', codiceSorgente):
                실패들.append('{}: 공개 eccezione dichiarazione'.format(percorso.relative_to(azione_radice)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for percorso in sorted((radice_del_repository/'os/codiceSorgente').glob('*.java')):
        x86자바파일수 += 1
        codiceSorgente = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', percorso.read_text())
        for Nome in re.findall(r'\b[^\W\d]\w*\b', codiceSorgente, re.UNICODE):
            if Nome not in 예약어 | 표준자바이름 and all(ord(carattere_VALORE)<128 for carattere_VALORE in Nome):
                실패들.append('{}: nativo 영어 identificatore_VALORE {}'.format(percorso.relative_to(radice_del_repository), Nome))
    LOG_riga = {'passed': False, 'python_files': File_CONTA_NUMERI, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if argomenti.C_Lingua:
        subprocess.check_call(['python3', str(azione_radice/'strumenti/시언어이름분석.py')])
        Analizza_VALORE = json.loads((azione_radice/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(errore) for errore in Analizza_VALORE['errore'])
        esportare_ABI = set(json.loads((azione_radice/'명명/규격이름.json').read_text()))
        for voce_VALORE in Analizza_VALORE['dichiarazione'].values():
            Nome = voce_VALORE['Nome']; percorso = Path(voce_VALORE['file'])
            codiceSorgente = percorso.read_bytes()
            # Italiano 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if codiceSorgente[voce_VALORE['SCARTO_VALORE']:voce_VALORE['SCARTO_VALORE']+len(Nome)] == Nome.encode() and Nome not in esportare_ABI:
                실패들.append('{}:{}: {}'.format(percorso.relative_to(azione_radice), voce_VALORE['riga_di_ingresso'], Nome))
        LOG_riga['c_semantic_checked'] = True
        LOG_riga['c_source_sha256'] = {str(Path(file).relative_to(azione_radice)):hash_File for file,hash_File in Analizza_VALORE['원문해시'].items()}
    LOG_riga['passed'] = not 실패들; LOG_riga['failures'] = 실패들
    meta_VALORE = azione_radice/'build/verification/naming'; meta_VALORE.mkdir(parents=True, exist_ok=True)
    (meta_VALORE/'report.json').write_text(json.dumps(LOG_riga, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Italiano dichiarazione·file percorso·호환 punto_di_ingresso·comunicazione 예제')

if __name__ == '__main__': avvia()
