#!/usr/bin/env python3
"""자체 커널의 shell, 프로세스 I_O, Unicode GUI 터미널을 attwali_data raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from eżegwixxa_kmand import pprojetta_għerq, kmand


def serje():
    출력결과 = pprojetta_għerq / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    validazzjoni_rapport = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((pprojetta_għerq / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proċess = subprocess.Popen(kmand()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proċess.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            data=bytearray(); ttermina_OFFSET=time.monotonic()+시간제한
            while 확인표시 not in data:
                if time.monotonic()>ttermina_OFFSET or Proċess.poll() is not None: raise AssertionError('UART timeout/exit: '+data.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8','replace').replace('\r\n','\n')
        def bagħat(data, 확인표시=b'jkoros-native> '):
            Proċess.stdin.write(data); Proċess.stdin.flush(); return 수신하기(확인표시)
        def shell(linja, *예상결과):
            miżura=bagħat(linja.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in miżura, (linja,VALUE,miżura)
            return miżura
        def fajl(isem):
            SMS=shell('hex '+isem,'HEX BEGIN','HEX END'); SEARCH_miżura=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',SMS,re.S)
            data=bytes.fromhex(''.join(SEARCH_miżura.group(2).split())); assert len(data)==int(SEARCH_miżura.group(1)); return data
        try:
            수신하기(b'jkoros-native> ')
            shell('mkdir 작업; cd 작업; pwd','/작업')
            shell('mkdir 하위; echo "한글 data 😀" > 인사.txt')
            assert fajl('인사.txt')=='한글 data 😀\n'.encode()
            shell('cp 인사.txt kkopja_VALUE.txt; mv kkopja_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 data 😀')
            shell('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 data 😀','/작업/하위')
            shell('cd ..; rmdir 하위; echo $?','1\n')
            shell('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            shell('cp 인사.txt 인사.txt; echo $?','1\n'); assert fajl('인사.txt')=='한글 data 😀\n'.encode()
            shell('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in fajl('인사.txt')
            shell("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert fajl('리터럴')=='$인사\n누리\n'.encode()
            shell('echo one > struzzjoni_VALUE; echo two >> struzzjoni_VALUE; echo three >> struzzjoni_VALUE')
            shell('cat < struzzjoni_VALUE | grep t | tee 추림 | wc -l','2\n'); assert fajl('추림')==b'two\nthree\n'
            shell('head -n 1 struzzjoni_VALUE > 앞; tail -n 1 struzzjoni_VALUE > Lura_VALUE'); assert fajl('앞')==b'one\n'; assert fajl('뒤')==b'three\n'
            shell('grep absent struzzjoni_VALUE; echo $?','1\n')
            shell('echo untouched > pproteġa_VALUE')
            shell('echo destroyed > pproteġa_VALUE |','명령이 빠졌습니다'); assert fajl('pproteġa_VALUE')==b'untouched\n'
            shell('echo "oops','따옴표가 닫히지 않았습니다')
            shell('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            shell('echo bad 2> pproteġa_VALUE','번호를 지정한 fajl 서술자 I_O qaleb_MODE'); assert fajl('pproteġa_VALUE')==b'untouched\n'
            shell('rm 빈파일 리터럴 struzzjoni_VALUE 추림 앞 Lura_VALUE pproteġa_VALUE')
            validazzjoni_rapport['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            shell("python -c 'print(123)' | wc -c",'4\n')
            shell("python -c 'print(456)' > programm_f5044b9b.txt"); assert fajl('programm_f5044b9b.txt')==b'456\n'
            shell("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            shell("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < programm_f5044b9b.txt", "b'456\\n'", "b''")
            shell("python -c 'print(\"x\"*17000)' | wc -c", 'żball -28')
            shell('echo recovered | wc -c','10\n')
            shell("python -c 'import jkoros; print(jkoros.read("+'"/작업/programm_f5044b9b.txt"'+"))'",'456','exit 0')
            shell('cd /; javac Hello.java','Compiled:','exit 0')
            shell('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in fajl('/작업/자바.txt')
            shell('cd 작업; echo "echo script > 실행결과" > kmand.sh; echo "false || echo recovered >> 실행결과" >> kmand.sh; sh kmand.sh')
            assert fajl('실행결과')==b'script\nrecovered\n'
            shell('rm 실행결과; echo "exit 7" > Ħruġ_programm.sh; sh Ħruġ_programm.sh; echo $?','7\n')
            shell('rm Ħruġ_programm.sh kmand.sh programm_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            validazzjoni_rapport['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            shell('echo history-proof','history-proof')
            miżura=bagħat(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert miżura.count('history-proof')>=2, miżura
            bagħat(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            miżura=bagħat(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in miżura, miżura
            miżura=bagħat(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in miżura,miżura
            miżura=bagħat('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in miżura,miżura
            긴글='한글'*50
            miżura=bagħat(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in miżura
            shell('terminal','TERMINAL READY')
            shell('clear')
            shell('echo "한글 Terminal ABC xyz 012 😀"','한글 Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klijent:
                klijent.settimeout(10); klijent.connect(str(모의제어접속))
                with klijent.makefile('rwb') as Stream_VALUE:
                    json.loads(Stream_VALUE.readline())
                    def 호출(isem,argument_ARRAY=None):
                        netwerk_messaġġ={'execute':isem}
                        if argument_ARRAY: netwerk_messaġġ['arguments']=argument_ARRAY
                        Stream_VALUE.write((json.dumps(netwerk_messaġġ)+'\n').encode()); Stream_VALUE.flush()
                        while True:
                            wieġeb=json.loads(Stream_VALUE.readline())
                            if 'error' in wieġeb: raise AssertionError(wieġeb)
                            if 'return' in wieġeb: return wieġeb['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    data=IMAGE.read_bytes().split(b'\n',3)[3]
                    def pel(koordinat_x,세로좌표): return tuple(data[(세로좌표*640+koordinat_x)*3:(세로좌표*640+koordinat_x)*3+3])
                    assert pel(12,48)==(32,80,144),pel(12,48)
                    assert len(set(pel(koordinat_x,세로좌표) for 세로좌표 in range(100,116) for koordinat_x in range(24,56)))>1,'Hangul glyphs missing'
                    shell('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    shell("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    shell('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): shell('echo scroll-'+str(순번),'scroll-'+str(순번))
                    bagħat(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    miżura=bagħat(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in miżura,miżura
                    shell('rm visible.txt')
                    호출('quit')
            Proċess.wait(timeout=5)
            validazzjoni_rapport['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            validazzjoni_rapport['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proċess.poll() is None:
                Proċess.terminate()
                try: Proċess.wait(timeout=5)
                except subprocess.TimeoutExpired: Proċess.kill(); Proċess.wait()
            준비살피미.close(); Proċess.stdin.close(); Proċess.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(validazzjoni_rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': serje()
