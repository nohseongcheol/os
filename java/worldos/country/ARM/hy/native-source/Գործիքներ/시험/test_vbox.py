import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Սահմանում_արժեք = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
հանգույց_արժեք_6d2d8bf4 = importlib.util.module_from_spec(Սահմանում_արժեք)
Սահմանում_արժեք.loader.exec_module(հանգույց_արժեք_6d2d8bf4)


class 가짜상자:
    def __init__(self, արմատ_արժեք):
        self.արմատ_արժեք = արմատ_արժեք
        self.명령들 = []
        self.가상기계들 = {}
        self.ձախողում_արժեք = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.ձախողում_արժեք == 인수[1] or (인수[0] == 'make' and self.ձախողում_արժեք == 'make'):
            self.ձախողում_արժեք = None
            raise հանգույց_արժեք_6d2d8bf4.실행오류('시험용 ձախողում_արժեք')
        if 인수[0] == 'make':
            Ճանապարհ = self.արմատ_արժեք / 'os/build/kernel.iso'
            Ճանապարհ.parent.mkdir(parents=True, exist_ok=True)
            Ճանապարհ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Գործողություն = 인수[1]
        if Գործողություն == 'list':
            return '\n'.join('"{}" {{{}}}'.format(արժեք['name'], դասիչ) for դասիչ, արժեք in self.가상기계들.items())
        if Գործողություն == 'createvm':
            դասիչ, Անուն = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[դասիչ] = {'UUID': դասիչ, 'name': Անուն, 'VMState': 'poweroff',
                'CfgFile': str(self.արմատ_արժեք / '.vbox/machines' / Անուն / (Անուն + '.vbox')), 'owner': None}
            return ''
        մեքենա = self.가상기계들[인수[2]]
        if Գործողություն == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Անուն), json.dumps(արժեք)) for Անուն, արժեք in մեքենա.items() if Անուն != 'owner')
        if Գործողություն == 'getextradata': return 'Value: ' + մեքենա['owner'] if մեքենա['owner'] else 'No value set!'
        if Գործողություն == 'setextradata': մեքենա['owner'] = 인수[4]
        elif Գործողություն == 'storagectl': մեքենա['storagecontrollername0'] = 'JKOROS IDE'
        elif Գործողություն == 'storageattach': մեքենա['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Գործողություն == 'startvm': մեքենա['VMState'] = 'running'
        elif Գործողություն == 'controlvm':
            assert 인수[3] == 'resume'
            մեքենա['VMState'] = 'running'
        elif Գործողություն != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.արմատ_արժեք = Path(self.임시.name)
        (self.արմատ_արժեք / '.vbox').mkdir()
        self.상자 = 가짜상자(self.արմատ_արժեք)
        self.կատարել_հրաման = հանգույց_արժեք_6d2d8bf4.ծրագիր_թողարկիչ(self.արմատ_արժեք, 'jkoros operating system', Հրահանգ=self.상자)

    def Կերտի_ր_մուտքագրում(self):
        չափ = self.կատարել_հրաման.կատարել_հրաման()
        self.상자.명령들.clear()
        return self.상자.가상기계들[չափ['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Հրահանգ[0] == 'VBoxManage' and Հրահանգ[1] in ('list', 'showvminfo', 'getextradata') for Հրահանգ in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        չափ = self.կատարել_հրաման.կատարել_հրաման()
        self.assertEqual(չափ['state'], 'running')
        self.assertTrue(Path(չափ['iso']).is_file())
        self.assertTrue(any('--nic1' in Հրահանգ and 'none' in Հրահանգ for Հրահանգ in self.상자.명령들))
        self.assertFalse(any('hdd' in Հրահանգ or 'discardstate' in Հրահանգ or 'createmedium' in Հրահանգ for Հրահանգ in self.상자.명령들))

    def test_실행중유지(self):
        self.Կերտի_ր_մուտքագրում()
        self.assertEqual(self.կատարել_հրաման.կատարել_հրաման()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        մեքենա = self.Կերտի_ր_մուտքագրում()
        մեքենա['VMState'] = 'saved'
        մատյան_արժեք = self.կատարել_հրաման.Ճանապարհ(self.կատարել_հրաման.Ընթերցում()['serial_log'])
        մատյան_արժեք.write_text('saved log')
        self.կատարել_հրաման.կատարել_հրաման()
        self.assertFalse(any(Հրահանգ[0] == 'make' or Հրահանգ[1] == 'modifyvm' for Հրահանգ in self.상자.명령들))
        self.assertEqual([Ճանապարհ.read_text() for Ճանապարհ in մատյան_արժեք.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Կերտի_ր_մուտքագրում()['VMState'] = 'paused'
        self.կատարել_հրաման.կատարել_հրաման()
        self.assertTrue(any(Հրահանգ[1] == 'controlvm' and Հրահանգ[3] == 'resume' for Հրահանգ in self.상자.명령들))
        self.assertFalse(any(Հրահանգ[0] == 'make' for Հրահանգ in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(հանգույց_արժեք_6d2d8bf4.실행오류): self.կատարել_հրաման.կատարել_հրաման()
        self.변경없음()

    def test_소유표식거부(self):
        self.Կերտի_ր_մուտքագրում()['owner'] = 'someone-else'
        with self.assertRaises(հանգույց_արժեք_6d2d8bf4.실행오류): self.կատարել_հրաման.կատարել_հրաման()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Կերտի_ր_մուտքագրում()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(հանգույց_արժեք_6d2d8bf4.실행오류): self.կատարել_հրաման.կատարել_հրաման()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        մեքենա = self.Կերտի_ր_մուտքագրում()
        մեքենա['VMState'] = 'poweroff'
        մեքենա['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(հանգույց_արժեք_6d2d8bf4.실행오류): self.կատարել_հրաման.կատարել_հրաման()
        self.변경없음()

    def test_전환중거부(self):
        self.Կերտի_ր_մուտքագրում()['VMState'] = 'saving'
        with self.assertRaises(հանգույց_արժեք_6d2d8bf4.실행오류): self.կատարել_հրաման.կատարել_հրաման()
        self.변경없음()

    def test_등록해제거부(self):
        self.Կերտի_ր_մուտքագրում()
        self.상자.가상기계들.clear()
        with self.assertRaises(հանգույց_արժեք_6d2d8bf4.실행오류): self.կատարել_հրաման.կատարել_հրաման()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        մեքենա = self.Կերտի_ր_մուտքագրում()
        մեքենա['VMState'] = 'poweroff'
        이전 = dict(մեքենա)
        self.상자.ձախողում_արժեք = 'make'
        with self.assertRaises(հանգույց_արժեք_6d2d8bf4.실행오류): self.կատարել_հրաման.կատարել_հրաման()
        self.assertEqual(մեքենա, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ձախողում_արժեք = 'setextradata'
        with self.assertRaises(հանգույց_արժեք_6d2d8bf4.실행오류): self.կատարել_հրաման.կատարել_հրաման()
        self.상자.명령들.clear()
        self.assertEqual(self.կատարել_հրաման.կատարել_հրաման()['state'], 'running')
        self.assertFalse(any(Հրահանգ[1] == 'createvm' for Հրահանգ in self.상자.명령들))

    def test_보존ISO변조거부(self):
        մեքենա = self.Կերտի_ր_մուտքագրում()
        մեքենա['VMState'] = 'poweroff'
        Path(մեքենա['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(հանգույց_արժեք_6d2d8bf4.실행오류): self.կատարել_հրաման.կատարել_հրաման()

    def test_상태미생성(self):
        self.assertEqual(self.կատարել_հրաման.ցուցադրել_վիճակ()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Ճանապարհ in ('../outside', '/tmp/outside'):
            with self.assertRaises(հանգույց_արժեք_6d2d8bf4.실행오류): self.կատարել_հրաման.Ճանապարհ(Ճանապարհ)
        (self.արմատ_արժեք / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(հանգույց_արժեք_6d2d8bf4.실행오류): self.կատարել_հրաման.Ճանապարհ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        չափ = հանգույց_արժեք_6d2d8bf4.հատկանիշ_արժեք('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(չափ['VMState'], 'running')
        self.assertEqual(չափ['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
