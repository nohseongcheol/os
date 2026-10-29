#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Suorita_komento import aloite_juuri

def Suorita_2():
    KR_data=aloite_juuri/'build/verification/coding';KR_data.mkdir(parents=True,exist_ok=True)
    vahvistus_raportti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((aloite_juuri/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(aloite_juuri/'työkalut/viedä_SDK.py')])
        with tarfile.open(str(aloite_juuri/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_data))
        ohjelmankehityspaketti=KR_data/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(ohjelmankehityspaketti/'lib/libposix-kor-user.a')]).decode()
        for Nimi in ('Luo_päätepiste','BIND_OSOITE','lähettää_datagrammi_data','saada_datagrammi_data','avata_Tiedosto','lukea_Tiedosto_data','kirjoitus_Tiedosto_data'):
            assert ' T '+Nimi+'\n' in 심볼목록, Nimi
        (KR_data/'korean-function-symbols.txt').write_text(심볼목록)
        vahvistus_raportti['checks'].append('real-korean-c-function-symbols')
        def Suorita_komento(Nimi,polku_2,argumentti_MATRIISI,예상결과):
            data_toimi=subprocess.run(['python3',str(aloite_juuri/'työkalut/Suorita_Tiedosto.py'),str(polku_2)]+argumentti_MATRIISI,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_data/(Nimi+'.log')).write_bytes(data_toimi.stdout);assert data_toimi.returncode==0,data_toimi.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in data_toimi.stdout,data_toimi.stdout;vahvistus_raportti['checks'].append(Nimi)
        for 뒷부분 in ('c','cpp'):
            suoritettava_tiedosto=KR_data/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(ohjelmankehityspaketti/'compile.py'),str(ohjelmankehityspaketti/'examples'/('인사.'+뒷부분)),'-o',str(suoritettava_tiedosto)])
            Suorita_komento('korean-'+뒷부분,suoritettava_tiedosto,[],'posix-kor 호출')
        suoritettava_tiedosto=KR_data/'virta_ARVO.elf'
        subprocess.check_call(['python3',str(ohjelmankehityspaketti/'compile.py'),str(ohjelmankehityspaketti/'examples/virta_ARVO.c'),'-o',str(suoritettava_tiedosto)])
        Suorita_komento('c-stream-queues',suoritettava_tiedosto,[],'C posix-kor 연결형 통신 PASS')
        Suorita_komento('korean-python',aloite_juuri/'예제/한글코딩/인사.py',['--include',str(aloite_juuri/'예제/한글코딩/suomi.py')],'안녕하세요 누리')
        Suorita_komento('guest-korean-javac',aloite_juuri/'예제/한글코딩/인사.java',[],'안녕하세요 · summa_ARVO=42')
        vahvistus_raportti['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_data/'report.json').write_text(json.dumps(vahvistus_raportti,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Suorita_2()
