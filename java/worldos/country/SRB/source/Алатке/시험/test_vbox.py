import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Дефиниција_вриједност = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
модул_вриједност = importlib.util.module_from_spec(Дефиниција_вриједност)
Дефиниција_вриједност.loader.exec_module(модул_вриједност)


class 가짜상자:
    def __init__(self, корен_вриједност):
        self.корен_вриједност = корен_вриједност
        self.명령들 = []
        self.가상기계들 = {}
        self.неуспјех_вриједност = None

    def __call__(self, Аргументи):
        Аргументи = list(map(str, Аргументи))
        self.명령들.append(Аргументи)
        if self.неуспјех_вриједност == Аргументи[1] or (Аргументи[0] == 'make' and self.неуспјех_вриједност == 'make'):
            self.неуспјех_вриједност = None
            raise модул_вриједност.실행오류('시험용 неуспјех_вриједност')
        if Аргументи[0] == 'make':
            ПУТАЊА = self.корен_вриједност / 'os/build/kernel.iso'
            ПУТАЊА.parent.mkdir(parents=True, exist_ok=True)
            ПУТАЊА.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        радња = Аргументи[1]
        if радња == 'list':
            return '\n'.join('"{}" {{{}}}'.format(вриједност['name'], индекс) for индекс, вриједност in self.가상기계들.items())
        if радња == 'createvm':
            индекс, Назив = Аргументи[Аргументи.index('--uuid') + 1], Аргументи[Аргументи.index('--name') + 1]
            self.가상기계들[индекс] = {'UUID': индекс, 'name': Назив, 'VMState': 'poweroff',
                'CfgFile': str(self.корен_вриједност / '.vbox/machines' / Назив / (Назив + '.vbox')), 'owner': None}
            return ''
        рачунар = self.가상기계들[Аргументи[2]]
        if радња == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Назив), json.dumps(вриједност)) for Назив, вриједност in рачунар.items() if Назив != 'owner')
        if радња == 'getextradata': return 'Value: ' + рачунар['owner'] if рачунар['owner'] else 'No value set!'
        if радња == 'setextradata': рачунар['owner'] = Аргументи[4]
        elif радња == 'storagectl': рачунар['storagecontrollername0'] = 'JKOROS IDE'
        elif радња == 'storageattach': рачунар['JKOROS IDE-0-0'] = Аргументи[Аргументи.index('--medium') + 1]
        elif радња == 'startvm': рачунар['VMState'] = 'running'
        elif радња == 'controlvm':
            assert Аргументи[3] == 'resume'
            рачунар['VMState'] = 'running'
        elif радња != 'modifyvm': raise AssertionError(Аргументи)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.корен_вриједност = Path(self.임시.name)
        (self.корен_вриједност / '.vbox').mkdir()
        self.상자 = 가짜상자(self.корен_вриједност)
        self.Изврши_команда = модул_вриједност.програм_покретач(self.корен_вриједност, 'jkoros operating system', Наредба=self.상자)

    def Направи_унос(self):
        ИСХОД = self.Изврши_команда.Изврши_команда()
        self.상자.명령들.clear()
        return self.상자.가상기계들[ИСХОД['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Наредба[0] == 'VBoxManage' and Наредба[1] in ('list', 'showvminfo', 'getextradata') for Наредба in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        ИСХОД = self.Изврши_команда.Изврши_команда()
        self.assertEqual(ИСХОД['state'], 'running')
        self.assertTrue(Path(ИСХОД['iso']).is_file())
        self.assertTrue(any('--nic1' in Наредба and 'none' in Наредба for Наредба in self.상자.명령들))
        self.assertFalse(any('hdd' in Наредба or 'discardstate' in Наредба or 'createmedium' in Наредба for Наредба in self.상자.명령들))

    def test_실행중유지(self):
        self.Направи_унос()
        self.assertEqual(self.Изврши_команда.Изврши_команда()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        рачунар = self.Направи_унос()
        рачунар['VMState'] = 'saved'
        евиденција_вриједност = self.Изврши_команда.ПУТАЊА(self.Изврши_команда.Чита()['serial_log'])
        евиденција_вриједност.write_text('saved log')
        self.Изврши_команда.Изврши_команда()
        self.assertFalse(any(Наредба[0] == 'make' or Наредба[1] == 'modifyvm' for Наредба in self.상자.명령들))
        self.assertEqual([ПУТАЊА.read_text() for ПУТАЊА in евиденција_вриједност.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Направи_унос()['VMState'] = 'paused'
        self.Изврши_команда.Изврши_команда()
        self.assertTrue(any(Наредба[1] == 'controlvm' and Наредба[3] == 'resume' for Наредба in self.상자.명령들))
        self.assertFalse(any(Наредба[0] == 'make' for Наредба in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(модул_вриједност.실행오류): self.Изврши_команда.Изврши_команда()
        self.변경없음()

    def test_소유표식거부(self):
        self.Направи_унос()['owner'] = 'someone-else'
        with self.assertRaises(модул_вриједност.실행오류): self.Изврши_команда.Изврши_команда()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Направи_унос()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(модул_вриједност.실행오류): self.Изврши_команда.Изврши_команда()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        рачунар = self.Направи_унос()
        рачунар['VMState'] = 'poweroff'
        рачунар['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(модул_вриједност.실행오류): self.Изврши_команда.Изврши_команда()
        self.변경없음()

    def test_전환중거부(self):
        self.Направи_унос()['VMState'] = 'saving'
        with self.assertRaises(модул_вриједност.실행오류): self.Изврши_команда.Изврши_команда()
        self.변경없음()

    def test_등록해제거부(self):
        self.Направи_унос()
        self.상자.가상기계들.clear()
        with self.assertRaises(модул_вриједност.실행오류): self.Изврши_команда.Изврши_команда()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        рачунар = self.Направи_унос()
        рачунар['VMState'] = 'poweroff'
        이전 = dict(рачунар)
        self.상자.неуспјех_вриједност = 'make'
        with self.assertRaises(модул_вриједност.실행오류): self.Изврши_команда.Изврши_команда()
        self.assertEqual(рачунар, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.неуспјех_вриједност = 'setextradata'
        with self.assertRaises(модул_вриједност.실행오류): self.Изврши_команда.Изврши_команда()
        self.상자.명령들.clear()
        self.assertEqual(self.Изврши_команда.Изврши_команда()['state'], 'running')
        self.assertFalse(any(Наредба[1] == 'createvm' for Наредба in self.상자.명령들))

    def test_보존ISO변조거부(self):
        рачунар = self.Направи_унос()
        рачунар['VMState'] = 'poweroff'
        Path(рачунар['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(модул_вриједност.실행오류): self.Изврши_команда.Изврши_команда()

    def test_상태미생성(self):
        self.assertEqual(self.Изврши_команда.емисија_стање()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ПУТАЊА in ('../outside', '/tmp/outside'):
            with self.assertRaises(модул_вриједност.실행오류): self.Изврши_команда.ПУТАЊА(ПУТАЊА)
        (self.корен_вриједност / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(модул_вриједност.실행오류): self.Изврши_команда.ПУТАЊА('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        ИСХОД = модул_вриједност.атрибут_вриједност('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(ИСХОД['VMState'], 'running')
        self.assertEqual(ИСХОД['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
