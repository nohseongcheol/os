#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Utfør_kommando import speile_rot

def Kjør_2():
    KR_data=speile_rot/'build/verification/coding';KR_data.mkdir(parents=True,exist_ok=True)
    validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((speile_rot/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(speile_rot/'Verktøy/eksportere_SDK.py')])
        with tarfile.open(str(speile_rot/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_data))
        utviklingspakke=KR_data/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(utviklingspakke/'lib/libposix-kor-user.a')]).decode()
        for Navn in ('åpne_deltaker','BIND_e_post','sende_datagram_data','motta_datagram_data','åpen_Fil','파일자료읽기','skrive_Fil_data'):
            assert ' T '+Navn+'\n' in 심볼목록, Navn
        (KR_data/'korean-function-symbols.txt').write_text(심볼목록)
        validering_rapport['checks'].append('real-korean-c-function-symbols')
        def Utfør_kommando(Navn,Sti,argument_MATRISE,예상결과):
            data_plassere=subprocess.run(['python3',str(speile_rot/'Verktøy/Utfør_Fil.py'),str(Sti)]+argument_MATRISE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_data/(Navn+'.log')).write_bytes(data_plassere.stdout);assert data_plassere.returncode==0,data_plassere.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in data_plassere.stdout,data_plassere.stdout;validering_rapport['checks'].append(Navn)
        for 뒷부분 in ('c','cpp'):
            kjørbar_fil=KR_data/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(utviklingspakke/'compile.py'),str(utviklingspakke/'examples'/('인사.'+뒷부분)),'-o',str(kjørbar_fil)])
            Utfør_kommando('korean-'+뒷부분,kjørbar_fil,[],'posix-kor 호출')
        kjørbar_fil=KR_data/'strøm_VERDI.elf'
        subprocess.check_call(['python3',str(utviklingspakke/'compile.py'),str(utviklingspakke/'examples/strøm_VERDI.c'),'-o',str(kjørbar_fil)])
        Utfør_kommando('c-stream-queues',kjørbar_fil,[],'C posix-kor 연결형 통신 PASS')
        Utfør_kommando('korean-python',speile_rot/'예제/한글코딩/인사.py',['--include',str(speile_rot/'예제/한글코딩/norsk.py')],'안녕하세요 누리')
        Utfør_kommando('guest-korean-javac',speile_rot/'예제/한글코딩/인사.java',[],'안녕하세요 · total_VERDI=42')
        validering_rapport['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_data/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Kjør_2()
