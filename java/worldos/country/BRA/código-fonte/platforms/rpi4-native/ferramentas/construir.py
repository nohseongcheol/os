#!/usr/bin/env python3
"""host javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from BLD_usuário_ESPAÇO import Criar_usuário_ESPAÇO
from BLD_rede import Criar_rede
from 예제빌드 import 예제만들기
from BLD_remoto import Criar_remoto

ação_raiz = Path(__file__).resolve().parents[1]
repositório_raiz = ação_raiz.parents[1]
BLD_caminho = ação_raiz / 'build'


def Executar_comando(argumento_MATRIZ):
    subprocess.check_call([str(첫째값) for 첫째값 in argumento_MATRIZ], cwd=str(ação_raiz))


def iniciar():
    BLD_caminho.mkdir(exist_ok=True)
    C_compilador = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    vinculador_ferramenta = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    arquivo_objeto_conversor = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    arquivo_ferramenta = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for ferramentas in ('javac', C_compilador, 시플플번역기, vinculador_ferramenta, arquivo_objeto_conversor, arquivo_ferramenta):
        if not shutil.which(ferramentas):
            raise SystemExit('필요한 construir ferramentas 없음: ' + ferramentas)
    fonte_informações = json.loads((ação_raiz / 'vendor/terminal-font.json').read_text())
    fonte_dados = (ação_raiz / 'vendor/terminal-font.bin').read_bytes()
    if len(fonte_dados) != 65616 * 32 or hashlib.sha256(fonte_dados).hexdigest() != fonte_informações['sha256']:
        raise SystemExit('terminal fonte_VALOR Tamanho/SHA256 불일치')
    exportar_tabela = {'jshell_interactive': '셸입출력.TI_interativo', 'jshell_output': '셸입출력.saídaTexto', 'jshell_input': '셸입출력.entrada_VALOR', 'java_task': 'Núcleo.작업', 'jfs_path_start': 'FicheirosMemória.caminho_START',
               'jfs_path_byte': 'FicheirosMemória.caminho_byte', 'jfs_open': 'FicheirosMemória.Abrir',
               'jfs_read': 'FicheirosMemória.Leitura', 'jfs_write': 'FicheirosMemória.Escrita',
               'jfs_seek': 'FicheirosMemória.busca_cargo', 'jfs_close': 'FicheirosMemória.Fechar',
               'jfs_size': 'FicheirosMemória.Tamanho', 'jfs_unlink': 'FicheirosMemória.apagar_entrada',
               'jfs_truncate': 'FicheirosMemória.set_duração'}
    exportar_tabela.update({'jfs_entry_count': 'FicheirosMemória.파일한도', 'jfs_entry_length': 'FicheirosMemória.공개이름길이', 'jfs_entry_byte': 'FicheirosMemória.공개이름바이트', 'jfs_entry_size': 'FicheirosMemória.공개파일크기'})
    exportar_tabela.update({'jdraw_prepare': 'ComposiçãoEcrã.Preparar', 'jdraw_width': 'ComposiçãoEcrã.너비얻기',
        'jdraw_height': 'ComposiçãoEcrã.get_altura', 'jdraw_count_low': 'ComposiçãoEcrã.기록아래얻기',
        'jdraw_count_high': 'ComposiçãoEcrã.기록위얻기', 'jdraw_clip': 'ComposiçãoEcrã.recortar',
        'jdraw_clip_value': 'ComposiçãoEcrã.recortar_VALOR', 'jdraw_begin': 'ComposiçãoEcrã.iniciar',
        'jdraw_end': 'ComposiçãoEcrã.fim', 'jdraw_pixel': 'ComposiçãoEcrã.pixel',
        'jdraw_rectangle': 'ComposiçãoEcrã.retângulo_preencher', 'jdraw_pointer': 'ComposiçãoEcrã.ponteiro'})
    exportar_tabela.update({'jfs_mkdir': 'FicheirosMemória.Criar_Diretório', 'jfs_rmdir': 'FicheirosMemória.remover_Diretório', 'jfs_kind': 'FicheirosMemória.entrada_Tipo'})
    exportar_tabela.update({'jnet_socket': 'loopback_rede.Criar_entrada', 'jnet_bind': 'loopback_rede.BIND_empresa',
        'jnet_put': 'loopback_rede.자료넣기', 'jnet_get': 'loopback_rede.leitura_dados', 'jnet_send': 'loopback_rede.enviar',
        'jnet_recv': 'loopback_rede.receber', 'jnet_port': 'loopback_rede.leitura_empresa_porta', 'jnet_address': 'loopback_rede.leitura_email',
        'jnet_peer': 'loopback_rede.remetente_empresa', 'jnet_close': 'loopback_rede.Fechar'})
    exportar_tabela.update({'jstream_create': 'fluxo_rede.Criar_entrada', 'jstream_bind': 'fluxo_rede.BIND_empresa', 'jstream_listen': 'fluxo_rede.escutar_empresa', 'jstream_connect': 'fluxo_rede.Ligar', 'jstream_accept': 'fluxo_rede.aceitar_conexão', 'jstream_read': 'fluxo_rede.Leitura', 'jstream_write': 'fluxo_rede.Escrita', 'jstream_port': 'fluxo_rede.leitura_empresa_porta', 'jstream_peer': 'fluxo_rede.leitura_par_porta', 'jstream_close': 'fluxo_rede.Fechar'})
    for símbolo_VALOR in list(exportar_tabela):
        if símbolo_VALOR.startswith('jstream_') or símbolo_VALOR.startswith('jnet_') and símbolo_VALOR not in ('jnet_put', 'jnet_get'):
            exportar_tabela[símbolo_VALOR.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = exportar_tabela.pop(símbolo_VALOR)
    예제들 = ['public final class grupo { public static void Preparar() {']
    for caminho in sorted((ação_raiz / '예제').iterdir()):
        if caminho.is_file():
            예제들.append('InterpretadorComandos.estático_Arquivo(%s, %s);' %
                (json.dumps(caminho.name), json.dumps(caminho.read_text(encoding='utf-8'), ensure_ascii=True)))
    (BLD_caminho / 'grupo.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(ação_raiz, repositório_raiz, Executar_comando)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(BLD_caminho)) as 작업경로:
        aula_caminho = Path(작업경로)
        Executar_comando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', aula_caminho, '-sourcepath', aula_caminho, '-d', aula_caminho] + sorted((ação_raiz / 'códigoFonte').glob('*.java')) + [BLD_caminho / 'grupo.java', BLD_caminho / '예제꾸러미.java'])
        # ficheiro·shell·Janela 세션·통신과 Java tela 합성 배열을 모두 수용한다.
        argumento_MATRIZ = ['sh', repositório_raiz / 'compiler/미리번역.sh', '--entry', 'Núcleo.iniciar', '--heap-words', '1048576', '-o', BLD_caminho / 'kernel-java.c']
        for símbolo_VALOR, método_entrada in sorted(exportar_tabela.items()):
            argumento_MATRIZ += ['--export', símbolo_VALOR + '=' + método_entrada]
        Executar_comando(argumento_MATRIZ + sorted(aula_caminho.glob('*.class')))
    (BLD_caminho / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    Configuração_BITS = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = repositório_raiz / 'posix-kor/arm64-native'
    Criar_usuário_ESPAÇO(ação_raiz, repositório_raiz, C_compilador, 시플플번역기, vinculador_ferramenta, arquivo_ferramenta, Configuração_BITS, Executar_comando)
    rede = Criar_rede(ação_raiz, C_compilador, arquivo_ferramenta, Configuração_BITS, Executar_comando)
    remoto_uso = Criar_remoto(ação_raiz, C_compilador, arquivo_ferramenta, Configuração_BITS, Executar_comando)
    포함인수 = ['-I', 포직스경로 / 'declarações', '-I', BLD_caminho]
    빌드작업 = [(C_compilador, [], BLD_caminho / 'terminal-font.S', 'font.o'),
            (C_compilador, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ação_raiz / 'computador/terminal.c', 'terminal.o'),
            (C_compilador, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ação_raiz / 'computador/elemento_de_ecrã.c', 'widgets.o'),
            (C_compilador, ['-std=c11'], BLD_caminho / 'kernel-java.c', 'java.o'),
            (C_compilador, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ação_raiz / 'computador/Quadro.c', 'board.o'),
            (C_compilador, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ação_raiz / 'computador/tela_desenho.c', 'drawing.o'),
            (C_compilador, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ação_raiz / 'computador/espaço_do_utilizador.c', 'user.o'),
            (C_compilador, [], ação_raiz / 'arranque_da_máquina/ponto_de_entrada_VALOR.S', 'entry.o'),
            (C_compilador, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Ligar.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], ação_raiz / 'testes/Arquivo_Chamadas.cpp', 'cpp.o')]
    for compilador_ferramenta, 추가영역, 원본자료, saída in 빌드작업:
        원본설정 = [Arquivo_entrada for Arquivo_entrada in Configuração_BITS if Arquivo_entrada != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else Configuração_BITS
        Executar_comando([compilador_ferramenta] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', BLD_caminho / saída])
    Executar_comando([arquivo_ferramenta, 'rcs', BLD_caminho / 'libposix-kor-arm64.a', BLD_caminho / 'posix.o'])
    Executar_comando([vinculador_ferramenta, '--gc-sections', '-T', ação_raiz / 'arranque_da_máquina/disposição_de_ligação.ld', '-Map', BLD_caminho / 'kernel.map', '-o', BLD_caminho / 'kernel.elf'] +
        [BLD_caminho / Nome for Nome in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', BLD_caminho / 'libposix-kor-arm64.a', rede, remoto_uso, BLD_caminho / 'remote/libassh.a', BLD_caminho / 'remote/libbearssl.a', '--end-group'])
    Executar_comando([arquivo_objeto_conversor, '-O', 'binary', BLD_caminho / 'kernel.elf', BLD_caminho / 'kernel8.img'])
    grupo_manifesto = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Português.nativo', 'korean_exceptions': 20,
                                 'full_awt_swing': False, 'swing_subset': ['JFrame','JPanel','JLabel','JButton','JTextField','ActionListener','SwingUtilities.invokeLater'], 'java_se_certified': False},
                'python': 'MicroPython 1.24.1 integer build', 'cpython': False,
                'pip': {'kind': 'source installer with host PyPI HTTPS relay', 'commands': ['install','list','uninstall'], 'cpython_pip': False, 'dependencies': False, 'persistent': False},
                'korean_c_api': 'independent structs, enum constants and real function symbols',
                'framebuffer': {'format': 'RGB32', 'default': [640,480], 'maximum': [1920,1080], 'boot_configurable': True, 'size_syscall': 22},
                'shell': 'UTF-8 editor/history, directories, variables, scripts, sequential pipes, redirects, ELF execution',
                'system_commands': ['ipconfig','ip','ifconfig','ping','route','netstat','ss','ps','top','free','df','uptime','poweroff'],
                'system_status': 'real lwIP interface/endpoints, native task/session PIDs, AOT heap pools, RAM filesystem slots',
                'ip_configuration': 'GENET DHCP on real Pi4; static IPv4/netmask/gateway; volatile; close active sockets before address changes',
                'ping': 'real ICMPv4 echo, numeric addresses, count/timeout/RTT; no DNS resolver',
                'poweroff': 'BCM2835 PM firmware-halt watchdog; QEMU guest shutdown; physical Pi untested',
                'pipe_capacity_bytes': 16384, 'posix_shell_complete': False,
                'ram_files': {'count': 64, 'bytes_each': 16384, 'directories': 16, 'persistent': False},
                'user_abi': 1, 'user_elf64': True, 'elf_extension_required': False,
                'linux_static_elf_subset': True, 'full_linux_binary_compatibility': False,
                'mmu': True, 'user_timeout_seconds': 2, 'cooperative_user_sessions': 4,
                'interactive_wait_renews_deadline': True, 'vi': 'native EL0 UTF-8 vi subset',
                'network': 'lwIP 2.2.0 IPv4 TCP/UDP/ARP/ICMP; GENET v5 Ethernet or UART1 SLIP', 'external_network': True,
                'external_network_transport': 'Pi4 GENET (hardware untested); QEMU auxiliary UART SLIP bridge',
                'ftp': 'guest service, passive binary transfers, anonymous root RAM workspace',
                'genet_ethernet': True, 'genet_driver_status': 'implemented; MMIO/MDIO model tests only', 'physical_network_tested': False,
                'ssh': {'implementation': 'guest libassh 1.1 / LGPL-2.1-or-later', 'port': 22, 'password_auth': True, 'console': 'shared kernel shell', 'independent_sessions': False, 'sftp': False, 'port_forwarding': False},
                'vnc': {'implementation': 'guest RFB 3.8 / VNC authentication / raw incremental tiles', 'port': 5900, 'encrypted_pixels': False, 'clients': 1, 'korean_input': 'native two-set F9/Shift+Space'},
                'rdp': False,
                'gui': 'four native terminal windows and Swing subset peers; guest VNC server with native input; optional QEMU VNC bridge',
                'native_usb_input': False, 'full_swing': False, 'swing_subset': True, 'sha256': {}}
    for Nome in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        grupo_manifesto['sha256'][Nome] = hashlib.sha256((BLD_caminho / Nome).read_bytes()).hexdigest()
    (BLD_caminho / 'build.json').write_text(json.dumps(grupo_manifesto, indent=2) + '\n')
    print('완료:', BLD_caminho / 'kernel8.img')


if __name__ == '__main__':
    iniciar()
