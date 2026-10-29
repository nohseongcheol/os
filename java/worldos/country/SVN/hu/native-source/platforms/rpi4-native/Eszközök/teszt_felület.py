#!/usr/bin/env python3
"""saját 커널의 felület, 프로세스 I_O, Unicode GUI 터미널을 tényleges_adat raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from végrehajt_parancs import teendő_gyök, Parancs


def Futtatás():
    kimenet = teendő_gyök / 'build/verification/shell'; kimenet.mkdir(parents=True, exist_ok=True)
    ellenőrzés_jelent = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((teendő_gyök / 'build/kernel8.img').read_bytes()).hexdigest()}
    átirat = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Folyamat = subprocess.Popen(Parancs()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Folyamat.stdout,selectors.EVENT_READ)
        def fogad_e_mail(jelölő, végrehajtás_IDŐTÚLLÉPÉS=45):
            adat=bytearray(); megszüntet_Ofszet=time.monotonic()+végrehajtás_IDŐTÚLLÉPÉS
            while jelölő not in adat:
                if time.monotonic()>megszüntet_Ofszet or Folyamat.poll() is not None: raise AssertionError('UART timeout/exit: '+adat.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: adat.extend(조각); átirat.extend(조각)
                if b'PANIC:' in adat or b'FAIL ' in adat: raise AssertionError(adat)
            return adat.decode('utf-8','replace').replace('\r\n','\n')
        def küld(adat, jelölő=b'jkoros-native> '):
            Folyamat.stdin.write(adat); Folyamat.stdin.flush(); return fogad_e_mail(jelölő)
        def felület(Vonal, *예상결과):
            KR=küld(Vonal.encode()+b'\n')
            for ÉRTÉK in 예상결과: assert ÉRTÉK in KR, (Vonal,ÉRTÉK,KR)
            return KR
        def Fájl(Név):
            Szöveg=felület('hex '+Név,'HEX BEGIN','HEX END'); keres_KR=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Szöveg,re.S)
            adat=bytes.fromhex(''.join(keres_KR.group(2).split())); assert len(adat)==int(keres_KR.group(1)); return adat
        try:
            fogad_e_mail(b'jkoros-native> ')
            felület('mkdir 작업; cd 작업; pwd','/작업')
            felület('mkdir 하위; echo "한글 adat 😀" > 인사.txt')
            assert Fájl('인사.txt')=='한글 adat 😀\n'.encode()
            felület('cp 인사.txt másol_ÉRTÉK.txt; mv másol_ÉRTÉK.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 adat 😀')
            felület('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 adat 😀','/작업/하위')
            felület('cd ..; rmdir 하위; echo $?','1\n')
            felület('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            felület('cp 인사.txt 인사.txt; echo $?','1\n'); assert Fájl('인사.txt')=='한글 adat 😀\n'.encode()
            felület('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Fájl('인사.txt')
            felület("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Fájl('리터럴')=='$인사\n누리\n'.encode()
            felület('echo one > utasítás_ÉRTÉK; echo two >> utasítás_ÉRTÉK; echo three >> utasítás_ÉRTÉK')
            felület('cat < utasítás_ÉRTÉK | grep t | tee 추림 | wc -l','2\n'); assert Fájl('추림')==b'two\nthree\n'
            felület('head -n 1 utasítás_ÉRTÉK > elülső_kamera_ÉRTÉK; tail -n 1 utasítás_ÉRTÉK > BACK_ÉRTÉK'); assert Fájl('앞')==b'one\n'; assert Fájl('뒤')==b'three\n'
            felület('grep absent utasítás_ÉRTÉK; echo $?','1\n')
            felület('echo untouched > véd_ÉRTÉK')
            felület('echo destroyed > véd_ÉRTÉK |','명령이 빠졌습니다'); assert Fájl('véd_ÉRTÉK')==b'untouched\n'
            felület('echo "oops','따옴표가 닫히지 않았습니다')
            felület('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            felület('echo bad 2> véd_ÉRTÉK','번호를 지정한 Fájl 서술자 I_O vált_mód'); assert Fájl('véd_ÉRTÉK')==b'untouched\n'
            felület('rm 빈파일 리터럴 utasítás_ÉRTÉK 추림 elülső_kamera_ÉRTÉK BACK_ÉRTÉK véd_ÉRTÉK')
            ellenőrzés_jelent['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            felület("python -c 'print(123)' | wc -c",'4\n')
            felület("python -c 'print(456)' > app_f5044b9b.txt"); assert Fájl('app_f5044b9b.txt')==b'456\n'
            felület("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            felület("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < app_f5044b9b.txt", "b'456\\n'", "b''")
            felület("python -c 'print(\"x\"*17000)' | wc -c", 'HIBA -28')
            felület('echo recovered | wc -c','10\n')
            felület("python -c 'import jkoros; print(jkoros.read("+'"/작업/app_f5044b9b.txt"'+"))'",'456','exit 0')
            felület('cd /; javac Hello.java','Compiled:','exit 0')
            felület('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Fájl('/작업/자바.txt')
            felület('cd 작업; echo "echo script > végrehajtás_KR" > Parancs.sh; echo "false || echo recovered >> végrehajtás_KR" >> Parancs.sh; sh Parancs.sh')
            assert Fájl('végrehajtás_KR')==b'script\nrecovered\n'
            felület('rm végrehajtás_KR; echo "exit 7" > kilép_app.sh; sh kilép_app.sh; echo $?','7\n')
            felület('rm kilép_app.sh Parancs.sh app_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            ellenőrzés_jelent['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            felület('echo history-proof','history-proof')
            KR=küld(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert KR.count('history-proof')>=2, KR
            küld(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            KR=küld(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in KR, KR
            KR=küld(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in KR,KR
            KR=küld('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in KR,KR
            긴글='한글'*50
            KR=küld(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in KR
            felület('terminal','TERMINAL READY')
            felület('clear')
            felület('echo "한글 Terminál ABC xyz 012 😀"','한글 Terminál ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as kliens:
                kliens.settimeout(10); kliens.connect(str(모의제어접속))
                with kliens.makefile('rwb') as Stream_ÉRTÉK:
                    json.loads(Stream_ÉRTÉK.readline())
                    def 호출(Név,argumentum_TÖMB=None):
                        hálózat_e_mail={'execute':Név}
                        if argumentum_TÖMB: hálózat_e_mail['arguments']=argumentum_TÖMB
                        Stream_ÉRTÉK.write((json.dumps(hálózat_e_mail)+'\n').encode()); Stream_ÉRTÉK.flush()
                        while True:
                            válasz=json.loads(Stream_ÉRTÉK.readline())
                            if 'error' in válasz: raise AssertionError(válasz)
                            if 'return' in válasz: return válasz['return']
                    호출('qmp_capabilities')
                    KÉP=kimenet/'terminal.ppm'; 호출('screendump',{'filename':str(KÉP),'format':'ppm'})
                    호출('screendump',{'filename':str(kimenet/'terminal.png'),'format':'png'})
                    adat=KÉP.read_bytes().split(b'\n',3)[3]
                    def képpont(x_koordináta,Y_koordináta): return tuple(adat[(Y_koordináta*640+x_koordináta)*3:(Y_koordináta*640+x_koordináta)*3+3])
                    assert képpont(12,48)==(32,80,144),képpont(12,48)
                    assert len(set(képpont(x_koordináta,Y_koordináta) for Y_koordináta in range(100,116) for x_koordináta in range(24,56)))>1,'Hangul glyphs missing'
                    felület('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    felület("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(KÉP),'format':'ppm'})
                    복원자료=KÉP.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    felület('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): felület('echo scroll-'+str(순번),'scroll-'+str(순번))
                    küld(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(kimenet/'terminal-scroll.png'),'format':'png'})
                    KR=küld(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in KR,KR
                    felület('rm visible.txt')
                    호출('quit')
            Folyamat.wait(timeout=5)
            ellenőrzés_jelent['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            ellenőrzés_jelent['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Folyamat.poll() is None:
                Folyamat.terminate()
                try: Folyamat.wait(timeout=5)
                except subprocess.TimeoutExpired: Folyamat.kill(); Folyamat.wait()
            준비살피미.close(); Folyamat.stdin.close(); Folyamat.stdout.close()
            (kimenet/'serial.log').write_bytes(átirat)
            (kimenet/'report.json').write_text(json.dumps(ellenőrzés_jelent,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Futtatás()
