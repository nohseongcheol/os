import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

განსაზღვრება_მნიშვნელობა = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
მოდული_მნიშვნელობა = importlib.util.module_from_spec(განსაზღვრება_მნიშვნელობა)
განსაზღვრება_მნიშვნელობა.loader.exec_module(მოდული_მნიშვნელობა)


class 가짜상자:
    def __init__(self, ფესვი_მნიშვნელობა):
        self.ფესვი_მნიშვნელობა = ფესვი_მნიშვნელობა
        self.명령들 = []
        self.가상기계들 = {}
        self.მარცხი_მნიშვნელობა = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.მარცხი_მნიშვნელობა == 인수[1] or (인수[0] == 'make' and self.მარცხი_მნიშვნელობა == 'make'):
            self.მარცხი_მნიშვნელობა = None
            raise მოდული_მნიშვნელობა.실행오류('시험용 მარცხი_მნიშვნელობა')
        if 인수[0] == 'make':
            გეზი = self.ფესვი_მნიშვნელობა / 'os/build/kernel.iso'
            გეზი.parent.mkdir(parents=True, exist_ok=True)
            გეზი.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        ქმედება = 인수[1]
        if ქმედება == 'list':
            return '\n'.join('"{}" {{{}}}'.format(მნიშვნელობა['name'], ინდექსი) for ინდექსი, მნიშვნელობა in self.가상기계들.items())
        if ქმედება == 'createvm':
            ინდექსი, სახელი = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[ინდექსი] = {'UUID': ინდექსი, 'name': სახელი, 'VMState': 'poweroff',
                'CfgFile': str(self.ფესვი_მნიშვნელობა / '.vbox/machines' / სახელი / (სახელი + '.vbox')), 'owner': None}
            return ''
        კომპიუტერი = self.가상기계들[인수[2]]
        if ქმედება == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(სახელი), json.dumps(მნიშვნელობა)) for სახელი, მნიშვნელობა in კომპიუტერი.items() if სახელი != 'owner')
        if ქმედება == 'getextradata': return 'Value: ' + კომპიუტერი['owner'] if კომპიუტერი['owner'] else 'No value set!'
        if ქმედება == 'setextradata': კომპიუტერი['owner'] = 인수[4]
        elif ქმედება == 'storagectl': კომპიუტერი['storagecontrollername0'] = 'JKOROS IDE'
        elif ქმედება == 'storageattach': კომპიუტერი['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif ქმედება == 'startvm': კომპიუტერი['VMState'] = 'running'
        elif ქმედება == 'controlvm':
            assert 인수[3] == 'resume'
            კომპიუტერი['VMState'] = 'running'
        elif ქმედება != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.ფესვი_მნიშვნელობა = Path(self.임시.name)
        (self.ფესვი_მნიშვნელობა / '.vbox').mkdir()
        self.상자 = 가짜상자(self.ფესვი_მნიშვნელობა)
        self.შესრულება_ბრძანება = მოდული_მნიშვნელობა.აპი_გამშვები(self.ფესვი_მნიშვნელობა, 'jkoros operating system', ბრძანება=self.상자)

    def შექმნა_შენატანი(self):
        გაზომვა = self.შესრულება_ბრძანება.შესრულება_ბრძანება()
        self.상자.명령들.clear()
        return self.상자.가상기계들[გაზომვა['uuid']]

    def 변경없음(self):
        self.assertTrue(all(ბრძანება[0] == 'VBoxManage' and ბრძანება[1] in ('list', 'showvminfo', 'getextradata') for ბრძანება in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        გაზომვა = self.შესრულება_ბრძანება.შესრულება_ბრძანება()
        self.assertEqual(გაზომვა['state'], 'running')
        self.assertTrue(Path(გაზომვა['iso']).is_file())
        self.assertTrue(any('--nic1' in ბრძანება and 'none' in ბრძანება for ბრძანება in self.상자.명령들))
        self.assertFalse(any('hdd' in ბრძანება or 'discardstate' in ბრძანება or 'createmedium' in ბრძანება for ბრძანება in self.상자.명령들))

    def test_실행중유지(self):
        self.შექმნა_შენატანი()
        self.assertEqual(self.შესრულება_ბრძანება.შესრულება_ბრძანება()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        კომპიუტერი = self.შექმნა_შენატანი()
        კომპიუტერი['VMState'] = 'saved'
        ჟურნალი_მნიშვნელობა = self.შესრულება_ბრძანება.გეზი(self.შესრულება_ბრძანება.კითხვა()['serial_log'])
        ჟურნალი_მნიშვნელობა.write_text('saved log')
        self.შესრულება_ბრძანება.შესრულება_ბრძანება()
        self.assertFalse(any(ბრძანება[0] == 'make' or ბრძანება[1] == 'modifyvm' for ბრძანება in self.상자.명령들))
        self.assertEqual([გეზი.read_text() for გეზი in ჟურნალი_მნიშვნელობა.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.შექმნა_შენატანი()['VMState'] = 'paused'
        self.შესრულება_ბრძანება.შესრულება_ბრძანება()
        self.assertTrue(any(ბრძანება[1] == 'controlvm' and ბრძანება[3] == 'resume' for ბრძანება in self.상자.명령들))
        self.assertFalse(any(ბრძანება[0] == 'make' for ბრძანება in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(მოდული_მნიშვნელობა.실행오류): self.შესრულება_ბრძანება.შესრულება_ბრძანება()
        self.변경없음()

    def test_소유표식거부(self):
        self.შექმნა_შენატანი()['owner'] = 'someone-else'
        with self.assertRaises(მოდული_მნიშვნელობა.실행오류): self.შესრულება_ბრძანება.შესრულება_ბრძანება()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.შექმნა_შენატანი()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(მოდული_მნიშვნელობა.실행오류): self.შესრულება_ბრძანება.შესრულება_ბრძანება()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        კომპიუტერი = self.შექმნა_შენატანი()
        კომპიუტერი['VMState'] = 'poweroff'
        კომპიუტერი['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(მოდული_მნიშვნელობა.실행오류): self.შესრულება_ბრძანება.შესრულება_ბრძანება()
        self.변경없음()

    def test_전환중거부(self):
        self.შექმნა_შენატანი()['VMState'] = 'saving'
        with self.assertRaises(მოდული_მნიშვნელობა.실행오류): self.შესრულება_ბრძანება.შესრულება_ბრძანება()
        self.변경없음()

    def test_등록해제거부(self):
        self.შექმნა_შენატანი()
        self.상자.가상기계들.clear()
        with self.assertRaises(მოდული_მნიშვნელობა.실행오류): self.შესრულება_ბრძანება.შესრულება_ბრძანება()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        კომპიუტერი = self.შექმნა_შენატანი()
        კომპიუტერი['VMState'] = 'poweroff'
        이전 = dict(კომპიუტერი)
        self.상자.მარცხი_მნიშვნელობა = 'make'
        with self.assertRaises(მოდული_მნიშვნელობა.실행오류): self.შესრულება_ბრძანება.შესრულება_ბრძანება()
        self.assertEqual(კომპიუტერი, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.მარცხი_მნიშვნელობა = 'setextradata'
        with self.assertRaises(მოდული_მნიშვნელობა.실행오류): self.შესრულება_ბრძანება.შესრულება_ბრძანება()
        self.상자.명령들.clear()
        self.assertEqual(self.შესრულება_ბრძანება.შესრულება_ბრძანება()['state'], 'running')
        self.assertFalse(any(ბრძანება[1] == 'createvm' for ბრძანება in self.상자.명령들))

    def test_보존ISO변조거부(self):
        კომპიუტერი = self.შექმნა_შენატანი()
        კომპიუტერი['VMState'] = 'poweroff'
        Path(კომპიუტერი['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(მოდული_მნიშვნელობა.실행오류): self.შესრულება_ბრძანება.შესრულება_ბრძანება()

    def test_상태미생성(self):
        self.assertEqual(self.შესრულება_ბრძანება.ჩვენება_სტატუსი()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for გეზი in ('../outside', '/tmp/outside'):
            with self.assertRaises(მოდული_მნიშვნელობა.실행오류): self.შესრულება_ბრძანება.გეზი(გეზი)
        (self.ფესვი_მნიშვნელობა / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(მოდული_მნიშვნელობა.실행오류): self.შესრულება_ბრძანება.გეზი('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        გაზომვა = მოდული_მნიშვნელობა.ატრიბუტი_მნიშვნელობა('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(გაზომვა['VMState'], 'running')
        self.assertEqual(გაზომვა['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
