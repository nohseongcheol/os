# JCpvOS

em_dia_item nativo ARM64 배포판은 [LICENSE](LICENSE)의 COSL 상업 조건을 유지한다. 제3자 라이선스의 권리는 별도로 보장하며, distribuição_VALOR 시 fonte_árvore·재연결 자료를 포함하는 절차는 [COSL distribuição_VALOR LEIAME_eb81d7d9](platforms/rpi4-native/COSL배포안내.md)에 있다.

nativo ARM64 판의 `ipconfig`/`ip`, `ping`, `ps`/`top`, `free`/`df`, `poweroff`와 Português 명령은 [네트워크·SO_VALOR comando LEIAME_eb81d7d9](platforms/rpi4-native/네트워크와체계명령.md)를 참고한다. 새 커널을 부팅한 BACK_VALOR `help system`으로 볼 número 있다.

Raspberry Pi 4 **nativo Java ARM64 kernel_VALOR**은 [nativo Pi4 LEIAME_eb81d7d9](platforms/rpi4-native/LEIAME_eb81d7d9.md)에 있다. Linux 없이 부팅하며 GUI terminal·vi, nativo JVM의 Swing 일부 API, TCP/UDP·FTP, 게스트 TinyCC·MicroPython, C/C++의 posix-kor 호출을 제공한다. [Português Java comunicação·exceção API](platforms/rpi4-native/한국어자바/LEIAME_eb81d7d9.md)와 [Português fonte_árvore 명명](platforms/rpi4-native/명명/LEIAME_eb81d7d9.md)을 지원한다. [nativo SSH·VNC 및 GENET 드라이버](platforms/rpi4-native/externo_conexão_guia.md)를 포함하며, 네트워크는 QEMU의 UART SLIP 경로로 검증했다. real_dados Pi 4 GENET 동작은 미검증이고, USB entrada_VALOR·영속 저장과 전체 OpenJDK·Swing은 아직 Suporte_VALOR recortar 밖이다.

Raspberry Pi 4용 Linux·OpenJDK 실행판과 espaço_do_utilizador ambiente mover_VALOR 기능은 [라즈베리파이 실행판](platforms/rpi4/README.md)에 있다. real_dados ARM64 JDK/JRE와 시스템·espaço_do_utilizador BLD_foto construir 경로를 제공한다. 기존 nativo x86 커널과는 별도 Executar_comando 기반이다. 일반 Java `.class`/JAR의 Executar_comando ficheiro 생성은 [OpenJDK Executar_comando ficheiro](compiler/OpenJDK-executável.md), Português API는 [Português Java biblioteca](한국어자바/LEIAME_eb81d7d9.md)를 참고한다.

`jkoros`는 `engos`의 기능을 Java 관리 커널로 옮기는 프로젝트다. 프로젝트가 소유하는 Java FUNÇÃO_VALOR, variável_VALOR, formato_VALOR 및 Java ficheiro 이름은 한국어로 작성한다. 표준 Java 실행기의 `main`, Java 표준 biblioteca formato_VALOR, x86 부트 ABI 등 externo_VALOR 계약은 보존한다. nativo ARM64 실행기는 Português `iniciar()`도 진입점으로 지원하며, Português GUI·작업 가닥을 JVM에 직접 구현했다. nativo ARM64 C 연결부·Python 도구와 공용 x86·ARM64 AOT 번역기의 nativo 이름도 한국어로 작성한다. Anterior_item 경로의 호환 ponto_de_entrada, OpenJDK 보조 도구와 Linux versão_VALOR 도구에는 영어 이름이 남아 있고 [명명 원칙·말의 근거·전체 códigoFonte 검토 recortar](platforms/rpi4-native/명명/LEIAME_eb81d7d9.md)를 별도로 기록한다.

## em_dia_item implementação

아래 목록은 기존 `herdado_fonte/`의 JVM 관리 커널에 대한 것이다. real_dados 네이티브 커널의 범위는 `os/LEIAME_eb81d7d9.md`에서 별도로 설명한다.

- alinhar_VALOR 할당과 해제를 지원하는 Memória_região gerente_VALOR
- Endereço email_região, página_VALOR Ligar, Escrita 시 copiar_VALOR(COW)
- Processo_VALOR identificador_VALOR, Preparar 대기열, fork/wait Estado_VALOR
- 과정별 ficheiro descritor_entrada, open/read/seek/dup/close
- ELF32 식별 및 seção_VALOR 검사
- 키보드·마우스 entrada_VALOR Evento 대기열
- 직렬 단말과 네이티브 hardware_VALOR limite_VALOR
- 관리 kernel_VALOR 전체 자동 testes

세부 mapeamento_VALOR 범위와 아직 필요한 네이티브 연결은 [기능 대응표](문서/recurso_mapeamento.md)에 기록한다.

## 빌드와 testes

새 네이티브 구현은 `compiler/`와 `os/`에 있다. 기존 `herdado_fonte/`의 JVM 관리 커널은 그대로 보존하며, 두 구현의 시험과 기능 범위는 서로 다르다.

```sh
cd /home/user/jkoros
make                 # 네이티브 계산 예제 + Java kernel_VALOR ELF
make iso             # os/build/kernel.iso
make run             # QEMU 직렬 단말; help entrada_VALOR (종료는 Ctrl+A, X)
make run-gui         # ISO를 QEMU tela/PS2 키보드로 Executar_comando
make vbox            # 전용 VirtualBox VM 자동 gerar·Executar_comando (GUI)
make vbox-status     # VirtualBox Estado_VALOR·ISO·직렬 LOG_linha caminho verificar
make test-vbox       # VirtualBox app_Launcher Estado_VALOR Processo_VALOR_entrada testes (real_dados VM alterar_VALOR 없음)
make test            # compilador testes + ELF/ISO arranque_da_máquina 및 comando entrada_VALOR testes
make apps            # 독립 espaço_do_utilizador ELF app_f5044b9b construir
make test-network    # espaço_do_utilizador MODO_VALOR·UDP 왕복·Memória_dados proteger_VALOR testes
make test-java       # 게스트 javac/JVM + OpenJDK 양방향 교차 Executar_comando testes
make posix-kor       # Português C 헤더와 real_dados kernel_VALOR 호출 biblioteca
make test-posix      # ficheiro/UDP/Store_VALOR/Java ficheiro E_S testes
make -C os run-store # 전용 Store_VALOR 매체로 QEMU arranque_da_máquina
make legacy-test     # 아래 기존 JVM 관리 커널의 47개 testes
```

`compiler/`는 호스트의 `javac`를 문법·TIPO_VALOR 검사 전단으로 사용하고 nativo 바이트코드→x86 변환기로 ELF32 기계어를 만든다. 빌드할 때는 JDK가 필요하지만 생성된 커널과 ELF는 externo_VALOR JVM 없이 실행된다. 전체 Java, objeto_VALOR 모델, 표준 라이브러리와 기존 관리 kernel_VALOR 전체의 AOT 변환은 아직 지원하지 않는다. 자세한 Suporte_VALOR 문법과 명령은 [compilador LEIAME_eb81d7d9](compiler/LEIAME_eb81d7d9.md), real_dados arranque_da_máquina 기능과 한계는 [네이티브 SO LEIAME_eb81d7d9](os/LEIAME_eb81d7d9.md)를 참고한다.

네이티브 셸에 nativo 제한형 `javac`와 `java`를 추가했다. `edit Demo.java`로 소스를 입력하고 `.save`로 저장한 BACK_VALOR `javac Demo.java`, `java Demo`로 **게스트 내부에서 컴파일하고 Executar_comando**할 número 있다. valor_padrão 예제는 `javac Hello.java`, `java Hello`다. 파일은 RAM에서 동작하며, 전용 Store_VALOR 매체를 연결하면 `sync`로 재부팅 후에도 보존할 número 있다. **OpenJDK/JDK 전체 이식은 아니며**, 단일 aula_VALOR·estático_VALOR FUNÇÃO_VALOR·inteiro·cadeia_VALOR·doença/반복문과 일부 표준 호출을 지원한다. Suporte_VALOR recortar, externo_VALOR ficheiro 적재와 시험은 [Java 개발 ambiente LEIAME_eb81d7d9](문서/Java_IDE.md)에 있다.

네이티브 셸에서 `apps`, `run hello first second`, `net`, `run netcheck`를 사용할 número 있다. 독립 ELF를 ring 3에 적재하고 `int 0x80` 호출을 통해 saídaTexto·argumentos·UDP 네트워크를 제공한다. 별도 host 터미널에서 `python3 os/ferramentas/eco_dados.py --port 9000`을 실행한 BACK_VALOR 게스트에서 `run udp 10.0.2.2 9000 hello`로 real_dados 왕복을 확인한다. 새 app_f5044b9b registro_entrada, API 및 제한은 [espaço_do_utilizador Executar_comando·네트워크 LEIAME_eb81d7d9](os/espaço_do_utilizador/LEIAME_eb81d7d9.md)를 참고한다. em_dia_item QEMU RTL8139·estático_VALOR IPv4·UDP 전용이며 TCP/DNS는 미지원이며, 전용 IDE Store_VALOR 형식과 POSIX ficheiro/UDP 일부 기능을 추가했다.

`make vbox`는 `jkoros operating system` 전용 VM을 만들고 디스크 없이 ISO로 부팅한다. Executar_comando 중이면 유지하고, Store_VALOR·일시정지 상태이면 재개하며, 꺼져 있을 때만 새 ISO를 빌드해 연결한다. VirtualBox에서 부팅과 셸의 espaço_do_utilizador app_f5044b9b 실행을 확인했다. 다만 em_dia_item VirtualBox용 네트워크 드라이버는 없어 네트워크 장치를 비활성화한다. UDP 시험에는 `make run`을 사용한다. 상태별 동작과 새 construir 반영 방법은 [VirtualBox Executar_comando LEIAME_eb81d7d9](문서/가상상자실행.md)에 있다.

기존 관리 커널만 시험하려면:

```sh
cd /home/user/jkoros
make -f Criar_entrada.mk 검사
make -f Criar_entrada.mk host
```

`host`는 여전히 JVM 관리 계층의 Acção 시험이다. `make -f Criar_entrada.mk BLD_foto`는 새 `os/`의 제한형 네이티브 kernel_VALOR ISO를 만든다. 기존 `herdado_fonte/`의 sistema_de_arquivos·Processo_VALOR·rede_pilha implementação 전체를 이 ISO에 이식했다는 의미는 아니다.

Português FUNÇÃO_VALOR·variável_VALOR·ficheiro 이름과 real_dados C API는 [posix-kor](posix-kor/LEIAME_eb81d7d9.md)에 있다. 게스트 Java에서는 `FileInputStream`·`FileOutputStream`의 단일 byte_VALOR 입출력도 지원한다. 전체 POSIX·OpenJDK·Swing 지원으로 확대된 것은 아니다.

externo_VALOR 배포용 `pack.sh` / `unpack.sh`와 자동 의존성 복원은 [distribuição_VALOR LEIAME_eb81d7d9](distribution/README.md)를 참고하세요.
