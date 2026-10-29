import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

정의 = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(정의)
정의.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.неуспјех_вриједност = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.неуспјех_вриједност == 인수[1] or (인수[0] == 'make' and self.неуспјех_вриједност == 'make'):
            self.неуспјех_вриједност = None
            raise 모듈.실행오류('시험용 неуспјех_вриједност')
        if 인수[0] == 'make':
            пут = self.뿌리 / 'os/build/kernel.iso'
            пут.parent.mkdir(parents=True, exist_ok=True)
            пут.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        радња = 인수[1]
        if радња == 'list':
            return '\n'.join('"{}" {{{}}}'.format(вриједност['name'], индекс) for индекс, вриједност in self.가상기계들.items())
        if радња == 'createvm':
            индекс, назив = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[индекс] = {'UUID': индекс, 'name': назив, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / назив / (назив + '.vbox')), 'owner': None}
            return ''
        기계 = self.가상기계들[인수[2]]
        if радња == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(назив), json.dumps(вриједност)) for назив, вриједност in 기계.items() if назив != 'owner')
        if радња == 'getextradata': return 'Value: ' + 기계['owner'] if 기계['owner'] else 'No value set!'
        if радња == 'setextradata': 기계['owner'] = 인수[4]
        elif радња == 'storagectl': 기계['storagecontrollername0'] = 'JKOROS IDE'
        elif радња == 'storageattach': 기계['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif радња == 'startvm': 기계['VMState'] = 'running'
        elif радња == 'controlvm':
            assert 인수[3] == 'resume'
            기계['VMState'] = 'running'
        elif радња != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.실행 = 모듈.실행기(self.뿌리, 'jkoros operating system', команда=self.상자)

    def 만들기(self):
        결과 = self.실행.실행()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(команда[0] == 'VBoxManage' and команда[1] in ('list', 'showvminfo', 'getextradata') for команда in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.실행.실행()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in команда and 'none' in команда for команда in self.상자.명령들))
        self.assertFalse(any('hdd' in команда or 'discardstate' in команда or 'createmedium' in команда for команда in self.상자.명령들))

    def test_실행중유지(self):
        self.만들기()
        self.assertEqual(self.실행.실행()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        기계 = self.만들기()
        기계['VMState'] = 'saved'
        дневник_рада_вриједност = self.실행.пут(self.실행.읽기()['serial_log'])
        дневник_рада_вриједност.write_text('saved log')
        self.실행.실행()
        self.assertFalse(any(команда[0] == 'make' or команда[1] == 'modifyvm' for команда in self.상자.명령들))
        self.assertEqual([пут.read_text() for пут in дневник_рада_вриједност.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.만들기()['VMState'] = 'paused'
        self.실행.실행()
        self.assertTrue(any(команда[1] == 'controlvm' and команда[3] == 'resume' for команда in self.상자.명령들))
        self.assertFalse(any(команда[0] == 'make' for команда in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_소유표식거부(self):
        self.만들기()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.만들기()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        기계 = self.만들기()
        기계['VMState'] = 'poweroff'
        기계['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_전환중거부(self):
        self.만들기()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_등록해제거부(self):
        self.만들기()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        기계 = self.만들기()
        기계['VMState'] = 'poweroff'
        이전 = dict(기계)
        self.상자.неуспјех_вриједност = 'make'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.assertEqual(기계, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.неуспјех_вриједност = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.상자.명령들.clear()
        self.assertEqual(self.실행.실행()['state'], 'running')
        self.assertFalse(any(команда[1] == 'createvm' for команда in self.상자.명령들))

    def test_보존ISO변조거부(self):
        기계 = self.만들기()
        기계['VMState'] = 'poweroff'
        Path(기계['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.실행.실행()

    def test_상태미생성(self):
        self.assertEqual(self.실행.приказати_стање()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for пут in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.실행.пут(пут)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.실행.пут('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.атрибут_вриједност('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
