import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Аныктама_маани = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(Аныктама_маани)
Аныктама_маани.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.натыйжасыз_маани = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.натыйжасыз_маани == 인수[1] or (인수[0] == 'make' and self.натыйжасыз_маани == 'make'):
            self.натыйжасыз_маани = None
            raise 모듈.실행오류('시험용 натыйжасыз_маани')
        if 인수[0] == 'make':
            ЖОЛ = self.뿌리 / 'os/build/kernel.iso'
            ЖОЛ.parent.mkdir(parents=True, exist_ok=True)
            ЖОЛ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Аракети = 인수[1]
        if Аракети == 'list':
            return '\n'.join('"{}" {{{}}}'.format(маани['name'], индекс) for индекс, маани in self.가상기계들.items())
        if Аракети == 'createvm':
            индекс, Аты = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[индекс] = {'UUID': индекс, 'name': Аты, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Аты / (Аты + '.vbox')), 'owner': None}
            return ''
        машина = self.가상기계들[인수[2]]
        if Аракети == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Аты), json.dumps(маани)) for Аты, маани in машина.items() if Аты != 'owner')
        if Аракети == 'getextradata': return 'Value: ' + машина['owner'] if машина['owner'] else 'No value set!'
        if Аракети == 'setextradata': машина['owner'] = 인수[4]
        elif Аракети == 'storagectl': машина['storagecontrollername0'] = 'JKOROS IDE'
        elif Аракети == 'storageattach': машина['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Аракети == 'startvm': машина['VMState'] = 'running'
        elif Аракети == 'controlvm':
            assert 인수[3] == 'resume'
            машина['VMState'] = 'running'
        elif Аракети != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.аткаруу_буйрук = 모듈.програм_жаратма_тарткычы(self.뿌리, 'jkoros operating system', Команда=self.상자)

    def түзүү_киргизме_жазуу(self):
        결과 = self.аткаруу_буйрук.аткаруу_буйрук()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Команда[0] == 'VBoxManage' and Команда[1] in ('list', 'showvminfo', 'getextradata') for Команда in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.аткаруу_буйрук.аткаруу_буйрук()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in Команда and 'none' in Команда for Команда in self.상자.명령들))
        self.assertFalse(any('hdd' in Команда or 'discardstate' in Команда or 'createmedium' in Команда for Команда in self.상자.명령들))

    def test_실행중유지(self):
        self.түзүү_киргизме_жазуу()
        self.assertEqual(self.аткаруу_буйрук.аткаруу_буйрук()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        машина = self.түзүү_киргизме_жазуу()
        машина['VMState'] = 'saved'
        жазуу_маани = self.аткаруу_буйрук.ЖОЛ(self.аткаруу_буйрук.Окуу()['serial_log'])
        жазуу_маани.write_text('saved log')
        self.аткаруу_буйрук.аткаруу_буйрук()
        self.assertFalse(any(Команда[0] == 'make' or Команда[1] == 'modifyvm' for Команда in self.상자.명령들))
        self.assertEqual([ЖОЛ.read_text() for ЖОЛ in жазуу_маани.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.түзүү_киргизме_жазуу()['VMState'] = 'paused'
        self.аткаруу_буйрук.аткаруу_буйрук()
        self.assertTrue(any(Команда[1] == 'controlvm' and Команда[3] == 'resume' for Команда in self.상자.명령들))
        self.assertFalse(any(Команда[0] == 'make' for Команда in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.аткаруу_буйрук.аткаруу_буйрук()
        self.변경없음()

    def test_소유표식거부(self):
        self.түзүү_киргизме_жазуу()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.аткаруу_буйрук.аткаруу_буйрук()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.түзүү_киргизме_жазуу()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.аткаруу_буйрук.аткаруу_буйрук()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        машина = self.түзүү_киргизме_жазуу()
        машина['VMState'] = 'poweroff'
        машина['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.аткаруу_буйрук.аткаруу_буйрук()
        self.변경없음()

    def test_전환중거부(self):
        self.түзүү_киргизме_жазуу()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.аткаруу_буйрук.аткаруу_буйрук()
        self.변경없음()

    def test_등록해제거부(self):
        self.түзүү_киргизме_жазуу()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.аткаруу_буйрук.аткаруу_буйрук()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        машина = self.түзүү_киргизме_жазуу()
        машина['VMState'] = 'poweroff'
        이전 = dict(машина)
        self.상자.натыйжасыз_маани = 'make'
        with self.assertRaises(모듈.실행오류): self.аткаруу_буйрук.аткаруу_буйрук()
        self.assertEqual(машина, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.натыйжасыз_маани = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.аткаруу_буйрук.аткаруу_буйрук()
        self.상자.명령들.clear()
        self.assertEqual(self.аткаруу_буйрук.аткаруу_буйрук()['state'], 'running')
        self.assertFalse(any(Команда[1] == 'createvm' for Команда in self.상자.명령들))

    def test_보존ISO변조거부(self):
        машина = self.түзүү_киргизме_жазуу()
        машина['VMState'] = 'poweroff'
        Path(машина['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.аткаруу_буйрук.аткаруу_буйрук()

    def test_상태미생성(self):
        self.assertEqual(self.аткаруу_буйрук.көрсөтүү_абал()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ЖОЛ in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.аткаруу_буйрук.ЖОЛ(ЖОЛ)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.аткаруу_буйрук.ЖОЛ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.атрибут_маани('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
