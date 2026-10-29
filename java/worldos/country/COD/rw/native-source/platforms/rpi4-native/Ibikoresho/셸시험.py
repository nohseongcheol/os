#!/usr/bin/env python3
"""자체 커널의 insomamabwiriza, 프로세스 I_O, Unicode GUI 터미널을 nyakuri_amakurushingiro raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from gukora_ibwiriza import 기준, Icyo_wifuza


def ihuriro():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    iyemeza_raporo = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Inzira_a7054519 = subprocess.Popen(Icyo_wifuza()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Inzira_a7054519.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            amakurushingiro=bytearray(); kurangiza_Ofuseti=time.monotonic()+시간제한
            while 확인표시 not in amakurushingiro:
                if time.monotonic()>kurangiza_Ofuseti or Inzira_a7054519.poll() is not None: raise AssertionError('UART timeout/exit: '+amakurushingiro.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: amakurushingiro.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in amakurushingiro or b'FAIL ' in amakurushingiro: raise AssertionError(amakurushingiro)
            return amakurushingiro.decode('utf-8','replace').replace('\r\n','\n')
        def kohereza(amakurushingiro, 확인표시=b'jkoros-native> '):
            Inzira_a7054519.stdin.write(amakurushingiro); Inzira_a7054519.stdin.flush(); return 수신하기(확인표시)
        def insomamabwiriza(umurongo, *예상결과):
            결과=kohereza(umurongo.encode()+b'\n')
            for agaciro in 예상결과: assert agaciro in 결과, (umurongo,agaciro,결과)
            return 결과
        def Idosiye(Izina):
            Umwandiko=insomamabwiriza('hex '+Izina,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Umwandiko,re.S)
            amakurushingiro=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(amakurushingiro)==int(찾은결과.group(1)); return amakurushingiro
        try:
            수신하기(b'jkoros-native> ')
            insomamabwiriza('mkdir 작업; cd 작업; pwd','/작업')
            insomamabwiriza('mkdir 하위; echo "한글 amakurushingiro 😀" > 인사.txt')
            assert Idosiye('인사.txt')=='한글 amakurushingiro 😀\n'.encode()
            insomamabwiriza('cp 인사.txt kopi_agaciro.txt; mv kopi_agaciro.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 amakurushingiro 😀')
            insomamabwiriza('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 amakurushingiro 😀','/작업/하위')
            insomamabwiriza('cd ..; rmdir 하위; echo $?','1\n')
            insomamabwiriza('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            insomamabwiriza('cp 인사.txt 인사.txt; echo $?','1\n'); assert Idosiye('인사.txt')=='한글 amakurushingiro 😀\n'.encode()
            insomamabwiriza('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Idosiye('인사.txt')
            insomamabwiriza("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Idosiye('리터럴')=='$인사\n누리\n'.encode()
            insomamabwiriza('echo one > ibwiriza_agaciro; echo two >> ibwiriza_agaciro; echo three >> ibwiriza_agaciro')
            insomamabwiriza('cat < ibwiriza_agaciro | grep t | tee 추림 | wc -l','2\n'); assert Idosiye('추림')==b'two\nthree\n'
            insomamabwiriza('head -n 1 ibwiriza_agaciro > 앞; tail -n 1 ibwiriza_agaciro > Ikibanza_agaciro'); assert Idosiye('앞')==b'one\n'; assert Idosiye('뒤')==b'three\n'
            insomamabwiriza('grep absent ibwiriza_agaciro; echo $?','1\n')
            insomamabwiriza('echo untouched > kurinda_agaciro')
            insomamabwiriza('echo destroyed > kurinda_agaciro |','명령이 빠졌습니다'); assert Idosiye('kurinda_agaciro')==b'untouched\n'
            insomamabwiriza('echo "oops','따옴표가 닫히지 않았습니다')
            insomamabwiriza('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            insomamabwiriza('echo bad 2> kurinda_agaciro','번호를 지정한 Idosiye 서술자 I_O guhinduranya_uburyo'); assert Idosiye('kurinda_agaciro')==b'untouched\n'
            insomamabwiriza('rm 빈파일 리터럴 ibwiriza_agaciro 추림 앞 Ikibanza_agaciro kurinda_agaciro')
            iyemeza_raporo['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            insomamabwiriza("python -c 'print(123)' | wc -c",'4\n')
            insomamabwiriza("python -c 'print(456)' > porogaramu_f5044b9b.txt"); assert Idosiye('porogaramu_f5044b9b.txt')==b'456\n'
            insomamabwiriza("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            insomamabwiriza("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < porogaramu_f5044b9b.txt", "b'456\\n'", "b''")
            insomamabwiriza("python -c 'print(\"x\"*17000)' | wc -c", 'IKOSA -28')
            insomamabwiriza('echo recovered | wc -c','10\n')
            insomamabwiriza("python -c 'import jkoros; print(jkoros.read("+'"/작업/porogaramu_f5044b9b.txt"'+"))'",'456','exit 0')
            insomamabwiriza('cd /; javac Hello.java','Compiled:','exit 0')
            insomamabwiriza('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Idosiye('/작업/자바.txt')
            insomamabwiriza('cd 작업; echo "echo script > 실행결과" > Icyo_wifuza.sh; echo "false || echo recovered >> 실행결과" >> Icyo_wifuza.sh; sh Icyo_wifuza.sh')
            assert Idosiye('실행결과')==b'script\nrecovered\n'
            insomamabwiriza('rm 실행결과; echo "exit 7" > gusohoka_porogaramu.sh; sh gusohoka_porogaramu.sh; echo $?','7\n')
            insomamabwiriza('rm gusohoka_porogaramu.sh Icyo_wifuza.sh porogaramu_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            iyemeza_raporo['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            insomamabwiriza('echo history-proof','history-proof')
            결과=kohereza(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            kohereza(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=kohereza(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=kohereza(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=kohereza('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=kohereza(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            insomamabwiriza('terminal','TERMINAL READY')
            insomamabwiriza('clear')
            insomamabwiriza('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as umukiriya:
                umukiriya.settimeout(10); umukiriya.connect(str(모의제어접속))
                with umukiriya.makefile('rwb') as Stream_agaciro:
                    json.loads(Stream_agaciro.readline())
                    def 호출(Izina,ingingo_ARRAY=None):
                        Urusobemiyoboro_ubutumwa={'execute':Izina}
                        if ingingo_ARRAY: Urusobemiyoboro_ubutumwa['arguments']=ingingo_ARRAY
                        Stream_agaciro.write((json.dumps(Urusobemiyoboro_ubutumwa)+'\n').encode()); Stream_agaciro.flush()
                        while True:
                            gusubiza=json.loads(Stream_agaciro.readline())
                            if 'error' in gusubiza: raise AssertionError(gusubiza)
                            if 'return' in gusubiza: return gusubiza['return']
                    호출('qmp_capabilities')
                    ishusho=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(ishusho),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    amakurushingiro=ishusho.read_bytes().split(b'\n',3)[3]
                    def pel(Ihuza_rya_x,세로좌표): return tuple(amakurushingiro[(세로좌표*640+Ihuza_rya_x)*3:(세로좌표*640+Ihuza_rya_x)*3+3])
                    assert pel(12,48)==(32,80,144),pel(12,48)
                    assert len(set(pel(Ihuza_rya_x,세로좌표) for 세로좌표 in range(100,116) for Ihuza_rya_x in range(24,56)))>1,'Hangul glyphs missing'
                    insomamabwiriza('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    insomamabwiriza("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(ishusho),'format':'ppm'})
                    복원자료=ishusho.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    insomamabwiriza('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): insomamabwiriza('echo scroll-'+str(순번),'scroll-'+str(순번))
                    kohereza(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=kohereza(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    insomamabwiriza('rm visible.txt')
                    호출('quit')
            Inzira_a7054519.wait(timeout=5)
            iyemeza_raporo['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            iyemeza_raporo['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Inzira_a7054519.poll() is None:
                Inzira_a7054519.terminate()
                try: Inzira_a7054519.wait(timeout=5)
                except subprocess.TimeoutExpired: Inzira_a7054519.kill(); Inzira_a7054519.wait()
            준비살피미.close(); Inzira_a7054519.stdin.close(); Inzira_a7054519.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(iyemeza_raporo,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ihuriro()
