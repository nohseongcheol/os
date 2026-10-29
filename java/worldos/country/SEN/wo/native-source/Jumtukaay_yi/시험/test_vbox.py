import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Tekki_baat_xëyma = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(Tekki_baat_xëyma)
Tekki_baat_xëyma.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.foo_xëyma = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.foo_xëyma == 인수[1] or (인수[0] == 'make' and self.foo_xëyma == 'make'):
            self.foo_xëyma = None
            raise 모듈.실행오류('시험용 foo_xëyma')
        if 인수[0] == 'make':
            Yoonu_jëmale = self.뿌리 / 'os/build/kernel.iso'
            Yoonu_jëmale.parent.mkdir(parents=True, exist_ok=True)
            Yoonu_jëmale.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        jëf = 인수[1]
        if jëf == 'list':
            return '\n'.join('"{}" {{{}}}'.format(xëyma['name'], àlluwa_tur) for àlluwa_tur, xëyma in self.가상기계들.items())
        if jëf == 'createvm':
            àlluwa_tur, tur_253d1510 = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[àlluwa_tur] = {'UUID': àlluwa_tur, 'name': tur_253d1510, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / tur_253d1510 / (tur_253d1510 + '.vbox')), 'owner': None}
            return ''
        masin = self.가상기계들[인수[2]]
        if jëf == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(tur_253d1510), json.dumps(xëyma)) for tur_253d1510, xëyma in masin.items() if tur_253d1510 != 'owner')
        if jëf == 'getextradata': return 'Value: ' + masin['owner'] if masin['owner'] else 'No value set!'
        if jëf == 'setextradata': masin['owner'] = 인수[4]
        elif jëf == 'storagectl': masin['storagecontrollername0'] = 'JKOROS IDE'
        elif jëf == 'storageattach': masin['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif jëf == 'startvm': masin['VMState'] = 'running'
        elif jëf == 'controlvm':
            assert 인수[3] == 'resume'
            masin['VMState'] = 'running'
        elif jëf != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.def_ndigel = 모듈.jëfekaay_armuwaaru_jëfekaay(self.뿌리, 'jkoros operating system', ndigel=self.상자)

    def sos_dugal_xabaar(self):
        결과 = self.def_ndigel.def_ndigel()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(ndigel[0] == 'VBoxManage' and ndigel[1] in ('list', 'showvminfo', 'getextradata') for ndigel in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.def_ndigel.def_ndigel()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in ndigel and 'none' in ndigel for ndigel in self.상자.명령들))
        self.assertFalse(any('hdd' in ndigel or 'discardstate' in ndigel or 'createmedium' in ndigel for ndigel in self.상자.명령들))

    def test_실행중유지(self):
        self.sos_dugal_xabaar()
        self.assertEqual(self.def_ndigel.def_ndigel()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        masin = self.sos_dugal_xabaar()
        masin['VMState'] = 'saved'
        làq_xëyma = self.def_ndigel.Yoonu_jëmale(self.def_ndigel.읽기()['serial_log'])
        làq_xëyma.write_text('saved log')
        self.def_ndigel.def_ndigel()
        self.assertFalse(any(ndigel[0] == 'make' or ndigel[1] == 'modifyvm' for ndigel in self.상자.명령들))
        self.assertEqual([Yoonu_jëmale.read_text() for Yoonu_jëmale in làq_xëyma.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.sos_dugal_xabaar()['VMState'] = 'paused'
        self.def_ndigel.def_ndigel()
        self.assertTrue(any(ndigel[1] == 'controlvm' and ndigel[3] == 'resume' for ndigel in self.상자.명령들))
        self.assertFalse(any(ndigel[0] == 'make' for ndigel in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.def_ndigel.def_ndigel()
        self.변경없음()

    def test_소유표식거부(self):
        self.sos_dugal_xabaar()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.def_ndigel.def_ndigel()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.sos_dugal_xabaar()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.def_ndigel.def_ndigel()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        masin = self.sos_dugal_xabaar()
        masin['VMState'] = 'poweroff'
        masin['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.def_ndigel.def_ndigel()
        self.변경없음()

    def test_전환중거부(self):
        self.sos_dugal_xabaar()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.def_ndigel.def_ndigel()
        self.변경없음()

    def test_등록해제거부(self):
        self.sos_dugal_xabaar()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.def_ndigel.def_ndigel()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        masin = self.sos_dugal_xabaar()
        masin['VMState'] = 'poweroff'
        이전 = dict(masin)
        self.상자.foo_xëyma = 'make'
        with self.assertRaises(모듈.실행오류): self.def_ndigel.def_ndigel()
        self.assertEqual(masin, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.foo_xëyma = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.def_ndigel.def_ndigel()
        self.상자.명령들.clear()
        self.assertEqual(self.def_ndigel.def_ndigel()['state'], 'running')
        self.assertFalse(any(ndigel[1] == 'createvm' for ndigel in self.상자.명령들))

    def test_보존ISO변조거부(self):
        masin = self.sos_dugal_xabaar()
        masin['VMState'] = 'poweroff'
        Path(masin['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.def_ndigel.def_ndigel()

    def test_상태미생성(self):
        self.assertEqual(self.def_ndigel.féeñal_nekkin()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Yoonu_jëmale in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.def_ndigel.Yoonu_jëmale(Yoonu_jëmale)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.def_ndigel.Yoonu_jëmale('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.jagle_xëyma('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
