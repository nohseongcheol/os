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
from cầuNốiMạng import cầuNốiMạng
from thựcThiLệnh import gốcCâyDựÁn, lệnh
from MẫuThửVọngLại import MẫuThửVọngLại
from thửELF import víDụLinux


def chạy():
    dữLiệuKếtQuả = gốcCâyDựÁn / 'build/verification/ftp'; dữLiệuKếtQuả.mkdir(parents=True, exist_ok=True)
    báoCáoViệcThẩmĐịnh = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((gốcCâyDựÁn / 'build/kernel8.img').read_bytes()).hexdigest()}
    bảnGhiDiễnTiến = bytearray()
    nguồnJava = dữLiệuKếtQuả / 'thửGóiGộp.java'
    nguồnJava.write_text('public class thửGóiGộp { public static void main(String[] cácĐốiSố) throws Exception { tiếngViệt.tựThân.ĐầuRa.ghiDòng("JAR thựcThiLệnh: " + cácĐốiSố[0]); tiếngViệt.tựThân.Tệp.ghi("jar.txt", "tựThân giáTrịNhân Tệp"); tiếngViệt.tựThân.ĐầuRa.ghiDòng(tiếngViệt.tựThân.Tệp.đọc("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(gốcCâyDựÁn/'build/java-library/classes'), '-d', str(dữLiệuKếtQuả), str(nguồnJava)])
    khoLưuTrữ = io.BytesIO()
    with zipfile.ZipFile(khoLưuTrữ, 'w', zipfile.ZIP_DEFLATED) as góiGộpJava:
        góiGộpJava.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: thửGóiGộp\r\n\r\n')
        góiGộpJava.write(str(dữLiệuKếtQuả/'thửGóiGộp.class'), 'thửGóiGộp.class')
    with socket.socket() as tạm:
        tạm.bind(('127.0.0.1', 0)); sốCổng = tạm.getsockname()[1]
    with socket.socket() as tạm:
        tạm.bind(('127.0.0.1', 0)); cổngLuồngMáyChủ = tạm.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as tạm:
        tạm.bind(('127.0.0.1', 0)); cổngĐiệnDữLiệuMáyChủ = tạm.getsockname()[1]
    with cầuNốiMạng(sốCổng, ['tcp:{}:9300'.format(cổngLuồngMáyChủ), 'udp:{}:9301'.format(cổngĐiệnDữLiệuMáyChủ)], thuGiữ=True) as cầuNối:
        tiếnTrình = subprocess.Popen(lệnh() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + cầuNối.đốiSốĐãChuyểnTiếp(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        bộChọn = selectors.DefaultSelector(); bộChọn.register(tiếnTrình.stdout, selectors.EVENT_READ)
        def nhậnThôngĐiệp(dấuMốc=b'jkoros-native> ', hếtGiờViệcThựcThi=60):
            DữLiệu = bytearray(); độLệchKếtThúc = time.monotonic() + hếtGiờViệcThựcThi
            while dấuMốc not in DữLiệu:
                if time.monotonic() > độLệchKếtThúc or tiếnTrình.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + DữLiệu.decode('utf-8', 'replace'))
                for giáTrịĐãNhấn, _ in bộChọn.select(.1):
                    giáTrịĐoạn = giáTrịĐãNhấn.fileobj.read(4096)
                    if giáTrịĐoạn: DữLiệu.extend(giáTrịĐoạn); bảnGhiDiễnTiến.extend(giáTrịĐoạn)
                if b'PANIC:' in DữLiệu or b'FAIL ' in DữLiệu: raise AssertionError(DữLiệu)
            return DữLiệu.decode('utf-8', 'replace').replace('\r\n', '\n')
        def vỏLệnh(dòng):
            tiếnTrình.stdin.write(dòng.encode() + b'\n'); tiếnTrình.stdin.flush(); return nhậnThôngĐiệp()
        try:
            nhậnThôngĐiệp(); assert 'FTP listening' in vỏLệnh('ftpd start')
            kếtNốiChuyểnGiaoTệp = ftplib.FTP(); kếtNốiChuyểnGiaoTệp.encoding = 'utf-8'; kếtNốiChuyểnGiaoTệp.connect('127.0.0.1', sốCổng, timeout=20); kếtNốiChuyểnGiaoTệp.login()
            dữLiệuNộiTải = bytes(range(256)) * 32
            kếtNốiChuyểnGiaoTệp.storbinary('STOR binary.dat', io.BytesIO(dữLiệuNộiTải))
            kếtQuả = bytearray(); kếtNốiChuyểnGiaoTệp.retrbinary('RETR binary.dat', kếtQuả.extend)
            assert kếtQuả == dữLiệuNộiTải; assert kếtNốiChuyểnGiaoTệp.size('binary.dat') == len(dữLiệuNộiTải)
            báoCáoViệcThẩmĐịnh['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            kếtNốiChuyểnGiaoTệp.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in vỏLệnh('cat 한글.txt')
            assert '한글.txt' in kếtNốiChuyểnGiaoTệp.nlst()
            assert dict(kếtNốiChuyểnGiaoTệp.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            báoCáoViệcThẩmĐịnh['checks'].append('UTF-8 filename and content visible in guest shell')
            try: kếtNốiChuyểnGiaoTệp.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as mụcPhụTrợ: assert str(mụcPhụTrợ).startswith('552'), str(mụcPhụTrợ)
            else: raise AssertionError('oversized upload accepted')
            kếtQuả = bytearray(); kếtNốiChuyểnGiaoTệp.retrbinary('RETR binary.dat', kếtQuả.extend); assert kếtQuả == dữLiệuNộiTải
            báoCáoViệcThẩmĐịnh['checks'].append('oversized replacement rejected; previous file preserved')
            with kếtNốiChuyểnGiaoTệp.transfercmd('STOR pending.txt') as cácTệpTảiLên:
                # A control command must not change the active upload's destination.
                assert kếtNốiChuyểnGiaoTệp.size('binary.dat') == len(dữLiệuNộiTải)
                cácTệpTảiLên.sendall(b'UPLOAD TARGET PRESERVED')
            assert kếtNốiChuyểnGiaoTệp.voidresp().startswith('226')
            kếtQuả = bytearray(); kếtNốiChuyểnGiaoTệp.retrbinary('RETR pending.txt', kếtQuả.extend)
            assert kếtQuả == b'UPLOAD TARGET PRESERVED'
            kếtQuả = bytearray(); kếtNốiChuyểnGiaoTệp.retrbinary('RETR binary.dat', kếtQuả.extend)
            assert kếtQuả == dữLiệuNộiTải
            kếtNốiChuyểnGiaoTệp.delete('pending.txt')
            báoCáoViệcThẩmĐịnh['checks'].append('interleaved SIZE cannot change the active STOR destination')
            kếtNốiChuyểnGiaoTệp.storbinary('STOR LờiChào.jar', io.BytesIO(khoLưuTrữ.getvalue()))
            vănBản = vỏLệnh('java -jar LờiChào.jar 누리')
            assert 'JAR thựcThiLệnh: 누리' in vănBản and 'tựThân giáTrịNhân Tệp' in vănBản and 'exit 0' in vănBản, vănBản
            vănBản = vỏLệnh('./LờiChào.jar 세상')
            assert 'JAR thựcThiLệnh: 세상' in vănBản and 'exit 0' in vănBản, vănBản
            báoCáoViệcThẩmĐịnh['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            dữLiệuNguyênBản = '#include <ABITệp.h>\nstruct DữLiệu { int trịSố; double 비율; };\nint giáTrịTổng(int n) { return n ? n + giáTrịTổng(n-1) : 0; }\nint main(void) { struct DữLiệu giáTrị = {giáTrịTổng(10), 1.25}; if (giáTrị.trịSố != 55 || giáTrị.비율 * 2 != 2.5) return 3; const char LờiChào[] = "CC NATIVE PASS\\n"; int TàiLiệu = mởTệp("cc.txt", GhiĐọc | ThiếuNếuTạo | CácNộiDungCắtNgắn, 0600); if (TàiLiệu < 0) return 1; ghiDữLiệuTệp(TàiLiệu, LờiChào, sizeof(LờiChào)-1); đóngTệp(TàiLiệu); ghiDữLiệuTệp(1, LờiChào, sizeof(LờiChào)-1); return 0; }\n'
            kếtNốiChuyểnGiaoTệp.storbinary('STOR vănBảnHangul.c', io.BytesIO(dữLiệuNguyênBản.encode()))
            vănBản = vỏLệnh('cc vănBảnHangul.c -o vănBảnHangul.elf'); assert 'Compiled native ARM64 ELF:' in vănBản and 'exit 0' in vănBản, vănBản
            vănBản = vỏLệnh('run vănBảnHangul.elf'); assert 'CC NATIVE PASS' in vănBản and 'exit 0' in vănBản, vănBản
            assert 'CC NATIVE PASS' in vỏLệnh('cat cc.txt')
            tệpTệpThựcThi = bytearray(); kếtNốiChuyểnGiaoTệp.retrbinary('RETR vănBảnHangul.elf', tệpTệpThựcThi.extend)
            assert tệpTệpThựcThi[:4] == b'\x7fELF' and tệpTệpThựcThi[18:20] == b'\xb7\x00'
            kếtNốiChuyểnGiaoTệp.storbinary('STOR saoChépGiáTrị.elf', io.BytesIO(tệpTệpThựcThi)); vănBản = vỏLệnh('run saoChépGiáTrị.elf'); assert 'CC NATIVE PASS' in vănBản and 'exit 0' in vănBản, vănBản
            kếtNốiChuyểnGiaoTệp.storbinary('STOR thựcThiLệnh', io.BytesIO(tệpTệpThựcThi)); vănBản=vỏLệnh('./thựcThiLệnh');assert 'CC NATIVE PASS' in vănBản and 'exit 0' in vănBản,vănBản
            kếtNốiChuyểnGiaoTệp.storbinary('STOR tên.txt', io.BytesIO(tệpTệpThựcThi)); vănBản=vỏLệnh('./tên.txt');assert 'CC NATIVE PASS' in vănBản and 'exit 0' in vănBản,vănBản
            vỏLệnh('rm thựcThiLệnh tên.txt')
            báoCáoViệcThẩmĐịnh['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            vỏLệnh('rm binary.dat vănBảnHangul.txt vănBảnHangul.c vănBảnHangul.elf saoChépGiáTrị.elf cc.txt jar.txt')
            tệpLinux,dựKiến=víDụLinux(dữLiệuKếtQuả/'linux-reference')
            kếtNốiChuyểnGiaoTệp.storbinary('STOR 리눅스인사',io.BytesIO(tệpLinux.read_bytes()))
            vănBản=vỏLệnh('./리눅스인사');assert 'exit -8' in vănBản,vănBản
            vănBản=vỏLệnh('run --linux 리눅스인사 한글인수');assert dựKiến+'exit 0' in vănBản,vănBản
            assert 'LINUX ELF FILE IO' in vỏLệnh('cat linux.txt')
            kếtNốiChuyểnGiaoTệp.delete('리눅스인사');kếtNốiChuyểnGiaoTệp.delete('linux.txt')
            kếtNốiChuyểnGiaoTệp.storbinary('STOR giáTrịSaiLuậnLý.elf',io.BytesIO(b'plain text'))
            assert '실행할 trịSố 없습니다:' in vỏLệnh('./giáTrịSaiLuậnLý.elf');kếtNốiChuyểnGiaoTệp.delete('giáTrịSaiLuậnLý.elf')
            báoCáoViệcThẩmĐịnh['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with MẫuThửVọngLại() as mụcMáyChủVọngLại:
                nguồnMạngGọn = dữLiệuKếtQuả/'TruyềnThôngBênNgoài.java'
                nguồnMạngGọn.write_text('''import java.net.*; import java.io.*;
public class TruyềnThôngBênNgoài { public static void main(String[] args) throws Exception {
 Socket nốiKết = tiếngViệt.tựThân.vậnChuyểnKếtNối.nốiKết("10.0.2.2", Integer.parseInt(args[0]));
 nốiKết.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] mãNguồn = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<mãNguồn.length;i++) if (nốiKết.getInputStream().read() != (mãNguồn[i]&255)) throw new RuntimeException("TCP mismatch");
 nốiKết.close();
 DatagramSocket điểmCuối = tiếngViệt.tựThân.TruyềnThông.mở(0); tiếngViệt.tựThân.TruyềnThông.hếtGiờ(điểmCuối, 500);
 tiếngViệt.tựThân.TruyềnThông.gửi(điểmCuối, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!tiếngViệt.tựThân.TruyềnThông.nhận(điểmCuối).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 điểmCuối.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(gốcCâyDựÁn/'build/java-library/classes'),'-d',str(dữLiệuKếtQuả),str(nguồnMạngGọn)])
                kếtNốiChuyểnGiaoTệp.storbinary('STOR TruyềnThôngBênNgoài.class', io.BytesIO((dữLiệuKếtQuả/'TruyềnThôngBênNgoài.class').read_bytes()))
                vănBản = vỏLệnh('java TruyềnThôngBênNgoài {} {}'.format(mụcMáyChủVọngLại.cổngTCP, mụcMáyChủVọngLại.cổngUDP))
                assert 'EXTERNAL TCP UDP PASS' in vănBản and '10.0.2.2' in vănBản and 'exit 0' in vănBản, vănBản
                assert mụcMáyChủVọngLại.cóĐãNhận == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, mụcMáyChủVọngLại.cóĐãNhận
                assert not mụcMáyChủVọngLại.cácLỗi, mụcMáyChủVọngLại.cácLỗi
            báoCáoViệcThẩmĐịnh['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            kếtNốiChuyểnGiaoTệp.delete('TruyềnThôngBênNgoài.class')
            nguồnMáyChủ=dữLiệuKếtQuả/'ThửMáyChủ.java'
            nguồnMáyChủ.write_text('''import java.net.*; public class ThửMáyChủ {
 public static void main(String[] args) throws Exception {
  ServerSocket giáTrịMáyChủ = new ServerSocket(9300); DatagramSocket điểmCuối = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket giáTrịKhách = giáTrịMáyChủ.accept();
  giáTrịKhách.getOutputStream().write(giáTrịKhách.getInputStream().read()+1); giáTrịKhách.close(); giáTrịMáyChủ.close();
  byte[] giáTrịNộiDung = new byte[8]; DatagramPacket điệnDữLiệu = new DatagramPacket(giáTrịNộiDung, giáTrịNộiDung.length); điểmCuối.receive(điệnDữLiệu);
  điểmCuối.send(điệnDữLiệu); điểmCuối.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(dữLiệuKếtQuả),str(nguồnMáyChủ)])
            kếtNốiChuyểnGiaoTệp.storbinary('STOR ThửMáyChủ.class',io.BytesIO((dữLiệuKếtQuả/'ThửMáyChủ.class').read_bytes()))
            tiếnTrình.stdin.write('java ThửMáyChủ\n'.encode());tiếnTrình.stdin.flush();nhậnThôngĐiệp(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',cổngLuồngMáyChủ),timeout=5) as giáTrịĐốiTác:
                giáTrịĐốiTác.sendall(b'A');assert giáTrịĐốiTác.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as giáTrịĐốiTác:
                giáTrịĐốiTác.settimeout(5);giáTrịĐốiTác.sendto(b'UDP-IN',('127.0.0.1',cổngĐiệnDữLiệuMáyChủ));assert giáTrịĐốiTác.recvfrom(512)[0]==b'UDP-IN'
            vănBản=nhậnThôngĐiệp();assert 'INBOUND TCP UDP PASS' in vănBản and 'exit 0' in vănBản,vănBản
            báoCáoViệcThẩmĐịnh['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            kếtNốiChuyểnGiaoTệp.delete('ThửMáyChủ.class')
            dãyChỉLệnh = 'public class Màu { public static void main(String[] cácĐốiSố) throws Exception { int giáTrịTổng = 0; int trịSố = 1; while (trịSố <= 10) { giáTrịTổng = giáTrịTổng + trịSố; trịSố = trịSố + 1; } tiếngViệt.tựThân.ĐầuRa.ghiSố(giáTrịTổng); tiếngViệt.tựThân.Tệp.ghi("aot.txt", "한글 AOT Tệp 😀"); tiếngViệt.tựThân.ĐầuRa.ghiDòng(tiếngViệt.tựThân.Tệp.đọc("aot.txt")); } }'
            kếtNốiChuyểnGiaoTệp.storbinary('STOR Màu.java', io.BytesIO(dãyChỉLệnh.encode()))
            vănBản = vỏLệnh('javac Màu.java'); assert 'exit 0' in vănBản and 'Compiled:' in vănBản, vănBản
            vănBản = vỏLệnh('jaot Màu.class -o Màu.elf'); assert 'AOT compiled native ARM64 ELF:' in vănBản and 'exit 0' in vănBản, vănBản
            vănBản = vỏLệnh('run Màu.elf'); assert '\n55\n' in vănBản and '한글 AOT Tệp 😀' in vănBản and 'exit 0' in vănBản, vănBản
            bảnĐịa = bytearray(); kếtNốiChuyểnGiaoTệp.retrbinary('RETR Màu.elf', bảnĐịa.extend)
            vănBản = vỏLệnh('jaot LờiChào.jar -o Màu.elf'); assert 'exit 1' in vănBản and 'unsupported' in vănBản, vănBản
            dữLiệuĐãGiữNguyên = bytearray(); kếtNốiChuyểnGiaoTệp.retrbinary('RETR Màu.elf', dữLiệuĐãGiữNguyên.extend); assert bảnĐịa == dữLiệuĐãGiữNguyên
            mãByte = bytearray(); kếtNốiChuyểnGiaoTệp.retrbinary('RETR Màu.class', mãByte.extend)
            đãĐóngGói = io.BytesIO()
            with zipfile.ZipFile(đãĐóngGói, 'w', zipfile.ZIP_DEFLATED) as góiGộpJava:
                góiGộpJava.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: Màu\r\n\r\n')
                góiGộpJava.writestr('Màu.class', mãByte)
            kếtNốiChuyểnGiaoTệp.storbinary('STOR Màu.jar', io.BytesIO(đãĐóngGói.getvalue()))
            vănBản = vỏLệnh('jaot Màu.jar -o Màu.elf'); assert 'AOT compiled native ARM64 ELF:' in vănBản and 'exit 0' in vănBản, vănBản
            vănBản = vỏLệnh('run Màu.elf'); assert '\n55\n' in vănBản and '한글 AOT Tệp 😀' in vănBản and 'exit 0' in vănBản, vănBản
            báoCáoViệcThẩmĐịnh['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            báoCáoViệcThẩmĐịnh['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            nguồnTĩnh=dữLiệuKếtQuả/'ThửTĩnh.java'
            nguồnTĩnh.write_text('''public class ThửTĩnh {
 static int gốcCâyDựÁn = 3;
 static int giáTrịTổng(int n) { return n == 0 ? 0 : n + giáTrịTổng(n-1); }
 public static void main(String[] cácĐốiSố) {
  int[] giáTrị = new int[] {gốcCâyDựÁn, giáTrịTổng(10)};
  System.out.println(giáTrị[0] + giáTrị[1]); System.out.println(cácĐốiSố[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(dữLiệuKếtQuả),str(nguồnTĩnh)])
            kếtNốiChuyểnGiaoTệp.storbinary('STOR ThửTĩnh.class',io.BytesIO((dữLiệuKếtQuả/'ThửTĩnh.class').read_bytes()))
            vănBản=vỏLệnh('jaot ThửTĩnh.class -o ThửTĩnh.elf');assert 'exit 0' in vănBản,vănBản
            vănBản=vỏLệnh('run ThửTĩnh.elf 한글인수');assert '\n58\n한글인수\nexit 0' in vănBản,vănBản
            kếtNốiChuyểnGiaoTệp.delete('ThửTĩnh.class');kếtNốiChuyểnGiaoTệp.delete('ThửTĩnh.elf')
            báoCáoViệcThẩmĐịnh['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            hỏng=bytearray(khoLưuTrữ.getvalue());hỏng[14]^=1
            kếtNốiChuyểnGiaoTệp.storbinary('STOR LờiChào.jar',io.BytesIO(hỏng))
            vănBản=vỏLệnh('java -jar LờiChào.jar');assert 'Main-Class\nexit 1' in vănBản,vănBản
            báoCáoViệcThẩmĐịnh['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            kếtNốiChuyểnGiaoTệp.quit(); assert 'FTP stopped' in vỏLệnh('ftpd stop')
            assert not cầuNối.lỗi, cầuNối.lỗi
            báoCáoViệcThẩmĐịnh.update(passed=True, frames_to_guest=cầuNối.kháchĐếnCácKhung, frames_from_guest=cầuNối.kháchTừCácKhung)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for giáTrịĐãNhấn,_ in bộChọn.select(0):
                giáTrịĐoạn=giáTrịĐãNhấn.fileobj.read(65536)
                if giáTrịĐoạn: bảnGhiDiễnTiến.extend(giáTrịĐoạn)
            cầuNối.sựKiệnTạmDừng.set()
            tiếnTrình.terminate()
            try: tiếnTrình.wait(timeout=5)
            except subprocess.TimeoutExpired: tiếnTrình.kill(); tiếnTrình.wait()
            bộChọn.close(); tiếnTrình.stdin.close(); tiếnTrình.stdout.close()
            báoCáoViệcThẩmĐịnh['bridge_error'] = cầuNối.lỗi
            báoCáoViệcThẩmĐịnh['frames_to_guest'] = cầuNối.kháchĐếnCácKhung; báoCáoViệcThẩmĐịnh['frames_from_guest'] = cầuNối.kháchTừCácKhung
            (dữLiệuKếtQuả/'packets.json').write_text(json.dumps(cầuNối.nhậtKýDấuVết,indent=2)+'\n')
            (dữLiệuKếtQuả / 'serial.log').write_bytes(bảnGhiDiễnTiến)
            (dữLiệuKếtQuả / 'report.json').write_text(json.dumps(báoCáoViệcThẩmĐịnh, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': chạy()
