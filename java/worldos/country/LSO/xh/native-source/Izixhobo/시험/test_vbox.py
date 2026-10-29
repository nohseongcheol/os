import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Ingcaciso_ixabiso = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(Ingcaciso_ixabiso)
Ingcaciso_ixabiso.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.ukungaphumeleli_ixabiso = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.ukungaphumeleli_ixabiso == 인수[1] or (인수[0] == 'make' and self.ukungaphumeleli_ixabiso == 'make'):
            self.ukungaphumeleli_ixabiso = None
            raise 모듈.실행오류('시험용 ukungaphumeleli_ixabiso')
        if 인수[0] == 'make':
            INDLELA = self.뿌리 / 'os/build/kernel.iso'
            INDLELA.parent.mkdir(parents=True, exist_ok=True)
            INDLELA.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Intshukumo = 인수[1]
        if Intshukumo == 'list':
            return '\n'.join('"{}" {{{}}}'.format(ixabiso['name'], indeksa) for indeksa, ixabiso in self.가상기계들.items())
        if Intshukumo == 'createvm':
            indeksa, Igama = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[indeksa] = {'UUID': indeksa, 'name': Igama, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Igama / (Igama + '.vbox')), 'owner': None}
            return ''
        umatshini = self.가상기계들[인수[2]]
        if Intshukumo == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Igama), json.dumps(ixabiso)) for Igama, ixabiso in umatshini.items() if Igama != 'owner')
        if Intshukumo == 'getextradata': return 'Value: ' + umatshini['owner'] if umatshini['owner'] else 'No value set!'
        if Intshukumo == 'setextradata': umatshini['owner'] = 인수[4]
        elif Intshukumo == 'storagectl': umatshini['storagecontrollername0'] = 'JKOROS IDE'
        elif Intshukumo == 'storageattach': umatshini['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Intshukumo == 'startvm': umatshini['VMState'] = 'running'
        elif Intshukumo == 'controlvm':
            assert 인수[3] == 'resume'
            umatshini['VMState'] = 'running'
        elif Intshukumo != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.ukwenza_umyalelo = 모듈.inkqubo_idrowa_yosetyenziso(self.뿌리, 'jkoros operating system', Umyalelo=self.상자)

    def yila_ufako_nkcukacha(self):
        결과 = self.ukwenza_umyalelo.ukwenza_umyalelo()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Umyalelo[0] == 'VBoxManage' and Umyalelo[1] in ('list', 'showvminfo', 'getextradata') for Umyalelo in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.ukwenza_umyalelo.ukwenza_umyalelo()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in Umyalelo and 'none' in Umyalelo for Umyalelo in self.상자.명령들))
        self.assertFalse(any('hdd' in Umyalelo or 'discardstate' in Umyalelo or 'createmedium' in Umyalelo for Umyalelo in self.상자.명령들))

    def test_실행중유지(self):
        self.yila_ufako_nkcukacha()
        self.assertEqual(self.ukwenza_umyalelo.ukwenza_umyalelo()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        umatshini = self.yila_ufako_nkcukacha()
        umatshini['VMState'] = 'saved'
        ilog_ixabiso = self.ukwenza_umyalelo.INDLELA(self.ukwenza_umyalelo.Funda()['serial_log'])
        ilog_ixabiso.write_text('saved log')
        self.ukwenza_umyalelo.ukwenza_umyalelo()
        self.assertFalse(any(Umyalelo[0] == 'make' or Umyalelo[1] == 'modifyvm' for Umyalelo in self.상자.명령들))
        self.assertEqual([INDLELA.read_text() for INDLELA in ilog_ixabiso.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.yila_ufako_nkcukacha()['VMState'] = 'paused'
        self.ukwenza_umyalelo.ukwenza_umyalelo()
        self.assertTrue(any(Umyalelo[1] == 'controlvm' and Umyalelo[3] == 'resume' for Umyalelo in self.상자.명령들))
        self.assertFalse(any(Umyalelo[0] == 'make' for Umyalelo in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.ukwenza_umyalelo.ukwenza_umyalelo()
        self.변경없음()

    def test_소유표식거부(self):
        self.yila_ufako_nkcukacha()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.ukwenza_umyalelo.ukwenza_umyalelo()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.yila_ufako_nkcukacha()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.ukwenza_umyalelo.ukwenza_umyalelo()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        umatshini = self.yila_ufako_nkcukacha()
        umatshini['VMState'] = 'poweroff'
        umatshini['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.ukwenza_umyalelo.ukwenza_umyalelo()
        self.변경없음()

    def test_전환중거부(self):
        self.yila_ufako_nkcukacha()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.ukwenza_umyalelo.ukwenza_umyalelo()
        self.변경없음()

    def test_등록해제거부(self):
        self.yila_ufako_nkcukacha()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.ukwenza_umyalelo.ukwenza_umyalelo()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        umatshini = self.yila_ufako_nkcukacha()
        umatshini['VMState'] = 'poweroff'
        이전 = dict(umatshini)
        self.상자.ukungaphumeleli_ixabiso = 'make'
        with self.assertRaises(모듈.실행오류): self.ukwenza_umyalelo.ukwenza_umyalelo()
        self.assertEqual(umatshini, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ukungaphumeleli_ixabiso = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.ukwenza_umyalelo.ukwenza_umyalelo()
        self.상자.명령들.clear()
        self.assertEqual(self.ukwenza_umyalelo.ukwenza_umyalelo()['state'], 'running')
        self.assertFalse(any(Umyalelo[1] == 'createvm' for Umyalelo in self.상자.명령들))

    def test_보존ISO변조거부(self):
        umatshini = self.yila_ufako_nkcukacha()
        umatshini['VMState'] = 'poweroff'
        Path(umatshini['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.ukwenza_umyalelo.ukwenza_umyalelo()

    def test_상태미생성(self):
        self.assertEqual(self.ukwenza_umyalelo.bonisa_imo()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for INDLELA in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.ukwenza_umyalelo.INDLELA(INDLELA)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.ukwenza_umyalelo.INDLELA('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.uphawu_ixabiso('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
