#!/usr/bin/env python3
"""자체 커널의 isiniki_myalelo, 프로세스 i_I_O, Unicode GUI 터미널을 eyona_yenzekileyo_iingcombolo raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ukwenza_umyalelo import 기준, Umyalelo


def Phumeza():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    uqinisekiso_ingxelo = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Inkqubo = subprocess.Popen(Umyalelo()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Inkqubo.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            iingcombolo=bytearray(); phela_Ukulinganisa=time.monotonic()+시간제한
            while 확인표시 not in iingcombolo:
                if time.monotonic()>phela_Ukulinganisa or Inkqubo.poll() is not None: raise AssertionError('UART timeout/exit: '+iingcombolo.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: iingcombolo.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in iingcombolo or b'FAIL ' in iingcombolo: raise AssertionError(iingcombolo)
            return iingcombolo.decode('utf-8','replace').replace('\r\n','\n')
        def thumela(iingcombolo, 확인표시=b'jkoros-native> '):
            Inkqubo.stdin.write(iingcombolo); Inkqubo.stdin.flush(); return 수신하기(확인표시)
        def isiniki_myalelo(umgca, *예상결과):
            결과=thumela(umgca.encode()+b'\n')
            for ixabiso in 예상결과: assert ixabiso in 결과, (umgca,ixabiso,결과)
            return 결과
        def iFayili(Igama):
            Umbhalo=isiniki_myalelo('hex '+Igama,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Umbhalo,re.S)
            iingcombolo=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(iingcombolo)==int(찾은결과.group(1)); return iingcombolo
        try:
            수신하기(b'jkoros-native> ')
            isiniki_myalelo('mkdir 작업; cd 작업; pwd','/작업')
            isiniki_myalelo('mkdir 하위; echo "한글 iingcombolo 😀" > 인사.txt')
            assert iFayili('인사.txt')=='한글 iingcombolo 😀\n'.encode()
            isiniki_myalelo('cp 인사.txt kopa_ixabiso.txt; mv kopa_ixabiso.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 iingcombolo 😀')
            isiniki_myalelo('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 iingcombolo 😀','/작업/하위')
            isiniki_myalelo('cd ..; rmdir 하위; echo $?','1\n')
            isiniki_myalelo('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            isiniki_myalelo('cp 인사.txt 인사.txt; echo $?','1\n'); assert iFayili('인사.txt')=='한글 iingcombolo 😀\n'.encode()
            isiniki_myalelo('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in iFayili('인사.txt')
            isiniki_myalelo("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert iFayili('리터럴')=='$인사\n누리\n'.encode()
            isiniki_myalelo('echo one > ingxelo_ixabiso; echo two >> ingxelo_ixabiso; echo three >> ingxelo_ixabiso')
            isiniki_myalelo('cat < ingxelo_ixabiso | grep t | tee 추림 | wc -l','2\n'); assert iFayili('추림')==b'two\nthree\n'
            isiniki_myalelo('head -n 1 ingxelo_ixabiso > 앞; tail -n 1 ingxelo_ixabiso > Emva_ixabiso'); assert iFayili('앞')==b'one\n'; assert iFayili('뒤')==b'three\n'
            isiniki_myalelo('grep absent ingxelo_ixabiso; echo $?','1\n')
            isiniki_myalelo('echo untouched > khusela_ixabiso')
            isiniki_myalelo('echo destroyed > khusela_ixabiso |','명령이 빠졌습니다'); assert iFayili('khusela_ixabiso')==b'untouched\n'
            isiniki_myalelo('echo "oops','따옴표가 닫히지 않았습니다')
            isiniki_myalelo('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            isiniki_myalelo('echo bad 2> khusela_ixabiso','번호를 지정한 iFayili 서술자 i_I_O tshintshela_imo'); assert iFayili('khusela_ixabiso')==b'untouched\n'
            isiniki_myalelo('rm 빈파일 리터럴 ingxelo_ixabiso 추림 앞 Emva_ixabiso khusela_ixabiso')
            uqinisekiso_ingxelo['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            isiniki_myalelo("python -c 'print(123)' | wc -c",'4\n')
            isiniki_myalelo("python -c 'print(456)' > inkqubo_f5044b9b.txt"); assert iFayili('inkqubo_f5044b9b.txt')==b'456\n'
            isiniki_myalelo("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            isiniki_myalelo("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < inkqubo_f5044b9b.txt", "b'456\\n'", "b''")
            isiniki_myalelo("python -c 'print(\"x\"*17000)' | wc -c", 'Impazamo -28')
            isiniki_myalelo('echo recovered | wc -c','10\n')
            isiniki_myalelo("python -c 'import jkoros; print(jkoros.read("+'"/작업/inkqubo_f5044b9b.txt"'+"))'",'456','exit 0')
            isiniki_myalelo('cd /; javac Hello.java','Compiled:','exit 0')
            isiniki_myalelo('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in iFayili('/작업/자바.txt')
            isiniki_myalelo('cd 작업; echo "echo script > 실행결과" > Umyalelo.sh; echo "false || echo recovered >> 실행결과" >> Umyalelo.sh; sh Umyalelo.sh')
            assert iFayili('실행결과')==b'script\nrecovered\n'
            isiniki_myalelo('rm 실행결과; echo "exit 7" > phuma_inkqubo.sh; sh phuma_inkqubo.sh; echo $?','7\n')
            isiniki_myalelo('rm phuma_inkqubo.sh Umyalelo.sh inkqubo_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            uqinisekiso_ingxelo['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            isiniki_myalelo('echo history-proof','history-proof')
            결과=thumela(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            thumela(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=thumela(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=thumela(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=thumela('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=thumela(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            isiniki_myalelo('terminal','TERMINAL READY')
            isiniki_myalelo('clear')
            isiniki_myalelo('echo "한글 i_Terminal ABC xyz 012 😀"','한글 i_Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as iklayenti:
                iklayenti.settimeout(10); iklayenti.connect(str(모의제어접속))
                with iklayenti.makefile('rwb') as Stream_ixabiso:
                    json.loads(Stream_ixabiso.readline())
                    def 호출(Igama,isiniki_myalelo_ULUHLU=None):
                        Inethiwekhi_umyalezo={'execute':Igama}
                        if isiniki_myalelo_ULUHLU: Inethiwekhi_umyalezo['arguments']=isiniki_myalelo_ULUHLU
                        Stream_ixabiso.write((json.dumps(Inethiwekhi_umyalezo)+'\n').encode()); Stream_ixabiso.flush()
                        while True:
                            phendula=json.loads(Stream_ixabiso.readline())
                            if 'error' in phendula: raise AssertionError(phendula)
                            if 'return' in phendula: return phendula['return']
                    호출('qmp_capabilities')
                    umfanekiso=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(umfanekiso),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    iingcombolo=umfanekiso.read_bytes().split(b'\n',3)[3]
                    def i_pel(isilungelelanisi_x,세로좌표): return tuple(iingcombolo[(세로좌표*640+isilungelelanisi_x)*3:(세로좌표*640+isilungelelanisi_x)*3+3])
                    assert i_pel(12,48)==(32,80,144),i_pel(12,48)
                    assert len(set(i_pel(isilungelelanisi_x,세로좌표) for 세로좌표 in range(100,116) for isilungelelanisi_x in range(24,56)))>1,'Hangul glyphs missing'
                    isiniki_myalelo('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    isiniki_myalelo("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(umfanekiso),'format':'ppm'})
                    복원자료=umfanekiso.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    isiniki_myalelo('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): isiniki_myalelo('echo scroll-'+str(순번),'scroll-'+str(순번))
                    thumela(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=thumela(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    isiniki_myalelo('rm visible.txt')
                    호출('quit')
            Inkqubo.wait(timeout=5)
            uqinisekiso_ingxelo['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            uqinisekiso_ingxelo['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Inkqubo.poll() is None:
                Inkqubo.terminate()
                try: Inkqubo.wait(timeout=5)
                except subprocess.TimeoutExpired: Inkqubo.kill(); Inkqubo.wait()
            준비살피미.close(); Inkqubo.stdin.close(); Inkqubo.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(uqinisekiso_ingxelo,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Phumeza()
