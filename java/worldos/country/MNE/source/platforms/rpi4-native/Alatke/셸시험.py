#!/usr/bin/env python3
"""자체 커널의 ljuska, 프로세스 U_I, Unicode GUI 터미널을 stvarni_podaci raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Izvrši_komanda import radnja_koren, komanda


def koristiti():
    출력결과 = radnja_koren / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    provera_valjanosti_izveštaj = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((radnja_koren / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkript = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proces = subprocess.Popen(komanda()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proces.stdout,selectors.EVENT_READ)
        def primiti_poruka(označivač, 시간제한=45):
            podaci=bytearray(); završiti_razgovor_Pomak=time.monotonic()+시간제한
            while označivač not in podaci:
                if time.monotonic()>završiti_razgovor_Pomak or Proces.poll() is not None: raise AssertionError('UART timeout/exit: '+podaci.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: podaci.extend(조각); transkript.extend(조각)
                if b'PANIC:' in podaci or b'FAIL ' in podaci: raise AssertionError(podaci)
            return podaci.decode('utf-8','replace').replace('\r\n','\n')
        def poslati(podaci, označivač=b'jkoros-native> '):
            Proces.stdin.write(podaci); Proces.stdin.flush(); return primiti_poruka(označivač)
        def ljuska(red, *예상결과):
            KR=poslati(red.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in KR, (red,VALUE,KR)
            return KR
        def Datoteka(ime):
            SMS=ljuska('hex '+ime,'HEX BEGIN','HEX END'); SEARCH_KR=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',SMS,re.S)
            podaci=bytes.fromhex(''.join(SEARCH_KR.group(2).split())); assert len(podaci)==int(SEARCH_KR.group(1)); return podaci
        try:
            primiti_poruka(b'jkoros-native> ')
            ljuska('mkdir 작업; cd 작업; pwd','/작업')
            ljuska('mkdir 하위; echo "한글 podaci 😀" > 인사.txt')
            assert Datoteka('인사.txt')=='한글 podaci 😀\n'.encode()
            ljuska('cp 인사.txt instanca_VALUE.txt; mv instanca_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 podaci 😀')
            ljuska('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 podaci 😀','/작업/하위')
            ljuska('cd ..; rmdir 하위; echo $?','1\n')
            ljuska('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            ljuska('cp 인사.txt 인사.txt; echo $?','1\n'); assert Datoteka('인사.txt')=='한글 podaci 😀\n'.encode()
            ljuska('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Datoteka('인사.txt')
            ljuska("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Datoteka('리터럴')=='$인사\n누리\n'.encode()
            ljuska('echo one > instrukcija_VALUE; echo two >> instrukcija_VALUE; echo three >> instrukcija_VALUE')
            ljuska('cat < instrukcija_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Datoteka('추림')==b'two\nthree\n'
            ljuska('head -n 1 instrukcija_VALUE > čeona_kamera_VALUE; tail -n 1 instrukcija_VALUE > NAZAD_VALUE'); assert Datoteka('앞')==b'one\n'; assert Datoteka('뒤')==b'three\n'
            ljuska('grep absent instrukcija_VALUE; echo $?','1\n')
            ljuska('echo untouched > zaštititi_VALUE')
            ljuska('echo destroyed > zaštititi_VALUE |','명령이 빠졌습니다'); assert Datoteka('zaštititi_VALUE')==b'untouched\n'
            ljuska('echo "oops','따옴표가 닫히지 않았습니다')
            ljuska('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            ljuska('echo bad 2> zaštititi_VALUE','번호를 지정한 Datoteka 서술자 U_I SWITCH_MODE'); assert Datoteka('zaštititi_VALUE')==b'untouched\n'
            ljuska('rm 빈파일 리터럴 instrukcija_VALUE 추림 čeona_kamera_VALUE NAZAD_VALUE zaštititi_VALUE')
            provera_valjanosti_izveštaj['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            ljuska("python -c 'print(123)' | wc -c",'4\n')
            ljuska("python -c 'print(456)' > program_f5044b9b.txt"); assert Datoteka('program_f5044b9b.txt')==b'456\n'
            ljuska("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            ljuska("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < program_f5044b9b.txt", "b'456\\n'", "b''")
            ljuska("python -c 'print(\"x\"*17000)' | wc -c", 'greška -28')
            ljuska('echo recovered | wc -c','10\n')
            ljuska("python -c 'import jkoros; print(jkoros.read("+'"/작업/program_f5044b9b.txt"'+"))'",'456','exit 0')
            ljuska('cd /; javac Hello.java','Compiled:','exit 0')
            ljuska('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Datoteka('/작업/자바.txt')
            ljuska('cd 작업; echo "echo script > 실행결과" > komanda.sh; echo "false || echo recovered >> 실행결과" >> komanda.sh; sh komanda.sh')
            assert Datoteka('실행결과')==b'script\nrecovered\n'
            ljuska('rm 실행결과; echo "exit 7" > Izađi_program.sh; sh Izađi_program.sh; echo $?','7\n')
            ljuska('rm Izađi_program.sh komanda.sh program_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            provera_valjanosti_izveštaj['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            ljuska('echo history-proof','history-proof')
            KR=poslati(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert KR.count('history-proof')>=2, KR
            poslati(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            KR=poslati(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in KR, KR
            KR=poslati(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in KR,KR
            KR=poslati('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in KR,KR
            긴글='한글'*50
            KR=poslati(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in KR
            ljuska('terminal','TERMINAL READY')
            ljuska('clear')
            ljuska('echo "한글 Terminal ABC xyz 012 😀"','한글 Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klijent:
                klijent.settimeout(10); klijent.connect(str(모의제어접속))
                with klijent.makefile('rwb') as tok_VALUE:
                    json.loads(tok_VALUE.readline())
                    def 호출(ime,argument_niz=None):
                        Mreža_poruka={'execute':ime}
                        if argument_niz: Mreža_poruka['arguments']=argument_niz
                        tok_VALUE.write((json.dumps(Mreža_poruka)+'\n').encode()); tok_VALUE.flush()
                        while True:
                            odgovor=json.loads(tok_VALUE.readline())
                            if 'error' in odgovor: raise AssertionError(odgovor)
                            if 'return' in odgovor: return odgovor['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    podaci=IMAGE.read_bytes().split(b'\n',3)[3]
                    def piksel(x_koordinata,세로좌표): return tuple(podaci[(세로좌표*640+x_koordinata)*3:(세로좌표*640+x_koordinata)*3+3])
                    assert piksel(12,48)==(32,80,144),piksel(12,48)
                    assert len(set(piksel(x_koordinata,세로좌표) for 세로좌표 in range(100,116) for x_koordinata in range(24,56)))>1,'Hangul glyphs missing'
                    ljuska('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    ljuska("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    ljuska('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): ljuska('echo scroll-'+str(순번),'scroll-'+str(순번))
                    poslati(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    KR=poslati(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in KR,KR
                    ljuska('rm visible.txt')
                    호출('quit')
            Proces.wait(timeout=5)
            provera_valjanosti_izveštaj['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            provera_valjanosti_izveštaj['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proces.poll() is None:
                Proces.terminate()
                try: Proces.wait(timeout=5)
                except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
            준비살피미.close(); Proces.stdin.close(); Proces.stdout.close()
            (출력결과/'serial.log').write_bytes(transkript)
            (출력결과/'report.json').write_text(json.dumps(provera_valjanosti_izveštaj,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': koristiti()
