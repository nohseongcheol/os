#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from laksanakan_perintah import projek_akar

def Jalan():
    ukuran_data=projek_akar/'build/verification/coding';ukuran_data.mkdir(parents=True,exist_ok=True)
    pensahihan_lapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projek_akar/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(projek_akar/'alat/Eksport_SDK.py')])
        with tarfile.open(str(projek_akar/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(ukuran_data))
        개발꾸러미=ukuran_data/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Nama in ('cipta_peserta','ikat_e_mel','자료전문보내기','자료전문받기','buka_fail','파일자료읽기','tulis_fail_data'):
            assert ' T '+Nama+'\n' in 심볼목록, Nama
        (ukuran_data/'korean-function-symbols.txt').write_text(심볼목록)
        pensahihan_lapor['checks'].append('real-korean-c-function-symbols')
        def laksanakan_perintah(Nama,LALUAN,argumen_ARRAY,예상결과):
            data_jawatan=subprocess.run(['python3',str(projek_akar/'alat/laksanakan_fail.py'),str(LALUAN)]+argumen_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (ukuran_data/(Nama+'.log')).write_bytes(data_jawatan.stdout);assert data_jawatan.returncode==0,data_jawatan.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in data_jawatan.stdout,data_jawatan.stdout;pensahihan_lapor['checks'].append(Nama)
        for 뒷부분 in ('c','cpp'):
            fail_boleh_laku=ukuran_data/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(fail_boleh_laku)])
            laksanakan_perintah('korean-'+뒷부분,fail_boleh_laku,[],'posix-kor 호출')
        fail_boleh_laku=ukuran_data/'strim_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/strim_VALUE.c'),'-o',str(fail_boleh_laku)])
        laksanakan_perintah('c-stream-queues',fail_boleh_laku,[],'C posix-kor 연결형 통신 PASS')
        laksanakan_perintah('korean-python',projek_akar/'예제/한글코딩/인사.py',['--include',str(projek_akar/'예제/한글코딩/Melayu.py')],'안녕하세요 누리')
        laksanakan_perintah('guest-korean-javac',projek_akar/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        pensahihan_lapor['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(ukuran_data/'report.json').write_text(json.dumps(pensahihan_lapor,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Jalan()
