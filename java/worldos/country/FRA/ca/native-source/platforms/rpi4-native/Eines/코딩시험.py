#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Executa_ordre import Project_rel

def Executa_2():
    mesura_dades=Project_rel/'build/verification/coding';mesura_dades.mkdir(parents=True,exist_ok=True)
    validació_informe={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rel/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Project_rel/'Eines/개발꾸러미내보내기.py')])
        with tarfile.open(str(Project_rel/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(mesura_dades))
        개발꾸러미=mesura_dades/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Nom in ('Crear_extrem','enllaçar_ADREÇA','자료전문보내기','자료전문받기','crear_arxiu','tancar_arxiu_dades','escriure_arxiu_dades'):
            assert ' T '+Nom+'\n' in 심볼목록, Nom
        (mesura_dades/'korean-function-symbols.txt').write_text(심볼목록)
        validació_informe['checks'].append('real-korean-c-function-symbols')
        def Executa_ordre(Nom,Camí,arg_MATRIU,예상결과):
            dades_càrrec=subprocess.run(['python3',str(Project_rel/'Eines/Executa_arxiu.py'),str(Camí)]+arg_MATRIU,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (mesura_dades/(Nom+'.log')).write_bytes(dades_càrrec.stdout);assert dades_càrrec.returncode==0,dades_càrrec.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in dades_càrrec.stdout,dades_càrrec.stdout;validació_informe['checks'].append(Nom)
        for 뒷부분 in ('c','cpp'):
            실행파일=mesura_dades/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            Executa_ordre('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=mesura_dades/'flux_VALOR.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/flux_VALOR.c'),'-o',str(실행파일)])
        Executa_ordre('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        Executa_ordre('korean-python',Project_rel/'예제/한글코딩/인사.py',['--include',str(Project_rel/'예제/한글코딩/Català.py')],'안녕하세요 누리')
        Executa_ordre('guest-korean-javac',Project_rel/'예제/한글코딩/인사.java',[],'안녕하세요 · total_VALOR=42')
        validació_informe['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(mesura_dades/'report.json').write_text(json.dumps(validació_informe,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Executa_2()
