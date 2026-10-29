#!/usr/bin/env python3
"""자체 커널의 dop, 프로세스 I_O, Unicode GUI 터미널을 werklik_data raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from uitvoer_bevel import Project_wortel, Opdrag


def Loop():
    출력결과 = Project_wortel / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    validering_verslag = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Project_wortel / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proses = subprocess.Popen(Opdrag()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proses.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            data=bytearray(); beëindig_OFFSET=time.monotonic()+시간제한
            while 확인표시 not in data:
                if time.monotonic()>beëindig_OFFSET or Proses.poll() is not None: raise AssertionError('UART timeout/exit: '+data.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8','replace').replace('\r\n','\n')
        def e_pos(data, 확인표시=b'jkoros-native> '):
            Proses.stdin.write(data); Proses.stdin.flush(); return 수신하기(확인표시)
        def dop(lyn, *예상결과):
            maatreël=e_pos(lyn.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in maatreël, (lyn,VALUE,maatreël)
            return maatreël
        def Lêer(Naam):
            Teks=dop('hex '+Naam,'HEX BEGIN','HEX END'); Soek_maatreël=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Teks,re.S)
            data=bytes.fromhex(''.join(Soek_maatreël.group(2).split())); assert len(data)==int(Soek_maatreël.group(1)); return data
        try:
            수신하기(b'jkoros-native> ')
            dop('mkdir 작업; cd 작업; pwd','/작업')
            dop('mkdir 하위; echo "한글 data 😀" > 인사.txt')
            assert Lêer('인사.txt')=='한글 data 😀\n'.encode()
            dop('cp 인사.txt geval_VALUE.txt; mv geval_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 data 😀')
            dop('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 data 😀','/작업/하위')
            dop('cd ..; rmdir 하위; echo $?','1\n')
            dop('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            dop('cp 인사.txt 인사.txt; echo $?','1\n'); assert Lêer('인사.txt')=='한글 data 😀\n'.encode()
            dop('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Lêer('인사.txt')
            dop("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Lêer('리터럴')=='$인사\n누리\n'.encode()
            dop('echo one > stelling_VALUE; echo two >> stelling_VALUE; echo three >> stelling_VALUE')
            dop('cat < stelling_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Lêer('추림')==b'two\nthree\n'
            dop('head -n 1 stelling_VALUE > voor_VALUE; tail -n 1 stelling_VALUE > TERUG_VALUE'); assert Lêer('앞')==b'one\n'; assert Lêer('뒤')==b'three\n'
            dop('grep absent stelling_VALUE; echo $?','1\n')
            dop('echo untouched > beskerm_VALUE')
            dop('echo destroyed > beskerm_VALUE |','명령이 빠졌습니다'); assert Lêer('beskerm_VALUE')==b'untouched\n'
            dop('echo "oops','따옴표가 닫히지 않았습니다')
            dop('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            dop('echo bad 2> beskerm_VALUE','번호를 지정한 Lêer 서술자 I_O SWITCH_MODE'); assert Lêer('beskerm_VALUE')==b'untouched\n'
            dop('rm 빈파일 리터럴 stelling_VALUE 추림 voor_VALUE TERUG_VALUE beskerm_VALUE')
            validering_verslag['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            dop("python -c 'print(123)' | wc -c",'4\n')
            dop("python -c 'print(456)' > program_f5044b9b.txt"); assert Lêer('program_f5044b9b.txt')==b'456\n'
            dop("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            dop("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < program_f5044b9b.txt", "b'456\\n'", "b''")
            dop("python -c 'print(\"x\"*17000)' | wc -c", 'Fout -28')
            dop('echo recovered | wc -c','10\n')
            dop("python -c 'import jkoros; print(jkoros.read("+'"/작업/program_f5044b9b.txt"'+"))'",'456','exit 0')
            dop('cd /; javac Hello.java','Compiled:','exit 0')
            dop('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Lêer('/작업/자바.txt')
            dop('cd 작업; echo "echo script > 실행결과" > Opdrag.sh; echo "false || echo recovered >> 실행결과" >> Opdrag.sh; sh Opdrag.sh')
            assert Lêer('실행결과')==b'script\nrecovered\n'
            dop('rm 실행결과; echo "exit 7" > Verlaat_program.sh; sh Verlaat_program.sh; echo $?','7\n')
            dop('rm Verlaat_program.sh Opdrag.sh program_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            validering_verslag['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            dop('echo history-proof','history-proof')
            maatreël=e_pos(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert maatreël.count('history-proof')>=2, maatreël
            e_pos(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            maatreël=e_pos(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in maatreël, maatreël
            maatreël=e_pos(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in maatreël,maatreël
            maatreël=e_pos('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in maatreël,maatreël
            긴글='한글'*50
            maatreël=e_pos(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in maatreël
            dop('terminal','TERMINAL READY')
            dop('clear')
            dop('echo "한글 Terminaal ABC xyz 012 😀"','한글 Terminaal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as kliënt:
                kliënt.settimeout(10); kliënt.connect(str(모의제어접속))
                with kliënt.makefile('rwb') as Stream_VALUE:
                    json.loads(Stream_VALUE.readline())
                    def 호출(Naam,argument_ARRAY=None):
                        Netwerk_e_pos={'execute':Naam}
                        if argument_ARRAY: Netwerk_e_pos['arguments']=argument_ARRAY
                        Stream_VALUE.write((json.dumps(Netwerk_e_pos)+'\n').encode()); Stream_VALUE.flush()
                        while True:
                            antwoord=json.loads(Stream_VALUE.readline())
                            if 'error' in antwoord: raise AssertionError(antwoord)
                            if 'return' in antwoord: return antwoord['return']
                    호출('qmp_capabilities')
                    foto=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(foto),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    data=foto.read_bytes().split(b'\n',3)[3]
                    def pieksel(x_koördinaat,Y_koördinaat): return tuple(data[(Y_koördinaat*640+x_koördinaat)*3:(Y_koördinaat*640+x_koördinaat)*3+3])
                    assert pieksel(12,48)==(32,80,144),pieksel(12,48)
                    assert len(set(pieksel(x_koördinaat,Y_koördinaat) for Y_koördinaat in range(100,116) for x_koördinaat in range(24,56)))>1,'Hangul glyphs missing'
                    dop('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    dop("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(foto),'format':'ppm'})
                    복원자료=foto.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    dop('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): dop('echo scroll-'+str(순번),'scroll-'+str(순번))
                    e_pos(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    maatreël=e_pos(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in maatreël,maatreël
                    dop('rm visible.txt')
                    호출('quit')
            Proses.wait(timeout=5)
            validering_verslag['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            validering_verslag['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proses.poll() is None:
                Proses.terminate()
                try: Proses.wait(timeout=5)
                except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
            준비살피미.close(); Proses.stdin.close(); Proses.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(validering_verslag,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Loop()
