#!/usr/bin/env python3
"""자체 커널의 setlhalosataelo, 프로세스 I_O, Unicode GUI 터미널을 tota_tshedimosetso raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from diragatsa_Taelo import 기준, Taelo


def dirisa():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    netefatso_pego = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Thulaganyo = subprocess.Popen(Taelo()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Thulaganyo.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            tshedimosetso=bytearray(); kgaola_Baya_ka_Tekatekanyo=time.monotonic()+시간제한
            while 확인표시 not in tshedimosetso:
                if time.monotonic()>kgaola_Baya_ka_Tekatekanyo or Thulaganyo.poll() is not None: raise AssertionError('UART timeout/exit: '+tshedimosetso.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: tshedimosetso.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in tshedimosetso or b'FAIL ' in tshedimosetso: raise AssertionError(tshedimosetso)
            return tshedimosetso.decode('utf-8','replace').replace('\r\n','\n')
        def romela(tshedimosetso, 확인표시=b'jkoros-native> '):
            Thulaganyo.stdin.write(tshedimosetso); Thulaganyo.stdin.flush(); return 수신하기(확인표시)
        def setlhalosataelo(Mola, *예상결과):
            결과=romela(Mola.encode()+b'\n')
            for Boleng in 예상결과: assert Boleng in 결과, (Mola,Boleng,결과)
            return 결과
        def faele(leina):
            SMS=setlhalosataelo('hex '+leina,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',SMS,re.S)
            tshedimosetso=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(tshedimosetso)==int(찾은결과.group(1)); return tshedimosetso
        try:
            수신하기(b'jkoros-native> ')
            setlhalosataelo('mkdir 작업; cd 작업; pwd','/작업')
            setlhalosataelo('mkdir 하위; echo "한글 tshedimosetso 😀" > 인사.txt')
            assert faele('인사.txt')=='한글 tshedimosetso 😀\n'.encode()
            setlhalosataelo('cp 인사.txt leloko_Boleng.txt; mv leloko_Boleng.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 tshedimosetso 😀')
            setlhalosataelo('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 tshedimosetso 😀','/작업/하위')
            setlhalosataelo('cd ..; rmdir 하위; echo $?','1\n')
            setlhalosataelo('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            setlhalosataelo('cp 인사.txt 인사.txt; echo $?','1\n'); assert faele('인사.txt')=='한글 tshedimosetso 😀\n'.encode()
            setlhalosataelo('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in faele('인사.txt')
            setlhalosataelo("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert faele('리터럴')=='$인사\n누리\n'.encode()
            setlhalosataelo('echo one > polelo_Boleng; echo two >> polelo_Boleng; echo three >> polelo_Boleng')
            setlhalosataelo('cat < polelo_Boleng | grep t | tee 추림 | wc -l','2\n'); assert faele('추림')==b'two\nthree\n'
            setlhalosataelo('head -n 1 polelo_Boleng > 앞; tail -n 1 polelo_Boleng > Morago_Boleng'); assert faele('앞')==b'one\n'; assert faele('뒤')==b'three\n'
            setlhalosataelo('grep absent polelo_Boleng; echo $?','1\n')
            setlhalosataelo('echo untouched > sireletsa_Boleng')
            setlhalosataelo('echo destroyed > sireletsa_Boleng |','명령이 빠졌습니다'); assert faele('sireletsa_Boleng')==b'untouched\n'
            setlhalosataelo('echo "oops','따옴표가 닫히지 않았습니다')
            setlhalosataelo('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            setlhalosataelo('echo bad 2> sireletsa_Boleng','번호를 지정한 faele 서술자 I_O fetola_mokgwa'); assert faele('sireletsa_Boleng')==b'untouched\n'
            setlhalosataelo('rm 빈파일 리터럴 polelo_Boleng 추림 앞 Morago_Boleng sireletsa_Boleng')
            netefatso_pego['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            setlhalosataelo("python -c 'print(123)' | wc -c",'4\n')
            setlhalosataelo("python -c 'print(456)' > Tiriso_f5044b9b.txt"); assert faele('Tiriso_f5044b9b.txt')==b'456\n'
            setlhalosataelo("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            setlhalosataelo("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < Tiriso_f5044b9b.txt", "b'456\\n'", "b''")
            setlhalosataelo("python -c 'print(\"x\"*17000)' | wc -c", 'phoso -28')
            setlhalosataelo('echo recovered | wc -c','10\n')
            setlhalosataelo("python -c 'import jkoros; print(jkoros.read("+'"/작업/Tiriso_f5044b9b.txt"'+"))'",'456','exit 0')
            setlhalosataelo('cd /; javac Hello.java','Compiled:','exit 0')
            setlhalosataelo('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in faele('/작업/자바.txt')
            setlhalosataelo('cd 작업; echo "echo script > 실행결과" > Taelo.sh; echo "false || echo recovered >> 실행결과" >> Taelo.sh; sh Taelo.sh')
            assert faele('실행결과')==b'script\nrecovered\n'
            setlhalosataelo('rm 실행결과; echo "exit 7" > tswaya_Tiriso.sh; sh tswaya_Tiriso.sh; echo $?','7\n')
            setlhalosataelo('rm tswaya_Tiriso.sh Taelo.sh Tiriso_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            netefatso_pego['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            setlhalosataelo('echo history-proof','history-proof')
            결과=romela(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            romela(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=romela(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=romela(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=romela('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=romela(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            setlhalosataelo('terminal','TERMINAL READY')
            setlhalosataelo('clear')
            setlhalosataelo('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as sedirelwa:
                sedirelwa.settimeout(10); sedirelwa.connect(str(모의제어접속))
                with sedirelwa.makefile('rwb') as moela_Boleng:
                    json.loads(moela_Boleng.readline())
                    def 호출(leina,Thulaganyo_setlhopha=None):
                        Neteweke_molaetsa={'execute':leina}
                        if Thulaganyo_setlhopha: Neteweke_molaetsa['arguments']=Thulaganyo_setlhopha
                        moela_Boleng.write((json.dumps(Neteweke_molaetsa)+'\n').encode()); moela_Boleng.flush()
                        while True:
                            araba=json.loads(moela_Boleng.readline())
                            if 'error' in araba: raise AssertionError(araba)
                            if 'return' in araba: return araba['return']
                    호출('qmp_capabilities')
                    Setshwantsho=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(Setshwantsho),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    tshedimosetso=Setshwantsho.read_bytes().split(b'\n',3)[3]
                    def phele(kgokagano_ya_x,세로좌표): return tuple(tshedimosetso[(세로좌표*640+kgokagano_ya_x)*3:(세로좌표*640+kgokagano_ya_x)*3+3])
                    assert phele(12,48)==(32,80,144),phele(12,48)
                    assert len(set(phele(kgokagano_ya_x,세로좌표) for 세로좌표 in range(100,116) for kgokagano_ya_x in range(24,56)))>1,'Hangul glyphs missing'
                    setlhalosataelo('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    setlhalosataelo("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(Setshwantsho),'format':'ppm'})
                    복원자료=Setshwantsho.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    setlhalosataelo('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): setlhalosataelo('echo scroll-'+str(순번),'scroll-'+str(순번))
                    romela(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=romela(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    setlhalosataelo('rm visible.txt')
                    호출('quit')
            Thulaganyo.wait(timeout=5)
            netefatso_pego['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            netefatso_pego['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Thulaganyo.poll() is None:
                Thulaganyo.terminate()
                try: Thulaganyo.wait(timeout=5)
                except subprocess.TimeoutExpired: Thulaganyo.kill(); Thulaganyo.wait()
            준비살피미.close(); Thulaganyo.stdin.close(); Thulaganyo.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(netefatso_pego,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': dirisa()
