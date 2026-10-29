#!/usr/bin/env python3
"""ကိုယ်ပိုင် 커널의 အမိန့်ဝင်း, 프로세스 အဝင်အထွက်, Unicode GUI 터미널을 တကယ့်ဒေတာ raspi4b에서 စမ်းသပ်မှု."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from စက်မောင်း import စီမံကိန်းအမြစ်, အမိန့်


def လုပ်ဆောင်():
    출력결과 = စီမံကိန်းအမြစ် / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    검증기록 = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((စီမံကိန်းအမြစ် / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as လုပ်ဆောင်လမ်း:
        모의제어접속 = Path(လုပ်ဆောင်လမ်း) / 'qmp.sock'
        실행과정 = subprocess.Popen(အမိန့်()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(실행과정.stdout,selectors.EVENT_READ)
        def စာပို့ချက်လက်ခံရယူ(확인표시, လုပ်ဆောင်မှုအချိန်လွန်=45):
            ဒေတာ=bytearray(); အဆုံးအရွေ့=time.monotonic()+လုပ်ဆောင်မှုအချိန်လွန်
            while 확인표시 not in ဒေတာ:
                if time.monotonic()>အဆုံးအရွေ့ or 실행과정.poll() is not None: raise AssertionError('UART timeout/exit: '+ဒေတာ.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    အစိတ်အပိုင်း=누름값.fileobj.read(4096)
                    if အစိတ်အပိုင်း: ဒေတာ.extend(အစိတ်အပိုင်း); 대화기록.extend(အစိတ်အပိုင်း)
                if b'PANIC:' in ဒေတာ or b'FAIL ' in ဒေတာ: raise AssertionError(ဒေတာ)
            return ဒေတာ.decode('utf-8','replace').replace('\r\n','\n')
        def ပို့(ဒေတာ, 확인표시=b'jkoros-native> '):
            실행과정.stdin.write(ဒေတာ); 실행과정.stdin.flush(); return စာပို့ချက်လက်ခံရယူ(확인표시)
        def အမိန့်ဝင်း(စာကြောင်း, *예상결과):
            ရလဒ်=ပို့(စာကြောင်း.encode()+b'\n')
            for တန်ဖိုး in 예상결과: assert တန်ဖိုး in ရလဒ်, (စာကြောင်း,တန်ဖိုး,ရလဒ်)
            return ရလဒ်
        def ဖိုင်(အမည်):
            စာသား=အမိန့်ဝင်း('hex '+အမည်,'HEX BEGIN','HEX END'); ရလဒ်ရှာဖွေ=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',စာသား,re.S)
            ဒေတာ=bytes.fromhex(''.join(ရလဒ်ရှာဖွေ.group(2).split())); assert len(ဒေတာ)==int(ရလဒ်ရှာဖွေ.group(1)); return ဒေတာ
        try:
            စာပို့ချက်လက်ခံရယူ(b'jkoros-native> ')
            အမိန့်ဝင်း('mkdir အလုပ်; cd အလုပ်; pwd','/အလုပ်')
            အမိန့်ဝင်း('mkdir 하위; echo "한글 ဒေတာ 😀" > နှုတ်ဆက်.txt')
            assert ဖိုင်('နှုတ်ဆက်.txt')=='한글 ဒေတာ 😀\n'.encode()
            အမိန့်ဝင်း('cp နှုတ်ဆက်.txt တန်ဖိုးမိတ္တူကူး.txt; mv တန်ဖိုးမိတ္တူကူး.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ဒေတာ 😀')
            အမိန့်ဝင်း('cd 하위; cat ../နှုတ်ဆက်.txt; cat /အလုပ်/နှုတ်ဆက်.txt; pwd','한글 ဒေတာ 😀','/အလုပ်/하위')
            အမိန့်ဝင်း('cd ..; rmdir 하위; echo $?','1\n')
            အမိန့်ဝင်း('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            အမိန့်ဝင်း('cp နှုတ်ဆက်.txt နှုတ်ဆက်.txt; echo $?','1\n'); assert ဖိုင်('နှုတ်ဆက်.txt')=='한글 ဒေတာ 😀\n'.encode()
            အမိန့်ဝင်း('export နှုတ်ဆက်=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/အလုပ်','GOOD')
            assert b'BAD\n' not in ဖိုင်('နှုတ်ဆက်.txt')
            အမိန့်ဝင်း("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ဖိုင်('리터럴')=='$인사\n누리\n'.encode()
            အမိန့်ဝင်း('echo one > အမိန့်ကြောင်းတန်ဖိုး; echo two >> အမိန့်ကြောင်းတန်ဖိုး; echo three >> အမိန့်ကြောင်းတန်ဖိုး')
            အမိန့်ဝင်း('cat < အမိန့်ကြောင်းတန်ဖိုး | grep t | tee 추림 | wc -l','2\n'); assert ဖိုင်('추림')==b'two\nthree\n'
            အမိန့်ဝင်း('head -n 1 အမိန့်ကြောင်းတန်ဖိုး > ရှေ့တန်ဖိုး; tail -n 1 အမိန့်ကြောင်းတန်ဖိုး > နောက်တန်ဖိုး'); assert ဖိုင်('앞')==b'one\n'; assert ဖိုင်('뒤')==b'three\n'
            အမိန့်ဝင်း('grep absent အမိန့်ကြောင်းတန်ဖိုး; echo $?','1\n')
            အမိန့်ဝင်း('echo untouched > တန်ဖိုးကာကွယ်')
            အမိန့်ဝင်း('echo destroyed > တန်ဖိုးကာကွယ် |','명령이 빠졌습니다'); assert ဖိုင်('တန်ဖိုးကာကွယ်')==b'untouched\n'
            အမိန့်ဝင်း('echo "oops','따옴표가 닫히지 않았습니다')
            အမိန့်ဝင်း('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            အမိန့်ဝင်း('echo bad 2> တန်ဖိုးကာကွယ်','번호를 지정한 ဖိုင် အညွှန်း အဝင်အထွက် အလှည့်ပြောင်းနည်းစနစ်'); assert ဖိုင်('တန်ဖိုးကာကွယ်')==b'untouched\n'
            အမိန့်ဝင်း('rm 빈파일 리터럴 အမိန့်ကြောင်းတန်ဖိုး 추림 ရှေ့တန်ဖိုး နောက်တန်ဖိုး တန်ဖိုးကာကွယ်')
            검증기록['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            အမိန့်ဝင်း("python -c 'print(123)' | wc -c",'4\n')
            အမိန့်ဝင်း("python -c 'print(456)' > ပရိုဂရမ်.txt"); assert ဖိုင်('ပရိုဂရမ်.txt')==b'456\n'
            အမိန့်ဝင်း("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            အမိန့်ဝင်း("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ပရိုဂရမ်.txt", "b'456\\n'", "b''")
            အမိန့်ဝင်း("python -c 'print(\"x\"*17000)' | wc -c", 'အမှား -28')
            အမိန့်ဝင်း('echo recovered | wc -c','10\n')
            အမိန့်ဝင်း("python -c 'import jkoros; print(jkoros.read("+'"/အလုပ်/ပရိုဂရမ်.txt"'+"))'",'456','exit 0')
            အမိန့်ဝင်း('cd /; javac Hello.java','Compiled:','exit 0')
            အမိန့်ဝင်း('java Hello > /အလုပ်/Java.txt'); assert '안녕하세요'.encode() in ဖိုင်('/အလုပ်/Java.txt')
            အမိန့်ဝင်း('cd အလုပ်; echo "echo script > လုပ်ဆောင်မှုရလဒ်" > အမိန့်.sh; echo "false || echo recovered >> လုပ်ဆောင်မှုရလဒ်" >> အမိန့်.sh; sh အမိန့်.sh')
            assert ဖိုင်('လုပ်ဆောင်မှုရလဒ်')==b'script\nrecovered\n'
            အမိန့်ဝင်း('rm လုပ်ဆောင်မှုရလဒ်; echo "exit 7" > ထွက်ပရိုဂရမ်.sh; sh ထွက်ပရိုဂရမ်.sh; echo $?','7\n')
            အမိန့်ဝင်း('rm ထွက်ပရိုဂရမ်.sh အမိန့်.sh ပရိုဂရမ်.txt Java.txt နှုတ်ဆက်.txt; cd /; rmdir အလုပ်')
            검증기록['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            အမိန့်ဝင်း('echo history-proof','history-proof')
            ရလဒ်=ပို့(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert ရလဒ်.count('history-proof')>=2, ရလဒ်
            ပို့(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            ရလဒ်=ပို့(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in ရလဒ်, ရလဒ်
            ရလဒ်=ပို့(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in ရလဒ်,ရလဒ်
            ရလဒ်=ပို့('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in ရလဒ်,ရလဒ်
            ရှည်စာသား='한글'*50
            ရလဒ်=ပို့(('echo '+ရှည်စာသား+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+ရှည်စာသား+'\r\njkoros-native> ').encode()); assert '\n'+ရှည်စာသား+'\n' in ရလဒ်
            အမိန့်ဝင်း('terminal','TERMINAL READY')
            အမိန့်ဝင်း('clear')
            အမိန့်ဝင်း('echo "한글 အဆုံးသုံးမျက်နှာပြင် ABC xyz 012 😀"','한글 အဆုံးသုံးမျက်နှာပြင် ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as လက်ခံစက်:
                လက်ခံစက်.settimeout(10); လက်ခံစက်.connect(str(모의제어접속))
                with လက်ခံစက်.makefile('rwb') as စီးကြောင်းတန်ဖိုး:
                    json.loads(စီးကြောင်းတန်ဖိုး.readline())
                    def ခေါ်လုပ်(အမည်,ပေးအချက်အခင်းအကျင်း=None):
                        ကွန်ရက်စာ={'execute':အမည်}
                        if ပေးအချက်အခင်းအကျင်း: ကွန်ရက်စာ['arguments']=ပေးအချက်အခင်းအကျင်း
                        စီးကြောင်းတန်ဖိုး.write((json.dumps(ကွန်ရက်စာ)+'\n').encode()); စီးကြောင်းတန်ဖိုး.flush()
                        while True:
                            အကြောင်းပြန်ချက်=json.loads(စီးကြောင်းတန်ဖိုး.readline())
                            if 'error' in အကြောင်းပြန်ချက်: raise AssertionError(အကြောင်းပြန်ချက်)
                            if 'return' in အကြောင်းပြန်ချက်: return အကြောင်းပြန်ချက်['return']
                    ခေါ်လုပ်('qmp_capabilities')
                    စက်ကုဒ်ပုံရိပ်=출력결과/'terminal.ppm'; ခေါ်လုပ်('screendump',{'filename':str(စက်ကုဒ်ပုံရိပ်),'format':'ppm'})
                    ခေါ်လုပ်('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    ဒေတာ=စက်ကုဒ်ပုံရိပ်.read_bytes().split(b'\n',3)[3]
                    def ပုံမှတ်(xတည်နေရာအမှတ်,yတည်နေရာအမှတ်): return tuple(ဒေတာ[(yတည်နေရာအမှတ်*640+xတည်နေရာအမှတ်)*3:(yတည်နေရာအမှတ်*640+xတည်နေရာအမှတ်)*3+3])
                    assert ပုံမှတ်(12,48)==(32,80,144),ပုံမှတ်(12,48)
                    assert len(set(ပုံမှတ်(xတည်နေရာအမှတ်,yတည်နေရာအမှတ်) for yတည်နေရာအမှတ် in range(100,116) for xတည်နေရာအမှတ် in range(24,56)))>1,'Hangul glyphs missing'
                    အမိန့်ဝင်း('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    အမိန့်ဝင်း("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    ခေါ်လုပ်('screendump',{'filename':str(စက်ကုဒ်ပုံရိပ်),'format':'ppm'})
                    복원자료=စက်ကုဒ်ပုံရိပ်.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    အမိန့်ဝင်း('echo test > visible.txt; cat visible.txt','test')
                    for အစဉ်အမှတ် in range(27): အမိန့်ဝင်း('echo scroll-'+str(အစဉ်အမှတ်),'scroll-'+str(အစဉ်အမှတ်))
                    ပို့(b'\x1b[5~\x1b[6~\n')
                    ခေါ်လုပ်('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    ရလဒ်=ပို့(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in ရလဒ်,ရလဒ်
                    အမိန့်ဝင်း('rm visible.txt')
                    ခေါ်လုပ်('quit')
            실행과정.wait(timeout=5)
            검증기록['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            검증기록['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if 실행과정.poll() is None:
                실행과정.terminate()
                try: 실행과정.wait(timeout=5)
                except subprocess.TimeoutExpired: 실행과정.kill(); 실행과정.wait()
            준비살피미.close(); 실행과정.stdin.close(); 실행과정.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(검증기록,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': လုပ်ဆောင်()
