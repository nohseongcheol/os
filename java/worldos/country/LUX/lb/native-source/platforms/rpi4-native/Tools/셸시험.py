#!/usr/bin/env python3
"""자체 커널의 Shell, 프로세스 I_O, Unicode GUI 터미널을 aktuell_Daten raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ausféieren_Befeel import projezéieren_Racinn, Befeel


def Laf():
    출력결과 = projezéieren_Racinn / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    Validatioun_mellen = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((projezéieren_Racinn / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Prozess = subprocess.Popen(Befeel()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Prozess.stdout,selectors.EVENT_READ)
        def 수신하기(Markéierung, 시간제한=45):
            Daten=bytearray(); bëennegen_OFFSET=time.monotonic()+시간제한
            while Markéierung not in Daten:
                if time.monotonic()>bëennegen_OFFSET or Prozess.poll() is not None: raise AssertionError('UART timeout/exit: '+Daten.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: Daten.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in Daten or b'FAIL ' in Daten: raise AssertionError(Daten)
            return Daten.decode('utf-8','replace').replace('\r\n','\n')
        def mailen(Daten, Markéierung=b'jkoros-native> '):
            Prozess.stdin.write(Daten); Prozess.stdin.flush(); return 수신하기(Markéierung)
        def Shell(Zeil, *예상결과):
            Mooss=mailen(Zeil.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in Mooss, (Zeil,VALUE,Mooss)
            return Mooss
        def Fichier(Numm):
            SMS=Shell('hex '+Numm,'HEX BEGIN','HEX END'); Sich_Mooss=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',SMS,re.S)
            Daten=bytes.fromhex(''.join(Sich_Mooss.group(2).split())); assert len(Daten)==int(Sich_Mooss.group(1)); return Daten
        try:
            수신하기(b'jkoros-native> ')
            Shell('mkdir 작업; cd 작업; pwd','/작업')
            Shell('mkdir 하위; echo "한글 Daten 😀" > 인사.txt')
            assert Fichier('인사.txt')=='한글 Daten 😀\n'.encode()
            Shell('cp 인사.txt Instanz_VALUE.txt; mv Instanz_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 Daten 😀')
            Shell('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 Daten 😀','/작업/하위')
            Shell('cd ..; rmdir 하위; echo $?','1\n')
            Shell('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            Shell('cp 인사.txt 인사.txt; echo $?','1\n'); assert Fichier('인사.txt')=='한글 Daten 😀\n'.encode()
            Shell('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Fichier('인사.txt')
            Shell("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Fichier('리터럴')=='$인사\n누리\n'.encode()
            Shell('echo one > Ausso_VALUE; echo two >> Ausso_VALUE; echo three >> Ausso_VALUE')
            Shell('cat < Ausso_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Fichier('추림')==b'two\nthree\n'
            Shell('head -n 1 Ausso_VALUE > 앞; tail -n 1 Ausso_VALUE > Zeréck_VALUE'); assert Fichier('앞')==b'one\n'; assert Fichier('뒤')==b'three\n'
            Shell('grep absent Ausso_VALUE; echo $?','1\n')
            Shell('echo untouched > schützen_VALUE')
            Shell('echo destroyed > schützen_VALUE |','명령이 빠졌습니다'); assert Fichier('schützen_VALUE')==b'untouched\n'
            Shell('echo "oops','따옴표가 닫히지 않았습니다')
            Shell('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            Shell('echo bad 2> schützen_VALUE','번호를 지정한 Fichier 서술자 I_O SWITCH_MODE'); assert Fichier('schützen_VALUE')==b'untouched\n'
            Shell('rm 빈파일 리터럴 Ausso_VALUE 추림 앞 Zeréck_VALUE schützen_VALUE')
            Validatioun_mellen['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            Shell("python -c 'print(123)' | wc -c",'4\n')
            Shell("python -c 'print(456)' > App_f5044b9b.txt"); assert Fichier('App_f5044b9b.txt')==b'456\n'
            Shell("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            Shell("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < App_f5044b9b.txt", "b'456\\n'", "b''")
            Shell("python -c 'print(\"x\"*17000)' | wc -c", 'Feeler -28')
            Shell('echo recovered | wc -c','10\n')
            Shell("python -c 'import jkoros; print(jkoros.read("+'"/작업/App_f5044b9b.txt"'+"))'",'456','exit 0')
            Shell('cd /; javac Hello.java','Compiled:','exit 0')
            Shell('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Fichier('/작업/자바.txt')
            Shell('cd 작업; echo "echo script > 실행결과" > Befeel.sh; echo "false || echo recovered >> 실행결과" >> Befeel.sh; sh Befeel.sh')
            assert Fichier('실행결과')==b'script\nrecovered\n'
            Shell('rm 실행결과; echo "exit 7" > Schluss_App.sh; sh Schluss_App.sh; echo $?','7\n')
            Shell('rm Schluss_App.sh Befeel.sh App_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            Validatioun_mellen['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            Shell('echo history-proof','history-proof')
            Mooss=mailen(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert Mooss.count('history-proof')>=2, Mooss
            mailen(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            Mooss=mailen(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in Mooss, Mooss
            Mooss=mailen(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in Mooss,Mooss
            Mooss=mailen('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in Mooss,Mooss
            긴글='한글'*50
            Mooss=mailen(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in Mooss
            Shell('terminal','TERMINAL READY')
            Shell('clear')
            Shell('echo "한글 Terminal ABC xyz 012 😀"','한글 Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as Client:
                Client.settimeout(10); Client.connect(str(모의제어접속))
                with Client.makefile('rwb') as Stream_VALUE:
                    json.loads(Stream_VALUE.readline())
                    def 호출(Numm,Argument_ARRAY=None):
                        Reseau_Noriicht={'execute':Numm}
                        if Argument_ARRAY: Reseau_Noriicht['arguments']=Argument_ARRAY
                        Stream_VALUE.write((json.dumps(Reseau_Noriicht)+'\n').encode()); Stream_VALUE.flush()
                        while True:
                            äntweren=json.loads(Stream_VALUE.readline())
                            if 'error' in äntweren: raise AssertionError(äntweren)
                            if 'return' in äntweren: return äntweren['return']
                    호출('qmp_capabilities')
                    Bild=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(Bild),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    Daten=Bild.read_bytes().split(b'\n',3)[3]
                    def Pel(X_Koordinat,세로좌표): return tuple(Daten[(세로좌표*640+X_Koordinat)*3:(세로좌표*640+X_Koordinat)*3+3])
                    assert Pel(12,48)==(32,80,144),Pel(12,48)
                    assert len(set(Pel(X_Koordinat,세로좌표) for 세로좌표 in range(100,116) for X_Koordinat in range(24,56)))>1,'Hangul glyphs missing'
                    Shell('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    Shell("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(Bild),'format':'ppm'})
                    복원자료=Bild.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    Shell('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): Shell('echo scroll-'+str(순번),'scroll-'+str(순번))
                    mailen(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    Mooss=mailen(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in Mooss,Mooss
                    Shell('rm visible.txt')
                    호출('quit')
            Prozess.wait(timeout=5)
            Validatioun_mellen['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            Validatioun_mellen['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Prozess.poll() is None:
                Prozess.terminate()
                try: Prozess.wait(timeout=5)
                except subprocess.TimeoutExpired: Prozess.kill(); Prozess.wait()
            준비살피미.close(); Prozess.stdin.close(); Prozess.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(Validatioun_mellen,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Laf()
