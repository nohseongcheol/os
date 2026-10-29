"""वास्तविक_डेटा ELF आज्ञा_कार्यवाही_करा + OpenJDK मोजमाप 대조. तात्पुरते_मूल्य चाचण्या 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

संकलक = Path(__file__).resolve().parents[1] / 'संकलक.py'


class स्वकीय_चाचणी(unittest.TestCase):
    def setUp(self):
        self.तात्पुरते_मूल्य = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.तात्पुरते_मूल्य.cleanup)
        self.निर्देशिका_मूल्य = Path(self.तात्पुरते_मूल्य.name)

    def स्रोत_बांधणी(self, स्रोत, शेवटीजोडा_प्रविष्टी=None, यश_मूल्य=True, लक्ष्य='linux', निर्यातकेलेले_मूल्य=None):
        पथ_यादी = []
        for नाव, सामुग्री_मूल्य in dict({'चाचण्या': स्रोत}, **(शेवटीजोडा_प्रविष्टी or {})).items():
            मार्ग = self.निर्देशिका_मूल्य / (नाव + '.java')
            मार्ग.write_text(सामुग्री_मूल्य, encoding='utf-8')
            पथ_यादी.append(str(मार्ग))
        आदेश = [sys.executable, str(संकलक), '--target', लक्ष्य, '--entry', 'चाचण्या.सुरू_करा', '-o', str(self.निर्देशिका_मूल्य / 'native')]
        if निर्यातकेलेले_मूल्य is not None: आदेश += ['--export', निर्यातकेलेले_मूल्य]
        मोजमाप = subprocess.run(आदेश + पथ_यादी,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if यश_मूल्य:
            self.assertEqual(मोजमाप.returncode, 0, मोजमाप.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(मोजमाप.returncode, 0)
            self.assertIn('स्रोत_बांधणी त्रुटी'.encode(), मोजमाप.stderr)
        return मोजमाप

    def निष्पादन_मोजमाप(self):
        return subprocess.run([str(self.निर्देशिका_मूल्य / 'native')], timeout=5).returncode

    def जावा_तुलना(self, स्रोत, शेवटीजोडा_प्रविष्टी=None):
        self.स्रोत_बांधणी(स्रोत, शेवटीजोडा_प्रविष्टी)
        (self.निर्देशिका_मूल्य / 'होस्ट.java').write_text(
            'public class होस्ट { public static void main(String[] बाबी) { System.exit(चाचण्या.सुरू_करा()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.निर्देशिका_मूल्य)] +
                       [str(मार्ग) for मार्ग in self.निर्देशिका_मूल्य.glob('*.java')], check=True, timeout=30)
        अपेक्षा = subprocess.run(['java', '-cp', str(self.निर्देशिका_मूल्य), 'होस्ट'], timeout=5).returncode
        वास्तविक_डेटा = self.निष्पादन_मोजमाप()
        self.assertGreaterEqual(वास्तविक_डेटा, 0, '신호로 आहे_बाहेरपडलेले (샌드박스의 32비트 syscall मर्यादा_मूल्य 여부 पडताळा)')
        self.assertEqual(वास्तविक_डेटा, अपेक्षा)

    def पूर्णांक_अंकगणिती_आणि_सरकवण्या_चाचणी(self):
        self.जावा_तुलना('''public class चाचण्या {
            static int मिक्स_अंकगणिती(int पहिले_संकार्य, int दुसरे_संकार्य) {
                return ((पहिले_संकार्य + दुसरे_संकार्य) ^ (पहिले_संकार्य - दुसरे_संकार्य) ^ (पहिले_संकार्य * दुसरे_संकार्य) ^ (पहिले_संकार्य & दुसरे_संकार्य) ^ (पहिले_संकार्य | दुसरे_संकार्य))
                    + (पहिले_संकार्य << दुसरे_संकार्य) + (पहिले_संकार्य >> दुसरे_संकार्य) + (पहिले_संकार्य >>> दुसरे_संकार्य);
            }
            public static int सुरू_करा() {
                int बेरीज_मूल्य = 7;
                int मूल्य = 12345;
                for (int अनुक्रमणिका = -65; अनुक्रमणिका <= 65; अनुक्रमणिका++) {
                    मूल्य = मूल्य * 1664525 + 1013904223;
                    बेरीज_मूल्य = बेरीज_मूल्य * 31 + मिक्स_अंकगणिती(मूल्य, अनुक्रमणिका);
                    बेरीज_मूल्य += (byte)मूल्य + (short)मूल्य + (char)मूल्य;
                }
                return (बेरीज_मूल्य & 0x7fffffff) % 251;
            }
        }''')

    def भागाकार_अत्यंत_मूल्ये_चाचणी(self):
        self.जावा_तुलना('''public class चाचण्या {
            static int[] मूल्य = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int सुरू_करा() {
                int बेरीज_मूल्य = 13;
                for (int पहिले_संकार्य = 0; पहिले_संकार्य < मूल्य.length; पहिले_संकार्य++)
                    for (int दुसरे_संकार्य = 1; दुसरे_संकार्य < मूल्य.length; दुसरे_संकार्य++)
                        बेरीज_मूल्य = बेरीज_मूल्य * 31 + मूल्य[पहिले_संकार्य] / मूल्य[दुसरे_संकार्य] + मूल्य[पहिले_संकार्य] % मूल्य[दुसरे_संकार्य];
                return (बेरीज_मूल्य & 0x7fffffff) % 251;
            }
        }''')

    def व्यूह_आणि_संदर्भ_चाचणी(self):
        self.जावा_तुलना('''public class चाचण्या {
            static int[] प्रविष्टी_तयार_करा(int आकार) { return new int[आकार]; }
            public static int सुरू_करा() {
                int[] पहिले_संकार्य = प्रविष्टी_तयार_करा(8); int[] दुसरे_संकार्य = पहिले_संकार्य; int[] रिक्त_ऑब्जेक्ट = new int[0];
                if (पहिले_संकार्य != दुसरे_संकार्य || पहिले_संकार्य == null || रिक्त_ऑब्जेक्ट.length != 0 || पहिले_संकार्य[7] != 0) return 99;
                int मूल्य = (पहिले_संकार्य[2] = 40); पहिले_संकार्य[2]++; ++पहिले_संकार्य[3]; पहिले_संकार्य[2] += 7;
                return मूल्य + दुसरे_संकार्य[2] + दुसरे_संकार्य[3];
            }
        }''')

    def स्थिर_क्षेत्रे_आणि_वितर्क_क्रम_चाचणी(self):
        self.जावा_तुलना('''public class चाचण्या {
            static int मूल्य = सहायक_मूल्य.प्रारंभिक_मूल्य();
            static int गणना(int पहिले_संकार्य, int दुसरे_संकार्य, int तिसरे_संकार्य, int चौथे_संकार्य, int पाचवे_संकार्य) {
                return पहिले_संकार्य + दुसरे_संकार्य * 2 + तिसरे_संकार्य * 3 + चौथे_संकार्य * 4 + पाचवे_संकार्य * 5;
            }
            public static int सुरू_करा() { return गणना(1, 2, 3, 4, मूल्य) + सहायक_मूल्य.वाचन(); }
        }''', {'सहायक_मूल्य': '''public class सहायक_मूल्य {
            static int मूल्य = 3;
            static int प्रारंभिक_मूल्य() { return ++मूल्य; }
            static int वाचन() { return मूल्य; }
        }'''})

    def आरंभीकरण_चक्र_चाचणी(self):
        self.जावा_तुलना('''public class चाचण्या {
            static int मूल्य = सहायक_मूल्य.वाचन() + 1;
            public static int सुरू_करा() { return मूल्य * 10 + सहायक_मूल्य.वाचन(); }
        }''', {'सहायक_मूल्य': '''public class सहायक_मूल्य {
            static int मूल्य = चाचण्या.मूल्य + 2;
            static int वाचन() { return मूल्य; }
        }'''})

    def सुधारित_युनिकोडसंकेतन_8_अक्षरमाला_चाचणी(self):
        self.जावा_तुलना('''public class चाचण्या {
            static String पाठ्य = "한글\\u0000😀";
            public static int सुरू_करा() {
                if (पाठ्य != "한글\\u0000😀") return 99;
                return (पाठ्य.length() + पाठ्य.charAt(2) + पाठ्य.charAt(3) + पाठ्य.charAt(4)) % 251;
            }
        }''')

    def स्विच_आणि_पुनरावर्तन_चाचणी(self):
        self.जावा_तुलना('''public class चाचण्या {
            static int क्रमगुणित(int मूल्य) { return मूल्य <= 1 ? 1 : मूल्य * क्रमगुणित(मूल्य - 1); }
            static int दाट_स्विच_प्रकरणे(int मूल्य) {
                switch (मूल्य) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int विरळ_स्विच_प्रकरणे(int मूल्य) {
                switch (मूल्य) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int सुरू_करा() { return (क्रमगुणित(5) + दाट_स्विच_प्रकरणे(0) + दाट_स्विच_प्रकरणे(2) + दाट_स्विच_प्रकरणे(9) + विरळ_स्विच_प्रकरणे(-1000) + विरळ_स्विच_प्रकरणे(0)) % 251; }
        }''')

    def रुंद_स्थानिक_चले_चाचणी(self):
        घोषणा = '\n'.join('int मूल्य{} = {};'.format(अनुक्रमणिका, अनुक्रमणिका) for अनुक्रमणिका in range(270))
        बेरीज_मोजमाप = '+'.join('मूल्य{}'.format(अनुक्रमणिका) for अनुक्रमणिका in range(270))
        self.जावा_तुलना('public class चाचण्या { public static int सुरू_करा() {' + घोषणा +
                    'मूल्य_269 += 300; return (' + बेरीज_मोजमाप + ') % 251; } }')

    def सामान्य_भाषा_रनटाइम_त्रुटी_संख्या_चाचणी(self):
        काम_नोंदी = [
            ('int शून्य_संकार्य = 0; return 1 / शून्य_संकार्य;', 101),
            ('int[] मूल्य = null; return मूल्य.length;', 102),
            ('int[] मूल्य = new int[1]; return मूल्य[1];', 103),
            ('int[] मूल्य = new int[1]; मूल्य[-1] = 3; return 0;', 103),
            ('int मूल्य = -1; return new int[मूल्य].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] पहिले_संकार्य = new int[65535]; return new int[1].length;', 105),
        ]
        for मुख्य_भाग_मूल्य, अपेक्षा in काम_नोंदी:
            with self.subTest(मुख्य_भाग_मूल्य=मुख्य_भाग_मूल्य):
                self.स्रोत_बांधणी('public class चाचण्या { public static int सुरू_करा() { ' + मुख्य_भाग_मूल्य + ' } }')
                self.assertEqual(self.निष्पादन_मोजमाप(), अपेक्षा)

    def असमर्थित_वैशिष्ट्य_नाकारलेले_चाचणी(self):
        काम_नोंदी = [
            'static long मूल्य; public static int सुरू_करा() { return 0; }',
            'public static int सुरू_करा() { Object मूल्य = new Object(); return 0; }',
            'public static int सुरू_करा() { System.out.println("hello"); return 0; }',
            'public static int सुरू_करा() { try { return 1; } catch (Exception त्रुटी) { return 2; } }',
            'public static synchronized int सुरू_करा() { return 0; }',
            'public static int सुरू_करा() { return new byte[3].length; }',
            'static native int बाह्य_मूल्य(); public static int सुरू_करा() { return बाह्य_मूल्य(); }',
            'int मूल्य; public static int सुरू_करा() { return 0; }',
        ]
        for मुख्य_भाग_मूल्य in काम_नोंदी:
            with self.subTest(मुख्य_भाग_मूल्य=मुख्य_भाग_मूल्य):
                self.स्रोत_बांधणी('public class चाचण्या { ' + मुख्य_भाग_मूल्य + ' }', यश_मूल्य=False)

    def विद्यमान_प्रदान_जतनकेलेले_चालू_बिघाड_चाचणी(self):
        आउटपुट = self.निर्देशिका_मूल्य / 'native'
        आउटपुट.write_bytes(b'original-output')
        self.स्रोत_बांधणी('public class चाचण्या { public static int सुरू_करा() { return missing; } }', यश_मूल्य=False)
        self.assertEqual(आउटपुट.read_bytes(), b'original-output')

    def ईएलएफ_आणि_स्वतंत्र_निष्पादन_चाचणी(self):
        self.स्रोत_बांधणी('public class चाचण्या { public static int सुरू_करा() { return 37; } }')
        self.assertEqual((self.निर्देशिका_मूल्य / 'native').read_bytes()[:5], b'\x7fELF\x01')
        लुकअप_सारणी = subprocess.check_output(['readelf', '-l', str(self.निर्देशिका_मूल्य / 'native')])
        self.assertNotIn(b'INTERP', लुकअप_सारणी)
        self.assertEqual(self.निष्पादन_मोजमाप(), 37)

    def प्रयोक्ता_ईएलएफ_आणि_द्विमानजोडणी_विभाजन_चाचणी(self):
        self.स्रोत_बांधणी('public class चाचण्या { public static int सुरू_करा() { return प्रयोक्ता.निष्पादन_परवानगी(); } }',
                    {'प्रयोक्ता': 'public class प्रयोक्ता { public static native int निष्पादन_परवानगी(); }'}, लक्ष्य='user')
        डेटा = (self.निर्देशिका_मूल्य / 'native').read_bytes()
        self.assertEqual(डेटा[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', डेटा, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.निर्देशिका_मूल्य / 'native')]))
        # प्रयोक्ता ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.स्रोत_बांधणी('public class चाचण्या { public static int सुरू_करा() { return मोबाइल_मूल्य.हार्डवेअर_पॉर्ट_वाचा(1); } }',
                    {'मोबाइल_मूल्य': 'public class मोबाइल_मूल्य { public static native int हार्डवेअर_पॉर्ट_वाचा(int मूल्य); }'}, यश_मूल्य=False, लक्ष्य='user')

    def निर्यात_करा_पडताळणी_चाचणी(self):
        स्रोत = 'public class चाचण्या { public static int सुरू_करा() { return 0; } static int आवाहन(int मूल्य) { return मूल्य; } }'
        self.स्रोत_बांधणी(स्रोत, लक्ष्य='kernel', निर्यातकेलेले_मूल्य='kernel_dispatch=चाचण्या.आवाहन')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.निर्देशिका_मूल्य / 'native')]))
        self.स्रोत_बांधणी(स्रोत, यश_मूल्य=False, निर्यातकेलेले_मूल्य='bad;name=चाचण्या.आवाहन')
        self.स्रोत_बांधणी(स्रोत, यश_मूल्य=False, निर्यातकेलेले_मूल्य='missing=चाचण्या.अनुपस्थित_पद्धत')


if __name__ == '__main__':
    unittest.main()
