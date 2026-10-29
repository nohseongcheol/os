#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Udfør_kommando import To_do_rod

def Kør_2():
    KR_data=To_do_rod/'build/verification/coding';KR_data.mkdir(parents=True,exist_ok=True)
    validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((To_do_rod/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(To_do_rod/'Værktøjer/eksportere_SDK.py')])
        with tarfile.open(str(To_do_rod/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_data))
        Development_Kit=KR_data/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(Development_Kit/'lib/libposix-kor-user.a')]).decode()
        for Navn in ('åbne_slutpunkt','BIND_mail','maile_datagram_data','modtage_datagram_data','åben_fil','파일자료읽기','skrive_fil_data'):
            assert ' T '+Navn+'\n' in 심볼목록, Navn
        (KR_data/'korean-function-symbols.txt').write_text(심볼목록)
        validering_rapport['checks'].append('real-korean-c-function-symbols')
        def Udfør_kommando(Navn,Sti,argument_MATRIX,예상결과):
            data_placere=subprocess.run(['python3',str(To_do_rod/'Værktøjer/Udfør_fil.py'),str(Sti)]+argument_MATRIX,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_data/(Navn+'.log')).write_bytes(data_placere.stdout);assert data_placere.returncode==0,data_placere.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in data_placere.stdout,data_placere.stdout;validering_rapport['checks'].append(Navn)
        for 뒷부분 in ('c','cpp'):
            eksekverbar_fil=KR_data/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(Development_Kit/'compile.py'),str(Development_Kit/'examples'/('인사.'+뒷부분)),'-o',str(eksekverbar_fil)])
            Udfør_kommando('korean-'+뒷부분,eksekverbar_fil,[],'posix-kor 호출')
        eksekverbar_fil=KR_data/'strøm_VÆRDI.elf'
        subprocess.check_call(['python3',str(Development_Kit/'compile.py'),str(Development_Kit/'examples/strøm_VÆRDI.c'),'-o',str(eksekverbar_fil)])
        Udfør_kommando('c-stream-queues',eksekverbar_fil,[],'C posix-kor 연결형 통신 PASS')
        Udfør_kommando('korean-python',To_do_rod/'예제/한글코딩/인사.py',['--include',str(To_do_rod/'예제/한글코딩/Dansk.py')],'안녕하세요 누리')
        Udfør_kommando('guest-korean-javac',To_do_rod/'예제/한글코딩/인사.java',[],'안녕하세요 · i_alt_VÆRDI=42')
        validering_rapport['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_data/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Kør_2()
