import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Анықтама_мән = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
модуль_мән = importlib.util.module_from_spec(Анықтама_мән)
Анықтама_мән.loader.exec_module(модуль_мән)


class 가짜상자:
    def __init__(self, түбір_мән):
        self.түбір_мән = түбір_мән
        self.명령들 = []
        self.가상기계들 = {}
        self.қате_мән = None

    def __call__(self, Аргументтер):
        Аргументтер = list(map(str, Аргументтер))
        self.명령들.append(Аргументтер)
        if self.қате_мән == Аргументтер[1] or (Аргументтер[0] == 'make' and self.қате_мән == 'make'):
            self.қате_мән = None
            raise модуль_мән.실행오류('시험용 қате_мән')
        if Аргументтер[0] == 'make':
            Жол_2 = self.түбір_мән / 'os/build/kernel.iso'
            Жол_2.parent.mkdir(parents=True, exist_ok=True)
            Жол_2.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Әрекет = Аргументтер[1]
        if Әрекет == 'list':
            return '\n'.join('"{}" {{{}}}'.format(мән['name'], индекс) for индекс, мән in self.가상기계들.items())
        if Әрекет == 'createvm':
            индекс, Аты = Аргументтер[Аргументтер.index('--uuid') + 1], Аргументтер[Аргументтер.index('--name') + 1]
            self.가상기계들[индекс] = {'UUID': индекс, 'name': Аты, 'VMState': 'poweroff',
                'CfgFile': str(self.түбір_мән / '.vbox/machines' / Аты / (Аты + '.vbox')), 'owner': None}
            return ''
        компьютер = self.가상기계들[Аргументтер[2]]
        if Әрекет == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Аты), json.dumps(мән)) for Аты, мән in компьютер.items() if Аты != 'owner')
        if Әрекет == 'getextradata': return 'Value: ' + компьютер['owner'] if компьютер['owner'] else 'No value set!'
        if Әрекет == 'setextradata': компьютер['owner'] = Аргументтер[4]
        elif Әрекет == 'storagectl': компьютер['storagecontrollername0'] = 'JKOROS IDE'
        elif Әрекет == 'storageattach': компьютер['JKOROS IDE-0-0'] = Аргументтер[Аргументтер.index('--medium') + 1]
        elif Әрекет == 'startvm': компьютер['VMState'] = 'running'
        elif Әрекет == 'controlvm':
            assert Аргументтер[3] == 'resume'
            компьютер['VMState'] = 'running'
        elif Әрекет != 'modifyvm': raise AssertionError(Аргументтер)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.түбір_мән = Path(self.임시.name)
        (self.түбір_мән / '.vbox').mkdir()
        self.상자 = 가짜상자(self.түбір_мән)
        self.орындау_пәрмен = модуль_мән.бағдарлама_іске_қосу_құралы(self.түбір_мән, 'jkoros operating system', Команда=self.상자)

    def жасау_енгізу(self):
        НӘТИЖЕ = self.орындау_пәрмен.орындау_пәрмен()
        self.상자.명령들.clear()
        return self.상자.가상기계들[НӘТИЖЕ['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Команда[0] == 'VBoxManage' and Команда[1] in ('list', 'showvminfo', 'getextradata') for Команда in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        НӘТИЖЕ = self.орындау_пәрмен.орындау_пәрмен()
        self.assertEqual(НӘТИЖЕ['state'], 'running')
        self.assertTrue(Path(НӘТИЖЕ['iso']).is_file())
        self.assertTrue(any('--nic1' in Команда and 'none' in Команда for Команда in self.상자.명령들))
        self.assertFalse(any('hdd' in Команда or 'discardstate' in Команда or 'createmedium' in Команда for Команда in self.상자.명령들))

    def test_실행중유지(self):
        self.жасау_енгізу()
        self.assertEqual(self.орындау_пәрмен.орындау_пәрмен()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        компьютер = self.жасау_енгізу()
        компьютер['VMState'] = 'saved'
        журнал_мән = self.орындау_пәрмен.Жол_2(self.орындау_пәрмен.Оқу()['serial_log'])
        журнал_мән.write_text('saved log')
        self.орындау_пәрмен.орындау_пәрмен()
        self.assertFalse(any(Команда[0] == 'make' or Команда[1] == 'modifyvm' for Команда in self.상자.명령들))
        self.assertEqual([Жол_2.read_text() for Жол_2 in журнал_мән.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.жасау_енгізу()['VMState'] = 'paused'
        self.орындау_пәрмен.орындау_пәрмен()
        self.assertTrue(any(Команда[1] == 'controlvm' and Команда[3] == 'resume' for Команда in self.상자.명령들))
        self.assertFalse(any(Команда[0] == 'make' for Команда in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(модуль_мән.실행오류): self.орындау_пәрмен.орындау_пәрмен()
        self.변경없음()

    def test_소유표식거부(self):
        self.жасау_енгізу()['owner'] = 'someone-else'
        with self.assertRaises(модуль_мән.실행오류): self.орындау_пәрмен.орындау_пәрмен()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.жасау_енгізу()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(модуль_мән.실행오류): self.орындау_пәрмен.орындау_пәрмен()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        компьютер = self.жасау_енгізу()
        компьютер['VMState'] = 'poweroff'
        компьютер['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(модуль_мән.실행오류): self.орындау_пәрмен.орындау_пәрмен()
        self.변경없음()

    def test_전환중거부(self):
        self.жасау_енгізу()['VMState'] = 'saving'
        with self.assertRaises(модуль_мән.실행오류): self.орындау_пәрмен.орындау_пәрмен()
        self.변경없음()

    def test_등록해제거부(self):
        self.жасау_енгізу()
        self.상자.가상기계들.clear()
        with self.assertRaises(модуль_мән.실행오류): self.орындау_пәрмен.орындау_пәрмен()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        компьютер = self.жасау_енгізу()
        компьютер['VMState'] = 'poweroff'
        이전 = dict(компьютер)
        self.상자.қате_мән = 'make'
        with self.assertRaises(модуль_мән.실행오류): self.орындау_пәрмен.орындау_пәрмен()
        self.assertEqual(компьютер, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.қате_мән = 'setextradata'
        with self.assertRaises(модуль_мән.실행오류): self.орындау_пәрмен.орындау_пәрмен()
        self.상자.명령들.clear()
        self.assertEqual(self.орындау_пәрмен.орындау_пәрмен()['state'], 'running')
        self.assertFalse(any(Команда[1] == 'createvm' for Команда in self.상자.명령들))

    def test_보존ISO변조거부(self):
        компьютер = self.жасау_енгізу()
        компьютер['VMState'] = 'poweroff'
        Path(компьютер['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(модуль_мән.실행오류): self.орындау_пәрмен.орындау_пәрмен()

    def test_상태미생성(self):
        self.assertEqual(self.орындау_пәрмен.көрсету_күй()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Жол_2 in ('../outside', '/tmp/outside'):
            with self.assertRaises(модуль_мән.실행오류): self.орындау_пәрмен.Жол_2(Жол_2)
        (self.түбір_мән / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(модуль_мән.실행오류): self.орындау_пәрмен.Жол_2('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        НӘТИЖЕ = модуль_мән.атрибут_мән('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(НӘТИЖЕ['VMState'], 'running')
        self.assertEqual(НӘТИЖЕ['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
