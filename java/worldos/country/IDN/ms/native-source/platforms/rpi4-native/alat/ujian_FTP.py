#!/usr/bin/env python3
"""Real host TCP client -> SLIP -> bare-metal lwIP -> FTP -> Java VFS."""
import ftplib
import hashlib
import io
import json
import selectors
import socket
import subprocess
import time
import zipfile
from rangkaian_penghubung import rangkaian_penghubung
from laksanakan_perintah import projek_akar, Perintah
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Jalan():
    ukuran_data = projek_akar / 'build/verification/ftp'; ukuran_data.mkdir(parents=True, exist_ok=True)
    pensahihan_lapor = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((projek_akar / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = ukuran_data / 'ujian_pakej.java'
    자바원문.write_text('public class ujian_pakej { public static void main(String[] 인수) throws Exception { Melayu.Asli.출력.tulis_baris("JAR laksanakan_perintah: " + 인수[0]); Melayu.Asli.Fail.Tulis("jar.txt", "Asli kernel_VALUE Fail"); Melayu.Asli.출력.tulis_baris(Melayu.Asli.Fail.Baca("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(projek_akar/'build/java-library/classes'), '-d', str(ukuran_data), str(자바원문)])
    Arkib = io.BytesIO()
    with zipfile.ZipFile(Arkib, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: ujian_pakej\r\n\r\n')
        자바꾸러미.write(str(ukuran_data/'ujian_pakej.class'), 'ujian_pakej.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); nombor_port = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); pelayan_strim_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with rangkaian_penghubung(nombor_port, ['tcp:{}:9300'.format(pelayan_strim_port), 'udp:{}:9301'.format(서버전문접속번호)], rakam=True) as penghubung:
        Proses = subprocess.Popen(Perintah() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + penghubung.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        준비선택기 = selectors.DefaultSelector(); 준비선택기.register(Proses.stdout, selectors.EVENT_READ)
        def 수신하기(penanda=b'jkoros-native> ', 시간제한=60):
            data = bytearray(); tamat_Ofset = time.monotonic() + 시간제한
            while penanda not in data:
                if time.monotonic() > tamat_Ofset or Proses.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + data.decode('utf-8', 'replace'))
                for 누름값, _ in 준비선택기.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8', 'replace').replace('\r\n', '\n')
        def cangkerang(baris):
            Proses.stdin.write(baris.encode() + b'\n'); Proses.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in cangkerang('ftpd start')
            pemindahan_fail_hubungan = ftplib.FTP(); pemindahan_fail_hubungan.encoding = 'utf-8'; pemindahan_fail_hubungan.connect('127.0.0.1', nombor_port, timeout=20); pemindahan_fail_hubungan.login()
            muat_beban_data = bytes(range(256)) * 32
            pemindahan_fail_hubungan.storbinary('STOR binary.dat', io.BytesIO(muat_beban_data))
            ukuran = bytearray(); pemindahan_fail_hubungan.retrbinary('RETR binary.dat', ukuran.extend)
            assert ukuran == muat_beban_data; assert pemindahan_fail_hubungan.size('binary.dat') == len(muat_beban_data)
            pensahihan_lapor['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            pemindahan_fail_hubungan.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in cangkerang('cat 한글.txt')
            assert '한글.txt' in pemindahan_fail_hubungan.nlst()
            assert dict(pemindahan_fail_hubungan.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            pensahihan_lapor['checks'].append('UTF-8 filename and content visible in guest shell')
            try: pemindahan_fail_hubungan.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            ukuran = bytearray(); pemindahan_fail_hubungan.retrbinary('RETR binary.dat', ukuran.extend); assert ukuran == muat_beban_data
            pensahihan_lapor['checks'].append('oversized replacement rejected; previous file preserved')
            with pemindahan_fail_hubungan.transfercmd('STOR pending.txt') as Upload_Fail:
                # A control command must not change the active upload's destination.
                assert pemindahan_fail_hubungan.size('binary.dat') == len(muat_beban_data)
                Upload_Fail.sendall(b'UPLOAD TARGET PRESERVED')
            assert pemindahan_fail_hubungan.voidresp().startswith('226')
            ukuran = bytearray(); pemindahan_fail_hubungan.retrbinary('RETR pending.txt', ukuran.extend)
            assert ukuran == b'UPLOAD TARGET PRESERVED'
            ukuran = bytearray(); pemindahan_fail_hubungan.retrbinary('RETR binary.dat', ukuran.extend)
            assert ukuran == muat_beban_data
            pemindahan_fail_hubungan.delete('pending.txt')
            pensahihan_lapor['checks'].append('interleaved SIZE cannot change the active STOR destination')
            pemindahan_fail_hubungan.storbinary('STOR 인사.jar', io.BytesIO(Arkib.getvalue()))
            Teks = cangkerang('java -jar 인사.jar 누리')
            assert 'JAR laksanakan_perintah: 누리' in Teks and 'Asli kernel_VALUE Fail' in Teks and 'exit 0' in Teks, Teks
            Teks = cangkerang('./인사.jar 세상')
            assert 'JAR laksanakan_perintah: 세상' in Teks and 'exit 0' in Teks, Teks
            pensahihan_lapor['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct data { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct data VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = buka_fail("cc.txt", baca_tulis | 없으면만들기 | potong_TOC, 0600); if (문서 < 0) return 1; tulis_fail_data(문서, 인사, sizeof(인사)-1); Tutup_fail(문서); tulis_fail_data(1, 인사, sizeof(인사)-1); return 0; }\n'
            pemindahan_fail_hubungan.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Teks = cangkerang('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Teks and 'exit 0' in Teks, Teks
            Teks = cangkerang('run 한글.elf'); assert 'CC NATIVE PASS' in Teks and 'exit 0' in Teks, Teks
            assert 'CC NATIVE PASS' in cangkerang('cat cc.txt')
            fail_boleh_laku = bytearray(); pemindahan_fail_hubungan.retrbinary('RETR 한글.elf', fail_boleh_laku.extend)
            assert fail_boleh_laku[:4] == b'\x7fELF' and fail_boleh_laku[18:20] == b'\xb7\x00'
            pemindahan_fail_hubungan.storbinary('STOR tika_VALUE.elf', io.BytesIO(fail_boleh_laku)); Teks = cangkerang('run tika_VALUE.elf'); assert 'CC NATIVE PASS' in Teks and 'exit 0' in Teks, Teks
            pemindahan_fail_hubungan.storbinary('STOR laksanakan_perintah', io.BytesIO(fail_boleh_laku)); Teks=cangkerang('./laksanakan_perintah');assert 'CC NATIVE PASS' in Teks and 'exit 0' in Teks,Teks
            pemindahan_fail_hubungan.storbinary('STOR Nama.txt', io.BytesIO(fail_boleh_laku)); Teks=cangkerang('./Nama.txt');assert 'CC NATIVE PASS' in Teks and 'exit 0' in Teks,Teks
            cangkerang('rm laksanakan_perintah Nama.txt')
            pensahihan_lapor['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            cangkerang('rm binary.dat 한글.txt 한글.c 한글.elf tika_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(ukuran_data/'linux-reference')
            pemindahan_fail_hubungan.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Teks=cangkerang('./리눅스인사');assert 'exit -8' in Teks,Teks
            Teks=cangkerang('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Teks,Teks
            assert 'LINUX ELF FILE IO' in cangkerang('cat linux.txt')
            pemindahan_fail_hubungan.delete('리눅스인사');pemindahan_fail_hubungan.delete('linux.txt')
            pemindahan_fail_hubungan.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in cangkerang('./FALSE_VALUE.elf');pemindahan_fail_hubungan.delete('FALSE_VALUE.elf')
            pensahihan_lapor['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = ukuran_data/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Sambung = Melayu.Asli.연결통신.Sambung("10.0.2.2", Integer.parseInt(args[0]));
 Sambung.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] SUMBER = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<SUMBER.length;i++) if (Sambung.getInputStream().read() != (SUMBER[i]&255)) throw new RuntimeException("TCP mismatch");
 Sambung.close();
 DatagramSocket peserta = Melayu.Asli.통신.Buka(0); Melayu.Asli.통신.TIMEOUT(peserta, 500);
 Melayu.Asli.통신.e_mel_9aee63bd(peserta, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Melayu.Asli.통신.받기(peserta).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 peserta.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(projek_akar/'build/java-library/classes'),'-d',str(ukuran_data),str(통신원문)])
                pemindahan_fail_hubungan.storbinary('STOR 바깥통신.class', io.BytesIO((ukuran_data/'바깥통신.class').read_bytes()))
                Teks = cangkerang('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_port, 되돌림서버항목.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in Teks and '10.0.2.2' in Teks and 'exit 0' in Teks, Teks
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            pensahihan_lapor['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            pemindahan_fail_hubungan.delete('바깥통신.class')
            pelayan_sumber=ukuran_data/'pelayan_ujian.java'
            pelayan_sumber.write_text('''import java.net.*; public class pelayan_ujian {
 public static void main(String[] args) throws Exception {
  ServerSocket pelayan_VALUE = new ServerSocket(9300); DatagramSocket peserta = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket tetamu_VALUE = pelayan_VALUE.accept();
  tetamu_VALUE.getOutputStream().write(tetamu_VALUE.getInputStream().read()+1); tetamu_VALUE.close(); pelayan_VALUE.close();
  byte[] Kandungan_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Kandungan_VALUE, Kandungan_VALUE.length); peserta.receive(전문);
  peserta.send(전문); peserta.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ukuran_data),str(pelayan_sumber)])
            pemindahan_fail_hubungan.storbinary('STOR pelayan_ujian.class',io.BytesIO((ukuran_data/'pelayan_ujian.class').read_bytes()))
            Proses.stdin.write('java pelayan_ujian\n'.encode());Proses.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',pelayan_strim_port),timeout=5) as rakan_VALUE:
                rakan_VALUE.sendall(b'A');assert rakan_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as rakan_VALUE:
                rakan_VALUE.settimeout(5);rakan_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert rakan_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Teks=수신하기();assert 'INBOUND TCP UDP PASS' in Teks and 'exit 0' in Teks,Teks
            pensahihan_lapor['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            pemindahan_fail_hubungan.delete('pelayan_ujian.class')
            suruhan_jujukan = 'public class 빛 { public static void main(String[] 인수) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } Melayu.Asli.출력.수쓰기(SUM_VALUE); Melayu.Asli.Fail.Tulis("aot.txt", "한글 AOT Fail 😀"); Melayu.Asli.출력.tulis_baris(Melayu.Asli.Fail.Baca("aot.txt")); } }'
            pemindahan_fail_hubungan.storbinary('STOR 빛.java', io.BytesIO(suruhan_jujukan.encode()))
            Teks = cangkerang('javac 빛.java'); assert 'exit 0' in Teks and 'Compiled:' in Teks, Teks
            Teks = cangkerang('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Teks and 'exit 0' in Teks, Teks
            Teks = cangkerang('run 빛.elf'); assert '\n55\n' in Teks and '한글 AOT Fail 😀' in Teks and 'exit 0' in Teks, Teks
            asal = bytearray(); pemindahan_fail_hubungan.retrbinary('RETR 빛.elf', asal.extend)
            Teks = cangkerang('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Teks and 'unsupported' in Teks, Teks
            보존자료 = bytearray(); pemindahan_fail_hubungan.retrbinary('RETR 빛.elf', 보존자료.extend); assert asal == 보존자료
            바이트코드 = bytearray(); pemindahan_fail_hubungan.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            pemindahan_fail_hubungan.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Teks = cangkerang('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Teks and 'exit 0' in Teks, Teks
            Teks = cangkerang('run 빛.elf'); assert '\n55\n' in Teks and '한글 AOT Fail 😀' in Teks and 'exit 0' in Teks, Teks
            pensahihan_lapor['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            pensahihan_lapor['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statik_sumber=ukuran_data/'statik_ujian.java'
            statik_sumber.write_text('''public class statik_ujian {
 static int projek_akar = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] 인수) {
  int[] VALUE = new int[] {projek_akar, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ukuran_data),str(statik_sumber)])
            pemindahan_fail_hubungan.storbinary('STOR statik_ujian.class',io.BytesIO((ukuran_data/'statik_ujian.class').read_bytes()))
            Teks=cangkerang('jaot statik_ujian.class -o statik_ujian.elf');assert 'exit 0' in Teks,Teks
            Teks=cangkerang('run statik_ujian.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Teks,Teks
            pemindahan_fail_hubungan.delete('statik_ujian.class');pemindahan_fail_hubungan.delete('statik_ujian.elf')
            pensahihan_lapor['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arkib.getvalue());손상자료[14]^=1
            pemindahan_fail_hubungan.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Teks=cangkerang('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Teks,Teks
            pensahihan_lapor['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            pemindahan_fail_hubungan.quit(); assert 'FTP stopped' in cangkerang('ftpd stop')
            assert not penghubung.RALAT, penghubung.RALAT
            pensahihan_lapor.update(passed=True, frames_to_guest=penghubung.커널수신틀수, frames_from_guest=penghubung.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in 준비선택기.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            penghubung.Jeda_acara.set()
            Proses.terminate()
            try: Proses.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
            준비선택기.close(); Proses.stdin.close(); Proses.stdout.close()
            pensahihan_lapor['bridge_error'] = penghubung.RALAT
            pensahihan_lapor['frames_to_guest'] = penghubung.커널수신틀수; pensahihan_lapor['frames_from_guest'] = penghubung.커널발신틀수
            (ukuran_data/'packets.json').write_text(json.dumps(penghubung.jejak_LOG,indent=2)+'\n')
            (ukuran_data / 'serial.log').write_bytes(대화기록)
            (ukuran_data / 'report.json').write_text(json.dumps(pensahihan_lapor, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Jalan()
