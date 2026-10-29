#!/usr/bin/env python3
"""eigin 커널의 skel, 프로세스 I_Ú, Unicode GUI 터미널을 raun_gögn raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from keyra_skipun import verk_rót, Skipun


def Keyra_2():
    úttak_54cd5e1d = verk_rót / 'build/verification/shell'; úttak_54cd5e1d.mkdir(parents=True, exist_ok=True)
    prófun_skrá = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((verk_rót / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Ferli = subprocess.Popen(Skipun()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Ferli.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            gögn=bytearray(); ljúka_OFFSET=time.monotonic()+시간제한
            while 확인표시 not in gögn:
                if time.monotonic()>ljúka_OFFSET or Ferli.poll() is not None: raise AssertionError('UART timeout/exit: '+gögn.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: gögn.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in gögn or b'FAIL ' in gögn: raise AssertionError(gögn)
            return gögn.decode('utf-8','replace').replace('\r\n','\n')
        def senda(gögn, 확인표시=b'jkoros-native> '):
            Ferli.stdin.write(gögn); Ferli.stdin.flush(); return 수신하기(확인표시)
        def skel(Lína, *예상결과):
            NIÐURSTAÐA=senda(Lína.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in NIÐURSTAÐA, (Lína,VALUE,NIÐURSTAÐA)
            return NIÐURSTAÐA
        def Skrá(Heiti):
            Texti=skel('hex '+Heiti,'HEX BEGIN','HEX END'); Leit_mæld_stærð=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Texti,re.S)
            gögn=bytes.fromhex(''.join(Leit_mæld_stærð.group(2).split())); assert len(gögn)==int(Leit_mæld_stærð.group(1)); return gögn
        try:
            수신하기(b'jkoros-native> ')
            skel('mkdir 작업; cd 작업; pwd','/작업')
            skel('mkdir 하위; echo "한글 gögn 😀" > 인사.txt')
            assert Skrá('인사.txt')=='한글 gögn 😀\n'.encode()
            skel('cp 인사.txt afrita_VALUE.txt; mv afrita_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 gögn 😀')
            skel('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 gögn 😀','/작업/하위')
            skel('cd ..; rmdir 하위; echo $?','1\n')
            skel('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            skel('cp 인사.txt 인사.txt; echo $?','1\n'); assert Skrá('인사.txt')=='한글 gögn 😀\n'.encode()
            skel('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Skrá('인사.txt')
            skel("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Skrá('리터럴')=='$인사\n누리\n'.encode()
            skel('echo one > setning_VALUE; echo two >> setning_VALUE; echo three >> setning_VALUE')
            skel('cat < setning_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Skrá('추림')==b'two\nthree\n'
            skel('head -n 1 setning_VALUE > myndavél_að_framan_VALUE; tail -n 1 setning_VALUE > TIL_BAKA_VALUE'); assert Skrá('앞')==b'one\n'; assert Skrá('뒤')==b'three\n'
            skel('grep absent setning_VALUE; echo $?','1\n')
            skel('echo untouched > verja_VALUE')
            skel('echo destroyed > verja_VALUE |','명령이 빠졌습니다'); assert Skrá('verja_VALUE')==b'untouched\n'
            skel('echo "oops','따옴표가 닫히지 않았습니다')
            skel('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            skel('echo bad 2> verja_VALUE','번호를 지정한 Skrá 서술자 I_Ú SWITCH_MODE'); assert Skrá('verja_VALUE')==b'untouched\n'
            skel('rm 빈파일 리터럴 setning_VALUE 추림 myndavél_að_framan_VALUE TIL_BAKA_VALUE verja_VALUE')
            prófun_skrá['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            skel("python -c 'print(123)' | wc -c",'4\n')
            skel("python -c 'print(456)' > forrit_f5044b9b.txt"); assert Skrá('forrit_f5044b9b.txt')==b'456\n'
            skel("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            skel("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < forrit_f5044b9b.txt", "b'456\\n'", "b''")
            skel("python -c 'print(\"x\"*17000)' | wc -c", 'Villa -28')
            skel('echo recovered | wc -c','10\n')
            skel("python -c 'import jkoros; print(jkoros.read("+'"/작업/forrit_f5044b9b.txt"'+"))'",'456','exit 0')
            skel('cd /; javac Hello.java','Compiled:','exit 0')
            skel('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Skrá('/작업/자바.txt')
            skel('cd 작업; echo "echo script > 실행결과" > Skipun.sh; echo "false || echo recovered >> 실행결과" >> Skipun.sh; sh Skipun.sh')
            assert Skrá('실행결과')==b'script\nrecovered\n'
            skel('rm 실행결과; echo "exit 7" > loka_forrit.sh; sh loka_forrit.sh; echo $?','7\n')
            skel('rm loka_forrit.sh Skipun.sh forrit_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            prófun_skrá['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            skel('echo history-proof','history-proof')
            NIÐURSTAÐA=senda(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert NIÐURSTAÐA.count('history-proof')>=2, NIÐURSTAÐA
            senda(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            NIÐURSTAÐA=senda(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in NIÐURSTAÐA, NIÐURSTAÐA
            NIÐURSTAÐA=senda(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in NIÐURSTAÐA,NIÐURSTAÐA
            NIÐURSTAÐA=senda('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in NIÐURSTAÐA,NIÐURSTAÐA
            긴글='한글'*50
            NIÐURSTAÐA=senda(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in NIÐURSTAÐA
            skel('terminal','TERMINAL READY')
            skel('clear')
            skel('echo "한글 Skjáhermir ABC xyz 012 😀"','한글 Skjáhermir ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as biðlari:
                biðlari.settimeout(10); biðlari.connect(str(모의제어접속))
                with biðlari.makefile('rwb') as Stream_VALUE:
                    json.loads(Stream_VALUE.readline())
                    def 호출(Heiti,frumbreyta_ARRAY=None):
                        Net_skeyti={'execute':Heiti}
                        if frumbreyta_ARRAY: Net_skeyti['arguments']=frumbreyta_ARRAY
                        Stream_VALUE.write((json.dumps(Net_skeyti)+'\n').encode()); Stream_VALUE.flush()
                        while True:
                            svara=json.loads(Stream_VALUE.readline())
                            if 'error' in svara: raise AssertionError(svara)
                            if 'return' in svara: return svara['return']
                    호출('qmp_capabilities')
                    mynd=úttak_54cd5e1d/'terminal.ppm'; 호출('screendump',{'filename':str(mynd),'format':'ppm'})
                    호출('screendump',{'filename':str(úttak_54cd5e1d/'terminal.png'),'format':'png'})
                    gögn=mynd.read_bytes().split(b'\n',3)[3]
                    def díll(x_hnit,Y_hnit): return tuple(gögn[(Y_hnit*640+x_hnit)*3:(Y_hnit*640+x_hnit)*3+3])
                    assert díll(12,48)==(32,80,144),díll(12,48)
                    assert len(set(díll(x_hnit,Y_hnit) for Y_hnit in range(100,116) for x_hnit in range(24,56)))>1,'Hangul glyphs missing'
                    skel('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    skel("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(mynd),'format':'ppm'})
                    복원자료=mynd.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    skel('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): skel('echo scroll-'+str(순번),'scroll-'+str(순번))
                    senda(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(úttak_54cd5e1d/'terminal-scroll.png'),'format':'png'})
                    NIÐURSTAÐA=senda(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in NIÐURSTAÐA,NIÐURSTAÐA
                    skel('rm visible.txt')
                    호출('quit')
            Ferli.wait(timeout=5)
            prófun_skrá['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            prófun_skrá['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Ferli.poll() is None:
                Ferli.terminate()
                try: Ferli.wait(timeout=5)
                except subprocess.TimeoutExpired: Ferli.kill(); Ferli.wait()
            준비살피미.close(); Ferli.stdin.close(); Ferli.stdout.close()
            (úttak_54cd5e1d/'serial.log').write_bytes(대화기록)
            (úttak_54cd5e1d/'report.json').write_text(json.dumps(prófun_skrá,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Keyra_2()
