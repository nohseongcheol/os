import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Igisobanuro_agaciro = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(Igisobanuro_agaciro)
Igisobanuro_agaciro.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.kudakora_agaciro = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.kudakora_agaciro == 인수[1] or (인수[0] == 'make' and self.kudakora_agaciro == 'make'):
            self.kudakora_agaciro = None
            raise 모듈.실행오류('시험용 kudakora_agaciro')
        if 인수[0] == 'make':
            Inzira = self.뿌리 / 'os/build/kernel.iso'
            Inzira.parent.mkdir(parents=True, exist_ok=True)
            Inzira.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Igikorwa = 인수[1]
        if Igikorwa == 'list':
            return '\n'.join('"{}" {{{}}}'.format(agaciro['name'], umugerekashakiro) for umugerekashakiro, agaciro in self.가상기계들.items())
        if Igikorwa == 'createvm':
            umugerekashakiro, Izina = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[umugerekashakiro] = {'UUID': umugerekashakiro, 'name': Izina, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Izina / (Izina + '.vbox')), 'owner': None}
            return ''
        imashini = self.가상기계들[인수[2]]
        if Igikorwa == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Izina), json.dumps(agaciro)) for Izina, agaciro in imashini.items() if Izina != 'owner')
        if Igikorwa == 'getextradata': return 'Value: ' + imashini['owner'] if imashini['owner'] else 'No value set!'
        if Igikorwa == 'setextradata': imashini['owner'] = 인수[4]
        elif Igikorwa == 'storagectl': imashini['storagecontrollername0'] = 'JKOROS IDE'
        elif Igikorwa == 'storageattach': imashini['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Igikorwa == 'startvm': imashini['VMState'] = 'running'
        elif Igikorwa == 'controlvm':
            assert 인수[3] == 'resume'
            imashini['VMState'] = 'running'
        elif Igikorwa != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.gukora_ibwiriza = 모듈.porogaramu_umukozi(self.뿌리, 'jkoros operating system', Icyo_wifuza=self.상자)

    def kurema_icyinjizwa(self):
        결과 = self.gukora_ibwiriza.gukora_ibwiriza()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Icyo_wifuza[0] == 'VBoxManage' and Icyo_wifuza[1] in ('list', 'showvminfo', 'getextradata') for Icyo_wifuza in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.gukora_ibwiriza.gukora_ibwiriza()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in Icyo_wifuza and 'none' in Icyo_wifuza for Icyo_wifuza in self.상자.명령들))
        self.assertFalse(any('hdd' in Icyo_wifuza or 'discardstate' in Icyo_wifuza or 'createmedium' in Icyo_wifuza for Icyo_wifuza in self.상자.명령들))

    def test_실행중유지(self):
        self.kurema_icyinjizwa()
        self.assertEqual(self.gukora_ibwiriza.gukora_ibwiriza()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        imashini = self.kurema_icyinjizwa()
        imashini['VMState'] = 'saved'
        kubika_agaciro = self.gukora_ibwiriza.Inzira(self.gukora_ibwiriza.읽기()['serial_log'])
        kubika_agaciro.write_text('saved log')
        self.gukora_ibwiriza.gukora_ibwiriza()
        self.assertFalse(any(Icyo_wifuza[0] == 'make' or Icyo_wifuza[1] == 'modifyvm' for Icyo_wifuza in self.상자.명령들))
        self.assertEqual([Inzira.read_text() for Inzira in kubika_agaciro.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.kurema_icyinjizwa()['VMState'] = 'paused'
        self.gukora_ibwiriza.gukora_ibwiriza()
        self.assertTrue(any(Icyo_wifuza[1] == 'controlvm' and Icyo_wifuza[3] == 'resume' for Icyo_wifuza in self.상자.명령들))
        self.assertFalse(any(Icyo_wifuza[0] == 'make' for Icyo_wifuza in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.gukora_ibwiriza.gukora_ibwiriza()
        self.변경없음()

    def test_소유표식거부(self):
        self.kurema_icyinjizwa()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.gukora_ibwiriza.gukora_ibwiriza()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.kurema_icyinjizwa()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.gukora_ibwiriza.gukora_ibwiriza()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        imashini = self.kurema_icyinjizwa()
        imashini['VMState'] = 'poweroff'
        imashini['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.gukora_ibwiriza.gukora_ibwiriza()
        self.변경없음()

    def test_전환중거부(self):
        self.kurema_icyinjizwa()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.gukora_ibwiriza.gukora_ibwiriza()
        self.변경없음()

    def test_등록해제거부(self):
        self.kurema_icyinjizwa()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.gukora_ibwiriza.gukora_ibwiriza()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        imashini = self.kurema_icyinjizwa()
        imashini['VMState'] = 'poweroff'
        이전 = dict(imashini)
        self.상자.kudakora_agaciro = 'make'
        with self.assertRaises(모듈.실행오류): self.gukora_ibwiriza.gukora_ibwiriza()
        self.assertEqual(imashini, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.kudakora_agaciro = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.gukora_ibwiriza.gukora_ibwiriza()
        self.상자.명령들.clear()
        self.assertEqual(self.gukora_ibwiriza.gukora_ibwiriza()['state'], 'running')
        self.assertFalse(any(Icyo_wifuza[1] == 'createvm' for Icyo_wifuza in self.상자.명령들))

    def test_보존ISO변조거부(self):
        imashini = self.kurema_icyinjizwa()
        imashini['VMState'] = 'poweroff'
        Path(imashini['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.gukora_ibwiriza.gukora_ibwiriza()

    def test_상태미생성(self):
        self.assertEqual(self.gukora_ibwiriza.kugaragaza_imimerere()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Inzira in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.gukora_ibwiriza.Inzira(Inzira)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.gukora_ibwiriza.Inzira('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.ikiranga_agaciro('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
