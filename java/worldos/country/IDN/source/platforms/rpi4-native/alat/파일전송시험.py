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
from jaringan_bridge import jaringan_bridge
from Jalankan_perintah import Tugas_akar, perintah
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def jalankan():
    KR_data = Tugas_akar / 'build/verification/ftp'; KR_data.mkdir(parents=True, exist_ok=True)
    validasi_lapor = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Tugas_akar / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkrip = bytearray()
    자바원문 = KR_data / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] argumen) throws Exception { Indonesia.Asli.keluaranTeks.tulis_baris("JAR Jalankan_perintah: " + argumen[0]); Indonesia.Asli.berkas.Tulis("jar.txt", "Asli kernel_VALUE berkas"); Indonesia.Asli.keluaranTeks.tulis_baris(Indonesia.Asli.berkas.Baca("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Tugas_akar/'build/java-library/classes'), '-d', str(KR_data), str(자바원문)])
    Arsip = io.BytesIO()
    with zipfile.ZipFile(Arsip, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(KR_data/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); nomor_port = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_Stream_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with jaringan_bridge(nomor_port, ['tcp:{}:9300'.format(server_Stream_port), 'udp:{}:9301'.format(서버전문접속번호)], ambil=True) as bridge:
        Proses = subprocess.Popen(perintah() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + bridge.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        pemilih = selectors.DefaultSelector(); pemilih.register(Proses.stdout, selectors.EVENT_READ)
        def terima_email(확인표시=b'jkoros-native> ', 시간제한=60):
            data = bytearray(); mengakhiri_OFFSET = time.monotonic() + 시간제한
            while 확인표시 not in data:
                if time.monotonic() > mengakhiri_OFFSET or Proses.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + data.decode('utf-8', 'replace'))
                for 누름값, _ in pemilih.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); transkrip.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8', 'replace').replace('\r\n', '\n')
        def shell(baris_masukan):
            Proses.stdin.write(baris_masukan.encode() + b'\n'); Proses.stdin.flush(); return terima_email()
        try:
            terima_email(); assert 'FTP listening' in shell('ftpd start')
            transfer_file_koneksi = ftplib.FTP(); transfer_file_koneksi.encoding = 'utf-8'; transfer_file_koneksi.connect('127.0.0.1', nomor_port, timeout=20); transfer_file_koneksi.login()
            payload_data = bytes(range(256)) * 32
            transfer_file_koneksi.storbinary('STOR binary.dat', io.BytesIO(payload_data))
            hasil = bytearray(); transfer_file_koneksi.retrbinary('RETR binary.dat', hasil.extend)
            assert hasil == payload_data; assert transfer_file_koneksi.size('binary.dat') == len(payload_data)
            validasi_lapor['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            transfer_file_koneksi.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in shell('cat 한글.txt')
            assert '한글.txt' in transfer_file_koneksi.nlst()
            assert dict(transfer_file_koneksi.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            validasi_lapor['checks'].append('UTF-8 filename and content visible in guest shell')
            try: transfer_file_koneksi.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            hasil = bytearray(); transfer_file_koneksi.retrbinary('RETR binary.dat', hasil.extend); assert hasil == payload_data
            validasi_lapor['checks'].append('oversized replacement rejected; previous file preserved')
            with transfer_file_koneksi.transfercmd('STOR pending.txt') as Upload_File:
                # A control command must not change the active upload's destination.
                assert transfer_file_koneksi.size('binary.dat') == len(payload_data)
                Upload_File.sendall(b'UPLOAD TARGET PRESERVED')
            assert transfer_file_koneksi.voidresp().startswith('226')
            hasil = bytearray(); transfer_file_koneksi.retrbinary('RETR pending.txt', hasil.extend)
            assert hasil == b'UPLOAD TARGET PRESERVED'
            hasil = bytearray(); transfer_file_koneksi.retrbinary('RETR binary.dat', hasil.extend)
            assert hasil == payload_data
            transfer_file_koneksi.delete('pending.txt')
            validasi_lapor['checks'].append('interleaved SIZE cannot change the active STOR destination')
            transfer_file_koneksi.storbinary('STOR 인사.jar', io.BytesIO(Arsip.getvalue()))
            teks = shell('java -jar 인사.jar 누리')
            assert 'JAR Jalankan_perintah: 누리' in teks and 'Asli kernel_VALUE berkas' in teks and 'exit 0' in teks, teks
            teks = shell('./인사.jar 세상')
            assert 'JAR Jalankan_perintah: 세상' in teks and 'exit 0' in teks, teks
            validasi_lapor['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct data { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct data VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = buat_file("cc.txt", baca_tulis | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; tulis_file_data(문서, 인사, sizeof(인사)-1); Tutup_file(문서); tulis_file_data(1, 인사, sizeof(인사)-1); return 0; }\n'
            transfer_file_koneksi.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            teks = shell('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in teks and 'exit 0' in teks, teks
            teks = shell('run 한글.elf'); assert 'CC NATIVE PASS' in teks and 'exit 0' in teks, teks
            assert 'CC NATIVE PASS' in shell('cat cc.txt')
            실행파일 = bytearray(); transfer_file_koneksi.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            transfer_file_koneksi.storbinary('STOR salin_VALUE.elf', io.BytesIO(실행파일)); teks = shell('run salin_VALUE.elf'); assert 'CC NATIVE PASS' in teks and 'exit 0' in teks, teks
            transfer_file_koneksi.storbinary('STOR Jalankan_perintah', io.BytesIO(실행파일)); teks=shell('./Jalankan_perintah');assert 'CC NATIVE PASS' in teks and 'exit 0' in teks,teks
            transfer_file_koneksi.storbinary('STOR Nama_2.txt', io.BytesIO(실행파일)); teks=shell('./Nama_2.txt');assert 'CC NATIVE PASS' in teks and 'exit 0' in teks,teks
            shell('rm Jalankan_perintah Nama_2.txt')
            validasi_lapor['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            shell('rm binary.dat 한글.txt 한글.c 한글.elf salin_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_data/'linux-reference')
            transfer_file_koneksi.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            teks=shell('./리눅스인사');assert 'exit -8' in teks,teks
            teks=shell('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in teks,teks
            assert 'LINUX ELF FILE IO' in shell('cat linux.txt')
            transfer_file_koneksi.delete('리눅스인사');transfer_file_koneksi.delete('linux.txt')
            transfer_file_koneksi.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in shell('./FALSE_VALUE.elf');transfer_file_koneksi.delete('FALSE_VALUE.elf')
            validasi_lapor['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as echo_server_entri:
                통신원문 = KR_data/'eksternal_komunikasi.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class eksternal_komunikasi { public static void main(String[] args) throws Exception {
 Socket Sambung = Indonesia.Asli.연결통신.Sambung("10.0.2.2", Integer.parseInt(args[0]));
 Sambung.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] kodeSumber = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<kodeSumber.length;i++) if (Sambung.getInputStream().read() != (kodeSumber[i]&255)) throw new RuntimeException("TCP mismatch");
 Sambung.close();
 DatagramSocket peserta = Indonesia.Asli.komunikasi.Buka(0); Indonesia.Asli.komunikasi.TIMEOUT(peserta, 500);
 Indonesia.Asli.komunikasi.kirim(peserta, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Indonesia.Asli.komunikasi.terima(peserta).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 peserta.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Tugas_akar/'build/java-library/classes'),'-d',str(KR_data),str(통신원문)])
                transfer_file_koneksi.storbinary('STOR eksternal_komunikasi.class', io.BytesIO((KR_data/'eksternal_komunikasi.class').read_bytes()))
                teks = shell('java eksternal_komunikasi {} {}'.format(echo_server_entri.TCP_port, echo_server_entri.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in teks and '10.0.2.2' in teks and 'exit 0' in teks, teks
                assert echo_server_entri.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, echo_server_entri.수신됨
                assert not echo_server_entri.오류들, echo_server_entri.오류들
            validasi_lapor['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            transfer_file_koneksi.delete('eksternal_komunikasi.class')
            server_sumber=KR_data/'서버시험.java'
            server_sumber.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); DatagramSocket peserta = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket tamu_VALUE = server_VALUE.accept();
  tamu_VALUE.getOutputStream().write(tamu_VALUE.getInputStream().read()+1); tamu_VALUE.close(); server_VALUE.close();
  byte[] Isi_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Isi_VALUE, Isi_VALUE.length); peserta.receive(전문);
  peserta.send(전문); peserta.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_data),str(server_sumber)])
            transfer_file_koneksi.storbinary('STOR 서버시험.class',io.BytesIO((KR_data/'서버시험.class').read_bytes()))
            Proses.stdin.write('java 서버시험\n'.encode());Proses.stdin.flush();terima_email(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_Stream_port),timeout=5) as serekan_VALUE:
                serekan_VALUE.sendall(b'A');assert serekan_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as serekan_VALUE:
                serekan_VALUE.settimeout(5);serekan_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert serekan_VALUE.recvfrom(512)[0]==b'UDP-IN'
            teks=terima_email();assert 'INBOUND TCP UDP PASS' in teks and 'exit 0' in teks,teks
            validasi_lapor['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            transfer_file_koneksi.delete('서버시험.class')
            instruksi_urutan = 'public class 빛 { public static void main(String[] argumen) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } Indonesia.Asli.keluaranTeks.수쓰기(SUM_VALUE); Indonesia.Asli.berkas.Tulis("aot.txt", "한글 AOT berkas 😀"); Indonesia.Asli.keluaranTeks.tulis_baris(Indonesia.Asli.berkas.Baca("aot.txt")); } }'
            transfer_file_koneksi.storbinary('STOR 빛.java', io.BytesIO(instruksi_urutan.encode()))
            teks = shell('javac 빛.java'); assert 'exit 0' in teks and 'Compiled:' in teks, teks
            teks = shell('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in teks and 'exit 0' in teks, teks
            teks = shell('run 빛.elf'); assert '\n55\n' in teks and '한글 AOT berkas 😀' in teks and 'exit 0' in teks, teks
            자체실행파일 = bytearray(); transfer_file_koneksi.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            teks = shell('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in teks and 'unsupported' in teks, teks
            보존자료 = bytearray(); transfer_file_koneksi.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); transfer_file_koneksi.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            transfer_file_koneksi.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            teks = shell('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in teks and 'exit 0' in teks, teks
            teks = shell('run 빛.elf'); assert '\n55\n' in teks and '한글 AOT berkas 😀' in teks and 'exit 0' in teks, teks
            validasi_lapor['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            validasi_lapor['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statik_sumber=KR_data/'정적시험.java'
            statik_sumber.write_text('''public class 정적시험 {
 static int Tugas_akar = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] argumen) {
  int[] VALUE = new int[] {Tugas_akar, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(argumen[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_data),str(statik_sumber)])
            transfer_file_koneksi.storbinary('STOR 정적시험.class',io.BytesIO((KR_data/'정적시험.class').read_bytes()))
            teks=shell('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in teks,teks
            teks=shell('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in teks,teks
            transfer_file_koneksi.delete('정적시험.class');transfer_file_koneksi.delete('정적시험.elf')
            validasi_lapor['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arsip.getvalue());손상자료[14]^=1
            transfer_file_koneksi.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            teks=shell('java -jar 인사.jar');assert 'Main-Class\nexit 1' in teks,teks
            validasi_lapor['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            transfer_file_koneksi.quit(); assert 'FTP stopped' in shell('ftpd stop')
            assert not bridge.galat, bridge.galat
            validasi_lapor.update(passed=True, frames_to_guest=bridge.커널수신틀수, frames_from_guest=bridge.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in pemilih.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: transkrip.extend(조각)
            bridge.Jeda_acara.set()
            Proses.terminate()
            try: Proses.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
            pemilih.close(); Proses.stdin.close(); Proses.stdout.close()
            validasi_lapor['bridge_error'] = bridge.galat
            validasi_lapor['frames_to_guest'] = bridge.커널수신틀수; validasi_lapor['frames_from_guest'] = bridge.커널발신틀수
            (KR_data/'packets.json').write_text(json.dumps(bridge.log_jejak,indent=2)+'\n')
            (KR_data / 'serial.log').write_bytes(transkrip)
            (KR_data / 'report.json').write_text(json.dumps(validasi_lapor, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': jalankan()
