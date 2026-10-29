#!/usr/bin/env python3
"""자체 커널의 šele, 프로세스 I_O, Unicode GUI 터미널을 kgonthe_data raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from phethagatša_taelo import 기준, Taelo


def Diriša():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    tiišetšo_pego = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        tiragalo_a7054519 = subprocess.Popen(Taelo()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(tiragalo_a7054519.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            data=bytearray(); fetša_E_Šetšego=time.monotonic()+시간제한
            while 확인표시 not in data:
                if time.monotonic()>fetša_E_Šetšego or tiragalo_a7054519.poll() is not None: raise AssertionError('UART timeout/exit: '+data.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8','replace').replace('\r\n','\n')
        def Romela(data, 확인표시=b'jkoros-native> '):
            tiragalo_a7054519.stdin.write(data); tiragalo_a7054519.stdin.flush(); return 수신하기(확인표시)
        def šele(mothaladi, *예상결과):
            결과=Romela(mothaladi.encode()+b'\n')
            for boleng in 예상결과: assert boleng in 결과, (mothaladi,boleng,결과)
            return 결과
        def Faele(Leina):
            Sengwalwa=šele('hex '+Leina,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Sengwalwa,re.S)
            data=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(data)==int(찾은결과.group(1)); return data
        try:
            수신하기(b'jkoros-native> ')
            šele('mkdir 작업; cd 작업; pwd','/작업')
            šele('mkdir 하위; echo "한글 data 😀" > 인사.txt')
            assert Faele('인사.txt')=='한글 data 😀\n'.encode()
            šele('cp 인사.txt kopiša_boleng.txt; mv kopiša_boleng.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 data 😀')
            šele('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 data 😀','/작업/하위')
            šele('cd ..; rmdir 하위; echo $?','1\n')
            šele('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            šele('cp 인사.txt 인사.txt; echo $?','1\n'); assert Faele('인사.txt')=='한글 data 😀\n'.encode()
            šele('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Faele('인사.txt')
            šele("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Faele('리터럴')=='$인사\n누리\n'.encode()
            šele('echo one > setatamente_boleng; echo two >> setatamente_boleng; echo three >> setatamente_boleng')
            šele('cat < setatamente_boleng | grep t | tee 추림 | wc -l','2\n'); assert Faele('추림')==b'two\nthree\n'
            šele('head -n 1 setatamente_boleng > 앞; tail -n 1 setatamente_boleng > Morago_boleng'); assert Faele('앞')==b'one\n'; assert Faele('뒤')==b'three\n'
            šele('grep absent setatamente_boleng; echo $?','1\n')
            šele('echo untouched > šireletša_boleng')
            šele('echo destroyed > šireletša_boleng |','명령이 빠졌습니다'); assert Faele('šireletša_boleng')==b'untouched\n'
            šele('echo "oops','따옴표가 닫히지 않았습니다')
            šele('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            šele('echo bad 2> šireletša_boleng','번호를 지정한 Faele 서술자 I_O fetogela_mokgwa'); assert Faele('šireletša_boleng')==b'untouched\n'
            šele('rm 빈파일 리터럴 setatamente_boleng 추림 앞 Morago_boleng šireletša_boleng')
            tiišetšo_pego['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            šele("python -c 'print(123)' | wc -c",'4\n')
            šele("python -c 'print(456)' > tirišo_f5044b9b.txt"); assert Faele('tirišo_f5044b9b.txt')==b'456\n'
            šele("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            šele("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < tirišo_f5044b9b.txt", "b'456\\n'", "b''")
            šele("python -c 'print(\"x\"*17000)' | wc -c", 'Phošo -28')
            šele('echo recovered | wc -c','10\n')
            šele("python -c 'import jkoros; print(jkoros.read("+'"/작업/tirišo_f5044b9b.txt"'+"))'",'456','exit 0')
            šele('cd /; javac Hello.java','Compiled:','exit 0')
            šele('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Faele('/작업/자바.txt')
            šele('cd 작업; echo "echo script > 실행결과" > Taelo.sh; echo "false || echo recovered >> 실행결과" >> Taelo.sh; sh Taelo.sh')
            assert Faele('실행결과')==b'script\nrecovered\n'
            šele('rm 실행결과; echo "exit 7" > Etšwa_tirišo.sh; sh Etšwa_tirišo.sh; echo $?','7\n')
            šele('rm Etšwa_tirišo.sh Taelo.sh tirišo_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            tiišetšo_pego['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            šele('echo history-proof','history-proof')
            결과=Romela(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            Romela(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=Romela(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=Romela(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=Romela('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=Romela(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            šele('terminal','TERMINAL READY')
            šele('clear')
            šele('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klaente:
                klaente.settimeout(10); klaente.connect(str(모의제어접속))
                with klaente.makefile('rwb') as Stream_boleng:
                    json.loads(Stream_boleng.readline())
                    def 호출(Leina,akumente_arei=None):
                        Netweke_molaetša={'execute':Leina}
                        if akumente_arei: Netweke_molaetša['arguments']=akumente_arei
                        Stream_boleng.write((json.dumps(Netweke_molaetša)+'\n').encode()); Stream_boleng.flush()
                        while True:
                            fetola=json.loads(Stream_boleng.readline())
                            if 'error' in fetola: raise AssertionError(fetola)
                            if 'return' in fetola: return fetola['return']
                    호출('qmp_capabilities')
                    seswantšho=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(seswantšho),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    data=seswantšho.read_bytes().split(b'\n',3)[3]
                    def phele(kamano_ya_x,세로좌표): return tuple(data[(세로좌표*640+kamano_ya_x)*3:(세로좌표*640+kamano_ya_x)*3+3])
                    assert phele(12,48)==(32,80,144),phele(12,48)
                    assert len(set(phele(kamano_ya_x,세로좌표) for 세로좌표 in range(100,116) for kamano_ya_x in range(24,56)))>1,'Hangul glyphs missing'
                    šele('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    šele("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(seswantšho),'format':'ppm'})
                    복원자료=seswantšho.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    šele('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): šele('echo scroll-'+str(순번),'scroll-'+str(순번))
                    Romela(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=Romela(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    šele('rm visible.txt')
                    호출('quit')
            tiragalo_a7054519.wait(timeout=5)
            tiišetšo_pego['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            tiišetšo_pego['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if tiragalo_a7054519.poll() is None:
                tiragalo_a7054519.terminate()
                try: tiragalo_a7054519.wait(timeout=5)
                except subprocess.TimeoutExpired: tiragalo_a7054519.kill(); tiragalo_a7054519.wait()
            준비살피미.close(); tiragalo_a7054519.stdin.close(); tiragalo_a7054519.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(tiišetšo_pego,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Diriša()
