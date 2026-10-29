#!/usr/bin/env python3
"""real_dados ring 3 ELF/host UDP 왕복/proteger_VALOR erro/valor_temporal 제한/잘못된 ELF를 검증한다."""
import json
import hashlib
from pathlib import Path
import select
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time

posição = Path(__file__).resolve().parents[1]


class VM:
    def __init__(self, caminho, Tipo_VALOR='elf', rede_VALOR=True, Armazenamento_meio=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Diretório_VALOR = Path(self.임시.name)
        self.LOG_linha = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VALOR = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_caminho = Diretório_VALOR / 'serial.sock', Diretório_VALOR / 'monitor.sock'
        comando = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_caminho) + ',server,nowait']
        comando += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if rede_VALOR else ['-net', 'none']
        comando += ['-kernel', str(caminho)] if Tipo_VALOR == 'elf' else ['-cdrom', str(caminho), '-boot', 'd']
        if Armazenamento_meio is not None:
            comando += ['-drive', 'file=' + str(Armazenamento_meio) + ',format=raw,if=ide,index=0']
        self.Processo_VALOR = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_caminho.exists()):
                if self.Processo_VALOR.poll() is not None:
                    raise AssertionError(self.Processo_VALOR.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU iniciar valor_temporal 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VALOR.connect(str(monitor_caminho))
            self.직렬.setblocking(False)
            self.monitor_VALOR.sendall(b'cont\n')
            self.estado_de_espera('jkoros> ')
        except BaseException:
            self.Fechar()
            raise

    def estado_de_espera(self, 문구, iniciar=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_linha[iniciar:]:
                return self.LOG_linha[iniciar:].decode('utf-8', 'replace')
            Leitura, _, _ = select.select([self.직렬], [], [], 0.1)
            if Leitura:
                dados = self.직렬.recv(65536)
                if not dados: break
                self.LOG_linha.extend(dados)
            if self.Processo_VALOR.poll() is not None: break
        raise AssertionError('aguarde_VALOR falha_VALOR: ' + 문구 + '\n' + self.LOG_linha.decode('utf-8', 'replace'))

    def comando(self, cadeia_VALOR, 기대):
        iniciar = len(self.LOG_linha)
        self.직렬.sendall((cadeia_VALOR + '\n').encode())
        resultado = self.estado_de_espera('jkoros> ', iniciar)
        for 문구 in 기대:
            assert 문구 in resultado, (cadeia_VALOR, 문구, resultado)
        assert 'PANIC' not in resultado, resultado
        return resultado

    def Fechar(self):
        self.직렬.close()
        self.monitor_VALOR.close()
        if self.Processo_VALOR.poll() is None:
            self.Processo_VALOR.terminate()
            try: self.Processo_VALOR.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Processo_VALOR.kill()
                self.Processo_VALOR.wait()
        self.Processo_VALOR.communicate()
        self.임시.cleanup()


def 보호커널(Diretório_VALOR):
    사례들 = {
        'badmem': 'movl $7, 0x00100000',
        'badport': 'movw $0x3f8, %dx\noutb %al, %dx',
        'spin': '1: jmp 1b',
        'badptr': 'movl $1,%eax\nmovl $0x00100000,%ebx\nint $0x80\ncmpl $-14,%eax\njne fail\n'
                  'movl $999,%eax\nint $0x80\ncmpl $-38,%eax\njne fail\n'
                  'xorl %ebx,%ebx\nxorl %eax,%eax\nint $0x80\nfail: movl $1,%ebx\nxorl %eax,%eax\nint $0x80',
        'fault': 'ud2',
        'badfile': '''
            movl $20,%eax
            movl $0x00100000,%ebx
            movl $empty,%ecx
            int $0x80
            cmpl $-14,%eax
            jne fail
            movl $20,%eax
            movl $name,%ebx
            movl $0x00100000,%ecx
            int $0x80
            cmpl $-14,%eax
            jne fail
            movl $21,%eax
            movl $name,%ebx
            movl $negative,%ecx
            xorl %edx,%edx
            int $0x80
            cmpl $-14,%eax
            jne fail
            movl $21,%eax
            movl $name,%ebx
            movl $empty,%ecx
            movl $1,%edx
            int $0x80
            cmpl $-22,%eax
            jne fail
            movl $20,%eax
            movl $empty,%ebx
            movl $empty,%ecx
            int $0x80
            cmpl $-22,%eax
            jne fail
            xorl %eax,%eax
            xorl %ebx,%ebx
            int $0x80
        fail:
            xorl %eax,%eax
            movl $1,%ebx
            int $0x80
        .balign 4
        name: .long 1,88
        empty: .long 0
        negative: .long -1
        ''',
    }
    항목들 = ['hello=' + str(posição / 'build/apps/hello.elf')]
    for Nome, Conteúdo_VALOR in 사례들.items():
        códigoFonte = Diretório_VALOR / (Nome + '.s')
        códigoFonte.write_text('.code32\n.text\n.globl _start\n_start:\n' + Conteúdo_VALOR +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Diretório_VALOR / (Nome + '.o')), str(códigoFonte)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(posição.parent / 'compiler/usuário_Link_Layout.ld'),
                        '-o', str(Diretório_VALOR / (Nome + '.elf')), str(Diretório_VALOR / (Nome + '.o'))], check=True)
        항목들.append(Nome + '=' + str(Diretório_VALOR / (Nome + '.elf')))
    TI_normal = bytearray((posição / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    inválido_RC = bytearray(TI_normal); inválido_RC[0] = 0; 변형들['badelf'] = inválido_RC
    inválido_RC = bytearray(TI_normal); struct.pack_into('<I', inválido_RC, 24, 0x00100000); 변형들['badentry'] = inválido_RC
    inválido_RC = bytearray(TI_normal); struct.pack_into('<I', inválido_RC, 28, 0x7fffffff); 변형들['badtable'] = inválido_RC
    inválido_RC = bytearray(TI_normal); tabela_de_pesquisa = struct.unpack_from('<I', inválido_RC, 28)[0]
    struct.pack_into('<I', inválido_RC, tabela_de_pesquisa + 20, 0x7fffffff); 변형들['badsize'] = inválido_RC
    for Nome, dados in 변형들.items():
        ficheiro = Diretório_VALOR / (Nome + '.elf'); ficheiro.write_bytes(dados)
        항목들.append(Nome + '=' + str(ficheiro))
    subprocess.run([sys.executable, str(posição / 'ferramentas/BIND_empresa.py'), '-o', str(Diretório_VALOR / 'apps.bin')] + 항목들, check=True)
    códigoFonte = Diretório_VALOR / 'apps.s'
    códigoFonte.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Diretório_VALOR / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Diretório_VALOR / 'apps.o'), str(códigoFonte)], check=True)
    kernel_VALOR = Diretório_VALOR / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(posição / 'arranque_da_máquina/disposição_de_ligação.ld'), '-o', str(kernel_VALOR),
                    str(posição / 'build/boot.o'), str(posição / 'build/java.o'), str(posição / 'build/user.o'), str(Diretório_VALOR / 'apps.o')], check=True)
    return kernel_VALOR


def Executar_comando():
    resultado = {}
    servidor_VALOR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor_VALOR.bind(('127.0.0.1', 0))
    servidor_VALOR.settimeout(0.1)
    porta_VALOR = servidor_VALOR.getsockname()[1]
    RECEBER_item = []
    sair_app = threading.Event()
    def eco_resposta():
        while not sair_app.is_set():
            try: dados, par_VALOR = servidor_VALOR.recvfrom(4096)
            except socket.timeout: continue
            RECEBER_item.append(dados)
            if dados != b'drop-me': servidor_VALOR.sendto(dados, par_VALOR)
    trabalho_VALOR = threading.Thread(target=eco_resposta, daemon=True)
    trabalho_VALOR.start()
    try:
        for Tipo_VALOR in ('elf', 'iso'):
            computador = VM(posição / ('build/kernel.elf' if Tipo_VALOR == 'elf' else 'build/kernel.iso'), Tipo_VALOR)
            try:
                computador.comando('apps', ['hello', 'udp', 'netcheck', 'stress'])
                computador.comando('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                computador.comando('run missing', ['Exit: -2'])
                computador.comando('net', ['NET RTL8139'])
                computador.comando('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Conteúdo_VALOR in ('hello-network', 'odd', 'even', 'repeat-123'):
                    computador.comando('run udp 10.0.2.2 {} {}'.format(porta_VALOR, Conteúdo_VALOR), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Conteúdo_VALOR.encode() in RECEBER_item, 'host 서버에서 자료를 받지 못함'
                computador.comando('run stress {}'.format(porta_VALOR), ['UDP STRESS PASS', 'Exit: 0'])
                computador.comando('run udp 10.0.2.2 {} drop-me'.format(porta_VALOR), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                computador.comando('run hello recovered', ['arg: recovered', 'Exit: 0'])
                resultado[Tipo_VALOR] = computador.LOG_linha.decode('utf-8', 'replace')
                print('PASS: {} espaço_do_utilizador ELF/ring 3/argumentos/UDP host 왕복/valor_temporal 초과/shell 복귀'.format(Tipo_VALOR), flush=True)
            finally:
                try: computador.comando('net', [])
                except Exception: pass
                (posição / 'build/사용자통신-last.log').write_bytes(computador.LOG_linha)
                computador.Fechar()
        computador = VM(posição / 'build/kernel.elf', rede_VALOR=False)
        try:
            computador.comando('net', ['NET unavailable'])
            computador.comando('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            computador.comando('run hello', ['USER MODE ring 3', 'Exit: 0'])
            resultado['no_nic'] = computador.LOG_linha.decode()
        finally: computador.Fechar()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            computador = VM(보호커널(Path(임시)), rede_VALOR=False)
            try:
                for Nome, Estado_VALOR in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    computador.comando('run ' + Nome, ['Exit: ' + str(Estado_VALOR)])
                    computador.comando('run hello', ['USER MODE ring 3', 'Exit: 0'])
                resultado['protection'] = computador.LOG_linha.decode()
                print('PASS: espaço_do_utilizador Memória_dados/hardware_porta 격리, 잘못된 ponteiro/ELF, CPU exceção, 무한 sprint_VALOR 제한', flush=True)
            finally:
                (posição / 'build/Proteção_teste-last.log').write_bytes(computador.LOG_linha)
                computador.Fechar()
    finally:
        sair_app.set()
        trabalho_VALOR.join(timeout=2)
        servidor_VALOR.close()
    resultado['host_udp_received'] = [{'length': len(dados), 'sha256': hashlib.sha256(dados).hexdigest()} for dados in RECEBER_item]
    (posição / 'build/teste_Usenet.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Executar_comando()
