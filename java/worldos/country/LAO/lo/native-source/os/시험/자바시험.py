#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ, ຫຼົ້ມເຫຼວ_ຄ່າ/ແຫຼ່ງ_ຄ່າ 경계 시험."""
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
from 사용자통신시험 import ຈໍາລອງ_ເຄື່ອງຈັກ, ຈັດຕໍາແຫນ່ງ


def ແກ້ໄຂ_ຄ່າ(ເຄື່ອງຈັກ, ຊື່, ເນື້ອໃນ_ຄ່າ_cb0f2404, ຮ້ານຄ້າ_ຄ່າ=True):
    ແລ່ນ = len(ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ)
    ເຄື່ອງຈັກ.직렬.sendall(('edit ' + ຊື່ + '\n').encode())
    ເຄື່ອງຈັກ.ລໍຖ້າ_ສະຖານະ('...> ', ແລ່ນ)
    for ສາຍ in ເນື້ອໃນ_ຄ່າ_cb0f2404.splitlines():
        assert len(ສາຍ) <= 128
        ແລ່ນ = len(ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ)
        ເຄື່ອງຈັກ.직렬.sendall((ສາຍ + '\n').encode())
        ເຄື່ອງຈັກ.ລໍຖ້າ_ສະຖານະ('...> ', ແລ່ນ)
    ແລ່ນ = len(ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ)
    ເຄື່ອງຈັກ.직렬.sendall(b'.save\n' if ຮ້ານຄ້າ_ຄ່າ else b'.cancel\n')
    ມາດຕະການ = ເຄື່ອງຈັກ.ລໍຖ້າ_ສະຖານະ('jkoros> ', ແລ່ນ)
    assert ('Saved:' if ຮ້ານຄ້າ_ຄ່າ else 'Cancelled; original preserved') in ມາດຕະການ, ມາດຕະການ


def ຟາຍ_ອີເມວ():
    ມາດຕະການ = subprocess.check_output(['nm', '-n', str(ຈັດຕໍາແຫນ່ງ / 'build/kernel.elf')], universal_newlines=True)
    for ສາຍ in ມາດຕະການ.splitlines():
        if ສາຍ.endswith(' ram_files'):
            return int(ສາຍ.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def ແຂກ_ຟາຍ(ເຄື່ອງຈັກ, ຊ່ອງ_ຄ່າ, ຂະ_ຫນາດ, ທາງໂຄຈອນ):
    # 시험 VM의 메모리에서 ຕົວ_ຈິງ_ຂໍ້ມູນ 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ອີເມວ = ຟາຍ_ອີເມວ() + ຊ່ອງ_ຄ່າ * 16384
    ເຄື່ອງຈັກ.ຫນ້າຈໍ_ຄ່າ.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ອີເມວ, ຂະ_ຫນາດ, ທາງໂຄຈອນ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ທາງໂຄຈອນ.exists() and ທາງໂຄຈອນ.stat().st_size == ຂະ_ຫນາດ:
            return ທາງໂຄຈອນ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    ເຄື່ອງຈັກ = ຈໍາລອງ_ເຄື່ອງຈັກ(ຈັດຕໍາແຫນ່ງ / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, ເຄືອຂ່າຍ_ຄ່າ=False)
    ມາດຕະການ = {}
    try:
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java Missing', ['cannot read class: -2', 'Exit: 1'])
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        ເນື້ອໃນ_ຄ່າ_cb0f2404 = '''public class Calc {
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
        ແກ້ໄຂ_ຄ່າ(ເຄື່ອງຈັກ, 'Calc.java', ເນື້ອໃນ_ຄ່າ_cb0f2404)
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        ມາດຕະການ['guest_output'] = 출력
        ເຂົ້າໃນ_ລາຍຊື່ = ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('ls', ['Calc.class'])
        ຂະ_ຫນາດ = int(re.search(r'Calc\.class\s+(\d+) bytes', ເຂົ້າໃນ_ລາຍຊື່).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ກຸ່ມຂໍ້ມູນ_ຄ່າ:
            ທາງໂຄຈອນ = Path(ກຸ່ມຂໍ້ມູນ_ຄ່າ) / 'Calc.class'
            ຂໍ້ມູນ = ແຂກ_ຟາຍ(ເຄື່ອງຈັກ, 3, ຂະ_ຫນາດ, ທາງໂຄຈອນ)
            ຕົວ_ຈິງ_ຂໍ້ມູນ = subprocess.check_output(['java', '-Xverify:all', '-cp', ກຸ່ມຂໍ້ມູນ_ຄ່າ, 'Calc', '6', 'guest'], universal_newlines=True)
            assert ຕົວ_ຈິງ_ຂໍ້ມູນ.splitlines() == 기대, ຕົວ_ຈິງ_ຂໍ້ມູນ
            ມາດຕະການ['class_sha256'] = hashlib.sha256(ຂໍ້ມູນ).hexdigest()
            ມາດຕະການ['openjdk_output'] = ຕົວ_ຈິງ_ຂໍ້ມູນ
        # 실패한 ແກ້ໄຂ_ຄ່າ/컴파일은 기존 class를 보존한다.
        ແກ້ໄຂ_ຄ່າ(ເຄື່ອງຈັກ, 'Calc.java', 'not Java at all', ຮ້ານຄ້າ_ຄ່າ=False)
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for ໃຊ້ບໍ່ໄດ້_ມາດຕະການ in [
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
            ແກ້ໄຂ_ຄ່າ(ເຄື່ອງຈັກ, 'Calc.java', ໃຊ້ບໍ່ໄດ້_ມາດຕະການ)
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('javac Calc.java', ['javac error:', 'Exit: 1'])
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # ສະປຣິນ_ຄ່າ 실행은 ຜູ້ໃຊ້ 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        ແກ້ໄຂ_ຄ່າ(ເຄື່ອງຈັກ, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('javac Calc.java', ['Compiled:', 'Exit: 0'])
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java Calc', ['instruction limit', 'Exit: 1'])
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        ແກ້ໄຂ_ຄ່າ(ເຄື່ອງຈັກ, 'Bad.class', 'garbage')
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java Bad', ['JVM error:', 'Exit: 1'])
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('rm Bad.class', ['Removed'])
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java Bad', ['cannot read class: -2'])
        # ແກ້ໄຂ_ຄ່າ 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ແລ່ນ = len(ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ)
        ເຄື່ອງຈັກ.직렬.sendall(b'edit Hello.java\n')
        ເຄື່ອງຈັກ.ລໍຖ້າ_ສະຖານະ('...> ', ແລ່ນ)
        ແລ່ນ = len(ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ)
        ເຄື່ອງຈັກ.직렬.sendall(b'x' * 129 + b'\n')
        ເຄື່ອງຈັກ.ລໍຖ້າ_ສະຖານະ('...> ', ແລ່ນ)
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('.save', ['Too much input; original preserved'])
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('javac Hello.java', ['Compiled:', 'Exit: 0'])
        ແກ້ໄຂ_ຄ່າ(ເຄື່ອງຈັກ, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            ແກ້ໄຂ_ຄ່າ(ເຄື່ອງຈັກ, 'f' + str(수), 'occupied')
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ.decode('utf-8', 'replace')
        ມາດຕະການ['serial'] = ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return ມາດຕະການ
    finally:
        ເຄື່ອງຈັກ.ປິດ()


def 주코드(ຂໍ້ມູນ):
    """손상 시험용 main Code의 ຕົວ_ຈິງ_ຂໍ້ມູນ ຟາຍ 오프셋/길이만 읽는다."""
    ຈັດຕໍາແຫນ່ງ_ຄ່າ = 8
    def 짧():
        nonlocal ຈັດຕໍາແຫນ່ງ_ຄ່າ
        ຄ່າ = struct.unpack_from('>H', ຂໍ້ມູນ, ຈັດຕໍາແຫນ່ງ_ຄ່າ)[0]
        ຈັດຕໍາແຫນ່ງ_ຄ່າ += 2
        return ຄ່າ
    def 정():
        nonlocal ຈັດຕໍາແຫນ່ງ_ຄ່າ
        ຄ່າ = struct.unpack_from('>I', ຂໍ້ມູນ, ຈັດຕໍາແຫນ່ງ_ຄ່າ)[0]
        ຈັດຕໍາແຫນ່ງ_ຄ່າ += 4
        return ຄ່າ
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = ຂໍ້ມູນ[ຈັດຕໍາແຫນ່ງ_ຄ່າ]
        ຈັດຕໍາແຫນ່ງ_ຄ່າ += 1
        if 종류 == 1:
            ຄວາມຍາວ_ຄ່າ = 짧()
            문자들[수] = ຂໍ້ມູນ[ຈັດຕໍາແຫນ່ງ_ຄ່າ:ຈັດຕໍາແຫນ່ງ_ຄ່າ + ຄວາມຍາວ_ຄ່າ]
            ຈັດຕໍາແຫນ່ງ_ຄ່າ += ຄວາມຍາວ_ຄ່າ
        elif 종류 in (7, 8): ຈັດຕໍາແຫນ່ງ_ຄ່າ += 2
        elif 종류 in (3, 9, 10, 12): ຈັດຕໍາແຫນ່ງ_ຄ່າ += 4
        else: raise AssertionError(종류)
    ຈັດຕໍາແຫນ່ງ_ຄ່າ += 6
    개수 = 짧()
    ຈັດຕໍາແຫນ່ງ_ຄ່າ += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        ຊື່ = 짧()
        짧()
        for 수 in range(짧()):
            ຄຸນສົມບັດ_ຄ່າ = 짧()
            ຂະ_ຫນາດ = 정()
            if 문자들[ຊື່] == b'main' and 문자들[ຄຸນສົມບັດ_ຄ່າ] == b'Code':
                return ຈັດຕໍາແຫນ່ງ_ຄ່າ + 8, struct.unpack_from('>I', ຂໍ້ມູນ, ຈັດຕໍາແຫນ່ງ_ຄ່າ + 4)[0]
            ຈັດຕໍາແຫນ່ງ_ຄ່າ += ຂະ_ຫນາດ
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ກຸ່ມຂໍ້ມູນ_ຄ່າ = Path(임시)
        (ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'build').mkdir()
        ແຫຼ່ງທີ່ມາ = ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'Imported.java'
        ແຫຼ່ງທີ່ມາ.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ແຫຼ່ງທີ່ມາ)], check=True)
        원본 = (ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'Imported.class').read_bytes()
        ລະຫັດ_ຄ່າ, ຄວາມຍາວ_ຄ່າ = 주코드(원본)
        변형 = {}
        ຂໍ້ມູນ = bytearray(원본); ຂໍ້ມູນ[0] = 0; 변형['BadMagic'] = ຂໍ້ມູນ
        ຂໍ້ມູນ = bytearray(원본); ຂໍ້ມູນ[7] = 61; 변형['BadVer'] = ຂໍ້ມູນ
        ຂໍ້ມູນ = bytearray(원본); ຂໍ້ມູນ[8:10] = b'\xff\xff'; 변형['BadPool'] = ຂໍ້ມູນ
        ຂໍ້ມູນ = bytearray(원본); ຂໍ້ມູນ[ລະຫັດ_ຄ່າ:ລະຫັດ_ຄ່າ + ຄວາມຍາວ_ຄ່າ] = bytes(ຄວາມຍາວ_ຄ່າ)
        ຂໍ້ມູນ[ລະຫັດ_ຄ່າ:ລະຫັດ_ຄ່າ + 3] = b'\xa7\x00\x01'; ຂໍ້ມູນ[ລະຫັດ_ຄ່າ + ຄວາມຍາວ_ຄ່າ - 1] = 177; 변형['BadJump'] = ຂໍ້ມູນ
        ຂໍ້ມູນ = bytearray(원본); ຂໍ້ມູນ[ລະຫັດ_ຄ່າ:ລະຫັດ_ຄ່າ + ຄວາມຍາວ_ຄ່າ] = bytes(ຄວາມຍາວ_ຄ່າ)
        ຂໍ້ມູນ[ລະຫັດ_ຄ່າ] = 87; ຂໍ້ມູນ[ລະຫັດ_ຄ່າ + ຄວາມຍາວ_ຄ່າ - 1] = 177; 변형['BadStack'] = ຂໍ້ມູນ
        # ຊື່ 검사를 통과시켜 ຕົວ_ຈິງ_ຂໍ້ມູນ ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ເຂົ້າໃນ_ຄ່າ = ['Imported.class=' + str(ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'Imported.class'), 'Imported.java=' + str(ແຫຼ່ງທີ່ມາ)]
        for ຊື່, ຂໍ້ມູນ in 변형.items():
            ທາງໂຄຈອນ = ກຸ່ມຂໍ້ມູນ_ຄ່າ / (ຊື່ + '.class'); ທາງໂຄຈອນ.write_bytes(ຂໍ້ມູນ)
            ເຂົ້າໃນ_ຄ່າ.append(ຊື່ + '.class=' + str(ທາງໂຄຈອນ))
        ກຸ່ມ_ຄ່າ = ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'build/java-files.bin'
        subprocess.run([sys.executable, str(ຈັດຕໍາແຫນ່ງ / 'ເຄື່ອງມື/자바파일묶기.py'), '-o', str(ກຸ່ມ_ຄ່າ)] + ເຂົ້າໃນ_ຄ່າ, check=True)
        subprocess.run(['as', '--32', '-o', str(ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'user.o'), str(ຈັດຕໍາແຫນ່ງ / '부팅/ຜູ້ໃຊ້.s')], cwd=str(ກຸ່ມຂໍ້ມູນ_ຄ່າ), check=True)
        ແກນກາງ_ຄ່າ = ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ຈັດຕໍາແຫນ່ງ / '부팅/ລິ້ງ_ຮູບແບບ.ld'), '-o', str(ແກນກາງ_ຄ່າ),
                        str(ຈັດຕໍາແຫນ່ງ / 'build/boot.o'), str(ຈັດຕໍາແຫນ່ງ / 'build/java.o'), str(ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'user.o'), str(ຈັດຕໍາແຫນ່ງ / 'build/apps.o')], check=True)
        ເຄື່ອງຈັກ = ຈໍາລອງ_ເຄື່ອງຈັກ(ແກນກາງ_ຄ່າ, ເຄືອຂ່າຍ_ຄ່າ=False)
        try:
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('cat Imported.java', ['int[] values = new int[3]'])
            for ຊື່, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java ' + ຊື່, [문구, 'Exit: 1'])
                ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ.decode('utf-8', 'replace')
        finally:
            ເຄື່ອງຈັກ.ປິດ()


if __name__ == '__main__':
    ການແຈກຄໍາສັບ_ຄ່າ = argparse.ArgumentParser()
    ການແຈກຄໍາສັບ_ຄ່າ.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = ການແຈກຄໍາສັບ_ຄ່າ.parse_args()
    ມາດຕະການ = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    ມາດຕະການ['import'] = 적재시험()
    (ຈັດຕໍາແຫນ່ງ / 'build/자바시험.json').write_text(json.dumps(ມາດຕະການ, ensure_ascii=False, indent=2) + '\n')
