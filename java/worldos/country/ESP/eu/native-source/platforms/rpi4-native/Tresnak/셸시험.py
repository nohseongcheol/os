#!/usr/bin/env python3
"""자체 커널의 shell, 프로세스 S_I, Unicode GUI 터미널을 benetako_datuak raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from exekutatu_komando import Project_erro, Komandoa


def Exekutatu_2():
    출력결과 = Project_erro / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    balidazio_txosten = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Project_erro / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Prozesua = subprocess.Popen(Komandoa()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Prozesua.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            datuak=bytearray(); amaitu_Geruzak=time.monotonic()+시간제한
            while 확인표시 not in datuak:
                if time.monotonic()>amaitu_Geruzak or Prozesua.poll() is not None: raise AssertionError('UART timeout/exit: '+datuak.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: datuak.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in datuak or b'FAIL ' in datuak: raise AssertionError(datuak)
            return datuak.decode('utf-8','replace').replace('\r\n','\n')
        def bidali(datuak, 확인표시=b'jkoros-native> '):
            Prozesua.stdin.write(datuak); Prozesua.stdin.flush(); return 수신하기(확인표시)
        def shell(Marra, *예상결과):
            EMAITZA=bidali(Marra.encode()+b'\n')
            for balio in 예상결과: assert balio in EMAITZA, (Marra,balio,EMAITZA)
            return EMAITZA
        def Fitxategia(Izena):
            Testua=shell('hex '+Izena,'HEX BEGIN','HEX END'); BILATU_neurria=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Testua,re.S)
            datuak=bytes.fromhex(''.join(BILATU_neurria.group(2).split())); assert len(datuak)==int(BILATU_neurria.group(1)); return datuak
        try:
            수신하기(b'jkoros-native> ')
            shell('mkdir 작업; cd 작업; pwd','/작업')
            shell('mkdir 하위; echo "한글 datuak 😀" > 인사.txt')
            assert Fitxategia('인사.txt')=='한글 datuak 😀\n'.encode()
            shell('cp 인사.txt kopiatu_balio.txt; mv kopiatu_balio.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 datuak 😀')
            shell('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 datuak 😀','/작업/하위')
            shell('cd ..; rmdir 하위; echo $?','1\n')
            shell('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            shell('cp 인사.txt 인사.txt; echo $?','1\n'); assert Fitxategia('인사.txt')=='한글 datuak 😀\n'.encode()
            shell('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Fitxategia('인사.txt')
            shell("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Fitxategia('리터럴')=='$인사\n누리\n'.encode()
            shell('echo one > instrukzio_balio; echo two >> instrukzio_balio; echo three >> instrukzio_balio')
            shell('cat < instrukzio_balio | grep t | tee 추림 | wc -l','2\n'); assert Fitxategia('추림')==b'two\nthree\n'
            shell('head -n 1 instrukzio_balio > aurrekoa_balio; tail -n 1 instrukzio_balio > ATZERA_balio'); assert Fitxategia('앞')==b'one\n'; assert Fitxategia('뒤')==b'three\n'
            shell('grep absent instrukzio_balio; echo $?','1\n')
            shell('echo untouched > babestu_balio')
            shell('echo destroyed > babestu_balio |','명령이 빠졌습니다'); assert Fitxategia('babestu_balio')==b'untouched\n'
            shell('echo "oops','따옴표가 닫히지 않았습니다')
            shell('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            shell('echo bad 2> babestu_balio','번호를 지정한 Fitxategia 서술자 S_I ALDATU_MODA'); assert Fitxategia('babestu_balio')==b'untouched\n'
            shell('rm 빈파일 리터럴 instrukzio_balio 추림 aurrekoa_balio ATZERA_balio babestu_balio')
            balidazio_txosten['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            shell("python -c 'print(123)' | wc -c",'4\n')
            shell("python -c 'print(456)' > aplik_f5044b9b.txt"); assert Fitxategia('aplik_f5044b9b.txt')==b'456\n'
            shell("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            shell("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < aplik_f5044b9b.txt", "b'456\\n'", "b''")
            shell("python -c 'print(\"x\"*17000)' | wc -c", 'errorea -28')
            shell('echo recovered | wc -c','10\n')
            shell("python -c 'import jkoros; print(jkoros.read("+'"/작업/aplik_f5044b9b.txt"'+"))'",'456','exit 0')
            shell('cd /; javac Hello.java','Compiled:','exit 0')
            shell('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Fitxategia('/작업/자바.txt')
            shell('cd 작업; echo "echo script > 실행결과" > Komandoa.sh; echo "false || echo recovered >> 실행결과" >> Komandoa.sh; sh Komandoa.sh')
            assert Fitxategia('실행결과')==b'script\nrecovered\n'
            shell('rm 실행결과; echo "exit 7" > irten_aplik.sh; sh irten_aplik.sh; echo $?','7\n')
            shell('rm irten_aplik.sh Komandoa.sh aplik_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            balidazio_txosten['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            shell('echo history-proof','history-proof')
            EMAITZA=bidali(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert EMAITZA.count('history-proof')>=2, EMAITZA
            bidali(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            EMAITZA=bidali(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in EMAITZA, EMAITZA
            EMAITZA=bidali(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in EMAITZA,EMAITZA
            EMAITZA=bidali('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in EMAITZA,EMAITZA
            긴글='한글'*50
            EMAITZA=bidali(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in EMAITZA
            shell('terminal','TERMINAL READY')
            shell('clear')
            shell('echo "한글 Terminala ABC xyz 012 😀"','한글 Terminala ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as bezero:
                bezero.settimeout(10); bezero.connect(str(모의제어접속))
                with bezero.makefile('rwb') as Stream_balio:
                    json.loads(Stream_balio.readline())
                    def 호출(Izena,arg_matrize=None):
                        sare_mezu={'execute':Izena}
                        if arg_matrize: sare_mezu['arguments']=arg_matrize
                        Stream_balio.write((json.dumps(sare_mezu)+'\n').encode()); Stream_balio.flush()
                        while True:
                            erantzun=json.loads(Stream_balio.readline())
                            if 'error' in erantzun: raise AssertionError(erantzun)
                            if 'return' in erantzun: return erantzun['return']
                    호출('qmp_capabilities')
                    irudi=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(irudi),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    datuak=irudi.read_bytes().split(b'\n',3)[3]
                    def pixel(X_koordenatu,Y_koordenatu): return tuple(datuak[(Y_koordenatu*640+X_koordenatu)*3:(Y_koordenatu*640+X_koordenatu)*3+3])
                    assert pixel(12,48)==(32,80,144),pixel(12,48)
                    assert len(set(pixel(X_koordenatu,Y_koordenatu) for Y_koordenatu in range(100,116) for X_koordenatu in range(24,56)))>1,'Hangul glyphs missing'
                    shell('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    shell("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(irudi),'format':'ppm'})
                    복원자료=irudi.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    shell('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): shell('echo scroll-'+str(순번),'scroll-'+str(순번))
                    bidali(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    EMAITZA=bidali(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in EMAITZA,EMAITZA
                    shell('rm visible.txt')
                    호출('quit')
            Prozesua.wait(timeout=5)
            balidazio_txosten['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            balidazio_txosten['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Prozesua.poll() is None:
                Prozesua.terminate()
                try: Prozesua.wait(timeout=5)
                except subprocess.TimeoutExpired: Prozesua.kill(); Prozesua.wait()
            준비살피미.close(); Prozesua.stdin.close(); Prozesua.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(balidazio_txosten,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Exekutatu_2()
