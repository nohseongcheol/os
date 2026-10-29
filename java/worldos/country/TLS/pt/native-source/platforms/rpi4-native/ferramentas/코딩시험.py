#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Executar_comando import ação_raiz

def iniciar():
    RC_dados=ação_raiz/'build/verification/coding';RC_dados.mkdir(parents=True,exist_ok=True)
    validação_relatar={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ação_raiz/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(ação_raiz/'ferramentas/exportar_SDK.py')])
        with tarfile.open(str(ação_raiz/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(RC_dados))
        kit_de_desenvolvimento=RC_dados/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(kit_de_desenvolvimento/'lib/libposix-kor-user.a')]).decode()
        for Nome in ('Criar_empresa','BIND_email','enviar_datagrama_dados','receber_datagrama_dados','abrir_Arquivo','leitura_Arquivo_dados','gravar_Arquivo_dados'):
            assert ' T '+Nome+'\n' in 심볼목록, Nome
        (RC_dados/'korean-function-symbols.txt').write_text(심볼목록)
        validação_relatar['checks'].append('real-korean-c-function-symbols')
        def Executar_comando(Nome,caminho,argumento_MATRIZ,예상결과):
            dados_cargo=subprocess.run(['python3',str(ação_raiz/'ferramentas/Executar_Arquivo.py'),str(caminho)]+argumento_MATRIZ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (RC_dados/(Nome+'.log')).write_bytes(dados_cargo.stdout);assert dados_cargo.returncode==0,dados_cargo.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in dados_cargo.stdout,dados_cargo.stdout;validação_relatar['checks'].append(Nome)
        for 뒷부분 in ('c','cpp'):
            executável=RC_dados/('saudação_ae353e94-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(kit_de_desenvolvimento/'compile.py'),str(kit_de_desenvolvimento/'examples'/('saudação_ae353e94.'+뒷부분)),'-o',str(executável)])
            Executar_comando('korean-'+뒷부분,executável,[],'posix-kor 호출')
        executável=RC_dados/'fluxo_VALOR.elf'
        subprocess.check_call(['python3',str(kit_de_desenvolvimento/'compile.py'),str(kit_de_desenvolvimento/'examples/fluxo_VALOR.c'),'-o',str(executável)])
        Executar_comando('c-stream-queues',executável,[],'C posix-kor 연결형 comunicação PASS')
        Executar_comando('korean-python',ação_raiz/'예제/한글코딩/saudação_ae353e94.py',['--include',str(ação_raiz/'예제/한글코딩/Português.py')],'안녕하세요 누리')
        Executar_comando('guest-korean-javac',ação_raiz/'예제/한글코딩/saudação_ae353e94.java',[],'안녕하세요 · total_VALOR=42')
        validação_relatar['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(RC_dados/'report.json').write_text(json.dumps(validação_relatar,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':iniciar()
