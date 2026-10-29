import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Дефиниција_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
модул_VALUE = importlib.util.module_from_spec(Дефиниција_VALUE)
Дефиниција_VALUE.loader.exec_module(модул_VALUE)


class 가짜상자:
    def __init__(self, корен_VALUE):
        self.корен_VALUE = корен_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.неуспех_VALUE = None

    def __call__(self, Аргументи):
        Аргументи = list(map(str, Аргументи))
        self.명령들.append(Аргументи)
        if self.неуспех_VALUE == Аргументи[1] or (Аргументи[0] == 'make' and self.неуспех_VALUE == 'make'):
            self.неуспех_VALUE = None
            raise модул_VALUE.실행오류('시험용 неуспех_VALUE')
        if Аргументи[0] == 'make':
            ПАТЕКА = self.корен_VALUE / 'os/build/kernel.iso'
            ПАТЕКА.parent.mkdir(parents=True, exist_ok=True)
            ПАТЕКА.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Дејство = Аргументи[1]
        if Дејство == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Дејство == 'createvm':
            INDEX, Име = Аргументи[Аргументи.index('--uuid') + 1], Аргументи[Аргументи.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Име, 'VMState': 'poweroff',
                'CfgFile': str(self.корен_VALUE / '.vbox/machines' / Име / (Име + '.vbox')), 'owner': None}
            return ''
        машина = self.가상기계들[Аргументи[2]]
        if Дејство == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Име), json.dumps(VALUE)) for Име, VALUE in машина.items() if Име != 'owner')
        if Дејство == 'getextradata': return 'Value: ' + машина['owner'] if машина['owner'] else 'No value set!'
        if Дејство == 'setextradata': машина['owner'] = Аргументи[4]
        elif Дејство == 'storagectl': машина['storagecontrollername0'] = 'JKOROS IDE'
        elif Дејство == 'storageattach': машина['JKOROS IDE-0-0'] = Аргументи[Аргументи.index('--medium') + 1]
        elif Дејство == 'startvm': машина['VMState'] = 'running'
        elif Дејство == 'controlvm':
            assert Аргументи[3] == 'resume'
            машина['VMState'] = 'running'
        elif Дејство != 'modifyvm': raise AssertionError(Аргументи)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.корен_VALUE = Path(self.임시.name)
        (self.корен_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.корен_VALUE)
        self.Изврши_наредба = модул_VALUE.програма_стартувач(self.корен_VALUE, 'jkoros operating system', Команда=self.상자)

    def Create_внес(self):
        мерка = self.Изврши_наредба.Изврши_наредба()
        self.상자.명령들.clear()
        return self.상자.가상기계들[мерка['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Команда[0] == 'VBoxManage' and Команда[1] in ('list', 'showvminfo', 'getextradata') for Команда in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        мерка = self.Изврши_наредба.Изврши_наредба()
        self.assertEqual(мерка['state'], 'running')
        self.assertTrue(Path(мерка['iso']).is_file())
        self.assertTrue(any('--nic1' in Команда and 'none' in Команда for Команда in self.상자.명령들))
        self.assertFalse(any('hdd' in Команда or 'discardstate' in Команда or 'createmedium' in Команда for Команда in self.상자.명령들))

    def test_실행중유지(self):
        self.Create_внес()
        self.assertEqual(self.Изврши_наредба.Изврши_наредба()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        машина = self.Create_внес()
        машина['VMState'] = 'saved'
        LOG_VALUE = self.Изврши_наредба.ПАТЕКА(self.Изврши_наредба.Читај()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.Изврши_наредба.Изврши_наредба()
        self.assertFalse(any(Команда[0] == 'make' or Команда[1] == 'modifyvm' for Команда in self.상자.명령들))
        self.assertEqual([ПАТЕКА.read_text() for ПАТЕКА in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Create_внес()['VMState'] = 'paused'
        self.Изврши_наредба.Изврши_наредба()
        self.assertTrue(any(Команда[1] == 'controlvm' and Команда[3] == 'resume' for Команда in self.상자.명령들))
        self.assertFalse(any(Команда[0] == 'make' for Команда in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(модул_VALUE.실행오류): self.Изврши_наредба.Изврши_наредба()
        self.변경없음()

    def test_소유표식거부(self):
        self.Create_внес()['owner'] = 'someone-else'
        with self.assertRaises(модул_VALUE.실행오류): self.Изврши_наредба.Изврши_наредба()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Create_внес()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(модул_VALUE.실행오류): self.Изврши_наредба.Изврши_наредба()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        машина = self.Create_внес()
        машина['VMState'] = 'poweroff'
        машина['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(модул_VALUE.실행오류): self.Изврши_наредба.Изврши_наредба()
        self.변경없음()

    def test_전환중거부(self):
        self.Create_внес()['VMState'] = 'saving'
        with self.assertRaises(модул_VALUE.실행오류): self.Изврши_наредба.Изврши_наредба()
        self.변경없음()

    def test_등록해제거부(self):
        self.Create_внес()
        self.상자.가상기계들.clear()
        with self.assertRaises(модул_VALUE.실행오류): self.Изврши_наредба.Изврши_наредба()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        машина = self.Create_внес()
        машина['VMState'] = 'poweroff'
        이전 = dict(машина)
        self.상자.неуспех_VALUE = 'make'
        with self.assertRaises(модул_VALUE.실행오류): self.Изврши_наредба.Изврши_наредба()
        self.assertEqual(машина, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.неуспех_VALUE = 'setextradata'
        with self.assertRaises(модул_VALUE.실행오류): self.Изврши_наредба.Изврши_наредба()
        self.상자.명령들.clear()
        self.assertEqual(self.Изврши_наредба.Изврши_наредба()['state'], 'running')
        self.assertFalse(any(Команда[1] == 'createvm' for Команда in self.상자.명령들))

    def test_보존ISO변조거부(self):
        машина = self.Create_внес()
        машина['VMState'] = 'poweroff'
        Path(машина['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(модул_VALUE.실행오류): self.Изврши_наредба.Изврши_наредба()

    def test_상태미생성(self):
        self.assertEqual(self.Изврши_наредба.прикажи_статус()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ПАТЕКА in ('../outside', '/tmp/outside'):
            with self.assertRaises(модул_VALUE.실행오류): self.Изврши_наредба.ПАТЕКА(ПАТЕКА)
        (self.корен_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(модул_VALUE.실행오류): self.Изврши_наредба.ПАТЕКА('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        мерка = модул_VALUE.атрибут_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(мерка['VMState'], 'running')
        self.assertEqual(мерка['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
