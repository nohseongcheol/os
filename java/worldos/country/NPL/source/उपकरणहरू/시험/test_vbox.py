import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

परिभाषा_मान = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
मोड्युल_मान = importlib.util.module_from_spec(परिभाषा_मान)
परिभाषा_मान.loader.exec_module(मोड्युल_मान)


class 가짜상자:
    def __init__(self, रूट_मान):
        self.रूट_मान = रूट_मान
        self.명령들 = []
        self.가상기계들 = {}
        self.विफल_मान = None

    def __call__(self, तर्क):
        तर्क = list(map(str, तर्क))
        self.명령들.append(तर्क)
        if self.विफल_मान == तर्क[1] or (तर्क[0] == 'make' and self.विफल_मान == 'make'):
            self.विफल_मान = None
            raise मोड्युल_मान.실행오류('시험용 विफल_मान')
        if तर्क[0] == 'make':
            मार्ग = self.रूट_मान / 'os/build/kernel.iso'
            मार्ग.parent.mkdir(parents=True, exist_ok=True)
            मार्ग.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        कार्य = तर्क[1]
        if कार्य == 'list':
            return '\n'.join('"{}" {{{}}}'.format(मान['name'], अनुक्रमणिका) for अनुक्रमणिका, मान in self.가상기계들.items())
        if कार्य == 'createvm':
            अनुक्रमणिका, नाम = तर्क[तर्क.index('--uuid') + 1], तर्क[तर्क.index('--name') + 1]
            self.가상기계들[अनुक्रमणिका] = {'UUID': अनुक्रमणिका, 'name': नाम, 'VMState': 'poweroff',
                'CfgFile': str(self.रूट_मान / '.vbox/machines' / नाम / (नाम + '.vbox')), 'owner': None}
            return ''
        मेशिन = self.가상기계들[तर्क[2]]
        if कार्य == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(नाम), json.dumps(मान)) for नाम, मान in मेशिन.items() if नाम != 'owner')
        if कार्य == 'getextradata': return 'Value: ' + मेशिन['owner'] if मेशिन['owner'] else 'No value set!'
        if कार्य == 'setextradata': मेशिन['owner'] = तर्क[4]
        elif कार्य == 'storagectl': मेशिन['storagecontrollername0'] = 'JKOROS IDE'
        elif कार्य == 'storageattach': मेशिन['JKOROS IDE-0-0'] = तर्क[तर्क.index('--medium') + 1]
        elif कार्य == 'startvm': मेशिन['VMState'] = 'running'
        elif कार्य == 'controlvm':
            assert तर्क[3] == 'resume'
            मेशिन['VMState'] = 'running'
        elif कार्य != 'modifyvm': raise AssertionError(तर्क)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.रूट_मान = Path(self.임시.name)
        (self.रूट_मान / '.vbox').mkdir()
        self.상자 = 가짜상자(self.रूट_मान)
        self.कार्यान्वयन_गर्नुहोस्_आदेश = मोड्युल_मान.अनुप्रयोग_कर्मचारी_अगुवा(self.रूट_मान, 'jkoros operating system', आदेश=self.상자)

    def सिर्जना_प्रविष्टि(self):
        मापन = self.कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश()
        self.상자.명령들.clear()
        return self.상자.가상기계들[मापन['uuid']]

    def 변경없음(self):
        self.assertTrue(all(आदेश[0] == 'VBoxManage' and आदेश[1] in ('list', 'showvminfo', 'getextradata') for आदेश in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        मापन = self.कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश()
        self.assertEqual(मापन['state'], 'running')
        self.assertTrue(Path(मापन['iso']).is_file())
        self.assertTrue(any('--nic1' in आदेश and 'none' in आदेश for आदेश in self.상자.명령들))
        self.assertFalse(any('hdd' in आदेश or 'discardstate' in आदेश or 'createmedium' in आदेश for आदेश in self.상자.명령들))

    def test_실행중유지(self):
        self.सिर्जना_प्रविष्टि()
        self.assertEqual(self.कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        मेशिन = self.सिर्जना_प्रविष्टि()
        मेशिन['VMState'] = 'saved'
        लग_मान = self.कार्यान्वयन_गर्नुहोस्_आदेश.मार्ग(self.कार्यान्वयन_गर्नुहोस्_आदेश.पढनुहोस्()['serial_log'])
        लग_मान.write_text('saved log')
        self.कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश()
        self.assertFalse(any(आदेश[0] == 'make' or आदेश[1] == 'modifyvm' for आदेश in self.상자.명령들))
        self.assertEqual([मार्ग.read_text() for मार्ग in लग_मान.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.सिर्जना_प्रविष्टि()['VMState'] = 'paused'
        self.कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश()
        self.assertTrue(any(आदेश[1] == 'controlvm' and आदेश[3] == 'resume' for आदेश in self.상자.명령들))
        self.assertFalse(any(आदेश[0] == 'make' for आदेश in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(मोड्युल_मान.실행오류): self.कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश()
        self.변경없음()

    def test_소유표식거부(self):
        self.सिर्जना_प्रविष्टि()['owner'] = 'someone-else'
        with self.assertRaises(मोड्युल_मान.실행오류): self.कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.सिर्जना_प्रविष्टि()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(मोड्युल_मान.실행오류): self.कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        मेशिन = self.सिर्जना_प्रविष्टि()
        मेशिन['VMState'] = 'poweroff'
        मेशिन['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(मोड्युल_मान.실행오류): self.कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश()
        self.변경없음()

    def test_전환중거부(self):
        self.सिर्जना_प्रविष्टि()['VMState'] = 'saving'
        with self.assertRaises(मोड्युल_मान.실행오류): self.कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश()
        self.변경없음()

    def test_등록해제거부(self):
        self.सिर्जना_प्रविष्टि()
        self.상자.가상기계들.clear()
        with self.assertRaises(मोड्युल_मान.실행오류): self.कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        मेशिन = self.सिर्जना_प्रविष्टि()
        मेशिन['VMState'] = 'poweroff'
        이전 = dict(मेशिन)
        self.상자.विफल_मान = 'make'
        with self.assertRaises(मोड्युल_मान.실행오류): self.कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश()
        self.assertEqual(मेशिन, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.विफल_मान = 'setextradata'
        with self.assertRaises(मोड्युल_मान.실행오류): self.कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश()
        self.상자.명령들.clear()
        self.assertEqual(self.कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश()['state'], 'running')
        self.assertFalse(any(आदेश[1] == 'createvm' for आदेश in self.상자.명령들))

    def test_보존ISO변조거부(self):
        मेशिन = self.सिर्जना_प्रविष्टि()
        मेशिन['VMState'] = 'poweroff'
        Path(मेशिन['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(मोड्युल_मान.실행오류): self.कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश()

    def test_상태미생성(self):
        self.assertEqual(self.कार्यान्वयन_गर्नुहोस्_आदेश.शो_स्थिति()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for मार्ग in ('../outside', '/tmp/outside'):
            with self.assertRaises(मोड्युल_मान.실행오류): self.कार्यान्वयन_गर्नुहोस्_आदेश.मार्ग(मार्ग)
        (self.रूट_मान / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(मोड्युल_मान.실행오류): self.कार्यान्वयन_गर्नुहोस्_आदेश.मार्ग('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        मापन = मोड्युल_मान.विशेषण_मान('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(मापन['VMState'], 'running')
        self.assertEqual(मापन['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
