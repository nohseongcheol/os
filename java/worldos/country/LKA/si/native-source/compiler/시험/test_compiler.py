"""තථ්_ය_දත්ත ELF ක්_රියාත්මක_කරන්න_විධානය + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.නාමාවලිය_අගය = Path(self.임시.name)

    def සාදන්න_මූලය(self, මූලය, 추가=None, 성공=True, ඉලක්කය='linux', 내보냄=None):
        පෙත_ලැයිස්තුව = []
        for නම, අන්තර්ගතය_අගය in dict({'시험': මූලය}, **(추가 or {})).items():
            මාර්_ගය = self.නාමාවලිය_අගය / (නම + '.java')
            මාර්_ගය.write_text(අන්තර්ගතය_අගය, encoding='utf-8')
            පෙත_ලැයිස්තුව.append(str(මාර්_ගය))
        විධානය = [sys.executable, str(컴파일러), '--target', ඉලක්කය, '--entry', '시험.ක්_රියාත්මක_කරන්න_2', '-o', str(self.නාමාවලිය_අගය / 'native')]
        if 내보냄 is not None: විධානය += ['--export', 내보냄]
        결과 = subprocess.run(විධානය + පෙත_ලැයිස්තුව,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('සාදන්න_මූලය දෝෂය'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.නාමාවලිය_අගය / 'native')], timeout=5).returncode

    def 자바대조(self, මූලය, 추가=None):
        self.සාදන්න_මූලය(මූලය, 추가)
        (self.නාමාවලිය_අගය / 'ධාරකය.java').write_text(
            'public class ධාරකය { public static void main(String[] විස්තාරක) { System.exit(시험.ක්_රියාත්මක_කරන්න_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.නාමාවලිය_අගය)] +
                       [str(මාර්_ගය) for මාර්_ගය in self.නාමාවලිය_අගය.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.නාමාවලිය_අගය), 'ධාරකය'], timeout=5).returncode
        තථ්_ය_දත්ත = self.실행결과()
        self.assertGreaterEqual(තථ්_ය_දත්ත, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 තහවුරු_කරන්න)')
        self.assertEqual(තථ්_ය_දත්ත, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int ක්_රියාත්මක_කරන්න_2() {
                int 합 = 7;
                int අගය = 12345;
                for (int සූචිය = -65; සූචිය <= 65; සූචිය++) {
                    අගය = අගය * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(අගය, සූචිය);
                    합 += (byte)අගය + (short)අගය + (char)අගය;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] අගය = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int ක්_රියාත්මක_කරන්න_2() {
                int 합 = 13;
                for (int 가 = 0; 가 < අගය.length; 가++)
                    for (int 나 = 1; 나 < අගය.length; 나++)
                        합 = 합 * 31 + අගය[가] / අගය[나] + අගය[가] % අගය[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] සාදන්න_පිවිසුම(int ප්_රමාණය) { return new int[ප්_රමාණය]; }
            public static int ක්_රියාත්මක_කරන්න_2() {
                int[] 가 = සාදන්න_පිවිසුම(8); int[] 나 = 가; int[] ශූන්_ය_වස්තුව = new int[0];
                if (가 != 나 || 가 == null || ශූන්_ය_වස්තුව.length != 0 || 가[7] != 0) return 99;
                int අගය = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return අගය + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int අගය = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int ක්_රියාත්මක_කරන්න_2() { return 계산(1, 2, 3, 4, අගය) + 보조.කියවීම(); }
        }''', {'보조': '''public class 보조 {
            static int අගය = 3;
            static int 초기값() { return ++අගය; }
            static int කියවීම() { return අගය; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int අගය = 보조.කියවීම() + 1;
            public static int ක්_රියාත්මක_කරන්න_2() { return අගය * 10 + 보조.කියවීම(); }
        }''', {'보조': '''public class 보조 {
            static int අගය = 시험.අගය + 2;
            static int කියවීම() { return අගය; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String පෙළ = "한글\\u0000😀";
            public static int ක්_රියාත්මක_කරන්න_2() {
                if (පෙළ != "한글\\u0000😀") return 99;
                return (පෙළ.length() + පෙළ.charAt(2) + පෙළ.charAt(3) + පෙළ.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ක්_රමාරෝපිත(int අගය) { return අගය <= 1 ? 1 : අගය * ක්_රමාරෝපිත(අගය - 1); }
            static int 연속(int අගය) {
                switch (අගය) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int අගය) {
                switch (අගය) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int ක්_රියාත්මක_කරන්න_2() { return (ක්_රමාරෝපිත(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int අගය{} = {};'.format(සූචිය, සූචිය) for සූචිය in range(270))
        덧셈 = '+'.join('අගය{}'.format(සූචිය) for සූචිය in range(270))
        self.자바대조('public class 시험 { public static int ක්_රියාත්මක_කරන්න_2() {' + 선언 +
                    'අගය_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] අගය = null; return අගය.length;', 102),
            ('int[] අගය = new int[1]; return අගය[1];', 103),
            ('int[] අගය = new int[1]; අගය[-1] = 3; return 0;', 103),
            ('int අගය = -1; return new int[අගය].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.සාදන්න_මූලය('public class 시험 { public static int ක්_රියාත්මක_කරන්න_2() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long අගය; public static int ක්_රියාත්මක_කරන්න_2() { return 0; }',
            'public static int ක්_රියාත්මක_කරන්න_2() { Object අගය = new Object(); return 0; }',
            'public static int ක්_රියාත්මක_කරන්න_2() { System.out.println("hello"); return 0; }',
            'public static int ක්_රියාත්මක_කරන්න_2() { try { return 1; } catch (Exception දෝෂය) { return 2; } }',
            'public static synchronized int ක්_රියාත්මක_කරන්න_2() { return 0; }',
            'public static int ක්_රියාත්මක_කරන්න_2() { return new byte[3].length; }',
            'static native int 외부(); public static int ක්_රියාත්මක_කරන්න_2() { return 외부(); }',
            'int අගය; public static int ක්_රියාත්මක_කරන්න_2() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.සාදන්න_මූලය('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.නාමාවලිය_අගය / 'native'
        출력.write_bytes(b'original-output')
        self.සාදන්න_මූලය('public class 시험 { public static int ක්_රියාත්මක_කරන්න_2() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.සාදන්න_මූලය('public class 시험 { public static int ක්_රියාත්මක_කරන්න_2() { return 37; } }')
        self.assertEqual((self.නාමාවලිය_අගය / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.නාමාවලිය_අගය / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.සාදන්න_මූලය('public class 시험 { public static int ක්_රියාත්මක_කරන්න_2() { return පරිශීලක.실행권한(); } }',
                    {'පරිශීලක': 'public class පරිශීලක { public static native int 실행권한(); }'}, ඉලක්කය='user')
        දත්ත = (self.නාමාවලිය_අගය / 'native').read_bytes()
        self.assertEqual(දත්ත[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', දත්ත, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.නාමාවලිය_අගය / 'native')]))
        # පරිශීලක ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.සාදන්න_මූලය('public class 시험 { public static int ක්_රියාත්මක_කරන්න_2() { return ජංගම_අගය.포트읽기(1); } }',
                    {'ජංගම_අගය': 'public class ජංගම_අගය { public static native int 포트읽기(int අගය); }'}, 성공=False, ඉලක්කය='user')

    def test_내보내기검증(self):
        මූලය = 'public class 시험 { public static int ක්_රියාත්මක_කරන්න_2() { return 0; } static int 호출(int අගය) { return අගය; } }'
        self.සාදන්න_මූලය(මූලය, ඉලක්කය='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.නාමාවලිය_අගය / 'native')]))
        self.සාදන්න_මූලය(මූලය, 성공=False, 내보냄='bad;name=시험.호출')
        self.සාදන්න_මූලය(මූලය, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
