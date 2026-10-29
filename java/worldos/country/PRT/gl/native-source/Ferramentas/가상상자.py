#!/usr/bin/env python3
"""jkoros 전용 VirtualBox apl_iniciador. 기존 VM/디스크/Store_VALOR 상태는 삭제하지 않는다."""
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


class 실행오류(RuntimeError):
    pass


def executar_shell_comando(Argumentos):
    환경 = dict(os.environ, LC_ALL='C')
    RESULTANTE = subprocess.run([str(VALOR) for VALOR in Argumentos], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Contido_VALOR = RESULTANTE.stdout.decode('utf-8', 'replace')
    if RESULTANTE.returncode:
        raise 실행오류('Orde erro_VALOR: ' + ' '.join(str(VALOR) for VALOR in Argumentos) + '\n' + Contido_VALOR[-10000:])
    return Contido_VALOR


def atributo_VALOR(Contido_VALOR):
    RESULTANTE = {}
    for Liña in Contido_VALOR.splitlines():
        if '=' not in Liña:
            continue
        Nome, VALOR = Liña.split('=', 1)
        if Nome.startswith('"'):
            Nome = json.loads(Nome)
        if VALOR.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALOR)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALOR): VALOR = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox atributo_VALOR formato_VALOR ERRO: ' + Liña)
        RESULTANTE[Nome] = VALOR
    return RESULTANTE


def 등록목록(Contido_VALOR):
    RESULTANTE = {}
    for Liña in Contido_VALOR.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Liña)
        if 일치: RESULTANTE[일치.group(2).lower()] = 일치.group(1)
    return RESULTANTE


def suma_de_comprobación(CAMIÑO):
    VALOR = hashlib.sha256()
    with CAMIÑO.open('rb') as Ficheiro:
        for datos in iter(lambda: Ficheiro.read(1024 * 1024), b''): VALOR.update(datos)
    return VALOR.hexdigest()


class apl_iniciador:
    def __init__(self, raíz_VALOR, Nome, 방식='gui', Orde=executar_shell_comando):
        self.raíz_VALOR = Path(raíz_VALOR).resolve()
        self.Nome, self.방식, self.Orde = Nome, 방식, Orde
        self.보관 = self.raíz_VALOR / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Nome) or Nome in ('.', '..'):
            raise 실행오류('VM 이름은 문자·díxito_VALOR·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if 방식 not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def CAMIÑO(self, punto_VALOR):
        if Path(punto_VALOR).is_absolute() or '..' in Path(punto_VALOR).parts:
            raise 실행오류('잘못된 관리 CAMIÑO: ' + str(punto_VALOR))
        RESULTANTE = self.보관
        for 부분 in ['.vbox'] + list(Path(punto_VALOR).parts):
            if 부분 == '.vbox': RESULTANTE = self.보관
            else: RESULTANTE = RESULTANTE / 부분
            if RESULTANTE.is_symlink(): raise 실행오류('Conectar 경로는 사용하지 않습니다: ' + str(RESULTANTE))
        return RESULTANTE

    def Lectura(self):
        CAMIÑO = self.CAMIÑO('state.json')
        if not CAMIÑO.exists(): return None
        Estado_VALOR = json.loads(CAMIÑO.read_text(encoding='utf-8'))
        if Estado_VALOR.get('version') != 1 or Estado_VALOR.get('name') != self.Nome:
            raise 실행오류('관리 상태의 VM Nome/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Nome in ('uuid', 'owner'):
            if str(uuid.UUID(Estado_VALOR[Nome])) != Estado_VALOR[Nome]: raise 실행오류('잘못된 VM 식별자')
        return Estado_VALOR

    def Store_VALOR(self, Estado_VALOR):
        destino_VALOR = self.CAMIÑO('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Ficheiro:
            json.dump(Estado_VALOR, Ficheiro, ensure_ascii=False, indent=2)
            Ficheiro.write('\n')
            임시 = Ficheiro.name
        os.replace(임시, str(destino_VALOR))

    def msinfo32_exe(self, Estado_VALOR, 등록됨, recuperar_Estado=False):
        if Estado_VALOR['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = atributo_VALOR(self.Orde(['VBoxManage', 'showvminfo', Estado_VALOR['uuid'], '--machinereadable']))
        Posición = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.CAMIÑO('machines').resolve() not in Posición.parents or msinfo32_exe.get('UUID') != Estado_VALOR['uuid']:
            raise 실행오류('이 프로젝트의 VM Configuración CAMIÑO/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Orde(['VBoxManage', 'getextradata', Estado_VALOR['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + Estado_VALOR['owner']:
            if recuperar_Estado and Estado_VALOR.get('pending') and 표식 == 'No value set!':
                self.Orde(['VBoxManage', 'setextradata', Estado_VALOR['uuid'], 'JKOROS/Owner', Estado_VALOR['owner']])
            else:
                raise 실행오류('VM propietario_VALOR 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def cheque_soporte(self, Estado_VALOR, msinfo32_exe):
        제어기들 = [VALOR for Nome, VALOR in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nome)]
        Permitir_VALOR = [str(self.CAMIÑO(VALOR)) for VALOR in Estado_VALOR.get('media', [])]
        for Nome, VALOR in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(mando) + r'-\d+-\d+', Nome) for mando in 제어기들):
                if VALOR not in ('none', 'emptydrive') and VALOR not in Permitir_VALOR:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALOR)

    def mostrar_Estado(self):
        Estado_VALOR = self.Lectura()
        if Estado_VALOR is None: return {'name': self.Nome, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Estado_VALOR, 등록목록(self.Orde(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Estado_VALOR['name']), 'uuid': Estado_VALOR['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.CAMIÑO(Estado_VALOR['iso'])) if Estado_VALOR.get('iso') else None,
                'serial_log': str(self.CAMIÑO(Estado_VALOR['serial_log'])) if Estado_VALOR.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def executar_comando(self):
        Estado_VALOR = self.Lectura()
        등록됨 = 등록목록(self.Orde(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Estado_VALOR is not None and Estado_VALOR['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Estado_VALOR, 등록됨, recuperar_Estado=True)
            ao_corrente_elemento = msinfo32_exe.get('VMState')
            if ao_corrente_elemento == 'running':
                print('이미 executar_comando 중입니다. 재빌드·재시작하지 않습니다.')
                return self.mostrar_Estado()
            self.cheque_soporte(Estado_VALOR, msinfo32_exe)
            if ao_corrente_elemento in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALOR 상태를 버리지 않습니다.'.format(ao_corrente_elemento))
                if ao_corrente_elemento == 'paused':
                    self.Orde(['VBoxManage', 'controlvm', Estado_VALOR['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Abrir 전에 기존 기록도 보관한다.
                    if Estado_VALOR.get('serial_log'):
                        원본 = self.CAMIÑO(Estado_VALOR['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.CAMIÑO('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Orde(['VBoxManage', 'startvm', Estado_VALOR['uuid'], '--type', self.방식])
                return self.mostrar_Estado()
            if ao_corrente_elemento not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 mudar_MODO 중입니다 ({}). 작업이 끝난 ATRÁS_VALOR 다시 실행하세요.'.format(ao_corrente_elemento))
        elif Estado_VALOR is not None and not Estado_VALOR.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Nome in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALOR/executar_comando 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Orde(['make', '-C', str(self.raíz_VALOR / 'os'), 'iso']), end='')
        원본 = self.raíz_VALOR / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        soporte_VALOR_e2cae547 = 'media/kernel-' + suma_de_comprobación(원본) + '.iso'
        destino_VALOR = self.CAMIÑO(soporte_VALOR_e2cae547)
        destino_VALOR.parent.mkdir(exist_ok=True)
        if destino_VALOR.exists():
            if suma_de_comprobación(destino_VALOR) != suma_de_comprobación(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(destino_VALOR))
        else:
            with tempfile.NamedTemporaryFile(dir=str(destino_VALOR.parent)) as Ficheiro:
                shutil.copyfile(str(원본), Ficheiro.name)
                os.link(Ficheiro.name, str(destino_VALOR))

        if Estado_VALOR is None:
            Estado_VALOR = {'version': 1, 'name': self.Nome, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALOR(Estado_VALOR)
        if msinfo32_exe is None:
            self.Orde(['VBoxManage', 'createvm', '--name', Estado_VALOR['name'], '--uuid', Estado_VALOR['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.CAMIÑO('machines')), '--register'])
            self.Orde(['VBoxManage', 'setextradata', Estado_VALOR['uuid'], 'JKOROS/Owner', Estado_VALOR['owner']])
        # compilar_sistema 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Estado_VALOR, 등록목록(self.Orde(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('compilar_sistema 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.cheque_soporte(Estado_VALOR, msinfo32_exe)
        Estado_VALOR['iso'] = soporte_VALOR_e2cae547
        if soporte_VALOR_e2cae547 not in Estado_VALOR['media']: Estado_VALOR['media'].append(soporte_VALOR_e2cae547)
        Estado_VALOR['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALOR = self.CAMIÑO(Estado_VALOR['serial_log'])
        LOG_VALOR.parent.mkdir(exist_ok=True)
        self.Store_VALOR(Estado_VALOR)
        self.Orde(['VBoxManage', 'modifyvm', Estado_VALOR['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALOR)])
        제어기들 = [VALOR for Nome, VALOR in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nome)]
        if 'JKOROS IDE' not in 제어기들:
            self.Orde(['VBoxManage', 'storagectl', Estado_VALOR['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Orde(['VBoxManage', 'storageattach', Estado_VALOR['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(destino_VALOR)])
        Estado_VALOR['pending'] = False
        self.Store_VALOR(Estado_VALOR)
        self.Orde(['VBoxManage', 'startvm', Estado_VALOR['uuid'], '--type', self.방식])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.mostrar_Estado()


def Executar_2():
    analizar_VALOR = argparse.ArgumentParser(description='jkoros 전용 VirtualBox executar_comando 및 Estado_VALOR consulta_VALOR')
    analizar_VALOR.add_argument('action', choices=['run', 'status'])
    parámetro_argumento = analizar_VALOR.parse_args()
    executar_comando = apl_iniciador(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parámetro_argumento.action == 'status':
        print(json.dumps(executar_comando.mostrar_Estado(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. hospedar 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/permiso_VALOR 변경은 하지 않습니다.')
    os.umask(0o077)
    executar_comando.CAMIÑO('lock').parent.mkdir(parents=True, exist_ok=True)
    with executar_comando.CAMIÑO('lock').open('a') as bloquear_VALOR:
        try: fcntl.flock(bloquear_VALOR, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox executar_comando 작업이 진행 중입니다.')
        print(json.dumps(executar_comando.executar_comando(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Executar_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ERRO:
        print('VBOX ERRO: ' + str(ERRO), file=sys.stderr)
        sys.exit(1)
