import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definició_VALOR = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
mòdul_VALOR = importlib.util.module_from_spec(Definició_VALOR)
Definició_VALOR.loader.exec_module(mòdul_VALOR)


class 가짜상자:
    def __init__(self, rel_VALOR):
        self.rel_VALOR = rel_VALOR
        self.명령들 = []
        self.가상기계들 = {}
        self.error_VALOR = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.error_VALOR == 인수[1] or (인수[0] == 'make' and self.error_VALOR == 'make'):
            self.error_VALOR = None
            raise mòdul_VALOR.실행오류('시험용 error_VALOR')
        if 인수[0] == 'make':
            Camí = self.rel_VALOR / 'os/build/kernel.iso'
            Camí.parent.mkdir(parents=True, exist_ok=True)
            Camí.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Acció = 인수[1]
        if Acció == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALOR['name'], INDEX) for INDEX, VALOR in self.가상기계들.items())
        if Acció == 'createvm':
            INDEX, Nom = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Nom, 'VMState': 'poweroff',
                'CfgFile': str(self.rel_VALOR / '.vbox/machines' / Nom / (Nom + '.vbox')), 'owner': None}
            return ''
        màquina = self.가상기계들[인수[2]]
        if Acció == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Nom), json.dumps(VALOR)) for Nom, VALOR in màquina.items() if Nom != 'owner')
        if Acció == 'getextradata': return 'Value: ' + màquina['owner'] if màquina['owner'] else 'No value set!'
        if Acció == 'setextradata': màquina['owner'] = 인수[4]
        elif Acció == 'storagectl': màquina['storagecontrollername0'] = 'JKOROS IDE'
        elif Acció == 'storageattach': màquina['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Acció == 'startvm': màquina['VMState'] = 'running'
        elif Acció == 'controlvm':
            assert 인수[3] == 'resume'
            màquina['VMState'] = 'running'
        elif Acció != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.rel_VALOR = Path(self.임시.name)
        (self.rel_VALOR / '.vbox').mkdir()
        self.상자 = 가짜상자(self.rel_VALOR)
        self.Executa_ordre = mòdul_VALOR.programa_iniciador(self.rel_VALOR, 'jkoros operating system', Ordre=self.상자)

    def Crear_introducció(self):
        RESULTAT = self.Executa_ordre.Executa_ordre()
        self.상자.명령들.clear()
        return self.상자.가상기계들[RESULTAT['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Ordre[0] == 'VBoxManage' and Ordre[1] in ('list', 'showvminfo', 'getextradata') for Ordre in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        RESULTAT = self.Executa_ordre.Executa_ordre()
        self.assertEqual(RESULTAT['state'], 'running')
        self.assertTrue(Path(RESULTAT['iso']).is_file())
        self.assertTrue(any('--nic1' in Ordre and 'none' in Ordre for Ordre in self.상자.명령들))
        self.assertFalse(any('hdd' in Ordre or 'discardstate' in Ordre or 'createmedium' in Ordre for Ordre in self.상자.명령들))

    def test_실행중유지(self):
        self.Crear_introducció()
        self.assertEqual(self.Executa_ordre.Executa_ordre()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        màquina = self.Crear_introducció()
        màquina['VMState'] = 'saved'
        LOG_VALOR = self.Executa_ordre.Camí(self.Executa_ordre.Lectura()['serial_log'])
        LOG_VALOR.write_text('saved log')
        self.Executa_ordre.Executa_ordre()
        self.assertFalse(any(Ordre[0] == 'make' or Ordre[1] == 'modifyvm' for Ordre in self.상자.명령들))
        self.assertEqual([Camí.read_text() for Camí in LOG_VALOR.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Crear_introducció()['VMState'] = 'paused'
        self.Executa_ordre.Executa_ordre()
        self.assertTrue(any(Ordre[1] == 'controlvm' and Ordre[3] == 'resume' for Ordre in self.상자.명령들))
        self.assertFalse(any(Ordre[0] == 'make' for Ordre in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(mòdul_VALOR.실행오류): self.Executa_ordre.Executa_ordre()
        self.변경없음()

    def test_소유표식거부(self):
        self.Crear_introducció()['owner'] = 'someone-else'
        with self.assertRaises(mòdul_VALOR.실행오류): self.Executa_ordre.Executa_ordre()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Crear_introducció()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(mòdul_VALOR.실행오류): self.Executa_ordre.Executa_ordre()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        màquina = self.Crear_introducció()
        màquina['VMState'] = 'poweroff'
        màquina['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(mòdul_VALOR.실행오류): self.Executa_ordre.Executa_ordre()
        self.변경없음()

    def test_전환중거부(self):
        self.Crear_introducció()['VMState'] = 'saving'
        with self.assertRaises(mòdul_VALOR.실행오류): self.Executa_ordre.Executa_ordre()
        self.변경없음()

    def test_등록해제거부(self):
        self.Crear_introducció()
        self.상자.가상기계들.clear()
        with self.assertRaises(mòdul_VALOR.실행오류): self.Executa_ordre.Executa_ordre()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        màquina = self.Crear_introducció()
        màquina['VMState'] = 'poweroff'
        이전 = dict(màquina)
        self.상자.error_VALOR = 'make'
        with self.assertRaises(mòdul_VALOR.실행오류): self.Executa_ordre.Executa_ordre()
        self.assertEqual(màquina, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.error_VALOR = 'setextradata'
        with self.assertRaises(mòdul_VALOR.실행오류): self.Executa_ordre.Executa_ordre()
        self.상자.명령들.clear()
        self.assertEqual(self.Executa_ordre.Executa_ordre()['state'], 'running')
        self.assertFalse(any(Ordre[1] == 'createvm' for Ordre in self.상자.명령들))

    def test_보존ISO변조거부(self):
        màquina = self.Crear_introducció()
        màquina['VMState'] = 'poweroff'
        Path(màquina['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(mòdul_VALOR.실행오류): self.Executa_ordre.Executa_ordre()

    def test_상태미생성(self):
        self.assertEqual(self.Executa_ordre.mostrar_Estat()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Camí in ('../outside', '/tmp/outside'):
            with self.assertRaises(mòdul_VALOR.실행오류): self.Executa_ordre.Camí(Camí)
        (self.rel_VALOR / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(mòdul_VALOR.실행오류): self.Executa_ordre.Camí('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        RESULTAT = mòdul_VALOR.valor_d_atribut('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(RESULTAT['VMState'], 'running')
        self.assertEqual(RESULTAT['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
