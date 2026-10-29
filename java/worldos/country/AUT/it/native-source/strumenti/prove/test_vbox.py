import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

definizione_VALORE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modulo_VALORE = importlib.util.module_from_spec(definizione_VALORE)
definizione_VALORE.loader.exec_module(modulo_VALORE)


class 가짜상자:
    def __init__(self, radice_VALORE):
        self.radice_VALORE = radice_VALORE
        self.명령들 = []
        self.Macchine_virtuali = {}
        self.errore_VALORE = None

    def __call__(self, argomenti):
        argomenti = list(map(str, argomenti))
        self.명령들.append(argomenti)
        if self.errore_VALORE == argomenti[1] or (argomenti[0] == 'make' and self.errore_VALORE == 'make'):
            self.errore_VALORE = None
            raise modulo_VALORE.esecuzione_errore('시험용 errore_VALORE')
        if argomenti[0] == 'make':
            percorso = self.radice_VALORE / 'os/build/kernel.iso'
            percorso.parent.mkdir(parents=True, exist_ok=True)
            percorso.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Azione = argomenti[1]
        if Azione == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALORE['name'], INDICE) for INDICE, VALORE in self.Macchine_virtuali.items())
        if Azione == 'createvm':
            INDICE, Nome = argomenti[argomenti.index('--uuid') + 1], argomenti[argomenti.index('--name') + 1]
            self.Macchine_virtuali[INDICE] = {'UUID': INDICE, 'name': Nome, 'VMState': 'poweroff',
                'CfgFile': str(self.radice_VALORE / '.vbox/machines' / Nome / (Nome + '.vbox')), 'owner': None}
            return ''
        computer = self.Macchine_virtuali[argomenti[2]]
        if Azione == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Nome), json.dumps(VALORE)) for Nome, VALORE in computer.items() if Nome != 'owner')
        if Azione == 'getextradata': return 'Value: ' + computer['owner'] if computer['owner'] else 'No value set!'
        if Azione == 'setextradata': computer['owner'] = argomenti[4]
        elif Azione == 'storagectl': computer['storagecontrollername0'] = 'JKOROS IDE'
        elif Azione == 'storageattach': computer['JKOROS IDE-0-0'] = argomenti[argomenti.index('--medium') + 1]
        elif Azione == 'startvm': computer['VMState'] = 'running'
        elif Azione == 'controlvm':
            assert argomenti[3] == 'resume'
            computer['VMState'] = 'running'
        elif Azione != 'modifyvm': raise AssertionError(argomenti)
        return ''


class esecuzione_dei_test(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.radice_VALORE = Path(self.임시.name)
        (self.radice_VALORE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.radice_VALORE)
        self.Esegui_comando = modulo_VALORE.app_Launcher(self.radice_VALORE, 'jkoros operating system', comando=self.상자)

    def Crea_voce(self):
        risultato = self.Esegui_comando.Esegui_comando()
        self.상자.명령들.clear()
        return self.상자.Macchine_virtuali[risultato['uuid']]

    def 변경없음(self):
        self.assertTrue(all(comando[0] == 'VBoxManage' and comando[1] in ('list', 'showvminfo', 'getextradata') for comando in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        risultato = self.Esegui_comando.Esegui_comando()
        self.assertEqual(risultato['state'], 'running')
        self.assertTrue(Path(risultato['iso']).is_file())
        self.assertTrue(any('--nic1' in comando and 'none' in comando for comando in self.상자.명령들))
        self.assertFalse(any('hdd' in comando or 'discardstate' in comando or 'createmedium' in comando for comando in self.상자.명령들))

    def test_실행중유지(self):
        self.Crea_voce()
        self.assertEqual(self.Esegui_comando.Esegui_comando()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        computer = self.Crea_voce()
        computer['VMState'] = 'saved'
        LOG_VALORE = self.Esegui_comando.percorso(self.Esegui_comando.Lettura()['serial_log'])
        LOG_VALORE.write_text('saved log')
        self.Esegui_comando.Esegui_comando()
        self.assertFalse(any(comando[0] == 'make' or comando[1] == 'modifyvm' for comando in self.상자.명령들))
        self.assertEqual([percorso.read_text() for percorso in LOG_VALORE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_Pause_E_CV(self):
        self.Crea_voce()['VMState'] = 'paused'
        self.Esegui_comando.Esegui_comando()
        self.assertTrue(any(comando[1] == 'controlvm' and comando[3] == 'resume' for comando in self.상자.명령들))
        self.assertFalse(any(comando[0] == 'make' for comando in self.상자.명령들))

    def test_Altro_VM_nome_collisione(self):
        self.상자.Macchine_virtuali[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modulo_VALORE.esecuzione_errore): self.Esegui_comando.Esegui_comando()
        self.변경없음()

    def test_소유표식거부(self):
        self.Crea_voce()['owner'] = 'someone-else'
        with self.assertRaises(modulo_VALORE.esecuzione_errore): self.Esegui_comando.Esegui_comando()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Crea_voce()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modulo_VALORE.esecuzione_errore): self.Esegui_comando.Esegui_comando()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        computer = self.Crea_voce()
        computer['VMState'] = 'poweroff'
        computer['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modulo_VALORE.esecuzione_errore): self.Esegui_comando.Esegui_comando()
        self.변경없음()

    def test_전환중거부(self):
        self.Crea_voce()['VMState'] = 'saving'
        with self.assertRaises(modulo_VALORE.esecuzione_errore): self.Esegui_comando.Esegui_comando()
        self.변경없음()

    def test_등록해제거부(self):
        self.Crea_voce()
        self.상자.Macchine_virtuali.clear()
        with self.assertRaises(modulo_VALORE.esecuzione_errore): self.Esegui_comando.Esegui_comando()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        computer = self.Crea_voce()
        computer['VMState'] = 'poweroff'
        Indietro_articolo = dict(computer)
        self.상자.errore_VALORE = 'make'
        with self.assertRaises(modulo_VALORE.esecuzione_errore): self.Esegui_comando.Esegui_comando()
        self.assertEqual(computer, Indietro_articolo)

    def test_중단된소유표식설정복구(self):
        self.상자.errore_VALORE = 'setextradata'
        with self.assertRaises(modulo_VALORE.esecuzione_errore): self.Esegui_comando.Esegui_comando()
        self.상자.명령들.clear()
        self.assertEqual(self.Esegui_comando.Esegui_comando()['state'], 'running')
        self.assertFalse(any(comando[1] == 'createvm' for comando in self.상자.명령들))

    def test_보존ISO변조거부(self):
        computer = self.Crea_voce()
        computer['VMState'] = 'poweroff'
        Path(computer['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modulo_VALORE.esecuzione_errore): self.Esegui_comando.Esegui_comando()

    def test_상태미생성(self):
        self.assertEqual(self.Esegui_comando.mostrare_Stato()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for percorso in ('../outside', '/tmp/outside'):
            with self.assertRaises(modulo_VALORE.esecuzione_errore): self.Esegui_comando.percorso(percorso)
        (self.radice_VALORE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modulo_VALORE.esecuzione_errore): self.Esegui_comando.percorso('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        risultato = modulo_VALORE.valore_dell_attributo('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(risultato['VMState'], 'running')
        self.assertEqual(risultato['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
