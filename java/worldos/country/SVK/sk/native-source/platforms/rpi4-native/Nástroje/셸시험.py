#!/usr/bin/env python3
"""vlastné 커널의 셸, 프로세스 vstup_a_výstup, Unicode GUI 터미널을 skutočný_údaje raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Vykonať_príkaz import akcia_koreň, Príkaz


def Spustiť_2():
    출력결과 = akcia_koreň / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    overenie_správa = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((akcia_koreň / 'build/kernel8.img').read_bytes()).hexdigest()}
    prepis = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proces = subprocess.Popen(Príkaz()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proces.stdout,selectors.EVENT_READ)
        def dostať_e_mail(fixka, 시간제한=45):
            údaje=bytearray(); ukončiť_hovor_Posun=time.monotonic()+시간제한
            while fixka not in údaje:
                if time.monotonic()>ukončiť_hovor_Posun or Proces.poll() is not None: raise AssertionError('UART timeout/exit: '+údaje.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: údaje.extend(조각); prepis.extend(조각)
                if b'PANIC:' in údaje or b'FAIL ' in údaje: raise AssertionError(údaje)
            return údaje.decode('utf-8','replace').replace('\r\n','\n')
        def odoslať(údaje, fixka=b'jkoros-native> '):
            Proces.stdin.write(údaje); Proces.stdin.flush(); return dostať_e_mail(fixka)
        def 셸(riadok, *예상결과):
            KR=odoslať(riadok.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in KR, (riadok,VALUE,KR)
            return KR
        def Súbor(Názov):
            Spracovanie_textu=셸('hex '+Názov,'HEX BEGIN','HEX END'); Hľadať_KR=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Spracovanie_textu,re.S)
            údaje=bytes.fromhex(''.join(Hľadať_KR.group(2).split())); assert len(údaje)==int(Hľadať_KR.group(1)); return údaje
        try:
            dostať_e_mail(b'jkoros-native> ')
            셸('mkdir 작업; cd 작업; pwd','/작업')
            셸('mkdir 하위; echo "한글 údaje 😀" > 인사.txt')
            assert Súbor('인사.txt')=='한글 údaje 😀\n'.encode()
            셸('cp 인사.txt inštancia_VALUE.txt; mv inštancia_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 údaje 😀')
            셸('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 údaje 😀','/작업/하위')
            셸('cd ..; rmdir 하위; echo $?','1\n')
            셸('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            셸('cp 인사.txt 인사.txt; echo $?','1\n'); assert Súbor('인사.txt')=='한글 údaje 😀\n'.encode()
            셸('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Súbor('인사.txt')
            셸("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Súbor('리터럴')=='$인사\n누리\n'.encode()
            셸('echo one > príkaz_VALUE; echo two >> príkaz_VALUE; echo three >> príkaz_VALUE')
            셸('cat < príkaz_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Súbor('추림')==b'two\nthree\n'
            셸('head -n 1 príkaz_VALUE > predný_VALUE; tail -n 1 príkaz_VALUE > BACK_VALUE'); assert Súbor('앞')==b'one\n'; assert Súbor('뒤')==b'three\n'
            셸('grep absent príkaz_VALUE; echo $?','1\n')
            셸('echo untouched > chrániť_VALUE')
            셸('echo destroyed > chrániť_VALUE |','명령이 빠졌습니다'); assert Súbor('chrániť_VALUE')==b'untouched\n'
            셸('echo "oops','따옴표가 닫히지 않았습니다')
            셸('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            셸('echo bad 2> chrániť_VALUE','번호를 지정한 Súbor 서술자 vstup_a_výstup SWITCH_MODE'); assert Súbor('chrániť_VALUE')==b'untouched\n'
            셸('rm 빈파일 리터럴 príkaz_VALUE 추림 predný_VALUE BACK_VALUE chrániť_VALUE')
            overenie_správa['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            셸("python -c 'print(123)' | wc -c",'4\n')
            셸("python -c 'print(456)' > program_f5044b9b.txt"); assert Súbor('program_f5044b9b.txt')==b'456\n'
            셸("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            셸("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < program_f5044b9b.txt", "b'456\\n'", "b''")
            셸("python -c 'print(\"x\"*17000)' | wc -c", 'chyba -28')
            셸('echo recovered | wc -c','10\n')
            셸("python -c 'import jkoros; print(jkoros.read("+'"/작업/program_f5044b9b.txt"'+"))'",'456','exit 0')
            셸('cd /; javac Hello.java','Compiled:','exit 0')
            셸('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Súbor('/작업/자바.txt')
            셸('cd 작업; echo "echo script > 실행결과" > Príkaz.sh; echo "false || echo recovered >> 실행결과" >> Príkaz.sh; sh Príkaz.sh')
            assert Súbor('실행결과')==b'script\nrecovered\n'
            셸('rm 실행결과; echo "exit 7" > Skončiť_program.sh; sh Skončiť_program.sh; echo $?','7\n')
            셸('rm Skončiť_program.sh Príkaz.sh program_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            overenie_správa['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            셸('echo history-proof','history-proof')
            KR=odoslať(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert KR.count('history-proof')>=2, KR
            odoslať(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            KR=odoslať(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in KR, KR
            KR=odoslať(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in KR,KR
            KR=odoslať('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in KR,KR
            긴글='한글'*50
            KR=odoslať(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in KR
            셸('terminal','TERMINAL READY')
            셸('clear')
            셸('echo "한글 Terminál ABC xyz 012 😀"','한글 Terminál ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klient:
                klient.settimeout(10); klient.connect(str(모의제어접속))
                with klient.makefile('rwb') as Stream_VALUE:
                    json.loads(Stream_VALUE.readline())
                    def 호출(Názov,argument_pole=None):
                        sieť_e_mail={'execute':Názov}
                        if argument_pole: sieť_e_mail['arguments']=argument_pole
                        Stream_VALUE.write((json.dumps(sieť_e_mail)+'\n').encode()); Stream_VALUE.flush()
                        while True:
                            odozva=json.loads(Stream_VALUE.readline())
                            if 'error' in odozva: raise AssertionError(odozva)
                            if 'return' in odozva: return odozva['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    údaje=IMAGE.read_bytes().split(b'\n',3)[3]
                    def pixel(X_súradnica,Y_súradnica): return tuple(údaje[(Y_súradnica*640+X_súradnica)*3:(Y_súradnica*640+X_súradnica)*3+3])
                    assert pixel(12,48)==(32,80,144),pixel(12,48)
                    assert len(set(pixel(X_súradnica,Y_súradnica) for Y_súradnica in range(100,116) for X_súradnica in range(24,56)))>1,'Hangul glyphs missing'
                    셸('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    셸("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    셸('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): 셸('echo scroll-'+str(순번),'scroll-'+str(순번))
                    odoslať(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    KR=odoslať(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in KR,KR
                    셸('rm visible.txt')
                    호출('quit')
            Proces.wait(timeout=5)
            overenie_správa['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            overenie_správa['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proces.poll() is None:
                Proces.terminate()
                try: Proces.wait(timeout=5)
                except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
            준비살피미.close(); Proces.stdin.close(); Proces.stdout.close()
            (출력결과/'serial.log').write_bytes(prepis)
            (출력결과/'report.json').write_text(json.dumps(overenie_správa,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Spustiť_2()
