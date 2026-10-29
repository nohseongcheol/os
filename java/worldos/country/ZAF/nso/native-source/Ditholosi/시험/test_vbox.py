import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Tlhaloso_boleng = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(Tlhaloso_boleng)
Tlhaloso_boleng.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.go_palelwa_boleng = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.go_palelwa_boleng == 인수[1] or (인수[0] == 'make' and self.go_palelwa_boleng == 'make'):
            self.go_palelwa_boleng = None
            raise 모듈.실행오류('시험용 go_palelwa_boleng')
        if 인수[0] == 'make':
            Tsejana = self.뿌리 / 'os/build/kernel.iso'
            Tsejana.parent.mkdir(parents=True, exist_ok=True)
            Tsejana.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Mogato = 인수[1]
        if Mogato == 'list':
            return '\n'.join('"{}" {{{}}}'.format(boleng['name'], lokela) for lokela, boleng in self.가상기계들.items())
        if Mogato == 'createvm':
            lokela, Leina = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[lokela] = {'UUID': lokela, 'name': Leina, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Leina / (Leina + '.vbox')), 'owner': None}
            return ''
        motšhene = self.가상기계들[인수[2]]
        if Mogato == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Leina), json.dumps(boleng)) for Leina, boleng in motšhene.items() if Leina != 'owner')
        if Mogato == 'getextradata': return 'Value: ' + motšhene['owner'] if motšhene['owner'] else 'No value set!'
        if Mogato == 'setextradata': motšhene['owner'] = 인수[4]
        elif Mogato == 'storagectl': motšhene['storagecontrollername0'] = 'JKOROS IDE'
        elif Mogato == 'storageattach': motšhene['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Mogato == 'startvm': motšhene['VMState'] = 'running'
        elif Mogato == 'controlvm':
            assert 인수[3] == 'resume'
            motšhene['VMState'] = 'running'
        elif Mogato != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.phethagatša_taelo = 모듈.tirišo_sethala_tirišo(self.뿌리, 'jkoros operating system', Taelo=self.상자)

    def 만들기(self):
        결과 = self.phethagatša_taelo.phethagatša_taelo()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Taelo[0] == 'VBoxManage' and Taelo[1] in ('list', 'showvminfo', 'getextradata') for Taelo in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.phethagatša_taelo.phethagatša_taelo()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in Taelo and 'none' in Taelo for Taelo in self.상자.명령들))
        self.assertFalse(any('hdd' in Taelo or 'discardstate' in Taelo or 'createmedium' in Taelo for Taelo in self.상자.명령들))

    def test_실행중유지(self):
        self.만들기()
        self.assertEqual(self.phethagatša_taelo.phethagatša_taelo()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        motšhene = self.만들기()
        motšhene['VMState'] = 'saved'
        pego_boleng_e0918eb0 = self.phethagatša_taelo.Tsejana(self.phethagatša_taelo.Bala()['serial_log'])
        pego_boleng_e0918eb0.write_text('saved log')
        self.phethagatša_taelo.phethagatša_taelo()
        self.assertFalse(any(Taelo[0] == 'make' or Taelo[1] == 'modifyvm' for Taelo in self.상자.명령들))
        self.assertEqual([Tsejana.read_text() for Tsejana in pego_boleng_e0918eb0.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.만들기()['VMState'] = 'paused'
        self.phethagatša_taelo.phethagatša_taelo()
        self.assertTrue(any(Taelo[1] == 'controlvm' and Taelo[3] == 'resume' for Taelo in self.상자.명령들))
        self.assertFalse(any(Taelo[0] == 'make' for Taelo in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.phethagatša_taelo.phethagatša_taelo()
        self.변경없음()

    def test_소유표식거부(self):
        self.만들기()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.phethagatša_taelo.phethagatša_taelo()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.만들기()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.phethagatša_taelo.phethagatša_taelo()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        motšhene = self.만들기()
        motšhene['VMState'] = 'poweroff'
        motšhene['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.phethagatša_taelo.phethagatša_taelo()
        self.변경없음()

    def test_전환중거부(self):
        self.만들기()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.phethagatša_taelo.phethagatša_taelo()
        self.변경없음()

    def test_등록해제거부(self):
        self.만들기()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.phethagatša_taelo.phethagatša_taelo()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        motšhene = self.만들기()
        motšhene['VMState'] = 'poweroff'
        이전 = dict(motšhene)
        self.상자.go_palelwa_boleng = 'make'
        with self.assertRaises(모듈.실행오류): self.phethagatša_taelo.phethagatša_taelo()
        self.assertEqual(motšhene, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.go_palelwa_boleng = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.phethagatša_taelo.phethagatša_taelo()
        self.상자.명령들.clear()
        self.assertEqual(self.phethagatša_taelo.phethagatša_taelo()['state'], 'running')
        self.assertFalse(any(Taelo[1] == 'createvm' for Taelo in self.상자.명령들))

    def test_보존ISO변조거부(self):
        motšhene = self.만들기()
        motšhene['VMState'] = 'poweroff'
        Path(motšhene['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.phethagatša_taelo.phethagatša_taelo()

    def test_상태미생성(self):
        self.assertEqual(self.phethagatša_taelo.bontšha_boemo()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Tsejana in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.phethagatša_taelo.Tsejana(Tsejana)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.phethagatša_taelo.Tsejana('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.tlhaodi_ya_faele_boleng('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
