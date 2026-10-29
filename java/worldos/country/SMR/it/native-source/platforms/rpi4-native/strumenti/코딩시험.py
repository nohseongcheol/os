#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Esegui_comando import azione_radice

def avvia():
    KR_dati=azione_radice/'build/verification/coding';KR_dati.mkdir(parents=True,exist_ok=True)
    convalida_Report={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((azione_radice/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(azione_radice/'strumenti/esportare_SDK.py')])
        with tarfile.open(str(azione_radice/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_dati))
        kit_di_sviluppo=KR_dati/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(kit_di_sviluppo/'lib/libposix-kor-user.a')]).decode()
        for Nome in ('Crea_endpoint','BIND_e_mail','inviare_datagramma_dati','ricevere_datagramma_dati','aperto_File','파일자료읽기','scrivere_File_dati'):
            assert ' T '+Nome+'\n' in 심볼목록, Nome
        (KR_dati/'korean-function-symbols.txt').write_text(심볼목록)
        convalida_Report['checks'].append('real-korean-c-function-symbols')
        def Esegui_comando(Nome,percorso,argomento_array,예상결과):
            dati_funzione=subprocess.run(['python3',str(azione_radice/'strumenti/Esegui_File.py'),str(percorso)]+argomento_array,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_dati/(Nome+'.log')).write_bytes(dati_funzione.stdout);assert dati_funzione.returncode==0,dati_funzione.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in dati_funzione.stdout,dati_funzione.stdout;convalida_Report['checks'].append(Nome)
        for 뒷부분 in ('c','cpp'):
            eseguibile=KR_dati/('messaggio_di_saluto_ae353e94-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(kit_di_sviluppo/'compile.py'),str(kit_di_sviluppo/'examples'/('messaggio_di_saluto_ae353e94.'+뒷부분)),'-o',str(eseguibile)])
            Esegui_comando('korean-'+뒷부분,eseguibile,[],'posix-kor 호출')
        eseguibile=KR_dati/'Stream_VALORE.elf'
        subprocess.check_call(['python3',str(kit_di_sviluppo/'compile.py'),str(kit_di_sviluppo/'examples/Stream_VALORE.c'),'-o',str(eseguibile)])
        Esegui_comando('c-stream-queues',eseguibile,[],'C posix-kor 연결형 comunicazione PASS')
        Esegui_comando('korean-python',azione_radice/'예제/한글코딩/messaggio_di_saluto_ae353e94.py',['--include',str(azione_radice/'예제/한글코딩/Italiano.py')],'안녕하세요 누리')
        Esegui_comando('guest-korean-javac',azione_radice/'예제/한글코딩/messaggio_di_saluto_ae353e94.java',[],'안녕하세요 · totale_VALORE=42')
        convalida_Report['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_dati/'report.json').write_text(json.dumps(convalida_Report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':avvia()
