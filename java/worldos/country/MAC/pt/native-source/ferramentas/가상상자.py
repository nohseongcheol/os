#!/usr/bin/env python3
"""jkoros 전용 VirtualBox app_Launcher. 기존 VM/디스크/Store_VALOR 상태는 삭제하지 않는다."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid


class execução_erro(RuntimeError):
    pass


def Executar_shell_comando(argumentos):
    ambiente = dict(os.environ, LC_ALL='C')
    resultado = subprocess.run([str(VALOR) for VALOR in argumentos], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=ambiente, timeout=180)
    Conteúdo_VALOR = resultado.stdout.decode('utf-8', 'replace')
    if resultado.returncode:
        raise execução_erro('comando falha_VALOR: ' + ' '.join(str(VALOR) for VALOR in argumentos) + '\n' + Conteúdo_VALOR[-10000:])
    return Conteúdo_VALOR


def valor_do_atributo(Conteúdo_VALOR):
    resultado = {}
    for linha_de_entrada in Conteúdo_VALOR.splitlines():
        if '=' not in linha_de_entrada:
            continue
        Nome, VALOR = linha_de_entrada.split('=', 1)
        if Nome.startswith('"'):
            Nome = json.loads(Nome)
        if VALOR.startswith('"'):
            try:
                leitura_VALOR, 끝 = json.JSONDecoder().raw_decode(VALOR)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALOR): VALOR = leitura_VALOR
            except ValueError:
                raise execução_erro('VirtualBox valor_do_atributo formato_VALOR erro: ' + linha_de_entrada)
        resultado[Nome] = VALOR
    return resultado


def 등록목록(Conteúdo_VALOR):
    resultado = {}
    for linha_de_entrada in Conteúdo_VALOR.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', linha_de_entrada)
        if 일치: resultado[일치.group(2).lower()] = 일치.group(1)
    return resultado


def soma_de_verificação(caminho):
    VALOR = hashlib.sha256()
    with caminho.open('rb') as ficheiro:
        for dados in iter(lambda: ficheiro.read(1024 * 1024), b''): VALOR.update(dados)
    return VALOR.hexdigest()


class app_Launcher:
    def __init__(self, raiz_VALOR, Nome, método_MODO='gui', comando=Executar_shell_comando):
        self.raiz_VALOR = Path(raiz_VALOR).resolve()
        self.Nome, self.método_MODO, self.comando = Nome, método_MODO, comando
        self.보관 = self.raiz_VALOR / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Nome) or Nome in ('.', '..'):
            raise execução_erro('VM 이름은 문자·dígito_VALOR·공백·밑줄·괄호·마침표·하이픈만 사용할 número 있습니다.')
        if método_MODO not in ('gui', 'headless'): raise execução_erro('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def caminho(self, par_VALOR):
        if Path(par_VALOR).is_absolute() or '..' in Path(par_VALOR).parts:
            raise execução_erro('잘못된 관리 caminho: ' + str(par_VALOR))
        resultado = self.보관
        for 부분 in ['.vbox'] + list(Path(par_VALOR).parts):
            if 부분 == '.vbox': resultado = self.보관
            else: resultado = resultado / 부분
            if resultado.is_symlink(): raise execução_erro('Ligar 경로는 사용하지 않습니다: ' + str(resultado))
        return resultado

    def Leitura(self):
        caminho = self.caminho('state.json')
        if not caminho.exists(): return None
        Estado_VALOR = json.loads(caminho.read_text(encoding='utf-8'))
        if Estado_VALOR.get('version') != 1 or Estado_VALOR.get('name') != self.Nome:
            raise execução_erro('관리 상태의 VM Nome/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Nome in ('uuid', 'owner'):
            if str(uuid.UUID(Estado_VALOR[Nome])) != Estado_VALOR[Nome]: raise execução_erro('잘못된 VM identificador_VALOR')
        return Estado_VALOR

    def Store_VALOR(self, Estado_VALOR):
        destino_VALOR = self.caminho('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ficheiro:
            json.dump(Estado_VALOR, ficheiro, ensure_ascii=False, indent=2)
            ficheiro.write('\n')
            임시 = ficheiro.name
        os.replace(임시, str(destino_VALOR))

    def msinfo32_exe(self, Estado_VALOR, 등록됨, recuperar_Estado=False):
        if Estado_VALOR['uuid'] not in 등록됨:
            raise execução_erro('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = valor_do_atributo(self.comando(['VBoxManage', 'showvminfo', Estado_VALOR['uuid'], '--machinereadable']))
        posição = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.caminho('machines').resolve() not in posição.parents or msinfo32_exe.get('UUID') != Estado_VALOR['uuid']:
            raise execução_erro('이 프로젝트의 VM Definições caminho/UUID와 일치하지 않아 변경하지 않습니다.')
        favorito_VALOR = self.comando(['VBoxManage', 'getextradata', Estado_VALOR['uuid'], 'JKOROS/Owner']).strip()
        if favorito_VALOR != 'Value: ' + Estado_VALOR['owner']:
            if recuperar_Estado and Estado_VALOR.get('pending') and favorito_VALOR == 'No value set!':
                self.comando(['VBoxManage', 'setextradata', Estado_VALOR['uuid'], 'JKOROS/Owner', Estado_VALOR['owner']])
            else:
                raise execução_erro('VM proprietário_VALOR 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def cheque_Mídia(self, Estado_VALOR, msinfo32_exe):
        제어기들 = [VALOR for Nome, VALOR in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nome)]
        Permitir_VALOR = [str(self.caminho(VALOR)) for VALOR in Estado_VALOR.get('media', [])]
        for Nome, VALOR in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(controle) + r'-\d+-\d+', Nome) for controle in 제어기들):
                if VALOR not in ('none', 'emptydrive') and VALOR not in Permitir_VALOR:
                    raise execução_erro('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALOR)

    def mostrar_Estado(self):
        Estado_VALOR = self.Leitura()
        if Estado_VALOR is None: return {'name': self.Nome, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Estado_VALOR, 등록목록(self.comando(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Estado_VALOR['name']), 'uuid': Estado_VALOR['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.caminho(Estado_VALOR['iso'])) if Estado_VALOR.get('iso') else None,
                'serial_log': str(self.caminho(Estado_VALOR['serial_log'])) if Estado_VALOR.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Executar_comando(self):
        Estado_VALOR = self.Leitura()
        등록됨 = 등록목록(self.comando(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Estado_VALOR is not None and Estado_VALOR['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Estado_VALOR, 등록됨, recuperar_Estado=True)
            em_dia_item = msinfo32_exe.get('VMState')
            if em_dia_item == 'running':
                print('이미 Executar_comando 중입니다. 재빌드·재시작하지 않습니다.')
                return self.mostrar_Estado()
            self.cheque_Mídia(Estado_VALOR, msinfo32_exe)
            if em_dia_item in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALOR 상태를 버리지 않습니다.'.format(em_dia_item))
                if em_dia_item == 'paused':
                    self.comando(['VBoxManage', 'controlvm', Estado_VALOR['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 repetir_VALOR Abrir 전에 기존 기록도 보관한다.
                    if Estado_VALOR.get('serial_log'):
                        원본 = self.caminho(Estado_VALOR['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.caminho('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.comando(['VBoxManage', 'startvm', Estado_VALOR['uuid'], '--type', self.método_MODO])
                return self.mostrar_Estado()
            if em_dia_item not in ('poweroff', 'aborted'):
                raise execução_erro('VM이 mudar_MODO 중입니다 ({}). 작업이 끝난 BACK_VALOR repetir_VALOR 실행하세요.'.format(em_dia_item))
        elif Estado_VALOR is not None and not Estado_VALOR.get('pending'):
            raise execução_erro('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 repetir_VALOR 등록하세요.')
        elif self.Nome in 등록됨.values():
            raise execução_erro('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALOR/Executar_comando 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.comando(['make', '-C', str(self.raiz_VALOR / 'os'), 'iso']), end='')
        원본 = self.raiz_VALOR / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise execução_erro('arranque_da_máquina ISO가 생성되지 않았습니다.')
        Mídia_VALOR = 'media/kernel-' + soma_de_verificação(원본) + '.iso'
        destino_VALOR = self.caminho(Mídia_VALOR)
        destino_VALOR.parent.mkdir(exist_ok=True)
        if destino_VALOR.exists():
            if soma_de_verificação(destino_VALOR) != soma_de_verificação(원본): raise execução_erro('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(destino_VALOR))
        else:
            with tempfile.NamedTemporaryFile(dir=str(destino_VALOR.parent)) as ficheiro:
                shutil.copyfile(str(원본), ficheiro.name)
                os.link(ficheiro.name, str(destino_VALOR))

        if Estado_VALOR is None:
            Estado_VALOR = {'version': 1, 'name': self.Nome, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALOR(Estado_VALOR)
        if msinfo32_exe is None:
            self.comando(['VBoxManage', 'createvm', '--name', Estado_VALOR['name'], '--uuid', Estado_VALOR['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.caminho('machines')), '--register'])
            self.comando(['VBoxManage', 'setextradata', Estado_VALOR['uuid'], 'JKOROS/Owner', Estado_VALOR['owner']])
        # construir 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Estado_VALOR, 등록목록(self.comando(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise execução_erro('construir 중 VM 상태가 바뀌었습니다. repetir_VALOR make vbox를 실행하세요.')
        self.cheque_Mídia(Estado_VALOR, msinfo32_exe)
        Estado_VALOR['iso'] = Mídia_VALOR
        if Mídia_VALOR not in Estado_VALOR['media']: Estado_VALOR['media'].append(Mídia_VALOR)
        Estado_VALOR['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALOR = self.caminho(Estado_VALOR['serial_log'])
        LOG_VALOR.parent.mkdir(exist_ok=True)
        self.Store_VALOR(Estado_VALOR)
        self.comando(['VBoxManage', 'modifyvm', Estado_VALOR['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALOR)])
        제어기들 = [VALOR for Nome, VALOR in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nome)]
        if 'JKOROS IDE' not in 제어기들:
            self.comando(['VBoxManage', 'storagectl', Estado_VALOR['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.comando(['VBoxManage', 'storageattach', Estado_VALOR['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(destino_VALOR)])
        Estado_VALOR['pending'] = False
        self.Store_VALOR(Estado_VALOR)
        self.comando(['VBoxManage', 'startvm', Estado_VALOR['uuid'], '--type', self.método_MODO])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.mostrar_Estado()


def iniciar():
    analisar_VALOR = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Executar_comando 및 Estado_VALOR consulta_VALOR')
    analisar_VALOR.add_argument('action', choices=['run', 'status'])
    parâmetro_argumento = analisar_VALOR.parse_args()
    Executar_comando = app_Launcher(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parâmetro_argumento.action == 'status':
        print(json.dumps(Executar_comando.mostrar_Estado(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise execução_erro('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise execução_erro('/dev/vboxdrv에 접근할 número 없습니다. host 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/Permissão_VALOR 변경은 하지 않습니다.')
    os.umask(0o077)
    Executar_comando.caminho('lock').parent.mkdir(parents=True, exist_ok=True)
    with Executar_comando.caminho('lock').open('a') as bloquear_VALOR:
        try: fcntl.flock(bloquear_VALOR, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise execução_erro('다른 jkoros VirtualBox Executar_comando 작업이 진행 중입니다.')
        print(json.dumps(Executar_comando.Executar_comando(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: iniciar()
    except (execução_erro, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as erro:
        print('VBOX erro: ' + str(erro), file=sys.stderr)
        sys.exit(1)
