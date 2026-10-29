import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Дефиниция_стойност = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
модул_стойност = importlib.util.module_from_spec(Дефиниция_стойност)
Дефиниция_стойност.loader.exec_module(модул_стойност)


class 가짜상자:
    def __init__(self, корен_стойност):
        self.корен_стойност = корен_стойност
        self.명령들 = []
        self.가상기계들 = {}
        self.отказ_стойност = None

    def __call__(self, Параметри):
        Параметри = list(map(str, Параметри))
        self.명령들.append(Параметри)
        if self.отказ_стойност == Параметри[1] or (Параметри[0] == 'make' and self.отказ_стойност == 'make'):
            self.отказ_стойност = None
            raise модул_стойност.실행오류('시험용 отказ_стойност')
        if Параметри[0] == 'make':
            ПЪТ = self.корен_стойност / 'os/build/kernel.iso'
            ПЪТ.parent.mkdir(parents=True, exist_ok=True)
            ПЪТ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Операция = Параметри[1]
        if Операция == 'list':
            return '\n'.join('"{}" {{{}}}'.format(стойност['name'], индекс) for индекс, стойност in self.가상기계들.items())
        if Операция == 'createvm':
            индекс, Име = Параметри[Параметри.index('--uuid') + 1], Параметри[Параметри.index('--name') + 1]
            self.가상기계들[индекс] = {'UUID': индекс, 'name': Име, 'VMState': 'poweroff',
                'CfgFile': str(self.корен_стойност / '.vbox/machines' / Име / (Име + '.vbox')), 'owner': None}
            return ''
        машина = self.가상기계들[Параметри[2]]
        if Операция == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Име), json.dumps(стойност)) for Име, стойност in машина.items() if Име != 'owner')
        if Операция == 'getextradata': return 'Value: ' + машина['owner'] if машина['owner'] else 'No value set!'
        if Операция == 'setextradata': машина['owner'] = Параметри[4]
        elif Операция == 'storagectl': машина['storagecontrollername0'] = 'JKOROS IDE'
        elif Операция == 'storageattach': машина['JKOROS IDE-0-0'] = Параметри[Параметри.index('--medium') + 1]
        elif Операция == 'startvm': машина['VMState'] = 'running'
        elif Операция == 'controlvm':
            assert Параметри[3] == 'resume'
            машина['VMState'] = 'running'
        elif Операция != 'modifyvm': raise AssertionError(Параметри)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.корен_стойност = Path(self.임시.name)
        (self.корен_стойност / '.vbox').mkdir()
        self.상자 = 가짜상자(self.корен_стойност)
        self.изпълнявам_команда = модул_стойност.програма_програма_за_стартиране(self.корен_стойност, 'jkoros operating system', Команда=self.상자)

    def Създаване_запис(self):
        РЕЗУЛТАТ = self.изпълнявам_команда.изпълнявам_команда()
        self.상자.명령들.clear()
        return self.상자.가상기계들[РЕЗУЛТАТ['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Команда[0] == 'VBoxManage' and Команда[1] in ('list', 'showvminfo', 'getextradata') for Команда in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        РЕЗУЛТАТ = self.изпълнявам_команда.изпълнявам_команда()
        self.assertEqual(РЕЗУЛТАТ['state'], 'running')
        self.assertTrue(Path(РЕЗУЛТАТ['iso']).is_file())
        self.assertTrue(any('--nic1' in Команда and 'none' in Команда for Команда in self.상자.명령들))
        self.assertFalse(any('hdd' in Команда or 'discardstate' in Команда or 'createmedium' in Команда for Команда in self.상자.명령들))

    def test_실행중유지(self):
        self.Създаване_запис()
        self.assertEqual(self.изпълнявам_команда.изпълнявам_команда()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        машина = self.Създаване_запис()
        машина['VMState'] = 'saved'
        регистрирам_стойност = self.изпълнявам_команда.ПЪТ(self.изпълнявам_команда.Четене()['serial_log'])
        регистрирам_стойност.write_text('saved log')
        self.изпълнявам_команда.изпълнявам_команда()
        self.assertFalse(any(Команда[0] == 'make' or Команда[1] == 'modifyvm' for Команда in self.상자.명령들))
        self.assertEqual([ПЪТ.read_text() for ПЪТ in регистрирам_стойност.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Създаване_запис()['VMState'] = 'paused'
        self.изпълнявам_команда.изпълнявам_команда()
        self.assertTrue(any(Команда[1] == 'controlvm' and Команда[3] == 'resume' for Команда in self.상자.명령들))
        self.assertFalse(any(Команда[0] == 'make' for Команда in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(модул_стойност.실행오류): self.изпълнявам_команда.изпълнявам_команда()
        self.변경없음()

    def test_소유표식거부(self):
        self.Създаване_запис()['owner'] = 'someone-else'
        with self.assertRaises(модул_стойност.실행오류): self.изпълнявам_команда.изпълнявам_команда()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Създаване_запис()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(модул_стойност.실행오류): self.изпълнявам_команда.изпълнявам_команда()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        машина = self.Създаване_запис()
        машина['VMState'] = 'poweroff'
        машина['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(модул_стойност.실행오류): self.изпълнявам_команда.изпълнявам_команда()
        self.변경없음()

    def test_전환중거부(self):
        self.Създаване_запис()['VMState'] = 'saving'
        with self.assertRaises(модул_стойност.실행오류): self.изпълнявам_команда.изпълнявам_команда()
        self.변경없음()

    def test_등록해제거부(self):
        self.Създаване_запис()
        self.상자.가상기계들.clear()
        with self.assertRaises(модул_стойност.실행오류): self.изпълнявам_команда.изпълнявам_команда()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        машина = self.Създаване_запис()
        машина['VMState'] = 'poweroff'
        이전 = dict(машина)
        self.상자.отказ_стойност = 'make'
        with self.assertRaises(модул_стойност.실행오류): self.изпълнявам_команда.изпълнявам_команда()
        self.assertEqual(машина, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.отказ_стойност = 'setextradata'
        with self.assertRaises(модул_стойност.실행오류): self.изпълнявам_команда.изпълнявам_команда()
        self.상자.명령들.clear()
        self.assertEqual(self.изпълнявам_команда.изпълнявам_команда()['state'], 'running')
        self.assertFalse(any(Команда[1] == 'createvm' for Команда in self.상자.명령들))

    def test_보존ISO변조거부(self):
        машина = self.Създаване_запис()
        машина['VMState'] = 'poweroff'
        Path(машина['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(модул_стойност.실행오류): self.изпълнявам_команда.изпълнявам_команда()

    def test_상태미생성(self):
        self.assertEqual(self.изпълнявам_команда.показвам_Състояние()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ПЪТ in ('../outside', '/tmp/outside'):
            with self.assertRaises(модул_стойност.실행오류): self.изпълнявам_команда.ПЪТ(ПЪТ)
        (self.корен_стойност / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(модул_стойност.실행오류): self.изпълнявам_команда.ПЪТ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        РЕЗУЛТАТ = модул_стойност.атрибут_стойност('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(РЕЗУЛТАТ['VMState'], 'running')
        self.assertEqual(РЕЗУЛТАТ['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
