import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

നിർവ്വചനം_മൂല്യം = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
മൊഡ്യൂൾ_മൂല്യം = importlib.util.module_from_spec(നിർവ്വചനം_മൂല്യം)
നിർവ്വചനം_മൂല്യം.loader.exec_module(മൊഡ്യൂൾ_മൂല്യം)


class 가짜상자:
    def __init__(self, വർഗ്ഗമൂലം_മൂല്യം):
        self.വർഗ്ഗമൂലം_മൂല്യം = വർഗ്ഗമൂലം_മൂല്യം
        self.명령들 = []
        self.가상기계들 = {}
        self.പരാജയം_മൂല്യം = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.പരാജയം_മൂല്യം == 인수[1] or (인수[0] == 'make' and self.പരാജയം_മൂല്യം == 'make'):
            self.പരാജയം_മൂല്യം = None
            raise മൊഡ്യൂൾ_മൂല്യം.실행오류('시험용 പരാജയം_മൂല്യം')
        if 인수[0] == 'make':
            വഴി = self.വർഗ്ഗമൂലം_മൂല്യം / 'os/build/kernel.iso'
            വഴി.parent.mkdir(parents=True, exist_ok=True)
            വഴി.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        നടപടി = 인수[1]
        if നടപടി == 'list':
            return '\n'.join('"{}" {{{}}}'.format(മൂല്യം['name'], സൂചിക) for സൂചിക, മൂല്യം in self.가상기계들.items())
        if നടപടി == 'createvm':
            സൂചിക, പേരു് = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[സൂചിക] = {'UUID': സൂചിക, 'name': പേരു്, 'VMState': 'poweroff',
                'CfgFile': str(self.വർഗ്ഗമൂലം_മൂല്യം / '.vbox/machines' / പേരു് / (പേരു് + '.vbox')), 'owner': None}
            return ''
        മെഷീൻ = self.가상기계들[인수[2]]
        if നടപടി == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(പേരു്), json.dumps(മൂല്യം)) for പേരു്, മൂല്യം in മെഷീൻ.items() if പേരു് != 'owner')
        if നടപടി == 'getextradata': return 'Value: ' + മെഷീൻ['owner'] if മെഷീൻ['owner'] else 'No value set!'
        if നടപടി == 'setextradata': മെഷീൻ['owner'] = 인수[4]
        elif നടപടി == 'storagectl': മെഷീൻ['storagecontrollername0'] = 'JKOROS IDE'
        elif നടപടി == 'storageattach': മെഷീൻ['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif നടപടി == 'startvm': മെഷീൻ['VMState'] = 'running'
        elif നടപടി == 'controlvm':
            assert 인수[3] == 'resume'
            മെഷീൻ['VMState'] = 'running'
        elif നടപടി != 'modifyvm': raise AssertionError(인수)
        return ''


class പരിശോധന_പ്രവര്_ത്തനം(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.വർഗ്ഗമൂലം_മൂല്യം = Path(self.임시.name)
        (self.വർഗ്ഗമൂലം_മൂല്യം / '.vbox').mkdir()
        self.상자 = 가짜상자(self.വർഗ്ഗമൂലം_മൂല്യം)
        self.നടപ്പാക്കുക_കമാന്_ഡ് = മൊഡ്യൂൾ_മൂല്യം.പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ(self.വർഗ്ഗമൂലം_മൂല്യം, 'jkoros operating system', ആജ്ഞ=self.상자)

    def സൃഷ്_ടിക്കുക_എന്_ട്രി(self):
        അളവ് = self.നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്()
        self.상자.명령들.clear()
        return self.상자.가상기계들[അളവ്['uuid']]

    def 변경없음(self):
        self.assertTrue(all(ആജ്ഞ[0] == 'VBoxManage' and ആജ്ഞ[1] in ('list', 'showvminfo', 'getextradata') for ആജ്ഞ in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        അളവ് = self.നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്()
        self.assertEqual(അളവ്['state'], 'running')
        self.assertTrue(Path(അളവ്['iso']).is_file())
        self.assertTrue(any('--nic1' in ആജ്ഞ and 'none' in ആജ്ഞ for ആജ്ഞ in self.상자.명령들))
        self.assertFalse(any('hdd' in ആജ്ഞ or 'discardstate' in ആജ്ഞ or 'createmedium' in ആജ്ഞ for ആജ്ഞ in self.상자.명령들))

    def test_실행중유지(self):
        self.സൃഷ്_ടിക്കുക_എന്_ട്രി()
        self.assertEqual(self.നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        മെഷീൻ = self.സൃഷ്_ടിക്കുക_എന്_ട്രി()
        മെഷീൻ['VMState'] = 'saved'
        ലോഗ്_മൂല്യം = self.നടപ്പാക്കുക_കമാന്_ഡ്.വഴി(self.നടപ്പാക്കുക_കമാന്_ഡ്.വായന()['serial_log'])
        ലോഗ്_മൂല്യം.write_text('saved log')
        self.നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്()
        self.assertFalse(any(ആജ്ഞ[0] == 'make' or ആജ്ഞ[1] == 'modifyvm' for ആജ്ഞ in self.상자.명령들))
        self.assertEqual([വഴി.read_text() for വഴി in ലോഗ്_മൂല്യം.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.സൃഷ്_ടിക്കുക_എന്_ട്രി()['VMState'] = 'paused'
        self.നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്()
        self.assertTrue(any(ആജ്ഞ[1] == 'controlvm' and ആജ്ഞ[3] == 'resume' for ആജ്ഞ in self.상자.명령들))
        self.assertFalse(any(ആജ്ഞ[0] == 'make' for ആജ്ഞ in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(മൊഡ്യൂൾ_മൂല്യം.실행오류): self.നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്()
        self.변경없음()

    def test_소유표식거부(self):
        self.സൃഷ്_ടിക്കുക_എന്_ട്രി()['owner'] = 'someone-else'
        with self.assertRaises(മൊഡ്യൂൾ_മൂല്യം.실행오류): self.നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.സൃഷ്_ടിക്കുക_എന്_ട്രി()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(മൊഡ്യൂൾ_മൂല്യം.실행오류): self.നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        മെഷീൻ = self.സൃഷ്_ടിക്കുക_എന്_ട്രി()
        മെഷീൻ['VMState'] = 'poweroff'
        മെഷീൻ['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(മൊഡ്യൂൾ_മൂല്യം.실행오류): self.നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്()
        self.변경없음()

    def test_전환중거부(self):
        self.സൃഷ്_ടിക്കുക_എന്_ട്രി()['VMState'] = 'saving'
        with self.assertRaises(മൊഡ്യൂൾ_മൂല്യം.실행오류): self.നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്()
        self.변경없음()

    def test_등록해제거부(self):
        self.സൃഷ്_ടിക്കുക_എന്_ട്രി()
        self.상자.가상기계들.clear()
        with self.assertRaises(മൊഡ്യൂൾ_മൂല്യം.실행오류): self.നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        മെഷീൻ = self.സൃഷ്_ടിക്കുക_എന്_ട്രി()
        മെഷീൻ['VMState'] = 'poweroff'
        이전 = dict(മെഷീൻ)
        self.상자.പരാജയം_മൂല്യം = 'make'
        with self.assertRaises(മൊഡ്യൂൾ_മൂല്യം.실행오류): self.നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്()
        self.assertEqual(മെഷീൻ, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.പരാജയം_മൂല്യം = 'setextradata'
        with self.assertRaises(മൊഡ്യൂൾ_മൂല്യം.실행오류): self.നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്()
        self.상자.명령들.clear()
        self.assertEqual(self.നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്()['state'], 'running')
        self.assertFalse(any(ആജ്ഞ[1] == 'createvm' for ആജ്ഞ in self.상자.명령들))

    def test_보존ISO변조거부(self):
        മെഷീൻ = self.സൃഷ്_ടിക്കുക_എന്_ട്രി()
        മെഷീൻ['VMState'] = 'poweroff'
        Path(മെഷീൻ['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(മൊഡ്യൂൾ_മൂല്യം.실행오류): self.നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്()

    def test_상태미생성(self):
        self.assertEqual(self.നടപ്പാക്കുക_കമാന്_ഡ്.പ്രദർശനം_അവസ്ഥ()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for വഴി in ('../outside', '/tmp/outside'):
            with self.assertRaises(മൊഡ്യൂൾ_മൂല്യം.실행오류): self.നടപ്പാക്കുക_കമാന്_ഡ്.വഴി(വഴി)
        (self.വർഗ്ഗമൂലം_മൂല്യം / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(മൊഡ്യൂൾ_മൂല്യം.실행오류): self.നടപ്പാക്കുക_കമാന്_ഡ്.വഴി('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        അളവ് = മൊഡ്യൂൾ_മൂല്യം.ആട്രിബ്യൂട്ട്_മൂല്യം('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(അളവ്['VMState'], 'running')
        self.assertEqual(അളവ്['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
