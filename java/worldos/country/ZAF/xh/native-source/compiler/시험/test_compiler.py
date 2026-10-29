"""eyona_yenzekileyo_iingcombolo ELF ukwenza_umyalelo + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.isalathisi_ixabiso_e5561a2b = Path(self.임시.name)

    def yakha_umthombo(self, UMTHOMBO, 추가=None, 성공=True, ithagethi='linux', 내보냄=None):
        indlela_uludwe = []
        for Igama, Isiqulatho_ixabiso in dict({'시험': UMTHOMBO}, **(추가 or {})).items():
            INDLELA = self.isalathisi_ixabiso_e5561a2b / (Igama + '.java')
            INDLELA.write_text(Isiqulatho_ixabiso, encoding='utf-8')
            indlela_uludwe.append(str(INDLELA))
        Umyalelo = [sys.executable, str(컴파일러), '--target', ithagethi, '--entry', '시험.Phumeza', '-o', str(self.isalathisi_ixabiso_e5561a2b / 'native')]
        if 내보냄 is not None: Umyalelo += ['--export', 내보냄]
        결과 = subprocess.run(Umyalelo + indlela_uludwe,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('yakha_umthombo Impazamo'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.isalathisi_ixabiso_e5561a2b / 'native')], timeout=5).returncode

    def 자바대조(self, UMTHOMBO, 추가=None):
        self.yakha_umthombo(UMTHOMBO, 추가)
        (self.isalathisi_ixabiso_e5561a2b / 'umsingathi.java').write_text(
            'public class umsingathi { public static void main(String[] 인수) { System.exit(시험.Phumeza()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.isalathisi_ixabiso_e5561a2b)] +
                       [str(INDLELA) for INDLELA in self.isalathisi_ixabiso_e5561a2b.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.isalathisi_ixabiso_e5561a2b), 'umsingathi'], timeout=5).returncode
        eyona_yenzekileyo_iingcombolo = self.실행결과()
        self.assertGreaterEqual(eyona_yenzekileyo_iingcombolo, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 ngqinisisa)')
        self.assertEqual(eyona_yenzekileyo_iingcombolo, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Phumeza() {
                int 합 = 7;
                int ixabiso = 12345;
                for (int indeksa = -65; indeksa <= 65; indeksa++) {
                    ixabiso = ixabiso * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(ixabiso, indeksa);
                    합 += (byte)ixabiso + (short)ixabiso + (char)ixabiso;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] ixabiso = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Phumeza() {
                int 합 = 13;
                for (int 가 = 0; 가 < ixabiso.length; 가++)
                    for (int 나 = 1; 나 < ixabiso.length; 나++)
                        합 = 합 * 31 + ixabiso[가] / ixabiso[나] + ixabiso[가] % ixabiso[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] yila_ufako_nkcukacha(int Ubukhulu) { return new int[Ubukhulu]; }
            public static int Phumeza() {
                int[] 가 = yila_ufako_nkcukacha(8); int[] 나 = 가; int[] engenanto_into = new int[0];
                if (가 != 나 || 가 == null || engenanto_into.length != 0 || 가[7] != 0) return 99;
                int ixabiso = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return ixabiso + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int ixabiso = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Phumeza() { return 계산(1, 2, 3, 4, ixabiso) + 보조.Funda(); }
        }''', {'보조': '''public class 보조 {
            static int ixabiso = 3;
            static int 초기값() { return ++ixabiso; }
            static int Funda() { return ixabiso; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int ixabiso = 보조.Funda() + 1;
            public static int Phumeza() { return ixabiso * 10 + 보조.Funda(); }
        }''', {'보조': '''public class 보조 {
            static int ixabiso = 시험.ixabiso + 2;
            static int Funda() { return ixabiso; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Umbhalo = "한글\\u0000😀";
            public static int Phumeza() {
                if (Umbhalo != "한글\\u0000😀") return 99;
                return (Umbhalo.length() + Umbhalo.charAt(2) + Umbhalo.charAt(3) + Umbhalo.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ifekthotiyali(int ixabiso) { return ixabiso <= 1 ? 1 : ixabiso * ifekthotiyali(ixabiso - 1); }
            static int 연속(int ixabiso) {
                switch (ixabiso) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int ixabiso) {
                switch (ixabiso) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Phumeza() { return (ifekthotiyali(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int ixabiso{} = {};'.format(indeksa, indeksa) for indeksa in range(270))
        덧셈 = '+'.join('ixabiso{}'.format(indeksa) for indeksa in range(270))
        self.자바대조('public class 시험 { public static int Phumeza() {' + 선언 +
                    'ixabiso_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] ixabiso = null; return ixabiso.length;', 102),
            ('int[] ixabiso = new int[1]; return ixabiso[1];', 103),
            ('int[] ixabiso = new int[1]; ixabiso[-1] = 3; return 0;', 103),
            ('int ixabiso = -1; return new int[ixabiso].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.yakha_umthombo('public class 시험 { public static int Phumeza() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long ixabiso; public static int Phumeza() { return 0; }',
            'public static int Phumeza() { Object ixabiso = new Object(); return 0; }',
            'public static int Phumeza() { System.out.println("hello"); return 0; }',
            'public static int Phumeza() { try { return 1; } catch (Exception Impazamo) { return 2; } }',
            'public static synchronized int Phumeza() { return 0; }',
            'public static int Phumeza() { return new byte[3].length; }',
            'static native int 외부(); public static int Phumeza() { return 외부(); }',
            'int ixabiso; public static int Phumeza() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.yakha_umthombo('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.isalathisi_ixabiso_e5561a2b / 'native'
        출력.write_bytes(b'original-output')
        self.yakha_umthombo('public class 시험 { public static int Phumeza() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.yakha_umthombo('public class 시험 { public static int Phumeza() { return 37; } }')
        self.assertEqual((self.isalathisi_ixabiso_e5561a2b / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.isalathisi_ixabiso_e5561a2b / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.yakha_umthombo('public class 시험 { public static int Phumeza() { return umsebenzisi.실행권한(); } }',
                    {'umsebenzisi': 'public class umsebenzisi { public static native int 실행권한(); }'}, ithagethi='user')
        iingcombolo = (self.isalathisi_ixabiso_e5561a2b / 'native').read_bytes()
        self.assertEqual(iingcombolo[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', iingcombolo, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.isalathisi_ixabiso_e5561a2b / 'native')]))
        # umsebenzisi ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.yakha_umthombo('public class 시험 { public static int Phumeza() { return isixhobo_ixabiso.포트읽기(1); } }',
                    {'isixhobo_ixabiso': 'public class isixhobo_ixabiso { public static native int 포트읽기(int ixabiso); }'}, 성공=False, ithagethi='user')

    def test_내보내기검증(self):
        UMTHOMBO = 'public class 시험 { public static int Phumeza() { return 0; } static int 호출(int ixabiso) { return ixabiso; } }'
        self.yakha_umthombo(UMTHOMBO, ithagethi='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.isalathisi_ixabiso_e5561a2b / 'native')]))
        self.yakha_umthombo(UMTHOMBO, 성공=False, 내보냄='bad;name=시험.호출')
        self.yakha_umthombo(UMTHOMBO, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
