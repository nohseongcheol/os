#!/usr/bin/env python3
"""자체 커널의 isihumushi_miyalelo, 프로세스 i_I_O, Unicode GUI 터미널을 ulwazi_ngokwenzekile_imininingwane raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from yenza_umyalo import 기준, Umlayelo


def Sebenzisa():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    ukufakazisa_umbiko = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Inqubo = subprocess.Popen(Umlayelo()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Inqubo.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            imininingwane=bytearray(); yekisa_I_ofisethi=time.monotonic()+시간제한
            while 확인표시 not in imininingwane:
                if time.monotonic()>yekisa_I_ofisethi or Inqubo.poll() is not None: raise AssertionError('UART timeout/exit: '+imininingwane.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: imininingwane.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in imininingwane or b'FAIL ' in imininingwane: raise AssertionError(imininingwane)
            return imininingwane.decode('utf-8','replace').replace('\r\n','\n')
        def Thumela(imininingwane, 확인표시=b'jkoros-native> '):
            Inqubo.stdin.write(imininingwane); Inqubo.stdin.flush(); return 수신하기(확인표시)
        def isihumushi_miyalelo(umugqa, *예상결과):
            결과=Thumela(umugqa.encode()+b'\n')
            for inani in 예상결과: assert inani in 결과, (umugqa,inani,결과)
            return 결과
        def Ihele(Igama):
            Itekisi=isihumushi_miyalelo('hex '+Igama,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Itekisi,re.S)
            imininingwane=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(imininingwane)==int(찾은결과.group(1)); return imininingwane
        try:
            수신하기(b'jkoros-native> ')
            isihumushi_miyalelo('mkdir 작업; cd 작업; pwd','/작업')
            isihumushi_miyalelo('mkdir 하위; echo "한글 imininingwane 😀" > 인사.txt')
            assert Ihele('인사.txt')=='한글 imininingwane 😀\n'.encode()
            isihumushi_miyalelo('cp 인사.txt kopisha_inani.txt; mv kopisha_inani.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 imininingwane 😀')
            isihumushi_miyalelo('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 imininingwane 😀','/작업/하위')
            isihumushi_miyalelo('cd ..; rmdir 하위; echo $?','1\n')
            isihumushi_miyalelo('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            isihumushi_miyalelo('cp 인사.txt 인사.txt; echo $?','1\n'); assert Ihele('인사.txt')=='한글 imininingwane 😀\n'.encode()
            isihumushi_miyalelo('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Ihele('인사.txt')
            isihumushi_miyalelo("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Ihele('리터럴')=='$인사\n누리\n'.encode()
            isihumushi_miyalelo('echo one > isitatimende_inani; echo two >> isitatimende_inani; echo three >> isitatimende_inani')
            isihumushi_miyalelo('cat < isitatimende_inani | grep t | tee 추림 | wc -l','2\n'); assert Ihele('추림')==b'two\nthree\n'
            isihumushi_miyalelo('head -n 1 isitatimende_inani > 앞; tail -n 1 isitatimende_inani > Impindamuva_inani'); assert Ihele('앞')==b'one\n'; assert Ihele('뒤')==b'three\n'
            isihumushi_miyalelo('grep absent isitatimende_inani; echo $?','1\n')
            isihumushi_miyalelo('echo untouched > vikela_inani')
            isihumushi_miyalelo('echo destroyed > vikela_inani |','명령이 빠졌습니다'); assert Ihele('vikela_inani')==b'untouched\n'
            isihumushi_miyalelo('echo "oops','따옴표가 닫히지 않았습니다')
            isihumushi_miyalelo('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            isihumushi_miyalelo('echo bad 2> vikela_inani','번호를 지정한 Ihele 서술자 i_I_O guqulela_kokunye_inqubo'); assert Ihele('vikela_inani')==b'untouched\n'
            isihumushi_miyalelo('rm 빈파일 리터럴 isitatimende_inani 추림 앞 Impindamuva_inani vikela_inani')
            ukufakazisa_umbiko['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            isihumushi_miyalelo("python -c 'print(123)' | wc -c",'4\n')
            isihumushi_miyalelo("python -c 'print(456)' > i_app_f5044b9b.txt"); assert Ihele('i_app_f5044b9b.txt')==b'456\n'
            isihumushi_miyalelo("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            isihumushi_miyalelo("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < i_app_f5044b9b.txt", "b'456\\n'", "b''")
            isihumushi_miyalelo("python -c 'print(\"x\"*17000)' | wc -c", 'Iphutha -28')
            isihumushi_miyalelo('echo recovered | wc -c','10\n')
            isihumushi_miyalelo("python -c 'import jkoros; print(jkoros.read("+'"/작업/i_app_f5044b9b.txt"'+"))'",'456','exit 0')
            isihumushi_miyalelo('cd /; javac Hello.java','Compiled:','exit 0')
            isihumushi_miyalelo('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Ihele('/작업/자바.txt')
            isihumushi_miyalelo('cd 작업; echo "echo script > 실행결과" > Umlayelo.sh; echo "false || echo recovered >> 실행결과" >> Umlayelo.sh; sh Umlayelo.sh')
            assert Ihele('실행결과')==b'script\nrecovered\n'
            isihumushi_miyalelo('rm 실행결과; echo "exit 7" > phuma_i_app.sh; sh phuma_i_app.sh; echo $?','7\n')
            isihumushi_miyalelo('rm phuma_i_app.sh Umlayelo.sh i_app_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            ukufakazisa_umbiko['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            isihumushi_miyalelo('echo history-proof','history-proof')
            결과=Thumela(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            Thumela(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=Thumela(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=Thumela(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=Thumela('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=Thumela(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            isihumushi_miyalelo('terminal','TERMINAL READY')
            isihumushi_miyalelo('clear')
            isihumushi_miyalelo('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as iklayenti:
                iklayenti.settimeout(10); iklayenti.connect(str(모의제어접속))
                with iklayenti.makefile('rwb') as Stream_inani:
                    json.loads(Stream_inani.readline())
                    def 호출(Igama,i_agumenti_AMALUNGU_AFANAYO=None):
                        iNethiwekhi_umlayezo={'execute':Igama}
                        if i_agumenti_AMALUNGU_AFANAYO: iNethiwekhi_umlayezo['arguments']=i_agumenti_AMALUNGU_AFANAYO
                        Stream_inani.write((json.dumps(iNethiwekhi_umlayezo)+'\n').encode()); Stream_inani.flush()
                        while True:
                            phendula=json.loads(Stream_inani.readline())
                            if 'error' in phendula: raise AssertionError(phendula)
                            if 'return' in phendula: return phendula['return']
                    호출('qmp_capabilities')
                    isithombe=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(isithombe),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    imininingwane=isithombe.read_bytes().split(b'\n',3)[3]
                    def i_pel(okuxhumanisa_u_x,세로좌표): return tuple(imininingwane[(세로좌표*640+okuxhumanisa_u_x)*3:(세로좌표*640+okuxhumanisa_u_x)*3+3])
                    assert i_pel(12,48)==(32,80,144),i_pel(12,48)
                    assert len(set(i_pel(okuxhumanisa_u_x,세로좌표) for 세로좌표 in range(100,116) for okuxhumanisa_u_x in range(24,56)))>1,'Hangul glyphs missing'
                    isihumushi_miyalelo('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    isihumushi_miyalelo("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(isithombe),'format':'ppm'})
                    복원자료=isithombe.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    isihumushi_miyalelo('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): isihumushi_miyalelo('echo scroll-'+str(순번),'scroll-'+str(순번))
                    Thumela(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=Thumela(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    isihumushi_miyalelo('rm visible.txt')
                    호출('quit')
            Inqubo.wait(timeout=5)
            ukufakazisa_umbiko['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            ukufakazisa_umbiko['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Inqubo.poll() is None:
                Inqubo.terminate()
                try: Inqubo.wait(timeout=5)
                except subprocess.TimeoutExpired: Inqubo.kill(); Inqubo.wait()
            준비살피미.close(); Inqubo.stdin.close(); Inqubo.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(ukufakazisa_umbiko,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Sebenzisa()
