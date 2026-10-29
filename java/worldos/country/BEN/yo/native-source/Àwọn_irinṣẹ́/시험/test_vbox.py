import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Ìsọ̀tumọ̀_iye = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(Ìsọ̀tumọ̀_iye)
Ìsọ̀tumọ̀_iye.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.ìkùnà_iye = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.ìkùnà_iye == 인수[1] or (인수[0] == 'make' and self.ìkùnà_iye == 'make'):
            self.ìkùnà_iye = None
            raise 모듈.실행오류('시험용 ìkùnà_iye')
        if 인수[0] == 'make':
            ọ̀nà = self.뿌리 / 'os/build/kernel.iso'
            ọ̀nà.parent.mkdir(parents=True, exist_ok=True)
            ọ̀nà.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        ìṣe = 인수[1]
        if ìṣe == 'list':
            return '\n'.join('"{}" {{{}}}'.format(iye['name'], wá_atọ̀ka_àkóónú) for wá_atọ̀ka_àkóónú, iye in self.가상기계들.items())
        if ìṣe == 'createvm':
            wá_atọ̀ka_àkóónú, Orúkọ = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[wá_atọ̀ka_àkóónú] = {'UUID': wá_atọ̀ka_àkóónú, 'name': Orúkọ, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Orúkọ / (Orúkọ + '.vbox')), 'owner': None}
            return ''
        maṣíìnì = self.가상기계들[인수[2]]
        if ìṣe == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Orúkọ), json.dumps(iye)) for Orúkọ, iye in maṣíìnì.items() if Orúkọ != 'owner')
        if ìṣe == 'getextradata': return 'Value: ' + maṣíìnì['owner'] if maṣíìnì['owner'] else 'No value set!'
        if ìṣe == 'setextradata': maṣíìnì['owner'] = 인수[4]
        elif ìṣe == 'storagectl': maṣíìnì['storagecontrollername0'] = 'JKOROS IDE'
        elif ìṣe == 'storageattach': maṣíìnì['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif ìṣe == 'startvm': maṣíìnì['VMState'] = 'running'
        elif ìṣe == 'controlvm':
            assert 인수[3] == 'resume'
            maṣíìnì['VMState'] = 'running'
        elif ìṣe != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.ṣiṣẹ́_àṣẹ = 모듈.àtòjọ_ètò_aṣàfilọ́lẹ̀(self.뿌리, 'jkoros operating system', Àṣẹ=self.상자)

    def Ṣẹ̀dá_ìgbéwọlé(self):
        결과 = self.ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Àṣẹ[0] == 'VBoxManage' and Àṣẹ[1] in ('list', 'showvminfo', 'getextradata') for Àṣẹ in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in Àṣẹ and 'none' in Àṣẹ for Àṣẹ in self.상자.명령들))
        self.assertFalse(any('hdd' in Àṣẹ or 'discardstate' in Àṣẹ or 'createmedium' in Àṣẹ for Àṣẹ in self.상자.명령들))

    def test_실행중유지(self):
        self.Ṣẹ̀dá_ìgbéwọlé()
        self.assertEqual(self.ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        maṣíìnì = self.Ṣẹ̀dá_ìgbéwọlé()
        maṣíìnì['VMState'] = 'saved'
        àkọsílẹ̀_ìṣe_iye = self.ṣiṣẹ́_àṣẹ.ọ̀nà(self.ṣiṣẹ́_àṣẹ.Kàá()['serial_log'])
        àkọsílẹ̀_ìṣe_iye.write_text('saved log')
        self.ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ()
        self.assertFalse(any(Àṣẹ[0] == 'make' or Àṣẹ[1] == 'modifyvm' for Àṣẹ in self.상자.명령들))
        self.assertEqual([ọ̀nà.read_text() for ọ̀nà in àkọsílẹ̀_ìṣe_iye.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Ṣẹ̀dá_ìgbéwọlé()['VMState'] = 'paused'
        self.ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ()
        self.assertTrue(any(Àṣẹ[1] == 'controlvm' and Àṣẹ[3] == 'resume' for Àṣẹ in self.상자.명령들))
        self.assertFalse(any(Àṣẹ[0] == 'make' for Àṣẹ in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ()
        self.변경없음()

    def test_소유표식거부(self):
        self.Ṣẹ̀dá_ìgbéwọlé()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Ṣẹ̀dá_ìgbéwọlé()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        maṣíìnì = self.Ṣẹ̀dá_ìgbéwọlé()
        maṣíìnì['VMState'] = 'poweroff'
        maṣíìnì['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ()
        self.변경없음()

    def test_전환중거부(self):
        self.Ṣẹ̀dá_ìgbéwọlé()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ()
        self.변경없음()

    def test_등록해제거부(self):
        self.Ṣẹ̀dá_ìgbéwọlé()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        maṣíìnì = self.Ṣẹ̀dá_ìgbéwọlé()
        maṣíìnì['VMState'] = 'poweroff'
        이전 = dict(maṣíìnì)
        self.상자.ìkùnà_iye = 'make'
        with self.assertRaises(모듈.실행오류): self.ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ()
        self.assertEqual(maṣíìnì, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ìkùnà_iye = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ()
        self.상자.명령들.clear()
        self.assertEqual(self.ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ()['state'], 'running')
        self.assertFalse(any(Àṣẹ[1] == 'createvm' for Àṣẹ in self.상자.명령들))

    def test_보존ISO변조거부(self):
        maṣíìnì = self.Ṣẹ̀dá_ìgbéwọlé()
        maṣíìnì['VMState'] = 'poweroff'
        Path(maṣíìnì['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ()

    def test_상태미생성(self):
        self.assertEqual(self.ṣiṣẹ́_àṣẹ.ṣàfihàn_ipò()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ọ̀nà in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.ṣiṣẹ́_àṣẹ.ọ̀nà(ọ̀nà)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.ṣiṣẹ́_àṣẹ.ọ̀nà('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.àwòmọ́_iye('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
