#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from ፈጽም_ትእዛዝ import አሳይ_ስር

def ማስኬጃ():
    ልኬት_ውሂብ=አሳይ_ስር/'build/verification/coding';ልኬት_ውሂብ.mkdir(parents=True,exist_ok=True)
    ማረጋገጥ_ዘገባ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((አሳይ_ስር/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(አሳይ_ስር/'መሳሪያዎች/개발꾸러미내보내기.py')])
        with tarfile.open(str(አሳይ_ስር/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(ልኬት_ውሂብ))
        개발꾸러미=ልኬት_ውሂብ/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for ስም in ('통신종단점만들기','አጣምር_አድራሻ','자료전문보내기','자료전문받기','ክፈት_ፋይል','파일자료읽기','ጻፍ_ፋይል_ውሂብ'):
            assert ' T '+ስም+'\n' in 심볼목록, ስም
        (ልኬት_ውሂብ/'korean-function-symbols.txt').write_text(심볼목록)
        ማረጋገጥ_ዘገባ['checks'].append('real-korean-c-function-symbols')
        def ፈጽም_ትእዛዝ(ስም,መተላለፊያ,ነጋሪ_እሴት_ድርድር,예상결과):
            ውሂብ_በቦታ_አስቀመጠ=subprocess.run(['python3',str(አሳይ_ስር/'መሳሪያዎች/ፈጽም_ፋይል.py'),str(መተላለፊያ)]+ነጋሪ_እሴት_ድርድር,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (ልኬት_ውሂብ/(ስም+'.log')).write_bytes(ውሂብ_በቦታ_አስቀመጠ.stdout);assert ውሂብ_በቦታ_አስቀመጠ.returncode==0,ውሂብ_በቦታ_አስቀመጠ.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in ውሂብ_በቦታ_አስቀመጠ.stdout,ውሂብ_በቦታ_አስቀመጠ.stdout;ማረጋገጥ_ዘገባ['checks'].append(ስም)
        for 뒷부분 in ('c','cpp'):
            실행파일=ልኬት_ውሂብ/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            ፈጽም_ትእዛዝ('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=ልኬት_ውሂብ/'ልቀቅ_እሴት.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/ልቀቅ_እሴት.c'),'-o',str(실행파일)])
        ፈጽም_ትእዛዝ('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        ፈጽም_ትእዛዝ('korean-python',አሳይ_ስር/'예제/한글코딩/인사.py',['--include',str(አሳይ_ስር/'예제/한글코딩/አማርኛ.py')],'안녕하세요 누리')
        ፈጽም_ትእዛዝ('guest-korean-javac',አሳይ_ስር/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        ማረጋገጥ_ዘገባ['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(ልኬት_ውሂብ/'report.json').write_text(json.dumps(ማረጋገጥ_ዘገባ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ማስኬጃ()
