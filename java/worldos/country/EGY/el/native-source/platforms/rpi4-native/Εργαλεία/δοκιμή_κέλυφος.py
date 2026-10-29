#!/usr/bin/env python3
"""ίδιο 커널의 κέλυφος, 프로세스 είσοδος_έξοδος, Unicode GUI 터미널을 πραγματικός_δεδομένα raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from εκτελώ_εντολή import έργο_ρίζα, Εντολή


def Εκτέλεση_2():
    출력결과 = έργο_ρίζα / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    επικύρωση_έκθεση = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((έργο_ρίζα / 'build/kernel8.img').read_bytes()).hexdigest()}
    μεταγραφή = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Διεργασία = subprocess.Popen(Εντολή()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Διεργασία.stdout,selectors.EVENT_READ)
        def λαμβάνω_μήνυμα(δείκτης_8b722c5f, εκτέλεση_ΤΕΛΟΣ_ΧΡΟΝΟΥ=45):
            δεδομένα=bytearray(); Τελική_οντότητα_Υπέρθεση=time.monotonic()+εκτέλεση_ΤΕΛΟΣ_ΧΡΟΝΟΥ
            while δείκτης_8b722c5f not in δεδομένα:
                if time.monotonic()>Τελική_οντότητα_Υπέρθεση or Διεργασία.poll() is not None: raise AssertionError('UART timeout/exit: '+δεδομένα.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: δεδομένα.extend(조각); μεταγραφή.extend(조각)
                if b'PANIC:' in δεδομένα or b'FAIL ' in δεδομένα: raise AssertionError(δεδομένα)
            return δεδομένα.decode('utf-8','replace').replace('\r\n','\n')
        def στέλνω(δεδομένα, δείκτης_8b722c5f=b'jkoros-native> '):
            Διεργασία.stdin.write(δεδομένα); Διεργασία.stdin.flush(); return λαμβάνω_μήνυμα(δείκτης_8b722c5f)
        def κέλυφος(Γραμμή, *예상결과):
            μέτρηση=στέλνω(Γραμμή.encode()+b'\n')
            for τιμή in 예상결과: assert τιμή in μέτρηση, (Γραμμή,τιμή,μέτρηση)
            return μέτρηση
        def Αρχείο(Όνομα):
            Κείμενο=κέλυφος('hex '+Όνομα,'HEX BEGIN','HEX END'); αναζητώ_μέτρηση=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Κείμενο,re.S)
            δεδομένα=bytes.fromhex(''.join(αναζητώ_μέτρηση.group(2).split())); assert len(δεδομένα)==int(αναζητώ_μέτρηση.group(1)); return δεδομένα
        try:
            λαμβάνω_μήνυμα(b'jkoros-native> ')
            κέλυφος('mkdir 작업; cd 작업; pwd','/작업')
            κέλυφος('mkdir 하위; echo "한글 δεδομένα 😀" > 인사.txt')
            assert Αρχείο('인사.txt')=='한글 δεδομένα 😀\n'.encode()
            κέλυφος('cp 인사.txt παρουσία_τιμή.txt; mv παρουσία_τιμή.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 δεδομένα 😀')
            κέλυφος('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 δεδομένα 😀','/작업/하위')
            κέλυφος('cd ..; rmdir 하위; echo $?','1\n')
            κέλυφος('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            κέλυφος('cp 인사.txt 인사.txt; echo $?','1\n'); assert Αρχείο('인사.txt')=='한글 δεδομένα 😀\n'.encode()
            κέλυφος('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Αρχείο('인사.txt')
            κέλυφος("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Αρχείο('리터럴')=='$인사\n누리\n'.encode()
            κέλυφος('echo one > Πρόταση_τιμή; echo two >> Πρόταση_τιμή; echo three >> Πρόταση_τιμή')
            κέλυφος('cat < Πρόταση_τιμή | grep t | tee 추림 | wc -l','2\n'); assert Αρχείο('추림')==b'two\nthree\n'
            κέλυφος('head -n 1 Πρόταση_τιμή > μπροστινή_τιμή; tail -n 1 Πρόταση_τιμή > Πίσω_τιμή'); assert Αρχείο('앞')==b'one\n'; assert Αρχείο('뒤')==b'three\n'
            κέλυφος('grep absent Πρόταση_τιμή; echo $?','1\n')
            κέλυφος('echo untouched > προστασία_τιμή')
            κέλυφος('echo destroyed > προστασία_τιμή |','명령이 빠졌습니다'); assert Αρχείο('προστασία_τιμή')==b'untouched\n'
            κέλυφος('echo "oops','따옴표가 닫히지 않았습니다')
            κέλυφος('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            κέλυφος('echo bad 2> προστασία_τιμή','번호를 지정한 Αρχείο 서술자 είσοδος_έξοδος αλλάζω_λειτουργία'); assert Αρχείο('προστασία_τιμή')==b'untouched\n'
            κέλυφος('rm 빈파일 리터럴 Πρόταση_τιμή 추림 μπροστινή_τιμή Πίσω_τιμή προστασία_τιμή')
            επικύρωση_έκθεση['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            κέλυφος("python -c 'print(123)' | wc -c",'4\n')
            κέλυφος("python -c 'print(456)' > εφαρμογή_f5044b9b.txt"); assert Αρχείο('εφαρμογή_f5044b9b.txt')==b'456\n'
            κέλυφος("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            κέλυφος("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < εφαρμογή_f5044b9b.txt", "b'456\\n'", "b''")
            κέλυφος("python -c 'print(\"x\"*17000)' | wc -c", 'ΣΦΑΛΜΑ -28')
            κέλυφος('echo recovered | wc -c','10\n')
            κέλυφος("python -c 'import jkoros; print(jkoros.read("+'"/작업/εφαρμογή_f5044b9b.txt"'+"))'",'456','exit 0')
            κέλυφος('cd /; javac Hello.java','Compiled:','exit 0')
            κέλυφος('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Αρχείο('/작업/자바.txt')
            κέλυφος('cd 작업; echo "echo script > εκτέλεση_μέτρηση" > Εντολή.sh; echo "false || echo recovered >> εκτέλεση_μέτρηση" >> Εντολή.sh; sh Εντολή.sh')
            assert Αρχείο('εκτέλεση_μέτρηση')==b'script\nrecovered\n'
            κέλυφος('rm εκτέλεση_μέτρηση; echo "exit 7" > Έξοδος_εφαρμογή.sh; sh Έξοδος_εφαρμογή.sh; echo $?','7\n')
            κέλυφος('rm Έξοδος_εφαρμογή.sh Εντολή.sh εφαρμογή_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            επικύρωση_έκθεση['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            κέλυφος('echo history-proof','history-proof')
            μέτρηση=στέλνω(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert μέτρηση.count('history-proof')>=2, μέτρηση
            στέλνω(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            μέτρηση=στέλνω(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in μέτρηση, μέτρηση
            μέτρηση=στέλνω(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in μέτρηση,μέτρηση
            μέτρηση=στέλνω('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in μέτρηση,μέτρηση
            긴글='한글'*50
            μέτρηση=στέλνω(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in μέτρηση
            κέλυφος('terminal','TERMINAL READY')
            κέλυφος('clear')
            κέλυφος('echo "한글 Τερματικό ABC xyz 012 😀"','한글 Τερματικό ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as πελάτης:
                πελάτης.settimeout(10); πελάτης.connect(str(모의제어접속))
                with πελάτης.makefile('rwb') as ροή_τιμή:
                    json.loads(ροή_τιμή.readline())
                    def 호출(Όνομα,όρισμα_πίνακας=None):
                        δίκτυο_μήνυμα={'execute':Όνομα}
                        if όρισμα_πίνακας: δίκτυο_μήνυμα['arguments']=όρισμα_πίνακας
                        ροή_τιμή.write((json.dumps(δίκτυο_μήνυμα)+'\n').encode()); ροή_τιμή.flush()
                        while True:
                            απαντώ=json.loads(ροή_τιμή.readline())
                            if 'error' in απαντώ: raise AssertionError(απαντώ)
                            if 'return' in απαντώ: return απαντώ['return']
                    호출('qmp_capabilities')
                    εικόνα=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(εικόνα),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    δεδομένα=εικόνα.read_bytes().split(b'\n',3)[3]
                    def 화소(συντεταγμένη_x,κουμπί_Y_συντονισμός): return tuple(δεδομένα[(κουμπί_Y_συντονισμός*640+συντεταγμένη_x)*3:(κουμπί_Y_συντονισμός*640+συντεταγμένη_x)*3+3])
                    assert 화소(12,48)==(32,80,144),화소(12,48)
                    assert len(set(화소(συντεταγμένη_x,κουμπί_Y_συντονισμός) for κουμπί_Y_συντονισμός in range(100,116) for συντεταγμένη_x in range(24,56)))>1,'Hangul glyphs missing'
                    κέλυφος('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    κέλυφος("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(εικόνα),'format':'ppm'})
                    복원자료=εικόνα.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    κέλυφος('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): κέλυφος('echo scroll-'+str(순번),'scroll-'+str(순번))
                    στέλνω(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    μέτρηση=στέλνω(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in μέτρηση,μέτρηση
                    κέλυφος('rm visible.txt')
                    호출('quit')
            Διεργασία.wait(timeout=5)
            επικύρωση_έκθεση['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            επικύρωση_έκθεση['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Διεργασία.poll() is None:
                Διεργασία.terminate()
                try: Διεργασία.wait(timeout=5)
                except subprocess.TimeoutExpired: Διεργασία.kill(); Διεργασία.wait()
            준비살피미.close(); Διεργασία.stdin.close(); Διεργασία.stdout.close()
            (출력결과/'serial.log').write_bytes(μεταγραφή)
            (출력결과/'report.json').write_text(json.dumps(επικύρωση_έκθεση,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Εκτέλεση_2()
