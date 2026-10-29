#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from executar_comando import Project_raíz

def Executar_2():
    medida_datos=Project_raíz/'build/verification/coding';medida_datos.mkdir(parents=True,exist_ok=True)
    validación_informe={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_raíz/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Project_raíz/'Ferramentas/개발꾸러미내보내기.py')])
        with tarfile.open(str(Project_raíz/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(medida_datos))
        개발꾸러미=medida_datos/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Nome in ('crear_extremo','ligar_ENDEREZO','자료전문보내기','자료전문받기','abrir_Ficheiro','파일자료읽기','escribir_Ficheiro_datos'):
            assert ' T '+Nome+'\n' in 심볼목록, Nome
        (medida_datos/'korean-function-symbols.txt').write_text(심볼목록)
        validación_informe['checks'].append('real-korean-c-function-symbols')
        def executar_comando(Nome,CAMIÑO,argumento_MATRIZ,예상결과):
            datos_cargo=subprocess.run(['python3',str(Project_raíz/'Ferramentas/executar_Ficheiro.py'),str(CAMIÑO)]+argumento_MATRIZ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (medida_datos/(Nome+'.log')).write_bytes(datos_cargo.stdout);assert datos_cargo.returncode==0,datos_cargo.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in datos_cargo.stdout,datos_cargo.stdout;validación_informe['checks'].append(Nome)
        for 뒷부분 in ('c','cpp'):
            실행파일=medida_datos/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            executar_comando('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=medida_datos/'fluxo_VALOR.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/fluxo_VALOR.c'),'-o',str(실행파일)])
        executar_comando('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        executar_comando('korean-python',Project_raíz/'예제/한글코딩/인사.py',['--include',str(Project_raíz/'예제/한글코딩/Galego.py')],'안녕하세요 누리')
        executar_comando('guest-korean-javac',Project_raíz/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        validación_informe['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(medida_datos/'report.json').write_text(json.dumps(validación_informe,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Executar_2()
