#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Provést_příkaz import akce_kořen

def Spustit_2():
    KV_data=akce_kořen/'build/verification/coding';KV_data.mkdir(parents=True,exist_ok=True)
    ověření_Zpráva={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akce_kořen/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(akce_kořen/'nástroje/exportovat_sada_SDK.py')])
        with tarfile.open(str(akce_kořen/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KV_data))
        Development_Kit=KV_data/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(Development_Kit/'lib/libposix-kor-user.a')]).decode()
        for Název in ('Create_účastník','vázat_ODKAZ','poslat_datagram_data','dostat_datagram_data','otevřít_Soubor','파일자료읽기','zápis_Soubor_data'):
            assert ' T '+Název+'\n' in 심볼목록, Název
        (KV_data/'korean-function-symbols.txt').write_text(심볼목록)
        ověření_Zpráva['checks'].append('real-korean-c-function-symbols')
        def Provést_příkaz(Název,cesta_2,argument_pole,예상결과):
            data_pozice=subprocess.run(['python3',str(akce_kořen/'nástroje/Provést_Soubor.py'),str(cesta_2)]+argument_pole,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KV_data/(Název+'.log')).write_bytes(data_pozice.stdout);assert data_pozice.returncode==0,data_pozice.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in data_pozice.stdout,data_pozice.stdout;ověření_Zpráva['checks'].append(Název)
        for 뒷부분 in ('c','cpp'):
            spustitelný_soubor=KV_data/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(Development_Kit/'compile.py'),str(Development_Kit/'examples'/('인사.'+뒷부분)),'-o',str(spustitelný_soubor)])
            Provést_příkaz('korean-'+뒷부분,spustitelný_soubor,[],'posix-kor 호출')
        spustitelný_soubor=KV_data/'tok_HODNOTA.elf'
        subprocess.check_call(['python3',str(Development_Kit/'compile.py'),str(Development_Kit/'examples/tok_HODNOTA.c'),'-o',str(spustitelný_soubor)])
        Provést_příkaz('c-stream-queues',spustitelný_soubor,[],'C posix-kor 연결형 komunikace PASS')
        Provést_příkaz('korean-python',akce_kořen/'예제/한글코딩/인사.py',['--include',str(akce_kořen/'예제/한글코딩/čeština.py')],'안녕하세요 누리')
        Provést_příkaz('guest-korean-javac',akce_kořen/'예제/한글코딩/인사.java',[],'안녕하세요 · celkem_HODNOTA=42')
        ověření_Zpráva['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KV_data/'report.json').write_text(json.dumps(ověření_Zpráva,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Spustit_2()
