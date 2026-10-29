#!/usr/bin/env python3
"""propriu 커널의 shell, 프로세스 I_O, Unicode GUI 터미널을 real_date raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from executa_comandă import Project_rădăcină, Comandă


def Pornește():
    출력결과 = Project_rădăcină / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    validare_raport = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Project_rădăcină / 'build/kernel8.img').read_bytes()).hexdigest()}
    transcriere = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proces = subprocess.Popen(Comandă()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proces.stdout,selectors.EVENT_READ)
        def primi_mesaj(marcaj, executare_TIMEOUT=45):
            date=bytearray(); termina_un_apel_OFFSET=time.monotonic()+executare_TIMEOUT
            while marcaj not in date:
                if time.monotonic()>termina_un_apel_OFFSET or Proces.poll() is not None: raise AssertionError('UART timeout/exit: '+date.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: date.extend(조각); transcriere.extend(조각)
                if b'PANIC:' in date or b'FAIL ' in date: raise AssertionError(date)
            return date.decode('utf-8','replace').replace('\r\n','\n')
        def trimite(date, marcaj=b'jkoros-native> '):
            Proces.stdin.write(date); Proces.stdin.flush(); return primi_mesaj(marcaj)
        def shell(Linie, *예상결과):
            KR=trimite(Linie.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in KR, (Linie,VALUE,KR)
            return KR
        def Fișier(Nume):
            SMS=shell('hex '+Nume,'HEX BEGIN','HEX END'); căuta_KR=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',SMS,re.S)
            date=bytes.fromhex(''.join(căuta_KR.group(2).split())); assert len(date)==int(căuta_KR.group(1)); return date
        try:
            primi_mesaj(b'jkoros-native> ')
            shell('mkdir 작업; cd 작업; pwd','/작업')
            shell('mkdir 하위; echo "한글 date 😀" > 인사.txt')
            assert Fișier('인사.txt')=='한글 date 😀\n'.encode()
            shell('cp 인사.txt copia_VALUE.txt; mv copia_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 date 😀')
            shell('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 date 😀','/작업/하위')
            shell('cd ..; rmdir 하위; echo $?','1\n')
            shell('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            shell('cp 인사.txt 인사.txt; echo $?','1\n'); assert Fișier('인사.txt')=='한글 date 😀\n'.encode()
            shell('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Fișier('인사.txt')
            shell("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Fișier('리터럴')=='$인사\n누리\n'.encode()
            shell('echo one > declarație_VALUE; echo two >> declarație_VALUE; echo three >> declarație_VALUE')
            shell('cat < declarație_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Fișier('추림')==b'two\nthree\n'
            shell('head -n 1 declarație_VALUE > frontală_VALUE; tail -n 1 declarație_VALUE > ÎNAPOI_VALUE'); assert Fișier('앞')==b'one\n'; assert Fișier('뒤')==b'three\n'
            shell('grep absent declarație_VALUE; echo $?','1\n')
            shell('echo untouched > proteja_VALUE')
            shell('echo destroyed > proteja_VALUE |','명령이 빠졌습니다'); assert Fișier('proteja_VALUE')==b'untouched\n'
            shell('echo "oops','따옴표가 닫히지 않았습니다')
            shell('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            shell('echo bad 2> proteja_VALUE','번호를 지정한 Fișier 서술자 I_O SWITCH_mod'); assert Fișier('proteja_VALUE')==b'untouched\n'
            shell('rm 빈파일 리터럴 declarație_VALUE 추림 frontală_VALUE ÎNAPOI_VALUE proteja_VALUE')
            validare_raport['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            shell("python -c 'print(123)' | wc -c",'4\n')
            shell("python -c 'print(456)' > program_f5044b9b.txt"); assert Fișier('program_f5044b9b.txt')==b'456\n'
            shell("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            shell("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < program_f5044b9b.txt", "b'456\\n'", "b''")
            shell("python -c 'print(\"x\"*17000)' | wc -c", 'eroare -28')
            shell('echo recovered | wc -c','10\n')
            shell("python -c 'import jkoros; print(jkoros.read("+'"/작업/program_f5044b9b.txt"'+"))'",'456','exit 0')
            shell('cd /; javac Hello.java','Compiled:','exit 0')
            shell('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Fișier('/작업/자바.txt')
            shell('cd 작업; echo "echo script > executare_KR" > Comandă.sh; echo "false || echo recovered >> executare_KR" >> Comandă.sh; sh Comandă.sh')
            assert Fișier('executare_KR')==b'script\nrecovered\n'
            shell('rm executare_KR; echo "exit 7" > ieși_program.sh; sh ieși_program.sh; echo $?','7\n')
            shell('rm ieși_program.sh Comandă.sh program_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            validare_raport['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            shell('echo history-proof','history-proof')
            KR=trimite(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert KR.count('history-proof')>=2, KR
            trimite(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            KR=trimite(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in KR, KR
            KR=trimite(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in KR,KR
            KR=trimite('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in KR,KR
            긴글='한글'*50
            KR=trimite(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in KR
            shell('terminal','TERMINAL READY')
            shell('clear')
            shell('echo "한글 Terminal ABC xyz 012 😀"','한글 Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as client:
                client.settimeout(10); client.connect(str(모의제어접속))
                with client.makefile('rwb') as flux_VALUE:
                    json.loads(flux_VALUE.readline())
                    def 호출(Nume,argument_ARRAY=None):
                        rețea_mesaj={'execute':Nume}
                        if argument_ARRAY: rețea_mesaj['arguments']=argument_ARRAY
                        flux_VALUE.write((json.dumps(rețea_mesaj)+'\n').encode()); flux_VALUE.flush()
                        while True:
                            replică=json.loads(flux_VALUE.readline())
                            if 'error' in replică: raise AssertionError(replică)
                            if 'return' in replică: return replică['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    date=IMAGE.read_bytes().split(b'\n',3)[3]
                    def element_imagine(coordonata_X,세로좌표): return tuple(date[(세로좌표*640+coordonata_X)*3:(세로좌표*640+coordonata_X)*3+3])
                    assert element_imagine(12,48)==(32,80,144),element_imagine(12,48)
                    assert len(set(element_imagine(coordonata_X,세로좌표) for 세로좌표 in range(100,116) for coordonata_X in range(24,56)))>1,'Hangul glyphs missing'
                    shell('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    shell("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    shell('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): shell('echo scroll-'+str(순번),'scroll-'+str(순번))
                    trimite(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    KR=trimite(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in KR,KR
                    shell('rm visible.txt')
                    호출('quit')
            Proces.wait(timeout=5)
            validare_raport['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            validare_raport['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proces.poll() is None:
                Proces.terminate()
                try: Proces.wait(timeout=5)
                except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
            준비살피미.close(); Proces.stdin.close(); Proces.stdout.close()
            (출력결과/'serial.log').write_bytes(transcriere)
            (출력결과/'report.json').write_text(json.dumps(validare_raport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Pornește()
