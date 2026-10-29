#!/usr/bin/env python3
"""निज 커널의 शेल, 프로세스 आगत_लगत, Unicode GUI 터미널을 वास्तविक_लगत raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट, आदेश


def चलाउनुहोस्():
    출력결과 = परियोजना_रूट / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    वैधानिकता_रिपोर्ट = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((परियोजना_रूट / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        प्रक्रिया = subprocess.Popen(आदेश()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(प्रक्रिया.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            लगत=bytearray(); समाप्त_गर्नुहोस्_अफसेट=time.monotonic()+시간제한
            while 확인표시 not in लगत:
                if time.monotonic()>समाप्त_गर्नुहोस्_अफसेट or प्रक्रिया.poll() is not None: raise AssertionError('UART timeout/exit: '+लगत.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: लगत.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in लगत or b'FAIL ' in लगत: raise AssertionError(लगत)
            return लगत.decode('utf-8','replace').replace('\r\n','\n')
        def पठाउनुहोस्(लगत, 확인표시=b'jkoros-native> '):
            प्रक्रिया.stdin.write(लगत); प्रक्रिया.stdin.flush(); return 수신하기(확인표시)
        def शेल(रेखा, *예상결과):
            मापन=पठाउनुहोस्(रेखा.encode()+b'\n')
            for मान in 예상결과: assert मान in मापन, (रेखा,मान,मापन)
            return मापन
        def फाइल(नाम):
            पाठ=शेल('hex '+नाम,'HEX BEGIN','HEX END'); खोज_मापन=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',पाठ,re.S)
            लगत=bytes.fromhex(''.join(खोज_मापन.group(2).split())); assert len(लगत)==int(खोज_मापन.group(1)); return लगत
        try:
            수신하기(b'jkoros-native> ')
            शेल('mkdir 작업; cd 작업; pwd','/작업')
            शेल('mkdir 하위; echo "한글 लगत 😀" > 인사.txt')
            assert फाइल('인사.txt')=='한글 लगत 😀\n'.encode()
            शेल('cp 인사.txt उद्धरण_मान_37b3d3b1.txt; mv उद्धरण_मान_37b3d3b1.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 लगत 😀')
            शेल('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 लगत 😀','/작업/하위')
            शेल('cd ..; rmdir 하위; echo $?','1\n')
            शेल('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            शेल('cp 인사.txt 인사.txt; echo $?','1\n'); assert फाइल('인사.txt')=='한글 लगत 😀\n'.encode()
            शेल('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in फाइल('인사.txt')
            शेल("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert फाइल('리터럴')=='$인사\n누리\n'.encode()
            शेल('echo one > कथन_मान; echo two >> कथन_मान; echo three >> कथन_मान')
            शेल('cat < कथन_मान | grep t | tee 추림 | wc -l','2\n'); assert फाइल('추림')==b'two\nthree\n'
            शेल('head -n 1 कथन_मान > 앞; tail -n 1 कथन_मान > पछाडि_मान'); assert फाइल('앞')==b'one\n'; assert फाइल('뒤')==b'three\n'
            शेल('grep absent कथन_मान; echo $?','1\n')
            शेल('echo untouched > सुरक्षित_गर्नुहोस्_मान')
            शेल('echo destroyed > सुरक्षित_गर्नुहोस्_मान |','명령이 빠졌습니다'); assert फाइल('सुरक्षित_गर्नुहोस्_मान')==b'untouched\n'
            शेल('echo "oops','따옴표가 닫히지 않았습니다')
            शेल('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            शेल('echo bad 2> सुरक्षित_गर्नुहोस्_मान','번호를 지정한 फाइल 서술자 आगत_लगत परिवर्तन_मोड'); assert फाइल('सुरक्षित_गर्नुहोस्_मान')==b'untouched\n'
            शेल('rm 빈파일 리터럴 कथन_मान 추림 앞 पछाडि_मान सुरक्षित_गर्नुहोस्_मान')
            वैधानिकता_रिपोर्ट['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            शेल("python -c 'print(123)' | wc -c",'4\n')
            शेल("python -c 'print(456)' > अनुप्रयोग_f5044b9b.txt"); assert फाइल('अनुप्रयोग_f5044b9b.txt')==b'456\n'
            शेल("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            शेल("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < अनुप्रयोग_f5044b9b.txt", "b'456\\n'", "b''")
            शेल("python -c 'print(\"x\"*17000)' | wc -c", 'त्रुटि -28')
            शेल('echo recovered | wc -c','10\n')
            शेल("python -c 'import jkoros; print(jkoros.read("+'"/작업/अनुप्रयोग_f5044b9b.txt"'+"))'",'456','exit 0')
            शेल('cd /; javac Hello.java','Compiled:','exit 0')
            शेल('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in फाइल('/작업/자바.txt')
            शेल('cd 작업; echo "echo script > 실행결과" > आदेश.sh; echo "false || echo recovered >> 실행결과" >> आदेश.sh; sh आदेश.sh')
            assert फाइल('실행결과')==b'script\nrecovered\n'
            शेल('rm 실행결과; echo "exit 7" > बाहिर_जानुहोस्_अनुप्रयोग.sh; sh बाहिर_जानुहोस्_अनुप्रयोग.sh; echo $?','7\n')
            शेल('rm बाहिर_जानुहोस्_अनुप्रयोग.sh आदेश.sh अनुप्रयोग_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            वैधानिकता_रिपोर्ट['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            शेल('echo history-proof','history-proof')
            मापन=पठाउनुहोस्(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert मापन.count('history-proof')>=2, मापन
            पठाउनुहोस्(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            मापन=पठाउनुहोस्(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in मापन, मापन
            मापन=पठाउनुहोस्(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in मापन,मापन
            मापन=पठाउनुहोस्('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in मापन,मापन
            긴글='한글'*50
            मापन=पठाउनुहोस्(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in मापन
            शेल('terminal','TERMINAL READY')
            शेल('clear')
            शेल('echo "한글 टर्मिनल ABC xyz 012 😀"','한글 टर्मिनल ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as ग्राहक:
                ग्राहक.settimeout(10); ग्राहक.connect(str(모의제어접속))
                with ग्राहक.makefile('rwb') as प्रवाह_मान:
                    json.loads(प्रवाह_मान.readline())
                    def 호출(नाम,तर्क_विन्यास=None):
                        सञ्जाल_सन्देश={'execute':नाम}
                        if तर्क_विन्यास: सञ्जाल_सन्देश['arguments']=तर्क_विन्यास
                        प्रवाह_मान.write((json.dumps(सञ्जाल_सन्देश)+'\n').encode()); प्रवाह_मान.flush()
                        while True:
                            जवाफ_दिनुहोस्=json.loads(प्रवाह_मान.readline())
                            if 'error' in जवाफ_दिनुहोस्: raise AssertionError(जवाफ_दिनुहोस्)
                            if 'return' in जवाफ_दिनुहोस्: return जवाफ_दिनुहोस्['return']
                    호출('qmp_capabilities')
                    छवि=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(छवि),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    लगत=छवि.read_bytes().split(b'\n',3)[3]
                    def पेल(x_समन्वय,세로좌표): return tuple(लगत[(세로좌표*640+x_समन्वय)*3:(세로좌표*640+x_समन्वय)*3+3])
                    assert पेल(12,48)==(32,80,144),पेल(12,48)
                    assert len(set(पेल(x_समन्वय,세로좌표) for 세로좌표 in range(100,116) for x_समन्वय in range(24,56)))>1,'Hangul glyphs missing'
                    शेल('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    शेल("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(छवि),'format':'ppm'})
                    복원자료=छवि.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    शेल('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): शेल('echo scroll-'+str(순번),'scroll-'+str(순번))
                    पठाउनुहोस्(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    मापन=पठाउनुहोस्(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in मापन,मापन
                    शेल('rm visible.txt')
                    호출('quit')
            प्रक्रिया.wait(timeout=5)
            वैधानिकता_रिपोर्ट['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            वैधानिकता_रिपोर्ट['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if प्रक्रिया.poll() is None:
                प्रक्रिया.terminate()
                try: प्रक्रिया.wait(timeout=5)
                except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait()
            준비살피미.close(); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(वैधानिकता_रिपोर्ट,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': चलाउनुहोस्()
