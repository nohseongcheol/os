import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Ma_ana_Daraja = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
shiri_Daraja = importlib.util.module_from_spec(Ma_ana_Daraja)
Ma_ana_Daraja.loader.exec_module(shiri_Daraja)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.Kasa_aiki_Daraja = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.Kasa_aiki_Daraja == 인수[1] or (인수[0] == 'make' and self.Kasa_aiki_Daraja == 'make'):
            self.Kasa_aiki_Daraja = None
            raise shiri_Daraja.실행오류('시험용 Kasa_aiki_Daraja')
        if 인수[0] == 'make':
            Hanyar_shiga = self.뿌리 / 'os/build/kernel.iso'
            Hanyar_shiga.parent.mkdir(parents=True, exist_ok=True)
            Hanyar_shiga.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Aiki = 인수[1]
        if Aiki == 'list':
            return '\n'.join('"{}" {{{}}}'.format(Daraja['name'], Indes) for Indes, Daraja in self.가상기계들.items())
        if Aiki == 'createvm':
            Indes, Suna = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[Indes] = {'UUID': Indes, 'name': Suna, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Suna / (Suna + '.vbox')), 'owner': None}
            return ''
        na_ura_mai_kwakwalwa = self.가상기계들[인수[2]]
        if Aiki == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Suna), json.dumps(Daraja)) for Suna, Daraja in na_ura_mai_kwakwalwa.items() if Suna != 'owner')
        if Aiki == 'getextradata': return 'Value: ' + na_ura_mai_kwakwalwa['owner'] if na_ura_mai_kwakwalwa['owner'] else 'No value set!'
        if Aiki == 'setextradata': na_ura_mai_kwakwalwa['owner'] = 인수[4]
        elif Aiki == 'storagectl': na_ura_mai_kwakwalwa['storagecontrollername0'] = 'JKOROS IDE'
        elif Aiki == 'storageattach': na_ura_mai_kwakwalwa['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Aiki == 'startvm': na_ura_mai_kwakwalwa['VMState'] = 'running'
        elif Aiki == 'controlvm':
            assert 인수[3] == 'resume'
            na_ura_mai_kwakwalwa['VMState'] = 'running'
        elif Aiki != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.gudanar_Umarni = shiri_Daraja.Shiri_Mai_Fara_Ka_ida(self.뿌리, 'jkoros operating system', Umarni=self.상자)

    def ƙirƙíra_Mashigar_bayanai(self):
        결과 = self.gudanar_Umarni.gudanar_Umarni()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Umarni[0] == 'VBoxManage' and Umarni[1] in ('list', 'showvminfo', 'getextradata') for Umarni in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.gudanar_Umarni.gudanar_Umarni()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in Umarni and 'none' in Umarni for Umarni in self.상자.명령들))
        self.assertFalse(any('hdd' in Umarni or 'discardstate' in Umarni or 'createmedium' in Umarni for Umarni in self.상자.명령들))

    def test_실행중유지(self):
        self.ƙirƙíra_Mashigar_bayanai()
        self.assertEqual(self.gudanar_Umarni.gudanar_Umarni()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        na_ura_mai_kwakwalwa = self.ƙirƙíra_Mashigar_bayanai()
        na_ura_mai_kwakwalwa['VMState'] = 'saved'
        logu_Daraja = self.gudanar_Umarni.Hanyar_shiga(self.gudanar_Umarni.Yi_Karatu()['serial_log'])
        logu_Daraja.write_text('saved log')
        self.gudanar_Umarni.gudanar_Umarni()
        self.assertFalse(any(Umarni[0] == 'make' or Umarni[1] == 'modifyvm' for Umarni in self.상자.명령들))
        self.assertEqual([Hanyar_shiga.read_text() for Hanyar_shiga in logu_Daraja.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.ƙirƙíra_Mashigar_bayanai()['VMState'] = 'paused'
        self.gudanar_Umarni.gudanar_Umarni()
        self.assertTrue(any(Umarni[1] == 'controlvm' and Umarni[3] == 'resume' for Umarni in self.상자.명령들))
        self.assertFalse(any(Umarni[0] == 'make' for Umarni in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(shiri_Daraja.실행오류): self.gudanar_Umarni.gudanar_Umarni()
        self.변경없음()

    def test_소유표식거부(self):
        self.ƙirƙíra_Mashigar_bayanai()['owner'] = 'someone-else'
        with self.assertRaises(shiri_Daraja.실행오류): self.gudanar_Umarni.gudanar_Umarni()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.ƙirƙíra_Mashigar_bayanai()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(shiri_Daraja.실행오류): self.gudanar_Umarni.gudanar_Umarni()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        na_ura_mai_kwakwalwa = self.ƙirƙíra_Mashigar_bayanai()
        na_ura_mai_kwakwalwa['VMState'] = 'poweroff'
        na_ura_mai_kwakwalwa['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(shiri_Daraja.실행오류): self.gudanar_Umarni.gudanar_Umarni()
        self.변경없음()

    def test_전환중거부(self):
        self.ƙirƙíra_Mashigar_bayanai()['VMState'] = 'saving'
        with self.assertRaises(shiri_Daraja.실행오류): self.gudanar_Umarni.gudanar_Umarni()
        self.변경없음()

    def test_등록해제거부(self):
        self.ƙirƙíra_Mashigar_bayanai()
        self.상자.가상기계들.clear()
        with self.assertRaises(shiri_Daraja.실행오류): self.gudanar_Umarni.gudanar_Umarni()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        na_ura_mai_kwakwalwa = self.ƙirƙíra_Mashigar_bayanai()
        na_ura_mai_kwakwalwa['VMState'] = 'poweroff'
        이전 = dict(na_ura_mai_kwakwalwa)
        self.상자.Kasa_aiki_Daraja = 'make'
        with self.assertRaises(shiri_Daraja.실행오류): self.gudanar_Umarni.gudanar_Umarni()
        self.assertEqual(na_ura_mai_kwakwalwa, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.Kasa_aiki_Daraja = 'setextradata'
        with self.assertRaises(shiri_Daraja.실행오류): self.gudanar_Umarni.gudanar_Umarni()
        self.상자.명령들.clear()
        self.assertEqual(self.gudanar_Umarni.gudanar_Umarni()['state'], 'running')
        self.assertFalse(any(Umarni[1] == 'createvm' for Umarni in self.상자.명령들))

    def test_보존ISO변조거부(self):
        na_ura_mai_kwakwalwa = self.ƙirƙíra_Mashigar_bayanai()
        na_ura_mai_kwakwalwa['VMState'] = 'poweroff'
        Path(na_ura_mai_kwakwalwa['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(shiri_Daraja.실행오류): self.gudanar_Umarni.gudanar_Umarni()

    def test_상태미생성(self):
        self.assertEqual(self.gudanar_Umarni.Nuna_Matsayi()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Hanyar_shiga in ('../outside', '/tmp/outside'):
            with self.assertRaises(shiri_Daraja.실행오류): self.gudanar_Umarni.Hanyar_shiga(Hanyar_shiga)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(shiri_Daraja.실행오류): self.gudanar_Umarni.Hanyar_shiga('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = shiri_Daraja.siffofi_Daraja('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
