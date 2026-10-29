#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from köra_kommando import åtgärd_rot

def Kör():
    KR_data=åtgärd_rot/'build/verification/coding';KR_data.mkdir(parents=True,exist_ok=True)
    validering_Rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((åtgärd_rot/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(åtgärd_rot/'verktyg/exportera_SDK.py')])
        with tarfile.open(str(åtgärd_rot/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_data))
        development_kit=KR_data/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(development_kit/'lib/libposix-kor-user.a')]).decode()
        for Namn in ('Skapa_deltagare','BIND_ADRESS','skicka_datagram_data','få_datagram_data','skapa_fil','läsa_fil_data','skriva_fil_data'):
            assert ' T '+Namn+'\n' in 심볼목록, Namn
        (KR_data/'korean-function-symbols.txt').write_text(심볼목록)
        validering_Rapport['checks'].append('real-korean-c-function-symbols')
        def köra_kommando(Namn,sökväg_2,argument_MATRIS,예상결과):
            data_placera=subprocess.run(['python3',str(åtgärd_rot/'verktyg/köra_fil.py'),str(sökväg_2)]+argument_MATRIS,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_data/(Namn+'.log')).write_bytes(data_placera.stdout);assert data_placera.returncode==0,data_placera.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in data_placera.stdout,data_placera.stdout;validering_Rapport['checks'].append(Namn)
        for 뒷부분 in ('c','cpp'):
            körbar_fil_fil=KR_data/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(development_kit/'compile.py'),str(development_kit/'examples'/('인사.'+뒷부분)),'-o',str(körbar_fil_fil)])
            köra_kommando('korean-'+뒷부분,körbar_fil_fil,[],'posix-kor 호출')
        körbar_fil_fil=KR_data/'flöde_värde.elf'
        subprocess.check_call(['python3',str(development_kit/'compile.py'),str(development_kit/'examples/flöde_värde.c'),'-o',str(körbar_fil_fil)])
        köra_kommando('c-stream-queues',körbar_fil_fil,[],'C posix-kor 연결형 kommunikation PASS')
        köra_kommando('korean-python',åtgärd_rot/'예제/한글코딩/인사.py',['--include',str(åtgärd_rot/'예제/한글코딩/Svenska.py')],'안녕하세요 누리')
        köra_kommando('guest-korean-javac',åtgärd_rot/'예제/한글코딩/인사.java',[],'안녕하세요 · summa_värde=42')
        validering_Rapport['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_data/'report.json').write_text(json.dumps(validering_Rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Kör()
