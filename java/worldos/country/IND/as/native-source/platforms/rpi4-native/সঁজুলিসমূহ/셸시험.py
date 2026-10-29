#!/usr/bin/env python3
"""자체 커널의 শ্বেল, 프로세스 ইনপুট_আউটপুট, Unicode GUI 터미널을 প্ৰকৃত_ডাটা raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from নিষ্পাদন_আদেশ import 기준, কমান্ড


def সঞ্চালন():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    বৈধতা_ৰিপ_ৰ্ট = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        প্ৰসেস = subprocess.Popen(কমান্ড()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(প্ৰসেস.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            ডাটা=bytearray(); অন্ত_কৰক_অফছেট=time.monotonic()+시간제한
            while 확인표시 not in ডাটা:
                if time.monotonic()>অন্ত_কৰক_অফছেট or প্ৰসেস.poll() is not None: raise AssertionError('UART timeout/exit: '+ডাটা.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: ডাটা.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ডাটা or b'FAIL ' in ডাটা: raise AssertionError(ডাটা)
            return ডাটা.decode('utf-8','replace').replace('\r\n','\n')
        def ই_মেইল_কৰক(ডাটা, 확인표시=b'jkoros-native> '):
            প্ৰসেস.stdin.write(ডাটা); প্ৰসেস.stdin.flush(); return 수신하기(확인표시)
        def শ্বেল(লাইন, *예상결과):
            পৰিমাপ=ই_মেইল_কৰক(লাইন.encode()+b'\n')
            for মান in 예상결과: assert মান in পৰিমাপ, (লাইন,মান,পৰিমাপ)
            return পৰিমাপ
        def নথিপত্ৰ(নাম):
            টেক্সট=শ্বেল('hex '+নাম,'HEX BEGIN','HEX END'); অনুসন্ধান_পৰিমাপ=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',টেক্সট,re.S)
            ডাটা=bytes.fromhex(''.join(অনুসন্ধান_পৰিমাপ.group(2).split())); assert len(ডাটা)==int(অনুসন্ধান_পৰিমাপ.group(1)); return ডাটা
        try:
            수신하기(b'jkoros-native> ')
            শ্বেল('mkdir 작업; cd 작업; pwd','/작업')
            শ্বেল('mkdir 하위; echo "한글 ডাটা 😀" > 인사.txt')
            assert নথিপত্ৰ('인사.txt')=='한글 ডাটা 😀\n'.encode()
            শ্বেল('cp 인사.txt নজিৰ_মান.txt; mv নজিৰ_মান.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ডাটা 😀')
            শ্বেল('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 ডাটা 😀','/작업/하위')
            শ্বেল('cd ..; rmdir 하위; echo $?','1\n')
            শ্বেল('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            শ্বেল('cp 인사.txt 인사.txt; echo $?','1\n'); assert নথিপত্ৰ('인사.txt')=='한글 ডাটা 😀\n'.encode()
            শ্বেল('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in নথিপত্ৰ('인사.txt')
            শ্বেল("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert নথিপত্ৰ('리터럴')=='$인사\n누리\n'.encode()
            শ্বেল('echo one > বিবৃতি_মান; echo two >> বিবৃতি_মান; echo three >> বিবৃতি_মান')
            শ্বেল('cat < বিবৃতি_মান | grep t | tee 추림 | wc -l','2\n'); assert নথিপত্ৰ('추림')==b'two\nthree\n'
            শ্বেল('head -n 1 বিবৃতি_মান > 앞; tail -n 1 বিবৃতি_মান > পাছলৈ_মান'); assert নথিপত্ৰ('앞')==b'one\n'; assert নথিপত্ৰ('뒤')==b'three\n'
            শ্বেল('grep absent বিবৃতি_মান; echo $?','1\n')
            শ্বেল('echo untouched > প্রতিৰোধ_কৰক_মান')
            শ্বেল('echo destroyed > প্রতিৰোধ_কৰক_মান |','명령이 빠졌습니다'); assert নথিপত্ৰ('প্রতিৰোধ_কৰক_মান')==b'untouched\n'
            শ্বেল('echo "oops','따옴표가 닫히지 않았습니다')
            শ্বেল('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            শ্বেল('echo bad 2> প্রতিৰোধ_কৰক_মান','번호를 지정한 নথিপত্ৰ 서술자 ইনপুট_আউটপুট সাল_সলনি_মোড'); assert নথিপত্ৰ('প্রতিৰোধ_কৰক_মান')==b'untouched\n'
            শ্বেল('rm 빈파일 리터럴 বিবৃতি_মান 추림 앞 পাছলৈ_মান প্রতিৰোধ_কৰক_মান')
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            শ্বেল("python -c 'print(123)' | wc -c",'4\n')
            শ্বেল("python -c 'print(456)' > এপ্প্_f5044b9b.txt"); assert নথিপত্ৰ('এপ্প্_f5044b9b.txt')==b'456\n'
            শ্বেল("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            শ্বেল("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < এপ্প্_f5044b9b.txt", "b'456\\n'", "b''")
            শ্বেল("python -c 'print(\"x\"*17000)' | wc -c", 'ত্ৰুটি -28')
            শ্বেল('echo recovered | wc -c','10\n')
            শ্বেল("python -c 'import jkoros; print(jkoros.read("+'"/작업/এপ্প্_f5044b9b.txt"'+"))'",'456','exit 0')
            শ্বেল('cd /; javac Hello.java','Compiled:','exit 0')
            শ্বেল('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in নথিপত্ৰ('/작업/자바.txt')
            শ্বেল('cd 작업; echo "echo script > 실행결과" > কমান্ড.sh; echo "false || echo recovered >> 실행결과" >> কমান্ড.sh; sh কমান্ড.sh')
            assert নথিপত্ৰ('실행결과')==b'script\nrecovered\n'
            শ্বেল('rm 실행결과; echo "exit 7" > প্ৰস্থান_এপ্প্.sh; sh প্ৰস্থান_এপ্প্.sh; echo $?','7\n')
            শ্বেল('rm প্ৰস্থান_এপ্প্.sh কমান্ড.sh এপ্প্_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            শ্বেল('echo history-proof','history-proof')
            পৰিমাপ=ই_মেইল_কৰক(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert পৰিমাপ.count('history-proof')>=2, পৰিমাপ
            ই_মেইল_কৰক(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            পৰিমাপ=ই_মেইল_কৰক(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in পৰিমাপ, পৰিমাপ
            পৰিমাপ=ই_মেইল_কৰক(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in পৰিমাপ,পৰিমাপ
            পৰিমাপ=ই_মেইল_কৰক('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in পৰিমাপ,পৰিমাপ
            긴글='한글'*50
            পৰিমাপ=ই_মেইল_কৰক(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in পৰিমাপ
            শ্বেল('terminal','TERMINAL READY')
            শ্বেল('clear')
            শ্বেল('echo "한글 টাৰ্মিনেল ABC xyz 012 😀"','한글 টাৰ্মিনেল ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as ক্লায়েণ্ট:
                ক্লায়েণ্ট.settimeout(10); ক্লায়েণ্ট.connect(str(모의제어접속))
                with ক্লায়েণ্ট.makefile('rwb') as ষ্ট্ৰিম_মান:
                    json.loads(ষ্ট্ৰিম_মান.readline())
                    def 호출(নাম,যুক্তি_শৃঙ্খলা=None):
                        নেটৱৰ্ক_বাৰ্তা={'execute':নাম}
                        if যুক্তি_শৃঙ্খলা: নেটৱৰ্ক_বাৰ্তা['arguments']=যুক্তি_শৃঙ্খলা
                        ষ্ট্ৰিম_মান.write((json.dumps(নেটৱৰ্ক_বাৰ্তা)+'\n').encode()); ষ্ট্ৰিম_মান.flush()
                        while True:
                            প্ৰত্যুত্তৰ_দিয়ক=json.loads(ষ্ট্ৰিম_মান.readline())
                            if 'error' in প্ৰত্যুত্তৰ_দিয়ক: raise AssertionError(প্ৰত্যুত্তৰ_দিয়ক)
                            if 'return' in প্ৰত্যুত্তৰ_দিয়ক: return প্ৰত্যুত্তৰ_দিয়ক['return']
                    호출('qmp_capabilities')
                    ছবি=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(ছবি),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    ডাটা=ছবি.read_bytes().split(b'\n',3)[3]
                    def পিক্সেল(x_ক_ৰ্ডিনেট,세로좌표): return tuple(ডাটা[(세로좌표*640+x_ক_ৰ্ডিনেট)*3:(세로좌표*640+x_ক_ৰ্ডিনেট)*3+3])
                    assert পিক্সেল(12,48)==(32,80,144),পিক্সেল(12,48)
                    assert len(set(পিক্সেল(x_ক_ৰ্ডিনেট,세로좌표) for 세로좌표 in range(100,116) for x_ক_ৰ্ডিনেট in range(24,56)))>1,'Hangul glyphs missing'
                    শ্বেল('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    শ্বেল("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(ছবি),'format':'ppm'})
                    복원자료=ছবি.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    শ্বেল('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): শ্বেল('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ই_মেইল_কৰক(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    পৰিমাপ=ই_মেইল_কৰক(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in পৰিমাপ,পৰিমাপ
                    শ্বেল('rm visible.txt')
                    호출('quit')
            প্ৰসেস.wait(timeout=5)
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            বৈধতা_ৰিপ_ৰ্ট['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if প্ৰসেস.poll() is None:
                প্ৰসেস.terminate()
                try: প্ৰসেস.wait(timeout=5)
                except subprocess.TimeoutExpired: প্ৰসেস.kill(); প্ৰসেস.wait()
            준비살피미.close(); প্ৰসেস.stdin.close(); প্ৰসেস.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(বৈধতা_ৰিপ_ৰ্ট,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': সঞ্চালন()
