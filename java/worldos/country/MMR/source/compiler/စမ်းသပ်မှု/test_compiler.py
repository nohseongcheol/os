"""တကယ့်ဒေတာ ELF စက်မောင်း + OpenJDK ရလဒ် 대조. ယာယီတန်ဖိုး စမ်းသပ်မှု 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ဘာသာပြန်စက် = Path(__file__).resolve().parents[1] / 'ဘာသာပြန်စက်.py'


class ကိုယ်ပိုင်စမ်းသပ်(unittest.TestCase):
    def setUp(self):
        self.ယာယီတန်ဖိုး = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.ယာယီတန်ဖိုး.cleanup)
        self.ဖိုင်တွဲတန်ဖိုး = Path(self.ယာယီတန်ဖိုး.name)

    def မူရင်းကုဒ်ဘာသာပြန်(self, မူရင်းကုဒ်, အချက်နောက်တွဲ=None, အောင်မြင်မှုတန်ဖိုး=True, ဦးတည်ချက်တန်ဖိုး='linux', ထုတ်ပေးတန်ဖိုး=None):
        လမ်းများ = []
        for အမည်, အကြောင်းအရာတန်ဖိုး in dict({'စမ်းသပ်မှု': မူရင်းကုဒ်}, **(အချက်နောက်တွဲ or {})).items():
            လမ်း = self.ဖိုင်တွဲတန်ဖိုး / (အမည် + '.java')
            လမ်း.write_text(အကြောင်းအရာတန်ဖိုး, encoding='utf-8')
            လမ်းများ.append(str(လမ်း))
        အမိန့် = [sys.executable, str(ဘာသာပြန်စက်), '--target', ဦးတည်ချက်တန်ဖိုး, '--entry', 'စမ်းသပ်မှု.လုပ်ဆောင်', '-o', str(self.ဖိုင်တွဲတန်ဖိုး / 'native')]
        if ထုတ်ပေးတန်ဖိုး is not None: အမိန့် += ['--export', ထုတ်ပေးတန်ဖိုး]
        ရလဒ် = subprocess.run(အမိန့် + လမ်းများ,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if အောင်မြင်မှုတန်ဖိုး:
            self.assertEqual(ရလဒ်.returncode, 0, ရလဒ်.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(ရလဒ်.returncode, 0)
            self.assertIn('မူရင်းကုဒ်ဘာသာပြန် အမှား'.encode(), ရလဒ်.stderr)
        return ရလဒ်

    def လုပ်ဆောင်မှုရလဒ်(self):
        return subprocess.run([str(self.ဖိုင်တွဲတန်ဖိုး / 'native')], timeout=5).returncode

    def 자바대조(self, မူရင်းကုဒ်, အချက်နောက်တွဲ=None):
        self.မူရင်းကုဒ်ဘာသာပြန်(မူရင်းကုဒ်, အချက်နောက်တွဲ)
        (self.ဖိုင်တွဲတန်ဖိုး / 'အိမ်ရှင်.java').write_text(
            'public class အိမ်ရှင် { public static void main(String[] အချက်များ) { System.exit(စမ်းသပ်မှု.လုပ်ဆောင်()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ဖိုင်တွဲတန်ဖိုး)] +
                       [str(လမ်း) for လမ်း in self.ဖိုင်တွဲတန်ဖိုး.glob('*.java')], check=True, timeout=30)
        မျှော်လင့်ချက် = subprocess.run(['java', '-cp', str(self.ဖိုင်တွဲတန်ဖိုး), 'အိမ်ရှင်'], timeout=5).returncode
        တကယ့်ဒေတာ = self.လုပ်ဆောင်မှုရလဒ်()
        self.assertGreaterEqual(တကယ့်ဒေတာ, 0, '신호로 종료됨 (샌드박스의 32비트 syscall ကန့်သတ်ချက်တန်ဖိုး ဟုတ်မဟုတ် အတည်ပြု)')
        self.assertEqual(တကယ့်ဒေတာ, မျှော်လင့်ချက်)

    def test_정수연산과이동(self):
        self.자바대조('''public class စမ်းသပ်မှု {
            static int 섞기(int ပထမတွက်ချက်ခံ, int ဒုတိယတွက်ချက်ခံ) {
                return ((ပထမတွက်ချက်ခံ + ဒုတိယတွက်ချက်ခံ) ^ (ပထမတွက်ချက်ခံ - ဒုတိယတွက်ချက်ခံ) ^ (ပထမတွက်ချက်ခံ * ဒုတိယတွက်ချက်ခံ) ^ (ပထမတွက်ချက်ခံ & ဒုတိယတွက်ချက်ခံ) ^ (ပထမတွက်ချက်ခံ | ဒုတိယတွက်ချက်ခံ))
                    + (ပထမတွက်ချက်ခံ << ဒုတိယတွက်ချက်ခံ) + (ပထမတွက်ချက်ခံ >> ဒုတိယတွက်ချက်ခံ) + (ပထမတွက်ချက်ခံ >>> ဒုတိယတွက်ချက်ခံ);
            }
            public static int လုပ်ဆောင်() {
                int စုစုပေါင်းတန်ဖိုး = 7;
                int တန်ဖိုး = 12345;
                for (int နံပါတ် = -65; နံပါတ် <= 65; နံပါတ်++) {
                    တန်ဖိုး = တန်ဖိုး * 1664525 + 1013904223;
                    စုစုပေါင်းတန်ဖိုး = စုစုပေါင်းတန်ဖိုး * 31 + 섞기(တန်ဖိုး, နံပါတ်);
                    စုစုပေါင်းတန်ဖိုး += (byte)တန်ဖိုး + (short)တန်ဖိုး + (char)တန်ဖိုး;
                }
                return (စုစုပေါင်းတန်ဖိုး & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class စမ်းသပ်မှု {
            static int[] တန်ဖိုး = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int လုပ်ဆောင်() {
                int စုစုပေါင်းတန်ဖိုး = 13;
                for (int ပထမတွက်ချက်ခံ = 0; ပထမတွက်ချက်ခံ < တန်ဖိုး.length; ပထမတွက်ချက်ခံ++)
                    for (int ဒုတိယတွက်ချက်ခံ = 1; ဒုတိယတွက်ချက်ခံ < တန်ဖိုး.length; ဒုတိယတွက်ချက်ခံ++)
                        စုစုပေါင်းတန်ဖိုး = စုစုပေါင်းတန်ဖိုး * 31 + တန်ဖိုး[ပထမတွက်ချက်ခံ] / တန်ဖိုး[ဒုတိယတွက်ချက်ခံ] + တန်ဖိုး[ပထမတွက်ချက်ခံ] % တန်ဖိုး[ဒုတိယတွက်ချက်ခံ];
                return (စုစုပေါင်းတန်ဖိုး & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class စမ်းသပ်မှု {
            static int[] အချက်ဖန်တီး(int အရွယ်) { return new int[အရွယ်]; }
            public static int လုပ်ဆောင်() {
                int[] ပထမတွက်ချက်ခံ = အချက်ဖန်တီး(8); int[] ဒုတိယတွက်ချက်ခံ = ပထမတွက်ချက်ခံ; int[] အလွတ်အရာဝတ္ထု = new int[0];
                if (ပထမတွက်ချက်ခံ != ဒုတိယတွက်ချက်ခံ || ပထမတွက်ချက်ခံ == null || အလွတ်အရာဝတ္ထု.length != 0 || ပထမတွက်ချက်ခံ[7] != 0) return 99;
                int တန်ဖိုး = (ပထမတွက်ချက်ခံ[2] = 40); ပထမတွက်ချက်ခံ[2]++; ++ပထမတွက်ချက်ခံ[3]; ပထမတွက်ချက်ခံ[2] += 7;
                return တန်ဖိုး + ဒုတိယတွက်ချက်ခံ[2] + ဒုတိယတွက်ချက်ခံ[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class စမ်းသပ်မှု {
            static int တန်ဖိုး = 보조.အစဦးတန်ဖိုး();
            static int တွက်ချက်မှု(int ပထမတွက်ချက်ခံ, int ဒုတိယတွက်ချက်ခံ, int တတိယအော်ပရန်း, int စတုတ္ထအော်ပရန်း, int ပဉ္စမအော်ပရန်း) {
                return ပထမတွက်ချက်ခံ + ဒုတိယတွက်ချက်ခံ * 2 + တတိယအော်ပရန်း * 3 + စတုတ္ထအော်ပရန်း * 4 + ပဉ္စမအော်ပရန်း * 5;
            }
            public static int လုပ်ဆောင်() { return တွက်ချက်မှု(1, 2, 3, 4, တန်ဖိုး) + 보조.ဖတ်(); }
        }''', {'보조': '''public class 보조 {
            static int တန်ဖိုး = 3;
            static int အစဦးတန်ဖိုး() { return ++တန်ဖိုး; }
            static int ဖတ်() { return တန်ဖိုး; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class စမ်းသပ်မှု {
            static int တန်ဖိုး = 보조.ဖတ်() + 1;
            public static int လုပ်ဆောင်() { return တန်ဖိုး * 10 + 보조.ဖတ်(); }
        }''', {'보조': '''public class 보조 {
            static int တန်ဖိုး = စမ်းသပ်မှု.တန်ဖိုး + 2;
            static int ဖတ်() { return တန်ဖိုး; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class စမ်းသပ်မှု {
            static String စာသား = "한글\\u0000😀";
            public static int လုပ်ဆောင်() {
                if (စာသား != "한글\\u0000😀") return 99;
                return (စာသား.length() + စာသား.charAt(2) + စာသား.charAt(3) + စာသား.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class စမ်းသပ်မှု {
            static int 계승(int တန်ဖိုး) { return တန်ဖိုး <= 1 ? 1 : တန်ဖိုး * 계승(တန်ဖိုး - 1); }
            static int 연속(int တန်ဖိုး) {
                switch (တန်ဖိုး) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int တန်ဖိုး) {
                switch (တန်ဖိုး) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int လုပ်ဆောင်() { return (계승(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        ကြေညာချက် = '\n'.join('int တန်ဖိုး{} = {};'.format(နံပါတ်, နံပါတ်) for နံပါတ် in range(270))
        덧셈 = '+'.join('တန်ဖိုး{}'.format(နံပါတ်) for နံပါတ် in range(270))
        self.자바대조('public class စမ်းသပ်မှု { public static int လုပ်ဆောင်() {' + ကြေညာချက် +
                    'တန်ဖိုး269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int သုညတွက်ချက်ခံ = 0; return 1 / သုညတွက်ချက်ခံ;', 101),
            ('int[] တန်ဖိုး = null; return တန်ဖိုး.length;', 102),
            ('int[] တန်ဖိုး = new int[1]; return တန်ဖိုး[1];', 103),
            ('int[] တန်ဖိုး = new int[1]; တန်ဖိုး[-1] = 3; return 0;', 103),
            ('int တန်ဖိုး = -1; return new int[တန်ဖိုး].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] ပထမတွက်ချက်ခံ = new int[65535]; return new int[1].length;', 105),
        ]
        for ကိုယ်ထည်တန်ဖိုး, မျှော်လင့်ချက် in 경우들:
            with self.subTest(ကိုယ်ထည်တန်ဖိုး=ကိုယ်ထည်တန်ဖိုး):
                self.မူရင်းကုဒ်ဘာသာပြန်('public class စမ်းသပ်မှု { public static int လုပ်ဆောင်() { ' + ကိုယ်ထည်တန်ဖိုး + ' } }')
                self.assertEqual(self.လုပ်ဆောင်မှုရလဒ်(), မျှော်လင့်ချက်)

    def test_미지원기능거부(self):
        경우들 = [
            'static long တန်ဖိုး; public static int လုပ်ဆောင်() { return 0; }',
            'public static int လုပ်ဆောင်() { Object တန်ဖိုး = new Object(); return 0; }',
            'public static int လုပ်ဆောင်() { System.out.println("hello"); return 0; }',
            'public static int လုပ်ဆောင်() { try { return 1; } catch (Exception အမှား) { return 2; } }',
            'public static synchronized int လုပ်ဆောင်() { return 0; }',
            'public static int လုပ်ဆောင်() { return new byte[3].length; }',
            'static native int ပြင်ပတန်ဖိုး(); public static int လုပ်ဆောင်() { return ပြင်ပတန်ဖိုး(); }',
            'int တန်ဖိုး; public static int လုပ်ဆောင်() { return 0; }',
        ]
        for ကိုယ်ထည်တန်ဖိုး in 경우들:
            with self.subTest(ကိုယ်ထည်တန်ဖိုး=ကိုယ်ထည်တန်ဖိုး):
                self.မူရင်းကုဒ်ဘာသာပြန်('public class စမ်းသပ်မှု { ' + ကိုယ်ထည်တန်ဖိုး + ' }', အောင်မြင်မှုတန်ဖိုး=False)

    def test_실패시기존출력보존(self):
        အထွက် = self.ဖိုင်တွဲတန်ဖိုး / 'native'
        အထွက်.write_bytes(b'original-output')
        self.မူရင်းကုဒ်ဘာသာပြန်('public class စမ်းသပ်မှု { public static int လုပ်ဆောင်() { return missing; } }', အောင်မြင်မှုတန်ဖိုး=False)
        self.assertEqual(အထွက်.read_bytes(), b'original-output')

    def ELFနှင့်သီးခြားလုပ်ဆောင်မှုစမ်းသပ်(self):
        self.မူရင်းကုဒ်ဘာသာပြန်('public class စမ်းသပ်မှု { public static int လုပ်ဆောင်() { return 37; } }')
        self.assertEqual((self.ဖိုင်တွဲတန်ဖိုး / 'native').read_bytes()[:5], b'\x7fELF\x01')
        ဇယား = subprocess.check_output(['readelf', '-l', str(self.ဖိုင်တွဲတန်ဖိုး / 'native')])
        self.assertNotIn(b'INTERP', ဇယား)
        self.assertEqual(self.လုပ်ဆောင်မှုရလဒ်(), 37)

    def test_사용자ELF와ABI분리(self):
        self.မူရင်းကုဒ်ဘာသာပြန်('public class စမ်းသပ်မှု { public static int လုပ်ဆောင်() { return သုံးစွဲသူ.လုပ်ဆောင်မှုခွင့်ပြုချက်(); } }',
                    {'သုံးစွဲသူ': 'public class သုံးစွဲသူ { public static native int လုပ်ဆောင်မှုခွင့်ပြုချက်(); }'}, ဦးတည်ချက်တန်ဖိုး='user')
        ဒေတာ = (self.ဖိုင်တွဲတန်ဖိုး / 'native').read_bytes()
        self.assertEqual(ဒေတာ[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', ဒေတာ, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ဖိုင်တွဲတန်ဖိုး / 'native')]))
        # သုံးစွဲသူ ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.မူရင်းကုဒ်ဘာသာပြန်('public class စမ်းသပ်မှု { public static int လုပ်ဆောင်() { return ကိရိယာ.စက်ပစ္စည်းဆက်သွယ်ပေါက်ဖတ်(1); } }',
                    {'ကိရိယာ': 'public class ကိရိယာ { public static native int စက်ပစ္စည်းဆက်သွယ်ပေါက်ဖတ်(int တန်ဖိုး); }'}, အောင်မြင်မှုတန်ဖိုး=False, ဦးတည်ချက်တန်ဖိုး='user')

    def test_내보내기검증(self):
        မူရင်းကုဒ် = 'public class စမ်းသပ်မှု { public static int လုပ်ဆောင်() { return 0; } static int ခေါ်လုပ်(int တန်ဖိုး) { return တန်ဖိုး; } }'
        self.မူရင်းကုဒ်ဘာသာပြန်(မူရင်းကုဒ်, ဦးတည်ချက်တန်ဖိုး='kernel', ထုတ်ပေးတန်ဖိုး='kernel_dispatch=စမ်းသပ်မှု.ခေါ်လုပ်')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ဖိုင်တွဲတန်ဖိုး / 'native')]))
        self.မူရင်းကုဒ်ဘာသာပြန်(မူရင်းကုဒ်, အောင်မြင်မှုတန်ဖိုး=False, ထုတ်ပေးတန်ဖိုး='bad;name=စမ်းသပ်မှု.ခေါ်လုပ်')
        self.မူရင်းကုဒ်ဘာသာပြန်(မူရင်းကုဒ်, အောင်မြင်မှုတန်ဖိုး=False, ထုတ်ပေးတန်ဖိုး='missing=စမ်းသပ်မှု.없음')


if __name__ == '__main__':
    unittest.main()
