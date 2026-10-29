#!/usr/bin/env python3
"""własny 커널의 powłoka, 프로세스 We_Wy, Unicode GUI 터미널을 rzeczywisty_dane raspi4b에서 testy."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Wykonaj_polecenie import Project_korzeń, polecenie


def Uruchom_2():
    produkt_wyjściowy = Project_korzeń / 'build/verification/shell'; produkt_wyjściowy.mkdir(parents=True, exist_ok=True)
    walidacja_Raport = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Project_korzeń / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkrypcja = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proces = subprocess.Popen(polecenie()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proces.stdout,selectors.EVENT_READ)
        def odbierać_e_mail(pisak, wykonanie_TIMEOUT=45):
            dane=bytearray(); Koniec_przesunąć=time.monotonic()+wykonanie_TIMEOUT
            while pisak not in dane:
                if time.monotonic()>Koniec_przesunąć or Proces.poll() is not None: raise AssertionError('UART timeout/exit: '+dane.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    fragment_WARTOŚĆ_652d4b53=누름값.fileobj.read(4096)
                    if fragment_WARTOŚĆ_652d4b53: dane.extend(fragment_WARTOŚĆ_652d4b53); transkrypcja.extend(fragment_WARTOŚĆ_652d4b53)
                if b'PANIC:' in dane or b'FAIL ' in dane: raise AssertionError(dane)
            return dane.decode('utf-8','replace').replace('\r\n','\n')
        def wysłać(dane, pisak=b'jkoros-native> '):
            Proces.stdin.write(dane); Proces.stdin.flush(); return odbierać_e_mail(pisak)
        def powłoka(wiersz_wejścia, *예상결과):
            WYNIK=wysłać(wiersz_wejścia.encode()+b'\n')
            for WARTOŚĆ in 예상결과: assert WARTOŚĆ in WYNIK, (wiersz_wejścia,WARTOŚĆ,WYNIK)
            return WYNIK
        def nazwa_pliku(Nazwa):
            tekst=powłoka('hex '+Nazwa,'HEX BEGIN','HEX END'); Search_KR=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',tekst,re.S)
            dane=bytes.fromhex(''.join(Search_KR.group(2).split())); assert len(dane)==int(Search_KR.group(1)); return dane
        try:
            odbierać_e_mail(b'jkoros-native> ')
            powłoka('mkdir 작업; cd 작업; pwd','/작업')
            powłoka('mkdir 하위; echo "한글 dane 😀" > 인사.txt')
            assert nazwa_pliku('인사.txt')=='한글 dane 😀\n'.encode()
            powłoka('cp 인사.txt kopiować_WARTOŚĆ.txt; mv kopiować_WARTOŚĆ.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 dane 😀')
            powłoka('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 dane 😀','/작업/하위')
            powłoka('cd ..; rmdir 하위; echo $?','1\n')
            powłoka('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            powłoka('cp 인사.txt 인사.txt; echo $?','1\n'); assert nazwa_pliku('인사.txt')=='한글 dane 😀\n'.encode()
            powłoka('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in nazwa_pliku('인사.txt')
            powłoka("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert nazwa_pliku('리터럴')=='$인사\n누리\n'.encode()
            powłoka('echo one > wyciąg_WARTOŚĆ; echo two >> wyciąg_WARTOŚĆ; echo three >> wyciąg_WARTOŚĆ')
            powłoka('cat < wyciąg_WARTOŚĆ | grep t | tee 추림 | wc -l','2\n'); assert nazwa_pliku('추림')==b'two\nthree\n'
            powłoka('head -n 1 wyciąg_WARTOŚĆ > przód_WARTOŚĆ; tail -n 1 wyciąg_WARTOŚĆ > BACK_WARTOŚĆ'); assert nazwa_pliku('앞')==b'one\n'; assert nazwa_pliku('뒤')==b'three\n'
            powłoka('grep absent wyciąg_WARTOŚĆ; echo $?','1\n')
            powłoka('echo untouched > chronić_WARTOŚĆ')
            powłoka('echo destroyed > chronić_WARTOŚĆ |','명령이 빠졌습니다'); assert nazwa_pliku('chronić_WARTOŚĆ')==b'untouched\n'
            powłoka('echo "oops','따옴표가 닫히지 않았습니다')
            powłoka('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            powłoka('echo bad 2> chronić_WARTOŚĆ','번호를 지정한 nazwa_pliku deskryptor_wpis We_Wy zmiana_tryb'); assert nazwa_pliku('chronić_WARTOŚĆ')==b'untouched\n'
            powłoka('rm 빈파일 리터럴 wyciąg_WARTOŚĆ 추림 przód_WARTOŚĆ BACK_WARTOŚĆ chronić_WARTOŚĆ')
            walidacja_Raport['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            powłoka("python -c 'print(123)' | wc -c",'4\n')
            powłoka("python -c 'print(456)' > program_f5044b9b.txt"); assert nazwa_pliku('program_f5044b9b.txt')==b'456\n'
            powłoka("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            powłoka("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < program_f5044b9b.txt", "b'456\\n'", "b''")
            powłoka("python -c 'print(\"x\"*17000)' | wc -c", 'błąd -28')
            powłoka('echo recovered | wc -c','10\n')
            powłoka("python -c 'import jkoros; print(jkoros.read("+'"/작업/program_f5044b9b.txt"'+"))'",'456','exit 0')
            powłoka('cd /; javac Hello.java','Compiled:','exit 0')
            powłoka('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in nazwa_pliku('/작업/자바.txt')
            powłoka('cd 작업; echo "echo script > wykonanie_KR" > polecenie.sh; echo "false || echo recovered >> wykonanie_KR" >> polecenie.sh; sh polecenie.sh')
            assert nazwa_pliku('wykonanie_KR')==b'script\nrecovered\n'
            powłoka('rm wykonanie_KR; echo "exit 7" > wyjść_program.sh; sh wyjść_program.sh; echo $?','7\n')
            powłoka('rm wyjść_program.sh polecenie.sh program_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            walidacja_Raport['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            powłoka('echo history-proof','history-proof')
            WYNIK=wysłać(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert WYNIK.count('history-proof')>=2, WYNIK
            wysłać(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            WYNIK=wysłać(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in WYNIK, WYNIK
            WYNIK=wysłać(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in WYNIK,WYNIK
            WYNIK=wysłać('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in WYNIK,WYNIK
            긴글='한글'*50
            WYNIK=wysłać(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in WYNIK
            powłoka('terminal','TERMINAL READY')
            powłoka('clear')
            powłoka('echo "한글 interpretator_poleceń ABC xyz 012 😀"','한글 interpretator_poleceń ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klient:
                klient.settimeout(10); klient.connect(str(모의제어접속))
                with klient.makefile('rwb') as Stream_WARTOŚĆ:
                    json.loads(Stream_WARTOŚĆ.readline())
                    def 호출(Nazwa,argument_TABLICA=None):
                        sieć_e_mail={'execute':Nazwa}
                        if argument_TABLICA: sieć_e_mail['arguments']=argument_TABLICA
                        Stream_WARTOŚĆ.write((json.dumps(sieć_e_mail)+'\n').encode()); Stream_WARTOŚĆ.flush()
                        while True:
                            odpowiedź=json.loads(Stream_WARTOŚĆ.readline())
                            if 'error' in odpowiedź: raise AssertionError(odpowiedź)
                            if 'return' in odpowiedź: return odpowiedź['return']
                    호출('qmp_capabilities')
                    OBRAZ=produkt_wyjściowy/'terminal.ppm'; 호출('screendump',{'filename':str(OBRAZ),'format':'ppm'})
                    호출('screendump',{'filename':str(produkt_wyjściowy/'terminal.png'),'format':'png'})
                    dane=OBRAZ.read_bytes().split(b'\n',3)[3]
                    def piksel(współrzędna_X,Y_współrzędna): return tuple(dane[(Y_współrzędna*640+współrzędna_X)*3:(Y_współrzędna*640+współrzędna_X)*3+3])
                    assert piksel(12,48)==(32,80,144),piksel(12,48)
                    assert len(set(piksel(współrzędna_X,Y_współrzędna) for Y_współrzędna in range(100,116) for współrzędna_X in range(24,56)))>1,'Hangul glyphs missing'
                    powłoka('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    powłoka("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(OBRAZ),'format':'ppm'})
                    복원자료=OBRAZ.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    powłoka('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): powłoka('echo scroll-'+str(순번),'scroll-'+str(순번))
                    wysłać(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(produkt_wyjściowy/'terminal-scroll.png'),'format':'png'})
                    WYNIK=wysłać(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in WYNIK,WYNIK
                    powłoka('rm visible.txt')
                    호출('quit')
            Proces.wait(timeout=5)
            walidacja_Raport['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            walidacja_Raport['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proces.poll() is None:
                Proces.terminate()
                try: Proces.wait(timeout=5)
                except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
            준비살피미.close(); Proces.stdin.close(); Proces.stdout.close()
            (produkt_wyjściowy/'serial.log').write_bytes(transkrypcja)
            (produkt_wyjściowy/'report.json').write_text(json.dumps(walidacja_Raport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Uruchom_2()
