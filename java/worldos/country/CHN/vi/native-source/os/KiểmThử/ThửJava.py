#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 thựcThiLệnh, giáTrịSựThấtBại/giáTrịTàiNguyên giáTrịRanhGiới KiểmThử."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import time
from thửMạngNgườiDùng import MáyẢo, vịTrí


def giáTrịSửa(máy, tên, giáTrịNộiDung, giáTrịCất=True):
    chạy = len(máy.bảnGhiNhậtKý)
    máy.giáTrịNốiTiếp.sendall(('edit ' + tên + '\n').encode())
    máy.chờTrạngThái('...> ', chạy)
    for dòng in giáTrịNộiDung.splitlines():
        assert len(dòng) <= 128
        chạy = len(máy.bảnGhiNhậtKý)
        máy.giáTrịNốiTiếp.sendall((dòng + '\n').encode())
        máy.chờTrạngThái('...> ', chạy)
    chạy = len(máy.bảnGhiNhậtKý)
    máy.giáTrịNốiTiếp.sendall(b'.save\n' if giáTrịCất else b'.cancel\n')
    kếtQuả = máy.chờTrạngThái('jkoros> ', chạy)
    assert ('Saved:' if giáTrịCất else 'Cancelled; original preserved') in kếtQuả, kếtQuả


def địaChỉTệp():
    kếtQuả = subprocess.check_output(['nm', '-n', str(vịTrí / 'build/kernel.elf')], universal_newlines=True)
    for dòng in kếtQuả.splitlines():
        if dòng.endswith(' ram_files'):
            return int(dòng.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def tệpKhách(máy, giáTrịÔ, cỡ, đườngDẫn):
    # KiểmThử VM의 메모리에서 dữLiệuThựcTế 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    địaChỉ = địaChỉTệp() + giáTrịÔ * 16384
    máy.giáTrịBộGiámSát.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(địaChỉ, cỡ, đườngDẫn)).encode())
    phầnKết = time.monotonic() + 5
    while time.monotonic() < phầnKết:
        if đườngDẫn.exists() and đườngDẫn.stat().st_size == cỡ:
            return đườngDẫn.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def thửChạy(giáTrịLoại):
    máy = MáyẢo(vịTrí / ('build/kernel.elf' if giáTrịLoại == 'elf' else 'build/kernel.iso'), giáTrịLoại, giáTrịMạng=False)
    kếtQuả = {}
    try:
        máy.lệnh('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        máy.lệnh('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        máy.lệnh('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        máy.lệnh('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        máy.lệnh('java Missing', ['cannot read class: -2', 'Exit: 1'])
        máy.lệnh('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        máy.lệnh('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        giáTrịNộiDung = '''public class Calc {
 public static int fact(int n) {
  if (n <= 1) { return 1; } else { return n * fact(n - 1); }
 }
 public static boolean check(int n) { return n == 7; }
 public static void main(String[] args) {
  int n = Integer.parseInt(args[0]);
  System.out.println(fact(n));
  int sum = 0;
  for (int i = 1; i <= n; i++) { sum = sum + i; }
  while (n > 0) { n--; }
  System.out.println(sum);
  System.out.println(n);
  System.out.println(check(7) && false || true);
  System.out.println(false && 1 / 0 == 0);
  System.out.println(true || 1 / 0 == 0);
  System.out.println(-2147483648 / -1);
  System.out.println(args[1]);
  System.out.println(args[1].length());
  System.out.println(args.length);
  String label = "sum=";
  label += sum;
  System.out.println(label);
  System.out.println(12 + "x" + false);
  System.out.println("logic=" + (true && check(7)));
  char letter = 'a';
  letter++;
  System.out.println(letter);
  System.out.println("letter=" + letter);
  int extra = 7;
  extra *= 3;
  extra -= 1;
  System.out.println(extra);
 }
}'''
        giáTrịSửa(máy, 'Calc.java', giáTrịNộiDung)
        máy.lệnh('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        kỳVọng = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        ĐầuRa = máy.lệnh('java Calc 6 guest', ['\r\n' + '\r\n'.join(kỳVọng) + '\r\n', 'Exit: 0'])
        kếtQuả['guest_output'] = ĐầuRa
        danhSáchMục = máy.lệnh('ls', ['Calc.class'])
        cỡ = int(re.search(r'Calc\.class\s+(\d+) bytes', danhSáchMục).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as giáTrịThưMục:
            đườngDẫn = Path(giáTrịThưMục) / 'Calc.class'
            DữLiệu = tệpKhách(máy, 3, cỡ, đườngDẫn)
            dữLiệuThựcTế = subprocess.check_output(['java', '-Xverify:all', '-cp', giáTrịThưMục, 'Calc', '6', 'guest'], universal_newlines=True)
            assert dữLiệuThựcTế.splitlines() == kỳVọng, dữLiệuThựcTế
            kếtQuả['class_sha256'] = hashlib.sha256(DữLiệu).hexdigest()
            kếtQuả['openjdk_output'] = dữLiệuThựcTế
        # 실패한 giáTrịSửa/컴파일은 기존 class를 보존한다.
        giáTrịSửa(máy, 'Calc.java', 'not Java at all', giáTrịCất=False)
        máy.lệnh('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for kếtQuảKhôngHợpLệ in [
            'public class Calc { public static void main(String[] args) { int x = ; } }',
            'public class Calc { public static void main(String[] args) { int x = true; } }',
            'public class Calc { public static void main(String[] args) { int x = 2147483648; } }',
            'public class Calc { public static int f() { int x = 1; } }',
            'public class Calc { public static void main(String[] args) { Object x = new Object(); } }',
            'public class Other { public static void main(String[] args) {} }',
            'public class Calc { public static void main(String[] args) { int while = 3; } }',
            'public class Calc { public static void main(String[] args) { if (true) int x = 3; } }',
            'public class Calc { public static void main(String[] args) { int x = 010; } }',
        ]:
            giáTrịSửa(máy, 'Calc.java', kếtQuảKhôngHợpLệ)
            máy.lệnh('javac Calc.java', ['javac error:', 'Exit: 1'])
            máy.lệnh('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # giáTrịLầnLặp 실행은 NgườiDùng giáTrịVùngNhớĐộng/프레임을 매번 초기화한다.
        for trịSố in range(12):
            máy.lệnh('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        máy.lệnh('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        máy.lệnh('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        giáTrịSửa(máy, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        máy.lệnh('javac Calc.java', ['Compiled:', 'Exit: 0'])
        máy.lệnh('java Calc', ['instruction limit', 'Exit: 1'])
        máy.lệnh('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        giáTrịSửa(máy, 'Bad.class', 'garbage')
        máy.lệnh('java Bad', ['JVM error:', 'Exit: 1'])
        máy.lệnh('rm Bad.class', ['Removed'])
        máy.lệnh('java Bad', ['cannot read class: -2'])
        # giáTrịSửa 입력의 넘친 부분을 잘라서 저장하지 않는다.
        chạy = len(máy.bảnGhiNhậtKý)
        máy.giáTrịNốiTiếp.sendall(b'edit Hello.java\n')
        máy.chờTrạngThái('...> ', chạy)
        chạy = len(máy.bảnGhiNhậtKý)
        máy.giáTrịNốiTiếp.sendall(b'x' * 129 + b'\n')
        máy.chờTrạngThái('...> ', chạy)
        máy.lệnh('.save', ['Too much input; original preserved'])
        máy.lệnh('javac Hello.java', ['Compiled:', 'Exit: 0'])
        giáTrịSửa(máy, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for trịSố in range(3):
            giáTrịSửa(máy, 'f' + str(trịSố), 'occupied')
        máy.lệnh('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        máy.lệnh('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in máy.bảnGhiNhậtKý.decode('utf-8', 'replace')
        kếtQuả['serial'] = máy.bảnGhiNhậtKý.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(giáTrịLoại))
        return kếtQuả
    finally:
        máy.đóng()


def mãChínhYếu(DữLiệu):
    """손상 시험용 main Code의 dữLiệuThựcTế Tệp 오프셋/길이만 읽는다."""
    giáTrịVịTrí = 8
    def đọcNgắnKiểuKhôngDấu():
        nonlocal giáTrịVịTrí
        giáTrị = struct.unpack_from('>H', DữLiệu, giáTrịVịTrí)[0]
        giáTrịVịTrí += 2
        return giáTrị
    def đọcSốNguyênKhôngDấu():
        nonlocal giáTrịVịTrí
        giáTrị = struct.unpack_from('>I', DữLiệu, giáTrịVịTrí)[0]
        giáTrịVịTrí += 4
        return giáTrị
    cácGiáTrịKýTự = {}
    for trịSố in range(1, đọcNgắnKiểuKhôngDấu()):
        giáTrịLoại = DữLiệu[giáTrịVịTrí]
        giáTrịVịTrí += 1
        if giáTrịLoại == 1:
            độDài = đọcNgắnKiểuKhôngDấu()
            cácGiáTrịKýTự[trịSố] = DữLiệu[giáTrịVịTrí:giáTrịVịTrí + độDài]
            giáTrịVịTrí += độDài
        elif giáTrịLoại in (7, 8): giáTrịVịTrí += 2
        elif giáTrịLoại in (3, 9, 10, 12): giáTrịVịTrí += 4
        else: raise AssertionError(giáTrịLoại)
    giáTrịVịTrí += 6
    sốLượngPhầnMục = đọcNgắnKiểuKhôngDấu()
    giáTrịVịTrí += sốLượngPhầnMục * 2
    assert đọcNgắnKiểuKhôngDấu() == 0
    for trịSố in range(đọcNgắnKiểuKhôngDấu()):
        đọcNgắnKiểuKhôngDấu()
        tên = đọcNgắnKiểuKhôngDấu()
        đọcNgắnKiểuKhôngDấu()
        for trịSố in range(đọcNgắnKiểuKhôngDấu()):
            giáTrịThuộcTính = đọcNgắnKiểuKhôngDấu()
            cỡ = đọcSốNguyênKhôngDấu()
            if cácGiáTrịKýTự[tên] == b'main' and cácGiáTrịKýTự[giáTrịThuộcTính] == b'Code':
                return giáTrịVịTrí + 8, struct.unpack_from('>I', DữLiệu, giáTrịVịTrí + 4)[0]
            giáTrịVịTrí += cỡ
    raise AssertionError('main Code missing')


def thửĐangNạp():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as giáTrịTạm:
        giáTrịThưMục = Path(giáTrịTạm)
        (giáTrịThưMục / 'build').mkdir()
        mãNguồn = giáTrịThưMục / 'Imported.java'
        mãNguồn.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(mãNguồn)], check=True)
        nguyênBản = (giáTrịThưMục / 'Imported.class').read_bytes()
        giáTrịMã, độDài = mãChínhYếu(nguyênBản)
        giáTrịBiếnThể = {}
        DữLiệu = bytearray(nguyênBản); DữLiệu[0] = 0; giáTrịBiếnThể['BadMagic'] = DữLiệu
        DữLiệu = bytearray(nguyênBản); DữLiệu[7] = 61; giáTrịBiếnThể['BadVer'] = DữLiệu
        DữLiệu = bytearray(nguyênBản); DữLiệu[8:10] = b'\xff\xff'; giáTrịBiếnThể['BadPool'] = DữLiệu
        DữLiệu = bytearray(nguyênBản); DữLiệu[giáTrịMã:giáTrịMã + độDài] = bytes(độDài)
        DữLiệu[giáTrịMã:giáTrịMã + 3] = b'\xa7\x00\x01'; DữLiệu[giáTrịMã + độDài - 1] = 177; giáTrịBiếnThể['BadJump'] = DữLiệu
        DữLiệu = bytearray(nguyênBản); DữLiệu[giáTrịMã:giáTrịMã + độDài] = bytes(độDài)
        DữLiệu[giáTrịMã] = 87; DữLiệu[giáTrịMã + độDài - 1] = 177; giáTrịBiếnThể['BadStack'] = DữLiệu
        # tên 검사를 통과시켜 dữLiệuThựcTế thựcThiLệnh 중의 ngănXếpToánHạng 오류까지 검사한다.
        giáTrịBiếnThể['BadStack'] = giáTrịBiếnThể['BadStack'].replace(b'Imported', b'BadStack')
        giáTrịMục = ['Imported.class=' + str(giáTrịThưMục / 'Imported.class'), 'Imported.java=' + str(mãNguồn)]
        for tên, DữLiệu in giáTrịBiếnThể.items():
            đườngDẫn = giáTrịThưMục / (tên + '.class'); đườngDẫn.write_bytes(DữLiệu)
            giáTrịMục.append(tên + '.class=' + str(đườngDẫn))
        giáTrịNhóm = giáTrịThưMục / 'build/java-files.bin'
        subprocess.run([sys.executable, str(vịTrí / 'CôngCụ/GóiTệpJava.py'), '-o', str(giáTrịNhóm)] + giáTrịMục, check=True)
        subprocess.run(['as', '--32', '-o', str(giáTrịThưMục / 'user.o'), str(vịTrí / 'KhởiĐộng/NgườiDùng.s')], cwd=str(giáTrịThưMục), check=True)
        giáTrịNhân = giáTrịThưMục / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(vịTrí / 'KhởiĐộng/BốTríLiênKết.ld'), '-o', str(giáTrịNhân),
                        str(vịTrí / 'build/boot.o'), str(vịTrí / 'build/java.o'), str(giáTrịThưMục / 'user.o'), str(vịTrí / 'build/apps.o')], check=True)
        máy = MáyẢo(giáTrịNhân, giáTrịMạng=False)
        try:
            máy.lệnh('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            máy.lệnh('cat Imported.java', ['int[] values = new int[3]'])
            for tên, giáTrịCụmTừ in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                máy.lệnh('java ' + tên, [giáTrịCụmTừ, 'Exit: 1'])
                máy.lệnh('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return máy.bảnGhiNhậtKý.decode('utf-8', 'replace')
        finally:
            máy.đóng()


if __name__ == '__main__':
    phânTíchCúPhápGiáTrị = argparse.ArgumentParser()
    phânTíchCúPhápGiáTrị.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    cácĐốiSố = phânTíchCúPhápGiáTrị.parse_args()
    kếtQuả = {giáTrịLoại: thửChạy(giáTrịLoại) for giáTrịLoại in (('elf', 'iso') if cácĐốiSố.boot == 'both' else (cácĐốiSố.boot,))}
    kếtQuả['import'] = thửĐangNạp()
    (vịTrí / 'build/ThửJava.json').write_text(json.dumps(kếtQuả, ensure_ascii=False, indent=2) + '\n')
