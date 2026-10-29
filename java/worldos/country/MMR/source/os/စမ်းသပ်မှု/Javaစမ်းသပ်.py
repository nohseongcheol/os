#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 စက်မောင်း, မအောင်မြင်မှု/အရင်းအမြစ်တန်ဖိုး နယ်နိမိတ်တန်ဖိုး စမ်းသပ်မှု."""
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
from သုံးစွဲဆက်သွယ်စမ်းသပ် import စက်တု, နေရာ


def တည်းဖြတ်တန်ဖိုး(စက်, အမည်, အကြောင်းအရာတန်ဖိုး, သိုလှောင်တန်ဖိုး=True):
    လုပ်ဆောင် = len(စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု)
    စက်.အစဉ်ဆက်တန်ဖိုး.sendall(('edit ' + အမည် + '\n').encode())
    စက်.အခြေအနေစောင့်('...> ', လုပ်ဆောင်)
    for စာကြောင်း in အကြောင်းအရာတန်ဖိုး.splitlines():
        assert len(စာကြောင်း) <= 128
        လုပ်ဆောင် = len(စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု)
        စက်.အစဉ်ဆက်တန်ဖိုး.sendall((စာကြောင်း + '\n').encode())
        စက်.အခြေအနေစောင့်('...> ', လုပ်ဆောင်)
    လုပ်ဆောင် = len(စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု)
    စက်.အစဉ်ဆက်တန်ဖိုး.sendall(b'.save\n' if သိုလှောင်တန်ဖိုး else b'.cancel\n')
    ရလဒ် = စက်.အခြေအနေစောင့်('jkoros> ', လုပ်ဆောင်)
    assert ('Saved:' if သိုလှောင်တန်ဖိုး else 'Cancelled; original preserved') in ရလဒ်, ရလဒ်


def ဖိုင်လိပ်စာ():
    ရလဒ် = subprocess.check_output(['nm', '-n', str(နေရာ / 'build/kernel.elf')], universal_newlines=True)
    for စာကြောင်း in ရလဒ်.splitlines():
        if စာကြောင်း.endswith(' ram_files'):
            return int(စာကြောင်း.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def ဧည့်သည်ဖိုင်(စက်, နေရာကွက်တန်ဖိုး, အရွယ်, လမ်း):
    # စမ်းသပ်မှု VM의 메모리에서 တကယ့်ဒေတာ 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    လိပ်စာ = ဖိုင်လိပ်စာ() + နေရာကွက်တန်ဖိုး * 16384
    စက်.ကြီးကြပ်သူတန်ဖိုး.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(လိပ်စာ, အရွယ်, လမ်း)).encode())
    အဆုံး = time.monotonic() + 5
    while time.monotonic() < အဆုံး:
        if လမ်း.exists() and လမ်း.stat().st_size == အရွယ်:
            return လမ်း.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def စက်မောင်းစမ်းသပ်(အမျိုးအစားတန်ဖိုး):
    စက် = စက်တု(နေရာ / ('build/kernel.elf' if အမျိုးအစားတန်ဖိုး == 'elf' else 'build/kernel.iso'), အမျိုးအစားတန်ဖိုး, ကွန်ရက်တန်ဖိုး=False)
    ရလဒ် = {}
    try:
        စက်.အမိန့်('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        စက်.အမိန့်('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        စက်.အမိန့်('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        စက်.အမိန့်('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        စက်.အမိန့်('java Missing', ['cannot read class: -2', 'Exit: 1'])
        စက်.အမိန့်('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        စက်.အမိန့်('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        အကြောင်းအရာတန်ဖိုး = '''public class Calc {
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
        တည်းဖြတ်တန်ဖိုး(စက်, 'Calc.java', အကြောင်းအရာတန်ဖိုး)
        စက်.အမိန့်('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        မျှော်လင့်ချက် = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        အထွက် = စက်.အမိန့်('java Calc 6 guest', ['\r\n' + '\r\n'.join(မျှော်လင့်ချက်) + '\r\n', 'Exit: 0'])
        ရလဒ်['guest_output'] = အထွက်
        အချက်စာရင်း = စက်.အမိန့်('ls', ['Calc.class'])
        အရွယ် = int(re.search(r'Calc\.class\s+(\d+) bytes', အချက်စာရင်း).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ဖိုင်တွဲတန်ဖိုး:
            လမ်း = Path(ဖိုင်တွဲတန်ဖိုး) / 'Calc.class'
            ဒေတာ = ဧည့်သည်ဖိုင်(စက်, 3, အရွယ်, လမ်း)
            တကယ့်ဒေတာ = subprocess.check_output(['java', '-Xverify:all', '-cp', ဖိုင်တွဲတန်ဖိုး, 'Calc', '6', 'guest'], universal_newlines=True)
            assert တကယ့်ဒေတာ.splitlines() == မျှော်လင့်ချက်, တကယ့်ဒေတာ
            ရလဒ်['class_sha256'] = hashlib.sha256(ဒေတာ).hexdigest()
            ရလဒ်['openjdk_output'] = တကယ့်ဒေတာ
        # 실패한 တည်းဖြတ်တန်ဖိုး/컴파일은 기존 class를 보존한다.
        တည်းဖြတ်တန်ဖိုး(စက်, 'Calc.java', 'not Java at all', သိုလှောင်တန်ဖိုး=False)
        စက်.အမိန့်('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for မမှန်ကန်ရလဒ် in [
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
            တည်းဖြတ်တန်ဖိုး(စက်, 'Calc.java', မမှန်ကန်ရလဒ်)
            စက်.အမိန့်('javac Calc.java', ['javac error:', 'Exit: 1'])
            စက်.အမိန့်('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # 반복 실행은 သုံးစွဲသူ ပုံတင်မှတ်ဉာဏ်တန်ဖိုး/프레임을 매번 초기화한다.
        for ကိန်းတန်ဖိုး in range(12):
            စက်.အမိန့်('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        စက်.အမိန့်('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        စက်.အမိန့်('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        တည်းဖြတ်တန်ဖိုး(စက်, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        စက်.အမိန့်('javac Calc.java', ['Compiled:', 'Exit: 0'])
        စက်.အမိန့်('java Calc', ['instruction limit', 'Exit: 1'])
        စက်.အမိန့်('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        တည်းဖြတ်တန်ဖိုး(စက်, 'Bad.class', 'garbage')
        စက်.အမိန့်('java Bad', ['JVM error:', 'Exit: 1'])
        စက်.အမိန့်('rm Bad.class', ['Removed'])
        စက်.အမိန့်('java Bad', ['cannot read class: -2'])
        # တည်းဖြတ်တန်ဖိုး 입력의 넘친 부분을 잘라서 저장하지 않는다.
        လုပ်ဆောင် = len(စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု)
        စက်.အစဉ်ဆက်တန်ဖိုး.sendall(b'edit Hello.java\n')
        စက်.အခြေအနေစောင့်('...> ', လုပ်ဆောင်)
        လုပ်ဆောင် = len(စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု)
        စက်.အစဉ်ဆက်တန်ဖိုး.sendall(b'x' * 129 + b'\n')
        စက်.အခြေအနေစောင့်('...> ', လုပ်ဆောင်)
        စက်.အမိန့်('.save', ['Too much input; original preserved'])
        စက်.အမိန့်('javac Hello.java', ['Compiled:', 'Exit: 0'])
        တည်းဖြတ်တန်ဖိုး(စက်, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for ကိန်းတန်ဖိုး in range(3):
            တည်းဖြတ်တန်ဖိုး(စက်, 'f' + str(ကိန်းတန်ဖိုး), 'occupied')
        စက်.အမိန့်('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        စက်.အမိန့်('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု.decode('utf-8', 'replace')
        ရလဒ်['serial'] = စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(အမျိုးအစားတန်ဖိုး))
        return ရလဒ်
    finally:
        စက်.ပိတ်()


def 주코드(ဒေတာ):
    """손상 시험용 main Code의 တကယ့်ဒေတာ ဖိုင် 오프셋/길이만 읽는다."""
    နေရာတန်ဖိုး = 8
    def လက္ခဏာမပါတိုဖတ်():
        nonlocal နေရာတန်ဖိုး
        တန်ဖိုး = struct.unpack_from('>H', ဒေတာ, နေရာတန်ဖိုး)[0]
        နေရာတန်ဖိုး += 2
        return တန်ဖိုး
    def လက္ခဏာမပါကိန်းပြည့်ဖတ်():
        nonlocal နေရာတန်ဖိုး
        တန်ဖိုး = struct.unpack_from('>I', ဒေတာ, နေရာတန်ဖိုး)[0]
        နေရာတန်ဖိုး += 4
        return တန်ဖိုး
    အက္ခရာတန်ဖိုးများ = {}
    for ကိန်းတန်ဖိုး in range(1, လက္ခဏာမပါတိုဖတ်()):
        အမျိုးအစားတန်ဖိုး = ဒေတာ[နေရာတန်ဖိုး]
        နေရာတန်ဖိုး += 1
        if အမျိုးအစားတန်ဖိုး == 1:
            အလျား = လက္ခဏာမပါတိုဖတ်()
            အက္ခရာတန်ဖိုးများ[ကိန်းတန်ဖိုး] = ဒေတာ[နေရာတန်ဖိုး:နေရာတန်ဖိုး + အလျား]
            နေရာတန်ဖိုး += အလျား
        elif အမျိုးအစားတန်ဖိုး in (7, 8): နေရာတန်ဖိုး += 2
        elif အမျိုးအစားတန်ဖိုး in (3, 9, 10, 12): နေရာတန်ဖိုး += 4
        else: raise AssertionError(အမျိုးအစားတန်ဖိုး)
    နေရာတန်ဖိုး += 6
    အရေအတွက် = လက္ခဏာမပါတိုဖတ်()
    နေရာတန်ဖိုး += အရေအတွက် * 2
    assert လက္ခဏာမပါတိုဖတ်() == 0
    for ကိန်းတန်ဖိုး in range(လက္ခဏာမပါတိုဖတ်()):
        လက္ခဏာမပါတိုဖတ်()
        အမည် = လက္ခဏာမပါတိုဖတ်()
        လက္ခဏာမပါတိုဖတ်()
        for ကိန်းတန်ဖိုး in range(လက္ခဏာမပါတိုဖတ်()):
            ဂုဏ်သတ္တိတန်ဖိုး = လက္ခဏာမပါတိုဖတ်()
            အရွယ် = လက္ခဏာမပါကိန်းပြည့်ဖတ်()
            if အက္ခရာတန်ဖိုးများ[အမည်] == b'main' and အက္ခရာတန်ဖိုးများ[ဂုဏ်သတ္တိတန်ဖိုး] == b'Code':
                return နေရာတန်ဖိုး + 8, struct.unpack_from('>I', ဒေတာ, နေရာတန်ဖိုး + 4)[0]
            နေရာတန်ဖိုး += အရွယ်
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as ယာယီတန်ဖိုး:
        ဖိုင်တွဲတန်ဖိုး = Path(ယာယီတန်ဖိုး)
        (ဖိုင်တွဲတန်ဖိုး / 'build').mkdir()
        မူရင်းကုဒ် = ဖိုင်တွဲတန်ဖိုး / 'Imported.java'
        မူရင်းကုဒ်.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(မူရင်းကုဒ်)], check=True)
        မူရင်း = (ဖိုင်တွဲတန်ဖိုး / 'Imported.class').read_bytes()
        ကုဒ်တန်ဖိုး, အလျား = 주코드(မူရင်း)
        변형 = {}
        ဒေတာ = bytearray(မူရင်း); ဒေတာ[0] = 0; 변형['BadMagic'] = ဒေတာ
        ဒေတာ = bytearray(မူရင်း); ဒေတာ[7] = 61; 변형['BadVer'] = ဒေတာ
        ဒေတာ = bytearray(မူရင်း); ဒေတာ[8:10] = b'\xff\xff'; 변형['BadPool'] = ဒေတာ
        ဒေတာ = bytearray(မူရင်း); ဒေတာ[ကုဒ်တန်ဖိုး:ကုဒ်တန်ဖိုး + အလျား] = bytes(အလျား)
        ဒေတာ[ကုဒ်တန်ဖိုး:ကုဒ်တန်ဖိုး + 3] = b'\xa7\x00\x01'; ဒေတာ[ကုဒ်တန်ဖိုး + အလျား - 1] = 177; 변형['BadJump'] = ဒေတာ
        ဒေတာ = bytearray(မူရင်း); ဒေတာ[ကုဒ်တန်ဖိုး:ကုဒ်တန်ဖိုး + အလျား] = bytes(အလျား)
        ဒေတာ[ကုဒ်တန်ဖိုး] = 87; ဒေတာ[ကုဒ်တန်ဖိုး + အလျား - 1] = 177; 변형['BadStack'] = ဒေတာ
        # အမည် 검사를 통과시켜 တကယ့်ဒေတာ စက်မောင်း 중의 တွက်ချက်ခံထပ်ဆင့်အစု 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        အချက်တန်ဖိုး = ['Imported.class=' + str(ဖိုင်တွဲတန်ဖိုး / 'Imported.class'), 'Imported.java=' + str(မူရင်းကုဒ်)]
        for အမည်, ဒေတာ in 변형.items():
            လမ်း = ဖိုင်တွဲတန်ဖိုး / (အမည် + '.class'); လမ်း.write_bytes(ဒေတာ)
            အချက်တန်ဖိုး.append(အမည် + '.class=' + str(လမ်း))
        အုပ်စုတန်ဖိုး = ဖိုင်တွဲတန်ဖိုး / 'build/java-files.bin'
        subprocess.run([sys.executable, str(နေရာ / 'ကိရိယာစု/Javaဖိုင်ထုပ်ပိုး.py'), '-o', str(အုပ်စုတန်ဖိုး)] + အချက်တန်ဖိုး, check=True)
        subprocess.run(['as', '--32', '-o', str(ဖိုင်တွဲတန်ဖိုး / 'user.o'), str(နေရာ / 'စက်တင်/သုံးစွဲသူ.s')], cwd=str(ဖိုင်တွဲတန်ဖိုး), check=True)
        အူတိုင်တန်ဖိုး = ဖိုင်တွဲတန်ဖိုး / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(နေရာ / 'စက်တင်/နေရာချထားပုံ.ld'), '-o', str(အူတိုင်တန်ဖိုး),
                        str(နေရာ / 'build/boot.o'), str(နေရာ / 'build/java.o'), str(ဖိုင်တွဲတန်ဖိုး / 'user.o'), str(နေရာ / 'build/apps.o')], check=True)
        စက် = စက်တု(အူတိုင်တန်ဖိုး, ကွန်ရက်တန်ဖိုး=False)
        try:
            စက်.အမိန့်('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            စက်.အမိန့်('cat Imported.java', ['int[] values = new int[3]'])
            for အမည်, စကားစု in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                စက်.အမိန့်('java ' + အမည်, [စကားစု, 'Exit: 1'])
                စက်.အမိန့်('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု.decode('utf-8', 'replace')
        finally:
            စက်.ပိတ်()


if __name__ == '__main__':
    တန်ဖိုးသဒ္ဒါခွဲခြမ်း = argparse.ArgumentParser()
    တန်ဖိုးသဒ္ဒါခွဲခြမ်း.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    အချက်များ = တန်ဖိုးသဒ္ဒါခွဲခြမ်း.parse_args()
    ရလဒ် = {အမျိုးအစားတန်ဖိုး: စက်မောင်းစမ်းသပ်(အမျိုးအစားတန်ဖိုး) for အမျိုးအစားတန်ဖိုး in (('elf', 'iso') if အချက်များ.boot == 'both' else (အချက်များ.boot,))}
    ရလဒ်['import'] = 적재시험()
    (နေရာ / 'build/Javaစမ်းသပ်.json').write_text(json.dumps(ရလဒ်, ensure_ascii=False, indent=2) + '\n')
