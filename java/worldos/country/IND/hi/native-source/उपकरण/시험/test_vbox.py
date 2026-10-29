import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

परिभाषा_मान = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
मॉड्यूल_मान = importlib.util.module_from_spec(परिभाषा_मान)
परिभाषा_मान.loader.exec_module(मॉड्यूल_मान)


class 가짜상자:
    def __init__(self, मूल_मान):
        self.मूल_मान = मूल_मान
        self.명령들 = []
        self.가상기계들 = {}
        self.विफलता_मान = None

    def __call__(self, तर्क):
        तर्क = list(map(str, तर्क))
        self.명령들.append(तर्क)
        if self.विफलता_मान == तर्क[1] or (तर्क[0] == 'make' and self.विफलता_मान == 'make'):
            self.विफलता_मान = None
            raise मॉड्यूल_मान.실행오류('시험용 विफलता_मान')
        if तर्क[0] == 'make':
            पथ = self.मूल_मान / 'os/build/kernel.iso'
            पथ.parent.mkdir(parents=True, exist_ok=True)
            पथ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        क्रिया = तर्क[1]
        if क्रिया == 'list':
            return '\n'.join('"{}" {{{}}}'.format(मान['name'], इंडेक्स) for इंडेक्स, मान in self.가상기계들.items())
        if क्रिया == 'createvm':
            इंडेक्स, नाम = तर्क[तर्क.index('--uuid') + 1], तर्क[तर्क.index('--name') + 1]
            self.가상기계들[इंडेक्स] = {'UUID': इंडेक्स, 'name': नाम, 'VMState': 'poweroff',
                'CfgFile': str(self.मूल_मान / '.vbox/machines' / नाम / (नाम + '.vbox')), 'owner': None}
            return ''
        यंत्र = self.가상기계들[तर्क[2]]
        if क्रिया == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(नाम), json.dumps(मान)) for नाम, मान in यंत्र.items() if नाम != 'owner')
        if क्रिया == 'getextradata': return 'Value: ' + यंत्र['owner'] if यंत्र['owner'] else 'No value set!'
        if क्रिया == 'setextradata': यंत्र['owner'] = तर्क[4]
        elif क्रिया == 'storagectl': यंत्र['storagecontrollername0'] = 'JKOROS IDE'
        elif क्रिया == 'storageattach': यंत्र['JKOROS IDE-0-0'] = तर्क[तर्क.index('--medium') + 1]
        elif क्रिया == 'startvm': यंत्र['VMState'] = 'running'
        elif क्रिया == 'controlvm':
            assert तर्क[3] == 'resume'
            यंत्र['VMState'] = 'running'
        elif क्रिया != 'modifyvm': raise AssertionError(तर्क)
        return ''


class जाँच_मार्ग(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.मूल_मान = Path(self.임시.name)
        (self.मूल_मान / '.vbox').mkdir()
        self.상자 = 가짜상자(self.मूल_मान)
        self.निष्पादित_करें_आदेश = मॉड्यूल_मान.ऐप_लॉन्चर(self.मूल_मान, 'jkoros operating system', आदेश=self.상자)

    def बनाएँ_एन्ट्री(self):
        परिणाम = self.निष्पादित_करें_आदेश.निष्पादित_करें_आदेश()
        self.상자.명령들.clear()
        return self.상자.가상기계들[परिणाम['uuid']]

    def 변경없음(self):
        self.assertTrue(all(आदेश[0] == 'VBoxManage' and आदेश[1] in ('list', 'showvminfo', 'getextradata') for आदेश in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        परिणाम = self.निष्पादित_करें_आदेश.निष्पादित_करें_आदेश()
        self.assertEqual(परिणाम['state'], 'running')
        self.assertTrue(Path(परिणाम['iso']).is_file())
        self.assertTrue(any('--nic1' in आदेश and 'none' in आदेश for आदेश in self.상자.명령들))
        self.assertFalse(any('hdd' in आदेश or 'discardstate' in आदेश or 'createmedium' in आदेश for आदेश in self.상자.명령들))

    def test_실행중유지(self):
        self.बनाएँ_एन्ट्री()
        self.assertEqual(self.निष्पादित_करें_आदेश.निष्पादित_करें_आदेश()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        यंत्र = self.बनाएँ_एन्ट्री()
        यंत्र['VMState'] = 'saved'
        लॉग_मान = self.निष्पादित_करें_आदेश.पथ(self.निष्पादित_करें_आदेश.पढ़ें()['serial_log'])
        लॉग_मान.write_text('saved log')
        self.निष्पादित_करें_आदेश.निष्पादित_करें_आदेश()
        self.assertFalse(any(आदेश[0] == 'make' or आदेश[1] == 'modifyvm' for आदेश in self.상자.명령들))
        self.assertEqual([पथ.read_text() for पथ in लॉग_मान.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.बनाएँ_एन्ट्री()['VMState'] = 'paused'
        self.निष्पादित_करें_आदेश.निष्पादित_करें_आदेश()
        self.assertTrue(any(आदेश[1] == 'controlvm' and आदेश[3] == 'resume' for आदेश in self.상자.명령들))
        self.assertFalse(any(आदेश[0] == 'make' for आदेश in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(मॉड्यूल_मान.실행오류): self.निष्पादित_करें_आदेश.निष्पादित_करें_आदेश()
        self.변경없음()

    def test_소유표식거부(self):
        self.बनाएँ_एन्ट्री()['owner'] = 'someone-else'
        with self.assertRaises(मॉड्यूल_मान.실행오류): self.निष्पादित_करें_आदेश.निष्पादित_करें_आदेश()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.बनाएँ_एन्ट्री()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(मॉड्यूल_मान.실행오류): self.निष्पादित_करें_आदेश.निष्पादित_करें_आदेश()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        यंत्र = self.बनाएँ_एन्ट्री()
        यंत्र['VMState'] = 'poweroff'
        यंत्र['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(मॉड्यूल_मान.실행오류): self.निष्पादित_करें_आदेश.निष्पादित_करें_आदेश()
        self.변경없음()

    def test_전환중거부(self):
        self.बनाएँ_एन्ट्री()['VMState'] = 'saving'
        with self.assertRaises(मॉड्यूल_मान.실행오류): self.निष्पादित_करें_आदेश.निष्पादित_करें_आदेश()
        self.변경없음()

    def test_등록해제거부(self):
        self.बनाएँ_एन्ट्री()
        self.상자.가상기계들.clear()
        with self.assertRaises(मॉड्यूल_मान.실행오류): self.निष्पादित_करें_आदेश.निष्पादित_करें_आदेश()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        यंत्र = self.बनाएँ_एन्ट्री()
        यंत्र['VMState'] = 'poweroff'
        이전 = dict(यंत्र)
        self.상자.विफलता_मान = 'make'
        with self.assertRaises(मॉड्यूल_मान.실행오류): self.निष्पादित_करें_आदेश.निष्पादित_करें_आदेश()
        self.assertEqual(यंत्र, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.विफलता_मान = 'setextradata'
        with self.assertRaises(मॉड्यूल_मान.실행오류): self.निष्पादित_करें_आदेश.निष्पादित_करें_आदेश()
        self.상자.명령들.clear()
        self.assertEqual(self.निष्पादित_करें_आदेश.निष्पादित_करें_आदेश()['state'], 'running')
        self.assertFalse(any(आदेश[1] == 'createvm' for आदेश in self.상자.명령들))

    def test_보존ISO변조거부(self):
        यंत्र = self.बनाएँ_एन्ट्री()
        यंत्र['VMState'] = 'poweroff'
        Path(यंत्र['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(मॉड्यूल_मान.실행오류): self.निष्पादित_करें_आदेश.निष्पादित_करें_आदेश()

    def test_상태미생성(self):
        self.assertEqual(self.निष्पादित_करें_आदेश.शो_अवस्था()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for पथ in ('../outside', '/tmp/outside'):
            with self.assertRaises(मॉड्यूल_मान.실행오류): self.निष्पादित_करें_आदेश.पथ(पथ)
        (self.मूल_मान / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(मॉड्यूल_मान.실행오류): self.निष्पादित_करें_आदेश.पथ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        परिणाम = मॉड्यूल_मान.विशेषता_मान('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(परिणाम['VMState'], 'running')
        self.assertEqual(परिणाम['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
