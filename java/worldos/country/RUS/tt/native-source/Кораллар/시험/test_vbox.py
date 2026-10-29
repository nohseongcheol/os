import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Билгеләмә_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
модуль_VALUE = importlib.util.module_from_spec(Билгеләмә_VALUE)
Билгеләмә_VALUE.loader.exec_module(модуль_VALUE)


class 가짜상자:
    def __init__(self, тамыр_VALUE):
        self.тамыр_VALUE = тамыр_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.эштән_туктау_VALUE = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.эштән_туктау_VALUE == 인수[1] or (인수[0] == 'make' and self.эштән_туктау_VALUE == 'make'):
            self.эштән_туктау_VALUE = None
            raise модуль_VALUE.실행오류('시험용 эштән_туктау_VALUE')
        if 인수[0] == 'make':
            Yul = self.тамыр_VALUE / 'os/build/kernel.iso'
            Yul.parent.mkdir(parents=True, exist_ok=True)
            Yul.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Гамәл = 인수[1]
        if Гамәл == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Гамәл == 'createvm':
            INDEX, исем = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': исем, 'VMState': 'poweroff',
                'CfgFile': str(self.тамыр_VALUE / '.vbox/machines' / исем / (исем + '.vbox')), 'owner': None}
            return ''
        машина = self.가상기계들[인수[2]]
        if Гамәл == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(исем), json.dumps(VALUE)) for исем, VALUE in машина.items() if исем != 'owner')
        if Гамәл == 'getextradata': return 'Value: ' + машина['owner'] if машина['owner'] else 'No value set!'
        if Гамәл == 'setextradata': машина['owner'] = 인수[4]
        elif Гамәл == 'storagectl': машина['storagecontrollername0'] = 'JKOROS IDE'
        elif Гамәл == 'storageattach': машина['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Гамәл == 'startvm': машина['VMState'] = 'running'
        elif Гамәл == 'controlvm':
            assert 인수[3] == 'resume'
            машина['VMState'] = 'running'
        elif Гамәл != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.тамыр_VALUE = Path(self.임시.name)
        (self.тамыр_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.тамыр_VALUE)
        self.үтәргә_команда = модуль_VALUE.кушымта_хезмәткәр(self.тамыр_VALUE, 'jkoros operating system', команда=self.상자)

    def Төзү_кертү(self):
        үлчәм = self.үтәргә_команда.үтәргә_команда()
        self.상자.명령들.clear()
        return self.상자.가상기계들[үлчәм['uuid']]

    def 변경없음(self):
        self.assertTrue(all(команда[0] == 'VBoxManage' and команда[1] in ('list', 'showvminfo', 'getextradata') for команда in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        үлчәм = self.үтәргә_команда.үтәргә_команда()
        self.assertEqual(үлчәм['state'], 'running')
        self.assertTrue(Path(үлчәм['iso']).is_file())
        self.assertTrue(any('--nic1' in команда and 'none' in команда for команда in self.상자.명령들))
        self.assertFalse(any('hdd' in команда or 'discardstate' in команда or 'createmedium' in команда for команда in self.상자.명령들))

    def test_실행중유지(self):
        self.Төзү_кертү()
        self.assertEqual(self.үтәргә_команда.үтәргә_команда()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        машина = self.Төзү_кертү()
        машина['VMState'] = 'saved'
        LOG_VALUE = self.үтәргә_команда.Yul(self.үтәргә_команда.읽기()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.үтәргә_команда.үтәргә_команда()
        self.assertFalse(any(команда[0] == 'make' or команда[1] == 'modifyvm' for команда in self.상자.명령들))
        self.assertEqual([Yul.read_text() for Yul in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Төзү_кертү()['VMState'] = 'paused'
        self.үтәргә_команда.үтәргә_команда()
        self.assertTrue(any(команда[1] == 'controlvm' and команда[3] == 'resume' for команда in self.상자.명령들))
        self.assertFalse(any(команда[0] == 'make' for команда in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(модуль_VALUE.실행오류): self.үтәргә_команда.үтәргә_команда()
        self.변경없음()

    def test_소유표식거부(self):
        self.Төзү_кертү()['owner'] = 'someone-else'
        with self.assertRaises(модуль_VALUE.실행오류): self.үтәргә_команда.үтәргә_команда()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Төзү_кертү()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(модуль_VALUE.실행오류): self.үтәргә_команда.үтәргә_команда()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        машина = self.Төзү_кертү()
        машина['VMState'] = 'poweroff'
        машина['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(модуль_VALUE.실행오류): self.үтәргә_команда.үтәргә_команда()
        self.변경없음()

    def test_전환중거부(self):
        self.Төзү_кертү()['VMState'] = 'saving'
        with self.assertRaises(модуль_VALUE.실행오류): self.үтәргә_команда.үтәргә_команда()
        self.변경없음()

    def test_등록해제거부(self):
        self.Төзү_кертү()
        self.상자.가상기계들.clear()
        with self.assertRaises(модуль_VALUE.실행오류): self.үтәргә_команда.үтәргә_команда()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        машина = self.Төзү_кертү()
        машина['VMState'] = 'poweroff'
        이전 = dict(машина)
        self.상자.эштән_туктау_VALUE = 'make'
        with self.assertRaises(модуль_VALUE.실행오류): self.үтәргә_команда.үтәргә_команда()
        self.assertEqual(машина, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.эштән_туктау_VALUE = 'setextradata'
        with self.assertRaises(модуль_VALUE.실행오류): self.үтәргә_команда.үтәргә_команда()
        self.상자.명령들.clear()
        self.assertEqual(self.үтәргә_команда.үтәргә_команда()['state'], 'running')
        self.assertFalse(any(команда[1] == 'createvm' for команда in self.상자.명령들))

    def test_보존ISO변조거부(self):
        машина = self.Төзү_кертү()
        машина['VMState'] = 'poweroff'
        Path(машина['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(модуль_VALUE.실행오류): self.үтәргә_команда.үтәргә_команда()

    def test_상태미생성(self):
        self.assertEqual(self.үтәргә_команда.күрсәтү_халәт()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Yul in ('../outside', '/tmp/outside'):
            with self.assertRaises(модуль_VALUE.실행오류): self.үтәргә_команда.Yul(Yul)
        (self.тамыр_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(модуль_VALUE.실행오류): self.үтәргә_команда.Yul('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        үлчәм = модуль_VALUE.аергыч_VALUE_286d43f0('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(үлчәм['VMState'], 'running')
        self.assertEqual(үлчәм['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
