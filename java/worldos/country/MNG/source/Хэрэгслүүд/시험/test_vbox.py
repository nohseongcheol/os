import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Тайлбар_утга = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(Тайлбар_утга)
Тайлбар_утга.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.гэмтэл_утга = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.гэмтэл_утга == 인수[1] or (인수[0] == 'make' and self.гэмтэл_утга == 'make'):
            self.гэмтэл_утга = None
            raise 모듈.실행오류('시험용 гэмтэл_утга')
        if 인수[0] == 'make':
            ЗАМ = self.뿌리 / 'os/build/kernel.iso'
            ЗАМ.parent.mkdir(parents=True, exist_ok=True)
            ЗАМ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Үйлдэл = 인수[1]
        if Үйлдэл == 'list':
            return '\n'.join('"{}" {{{}}}'.format(утга['name'], индекс) for индекс, утга in self.가상기계들.items())
        if Үйлдэл == 'createvm':
            индекс, Нэр = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[индекс] = {'UUID': индекс, 'name': Нэр, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Нэр / (Нэр + '.vbox')), 'owner': None}
            return ''
        компьютер = self.가상기계들[인수[2]]
        if Үйлдэл == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Нэр), json.dumps(утга)) for Нэр, утга in компьютер.items() if Нэр != 'owner')
        if Үйлдэл == 'getextradata': return 'Value: ' + компьютер['owner'] if компьютер['owner'] else 'No value set!'
        if Үйлдэл == 'setextradata': компьютер['owner'] = 인수[4]
        elif Үйлдэл == 'storagectl': компьютер['storagecontrollername0'] = 'JKOROS IDE'
        elif Үйлдэл == 'storageattach': компьютер['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Үйлдэл == 'startvm': компьютер['VMState'] = 'running'
        elif Үйлдэл == 'controlvm':
            assert 인수[3] == 'resume'
            компьютер['VMState'] = 'running'
        elif Үйлдэл != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.Гүйцэтгэх_команд = 모듈.програм_гишүүн(self.뿌리, 'jkoros operating system', Тушаал=self.상자)

    def үүсгэх_оролт(self):
        결과 = self.Гүйцэтгэх_команд.Гүйцэтгэх_команд()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Тушаал[0] == 'VBoxManage' and Тушаал[1] in ('list', 'showvminfo', 'getextradata') for Тушаал in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.Гүйцэтгэх_команд.Гүйцэтгэх_команд()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in Тушаал and 'none' in Тушаал for Тушаал in self.상자.명령들))
        self.assertFalse(any('hdd' in Тушаал or 'discardstate' in Тушаал or 'createmedium' in Тушаал for Тушаал in self.상자.명령들))

    def test_실행중유지(self):
        self.үүсгэх_оролт()
        self.assertEqual(self.Гүйцэтгэх_команд.Гүйцэтгэх_команд()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        компьютер = self.үүсгэх_оролт()
        компьютер['VMState'] = 'saved'
        бичих_утга_e0918eb0 = self.Гүйцэтгэх_команд.ЗАМ(self.Гүйцэтгэх_команд.Унших()['serial_log'])
        бичих_утга_e0918eb0.write_text('saved log')
        self.Гүйцэтгэх_команд.Гүйцэтгэх_команд()
        self.assertFalse(any(Тушаал[0] == 'make' or Тушаал[1] == 'modifyvm' for Тушаал in self.상자.명령들))
        self.assertEqual([ЗАМ.read_text() for ЗАМ in бичих_утга_e0918eb0.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.үүсгэх_оролт()['VMState'] = 'paused'
        self.Гүйцэтгэх_команд.Гүйцэтгэх_команд()
        self.assertTrue(any(Тушаал[1] == 'controlvm' and Тушаал[3] == 'resume' for Тушаал in self.상자.명령들))
        self.assertFalse(any(Тушаал[0] == 'make' for Тушаал in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.Гүйцэтгэх_команд.Гүйцэтгэх_команд()
        self.변경없음()

    def test_소유표식거부(self):
        self.үүсгэх_оролт()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.Гүйцэтгэх_команд.Гүйцэтгэх_команд()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.үүсгэх_оролт()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.Гүйцэтгэх_команд.Гүйцэтгэх_команд()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        компьютер = self.үүсгэх_оролт()
        компьютер['VMState'] = 'poweroff'
        компьютер['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.Гүйцэтгэх_команд.Гүйцэтгэх_команд()
        self.변경없음()

    def test_전환중거부(self):
        self.үүсгэх_оролт()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.Гүйцэтгэх_команд.Гүйцэтгэх_команд()
        self.변경없음()

    def test_등록해제거부(self):
        self.үүсгэх_оролт()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.Гүйцэтгэх_команд.Гүйцэтгэх_команд()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        компьютер = self.үүсгэх_оролт()
        компьютер['VMState'] = 'poweroff'
        이전 = dict(компьютер)
        self.상자.гэмтэл_утга = 'make'
        with self.assertRaises(모듈.실행오류): self.Гүйцэтгэх_команд.Гүйцэтгэх_команд()
        self.assertEqual(компьютер, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.гэмтэл_утга = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.Гүйцэтгэх_команд.Гүйцэтгэх_команд()
        self.상자.명령들.clear()
        self.assertEqual(self.Гүйцэтгэх_команд.Гүйцэтгэх_команд()['state'], 'running')
        self.assertFalse(any(Тушаал[1] == 'createvm' for Тушаал in self.상자.명령들))

    def test_보존ISO변조거부(self):
        компьютер = self.үүсгэх_оролт()
        компьютер['VMState'] = 'poweroff'
        Path(компьютер['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.Гүйцэтгэх_команд.Гүйцэтгэх_команд()

    def test_상태미생성(self):
        self.assertEqual(self.Гүйцэтгэх_команд.үзүүлэх_төлөв()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ЗАМ in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.Гүйцэтгэх_команд.ЗАМ(ЗАМ)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.Гүйцэтгэх_команд.ЗАМ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.аттрибут_утга('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
