import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Nkwuke_valuu = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(Nkwuke_valuu)
Nkwuke_valuu.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.ọdịdà_valuu = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.ọdịdà_valuu == 인수[1] or (인수[0] == 'make' and self.ọdịdà_valuu == 'make'):
            self.ọdịdà_valuu = None
            raise 모듈.실행오류('시험용 ọdịdà_valuu')
        if 인수[0] == 'make':
            ụzọ_ozi = self.뿌리 / 'os/build/kernel.iso'
            ụzọ_ozi.parent.mkdir(parents=True, exist_ok=True)
            ụzọ_ozi.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        mmèm = 인수[1]
        if mmèm == 'list':
            return '\n'.join('"{}" {{{}}}'.format(valuu['name'], indèks) for indèks, valuu in self.가상기계들.items())
        if mmèm == 'createvm':
            indèks, Aha = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[indèks] = {'UUID': indèks, 'name': Aha, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Aha / (Aha + '.vbox')), 'owner': None}
            return ''
        ngwa_komputa = self.가상기계들[인수[2]]
        if mmèm == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Aha), json.dumps(valuu)) for Aha, valuu in ngwa_komputa.items() if Aha != 'owner')
        if mmèm == 'getextradata': return 'Value: ' + ngwa_komputa['owner'] if ngwa_komputa['owner'] else 'No value set!'
        if mmèm == 'setextradata': ngwa_komputa['owner'] = 인수[4]
        elif mmèm == 'storagectl': ngwa_komputa['storagecontrollername0'] = 'JKOROS IDE'
        elif mmèm == 'storageattach': ngwa_komputa['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif mmèm == 'startvm': ngwa_komputa['VMState'] = 'running'
        elif mmèm == 'controlvm':
            assert 인수[3] == 'resume'
            ngwa_komputa['VMState'] = 'running'
        elif mmèm != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.mee_nnyemiwu = 모듈.app_ihengosi_ndi_app(self.뿌리, 'jkoros operating system', Ntiiwu=self.상자)

    def mepụta_ndebà(self):
        결과 = self.mee_nnyemiwu.mee_nnyemiwu()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Ntiiwu[0] == 'VBoxManage' and Ntiiwu[1] in ('list', 'showvminfo', 'getextradata') for Ntiiwu in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.mee_nnyemiwu.mee_nnyemiwu()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in Ntiiwu and 'none' in Ntiiwu for Ntiiwu in self.상자.명령들))
        self.assertFalse(any('hdd' in Ntiiwu or 'discardstate' in Ntiiwu or 'createmedium' in Ntiiwu for Ntiiwu in self.상자.명령들))

    def test_실행중유지(self):
        self.mepụta_ndebà()
        self.assertEqual(self.mee_nnyemiwu.mee_nnyemiwu()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        ngwa_komputa = self.mepụta_ndebà()
        ngwa_komputa['VMState'] = 'saved'
        ndekọ_valuu = self.mee_nnyemiwu.ụzọ_ozi(self.mee_nnyemiwu.Wepụta_ọzi()['serial_log'])
        ndekọ_valuu.write_text('saved log')
        self.mee_nnyemiwu.mee_nnyemiwu()
        self.assertFalse(any(Ntiiwu[0] == 'make' or Ntiiwu[1] == 'modifyvm' for Ntiiwu in self.상자.명령들))
        self.assertEqual([ụzọ_ozi.read_text() for ụzọ_ozi in ndekọ_valuu.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.mepụta_ndebà()['VMState'] = 'paused'
        self.mee_nnyemiwu.mee_nnyemiwu()
        self.assertTrue(any(Ntiiwu[1] == 'controlvm' and Ntiiwu[3] == 'resume' for Ntiiwu in self.상자.명령들))
        self.assertFalse(any(Ntiiwu[0] == 'make' for Ntiiwu in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.mee_nnyemiwu.mee_nnyemiwu()
        self.변경없음()

    def test_소유표식거부(self):
        self.mepụta_ndebà()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.mee_nnyemiwu.mee_nnyemiwu()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.mepụta_ndebà()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.mee_nnyemiwu.mee_nnyemiwu()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        ngwa_komputa = self.mepụta_ndebà()
        ngwa_komputa['VMState'] = 'poweroff'
        ngwa_komputa['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.mee_nnyemiwu.mee_nnyemiwu()
        self.변경없음()

    def test_전환중거부(self):
        self.mepụta_ndebà()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.mee_nnyemiwu.mee_nnyemiwu()
        self.변경없음()

    def test_등록해제거부(self):
        self.mepụta_ndebà()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.mee_nnyemiwu.mee_nnyemiwu()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        ngwa_komputa = self.mepụta_ndebà()
        ngwa_komputa['VMState'] = 'poweroff'
        이전 = dict(ngwa_komputa)
        self.상자.ọdịdà_valuu = 'make'
        with self.assertRaises(모듈.실행오류): self.mee_nnyemiwu.mee_nnyemiwu()
        self.assertEqual(ngwa_komputa, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ọdịdà_valuu = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.mee_nnyemiwu.mee_nnyemiwu()
        self.상자.명령들.clear()
        self.assertEqual(self.mee_nnyemiwu.mee_nnyemiwu()['state'], 'running')
        self.assertFalse(any(Ntiiwu[1] == 'createvm' for Ntiiwu in self.상자.명령들))

    def test_보존ISO변조거부(self):
        ngwa_komputa = self.mepụta_ndebà()
        ngwa_komputa['VMState'] = 'poweroff'
        Path(ngwa_komputa['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.mee_nnyemiwu.mee_nnyemiwu()

    def test_상태미생성(self):
        self.assertEqual(self.mee_nnyemiwu.gòsi_ọnọdụ()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ụzọ_ozi in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.mee_nnyemiwu.ụzọ_ozi(ụzọ_ozi)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.mee_nnyemiwu.ụzọ_ozi('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.njìama_valuu('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
