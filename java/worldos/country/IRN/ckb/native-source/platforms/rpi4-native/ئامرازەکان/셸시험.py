#!/usr/bin/env python3
"""자체 커널의 توێکڵ, 프로세스 I_O, Unicode GUI 터미널을 ڕاستەکی_دەیتا raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from جێبەجێکردن_فەرمان import 기준, فەرمان


def ڕادان():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    ڕەواکردن_ڕاپۆرت = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        پرۆسە = subprocess.Popen(فەرمان()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(پرۆسە.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            دەیتا=bytearray(); دوایی_کردن_ئۆفسێت=time.monotonic()+시간제한
            while 확인표시 not in دەیتا:
                if time.monotonic()>دوایی_کردن_ئۆفسێت or پرۆسە.poll() is not None: raise AssertionError('UART timeout/exit: '+دەیتا.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: دەیتا.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in دەیتا or b'FAIL ' in دەیتا: raise AssertionError(دەیتا)
            return دەیتا.decode('utf-8','replace').replace('\r\n','\n')
        def ناردن(دەیتا, 확인표시=b'jkoros-native> '):
            پرۆسە.stdin.write(دەیتا); پرۆسە.stdin.flush(); return 수신하기(확인표시)
        def توێکڵ(دێڕ, *예상결과):
            결과=ناردن(دێڕ.encode()+b'\n')
            for نرخ in 예상결과: assert نرخ in 결과, (دێڕ,نرخ,결과)
            return 결과
        def فایل(ناو):
            دەق=توێکڵ('hex '+ناو,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',دەق,re.S)
            دەیتا=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(دەیتا)==int(찾은결과.group(1)); return دەیتا
        try:
            수신하기(b'jkoros-native> ')
            توێکڵ('mkdir 작업; cd 작업; pwd','/작업')
            توێکڵ('mkdir 하위; echo "한글 دەیتا 😀" > 인사.txt')
            assert فایل('인사.txt')=='한글 دەیتا 😀\n'.encode()
            توێکڵ('cp 인사.txt کۆپی_نرخ.txt; mv کۆپی_نرخ.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 دەیتا 😀')
            توێکڵ('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 دەیتا 😀','/작업/하위')
            توێکڵ('cd ..; rmdir 하위; echo $?','1\n')
            توێکڵ('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            توێکڵ('cp 인사.txt 인사.txt; echo $?','1\n'); assert فایل('인사.txt')=='한글 دەیتا 😀\n'.encode()
            توێکڵ('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in فایل('인사.txt')
            توێکڵ("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert فایل('리터럴')=='$인사\n누리\n'.encode()
            توێکڵ('echo one > وتە_نرخ; echo two >> وتە_نرخ; echo three >> وتە_نرخ')
            توێکڵ('cat < وتە_نرخ | grep t | tee 추림 | wc -l','2\n'); assert فایل('추림')==b'two\nthree\n'
            توێکڵ('head -n 1 وتە_نرخ > 앞; tail -n 1 وتە_نرخ > دواوە_نرخ'); assert فایل('앞')==b'one\n'; assert فایل('뒤')==b'three\n'
            توێکڵ('grep absent وتە_نرخ; echo $?','1\n')
            توێکڵ('echo untouched > پاراستن_نرخ')
            توێکڵ('echo destroyed > پاراستن_نرخ |','명령이 빠졌습니다'); assert فایل('پاراستن_نرخ')==b'untouched\n'
            توێکڵ('echo "oops','따옴표가 닫히지 않았습니다')
            توێکڵ('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            توێکڵ('echo bad 2> پاراستن_نرخ','번호를 지정한 فایل 서술자 I_O گۆڕین_دۆخ'); assert فایل('پاراستن_نرخ')==b'untouched\n'
            توێکڵ('rm 빈파일 리터럴 وتە_نرخ 추림 앞 دواوە_نرخ پاراستن_نرخ')
            ڕەواکردن_ڕاپۆرت['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            توێکڵ("python -c 'print(123)' | wc -c",'4\n')
            توێکڵ("python -c 'print(456)' > بەرنامە_f5044b9b.txt"); assert فایل('بەرنامە_f5044b9b.txt')==b'456\n'
            توێکڵ("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            توێکڵ("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < بەرنامە_f5044b9b.txt", "b'456\\n'", "b''")
            توێکڵ("python -c 'print(\"x\"*17000)' | wc -c", 'هەڵە -28')
            توێکڵ('echo recovered | wc -c','10\n')
            توێکڵ("python -c 'import jkoros; print(jkoros.read("+'"/작업/بەرنامە_f5044b9b.txt"'+"))'",'456','exit 0')
            توێکڵ('cd /; javac Hello.java','Compiled:','exit 0')
            توێکڵ('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in فایل('/작업/자바.txt')
            توێکڵ('cd 작업; echo "echo script > 실행결과" > فەرمان.sh; echo "false || echo recovered >> 실행결과" >> فەرمان.sh; sh فەرمان.sh')
            assert فایل('실행결과')==b'script\nrecovered\n'
            توێکڵ('rm 실행결과; echo "exit 7" > بزربوون_بەرنامە.sh; sh بزربوون_بەرنامە.sh; echo $?','7\n')
            توێکڵ('rm بزربوون_بەرنامە.sh فەرمان.sh بەرنامە_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            ڕەواکردن_ڕاپۆرت['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            توێکڵ('echo history-proof','history-proof')
            결과=ناردن(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            ناردن(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=ناردن(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=ناردن(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=ناردن('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=ناردن(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            توێکڵ('terminal','TERMINAL READY')
            توێکڵ('clear')
            توێکڵ('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as کلایەنت:
                کلایەنت.settimeout(10); کلایەنت.connect(str(모의제어접속))
                with کلایەنت.makefile('rwb') as Stream_نرخ:
                    json.loads(Stream_نرخ.readline())
                    def 호출(ناو,ئارگیومێنت_ڕیزی_داتا=None):
                        تۆڕ_پەیام={'execute':ناو}
                        if ئارگیومێنت_ڕیزی_داتا: تۆڕ_پەیام['arguments']=ئارگیومێنت_ڕیزی_داتا
                        Stream_نرخ.write((json.dumps(تۆڕ_پەیام)+'\n').encode()); Stream_نرخ.flush()
                        while True:
                            وەڵامدانەوه=json.loads(Stream_نرخ.readline())
                            if 'error' in وەڵامدانەوه: raise AssertionError(وەڵامدانەوه)
                            if 'return' in وەڵامدانەوه: return وەڵامدانەوه['return']
                    호출('qmp_capabilities')
                    وێنە=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(وێنە),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    دەیتا=وێنە.read_bytes().split(b'\n',3)[3]
                    def پێڵ(پۆوتانی_x,세로좌표): return tuple(دەیتا[(세로좌표*640+پۆوتانی_x)*3:(세로좌표*640+پۆوتانی_x)*3+3])
                    assert پێڵ(12,48)==(32,80,144),پێڵ(12,48)
                    assert len(set(پێڵ(پۆوتانی_x,세로좌표) for 세로좌표 in range(100,116) for پۆوتانی_x in range(24,56)))>1,'Hangul glyphs missing'
                    توێکڵ('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    توێکڵ("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(وێنە),'format':'ppm'})
                    복원자료=وێنە.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    توێکڵ('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): توێکڵ('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ناردن(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=ناردن(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    توێکڵ('rm visible.txt')
                    호출('quit')
            پرۆسە.wait(timeout=5)
            ڕەواکردن_ڕاپۆرت['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            ڕەواکردن_ڕاپۆرت['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if پرۆسە.poll() is None:
                پرۆسە.terminate()
                try: پرۆسە.wait(timeout=5)
                except subprocess.TimeoutExpired: پرۆسە.kill(); پرۆسە.wait()
            준비살피미.close(); پرۆسە.stdin.close(); پرۆسە.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(ڕەواکردن_ڕاپۆرت,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ڕادان()
