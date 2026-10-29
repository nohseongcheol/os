#!/usr/bin/env python3
"""자체 커널의 షెల్, 프로세스 మూ_ఫ, Unicode GUI 터미널을 వాస్తవ_డేటా raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం, ఆదేశము


def నడుపుము():
    출력결과 = ప్రొజెక్ట్_మూలం / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    నిర్ధారణ_నివేదిక = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((ప్రొజెక్ట్_మూలం / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        క్రమణం = subprocess.Popen(ఆదేశము()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(క్రమణం.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            డేటా=bytearray(); ముగించు_ఆఫ్_సెట్=time.monotonic()+시간제한
            while 확인표시 not in డేటా:
                if time.monotonic()>ముగించు_ఆఫ్_సెట్ or క్రమణం.poll() is not None: raise AssertionError('UART timeout/exit: '+డేటా.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: డేటా.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in డేటా or b'FAIL ' in డేటా: raise AssertionError(డేటా)
            return డేటా.decode('utf-8','replace').replace('\r\n','\n')
        def పంపు(డేటా, 확인표시=b'jkoros-native> '):
            క్రమణం.stdin.write(డేటా); క్రమణం.stdin.flush(); return 수신하기(확인표시)
        def షెల్(పంక్తి, *예상결과):
            ప్రమాణం=పంపు(పంక్తి.encode()+b'\n')
            for మూల్యం in 예상결과: assert మూల్యం in ప్రమాణం, (పంక్తి,మూల్యం,ప్రమాణం)
            return ప్రమాణం
        def దస్త్రం(పేరు):
            పాఠ్యము=షెల్('hex '+పేరు,'HEX BEGIN','HEX END'); శోధన_ప్రమాణం=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',పాఠ్యము,re.S)
            డేటా=bytes.fromhex(''.join(శోధన_ప్రమాణం.group(2).split())); assert len(డేటా)==int(శోధన_ప్రమాణం.group(1)); return డేటా
        try:
            수신하기(b'jkoros-native> ')
            షెల్('mkdir 작업; cd 작업; pwd','/작업')
            షెల్('mkdir 하위; echo "한글 డేటా 😀" > 인사.txt')
            assert దస్త్రం('인사.txt')=='한글 డేటా 😀\n'.encode()
            షెల్('cp 인사.txt కాపీ_మూల్యం.txt; mv కాపీ_మూల్యం.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 డేటా 😀')
            షెల్('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 డేటా 😀','/작업/하위')
            షెల్('cd ..; rmdir 하위; echo $?','1\n')
            షెల్('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            షెల్('cp 인사.txt 인사.txt; echo $?','1\n'); assert దస్త్రం('인사.txt')=='한글 డేటా 😀\n'.encode()
            షెల్('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in దస్త్రం('인사.txt')
            షెల్("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert దస్త్రం('리터럴')=='$인사\n누리\n'.encode()
            షెల్('echo one > ప్రకటన_మూల్యం; echo two >> ప్రకటన_మూల్యం; echo three >> ప్రకటన_మూల్యం')
            షెల్('cat < ప్రకటన_మూల్యం | grep t | tee 추림 | wc -l','2\n'); assert దస్త్రం('추림')==b'two\nthree\n'
            షెల్('head -n 1 ప్రకటన_మూల్యం > ముందు_మూల్యం; tail -n 1 ప్రకటన_మూల్యం > వెనుకకు_మూల్యం'); assert దస్త్రం('앞')==b'one\n'; assert దస్త్రం('뒤')==b'three\n'
            షెల్('grep absent ప్రకటన_మూల్యం; echo $?','1\n')
            షెల్('echo untouched > రక్షించు_మూల్యం')
            షెల్('echo destroyed > రక్షించు_మూల్యం |','명령이 빠졌습니다'); assert దస్త్రం('రక్షించు_మూల్యం')==b'untouched\n'
            షెల్('echo "oops','따옴표가 닫히지 않았습니다')
            షెల్('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            షెల్('echo bad 2> రక్షించు_మూల్యం','번호를 지정한 దస్త్రం 서술자 మూ_ఫ మారు_మోడ్'); assert దస్త్రం('రక్షించు_మూల్యం')==b'untouched\n'
            షెల్('rm 빈파일 리터럴 ప్రకటన_మూల్యం 추림 ముందు_మూల్యం వెనుకకు_మూల్యం రక్షించు_మూల్యం')
            నిర్ధారణ_నివేదిక['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            షెల్("python -c 'print(123)' | wc -c",'4\n')
            షెల్("python -c 'print(456)' > అనువర్తనం_f5044b9b.txt"); assert దస్త్రం('అనువర్తనం_f5044b9b.txt')==b'456\n'
            షెల్("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            షెల్("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < అనువర్తనం_f5044b9b.txt", "b'456\\n'", "b''")
            షెల్("python -c 'print(\"x\"*17000)' | wc -c", 'దోషం -28')
            షెల్('echo recovered | wc -c','10\n')
            షెల్("python -c 'import jkoros; print(jkoros.read("+'"/작업/అనువర్తనం_f5044b9b.txt"'+"))'",'456','exit 0')
            షెల్('cd /; javac Hello.java','Compiled:','exit 0')
            షెల్('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in దస్త్రం('/작업/자바.txt')
            షెల్('cd 작업; echo "echo script > 실행결과" > ఆదేశము.sh; echo "false || echo recovered >> 실행결과" >> ఆదేశము.sh; sh ఆదేశము.sh')
            assert దస్త్రం('실행결과')==b'script\nrecovered\n'
            షెల్('rm 실행결과; echo "exit 7" > నిష్క్రమణ_అనువర్తనం.sh; sh నిష్క్రమణ_అనువర్తనం.sh; echo $?','7\n')
            షెల్('rm నిష్క్రమణ_అనువర్తనం.sh ఆదేశము.sh అనువర్తనం_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            నిర్ధారణ_నివేదిక['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            షెల్('echo history-proof','history-proof')
            ప్రమాణం=పంపు(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert ప్రమాణం.count('history-proof')>=2, ప్రమాణం
            పంపు(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            ప్రమాణం=పంపు(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in ప్రమాణం, ప్రమాణం
            ప్రమాణం=పంపు(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in ప్రమాణం,ప్రమాణం
            ప్రమాణం=పంపు('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in ప్రమాణం,ప్రమాణం
            긴글='한글'*50
            ప్రమాణం=పంపు(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in ప్రమాణం
            షెల్('terminal','TERMINAL READY')
            షెల్('clear')
            షెల్('echo "한글 టెర్మినల్ ABC xyz 012 😀"','한글 టెర్మినల్ ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as క్లయింట్:
                క్లయింట్.settimeout(10); క్లయింట్.connect(str(모의제어접속))
                with క్లయింట్.makefile('rwb') as ధార_మూల్యం:
                    json.loads(ధార_మూల్యం.readline())
                    def 호출(పేరు,కారకం_శ్రేణి=None):
                        నెట్_వర్క్_సందేశం={'execute':పేరు}
                        if కారకం_శ్రేణి: నెట్_వర్క్_సందేశం['arguments']=కారకం_శ్రేణి
                        ధార_మూల్యం.write((json.dumps(నెట్_వర్క్_సందేశం)+'\n').encode()); ధార_మూల్యం.flush()
                        while True:
                            ప్రత్యుత్తరం_ఇవ్వు=json.loads(ధార_మూల్యం.readline())
                            if 'error' in ప్రత్యుత్తరం_ఇవ్వు: raise AssertionError(ప్రత్యుత్తరం_ఇవ్వు)
                            if 'return' in ప్రత్యుత్తరం_ఇవ్వు: return ప్రత్యుత్తరం_ఇవ్వు['return']
                    호출('qmp_capabilities')
                    చిత్రం=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(చిత్రం),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    డేటా=చిత్రం.read_bytes().split(b'\n',3)[3]
                    def పెల్(x_నిర్దేశాంకం,Y_బటన్_సమన్వయపరుచు): return tuple(డేటా[(Y_బటన్_సమన్వయపరుచు*640+x_నిర్దేశాంకం)*3:(Y_బటన్_సమన్వయపరుచు*640+x_నిర్దేశాంకం)*3+3])
                    assert పెల్(12,48)==(32,80,144),పెల్(12,48)
                    assert len(set(పెల్(x_నిర్దేశాంకం,Y_బటన్_సమన్వయపరుచు) for Y_బటన్_సమన్వయపరుచు in range(100,116) for x_నిర్దేశాంకం in range(24,56)))>1,'Hangul glyphs missing'
                    షెల్('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    షెల్("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(చిత్రం),'format':'ppm'})
                    복원자료=చిత్రం.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    షెల్('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): షెల్('echo scroll-'+str(순번),'scroll-'+str(순번))
                    పంపు(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    ప్రమాణం=పంపు(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in ప్రమాణం,ప్రమాణం
                    షెల్('rm visible.txt')
                    호출('quit')
            క్రమణం.wait(timeout=5)
            నిర్ధారణ_నివేదిక['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            నిర్ధారణ_నివేదిక['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if క్రమణం.poll() is None:
                క్రమణం.terminate()
                try: క్రమణం.wait(timeout=5)
                except subprocess.TimeoutExpired: క్రమణం.kill(); క్రమణం.wait()
            준비살피미.close(); క్రమణం.stdin.close(); క్రమణం.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': నడుపుము()
