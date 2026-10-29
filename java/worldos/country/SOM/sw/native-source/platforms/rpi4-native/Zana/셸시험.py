#!/usr/bin/env python3
"""자체 커널의 sheli, 프로세스 I_T, Unicode GUI 터미널을 halisi_data raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from tekeleza_amri import 기준, amri


def endesha():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    uhakikishi_ripoti = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Mchakato = subprocess.Popen(amri()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Mchakato.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            data=bytearray(); tamatia_Chipua=time.monotonic()+시간제한
            while 확인표시 not in data:
                if time.monotonic()>tamatia_Chipua or Mchakato.poll() is not None: raise AssertionError('UART timeout/exit: '+data.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8','replace').replace('\r\n','\n')
        def tuma(data, 확인표시=b'jkoros-native> '):
            Mchakato.stdin.write(data); Mchakato.stdin.flush(); return 수신하기(확인표시)
        def sheli(laini, *예상결과):
            결과=tuma(laini.encode()+b'\n')
            for thamani in 예상결과: assert thamani in 결과, (laini,thamani,결과)
            return 결과
        def faili(Jina):
            SMS=sheli('hex '+Jina,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',SMS,re.S)
            data=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(data)==int(찾은결과.group(1)); return data
        try:
            수신하기(b'jkoros-native> ')
            sheli('mkdir 작업; cd 작업; pwd','/작업')
            sheli('mkdir 하위; echo "한글 data 😀" > 인사.txt')
            assert faili('인사.txt')=='한글 data 😀\n'.encode()
            sheli('cp 인사.txt mfano_thamani.txt; mv mfano_thamani.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 data 😀')
            sheli('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 data 😀','/작업/하위')
            sheli('cd ..; rmdir 하위; echo $?','1\n')
            sheli('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            sheli('cp 인사.txt 인사.txt; echo $?','1\n'); assert faili('인사.txt')=='한글 data 😀\n'.encode()
            sheli('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in faili('인사.txt')
            sheli("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert faili('리터럴')=='$인사\n누리\n'.encode()
            sheli('echo one > kauli_thamani; echo two >> kauli_thamani; echo three >> kauli_thamani')
            sheli('cat < kauli_thamani | grep t | tee 추림 | wc -l','2\n'); assert faili('추림')==b'two\nthree\n'
            sheli('head -n 1 kauli_thamani > mbele_thamani; tail -n 1 kauli_thamani > Nyuma_thamani'); assert faili('앞')==b'one\n'; assert faili('뒤')==b'three\n'
            sheli('grep absent kauli_thamani; echo $?','1\n')
            sheli('echo untouched > linda_thamani')
            sheli('echo destroyed > linda_thamani |','명령이 빠졌습니다'); assert faili('linda_thamani')==b'untouched\n'
            sheli('echo "oops','따옴표가 닫히지 않았습니다')
            sheli('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            sheli('echo bad 2> linda_thamani','번호를 지정한 faili 서술자 I_T badili_hali_tumizi'); assert faili('linda_thamani')==b'untouched\n'
            sheli('rm 빈파일 리터럴 kauli_thamani 추림 mbele_thamani Nyuma_thamani linda_thamani')
            uhakikishi_ripoti['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            sheli("python -c 'print(123)' | wc -c",'4\n')
            sheli("python -c 'print(456)' > programu_f5044b9b.txt"); assert faili('programu_f5044b9b.txt')==b'456\n'
            sheli("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            sheli("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < programu_f5044b9b.txt", "b'456\\n'", "b''")
            sheli("python -c 'print(\"x\"*17000)' | wc -c", 'kosa -28')
            sheli('echo recovered | wc -c','10\n')
            sheli("python -c 'import jkoros; print(jkoros.read("+'"/작업/programu_f5044b9b.txt"'+"))'",'456','exit 0')
            sheli('cd /; javac Hello.java','Compiled:','exit 0')
            sheli('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in faili('/작업/자바.txt')
            sheli('cd 작업; echo "echo script > 실행결과" > amri.sh; echo "false || echo recovered >> 실행결과" >> amri.sh; sh amri.sh')
            assert faili('실행결과')==b'script\nrecovered\n'
            sheli('rm 실행결과; echo "exit 7" > toka_programu.sh; sh toka_programu.sh; echo $?','7\n')
            sheli('rm toka_programu.sh amri.sh programu_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            uhakikishi_ripoti['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            sheli('echo history-proof','history-proof')
            결과=tuma(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            tuma(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=tuma(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=tuma(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=tuma('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=tuma(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            sheli('terminal','TERMINAL READY')
            sheli('clear')
            sheli('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as teja:
                teja.settimeout(10); teja.connect(str(모의제어접속))
                with teja.makefile('rwb') as Stream_thamani:
                    json.loads(Stream_thamani.readline())
                    def 호출(Jina,hoja_ARRAY=None):
                        Mtandao_ujumbe={'execute':Jina}
                        if hoja_ARRAY: Mtandao_ujumbe['arguments']=hoja_ARRAY
                        Stream_thamani.write((json.dumps(Mtandao_ujumbe)+'\n').encode()); Stream_thamani.flush()
                        while True:
                            jibu=json.loads(Stream_thamani.readline())
                            if 'error' in jibu: raise AssertionError(jibu)
                            if 'return' in jibu: return jibu['return']
                    호출('qmp_capabilities')
                    picha=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(picha),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    data=picha.read_bytes().split(b'\n',3)[3]
                    def elepi(jira_x,Kitufe_cha_Y_kiratibu): return tuple(data[(Kitufe_cha_Y_kiratibu*640+jira_x)*3:(Kitufe_cha_Y_kiratibu*640+jira_x)*3+3])
                    assert elepi(12,48)==(32,80,144),elepi(12,48)
                    assert len(set(elepi(jira_x,Kitufe_cha_Y_kiratibu) for Kitufe_cha_Y_kiratibu in range(100,116) for jira_x in range(24,56)))>1,'Hangul glyphs missing'
                    sheli('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    sheli("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(picha),'format':'ppm'})
                    복원자료=picha.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    sheli('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): sheli('echo scroll-'+str(순번),'scroll-'+str(순번))
                    tuma(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=tuma(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    sheli('rm visible.txt')
                    호출('quit')
            Mchakato.wait(timeout=5)
            uhakikishi_ripoti['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            uhakikishi_ripoti['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Mchakato.poll() is None:
                Mchakato.terminate()
                try: Mchakato.wait(timeout=5)
                except subprocess.TimeoutExpired: Mchakato.kill(); Mchakato.wait()
            준비살피미.close(); Mchakato.stdin.close(); Mchakato.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(uhakikishi_ripoti,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': endesha()
