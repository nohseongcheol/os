#!/usr/bin/env python3
"""بومی 커널의 واسط, 프로세스 ورودی_خروجی, Unicode GUI 터미널을 واقعی_داده_ها raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from اجرا_فرمان import نمایش_دادن_جذر, فرمان


def اجرا_2():
    출력결과 = نمایش_دادن_جذر / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    اعتبارسنجی_گزارش = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((نمایش_دادن_جذر / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        فرآیند = subprocess.Popen(فرمان()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(فرآیند.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            داده_ها=bytearray(); پایان_دادن_جابجایی_لایه_ای=time.monotonic()+시간제한
            while 확인표시 not in داده_ها:
                if time.monotonic()>پایان_دادن_جابجایی_لایه_ای or فرآیند.poll() is not None: raise AssertionError('UART timeout/exit: '+داده_ها.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: داده_ها.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in داده_ها or b'FAIL ' in داده_ها: raise AssertionError(داده_ها)
            return داده_ها.decode('utf-8','replace').replace('\r\n','\n')
        def ارسال(داده_ها, 확인표시=b'jkoros-native> '):
            فرآیند.stdin.write(داده_ها); فرآیند.stdin.flush(); return 수신하기(확인표시)
        def واسط(خط, *예상결과):
            سنجش=ارسال(خط.encode()+b'\n')
            for مقدار in 예상결과: assert مقدار in سنجش, (خط,مقدار,سنجش)
            return سنجش
        def پرونده(نام):
            متن=واسط('hex '+نام,'HEX BEGIN','HEX END'); جستجو_سنجش=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',متن,re.S)
            داده_ها=bytes.fromhex(''.join(جستجو_سنجش.group(2).split())); assert len(داده_ها)==int(جستجو_سنجش.group(1)); return داده_ها
        try:
            수신하기(b'jkoros-native> ')
            واسط('mkdir 작업; cd 작업; pwd','/작업')
            واسط('mkdir 하위; echo "한글 داده_ها 😀" > 인사.txt')
            assert پرونده('인사.txt')=='한글 داده_ها 😀\n'.encode()
            واسط('cp 인사.txt کپی_مقدار.txt; mv کپی_مقدار.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 داده_ها 😀')
            واسط('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 داده_ها 😀','/작업/하위')
            واسط('cd ..; rmdir 하위; echo $?','1\n')
            واسط('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            واسط('cp 인사.txt 인사.txt; echo $?','1\n'); assert پرونده('인사.txt')=='한글 داده_ها 😀\n'.encode()
            واسط('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in پرونده('인사.txt')
            واسط("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert پرونده('리터럴')=='$인사\n누리\n'.encode()
            واسط('echo one > بیانیه_مقدار; echo two >> بیانیه_مقدار; echo three >> بیانیه_مقدار')
            واسط('cat < بیانیه_مقدار | grep t | tee 추림 | wc -l','2\n'); assert پرونده('추림')==b'two\nthree\n'
            واسط('head -n 1 بیانیه_مقدار > جلو_مقدار; tail -n 1 بیانیه_مقدار > برگشت_مقدار'); assert پرونده('앞')==b'one\n'; assert پرونده('뒤')==b'three\n'
            واسط('grep absent بیانیه_مقدار; echo $?','1\n')
            واسط('echo untouched > حفاظت_کردن_مقدار')
            واسط('echo destroyed > حفاظت_کردن_مقدار |','명령이 빠졌습니다'); assert پرونده('حفاظت_کردن_مقدار')==b'untouched\n'
            واسط('echo "oops','따옴표가 닫히지 않았습니다')
            واسط('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            واسط('echo bad 2> حفاظت_کردن_مقدار','번호를 지정한 پرونده 서술자 ورودی_خروجی جابجایی_حالت'); assert پرونده('حفاظت_کردن_مقدار')==b'untouched\n'
            واسط('rm 빈파일 리터럴 بیانیه_مقدار 추림 جلو_مقدار برگشت_مقدار حفاظت_کردن_مقدار')
            اعتبارسنجی_گزارش['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            واسط("python -c 'print(123)' | wc -c",'4\n')
            واسط("python -c 'print(456)' > برنامه_f5044b9b.txt"); assert پرونده('برنامه_f5044b9b.txt')==b'456\n'
            واسط("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            واسط("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < برنامه_f5044b9b.txt", "b'456\\n'", "b''")
            واسط("python -c 'print(\"x\"*17000)' | wc -c", 'خطا -28')
            واسط('echo recovered | wc -c','10\n')
            واسط("python -c 'import jkoros; print(jkoros.read("+'"/작업/برنامه_f5044b9b.txt"'+"))'",'456','exit 0')
            واسط('cd /; javac Hello.java','Compiled:','exit 0')
            واسط('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in پرونده('/작업/자바.txt')
            واسط('cd 작업; echo "echo script > 실행결과" > فرمان.sh; echo "false || echo recovered >> 실행결과" >> فرمان.sh; sh فرمان.sh')
            assert پرونده('실행결과')==b'script\nrecovered\n'
            واسط('rm 실행결과; echo "exit 7" > خروج_برنامه.sh; sh خروج_برنامه.sh; echo $?','7\n')
            واسط('rm خروج_برنامه.sh فرمان.sh برنامه_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            اعتبارسنجی_گزارش['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            واسط('echo history-proof','history-proof')
            سنجش=ارسال(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert سنجش.count('history-proof')>=2, سنجش
            ارسال(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            سنجش=ارسال(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in سنجش, سنجش
            سنجش=ارسال(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in سنجش,سنجش
            سنجش=ارسال('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in سنجش,سنجش
            긴글='한글'*50
            سنجش=ارسال(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in سنجش
            واسط('terminal','TERMINAL READY')
            واسط('clear')
            واسط('echo "한글 پایانه ABC xyz 012 😀"','한글 پایانه ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as سرویس_گیرنده:
                سرویس_گیرنده.settimeout(10); سرویس_گیرنده.connect(str(모의제어접속))
                with سرویس_گیرنده.makefile('rwb') as جریان_مقدار:
                    json.loads(جریان_مقدار.readline())
                    def 호출(نام,آرگومان_آرايه=None):
                        شبکه_پیام={'execute':نام}
                        if آرگومان_آرايه: شبکه_پیام['arguments']=آرگومان_آرايه
                        جریان_مقدار.write((json.dumps(شبکه_پیام)+'\n').encode()); جریان_مقدار.flush()
                        while True:
                            پاسخ_دادن=json.loads(جریان_مقدار.readline())
                            if 'error' in پاسخ_دادن: raise AssertionError(پاسخ_دادن)
                            if 'return' in پاسخ_دادن: return پاسخ_دادن['return']
                    호출('qmp_capabilities')
                    عکس=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(عکس),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    داده_ها=عکس.read_bytes().split(b'\n',3)[3]
                    def پیکسل(مختصات_x,دکمه_Y_مختصات): return tuple(داده_ها[(دکمه_Y_مختصات*640+مختصات_x)*3:(دکمه_Y_مختصات*640+مختصات_x)*3+3])
                    assert پیکسل(12,48)==(32,80,144),پیکسل(12,48)
                    assert len(set(پیکسل(مختصات_x,دکمه_Y_مختصات) for دکمه_Y_مختصات in range(100,116) for مختصات_x in range(24,56)))>1,'Hangul glyphs missing'
                    واسط('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    واسط("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(عکس),'format':'ppm'})
                    복원자료=عکس.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    واسط('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): واسط('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ارسال(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    سنجش=ارسال(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in سنجش,سنجش
                    واسط('rm visible.txt')
                    호출('quit')
            فرآیند.wait(timeout=5)
            اعتبارسنجی_گزارش['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            اعتبارسنجی_گزارش['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if فرآیند.poll() is None:
                فرآیند.terminate()
                try: فرآیند.wait(timeout=5)
                except subprocess.TimeoutExpired: فرآیند.kill(); فرآیند.wait()
            준비살피미.close(); فرآیند.stdin.close(); فرآیند.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(اعتبارسنجی_گزارش,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': اجرا_2()
