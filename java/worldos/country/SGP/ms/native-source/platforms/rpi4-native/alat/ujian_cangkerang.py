#!/usr/bin/env python3
"""Asli 커널의 cangkerang, 프로세스 I_O, Unicode GUI 터미널을 sebenar_data raspi4b에서 ujian."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from laksanakan_perintah import projek_akar, Perintah


def Jalan():
    출력결과 = projek_akar / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    pensahihan_lapor = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((projek_akar / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proses = subprocess.Popen(Perintah()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proses.stdout,selectors.EVENT_READ)
        def 수신하기(penanda, 시간제한=45):
            data=bytearray(); tamat_Ofset=time.monotonic()+시간제한
            while penanda not in data:
                if time.monotonic()>tamat_Ofset or Proses.poll() is not None: raise AssertionError('UART timeout/exit: '+data.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8','replace').replace('\r\n','\n')
        def e_mel_9aee63bd(data, penanda=b'jkoros-native> '):
            Proses.stdin.write(data); Proses.stdin.flush(); return 수신하기(penanda)
        def cangkerang(baris, *예상결과):
            ukuran=e_mel_9aee63bd(baris.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in ukuran, (baris,VALUE,ukuran)
            return ukuran
        def Fail(Nama):
            Teks=cangkerang('hex '+Nama,'HEX BEGIN','HEX END'); Cari_ukuran=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Teks,re.S)
            data=bytes.fromhex(''.join(Cari_ukuran.group(2).split())); assert len(data)==int(Cari_ukuran.group(1)); return data
        try:
            수신하기(b'jkoros-native> ')
            cangkerang('mkdir 작업; cd 작업; pwd','/작업')
            cangkerang('mkdir 하위; echo "한글 data 😀" > 인사.txt')
            assert Fail('인사.txt')=='한글 data 😀\n'.encode()
            cangkerang('cp 인사.txt tika_VALUE.txt; mv tika_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 data 😀')
            cangkerang('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 data 😀','/작업/하위')
            cangkerang('cd ..; rmdir 하위; echo $?','1\n')
            cangkerang('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            cangkerang('cp 인사.txt 인사.txt; echo $?','1\n'); assert Fail('인사.txt')=='한글 data 😀\n'.encode()
            cangkerang('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Fail('인사.txt')
            cangkerang("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Fail('리터럴')=='$인사\n누리\n'.encode()
            cangkerang('echo one > kenyataan_VALUE; echo two >> kenyataan_VALUE; echo three >> kenyataan_VALUE')
            cangkerang('cat < kenyataan_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Fail('추림')==b'two\nthree\n'
            cangkerang('head -n 1 kenyataan_VALUE > hadapan_VALUE; tail -n 1 kenyataan_VALUE > BACK_VALUE'); assert Fail('앞')==b'one\n'; assert Fail('뒤')==b'three\n'
            cangkerang('grep absent kenyataan_VALUE; echo $?','1\n')
            cangkerang('echo untouched > lindung_VALUE')
            cangkerang('echo destroyed > lindung_VALUE |','명령이 빠졌습니다'); assert Fail('lindung_VALUE')==b'untouched\n'
            cangkerang('echo "oops','따옴표가 닫히지 않았습니다')
            cangkerang('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            cangkerang('echo bad 2> lindung_VALUE','번호를 지정한 Fail 서술자 I_O tukar_mod'); assert Fail('lindung_VALUE')==b'untouched\n'
            cangkerang('rm 빈파일 리터럴 kenyataan_VALUE 추림 hadapan_VALUE BACK_VALUE lindung_VALUE')
            pensahihan_lapor['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            cangkerang("python -c 'print(123)' | wc -c",'4\n')
            cangkerang("python -c 'print(456)' > aplikasi_f5044b9b.txt"); assert Fail('aplikasi_f5044b9b.txt')==b'456\n'
            cangkerang("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            cangkerang("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < aplikasi_f5044b9b.txt", "b'456\\n'", "b''")
            cangkerang("python -c 'print(\"x\"*17000)' | wc -c", 'RALAT -28')
            cangkerang('echo recovered | wc -c','10\n')
            cangkerang("python -c 'import jkoros; print(jkoros.read("+'"/작업/aplikasi_f5044b9b.txt"'+"))'",'456','exit 0')
            cangkerang('cd /; javac Hello.java','Compiled:','exit 0')
            cangkerang('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Fail('/작업/자바.txt')
            cangkerang('cd 작업; echo "echo script > 실행결과" > Perintah.sh; echo "false || echo recovered >> 실행결과" >> Perintah.sh; sh Perintah.sh')
            assert Fail('실행결과')==b'script\nrecovered\n'
            cangkerang('rm 실행결과; echo "exit 7" > Keluar_aplikasi.sh; sh Keluar_aplikasi.sh; echo $?','7\n')
            cangkerang('rm Keluar_aplikasi.sh Perintah.sh aplikasi_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            pensahihan_lapor['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            cangkerang('echo history-proof','history-proof')
            ukuran=e_mel_9aee63bd(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert ukuran.count('history-proof')>=2, ukuran
            e_mel_9aee63bd(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            ukuran=e_mel_9aee63bd(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in ukuran, ukuran
            ukuran=e_mel_9aee63bd(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in ukuran,ukuran
            ukuran=e_mel_9aee63bd('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in ukuran,ukuran
            긴글='한글'*50
            ukuran=e_mel_9aee63bd(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in ukuran
            cangkerang('terminal','TERMINAL READY')
            cangkerang('clear')
            cangkerang('echo "한글 Terminal ABC xyz 012 😀"','한글 Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klien:
                klien.settimeout(10); klien.connect(str(모의제어접속))
                with klien.makefile('rwb') as strim_VALUE:
                    json.loads(strim_VALUE.readline())
                    def 호출(Nama,argumen_ARRAY=None):
                        rangkaian_e_mel={'execute':Nama}
                        if argumen_ARRAY: rangkaian_e_mel['arguments']=argumen_ARRAY
                        strim_VALUE.write((json.dumps(rangkaian_e_mel)+'\n').encode()); strim_VALUE.flush()
                        while True:
                            balas=json.loads(strim_VALUE.readline())
                            if 'error' in balas: raise AssertionError(balas)
                            if 'return' in balas: return balas['return']
                    호출('qmp_capabilities')
                    imej=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(imej),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    data=imej.read_bytes().split(b'\n',3)[3]
                    def pel(koordinat_x,Y_koordinat): return tuple(data[(Y_koordinat*640+koordinat_x)*3:(Y_koordinat*640+koordinat_x)*3+3])
                    assert pel(12,48)==(32,80,144),pel(12,48)
                    assert len(set(pel(koordinat_x,Y_koordinat) for Y_koordinat in range(100,116) for koordinat_x in range(24,56)))>1,'Hangul glyphs missing'
                    cangkerang('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    cangkerang("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(imej),'format':'ppm'})
                    복원자료=imej.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    cangkerang('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): cangkerang('echo scroll-'+str(순번),'scroll-'+str(순번))
                    e_mel_9aee63bd(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    ukuran=e_mel_9aee63bd(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in ukuran,ukuran
                    cangkerang('rm visible.txt')
                    호출('quit')
            Proses.wait(timeout=5)
            pensahihan_lapor['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            pensahihan_lapor['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proses.poll() is None:
                Proses.terminate()
                try: Proses.wait(timeout=5)
                except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
            준비살피미.close(); Proses.stdin.close(); Proses.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(pensahihan_lapor,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Jalan()
