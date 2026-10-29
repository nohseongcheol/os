import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

परिभाशा_मोल = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
मॉड्यूल_मोल = importlib.util.module_from_spec(परिभाशा_मोल)
परिभाशा_मोल.loader.exec_module(मॉड्यूल_मोल)


class 가짜상자:
    def __init__(self, रूट_मोल):
        self.रूट_मोल = रूट_मोल
        self.명령들 = []
        self.가상기계들 = {}
        self.अपेस_मोल = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.अपेस_मोल == 인수[1] or (인수[0] == 'make' and self.अपेस_मोल == 'make'):
            self.अपेस_मोल = None
            raise मॉड्यूल_मोल.실행오류('시험용 अपेस_मोल')
        if 인수[0] == 'make':
            पाथ = self.रूट_मोल / 'os/build/kernel.iso'
            पाथ.parent.mkdir(parents=True, exist_ok=True)
            पाथ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        कृती = 인수[1]
        if कृती == 'list':
            return '\n'.join('"{}" {{{}}}'.format(मोल['name'], INDEX) for INDEX, मोल in self.가상기계들.items())
        if कृती == 'createvm':
            INDEX, नांव = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': नांव, 'VMState': 'poweroff',
                'CfgFile': str(self.रूट_मोल / '.vbox/machines' / नांव / (नांव + '.vbox')), 'owner': None}
            return ''
        यंत्र = self.가상기계들[인수[2]]
        if कृती == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(नांव), json.dumps(मोल)) for नांव, मोल in यंत्र.items() if नांव != 'owner')
        if कृती == 'getextradata': return 'Value: ' + यंत्र['owner'] if यंत्र['owner'] else 'No value set!'
        if कृती == 'setextradata': यंत्र['owner'] = 인수[4]
        elif कृती == 'storagectl': यंत्र['storagecontrollername0'] = 'JKOROS IDE'
        elif कृती == 'storageattach': यंत्र['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif कृती == 'startvm': यंत्र['VMState'] = 'running'
        elif कृती == 'controlvm':
            assert 인수[3] == 'resume'
            यंत्र['VMState'] = 'running'
        elif कृती != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.रूट_मोल = Path(self.임시.name)
        (self.रूट_मोल / '.vbox').mkdir()
        self.상자 = 가짜상자(self.रूट_मोल)
        self.पाळो_दिवचो_आदेश = मॉड्यूल_मोल.एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर(self.रूट_मोल, 'jkoros operating system', आदेश=self.상자)

    def निर्माण_करचें_प्रवेश(self):
        मेजप = self.पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश()
        self.상자.명령들.clear()
        return self.상자.가상기계들[मेजप['uuid']]

    def 변경없음(self):
        self.assertTrue(all(आदेश[0] == 'VBoxManage' and आदेश[1] in ('list', 'showvminfo', 'getextradata') for आदेश in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        मेजप = self.पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश()
        self.assertEqual(मेजप['state'], 'running')
        self.assertTrue(Path(मेजप['iso']).is_file())
        self.assertTrue(any('--nic1' in आदेश and 'none' in आदेश for आदेश in self.상자.명령들))
        self.assertFalse(any('hdd' in आदेश or 'discardstate' in आदेश or 'createmedium' in आदेश for आदेश in self.상자.명령들))

    def test_실행중유지(self):
        self.निर्माण_करचें_प्रवेश()
        self.assertEqual(self.पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        यंत्र = self.निर्माण_करचें_प्रवेश()
        यंत्र['VMState'] = 'saved'
        LOG_मोल = self.पाळो_दिवचो_आदेश.पाथ(self.पाळो_दिवचो_आदेश.읽기()['serial_log'])
        LOG_मोल.write_text('saved log')
        self.पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश()
        self.assertFalse(any(आदेश[0] == 'make' or आदेश[1] == 'modifyvm' for आदेश in self.상자.명령들))
        self.assertEqual([पाथ.read_text() for पाथ in LOG_मोल.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.निर्माण_करचें_प्रवेश()['VMState'] = 'paused'
        self.पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश()
        self.assertTrue(any(आदेश[1] == 'controlvm' and आदेश[3] == 'resume' for आदेश in self.상자.명령들))
        self.assertFalse(any(आदेश[0] == 'make' for आदेश in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(मॉड्यूल_मोल.실행오류): self.पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश()
        self.변경없음()

    def test_소유표식거부(self):
        self.निर्माण_करचें_प्रवेश()['owner'] = 'someone-else'
        with self.assertRaises(मॉड्यूल_मोल.실행오류): self.पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.निर्माण_करचें_प्रवेश()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(मॉड्यूल_मोल.실행오류): self.पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        यंत्र = self.निर्माण_करचें_प्रवेश()
        यंत्र['VMState'] = 'poweroff'
        यंत्र['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(मॉड्यूल_मोल.실행오류): self.पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश()
        self.변경없음()

    def test_전환중거부(self):
        self.निर्माण_करचें_प्रवेश()['VMState'] = 'saving'
        with self.assertRaises(मॉड्यूल_मोल.실행오류): self.पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश()
        self.변경없음()

    def test_등록해제거부(self):
        self.निर्माण_करचें_प्रवेश()
        self.상자.가상기계들.clear()
        with self.assertRaises(मॉड्यूल_मोल.실행오류): self.पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        यंत्र = self.निर्माण_करचें_प्रवेश()
        यंत्र['VMState'] = 'poweroff'
        이전 = dict(यंत्र)
        self.상자.अपेस_मोल = 'make'
        with self.assertRaises(मॉड्यूल_मोल.실행오류): self.पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश()
        self.assertEqual(यंत्र, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.अपेस_मोल = 'setextradata'
        with self.assertRaises(मॉड्यूल_मोल.실행오류): self.पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश()
        self.상자.명령들.clear()
        self.assertEqual(self.पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश()['state'], 'running')
        self.assertFalse(any(आदेश[1] == 'createvm' for आदेश in self.상자.명령들))

    def test_보존ISO변조거부(self):
        यंत्र = self.निर्माण_करचें_प्रवेश()
        यंत्र['VMState'] = 'poweroff'
        Path(यंत्र['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(मॉड्यूल_मोल.실행오류): self.पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश()

    def test_상태미생성(self):
        self.assertEqual(self.पाळो_दिवचो_आदेश.शो_स्थिती()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for पाथ in ('../outside', '/tmp/outside'):
            with self.assertRaises(मॉड्यूल_मोल.실행오류): self.पाळो_दिवचो_आदेश.पाथ(पाथ)
        (self.रूट_मोल / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(मॉड्यूल_मोल.실행오류): self.पाळो_दिवचो_आदेश.पाथ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        मेजप = मॉड्यूल_मोल.खाशेलपण_मोल('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(मेजप['VMState'], 'running')
        self.assertEqual(मेजप['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
