#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल

def चलाएँ():
    परिणाम_डेटा=प्रोजेक्ट_करें_मूल/'build/verification/coding';परिणाम_डेटा.mkdir(parents=True,exist_ok=True)
    प्रमाणीकरण_रिपोर्ट={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रोजेक्ट_करें_मूल/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(प्रोजेक्ट_करें_मूल/'उपकरण/निर्यात_करें_सॉफ़्टवेयर_डेवलपमेंट_किट.py')])
        with tarfile.open(str(प्रोजेक्ट_करें_मूल/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(परिणाम_डेटा))
        डेवलपमेंट_किट=परिणाम_डेटा/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(डेवलपमेंट_किट/'lib/libposix-kor-user.a')]).decode()
        for नाम in ('बनाएँ_एंडपॉइंट','बाइंड_करें_पता','자료전문보내기','자료전문받기','जारी_फ़ाइल','पढें_फ़ाइल_डेटा','लिखना_फ़ाइल_डेटा'):
            assert ' T '+नाम+'\n' in 심볼목록, नाम
        (परिणाम_डेटा/'korean-function-symbols.txt').write_text(심볼목록)
        प्रमाणीकरण_रिपोर्ट['checks'].append('real-korean-c-function-symbols')
        def निष्पादित_करें_आदेश(नाम,पथ,तर्क_सरणी,예상결과):
            डेटा_पद=subprocess.run(['python3',str(प्रोजेक्ट_करें_मूल/'उपकरण/निष्पादित_करें_फ़ाइल.py'),str(पथ)]+तर्क_सरणी,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (परिणाम_डेटा/(नाम+'.log')).write_bytes(डेटा_पद.stdout);assert डेटा_पद.returncode==0,डेटा_पद.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in डेटा_पद.stdout,डेटा_पद.stdout;प्रमाणीकरण_रिपोर्ट['checks'].append(नाम)
        for 뒷부분 in ('c','cpp'):
            निष्पादन_योग्य_फ़ाइल=परिणाम_डेटा/('अभिनन्दन_ae353e94-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(डेवलपमेंट_किट/'compile.py'),str(डेवलपमेंट_किट/'examples'/('अभिनन्दन_ae353e94.'+뒷부분)),'-o',str(निष्पादन_योग्य_फ़ाइल)])
            निष्पादित_करें_आदेश('korean-'+뒷부분,निष्पादन_योग्य_फ़ाइल,[],'posix-kor 호출')
        निष्पादन_योग्य_फ़ाइल=परिणाम_डेटा/'स्ट्रीम_मान.elf'
        subprocess.check_call(['python3',str(डेवलपमेंट_किट/'compile.py'),str(डेवलपमेंट_किट/'examples/स्ट्रीम_मान.c'),'-o',str(निष्पादन_योग्य_फ़ाइल)])
        निष्पादित_करें_आदेश('c-stream-queues',निष्पादन_योग्य_फ़ाइल,[],'C posix-kor 연결형 통신 PASS')
        निष्पादित_करें_आदेश('korean-python',प्रोजेक्ट_करें_मूल/'예제/한글코딩/अभिनन्दन_ae353e94.py',['--include',str(प्रोजेक्ट_करें_मूल/'예제/한글코딩/हिंदी.py')],'안녕하세요 누리')
        निष्पादित_करें_आदेश('guest-korean-javac',प्रोजेक्ट_करें_मूल/'예제/한글코딩/अभिनन्दन_ae353e94.java',[],'안녕하세요 · 합계=42')
        प्रमाणीकरण_रिपोर्ट['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(परिणाम_डेटा/'report.json').write_text(json.dumps(प्रमाणीकरण_रिपोर्ट,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':चलाएँ()
