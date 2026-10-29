#!/usr/bin/env python3
"""নিজ 커널의 শেল, 프로세스 ইনপুট_আউটপুট, Unicode GUI 터미널을 প্রকৃত_ডাটা raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল, আদেশ


def চালনা():
    출력결과 = প্রকল্প_মূল / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    বৈধকরণ_রিপোর্ট = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((প্রকল্প_মূল / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        প্রসেস = subprocess.Popen(আদেশ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(প্রসেস.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            ডাটা=bytearray(); শেষ_করা_অফসেট=time.monotonic()+시간제한
            while 확인표시 not in ডাটা:
                if time.monotonic()>শেষ_করা_অফসেট or প্রসেস.poll() is not None: raise AssertionError('UART timeout/exit: '+ডাটা.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: ডাটা.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ডাটা or b'FAIL ' in ডাটা: raise AssertionError(ডাটা)
            return ডাটা.decode('utf-8','replace').replace('\r\n','\n')
        def পাঠান(ডাটা, 확인표시=b'jkoros-native> '):
            প্রসেস.stdin.write(ডাটা); প্রসেস.stdin.flush(); return 수신하기(확인표시)
        def শেল(নিবেশের_পঙ্_ক্তি, *예상결과):
            পরিমাপ=পাঠান(নিবেশের_পঙ্_ক্তি.encode()+b'\n')
            for মান in 예상결과: assert মান in পরিমাপ, (নিবেশের_পঙ্_ক্তি,মান,পরিমাপ)
            return পরিমাপ
        def নথির_নাম(নাম):
            পাঠ=শেল('hex '+নাম,'HEX BEGIN','HEX END'); দেখুন_পরিমাপ=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',পাঠ,re.S)
            ডাটা=bytes.fromhex(''.join(দেখুন_পরিমাপ.group(2).split())); assert len(ডাটা)==int(দেখুন_পরিমাপ.group(1)); return ডাটা
        try:
            수신하기(b'jkoros-native> ')
            শেল('mkdir 작업; cd 작업; pwd','/작업')
            শেল('mkdir 하위; echo "한글 ডাটা 😀" > 인사.txt')
            assert নথির_নাম('인사.txt')=='한글 ডাটা 😀\n'.encode()
            শেল('cp 인사.txt নজির_মান.txt; mv নজির_মান.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ডাটা 😀')
            শেল('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 ডাটা 😀','/작업/하위')
            শেল('cd ..; rmdir 하위; echo $?','1\n')
            শেল('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            শেল('cp 인사.txt 인사.txt; echo $?','1\n'); assert নথির_নাম('인사.txt')=='한글 ডাটা 😀\n'.encode()
            শেল('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in নথির_নাম('인사.txt')
            শেল("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert নথির_নাম('리터럴')=='$인사\n누리\n'.encode()
            শেল('echo one > বিবৃতি_মান; echo two >> বিবৃতি_মান; echo three >> বিবৃতি_মান')
            শেল('cat < বিবৃতি_মান | grep t | tee 추림 | wc -l','2\n'); assert নথির_নাম('추림')==b'two\nthree\n'
            শেল('head -n 1 বিবৃতি_মান > সম্মুখ_মান; tail -n 1 বিবৃতি_মান > ফিরে_যান_মান'); assert নথির_নাম('앞')==b'one\n'; assert নথির_নাম('뒤')==b'three\n'
            শেল('grep absent বিবৃতি_মান; echo $?','1\n')
            শেল('echo untouched > রক্ষা_করুন_মান')
            শেল('echo destroyed > রক্ষা_করুন_মান |','명령이 빠졌습니다'); assert নথির_নাম('রক্ষা_করুন_মান')==b'untouched\n'
            শেল('echo "oops','따옴표가 닫히지 않았습니다')
            শেল('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            শেল('echo bad 2> রক্ষা_করুন_মান','번호를 지정한 নথির_নাম 서술자 ইনপুট_আউটপুট সুইচ_মোড'); assert নথির_নাম('রক্ষা_করুন_মান')==b'untouched\n'
            শেল('rm 빈파일 리터럴 বিবৃতি_মান 추림 সম্মুখ_মান ফিরে_যান_মান রক্ষা_করুন_মান')
            বৈধকরণ_রিপোর্ট['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            শেল("python -c 'print(123)' | wc -c",'4\n')
            শেল("python -c 'print(456)' > অ্যাপ_f5044b9b.txt"); assert নথির_নাম('অ্যাপ_f5044b9b.txt')==b'456\n'
            শেল("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            শেল("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < অ্যাপ_f5044b9b.txt", "b'456\\n'", "b''")
            শেল("python -c 'print(\"x\"*17000)' | wc -c", 'ত্রুটি -28')
            শেল('echo recovered | wc -c','10\n')
            শেল("python -c 'import jkoros; print(jkoros.read("+'"/작업/অ্যাপ_f5044b9b.txt"'+"))'",'456','exit 0')
            শেল('cd /; javac Hello.java','Compiled:','exit 0')
            শেল('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in নথির_নাম('/작업/자바.txt')
            শেল('cd 작업; echo "echo script > 실행결과" > আদেশ.sh; echo "false || echo recovered >> 실행결과" >> আদেশ.sh; sh আদেশ.sh')
            assert নথির_নাম('실행결과')==b'script\nrecovered\n'
            শেল('rm 실행결과; echo "exit 7" > প্রস্থান_অ্যাপ.sh; sh প্রস্থান_অ্যাপ.sh; echo $?','7\n')
            শেল('rm প্রস্থান_অ্যাপ.sh আদেশ.sh অ্যাপ_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            বৈধকরণ_রিপোর্ট['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            শেল('echo history-proof','history-proof')
            পরিমাপ=পাঠান(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert পরিমাপ.count('history-proof')>=2, পরিমাপ
            পাঠান(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            পরিমাপ=পাঠান(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in পরিমাপ, পরিমাপ
            পরিমাপ=পাঠান(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in পরিমাপ,পরিমাপ
            পরিমাপ=পাঠান('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in পরিমাপ,পরিমাপ
            긴글='한글'*50
            পরিমাপ=পাঠান(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in পরিমাপ
            শেল('terminal','TERMINAL READY')
            শেল('clear')
            শেল('echo "한글 আদেশ_ব্যাখ্যাকারী ABC xyz 012 😀"','한글 আদেশ_ব্যাখ্যাকারী ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as গ্রাহক:
                গ্রাহক.settimeout(10); গ্রাহক.connect(str(모의제어접속))
                with গ্রাহক.makefile('rwb') as প্রবাহ_মান:
                    json.loads(প্রবাহ_মান.readline())
                    def 호출(নাম,যুক্তি_অ্যারে=None):
                        নেটওয়ার্ক_ইমেইল={'execute':নাম}
                        if যুক্তি_অ্যারে: নেটওয়ার্ক_ইমেইল['arguments']=যুক্তি_অ্যারে
                        প্রবাহ_মান.write((json.dumps(নেটওয়ার্ক_ইমেইল)+'\n').encode()); প্রবাহ_মান.flush()
                        while True:
                            উত্তর_দিন=json.loads(প্রবাহ_মান.readline())
                            if 'error' in উত্তর_দিন: raise AssertionError(উত্তর_দিন)
                            if 'return' in উত্তর_দিন: return উত্তর_দিন['return']
                    호출('qmp_capabilities')
                    ছবি=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(ছবি),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    ডাটা=ছবি.read_bytes().split(b'\n',3)[3]
                    def পেল্(X_বোতাম_অক্ষবিন্দু,Y_বোতাম_অক্ষবিন্দু): return tuple(ডাটা[(Y_বোতাম_অক্ষবিন্দু*640+X_বোতাম_অক্ষবিন্দু)*3:(Y_বোতাম_অক্ষবিন্দু*640+X_বোতাম_অক্ষবিন্দু)*3+3])
                    assert পেল্(12,48)==(32,80,144),পেল্(12,48)
                    assert len(set(পেল্(X_বোতাম_অক্ষবিন্দু,Y_বোতাম_অক্ষবিন্দু) for Y_বোতাম_অক্ষবিন্দু in range(100,116) for X_বোতাম_অক্ষবিন্দু in range(24,56)))>1,'Hangul glyphs missing'
                    শেল('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    শেল("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(ছবি),'format':'ppm'})
                    복원자료=ছবি.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    শেল('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): শেল('echo scroll-'+str(순번),'scroll-'+str(순번))
                    পাঠান(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    পরিমাপ=পাঠান(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in পরিমাপ,পরিমাপ
                    শেল('rm visible.txt')
                    호출('quit')
            প্রসেস.wait(timeout=5)
            বৈধকরণ_রিপোর্ট['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            বৈধকরণ_রিপোর্ট['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if প্রসেস.poll() is None:
                প্রসেস.terminate()
                try: প্রসেস.wait(timeout=5)
                except subprocess.TimeoutExpired: প্রসেস.kill(); প্রসেস.wait()
            준비살피미.close(); প্রসেস.stdin.close(); প্রসেস.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(বৈধকরণ_রিপোর্ট,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': চালনা()
