#!/usr/bin/env python3
"""Asli 커널의 shell, 프로세스 I_O, Unicode GUI 터미널을 aktual_data raspi4b에서 pengujian."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Jalankan_perintah import Tugas_akar, perintah


def jalankan():
    출력결과 = Tugas_akar / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    validasi_lapor = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Tugas_akar / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkrip = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proses = subprocess.Popen(perintah()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proses.stdout,selectors.EVENT_READ)
        def terima_email(확인표시, 시간제한=45):
            data=bytearray(); mengakhiri_OFFSET=time.monotonic()+시간제한
            while 확인표시 not in data:
                if time.monotonic()>mengakhiri_OFFSET or Proses.poll() is not None: raise AssertionError('UART timeout/exit: '+data.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); transkrip.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8','replace').replace('\r\n','\n')
        def kirim(data, 확인표시=b'jkoros-native> '):
            Proses.stdin.write(data); Proses.stdin.flush(); return terima_email(확인표시)
        def shell(baris_masukan, *예상결과):
            hasil=kirim(baris_masukan.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in hasil, (baris_masukan,VALUE,hasil)
            return hasil
        def berkas(Nama_2):
            teks=shell('hex '+Nama_2,'HEX BEGIN','HEX END'); Cari_KR=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',teks,re.S)
            data=bytes.fromhex(''.join(Cari_KR.group(2).split())); assert len(data)==int(Cari_KR.group(1)); return data
        try:
            terima_email(b'jkoros-native> ')
            shell('mkdir 작업; cd 작업; pwd','/작업')
            shell('mkdir 하위; echo "한글 data 😀" > 인사.txt')
            assert berkas('인사.txt')=='한글 data 😀\n'.encode()
            shell('cp 인사.txt salin_VALUE.txt; mv salin_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 data 😀')
            shell('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 data 😀','/작업/하위')
            shell('cd ..; rmdir 하위; echo $?','1\n')
            shell('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            shell('cp 인사.txt 인사.txt; echo $?','1\n'); assert berkas('인사.txt')=='한글 data 😀\n'.encode()
            shell('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in berkas('인사.txt')
            shell("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert berkas('리터럴')=='$인사\n누리\n'.encode()
            shell('echo one > pernyataan_VALUE; echo two >> pernyataan_VALUE; echo three >> pernyataan_VALUE')
            shell('cat < pernyataan_VALUE | grep t | tee 추림 | wc -l','2\n'); assert berkas('추림')==b'two\nthree\n'
            shell('head -n 1 pernyataan_VALUE > depan_VALUE; tail -n 1 pernyataan_VALUE > BACK_VALUE'); assert berkas('앞')==b'one\n'; assert berkas('뒤')==b'three\n'
            shell('grep absent pernyataan_VALUE; echo $?','1\n')
            shell('echo untouched > amankan_VALUE')
            shell('echo destroyed > amankan_VALUE |','명령이 빠졌습니다'); assert berkas('amankan_VALUE')==b'untouched\n'
            shell('echo "oops','따옴표가 닫히지 않았습니다')
            shell('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            shell('echo bad 2> amankan_VALUE','번호를 지정한 berkas 서술자 I_O SWITCH_MODE'); assert berkas('amankan_VALUE')==b'untouched\n'
            shell('rm 빈파일 리터럴 pernyataan_VALUE 추림 depan_VALUE BACK_VALUE amankan_VALUE')
            validasi_lapor['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            shell("python -c 'print(123)' | wc -c",'4\n')
            shell("python -c 'print(456)' > apl_f5044b9b.txt"); assert berkas('apl_f5044b9b.txt')==b'456\n'
            shell("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            shell("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < apl_f5044b9b.txt", "b'456\\n'", "b''")
            shell("python -c 'print(\"x\"*17000)' | wc -c", 'galat -28')
            shell('echo recovered | wc -c','10\n')
            shell("python -c 'import jkoros; print(jkoros.read("+'"/작업/apl_f5044b9b.txt"'+"))'",'456','exit 0')
            shell('cd /; javac Hello.java','Compiled:','exit 0')
            shell('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in berkas('/작업/자바.txt')
            shell('cd 작업; echo "echo script > 실행결과" > perintah.sh; echo "false || echo recovered >> 실행결과" >> perintah.sh; sh perintah.sh')
            assert berkas('실행결과')==b'script\nrecovered\n'
            shell('rm 실행결과; echo "exit 7" > Keluar_apl.sh; sh Keluar_apl.sh; echo $?','7\n')
            shell('rm Keluar_apl.sh perintah.sh apl_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            validasi_lapor['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            shell('echo history-proof','history-proof')
            hasil=kirim(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert hasil.count('history-proof')>=2, hasil
            kirim(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            hasil=kirim(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in hasil, hasil
            hasil=kirim(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in hasil,hasil
            hasil=kirim('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in hasil,hasil
            긴글='한글'*50
            hasil=kirim(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in hasil
            shell('terminal','TERMINAL READY')
            shell('clear')
            shell('echo "한글 terminal ABC xyz 012 😀"','한글 terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klien:
                klien.settimeout(10); klien.connect(str(모의제어접속))
                with klien.makefile('rwb') as Stream_VALUE:
                    json.loads(Stream_VALUE.readline())
                    def 호출(Nama_2,argumen_ARRAY=None):
                        jaringan_email={'execute':Nama_2}
                        if argumen_ARRAY: jaringan_email['arguments']=argumen_ARRAY
                        Stream_VALUE.write((json.dumps(jaringan_email)+'\n').encode()); Stream_VALUE.flush()
                        while True:
                            balas=json.loads(Stream_VALUE.readline())
                            if 'error' in balas: raise AssertionError(balas)
                            if 'return' in balas: return balas['return']
                    호출('qmp_capabilities')
                    foto=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(foto),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    data=foto.read_bytes().split(b'\n',3)[3]
                    def elgam(koordinat_x,Y_koordinat): return tuple(data[(Y_koordinat*640+koordinat_x)*3:(Y_koordinat*640+koordinat_x)*3+3])
                    assert elgam(12,48)==(32,80,144),elgam(12,48)
                    assert len(set(elgam(koordinat_x,Y_koordinat) for Y_koordinat in range(100,116) for koordinat_x in range(24,56)))>1,'Hangul glyphs missing'
                    shell('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    shell("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(foto),'format':'ppm'})
                    복원자료=foto.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    shell('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): shell('echo scroll-'+str(순번),'scroll-'+str(순번))
                    kirim(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    hasil=kirim(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in hasil,hasil
                    shell('rm visible.txt')
                    호출('quit')
            Proses.wait(timeout=5)
            validasi_lapor['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            validasi_lapor['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proses.poll() is None:
                Proses.terminate()
                try: Proses.wait(timeout=5)
                except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
            준비살피미.close(); Proses.stdin.close(); Proses.stdout.close()
            (출력결과/'serial.log').write_bytes(transkrip)
            (출력결과/'report.json').write_text(json.dumps(validasi_lapor,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': jalankan()
