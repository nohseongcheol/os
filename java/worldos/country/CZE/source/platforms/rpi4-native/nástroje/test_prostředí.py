#!/usr/bin/env python3
"""vlastní 커널의 prostředí, 프로세스 vstup_a_výstup, Unicode GUI 터미널을 skutečný_data raspi4b에서 zkoušky."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Provést_příkaz import akce_kořen, příkaz


def Spustit_2():
    výstup = akce_kořen / 'build/verification/shell'; výstup.mkdir(parents=True, exist_ok=True)
    ověření_Zpráva = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((akce_kořen / 'build/kernel8.img').read_bytes()).hexdigest()}
    přepis = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proces = subprocess.Popen(příkaz()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proces.stdout,selectors.EVENT_READ)
        def dostat_e_mail(značka, spuštění_TIMEOUT=45):
            data=bytearray(); konec_POSUN=time.monotonic()+spuštění_TIMEOUT
            while značka not in data:
                if time.monotonic()>konec_POSUN or Proces.poll() is not None: raise AssertionError('UART timeout/exit: '+data.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); přepis.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8','replace').replace('\r\n','\n')
        def poslat(data, značka=b'jkoros-native> '):
            Proces.stdin.write(data); Proces.stdin.flush(); return dostat_e_mail(značka)
        def prostředí(vstupní_řádek, *예상결과):
            VÝSLEDEK=poslat(vstupní_řádek.encode()+b'\n')
            for HODNOTA in 예상결과: assert HODNOTA in VÝSLEDEK, (vstupní_řádek,HODNOTA,VÝSLEDEK)
            return VÝSLEDEK
        def název_souboru(Název):
            text=prostředí('hex '+Název,'HEX BEGIN','HEX END'); HLEDAT_KV=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',text,re.S)
            data=bytes.fromhex(''.join(HLEDAT_KV.group(2).split())); assert len(data)==int(HLEDAT_KV.group(1)); return data
        try:
            dostat_e_mail(b'jkoros-native> ')
            prostředí('mkdir 작업; cd 작업; pwd','/작업')
            prostředí('mkdir 하위; echo "한글 data 😀" > 인사.txt')
            assert název_souboru('인사.txt')=='한글 data 😀\n'.encode()
            prostředí('cp 인사.txt instance_HODNOTA.txt; mv instance_HODNOTA.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 data 😀')
            prostředí('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 data 😀','/작업/하위')
            prostředí('cd ..; rmdir 하위; echo $?','1\n')
            prostředí('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            prostředí('cp 인사.txt 인사.txt; echo $?','1\n'); assert název_souboru('인사.txt')=='한글 data 😀\n'.encode()
            prostředí('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in název_souboru('인사.txt')
            prostředí("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert název_souboru('리터럴')=='$인사\n누리\n'.encode()
            prostředí('echo one > výpis_HODNOTA; echo two >> výpis_HODNOTA; echo three >> výpis_HODNOTA')
            prostředí('cat < výpis_HODNOTA | grep t | tee 추림 | wc -l','2\n'); assert název_souboru('추림')==b'two\nthree\n'
            prostředí('head -n 1 výpis_HODNOTA > přední_fotoaparát_HODNOTA; tail -n 1 výpis_HODNOTA > BACK_HODNOTA'); assert název_souboru('앞')==b'one\n'; assert název_souboru('뒤')==b'three\n'
            prostředí('grep absent výpis_HODNOTA; echo $?','1\n')
            prostředí('echo untouched > chránit_HODNOTA')
            prostředí('echo destroyed > chránit_HODNOTA |','명령이 빠졌습니다'); assert název_souboru('chránit_HODNOTA')==b'untouched\n'
            prostředí('echo "oops','따옴표가 닫히지 않았습니다')
            prostředí('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            prostředí('echo bad 2> chránit_HODNOTA','번호를 지정한 název_souboru popisovač_položka vstup_a_výstup SWITCH_MODE'); assert název_souboru('chránit_HODNOTA')==b'untouched\n'
            prostředí('rm 빈파일 리터럴 výpis_HODNOTA 추림 přední_fotoaparát_HODNOTA BACK_HODNOTA chránit_HODNOTA')
            ověření_Zpráva['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            prostředí("python -c 'print(123)' | wc -c",'4\n')
            prostředí("python -c 'print(456)' > program_f5044b9b.txt"); assert název_souboru('program_f5044b9b.txt')==b'456\n'
            prostředí("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            prostředí("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < program_f5044b9b.txt", "b'456\\n'", "b''")
            prostředí("python -c 'print(\"x\"*17000)' | wc -c", 'chyba -28')
            prostředí('echo recovered | wc -c','10\n')
            prostředí("python -c 'import jkoros; print(jkoros.read("+'"/작업/program_f5044b9b.txt"'+"))'",'456','exit 0')
            prostředí('cd /; javac Hello.java','Compiled:','exit 0')
            prostředí('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in název_souboru('/작업/자바.txt')
            prostředí('cd 작업; echo "echo script > spuštění_KV" > příkaz.sh; echo "false || echo recovered >> spuštění_KV" >> příkaz.sh; sh příkaz.sh')
            assert název_souboru('spuštění_KV')==b'script\nrecovered\n'
            prostředí('rm spuštění_KV; echo "exit 7" > Konec_program.sh; sh Konec_program.sh; echo $?','7\n')
            prostředí('rm Konec_program.sh příkaz.sh program_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            ověření_Zpráva['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            prostředí('echo history-proof','history-proof')
            VÝSLEDEK=poslat(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert VÝSLEDEK.count('history-proof')>=2, VÝSLEDEK
            poslat(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            VÝSLEDEK=poslat(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in VÝSLEDEK, VÝSLEDEK
            VÝSLEDEK=poslat(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in VÝSLEDEK,VÝSLEDEK
            VÝSLEDEK=poslat('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in VÝSLEDEK,VÝSLEDEK
            긴글='한글'*50
            VÝSLEDEK=poslat(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in VÝSLEDEK
            prostředí('terminal','TERMINAL READY')
            prostředí('clear')
            prostředí('echo "한글 interpret_příkazů ABC xyz 012 😀"','한글 interpret_příkazů ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klient:
                klient.settimeout(10); klient.connect(str(모의제어접속))
                with klient.makefile('rwb') as tok_HODNOTA:
                    json.loads(tok_HODNOTA.readline())
                    def 호출(Název,argument_pole=None):
                        síť_e_mail={'execute':Název}
                        if argument_pole: síť_e_mail['arguments']=argument_pole
                        tok_HODNOTA.write((json.dumps(síť_e_mail)+'\n').encode()); tok_HODNOTA.flush()
                        while True:
                            odezva=json.loads(tok_HODNOTA.readline())
                            if 'error' in odezva: raise AssertionError(odezva)
                            if 'return' in odezva: return odezva['return']
                    호출('qmp_capabilities')
                    image=výstup/'terminal.ppm'; 호출('screendump',{'filename':str(image),'format':'ppm'})
                    호출('screendump',{'filename':str(výstup/'terminal.png'),'format':'png'})
                    data=image.read_bytes().split(b'\n',3)[3]
                    def pixel(souřadnice_x,Y_souřadnice): return tuple(data[(Y_souřadnice*640+souřadnice_x)*3:(Y_souřadnice*640+souřadnice_x)*3+3])
                    assert pixel(12,48)==(32,80,144),pixel(12,48)
                    assert len(set(pixel(souřadnice_x,Y_souřadnice) for Y_souřadnice in range(100,116) for souřadnice_x in range(24,56)))>1,'Hangul glyphs missing'
                    prostředí('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    prostředí("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(image),'format':'ppm'})
                    복원자료=image.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    prostředí('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): prostředí('echo scroll-'+str(순번),'scroll-'+str(순번))
                    poslat(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(výstup/'terminal-scroll.png'),'format':'png'})
                    VÝSLEDEK=poslat(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in VÝSLEDEK,VÝSLEDEK
                    prostředí('rm visible.txt')
                    호출('quit')
            Proces.wait(timeout=5)
            ověření_Zpráva['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            ověření_Zpráva['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proces.poll() is None:
                Proces.terminate()
                try: Proces.wait(timeout=5)
                except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
            준비살피미.close(); Proces.stdin.close(); Proces.stdout.close()
            (výstup/'serial.log').write_bytes(přepis)
            (výstup/'report.json').write_text(json.dumps(ověření_Zpráva,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Spustit_2()
