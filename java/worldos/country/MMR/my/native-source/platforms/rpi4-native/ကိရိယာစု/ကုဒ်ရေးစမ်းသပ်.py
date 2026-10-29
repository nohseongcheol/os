#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from စက်မောင်း import စီမံကိန်းအမြစ်

def လုပ်ဆောင်():
    ရလဒ်ဒေတာ=စီမံကိန်းအမြစ်/'build/verification/coding';ရလဒ်ဒေတာ.mkdir(parents=True,exist_ok=True)
    검증기록={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((စီမံကိန်းအမြစ်/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(စီမံကိန်းအမြစ်/'ကိရိယာစု/개발꾸러미내보내기.py')])
        with tarfile.open(str(စီမံကိန်းအမြစ်/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(ရလဒ်ဒေတာ))
        개발꾸러미=ရလဒ်ဒေတာ/'jkoros-native-sdk'
        သင်္ကေတများစာရင်း=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for အမည် in ('အဆုံးမှတ်ဖန်တီး','လိပ်စာချည်နှောင်','ဒေတာစာဒေတာပို့','ဒေတာစာဒေတာလက်ခံရယူ','ဖိုင်ဖွင့်','ဖိုင်ဒေတာဖတ်','ဖိုင်ဒေတာရေး'):
            assert ' T '+အမည်+'\n' in သင်္ကေတများစာရင်း, အမည်
        (ရလဒ်ဒေတာ/'korean-function-symbols.txt').write_text(သင်္ကေတများစာရင်း)
        검증기록['checks'].append('real-korean-c-function-symbols')
        def စက်မောင်း(အမည်,လမ်း,ပေးအချက်အခင်းအကျင်း,예상결과):
            ဒေတာနေရာ=subprocess.run(['python3',str(စီမံကိန်းအမြစ်/'ကိရိယာစု/ဖိုင်လုပ်ဆောင်.py'),str(လမ်း)]+ပေးအချက်အခင်းအကျင်း,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (ရလဒ်ဒေတာ/(အမည်+'.log')).write_bytes(ဒေတာနေရာ.stdout);assert ဒေတာနေရာ.returncode==0,ဒေတာနေရာ.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in ဒေတာနေရာ.stdout,ဒေတာနေရာ.stdout;검증기록['checks'].append(အမည်)
        for 뒷부분 in ('c','cpp'):
            စက်ဖိုင်ဖိုင်=ရလဒ်ဒေတာ/('နှုတ်ဆက်-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('နှုတ်ဆက်.'+뒷부분)),'-o',str(စက်ဖိုင်ဖိုင်)])
            စက်မောင်း('korean-'+뒷부분,စက်ဖိုင်ဖိုင်,[],'posix-kor ခေါ်လုပ်')
        စက်ဖိုင်ဖိုင်=ရလဒ်ဒေတာ/'စီးကြောင်းတန်ဖိုး.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/စီးကြောင်းတန်ဖိုး.c'),'-o',str(စက်ဖိုင်ဖိုင်)])
        စက်မောင်း('c-stream-queues',စက်ဖိုင်ဖိုင်,[],'C posix-kor 연결형 ဆက်သွယ်မှု PASS')
        စက်မောင်း('korean-python',စီမံကိန်းအမြစ်/'ဥပမာ/ဟန်ဂုကုဒ်ရေး/နှုတ်ဆက်.py',['--include',str(စီမံကိန်းအမြစ်/'ဥပမာ/ဟန်ဂုကုဒ်ရေး/မြန်မာ.py')],'안녕하세요 누리')
        စက်မောင်း('guest-korean-javac',စီမံကိန်းအမြစ်/'ဥပမာ/ဟန်ဂုကုဒ်ရေး/နှုတ်ဆက်.java',[],'안녕하세요 · အကုန်စုစုပေါင်းတန်ဖိုး=42')
        검증기록['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(ရလဒ်ဒေတာ/'report.json').write_text(json.dumps(검증기록,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':လုပ်ဆောင်()
