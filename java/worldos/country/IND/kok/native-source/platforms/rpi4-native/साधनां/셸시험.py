#!/usr/bin/env python3
"""자체 커널의 शॅल, 프로세스 I_O, Unicode GUI 터미널을 प्रत्यक्ष_डेटा raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट, आदेश


def चलोवप():
    출력결과 = प्रॉजॅक्ट_रूट / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    वैधताय_अहवाल = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((प्रॉजॅक्ट_रूट / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        प्रक्रिया = subprocess.Popen(आदेश()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(प्रक्रिया.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            डेटा=bytearray(); सोपोवचें_ऑफसॅट=time.monotonic()+시간제한
            while 확인표시 not in डेटा:
                if time.monotonic()>सोपोवचें_ऑफसॅट or प्रक्रिया.poll() is not None: raise AssertionError('UART timeout/exit: '+डेटा.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: डेटा.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in डेटा or b'FAIL ' in डेटा: raise AssertionError(डेटा)
            return डेटा.decode('utf-8','replace').replace('\r\n','\n')
        def धाडचें(डेटा, 확인표시=b'jkoros-native> '):
            प्रक्रिया.stdin.write(डेटा); प्रक्रिया.stdin.flush(); return 수신하기(확인표시)
        def शॅल(रेग, *예상결과):
            मेजप=धाडचें(रेग.encode()+b'\n')
            for मोल in 예상결과: assert मोल in मेजप, (रेग,मोल,मेजप)
            return मेजप
        def फायल(नांव):
            SMS=शॅल('hex '+नांव,'HEX BEGIN','HEX END'); सोद_मेजप=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',SMS,re.S)
            डेटा=bytes.fromhex(''.join(सोद_मेजप.group(2).split())); assert len(डेटा)==int(सोद_मेजप.group(1)); return डेटा
        try:
            수신하기(b'jkoros-native> ')
            शॅल('mkdir 작업; cd 작업; pwd','/작업')
            शॅल('mkdir 하위; echo "한글 डेटा 😀" > 인사.txt')
            assert फायल('인사.txt')=='한글 डेटा 😀\n'.encode()
            शॅल('cp 인사.txt इन्सटन्स_मोल.txt; mv इन्सटन्स_मोल.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 डेटा 😀')
            शॅल('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 डेटा 😀','/작업/하위')
            शॅल('cd ..; rmdir 하위; echo $?','1\n')
            शॅल('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            शॅल('cp 인사.txt 인사.txt; echo $?','1\n'); assert फायल('인사.txt')=='한글 डेटा 😀\n'.encode()
            शॅल('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in फायल('인사.txt')
            शॅल("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert फायल('리터럴')=='$인사\n누리\n'.encode()
            शॅल('echo one > निवेदन_मोल; echo two >> निवेदन_मोल; echo three >> निवेदन_मोल')
            शॅल('cat < निवेदन_मोल | grep t | tee 추림 | wc -l','2\n'); assert फायल('추림')==b'two\nthree\n'
            शॅल('head -n 1 निवेदन_मोल > 앞; tail -n 1 निवेदन_मोल > फाटीं_मोल'); assert फायल('앞')==b'one\n'; assert फायल('뒤')==b'three\n'
            शॅल('grep absent निवेदन_मोल; echo $?','1\n')
            शॅल('echo untouched > राखचें_मोल')
            शॅल('echo destroyed > राखचें_मोल |','명령이 빠졌습니다'); assert फायल('राखचें_मोल')==b'untouched\n'
            शॅल('echo "oops','따옴표가 닫히지 않았습니다')
            शॅल('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            शॅल('echo bad 2> राखचें_मोल','번호를 지정한 फायल 서술자 I_O स्विच_मोड'); assert फायल('राखचें_मोल')==b'untouched\n'
            शॅल('rm 빈파일 리터럴 निवेदन_मोल 추림 앞 फाटीं_मोल राखचें_मोल')
            वैधताय_अहवाल['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            शॅल("python -c 'print(123)' | wc -c",'4\n')
            शॅल("python -c 'print(456)' > एप्लिकेशन_f5044b9b.txt"); assert फायल('एप्लिकेशन_f5044b9b.txt')==b'456\n'
            शॅल("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            शॅल("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < एप्लिकेशन_f5044b9b.txt", "b'456\\n'", "b''")
            शॅल("python -c 'print(\"x\"*17000)' | wc -c", 'चूक -28')
            शॅल('echo recovered | wc -c','10\n')
            शॅल("python -c 'import jkoros; print(jkoros.read("+'"/작업/एप्लिकेशन_f5044b9b.txt"'+"))'",'456','exit 0')
            शॅल('cd /; javac Hello.java','Compiled:','exit 0')
            शॅल('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in फायल('/작업/자바.txt')
            शॅल('cd 작업; echo "echo script > 실행결과" > आदेश.sh; echo "false || echo recovered >> 실행결과" >> आदेश.sh; sh आदेश.sh')
            assert फायल('실행결과')==b'script\nrecovered\n'
            शॅल('rm 실행결과; echo "exit 7" > प्रस्थान_करचें_एप्लिकेशन.sh; sh प्रस्थान_करचें_एप्लिकेशन.sh; echo $?','7\n')
            शॅल('rm प्रस्थान_करचें_एप्लिकेशन.sh आदेश.sh एप्लिकेशन_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            वैधताय_अहवाल['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            शॅल('echo history-proof','history-proof')
            मेजप=धाडचें(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert मेजप.count('history-proof')>=2, मेजप
            धाडचें(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            मेजप=धाडचें(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in मेजप, मेजप
            मेजप=धाडचें(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in मेजप,मेजप
            मेजप=धाडचें('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in मेजप,मेजप
            긴글='한글'*50
            मेजप=धाडचें(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in मेजप
            शॅल('terminal','TERMINAL READY')
            शॅल('clear')
            शॅल('echo "한글 टर्मिनल ABC xyz 012 😀"','한글 टर्मिनल ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as क्लायंट:
                क्लायंट.settimeout(10); क्लायंट.connect(str(모의제어접속))
                with क्लायंट.makefile('rwb') as Stream_मोल:
                    json.loads(Stream_मोल.readline())
                    def 호출(नांव,युक्तीवाद_क्रम=None):
                        नॅटवर्क_संदेश={'execute':नांव}
                        if युक्तीवाद_क्रम: नॅटवर्क_संदेश['arguments']=युक्तीवाद_क्रम
                        Stream_मोल.write((json.dumps(नॅटवर्क_संदेश)+'\n').encode()); Stream_मोल.flush()
                        while True:
                            जाप_दिवप=json.loads(Stream_मोल.readline())
                            if 'error' in जाप_दिवप: raise AssertionError(जाप_दिवप)
                            if 'return' in जाप_दिवप: return जाप_दिवप['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    डेटा=IMAGE.read_bytes().split(b'\n',3)[3]
                    def पिक्सॅल(x_coordinate,세로좌표): return tuple(डेटा[(세로좌표*640+x_coordinate)*3:(세로좌표*640+x_coordinate)*3+3])
                    assert पिक्सॅल(12,48)==(32,80,144),पिक्सॅल(12,48)
                    assert len(set(पिक्सॅल(x_coordinate,세로좌표) for 세로좌표 in range(100,116) for x_coordinate in range(24,56)))>1,'Hangul glyphs missing'
                    शॅल('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    शॅल("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    शॅल('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): शॅल('echo scroll-'+str(순번),'scroll-'+str(순번))
                    धाडचें(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    मेजप=धाडचें(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in मेजप,मेजप
                    शॅल('rm visible.txt')
                    호출('quit')
            प्रक्रिया.wait(timeout=5)
            वैधताय_अहवाल['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            वैधताय_अहवाल['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if प्रक्रिया.poll() is None:
                प्रक्रिया.terminate()
                try: प्रक्रिया.wait(timeout=5)
                except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait()
            준비살피미.close(); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(वैधताय_अहवाल,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': चलोवप()
