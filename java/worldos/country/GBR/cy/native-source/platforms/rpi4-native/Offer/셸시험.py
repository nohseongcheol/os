#!/usr/bin/env python3
"""자체 커널의 cragen, 프로세스 I_O, Unicode GUI 터미널을 go_iawn_data raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Gweithredu_gorchymyn import prosiect_gwraidd, Gorchymyn


def Gweithredu_2():
    출력결과 = prosiect_gwraidd / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    dilysu_adrodd = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((prosiect_gwraidd / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proses = subprocess.Popen(Gorchymyn()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proses.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            data=bytearray(); gorffen_OFFSET=time.monotonic()+시간제한
            while 확인표시 not in data:
                if time.monotonic()>gorffen_OFFSET or Proses.poll() is not None: raise AssertionError('UART timeout/exit: '+data.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8','replace').replace('\r\n','\n')
        def anfon(data, 확인표시=b'jkoros-native> '):
            Proses.stdin.write(data); Proses.stdin.flush(); return 수신하기(확인표시)
        def cragen(llinell, *예상결과):
            mesur=anfon(llinell.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in mesur, (llinell,VALUE,mesur)
            return mesur
        def Ffeil(Enw):
            Testun=cragen('hex '+Enw,'HEX BEGIN','HEX END'); SEARCH_mesur=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Testun,re.S)
            data=bytes.fromhex(''.join(SEARCH_mesur.group(2).split())); assert len(data)==int(SEARCH_mesur.group(1)); return data
        try:
            수신하기(b'jkoros-native> ')
            cragen('mkdir 작업; cd 작업; pwd','/작업')
            cragen('mkdir 하위; echo "한글 data 😀" > 인사.txt')
            assert Ffeil('인사.txt')=='한글 data 😀\n'.encode()
            cragen('cp 인사.txt copïo_VALUE.txt; mv copïo_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 data 😀')
            cragen('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 data 😀','/작업/하위')
            cragen('cd ..; rmdir 하위; echo $?','1\n')
            cragen('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            cragen('cp 인사.txt 인사.txt; echo $?','1\n'); assert Ffeil('인사.txt')=='한글 data 😀\n'.encode()
            cragen('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Ffeil('인사.txt')
            cragen("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Ffeil('리터럴')=='$인사\n누리\n'.encode()
            cragen('echo one > gosodiad_VALUE; echo two >> gosodiad_VALUE; echo three >> gosodiad_VALUE')
            cragen('cat < gosodiad_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Ffeil('추림')==b'two\nthree\n'
            cragen('head -n 1 gosodiad_VALUE > 앞; tail -n 1 gosodiad_VALUE > BACK_VALUE'); assert Ffeil('앞')==b'one\n'; assert Ffeil('뒤')==b'three\n'
            cragen('grep absent gosodiad_VALUE; echo $?','1\n')
            cragen('echo untouched > diogelu_VALUE')
            cragen('echo destroyed > diogelu_VALUE |','명령이 빠졌습니다'); assert Ffeil('diogelu_VALUE')==b'untouched\n'
            cragen('echo "oops','따옴표가 닫히지 않았습니다')
            cragen('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            cragen('echo bad 2> diogelu_VALUE','번호를 지정한 Ffeil 서술자 I_O newid_MODE'); assert Ffeil('diogelu_VALUE')==b'untouched\n'
            cragen('rm 빈파일 리터럴 gosodiad_VALUE 추림 앞 BACK_VALUE diogelu_VALUE')
            dilysu_adrodd['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            cragen("python -c 'print(123)' | wc -c",'4\n')
            cragen("python -c 'print(456)' > Rhaglen_f5044b9b.txt"); assert Ffeil('Rhaglen_f5044b9b.txt')==b'456\n'
            cragen("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            cragen("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < Rhaglen_f5044b9b.txt", "b'456\\n'", "b''")
            cragen("python -c 'print(\"x\"*17000)' | wc -c", 'Gwall -28')
            cragen('echo recovered | wc -c','10\n')
            cragen("python -c 'import jkoros; print(jkoros.read("+'"/작업/Rhaglen_f5044b9b.txt"'+"))'",'456','exit 0')
            cragen('cd /; javac Hello.java','Compiled:','exit 0')
            cragen('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Ffeil('/작업/자바.txt')
            cragen('cd 작업; echo "echo script > 실행결과" > Gorchymyn.sh; echo "false || echo recovered >> 실행결과" >> Gorchymyn.sh; sh Gorchymyn.sh')
            assert Ffeil('실행결과')==b'script\nrecovered\n'
            cragen('rm 실행결과; echo "exit 7" > gadael_Rhaglen.sh; sh gadael_Rhaglen.sh; echo $?','7\n')
            cragen('rm gadael_Rhaglen.sh Gorchymyn.sh Rhaglen_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            dilysu_adrodd['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            cragen('echo history-proof','history-proof')
            mesur=anfon(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert mesur.count('history-proof')>=2, mesur
            anfon(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            mesur=anfon(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in mesur, mesur
            mesur=anfon(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in mesur,mesur
            mesur=anfon('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in mesur,mesur
            긴글='한글'*50
            mesur=anfon(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in mesur
            cragen('terminal','TERMINAL READY')
            cragen('clear')
            cragen('echo "한글 Terfynell ABC xyz 012 😀"','한글 Terfynell ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as cleient:
                cleient.settimeout(10); cleient.connect(str(모의제어접속))
                with cleient.makefile('rwb') as ffrwd_VALUE:
                    json.loads(ffrwd_VALUE.readline())
                    def 호출(Enw,arg_ARAE=None):
                        Rhwydwaith_neges={'execute':Enw}
                        if arg_ARAE: Rhwydwaith_neges['arguments']=arg_ARAE
                        ffrwd_VALUE.write((json.dumps(Rhwydwaith_neges)+'\n').encode()); ffrwd_VALUE.flush()
                        while True:
                            ateb=json.loads(ffrwd_VALUE.readline())
                            if 'error' in ateb: raise AssertionError(ateb)
                            if 'return' in ateb: return ateb['return']
                    호출('qmp_capabilities')
                    llun=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(llun),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    data=llun.read_bytes().split(b'\n',3)[3]
                    def pel(cyfesuryn_x,Y_cyfesuryn): return tuple(data[(Y_cyfesuryn*640+cyfesuryn_x)*3:(Y_cyfesuryn*640+cyfesuryn_x)*3+3])
                    assert pel(12,48)==(32,80,144),pel(12,48)
                    assert len(set(pel(cyfesuryn_x,Y_cyfesuryn) for Y_cyfesuryn in range(100,116) for cyfesuryn_x in range(24,56)))>1,'Hangul glyphs missing'
                    cragen('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    cragen("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(llun),'format':'ppm'})
                    복원자료=llun.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    cragen('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): cragen('echo scroll-'+str(순번),'scroll-'+str(순번))
                    anfon(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    mesur=anfon(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in mesur,mesur
                    cragen('rm visible.txt')
                    호출('quit')
            Proses.wait(timeout=5)
            dilysu_adrodd['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            dilysu_adrodd['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proses.poll() is None:
                Proses.terminate()
                try: Proses.wait(timeout=5)
                except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
            준비살피미.close(); Proses.stdin.close(); Proses.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(dilysu_adrodd,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Gweithredu_2()
