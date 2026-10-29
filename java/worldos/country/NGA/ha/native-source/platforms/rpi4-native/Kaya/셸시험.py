#!/usr/bin/env python3
"""자체 커널의 Mai_fayyace_umani, 프로세스 I_O, Unicode GUI 터미널을 Na_hakika_Tarin_bayani raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from gudanar_Umarni import 기준, Umarni


def Tafiyar_da():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    amincewa_Rahoto = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        haryar_aikin_na_ura = subprocess.Popen(Umarni()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(haryar_aikin_na_ura.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            Tarin_bayani=bytearray(); Ƙarshe_Sassautawa=time.monotonic()+시간제한
            while 확인표시 not in Tarin_bayani:
                if time.monotonic()>Ƙarshe_Sassautawa or haryar_aikin_na_ura.poll() is not None: raise AssertionError('UART timeout/exit: '+Tarin_bayani.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: Tarin_bayani.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in Tarin_bayani or b'FAIL ' in Tarin_bayani: raise AssertionError(Tarin_bayani)
            return Tarin_bayani.decode('utf-8','replace').replace('\r\n','\n')
        def Aika(Tarin_bayani, 확인표시=b'jkoros-native> '):
            haryar_aikin_na_ura.stdin.write(Tarin_bayani); haryar_aikin_na_ura.stdin.flush(); return 수신하기(확인표시)
        def Mai_fayyace_umani(Layi, *예상결과):
            결과=Aika(Layi.encode()+b'\n')
            for Daraja in 예상결과: assert Daraja in 결과, (Layi,Daraja,결과)
            return 결과
        def Fayil(Suna):
            SMS=Mai_fayyace_umani('hex '+Suna,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',SMS,re.S)
            Tarin_bayani=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(Tarin_bayani)==int(찾은결과.group(1)); return Tarin_bayani
        try:
            수신하기(b'jkoros-native> ')
            Mai_fayyace_umani('mkdir 작업; cd 작업; pwd','/작업')
            Mai_fayyace_umani('mkdir 하위; echo "한글 Tarin_bayani 😀" > 인사.txt')
            assert Fayil('인사.txt')=='한글 Tarin_bayani 😀\n'.encode()
            Mai_fayyace_umani('cp 인사.txt Kwafi_Daraja.txt; mv Kwafi_Daraja.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 Tarin_bayani 😀')
            Mai_fayyace_umani('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 Tarin_bayani 😀','/작업/하위')
            Mai_fayyace_umani('cd ..; rmdir 하위; echo $?','1\n')
            Mai_fayyace_umani('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            Mai_fayyace_umani('cp 인사.txt 인사.txt; echo $?','1\n'); assert Fayil('인사.txt')=='한글 Tarin_bayani 😀\n'.encode()
            Mai_fayyace_umani('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Fayil('인사.txt')
            Mai_fayyace_umani("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Fayil('리터럴')=='$인사\n누리\n'.encode()
            Mai_fayyace_umani('echo one > bayani_Daraja; echo two >> bayani_Daraja; echo three >> bayani_Daraja')
            Mai_fayyace_umani('cat < bayani_Daraja | grep t | tee 추림 | wc -l','2\n'); assert Fayil('추림')==b'two\nthree\n'
            Mai_fayyace_umani('head -n 1 bayani_Daraja > kyamarar_gaba_Daraja; tail -n 1 bayani_Daraja > Baya_Daraja'); assert Fayil('앞')==b'one\n'; assert Fayil('뒤')==b'three\n'
            Mai_fayyace_umani('grep absent bayani_Daraja; echo $?','1\n')
            Mai_fayyace_umani('echo untouched > Kare_Daraja')
            Mai_fayyace_umani('echo destroyed > Kare_Daraja |','명령이 빠졌습니다'); assert Fayil('Kare_Daraja')==b'untouched\n'
            Mai_fayyace_umani('echo "oops','따옴표가 닫히지 않았습니다')
            Mai_fayyace_umani('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            Mai_fayyace_umani('echo bad 2> Kare_Daraja','번호를 지정한 Fayil 서술자 I_O Sauya_yanayin_aiki'); assert Fayil('Kare_Daraja')==b'untouched\n'
            Mai_fayyace_umani('rm 빈파일 리터럴 bayani_Daraja 추림 kyamarar_gaba_Daraja Baya_Daraja Kare_Daraja')
            amincewa_Rahoto['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            Mai_fayyace_umani("python -c 'print(123)' | wc -c",'4\n')
            Mai_fayyace_umani("python -c 'print(456)' > Shiri_f5044b9b.txt"); assert Fayil('Shiri_f5044b9b.txt')==b'456\n'
            Mai_fayyace_umani("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            Mai_fayyace_umani("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < Shiri_f5044b9b.txt", "b'456\\n'", "b''")
            Mai_fayyace_umani("python -c 'print(\"x\"*17000)' | wc -c", 'Kuskure -28')
            Mai_fayyace_umani('echo recovered | wc -c','10\n')
            Mai_fayyace_umani("python -c 'import jkoros; print(jkoros.read("+'"/작업/Shiri_f5044b9b.txt"'+"))'",'456','exit 0')
            Mai_fayyace_umani('cd /; javac Hello.java','Compiled:','exit 0')
            Mai_fayyace_umani('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Fayil('/작업/자바.txt')
            Mai_fayyace_umani('cd 작업; echo "echo script > 실행결과" > Umarni.sh; echo "false || echo recovered >> 실행결과" >> Umarni.sh; sh Umarni.sh')
            assert Fayil('실행결과')==b'script\nrecovered\n'
            Mai_fayyace_umani('rm 실행결과; echo "exit 7" > Mafita_Shiri.sh; sh Mafita_Shiri.sh; echo $?','7\n')
            Mai_fayyace_umani('rm Mafita_Shiri.sh Umarni.sh Shiri_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            amincewa_Rahoto['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            Mai_fayyace_umani('echo history-proof','history-proof')
            결과=Aika(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            Aika(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=Aika(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=Aika(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=Aika('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=Aika(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            Mai_fayyace_umani('terminal','TERMINAL READY')
            Mai_fayyace_umani('clear')
            Mai_fayyace_umani('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as abokin_hulda:
                abokin_hulda.settimeout(10); abokin_hulda.connect(str(모의제어접속))
                with abokin_hulda.makefile('rwb') as watsuwa_Daraja:
                    json.loads(watsuwa_Daraja.readline())
                    def 호출(Suna,Tubalin_aiki_TSARI=None):
                        Hanyar_sadarwa_imel={'execute':Suna}
                        if Tubalin_aiki_TSARI: Hanyar_sadarwa_imel['arguments']=Tubalin_aiki_TSARI
                        watsuwa_Daraja.write((json.dumps(Hanyar_sadarwa_imel)+'\n').encode()); watsuwa_Daraja.flush()
                        while True:
                            mayar_da_martani=json.loads(watsuwa_Daraja.readline())
                            if 'error' in mayar_da_martani: raise AssertionError(mayar_da_martani)
                            if 'return' in mayar_da_martani: return mayar_da_martani['return']
                    호출('qmp_capabilities')
                    Hoto=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(Hoto),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    Tarin_bayani=Hoto.read_bytes().split(b'\n',3)[3]
                    def pel(gamayyar_x,Maɓallin_Y_Mai_tsarawa): return tuple(Tarin_bayani[(Maɓallin_Y_Mai_tsarawa*640+gamayyar_x)*3:(Maɓallin_Y_Mai_tsarawa*640+gamayyar_x)*3+3])
                    assert pel(12,48)==(32,80,144),pel(12,48)
                    assert len(set(pel(gamayyar_x,Maɓallin_Y_Mai_tsarawa) for Maɓallin_Y_Mai_tsarawa in range(100,116) for gamayyar_x in range(24,56)))>1,'Hangul glyphs missing'
                    Mai_fayyace_umani('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    Mai_fayyace_umani("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(Hoto),'format':'ppm'})
                    복원자료=Hoto.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    Mai_fayyace_umani('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): Mai_fayyace_umani('echo scroll-'+str(순번),'scroll-'+str(순번))
                    Aika(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=Aika(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    Mai_fayyace_umani('rm visible.txt')
                    호출('quit')
            haryar_aikin_na_ura.wait(timeout=5)
            amincewa_Rahoto['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            amincewa_Rahoto['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if haryar_aikin_na_ura.poll() is None:
                haryar_aikin_na_ura.terminate()
                try: haryar_aikin_na_ura.wait(timeout=5)
                except subprocess.TimeoutExpired: haryar_aikin_na_ura.kill(); haryar_aikin_na_ura.wait()
            준비살피미.close(); haryar_aikin_na_ura.stdin.close(); haryar_aikin_na_ura.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(amincewa_Rahoto,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Tafiyar_da()
