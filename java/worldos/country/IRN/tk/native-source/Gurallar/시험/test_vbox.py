import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Kesgitleme_baha = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(Kesgitleme_baha)
Kesgitleme_baha.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.näsazlyk_baha = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.näsazlyk_baha == 인수[1] or (인수[0] == 'make' and self.näsazlyk_baha == 'make'):
            self.näsazlyk_baha = None
            raise 모듈.실행오류('시험용 näsazlyk_baha')
        if 인수[0] == 'make':
            Ýol = self.뿌리 / 'os/build/kernel.iso'
            Ýol.parent.mkdir(parents=True, exist_ok=True)
            Ýol.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        iş = 인수[1]
        if iş == 'list':
            return '\n'.join('"{}" {{{}}}'.format(baha['name'], indeks) for indeks, baha in self.가상기계들.items())
        if iş == 'createvm':
            indeks, Ad = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[indeks] = {'UUID': indeks, 'name': Ad, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Ad / (Ad + '.vbox')), 'owner': None}
            return ''
        kompýuter = self.가상기계들[인수[2]]
        if iş == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Ad), json.dumps(baha)) for Ad, baha in kompýuter.items() if Ad != 'owner')
        if iş == 'getextradata': return 'Value: ' + kompýuter['owner'] if kompýuter['owner'] else 'No value set!'
        if iş == 'setextradata': kompýuter['owner'] = 인수[4]
        elif iş == 'storagectl': kompýuter['storagecontrollername0'] = 'JKOROS IDE'
        elif iş == 'storageattach': kompýuter['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif iş == 'startvm': kompýuter['VMState'] = 'running'
        elif iş == 'controlvm':
            assert 인수[3] == 'resume'
            kompýuter['VMState'] = 'running'
        elif iş != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.ýerine_ýetir_buýruk = 모듈.programma_programma_paneli(self.뿌리, 'jkoros operating system', buýruk=self.상자)

    def döretmek_girizmeklik(self):
        결과 = self.ýerine_ýetir_buýruk.ýerine_ýetir_buýruk()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(buýruk[0] == 'VBoxManage' and buýruk[1] in ('list', 'showvminfo', 'getextradata') for buýruk in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.ýerine_ýetir_buýruk.ýerine_ýetir_buýruk()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in buýruk and 'none' in buýruk for buýruk in self.상자.명령들))
        self.assertFalse(any('hdd' in buýruk or 'discardstate' in buýruk or 'createmedium' in buýruk for buýruk in self.상자.명령들))

    def test_실행중유지(self):
        self.döretmek_girizmeklik()
        self.assertEqual(self.ýerine_ýetir_buýruk.ýerine_ýetir_buýruk()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        kompýuter = self.döretmek_girizmeklik()
        kompýuter['VMState'] = 'saved'
        hasaba_alyş_baha = self.ýerine_ýetir_buýruk.Ýol(self.ýerine_ýetir_buýruk.Oka()['serial_log'])
        hasaba_alyş_baha.write_text('saved log')
        self.ýerine_ýetir_buýruk.ýerine_ýetir_buýruk()
        self.assertFalse(any(buýruk[0] == 'make' or buýruk[1] == 'modifyvm' for buýruk in self.상자.명령들))
        self.assertEqual([Ýol.read_text() for Ýol in hasaba_alyş_baha.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.döretmek_girizmeklik()['VMState'] = 'paused'
        self.ýerine_ýetir_buýruk.ýerine_ýetir_buýruk()
        self.assertTrue(any(buýruk[1] == 'controlvm' and buýruk[3] == 'resume' for buýruk in self.상자.명령들))
        self.assertFalse(any(buýruk[0] == 'make' for buýruk in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.ýerine_ýetir_buýruk.ýerine_ýetir_buýruk()
        self.변경없음()

    def test_소유표식거부(self):
        self.döretmek_girizmeklik()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.ýerine_ýetir_buýruk.ýerine_ýetir_buýruk()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.döretmek_girizmeklik()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.ýerine_ýetir_buýruk.ýerine_ýetir_buýruk()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        kompýuter = self.döretmek_girizmeklik()
        kompýuter['VMState'] = 'poweroff'
        kompýuter['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.ýerine_ýetir_buýruk.ýerine_ýetir_buýruk()
        self.변경없음()

    def test_전환중거부(self):
        self.döretmek_girizmeklik()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.ýerine_ýetir_buýruk.ýerine_ýetir_buýruk()
        self.변경없음()

    def test_등록해제거부(self):
        self.döretmek_girizmeklik()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.ýerine_ýetir_buýruk.ýerine_ýetir_buýruk()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        kompýuter = self.döretmek_girizmeklik()
        kompýuter['VMState'] = 'poweroff'
        이전 = dict(kompýuter)
        self.상자.näsazlyk_baha = 'make'
        with self.assertRaises(모듈.실행오류): self.ýerine_ýetir_buýruk.ýerine_ýetir_buýruk()
        self.assertEqual(kompýuter, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.näsazlyk_baha = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.ýerine_ýetir_buýruk.ýerine_ýetir_buýruk()
        self.상자.명령들.clear()
        self.assertEqual(self.ýerine_ýetir_buýruk.ýerine_ýetir_buýruk()['state'], 'running')
        self.assertFalse(any(buýruk[1] == 'createvm' for buýruk in self.상자.명령들))

    def test_보존ISO변조거부(self):
        kompýuter = self.döretmek_girizmeklik()
        kompýuter['VMState'] = 'poweroff'
        Path(kompýuter['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.ýerine_ýetir_buýruk.ýerine_ýetir_buýruk()

    def test_상태미생성(self):
        self.assertEqual(self.ýerine_ýetir_buýruk.görkez_ýagdaý()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Ýol in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.ýerine_ýetir_buýruk.Ýol(Ýol)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.ýerine_ýetir_buýruk.Ýol('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.alamat_baha('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
