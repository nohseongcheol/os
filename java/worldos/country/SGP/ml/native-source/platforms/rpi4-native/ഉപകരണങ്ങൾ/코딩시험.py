#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം

def നടപ്പിലാക്കുക():
    അളവ്_ഡാറ്റാ=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/coding';അളവ്_ഡാറ്റാ.mkdir(parents=True,exist_ok=True)
    నిర్ధారణ_నివేదిక={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉപകരണങ്ങൾ/개발꾸러미내보내기.py')])
        with tarfile.open(str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(അളവ്_ഡാറ്റാ))
        개발꾸러미=അളവ്_ഡാറ്റാ/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for പേരു് in ('സൃഷ്_ടിക്കുക_അവസാനബിന്ദു','బైండ్_చేయి_ഇമെയിൽ','자료전문보내기','자료전문받기','തുറക്കുക_ഫയല്','파일자료읽기','റൈറ്റ്_ചെയ്യുക_ഫയല്_ഡാറ്റാ'):
            assert ' T '+പേരു്+'\n' in 심볼목록, പേരു്
        (അളവ്_ഡാറ്റാ/'korean-function-symbols.txt').write_text(심볼목록)
        నిర్ధారణ_నివేదిక['checks'].append('real-korean-c-function-symbols')
        def നടപ്പാക്കുക_കമാന്_ഡ്(പേരു്,വഴി,ആര്_ഗ്യുമെന്_റ്_അരേ,예상결과):
            ഡാറ്റാ_പദവി=subprocess.run(['python3',str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉപകരണങ്ങൾ/നടപ്പാക്കുക_ഫയല്.py'),str(വഴി)]+ആര്_ഗ്യുമെന്_റ്_അരേ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (അളവ്_ഡാറ്റാ/(പേരു്+'.log')).write_bytes(ഡാറ്റാ_പദവി.stdout);assert ഡാറ്റാ_പദവി.returncode==0,ഡാറ്റാ_പദവി.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in ഡാറ്റാ_പദവി.stdout,ഡാറ്റാ_പദവി.stdout;నిర్ధారణ_నివేదిక['checks'].append(പേരു്)
        for 뒷부분 in ('c','cpp'):
            നിര്_വ്വഹണക്ഷമമായ_ഫയല്=അളവ്_ഡാറ്റാ/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(നിര്_വ്വഹണക്ഷമമായ_ഫയല്)])
            നടപ്പാക്കുക_കമാന്_ഡ്('korean-'+뒷부분,നിര്_വ്വഹണക്ഷമമായ_ഫയല്,[],'posix-kor 호출')
        നിര്_വ്വഹണക്ഷമമായ_ഫയല്=അളവ്_ഡാറ്റാ/'സ്ട്രീം_മൂല്യം.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/സ്ട്രീം_മൂല്യം.c'),'-o',str(നിര്_വ്വഹണക്ഷമമായ_ഫയല്)])
        നടപ്പാക്കുക_കമാന്_ഡ്('c-stream-queues',നിര്_വ്വഹണക്ഷമമായ_ഫയല്,[],'C posix-kor 연결형 통신 PASS')
        നടപ്പാക്കുക_കമാന്_ഡ്('korean-python',പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'예제/한글코딩/인사.py',['--include',str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        നടപ്പാക്കുക_കമാന്_ഡ്('guest-korean-javac',പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        నిర్ధారణ_నివేదిక['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(അളവ്_ഡാറ്റാ/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':നടപ്പിലാക്കുക()
