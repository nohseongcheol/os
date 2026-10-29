#!/usr/bin/env python3
"""savas 커널의 apvalkalas, 프로세스 Į_I, Unicode GUI 터미널을 faktinis_duomenys raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Vykdyti_komanda import Project_šaknis, Komanda


def Paleisti():
    išeiga = Project_šaknis / 'build/verification/shell'; išeiga.mkdir(parents=True, exist_ok=True)
    tikrinimas_pranešti = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Project_šaknis / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkribavimas = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Procesas = subprocess.Popen(Komanda()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Procesas.stdout,selectors.EVENT_READ)
        def gauti_žinutė(žymeklis, 시간제한=45):
            duomenys=bytearray(); baigti_pokalbį_OFFSET=time.monotonic()+시간제한
            while žymeklis not in duomenys:
                if time.monotonic()>baigti_pokalbį_OFFSET or Procesas.poll() is not None: raise AssertionError('UART timeout/exit: '+duomenys.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: duomenys.extend(조각); transkribavimas.extend(조각)
                if b'PANIC:' in duomenys or b'FAIL ' in duomenys: raise AssertionError(duomenys)
            return duomenys.decode('utf-8','replace').replace('\r\n','\n')
        def siųsti(duomenys, žymeklis=b'jkoros-native> '):
            Procesas.stdin.write(duomenys); Procesas.stdin.flush(); return gauti_žinutė(žymeklis)
        def apvalkalas(Eilutė, *예상결과):
            REZULTATAS=siųsti(Eilutė.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in REZULTATAS, (Eilutė,VALUE,REZULTATAS)
            return REZULTATAS
        def Failas(Pavadinimas_2):
            Tekstas=apvalkalas('hex '+Pavadinimas_2,'HEX BEGIN','HEX END'); Ieška_KR=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Tekstas,re.S)
            duomenys=bytes.fromhex(''.join(Ieška_KR.group(2).split())); assert len(duomenys)==int(Ieška_KR.group(1)); return duomenys
        try:
            gauti_žinutė(b'jkoros-native> ')
            apvalkalas('mkdir 작업; cd 작업; pwd','/작업')
            apvalkalas('mkdir 하위; echo "한글 duomenys 😀" > 인사.txt')
            assert Failas('인사.txt')=='한글 duomenys 😀\n'.encode()
            apvalkalas('cp 인사.txt kopijuoti_VALUE.txt; mv kopijuoti_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 duomenys 😀')
            apvalkalas('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 duomenys 😀','/작업/하위')
            apvalkalas('cd ..; rmdir 하위; echo $?','1\n')
            apvalkalas('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            apvalkalas('cp 인사.txt 인사.txt; echo $?','1\n'); assert Failas('인사.txt')=='한글 duomenys 😀\n'.encode()
            apvalkalas('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Failas('인사.txt')
            apvalkalas("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Failas('리터럴')=='$인사\n누리\n'.encode()
            apvalkalas('echo one > išrašas_VALUE; echo two >> išrašas_VALUE; echo three >> išrašas_VALUE')
            apvalkalas('cat < išrašas_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Failas('추림')==b'two\nthree\n'
            apvalkalas('head -n 1 išrašas_VALUE > priekinis_VALUE; tail -n 1 išrašas_VALUE > ATGAL_VALUE'); assert Failas('앞')==b'one\n'; assert Failas('뒤')==b'three\n'
            apvalkalas('grep absent išrašas_VALUE; echo $?','1\n')
            apvalkalas('echo untouched > apsaugoti_VALUE')
            apvalkalas('echo destroyed > apsaugoti_VALUE |','명령이 빠졌습니다'); assert Failas('apsaugoti_VALUE')==b'untouched\n'
            apvalkalas('echo "oops','따옴표가 닫히지 않았습니다')
            apvalkalas('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            apvalkalas('echo bad 2> apsaugoti_VALUE','번호를 지정한 Failas 서술자 Į_I SWITCH_MODE'); assert Failas('apsaugoti_VALUE')==b'untouched\n'
            apvalkalas('rm 빈파일 리터럴 išrašas_VALUE 추림 priekinis_VALUE ATGAL_VALUE apsaugoti_VALUE')
            tikrinimas_pranešti['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            apvalkalas("python -c 'print(123)' | wc -c",'4\n')
            apvalkalas("python -c 'print(456)' > programa_f5044b9b.txt"); assert Failas('programa_f5044b9b.txt')==b'456\n'
            apvalkalas("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            apvalkalas("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < programa_f5044b9b.txt", "b'456\\n'", "b''")
            apvalkalas("python -c 'print(\"x\"*17000)' | wc -c", 'KLAIDA -28')
            apvalkalas('echo recovered | wc -c','10\n')
            apvalkalas("python -c 'import jkoros; print(jkoros.read("+'"/작업/programa_f5044b9b.txt"'+"))'",'456','exit 0')
            apvalkalas('cd /; javac Hello.java','Compiled:','exit 0')
            apvalkalas('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Failas('/작업/자바.txt')
            apvalkalas('cd 작업; echo "echo script > 실행결과" > Komanda.sh; echo "false || echo recovered >> 실행결과" >> Komanda.sh; sh Komanda.sh')
            assert Failas('실행결과')==b'script\nrecovered\n'
            apvalkalas('rm 실행결과; echo "exit 7" > Baigti_programa_086bb533.sh; sh Baigti_programa_086bb533.sh; echo $?','7\n')
            apvalkalas('rm Baigti_programa_086bb533.sh Komanda.sh programa_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            tikrinimas_pranešti['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            apvalkalas('echo history-proof','history-proof')
            REZULTATAS=siųsti(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert REZULTATAS.count('history-proof')>=2, REZULTATAS
            siųsti(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            REZULTATAS=siųsti(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in REZULTATAS, REZULTATAS
            REZULTATAS=siųsti(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in REZULTATAS,REZULTATAS
            REZULTATAS=siųsti('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in REZULTATAS,REZULTATAS
            긴글='한글'*50
            REZULTATAS=siųsti(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in REZULTATAS
            apvalkalas('terminal','TERMINAL READY')
            apvalkalas('clear')
            apvalkalas('echo "한글 Terminalas ABC xyz 012 😀"','한글 Terminalas ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klientas:
                klientas.settimeout(10); klientas.connect(str(모의제어접속))
                with klientas.makefile('rwb') as Stream_VALUE:
                    json.loads(Stream_VALUE.readline())
                    def 호출(Pavadinimas_2,argumentas_ARRAY=None):
                        tinklas_žinutė={'execute':Pavadinimas_2}
                        if argumentas_ARRAY: tinklas_žinutė['arguments']=argumentas_ARRAY
                        Stream_VALUE.write((json.dumps(tinklas_žinutė)+'\n').encode()); Stream_VALUE.flush()
                        while True:
                            atsakyti=json.loads(Stream_VALUE.readline())
                            if 'error' in atsakyti: raise AssertionError(atsakyti)
                            if 'return' in atsakyti: return atsakyti['return']
                    호출('qmp_capabilities')
                    IMAGE=išeiga/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(išeiga/'terminal.png'),'format':'png'})
                    duomenys=IMAGE.read_bytes().split(b'\n',3)[3]
                    def pikselis(x_koordinatė,세로좌표): return tuple(duomenys[(세로좌표*640+x_koordinatė)*3:(세로좌표*640+x_koordinatė)*3+3])
                    assert pikselis(12,48)==(32,80,144),pikselis(12,48)
                    assert len(set(pikselis(x_koordinatė,세로좌표) for 세로좌표 in range(100,116) for x_koordinatė in range(24,56)))>1,'Hangul glyphs missing'
                    apvalkalas('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    apvalkalas("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    apvalkalas('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): apvalkalas('echo scroll-'+str(순번),'scroll-'+str(순번))
                    siųsti(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(išeiga/'terminal-scroll.png'),'format':'png'})
                    REZULTATAS=siųsti(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in REZULTATAS,REZULTATAS
                    apvalkalas('rm visible.txt')
                    호출('quit')
            Procesas.wait(timeout=5)
            tikrinimas_pranešti['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            tikrinimas_pranešti['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Procesas.poll() is None:
                Procesas.terminate()
                try: Procesas.wait(timeout=5)
                except subprocess.TimeoutExpired: Procesas.kill(); Procesas.wait()
            준비살피미.close(); Procesas.stdin.close(); Procesas.stdout.close()
            (išeiga/'serial.log').write_bytes(transkribavimas)
            (išeiga/'report.json').write_text(json.dumps(tikrinimas_pranešti,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Paleisti()
