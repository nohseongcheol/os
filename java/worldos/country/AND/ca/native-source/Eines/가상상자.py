#!/usr/bin/env python3
"""jkoros 전용 VirtualBox programa_iniciador. 기존 VM/디스크/Store_VALOR 상태는 삭제하지 않는다."""
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


def Executa_shell_ordre(인수):
    entorn = dict(os.environ, LC_ALL='C')
    RESULTAT = subprocess.run([str(VALOR) for VALOR in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=entorn, timeout=180)
    contingut_VALOR = RESULTAT.stdout.decode('utf-8', 'replace')
    if RESULTAT.returncode:
        raise 실행오류('Ordre error_VALOR: ' + ' '.join(str(VALOR) for VALOR in 인수) + '\n' + contingut_VALOR[-10000:])
    return contingut_VALOR


def valor_d_atribut(contingut_VALOR):
    RESULTAT = {}
    for línia in contingut_VALOR.splitlines():
        if '=' not in línia:
            continue
        Nom, VALOR = línia.split('=', 1)
        if Nom.startswith('"'):
            Nom = json.loads(Nom)
        if VALOR.startswith('"'):
            try:
                tancar_VALOR, 끝 = json.JSONDecoder().raw_decode(VALOR)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALOR): VALOR = tancar_VALOR
            except ValueError:
                raise 실행오류('VirtualBox valor_d_atribut format_VALOR s_ha_produït_un_error: ' + línia)
        RESULTAT[Nom] = VALOR
    return RESULTAT


def 등록목록(contingut_VALOR):
    RESULTAT = {}
    for línia in contingut_VALOR.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', línia)
        if 일치: RESULTAT[일치.group(2).lower()] = 일치.group(1)
    return RESULTAT


def suma_de_comprovació(Camí):
    VALOR = hashlib.sha256()
    with Camí.open('rb') as Fitxer:
        for dades in iter(lambda: Fitxer.read(1024 * 1024), b''): VALOR.update(dades)
    return VALOR.hexdigest()


class programa_iniciador:
    def __init__(self, rel_VALOR, Nom, 방식='gui', Ordre=Executa_shell_ordre):
        self.rel_VALOR = Path(rel_VALOR).resolve()
        self.Nom, self.방식, self.Ordre = Nom, 방식, Ordre
        self.보관 = self.rel_VALOR / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Nom) or Nom in ('.', '..'):
            raise 실행오류('VM 이름은 문자·dígit_VALOR·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if 방식 not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Camí(self, homòleg_VALOR):
        if Path(homòleg_VALOR).is_absolute() or '..' in Path(homòleg_VALOR).parts:
            raise 실행오류('잘못된 관리 Camí: ' + str(homòleg_VALOR))
        RESULTAT = self.보관
        for 부분 in ['.vbox'] + list(Path(homòleg_VALOR).parts):
            if 부분 == '.vbox': RESULTAT = self.보관
            else: RESULTAT = RESULTAT / 부분
            if RESULTAT.is_symlink(): raise 실행오류('Connecta 경로는 사용하지 않습니다: ' + str(RESULTAT))
        return RESULTAT

    def Lectura(self):
        Camí = self.Camí('state.json')
        if not Camí.exists(): return None
        Estat_VALOR = json.loads(Camí.read_text(encoding='utf-8'))
        if Estat_VALOR.get('version') != 1 or Estat_VALOR.get('name') != self.Nom:
            raise 실행오류('관리 상태의 VM Nom/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Nom in ('uuid', 'owner'):
            if str(uuid.UUID(Estat_VALOR[Nom])) != Estat_VALOR[Nom]: raise 실행오류('잘못된 VM identificador_VALOR')
        return Estat_VALOR

    def Store_VALOR(self, Estat_VALOR):
        destinació_VALOR = self.Camí('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Fitxer:
            json.dump(Estat_VALOR, Fitxer, ensure_ascii=False, indent=2)
            Fitxer.write('\n')
            임시 = Fitxer.name
        os.replace(임시, str(destinació_VALOR))

    def msinfo32_exe(self, Estat_VALOR, 등록됨, recuperar_Estat=False):
        if Estat_VALOR['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = valor_d_atribut(self.Ordre(['VBoxManage', 'showvminfo', Estat_VALOR['uuid'], '--machinereadable']))
        Posició = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.Camí('machines').resolve() not in Posició.parents or msinfo32_exe.get('UUID') != Estat_VALOR['uuid']:
            raise 실행오류('이 프로젝트의 VM Ajusts Camí/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Ordre(['VBoxManage', 'getextradata', Estat_VALOR['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + Estat_VALOR['owner']:
            if recuperar_Estat and Estat_VALOR.get('pending') and 표식 == 'No value set!':
                self.Ordre(['VBoxManage', 'setextradata', Estat_VALOR['uuid'], 'JKOROS/Owner', Estat_VALOR['owner']])
            else:
                raise 실행오류('VM propietari_VALOR 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def xec_suport_físic(self, Estat_VALOR, msinfo32_exe):
        제어기들 = [VALOR for Nom, VALOR in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nom)]
        Permet_VALOR = [str(self.Camí(VALOR)) for VALOR in Estat_VALOR.get('media', [])]
        for Nom, VALOR in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(comandament) + r'-\d+-\d+', Nom) for comandament in 제어기들):
                if VALOR not in ('none', 'emptydrive') and VALOR not in Permet_VALOR:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALOR)

    def mostrar_Estat(self):
        Estat_VALOR = self.Lectura()
        if Estat_VALOR is None: return {'name': self.Nom, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Estat_VALOR, 등록목록(self.Ordre(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Estat_VALOR['name']), 'uuid': Estat_VALOR['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.Camí(Estat_VALOR['iso'])) if Estat_VALOR.get('iso') else None,
                'serial_log': str(self.Camí(Estat_VALOR['serial_log'])) if Estat_VALOR.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Executa_ordre(self):
        Estat_VALOR = self.Lectura()
        등록됨 = 등록목록(self.Ordre(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Estat_VALOR is not None and Estat_VALOR['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Estat_VALOR, 등록됨, recuperar_Estat=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 Executa_ordre 중입니다. 재빌드·재시작하지 않습니다.')
                return self.mostrar_Estat()
            self.xec_suport_físic(Estat_VALOR, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALOR 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Ordre(['VBoxManage', 'controlvm', Estat_VALOR['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 tornar_ho_a_provar_VALOR Obre 전에 기존 기록도 보관한다.
                    if Estat_VALOR.get('serial_log'):
                        원본 = self.Camí(Estat_VALOR['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Camí('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Ordre(['VBoxManage', 'startvm', Estat_VALOR['uuid'], '--type', self.방식])
                return self.mostrar_Estat()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 canvi_MODA 중입니다 ({}). 작업이 끝난 ENRERE_VALOR tornar_ho_a_provar_VALOR 실행하세요.'.format(현재))
        elif Estat_VALOR is not None and not Estat_VALOR.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 tornar_ho_a_provar_VALOR 등록하세요.')
        elif self.Nom in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALOR/Executa_ordre 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Ordre(['make', '-C', str(self.rel_VALOR / 'os'), 'iso']), end='')
        원본 = self.rel_VALOR / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        suport_físic_VALOR = 'media/kernel-' + suma_de_comprovació(원본) + '.iso'
        destinació_VALOR = self.Camí(suport_físic_VALOR)
        destinació_VALOR.parent.mkdir(exist_ok=True)
        if destinació_VALOR.exists():
            if suma_de_comprovació(destinació_VALOR) != suma_de_comprovació(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(destinació_VALOR))
        else:
            with tempfile.NamedTemporaryFile(dir=str(destinació_VALOR.parent)) as Fitxer:
                shutil.copyfile(str(원본), Fitxer.name)
                os.link(Fitxer.name, str(destinació_VALOR))

        if Estat_VALOR is None:
            Estat_VALOR = {'version': 1, 'name': self.Nom, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALOR(Estat_VALOR)
        if msinfo32_exe is None:
            self.Ordre(['VBoxManage', 'createvm', '--name', Estat_VALOR['name'], '--uuid', Estat_VALOR['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Camí('machines')), '--register'])
            self.Ordre(['VBoxManage', 'setextradata', Estat_VALOR['uuid'], 'JKOROS/Owner', Estat_VALOR['owner']])
        # generar_sistema 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Estat_VALOR, 등록목록(self.Ordre(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('generar_sistema 중 VM 상태가 바뀌었습니다. tornar_ho_a_provar_VALOR make vbox를 실행하세요.')
        self.xec_suport_físic(Estat_VALOR, msinfo32_exe)
        Estat_VALOR['iso'] = suport_físic_VALOR
        if suport_físic_VALOR not in Estat_VALOR['media']: Estat_VALOR['media'].append(suport_físic_VALOR)
        Estat_VALOR['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALOR = self.Camí(Estat_VALOR['serial_log'])
        LOG_VALOR.parent.mkdir(exist_ok=True)
        self.Store_VALOR(Estat_VALOR)
        self.Ordre(['VBoxManage', 'modifyvm', Estat_VALOR['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALOR)])
        제어기들 = [VALOR for Nom, VALOR in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nom)]
        if 'JKOROS IDE' not in 제어기들:
            self.Ordre(['VBoxManage', 'storagectl', Estat_VALOR['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Ordre(['VBoxManage', 'storageattach', Estat_VALOR['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(destinació_VALOR)])
        Estat_VALOR['pending'] = False
        self.Store_VALOR(Estat_VALOR)
        self.Ordre(['VBoxManage', 'startvm', Estat_VALOR['uuid'], '--type', self.방식])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.mostrar_Estat()


def Executa_2():
    analitzar_VALOR = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Executa_ordre 및 Estat_VALOR cerca_VALOR')
    analitzar_VALOR.add_argument('action', choices=['run', 'status'])
    paràmetre_arg = analitzar_VALOR.parse_args()
    Executa_ordre = programa_iniciador(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if paràmetre_arg.action == 'status':
        print(json.dumps(Executa_ordre.mostrar_Estat(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. allotjar 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/permís_VALOR 변경은 하지 않습니다.')
    os.umask(0o077)
    Executa_ordre.Camí('lock').parent.mkdir(parents=True, exist_ok=True)
    with Executa_ordre.Camí('lock').open('a') as blocar_VALOR:
        try: fcntl.flock(blocar_VALOR, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Executa_ordre 작업이 진행 중입니다.')
        print(json.dumps(Executa_ordre.Executa_ordre(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Executa_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as s_ha_produït_un_error:
        print('VBOX s_ha_produït_un_error: ' + str(s_ha_produït_un_error), file=sys.stderr)
        sys.exit(1)
