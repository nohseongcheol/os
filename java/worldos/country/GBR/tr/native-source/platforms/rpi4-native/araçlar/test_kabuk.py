#!/usr/bin/env python3
"""Öz 커널의 kabuk, 프로세스 G_Ç, Unicode GUI 터미널을 fiili_veri raspi4b에서 sınamalar."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from yürütmek_komut import işlem_kök, komut


def çalıştır():
    çıktı = işlem_kök / 'build/verification/shell'; çıktı.mkdir(parents=True, exist_ok=True)
    doğrulama_Rapor = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((işlem_kök / 'build/kernel8.img').read_bytes()).hexdigest()}
    döküm = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Süreç = subprocess.Popen(komut()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Süreç.stdout,selectors.EVENT_READ)
        def almak_belge(işaret, yürütme_ZAMANAŞIMI=45):
            veri=bytearray(); Bitiş_Ofset=time.monotonic()+yürütme_ZAMANAŞIMI
            while işaret not in veri:
                if time.monotonic()>Bitiş_Ofset or Süreç.poll() is not None: raise AssertionError('UART timeout/exit: '+veri.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    parça_değer=누름값.fileobj.read(4096)
                    if parça_değer: veri.extend(parça_değer); döküm.extend(parça_değer)
                if b'PANIC:' in veri or b'FAIL ' in veri: raise AssertionError(veri)
            return veri.decode('utf-8','replace').replace('\r\n','\n')
        def göndermek(veri, işaret=b'jkoros-native> '):
            Süreç.stdin.write(veri); Süreç.stdin.flush(); return almak_belge(işaret)
        def kabuk(girdi_satırı, *예상결과):
            sonuç=göndermek(girdi_satırı.encode()+b'\n')
            for değer in 예상결과: assert değer in sonuç, (girdi_satırı,değer,sonuç)
            return sonuç
        def dosya(İsim):
            metin=kabuk('hex '+İsim,'HEX BEGIN','HEX END'); Ara_KR=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',metin,re.S)
            veri=bytes.fromhex(''.join(Ara_KR.group(2).split())); assert len(veri)==int(Ara_KR.group(1)); return veri
        try:
            almak_belge(b'jkoros-native> ')
            kabuk('mkdir 작업; cd 작업; pwd','/작업')
            kabuk('mkdir 하위; echo "한글 veri 😀" > 인사.txt')
            assert dosya('인사.txt')=='한글 veri 😀\n'.encode()
            kabuk('cp 인사.txt örnek_değer.txt; mv örnek_değer.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 veri 😀')
            kabuk('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 veri 😀','/작업/하위')
            kabuk('cd ..; rmdir 하위; echo $?','1\n')
            kabuk('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            kabuk('cp 인사.txt 인사.txt; echo $?','1\n'); assert dosya('인사.txt')=='한글 veri 😀\n'.encode()
            kabuk('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in dosya('인사.txt')
            kabuk("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert dosya('리터럴')=='$인사\n누리\n'.encode()
            kabuk('echo one > deyim_değer; echo two >> deyim_değer; echo three >> deyim_değer')
            kabuk('cat < deyim_değer | grep t | tee 추림 | wc -l','2\n'); assert dosya('추림')==b'two\nthree\n'
            kabuk('head -n 1 deyim_değer > ön_kamera_değer; tail -n 1 deyim_değer > BACK_değer'); assert dosya('앞')==b'one\n'; assert dosya('뒤')==b'three\n'
            kabuk('grep absent deyim_değer; echo $?','1\n')
            kabuk('echo untouched > korumak_değer')
            kabuk('echo destroyed > korumak_değer |','명령이 빠졌습니다'); assert dosya('korumak_değer')==b'untouched\n'
            kabuk('echo "oops','따옴표가 닫히지 않았습니다')
            kabuk('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            kabuk('echo bad 2> korumak_değer','번호를 지정한 dosya tanımlayıcı_girdi G_Ç geçiş_mod'); assert dosya('korumak_değer')==b'untouched\n'
            kabuk('rm 빈파일 리터럴 deyim_değer 추림 ön_kamera_değer BACK_değer korumak_değer')
            doğrulama_Rapor['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            kabuk("python -c 'print(123)' | wc -c",'4\n')
            kabuk("python -c 'print(456)' > program_f5044b9b.txt"); assert dosya('program_f5044b9b.txt')==b'456\n'
            kabuk("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            kabuk("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < program_f5044b9b.txt", "b'456\\n'", "b''")
            kabuk("python -c 'print(\"x\"*17000)' | wc -c", 'hata -28')
            kabuk('echo recovered | wc -c','10\n')
            kabuk("python -c 'import jkoros; print(jkoros.read("+'"/작업/program_f5044b9b.txt"'+"))'",'456','exit 0')
            kabuk('cd /; javac Hello.java','Compiled:','exit 0')
            kabuk('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in dosya('/작업/자바.txt')
            kabuk('cd 작업; echo "echo script > yürütme_KR" > komut.sh; echo "false || echo recovered >> yürütme_KR" >> komut.sh; sh komut.sh')
            assert dosya('yürütme_KR')==b'script\nrecovered\n'
            kabuk('rm yürütme_KR; echo "exit 7" > Çıkış_program.sh; sh Çıkış_program.sh; echo $?','7\n')
            kabuk('rm Çıkış_program.sh komut.sh program_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            doğrulama_Rapor['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            kabuk('echo history-proof','history-proof')
            sonuç=göndermek(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert sonuç.count('history-proof')>=2, sonuç
            göndermek(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            sonuç=göndermek(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in sonuç, sonuç
            sonuç=göndermek(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in sonuç,sonuç
            sonuç=göndermek('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in sonuç,sonuç
            긴글='한글'*50
            sonuç=göndermek(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in sonuç
            kabuk('terminal','TERMINAL READY')
            kabuk('clear')
            kabuk('echo "한글 uçbirim ABC xyz 012 😀"','한글 uçbirim ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as istemci:
                istemci.settimeout(10); istemci.connect(str(모의제어접속))
                with istemci.makefile('rwb') as akış_değer:
                    json.loads(akış_değer.readline())
                    def 호출(İsim,bağımsız_değişken_DİZİ=None):
                        ağ_belge={'execute':İsim}
                        if bağımsız_değişken_DİZİ: ağ_belge['arguments']=bağımsız_değişken_DİZİ
                        akış_değer.write((json.dumps(ağ_belge)+'\n').encode()); akış_değer.flush()
                        while True:
                            yanıt=json.loads(akış_değer.readline())
                            if 'error' in yanıt: raise AssertionError(yanıt)
                            if 'return' in yanıt: return yanıt['return']
                    호출('qmp_capabilities')
                    RESİM=çıktı/'terminal.ppm'; 호출('screendump',{'filename':str(RESİM),'format':'ppm'})
                    호출('screendump',{'filename':str(çıktı/'terminal.png'),'format':'png'})
                    veri=RESİM.read_bytes().split(b'\n',3)[3]
                    def piksel(x_koordinatı,Y_koordinat): return tuple(veri[(Y_koordinat*640+x_koordinatı)*3:(Y_koordinat*640+x_koordinatı)*3+3])
                    assert piksel(12,48)==(32,80,144),piksel(12,48)
                    assert len(set(piksel(x_koordinatı,Y_koordinat) for Y_koordinat in range(100,116) for x_koordinatı in range(24,56)))>1,'Hangul glyphs missing'
                    kabuk('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    kabuk("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(RESİM),'format':'ppm'})
                    복원자료=RESİM.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    kabuk('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): kabuk('echo scroll-'+str(순번),'scroll-'+str(순번))
                    göndermek(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(çıktı/'terminal-scroll.png'),'format':'png'})
                    sonuç=göndermek(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in sonuç,sonuç
                    kabuk('rm visible.txt')
                    호출('quit')
            Süreç.wait(timeout=5)
            doğrulama_Rapor['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            doğrulama_Rapor['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Süreç.poll() is None:
                Süreç.terminate()
                try: Süreç.wait(timeout=5)
                except subprocess.TimeoutExpired: Süreç.kill(); Süreç.wait()
            준비살피미.close(); Süreç.stdin.close(); Süreç.stdout.close()
            (çıktı/'serial.log').write_bytes(döküm)
            (çıktı/'report.json').write_text(json.dumps(doğrulama_Rapor,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': çalıştır()
