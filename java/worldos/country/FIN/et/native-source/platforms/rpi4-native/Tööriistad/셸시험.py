#!/usr/bin/env python3
"""oma 커널의 kest, 프로세스 I_O, Unicode GUI 터미널을 tegelik_andmed raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Täida_käsk import Project_juur, Käsk


def Käivita_2():
    toodang = Project_juur / 'build/verification/shell'; toodang.mkdir(parents=True, exist_ok=True)
    kinnitamine_aruanne = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Project_juur / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkriptsioon = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Protsess = subprocess.Popen(Käsk()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Protsess.stdout,selectors.EVENT_READ)
        def saama_meil(marker, 시간제한=45):
            andmed=bytearray(); lõpeta_kõne_nihe=time.monotonic()+시간제한
            while marker not in andmed:
                if time.monotonic()>lõpeta_kõne_nihe or Protsess.poll() is not None: raise AssertionError('UART timeout/exit: '+andmed.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: andmed.extend(조각); transkriptsioon.extend(조각)
                if b'PANIC:' in andmed or b'FAIL ' in andmed: raise AssertionError(andmed)
            return andmed.decode('utf-8','replace').replace('\r\n','\n')
        def saatma(andmed, marker=b'jkoros-native> '):
            Protsess.stdin.write(andmed); Protsess.stdin.flush(); return saama_meil(marker)
        def kest(Joon, *예상결과):
            TULEMUS=saatma(Joon.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in TULEMUS, (Joon,VALUE,TULEMUS)
            return TULEMUS
        def Fail(Nimi_2):
            Tekst=kest('hex '+Nimi_2,'HEX BEGIN','HEX END'); Otsi_näitaja=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Tekst,re.S)
            andmed=bytes.fromhex(''.join(Otsi_näitaja.group(2).split())); assert len(andmed)==int(Otsi_näitaja.group(1)); return andmed
        try:
            saama_meil(b'jkoros-native> ')
            kest('mkdir 작업; cd 작업; pwd','/작업')
            kest('mkdir 하위; echo "한글 andmed 😀" > 인사.txt')
            assert Fail('인사.txt')=='한글 andmed 😀\n'.encode()
            kest('cp 인사.txt eksemplar_VALUE.txt; mv eksemplar_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 andmed 😀')
            kest('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 andmed 😀','/작업/하위')
            kest('cd ..; rmdir 하위; echo $?','1\n')
            kest('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            kest('cp 인사.txt 인사.txt; echo $?','1\n'); assert Fail('인사.txt')=='한글 andmed 😀\n'.encode()
            kest('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Fail('인사.txt')
            kest("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Fail('리터럴')=='$인사\n누리\n'.encode()
            kest('echo one > lause_VALUE; echo two >> lause_VALUE; echo three >> lause_VALUE')
            kest('cat < lause_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Fail('추림')==b'two\nthree\n'
            kest('head -n 1 lause_VALUE > esikaamera_VALUE; tail -n 1 lause_VALUE > Tagasi_VALUE'); assert Fail('앞')==b'one\n'; assert Fail('뒤')==b'three\n'
            kest('grep absent lause_VALUE; echo $?','1\n')
            kest('echo untouched > kaitsma_VALUE')
            kest('echo destroyed > kaitsma_VALUE |','명령이 빠졌습니다'); assert Fail('kaitsma_VALUE')==b'untouched\n'
            kest('echo "oops','따옴표가 닫히지 않았습니다')
            kest('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            kest('echo bad 2> kaitsma_VALUE','번호를 지정한 Fail 서술자 I_O SWITCH_MODE'); assert Fail('kaitsma_VALUE')==b'untouched\n'
            kest('rm 빈파일 리터럴 lause_VALUE 추림 esikaamera_VALUE Tagasi_VALUE kaitsma_VALUE')
            kinnitamine_aruanne['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            kest("python -c 'print(123)' | wc -c",'4\n')
            kest("python -c 'print(456)' > programm_f5044b9b.txt"); assert Fail('programm_f5044b9b.txt')==b'456\n'
            kest("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            kest("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < programm_f5044b9b.txt", "b'456\\n'", "b''")
            kest("python -c 'print(\"x\"*17000)' | wc -c", 'VIGA -28')
            kest('echo recovered | wc -c','10\n')
            kest("python -c 'import jkoros; print(jkoros.read("+'"/작업/programm_f5044b9b.txt"'+"))'",'456','exit 0')
            kest('cd /; javac Hello.java','Compiled:','exit 0')
            kest('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Fail('/작업/자바.txt')
            kest('cd 작업; echo "echo script > 실행결과" > Käsk.sh; echo "false || echo recovered >> 실행결과" >> Käsk.sh; sh Käsk.sh')
            assert Fail('실행결과')==b'script\nrecovered\n'
            kest('rm 실행결과; echo "exit 7" > Välju_programm.sh; sh Välju_programm.sh; echo $?','7\n')
            kest('rm Välju_programm.sh Käsk.sh programm_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            kinnitamine_aruanne['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            kest('echo history-proof','history-proof')
            TULEMUS=saatma(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert TULEMUS.count('history-proof')>=2, TULEMUS
            saatma(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            TULEMUS=saatma(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in TULEMUS, TULEMUS
            TULEMUS=saatma(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in TULEMUS,TULEMUS
            TULEMUS=saatma('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in TULEMUS,TULEMUS
            긴글='한글'*50
            TULEMUS=saatma(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in TULEMUS
            kest('terminal','TERMINAL READY')
            kest('clear')
            kest('echo "한글 terminal ABC xyz 012 😀"','한글 terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klient:
                klient.settimeout(10); klient.connect(str(모의제어접속))
                with klient.makefile('rwb') as voog_VALUE:
                    json.loads(voog_VALUE.readline())
                    def 호출(Nimi_2,argument_ARRAY=None):
                        võrk_meil={'execute':Nimi_2}
                        if argument_ARRAY: võrk_meil['arguments']=argument_ARRAY
                        voog_VALUE.write((json.dumps(võrk_meil)+'\n').encode()); voog_VALUE.flush()
                        while True:
                            vastus=json.loads(voog_VALUE.readline())
                            if 'error' in vastus: raise AssertionError(vastus)
                            if 'return' in vastus: return vastus['return']
                    호출('qmp_capabilities')
                    pilt=toodang/'terminal.ppm'; 호출('screendump',{'filename':str(pilt),'format':'ppm'})
                    호출('screendump',{'filename':str(toodang/'terminal.png'),'format':'png'})
                    andmed=pilt.read_bytes().split(b'\n',3)[3]
                    def piksel(가로좌표,세로좌표): return tuple(andmed[(세로좌표*640+가로좌표)*3:(세로좌표*640+가로좌표)*3+3])
                    assert piksel(12,48)==(32,80,144),piksel(12,48)
                    assert len(set(piksel(가로좌표,세로좌표) for 세로좌표 in range(100,116) for 가로좌표 in range(24,56)))>1,'Hangul glyphs missing'
                    kest('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    kest("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(pilt),'format':'ppm'})
                    복원자료=pilt.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    kest('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): kest('echo scroll-'+str(순번),'scroll-'+str(순번))
                    saatma(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(toodang/'terminal-scroll.png'),'format':'png'})
                    TULEMUS=saatma(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in TULEMUS,TULEMUS
                    kest('rm visible.txt')
                    호출('quit')
            Protsess.wait(timeout=5)
            kinnitamine_aruanne['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            kinnitamine_aruanne['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Protsess.poll() is None:
                Protsess.terminate()
                try: Protsess.wait(timeout=5)
                except subprocess.TimeoutExpired: Protsess.kill(); Protsess.wait()
            준비살피미.close(); Protsess.stdin.close(); Protsess.stdout.close()
            (toodang/'serial.log').write_bytes(transkriptsioon)
            (toodang/'report.json').write_text(json.dumps(kinnitamine_aruanne,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Käivita_2()
