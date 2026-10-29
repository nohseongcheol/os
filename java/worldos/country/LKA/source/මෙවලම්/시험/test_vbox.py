import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

නිර්වචනය_අගය = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(නිර්වචනය_අගය)
නිර්වචනය_අගය.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.අසමත්වීම_අගය = None

    def __call__(self, විස්තාරක):
        විස්තාරක = list(map(str, විස්තාරක))
        self.명령들.append(විස්තාරක)
        if self.අසමත්වීම_අගය == විස්තාරක[1] or (විස්තාරක[0] == 'make' and self.අසමත්වීම_අගය == 'make'):
            self.අසමත්වීම_අගය = None
            raise 모듈.실행오류('시험용 අසමත්වීම_අගය')
        if විස්තාරක[0] == 'make':
            මාර්_ගය = self.뿌리 / 'os/build/kernel.iso'
            මාර්_ගය.parent.mkdir(parents=True, exist_ok=True)
            මාර්_ගය.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        ක්_රීයාව = විස්තාරක[1]
        if ක්_රීයාව == 'list':
            return '\n'.join('"{}" {{{}}}'.format(අගය['name'], සූචිය) for සූචිය, අගය in self.가상기계들.items())
        if ක්_රීයාව == 'createvm':
            සූචිය, නම = විස්තාරක[විස්තාරක.index('--uuid') + 1], විස්තාරක[විස්තාරක.index('--name') + 1]
            self.가상기계들[සූචිය] = {'UUID': සූචිය, 'name': නම, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / නම / (නම + '.vbox')), 'owner': None}
            return ''
        යන්ත්_රය = self.가상기계들[විස්තාරක[2]]
        if ක්_රීයාව == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(නම), json.dumps(අගය)) for නම, අගය in යන්ත්_රය.items() if නම != 'owner')
        if ක්_රීයාව == 'getextradata': return 'Value: ' + යන්ත්_රය['owner'] if යන්ත්_රය['owner'] else 'No value set!'
        if ක්_රීයාව == 'setextradata': යන්ත්_රය['owner'] = විස්තාරක[4]
        elif ක්_රීයාව == 'storagectl': යන්ත්_රය['storagecontrollername0'] = 'JKOROS IDE'
        elif ක්_රීයාව == 'storageattach': යන්ත්_රය['JKOROS IDE-0-0'] = විස්තාරක[විස්තාරක.index('--medium') + 1]
        elif ක්_රීයාව == 'startvm': යන්ත්_රය['VMState'] = 'running'
        elif ක්_රීයාව == 'controlvm':
            assert විස්තාරක[3] == 'resume'
            යන්ත්_රය['VMState'] = 'running'
        elif ක්_රීයාව != 'modifyvm': raise AssertionError(විස්තාරක)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.ක්_රියාත්මක_කරන්න_විධානය = 모듈.යෙදු_යෙදුම්_ලාච්චුව(self.뿌리, 'jkoros operating system', විධානය=self.상자)

    def සාදන්න_පිවිසුම(self):
        결과 = self.ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(විධානය[0] == 'VBoxManage' and විධානය[1] in ('list', 'showvminfo', 'getextradata') for විධානය in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in විධානය and 'none' in විධානය for විධානය in self.상자.명령들))
        self.assertFalse(any('hdd' in විධානය or 'discardstate' in විධානය or 'createmedium' in විධානය for විධානය in self.상자.명령들))

    def test_실행중유지(self):
        self.සාදන්න_පිවිසුම()
        self.assertEqual(self.ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        යන්ත්_රය = self.සාදන්න_පිවිසුම()
        යන්ත්_රය['VMState'] = 'saved'
        ලොගය_අගය = self.ක්_රියාත්මක_කරන්න_විධානය.මාර්_ගය(self.ක්_රියාත්මක_කරන්න_විධානය.කියවීම()['serial_log'])
        ලොගය_අගය.write_text('saved log')
        self.ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය()
        self.assertFalse(any(විධානය[0] == 'make' or විධානය[1] == 'modifyvm' for විධානය in self.상자.명령들))
        self.assertEqual([මාර්_ගය.read_text() for මාර්_ගය in ලොගය_අගය.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.සාදන්න_පිවිසුම()['VMState'] = 'paused'
        self.ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය()
        self.assertTrue(any(විධානය[1] == 'controlvm' and විධානය[3] == 'resume' for විධානය in self.상자.명령들))
        self.assertFalse(any(විධානය[0] == 'make' for විධානය in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය()
        self.변경없음()

    def test_소유표식거부(self):
        self.සාදන්න_පිවිසුම()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.සාදන්න_පිවිසුම()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        යන්ත්_රය = self.සාදන්න_පිවිසුම()
        යන්ත්_රය['VMState'] = 'poweroff'
        යන්ත්_රය['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය()
        self.변경없음()

    def test_전환중거부(self):
        self.සාදන්න_පිවිසුම()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය()
        self.변경없음()

    def test_등록해제거부(self):
        self.සාදන්න_පිවිසුම()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        යන්ත්_රය = self.සාදන්න_පිවිසුම()
        යන්ත්_රය['VMState'] = 'poweroff'
        이전 = dict(යන්ත්_රය)
        self.상자.අසමත්වීම_අගය = 'make'
        with self.assertRaises(모듈.실행오류): self.ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය()
        self.assertEqual(යන්ත්_රය, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.අසමත්වීම_අගය = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය()
        self.상자.명령들.clear()
        self.assertEqual(self.ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය()['state'], 'running')
        self.assertFalse(any(විධානය[1] == 'createvm' for විධානය in self.상자.명령들))

    def test_보존ISO변조거부(self):
        යන්ත්_රය = self.සාදන්න_පිවිසුම()
        යන්ත්_රය['VMState'] = 'poweroff'
        Path(යන්ත්_රය['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය()

    def test_상태미생성(self):
        self.assertEqual(self.ක්_රියාත්මක_කරන්න_විධානය.දර්ශනය_තත්වය()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for මාර්_ගය in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.ක්_රියාත්මක_කරන්න_විධානය.මාර්_ගය(මාර්_ගය)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.ක්_රියාත්මක_කරන්න_විධානය.මාර්_ගය('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.ගුණාංගය_අගය('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
