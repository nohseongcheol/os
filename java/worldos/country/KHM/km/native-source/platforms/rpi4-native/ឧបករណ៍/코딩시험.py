#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស

def រត់():
    ការវាស់វែង_ទិន្នន័យ=បញ្ចាំង_ឬស/'build/verification/coding';ការវាស់វែង_ទិន្នន័យ.mkdir(parents=True,exist_ok=True)
    សុពលភាព_រាយការណ៍={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((បញ្ចាំង_ឬស/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(បញ្ចាំង_ឬស/'ឧបករណ៍/개발꾸러미내보내기.py')])
        with tarfile.open(str(បញ្ចាំង_ឬស/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(ការវាស់វែង_ទិន្នន័យ))
        개발꾸러미=ការវាស់វែង_ទិន្នន័យ/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for ឈ្មោះ in ('통신종단점만들기','ចង_អ៊ីម៉ែល','자료전문보내기','자료전문받기','បើក_ឯកសារ','파일자료읽기','សរសេរ_ឯកសារ_ទិន្នន័យ'):
            assert ' T '+ឈ្មោះ+'\n' in 심볼목록, ឈ្មោះ
        (ការវាស់វែង_ទិន្នន័យ/'korean-function-symbols.txt').write_text(심볼목록)
        សុពលភាព_រាយការណ៍['checks'].append('real-korean-c-function-symbols')
        def អនុវត្ត_ពាក្យបញ្ជា(ឈ្មោះ,ផ្លូវ,អាគុយម៉ង់_អារេ,예상결과):
            ទិន្នន័យ_កំណត់ទីតាំង=subprocess.run(['python3',str(បញ្ចាំង_ឬស/'ឧបករណ៍/អនុវត្ត_ឯកសារ.py'),str(ផ្លូវ)]+អាគុយម៉ង់_អារេ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (ការវាស់វែង_ទិន្នន័យ/(ឈ្មោះ+'.log')).write_bytes(ទិន្នន័យ_កំណត់ទីតាំង.stdout);assert ទិន្នន័យ_កំណត់ទីតាំង.returncode==0,ទិន្នន័យ_កំណត់ទីតាំង.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in ទិន្នន័យ_កំណត់ទីតាំង.stdout,ទិន្នន័យ_កំណត់ទីតាំង.stdout;សុពលភាព_រាយការណ៍['checks'].append(ឈ្មោះ)
        for 뒷부분 in ('c','cpp'):
            실행파일=ការវាស់វែង_ទិន្នន័យ/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            អនុវត្ត_ពាក្យបញ្ជា('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=ការវាស់វែង_ទិន្នន័យ/'ស្ទ្រីម_តំលៃ.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/ស្ទ្រីម_តំលៃ.c'),'-o',str(실행파일)])
        អនុវត្ត_ពាក្យបញ្ជា('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        អនុវត្ត_ពាក្យបញ្ជា('korean-python',បញ្ចាំង_ឬស/'예제/한글코딩/인사.py',['--include',str(បញ្ចាំង_ឬស/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        អនុវត្ត_ពាក្យបញ្ជា('guest-korean-javac',បញ្ចាំង_ឬស/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        សុពលភាព_រាយការណ៍['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(ការវាស់វែង_ទិន្នន័យ/'report.json').write_text(json.dumps(សុពលភាព_រាយការណ៍,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':រត់()
