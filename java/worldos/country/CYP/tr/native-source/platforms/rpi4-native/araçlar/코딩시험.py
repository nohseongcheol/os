#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from yürütmek_komut import işlem_kök

def çalıştır():
    KR_veri=işlem_kök/'build/verification/coding';KR_veri.mkdir(parents=True,exist_ok=True)
    doğrulama_Rapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((işlem_kök/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(işlem_kök/'araçlar/dışarı_aktarmak_SDK.py')])
        with tarfile.open(str(işlem_kök/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_veri))
        geliştirme_seti=KR_veri/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(geliştirme_seti/'lib/libposix-kor-user.a')]).decode()
        for İsim in ('açmak_uç_nokta','BIND_ADRES','göndermek_veri_birimi_veri','almak_veri_birimi_veri','açık_Dosya','파일자료읽기','yazma_Dosya_veri'):
            assert ' T '+İsim+'\n' in 심볼목록, İsim
        (KR_veri/'korean-function-symbols.txt').write_text(심볼목록)
        doğrulama_Rapor['checks'].append('real-korean-c-function-symbols')
        def yürütmek_komut(İsim,yol,bağımsız_değişken_DİZİ,예상결과):
            veri_konum=subprocess.run(['python3',str(işlem_kök/'araçlar/yürütmek_Dosya.py'),str(yol)]+bağımsız_değişken_DİZİ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_veri/(İsim+'.log')).write_bytes(veri_konum.stdout);assert veri_konum.returncode==0,veri_konum.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in veri_konum.stdout,veri_konum.stdout;doğrulama_Rapor['checks'].append(İsim)
        for 뒷부분 in ('c','cpp'):
            çalıştırılabilir=KR_veri/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(geliştirme_seti/'compile.py'),str(geliştirme_seti/'examples'/('인사.'+뒷부분)),'-o',str(çalıştırılabilir)])
            yürütmek_komut('korean-'+뒷부분,çalıştırılabilir,[],'posix-kor 호출')
        çalıştırılabilir=KR_veri/'akış_değer.elf'
        subprocess.check_call(['python3',str(geliştirme_seti/'compile.py'),str(geliştirme_seti/'examples/akış_değer.c'),'-o',str(çalıştırılabilir)])
        yürütmek_komut('c-stream-queues',çalıştırılabilir,[],'C posix-kor 연결형 iletişim PASS')
        yürütmek_komut('korean-python',işlem_kök/'예제/한글코딩/인사.py',['--include',str(işlem_kök/'예제/한글코딩/Türkçe.py')],'안녕하세요 누리')
        yürütmek_komut('guest-korean-javac',işlem_kök/'예제/한글코딩/인사.java',[],'안녕하세요 · toplam_değer=42')
        doğrulama_Rapor['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_veri/'report.json').write_text(json.dumps(doğrulama_Rapor,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':çalıştır()
