#!/usr/bin/env python3
"""자체 커널의 Wëreef, 프로세스 D_G, Unicode GUI 터미널을 liteew_mbir raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from def_ndigel import 기준, ndigel


def daw():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    wéral_tënk = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        yokkute = subprocess.Popen(ndigel()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(yokkute.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            mbir=bytearray(); jeexal_Randal=time.monotonic()+시간제한
            while 확인표시 not in mbir:
                if time.monotonic()>jeexal_Randal or yokkute.poll() is not None: raise AssertionError('UART timeout/exit: '+mbir.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: mbir.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in mbir or b'FAIL ' in mbir: raise AssertionError(mbir)
            return mbir.decode('utf-8','replace').replace('\r\n','\n')
        def Yónnee(mbir, 확인표시=b'jkoros-native> '):
            yokkute.stdin.write(mbir); yokkute.stdin.flush(); return 수신하기(확인표시)
        def Wëreef(buum, *예상결과):
            결과=Yónnee(buum.encode()+b'\n')
            for xëyma in 예상결과: assert xëyma in 결과, (buum,xëyma,결과)
            return 결과
        def bara_denc(tur_253d1510):
            Tekst=Wëreef('hex '+tur_253d1510,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Tekst,re.S)
            mbir=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(mbir)==int(찾은결과.group(1)); return mbir
        try:
            수신하기(b'jkoros-native> ')
            Wëreef('mkdir 작업; cd 작업; pwd','/작업')
            Wëreef('mkdir 하위; echo "한글 mbir 😀" > 인사.txt')
            assert bara_denc('인사.txt')=='한글 mbir 😀\n'.encode()
            Wëreef('cp 인사.txt mbokk_xëyma.txt; mv mbokk_xëyma.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 mbir 😀')
            Wëreef('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 mbir 😀','/작업/하위')
            Wëreef('cd ..; rmdir 하위; echo $?','1\n')
            Wëreef('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            Wëreef('cp 인사.txt 인사.txt; echo $?','1\n'); assert bara_denc('인사.txt')=='한글 mbir 😀\n'.encode()
            Wëreef('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in bara_denc('인사.txt')
            Wëreef("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert bara_denc('리터럴')=='$인사\n누리\n'.encode()
            Wëreef('echo one > nétali_xëyma; echo two >> nétali_xëyma; echo three >> nétali_xëyma')
            Wëreef('cat < nétali_xëyma | grep t | tee 추림 | wc -l','2\n'); assert bara_denc('추림')==b'two\nthree\n'
            Wëreef('head -n 1 nétali_xëyma > 앞; tail -n 1 nétali_xëyma > woñeeku_xëyma'); assert bara_denc('앞')==b'one\n'; assert bara_denc('뒤')==b'three\n'
            Wëreef('grep absent nétali_xëyma; echo $?','1\n')
            Wëreef('echo untouched > saama_xëyma')
            Wëreef('echo destroyed > saama_xëyma |','명령이 빠졌습니다'); assert bara_denc('saama_xëyma')==b'untouched\n'
            Wëreef('echo "oops','따옴표가 닫히지 않았습니다')
            Wëreef('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            Wëreef('echo bad 2> saama_xëyma','번호를 지정한 bara_denc 서술자 D_G jalantu_anam'); assert bara_denc('saama_xëyma')==b'untouched\n'
            Wëreef('rm 빈파일 리터럴 nétali_xëyma 추림 앞 woñeeku_xëyma saama_xëyma')
            wéral_tënk['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            Wëreef("python -c 'print(123)' | wc -c",'4\n')
            Wëreef("python -c 'print(456)' > jëfekaay_f5044b9b.txt"); assert bara_denc('jëfekaay_f5044b9b.txt')==b'456\n'
            Wëreef("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            Wëreef("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < jëfekaay_f5044b9b.txt", "b'456\\n'", "b''")
            Wëreef("python -c 'print(\"x\"*17000)' | wc -c", 'njumte -28')
            Wëreef('echo recovered | wc -c','10\n')
            Wëreef("python -c 'import jkoros; print(jkoros.read("+'"/작업/jëfekaay_f5044b9b.txt"'+"))'",'456','exit 0')
            Wëreef('cd /; javac Hello.java','Compiled:','exit 0')
            Wëreef('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in bara_denc('/작업/자바.txt')
            Wëreef('cd 작업; echo "echo script > 실행결과" > ndigel.sh; echo "false || echo recovered >> 실행결과" >> ndigel.sh; sh ndigel.sh')
            assert bara_denc('실행결과')==b'script\nrecovered\n'
            Wëreef('rm 실행결과; echo "exit 7" > Génn_jëfekaay.sh; sh Génn_jëfekaay.sh; echo $?','7\n')
            Wëreef('rm Génn_jëfekaay.sh ndigel.sh jëfekaay_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            wéral_tënk['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            Wëreef('echo history-proof','history-proof')
            결과=Yónnee(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            Yónnee(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=Yónnee(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=Yónnee(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=Yónnee('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=Yónnee(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            Wëreef('terminal','TERMINAL READY')
            Wëreef('clear')
            Wëreef('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as lëkkalekat:
                lëkkalekat.settimeout(10); lëkkalekat.connect(str(모의제어접속))
                with lëkkalekat.makefile('rwb') as dawal_xëyma:
                    json.loads(dawal_xëyma.readline())
                    def 호출(tur_253d1510,Tegtal_TABLO=None):
                        mbaal_bataaxal={'execute':tur_253d1510}
                        if Tegtal_TABLO: mbaal_bataaxal['arguments']=Tegtal_TABLO
                        dawal_xëyma.write((json.dumps(mbaal_bataaxal)+'\n').encode()); dawal_xëyma.flush()
                        while True:
                            tontu=json.loads(dawal_xëyma.readline())
                            if 'error' in tontu: raise AssertionError(tontu)
                            if 'return' in tontu: return tontu['return']
                    호출('qmp_capabilities')
                    nataal=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(nataal),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    mbir=nataal.read_bytes().split(b'\n',3)[3]
                    def piksel(rëddu_iks_yi,세로좌표): return tuple(mbir[(세로좌표*640+rëddu_iks_yi)*3:(세로좌표*640+rëddu_iks_yi)*3+3])
                    assert piksel(12,48)==(32,80,144),piksel(12,48)
                    assert len(set(piksel(rëddu_iks_yi,세로좌표) for 세로좌표 in range(100,116) for rëddu_iks_yi in range(24,56)))>1,'Hangul glyphs missing'
                    Wëreef('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    Wëreef("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(nataal),'format':'ppm'})
                    복원자료=nataal.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    Wëreef('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): Wëreef('echo scroll-'+str(순번),'scroll-'+str(순번))
                    Yónnee(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=Yónnee(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    Wëreef('rm visible.txt')
                    호출('quit')
            yokkute.wait(timeout=5)
            wéral_tënk['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            wéral_tënk['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if yokkute.poll() is None:
                yokkute.terminate()
                try: yokkute.wait(timeout=5)
                except subprocess.TimeoutExpired: yokkute.kill(); yokkute.wait()
            준비살피미.close(); yokkute.stdin.close(); yokkute.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(wéral_tënk,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': daw()
