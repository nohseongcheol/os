#!/usr/bin/env python3
"""자체 커널의 shell, 프로세스 I_O, Unicode GUI 터미널을 totoo_data raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Mag_execute_utos import Project_root, utos


def run():
    출력결과 = Project_root / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    pagpapatibay_ulat = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Project_root / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proseso = subprocess.Popen(utos()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proseso.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            data=bytearray(); tapusin_OFFSET=time.monotonic()+시간제한
            while 확인표시 not in data:
                if time.monotonic()>tapusin_OFFSET or Proseso.poll() is not None: raise AssertionError('UART timeout/exit: '+data.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8','replace').replace('\r\n','\n')
        def i_email(data, 확인표시=b'jkoros-native> '):
            Proseso.stdin.write(data); Proseso.stdin.flush(); return 수신하기(확인표시)
        def shell(linya, *예상결과):
            sukat=i_email(linya.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in sukat, (linya,VALUE,sukat)
            return sukat
        def file(pangalan):
            SMS=shell('hex '+pangalan,'HEX BEGIN','HEX END'); SEARCH_sukat=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',SMS,re.S)
            data=bytes.fromhex(''.join(SEARCH_sukat.group(2).split())); assert len(data)==int(SEARCH_sukat.group(1)); return data
        try:
            수신하기(b'jkoros-native> ')
            shell('mkdir 작업; cd 작업; pwd','/작업')
            shell('mkdir 하위; echo "한글 data 😀" > 인사.txt')
            assert file('인사.txt')=='한글 data 😀\n'.encode()
            shell('cp 인사.txt gumawa_ng_kopya_VALUE.txt; mv gumawa_ng_kopya_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 data 😀')
            shell('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 data 😀','/작업/하위')
            shell('cd ..; rmdir 하위; echo $?','1\n')
            shell('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            shell('cp 인사.txt 인사.txt; echo $?','1\n'); assert file('인사.txt')=='한글 data 😀\n'.encode()
            shell('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in file('인사.txt')
            shell("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert file('리터럴')=='$인사\n누리\n'.encode()
            shell('echo one > pahayag_VALUE; echo two >> pahayag_VALUE; echo three >> pahayag_VALUE')
            shell('cat < pahayag_VALUE | grep t | tee 추림 | wc -l','2\n'); assert file('추림')==b'two\nthree\n'
            shell('head -n 1 pahayag_VALUE > nasa_harap_VALUE; tail -n 1 pahayag_VALUE > Bumalik_VALUE'); assert file('앞')==b'one\n'; assert file('뒤')==b'three\n'
            shell('grep absent pahayag_VALUE; echo $?','1\n')
            shell('echo untouched > magprotekta_VALUE')
            shell('echo destroyed > magprotekta_VALUE |','명령이 빠졌습니다'); assert file('magprotekta_VALUE')==b'untouched\n'
            shell('echo "oops','따옴표가 닫히지 않았습니다')
            shell('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            shell('echo bad 2> magprotekta_VALUE','번호를 지정한 file 서술자 I_O SWITCH_MODE'); assert file('magprotekta_VALUE')==b'untouched\n'
            shell('rm 빈파일 리터럴 pahayag_VALUE 추림 nasa_harap_VALUE Bumalik_VALUE magprotekta_VALUE')
            pagpapatibay_ulat['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            shell("python -c 'print(123)' | wc -c",'4\n')
            shell("python -c 'print(456)' > app_f5044b9b.txt"); assert file('app_f5044b9b.txt')==b'456\n'
            shell("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            shell("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < app_f5044b9b.txt", "b'456\\n'", "b''")
            shell("python -c 'print(\"x\"*17000)' | wc -c", 'error -28')
            shell('echo recovered | wc -c','10\n')
            shell("python -c 'import jkoros; print(jkoros.read("+'"/작업/app_f5044b9b.txt"'+"))'",'456','exit 0')
            shell('cd /; javac Hello.java','Compiled:','exit 0')
            shell('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in file('/작업/자바.txt')
            shell('cd 작업; echo "echo script > 실행결과" > utos.sh; echo "false || echo recovered >> 실행결과" >> utos.sh; sh utos.sh')
            assert file('실행결과')==b'script\nrecovered\n'
            shell('rm 실행결과; echo "exit 7" > Paglabas_app.sh; sh Paglabas_app.sh; echo $?','7\n')
            shell('rm Paglabas_app.sh utos.sh app_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            pagpapatibay_ulat['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            shell('echo history-proof','history-proof')
            sukat=i_email(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert sukat.count('history-proof')>=2, sukat
            i_email(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            sukat=i_email(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in sukat, sukat
            sukat=i_email(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in sukat,sukat
            sukat=i_email('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in sukat,sukat
            긴글='한글'*50
            sukat=i_email(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in sukat
            shell('terminal','TERMINAL READY')
            shell('clear')
            shell('echo "한글 Terminal ABC xyz 012 😀"','한글 Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as client:
                client.settimeout(10); client.connect(str(모의제어접속))
                with client.makefile('rwb') as Stream_VALUE:
                    json.loads(Stream_VALUE.readline())
                    def 호출(pangalan,argumento_ARRAY=None):
                        Network_email={'execute':pangalan}
                        if argumento_ARRAY: Network_email['arguments']=argumento_ARRAY
                        Stream_VALUE.write((json.dumps(Network_email)+'\n').encode()); Stream_VALUE.flush()
                        while True:
                            tumugon=json.loads(Stream_VALUE.readline())
                            if 'error' in tumugon: raise AssertionError(tumugon)
                            if 'return' in tumugon: return tumugon['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    data=IMAGE.read_bytes().split(b'\n',3)[3]
                    def pel(x_coordinate,Y_button_coordinate): return tuple(data[(Y_button_coordinate*640+x_coordinate)*3:(Y_button_coordinate*640+x_coordinate)*3+3])
                    assert pel(12,48)==(32,80,144),pel(12,48)
                    assert len(set(pel(x_coordinate,Y_button_coordinate) for Y_button_coordinate in range(100,116) for x_coordinate in range(24,56)))>1,'Hangul glyphs missing'
                    shell('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    shell("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    shell('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): shell('echo scroll-'+str(순번),'scroll-'+str(순번))
                    i_email(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    sukat=i_email(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in sukat,sukat
                    shell('rm visible.txt')
                    호출('quit')
            Proseso.wait(timeout=5)
            pagpapatibay_ulat['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            pagpapatibay_ulat['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proseso.poll() is None:
                Proseso.terminate()
                try: Proseso.wait(timeout=5)
                except subprocess.TimeoutExpired: Proseso.kill(); Proseso.wait()
            준비살피미.close(); Proseso.stdin.close(); Proseso.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(pagpapatibay_ulat,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': run()
