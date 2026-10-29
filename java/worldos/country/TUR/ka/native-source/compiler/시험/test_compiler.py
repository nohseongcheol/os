"""რეალური_მონაცემები ELF შესრულება_ბრძანება + OpenJDK გაზომვა 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

컴파일러 = Path(__file__).resolve().parents[1] / '컴파일러.py'


class 네이티브시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.საქაღალდე_მნიშვნელობა = Path(self.임시.name)

    def აწყობა_წყარო(self, წყარო, 추가=None, 성공=True, მიზანი='linux', 내보냄=None):
        მდებარეობა_სია = []
        for სახელი, შიგთავსი_მნიშვნელობა in dict({'시험': წყარო}, **(추가 or {})).items():
            გეზი = self.საქაღალდე_მნიშვნელობა / (სახელი + '.java')
            გეზი.write_text(შიგთავსი_მნიშვნელობა, encoding='utf-8')
            მდებარეობა_სია.append(str(გეზი))
        ბრძანება = [sys.executable, str(컴파일러), '--target', მიზანი, '--entry', '시험.გაშვება', '-o', str(self.საქაღალდე_მნიშვნელობა / 'native')]
        if 내보냄 is not None: ბრძანება += ['--export', 내보냄]
        გაზომვა = subprocess.run(ბრძანება + მდებარეობა_სია,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(გაზომვა.returncode, 0, გაზომვა.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(გაზომვა.returncode, 0)
            self.assertIn('აწყობა_წყარო შეცდომა'.encode(), გაზომვა.stderr)
        return გაზომვა

    def 실행결과(self):
        return subprocess.run([str(self.საქაღალდე_მნიშვნელობა / 'native')], timeout=5).returncode

    def 자바대조(self, წყარო, 추가=None):
        self.აწყობა_წყარო(წყარო, 추가)
        (self.საქაღალდე_მნიშვნელობა / 'მასპინძელი.java').write_text(
            'public class მასპინძელი { public static void main(String[] 인수) { System.exit(시험.გაშვება()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.საქაღალდე_მნიშვნელობა)] +
                       [str(გეზი) for გეზი in self.საქაღალდე_მნიშვნელობა.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.საქაღალდე_მნიშვნელობა), 'მასპინძელი'], timeout=5).returncode
        რეალური_მონაცემები = self.실행결과()
        self.assertGreaterEqual(რეალური_მონაცემები, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 გადამოწმება)')
        self.assertEqual(რეალური_მონაცემები, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int გაშვება() {
                int 합 = 7;
                int მნიშვნელობა = 12345;
                for (int ინდექსი = -65; ინდექსი <= 65; ინდექსი++) {
                    მნიშვნელობა = მნიშვნელობა * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(მნიშვნელობა, ინდექსი);
                    합 += (byte)მნიშვნელობა + (short)მნიშვნელობა + (char)მნიშვნელობა;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] მნიშვნელობა = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int გაშვება() {
                int 합 = 13;
                for (int 가 = 0; 가 < მნიშვნელობა.length; 가++)
                    for (int 나 = 1; 나 < მნიშვნელობა.length; 나++)
                        합 = 합 * 31 + მნიშვნელობა[가] / მნიშვნელობა[나] + მნიშვნელობა[가] % მნიშვნელობა[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] შექმნა_შენატანი(int ზომა) { return new int[ზომა]; }
            public static int გაშვება() {
                int[] 가 = შექმნა_შენატანი(8); int[] 나 = 가; int[] ცარიელი_ობიექტი = new int[0];
                if (가 != 나 || 가 == null || ცარიელი_ობიექტი.length != 0 || 가[7] != 0) return 99;
                int მნიშვნელობა = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return მნიშვნელობა + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int მნიშვნელობა = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int გაშვება() { return 계산(1, 2, 3, 4, მნიშვნელობა) + 보조.კითხვა(); }
        }''', {'보조': '''public class 보조 {
            static int მნიშვნელობა = 3;
            static int 초기값() { return ++მნიშვნელობა; }
            static int კითხვა() { return მნიშვნელობა; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int მნიშვნელობა = 보조.კითხვა() + 1;
            public static int გაშვება() { return მნიშვნელობა * 10 + 보조.კითხვა(); }
        }''', {'보조': '''public class 보조 {
            static int მნიშვნელობა = 시험.მნიშვნელობა + 2;
            static int კითხვა() { return მნიშვნელობა; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String ტექსტი = "한글\\u0000😀";
            public static int გაშვება() {
                if (ტექსტი != "한글\\u0000😀") return 99;
                return (ტექსტი.length() + ტექსტი.charAt(2) + ტექსტი.charAt(3) + ტექსტი.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ფაქტორიალი(int მნიშვნელობა) { return მნიშვნელობა <= 1 ? 1 : მნიშვნელობა * ფაქტორიალი(მნიშვნელობა - 1); }
            static int 연속(int მნიშვნელობა) {
                switch (მნიშვნელობა) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int მნიშვნელობა) {
                switch (მნიშვნელობა) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int გაშვება() { return (ფაქტორიალი(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int მნიშვნელობა{} = {};'.format(ინდექსი, ინდექსი) for ინდექსი in range(270))
        덧셈 = '+'.join('მნიშვნელობა{}'.format(ინდექსი) for ინდექსი in range(270))
        self.자바대조('public class 시험 { public static int გაშვება() {' + 선언 +
                    'მნიშვნელობა_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] მნიშვნელობა = null; return მნიშვნელობა.length;', 102),
            ('int[] მნიშვნელობა = new int[1]; return მნიშვნელობა[1];', 103),
            ('int[] მნიშვნელობა = new int[1]; მნიშვნელობა[-1] = 3; return 0;', 103),
            ('int მნიშვნელობა = -1; return new int[მნიშვნელობა].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.აწყობა_წყარო('public class 시험 { public static int გაშვება() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long მნიშვნელობა; public static int გაშვება() { return 0; }',
            'public static int გაშვება() { Object მნიშვნელობა = new Object(); return 0; }',
            'public static int გაშვება() { System.out.println("hello"); return 0; }',
            'public static int გაშვება() { try { return 1; } catch (Exception შეცდომა) { return 2; } }',
            'public static synchronized int გაშვება() { return 0; }',
            'public static int გაშვება() { return new byte[3].length; }',
            'static native int 외부(); public static int გაშვება() { return 외부(); }',
            'int მნიშვნელობა; public static int გაშვება() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.აწყობა_წყარო('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.საქაღალდე_მნიშვნელობა / 'native'
        출력.write_bytes(b'original-output')
        self.აწყობა_წყარო('public class 시험 { public static int გაშვება() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.აწყობა_წყარო('public class 시험 { public static int გაშვება() { return 37; } }')
        self.assertEqual((self.საქაღალდე_მნიშვნელობა / 'native').read_bytes()[:5], b'\x7fELF\x01')
        ძებნა_ცხრილი = subprocess.check_output(['readelf', '-l', str(self.საქაღალდე_მნიშვნელობა / 'native')])
        self.assertNotIn(b'INTERP', ძებნა_ცხრილი)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.აწყობა_წყარო('public class 시험 { public static int გაშვება() { return მომხმარებელი.실행권한(); } }',
                    {'მომხმარებელი': 'public class მომხმარებელი { public static native int 실행권한(); }'}, მიზანი='user')
        მონაცემები = (self.საქაღალდე_მნიშვნელობა / 'native').read_bytes()
        self.assertEqual(მონაცემები[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', მონაცემები, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.საქაღალდე_მნიშვნელობა / 'native')]))
        # მომხმარებელი ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.აწყობა_წყარო('public class 시험 { public static int გაშვება() { return მობილური_მნიშვნელობა.포트읽기(1); } }',
                    {'მობილური_მნიშვნელობა': 'public class მობილური_მნიშვნელობა { public static native int 포트읽기(int მნიშვნელობა); }'}, 성공=False, მიზანი='user')

    def test_내보내기검증(self):
        წყარო = 'public class 시험 { public static int გაშვება() { return 0; } static int 호출(int მნიშვნელობა) { return მნიშვნელობა; } }'
        self.აწყობა_წყარო(წყარო, მიზანი='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.საქაღალდე_მნიშვნელობა / 'native')]))
        self.აწყობა_წყარო(წყარო, 성공=False, 내보냄='bad;name=시험.호출')
        self.აწყობა_წყარო(წყარო, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
