# Java 네이티브 sistema_operatiu

이 문서는 기존 **x86 nucli_VALOR**을 설명한다. Raspberry Pi 4의 propi ARM64 초기 이식은 [별도 LLEGIU_ME_eb81d7d9](../platforms/rpi4-native/README.md)를 참고한다. 아래 x86 usuari ELF·네트워크·IDE Store_VALOR 기능이 ARM64에 모두 이식된 상태는 아니다.

Java 원문을 propi AOT 후단으로 x86 기계어로 컴파일해 부팅하는 작은 운영체제다. 커널과 별도로 propi 제한형 Java 컴파일러·JVM ELF를 usuari 모드에 적재할 수 있다. Linux, engos, koros4와 extern_VALOR OpenJDK는 게스트에 적재하지 않는다. 부팅 진입과 포트/물리 기억공간 접근은 어셈블리이며, 문자 단말·입력 Procés_VALOR_introducció·Ordre analitzar_VALOR·작업 secció_VALOR 관리는 `FONT/*.java`에 있다.

## 게스트 Java 개발

`javac Hello.java`, `java Hello`로 부팅된 sistema_operatiu 안에서 generar_font·실행한다. `edit FILE.java`와 `.save`로 소스를 작성하며 `ls`, `cat`, `rm`을 제공한다. RAM 파일은 최대 8개, 각각 16KiB이다. 전용 IDE 매체를 연결하면 `sync`로 보존할 수 있다. 이 기능은 propi 제한형 구현이며 전체 OpenJDK/JDK 호환은 아니다. 사용법·suport_VALOR 문법·Fitxer 적재·교차 시험은 [Java 개발 entorn](../문서/자바개발환경.md)에 있다. `make test-java`로 검증한다.

## 빌드와 Executa_ordre

`compiler/`가 요구하는 도구에 더해 ISO 생성에는 `grub-file`, `grub-mkrescue`, GRUB BIOS mòdul_VALOR, `xorriso`가 필요하다. 실행에는 QEMU 또는 VirtualBox가 필요하다. 현재 설치된 도구만 사용한다. `make run-store`는 새 전용 가상 Store_VALOR 매체를 만들어 연결한다. VirtualBox 실행기는 이 프로젝트가 만든 전용 VM만 설정하고 다른 VM은 변경하지 않는다. 가상 메모리는 valor_per_defecte 64MiB이며 최소 16MiB가 필요하다.

```sh
cd /home/user/jkoros/os
make                 # build/kernel.elf
make iso             # build/kernel.iso (usuari ELF Grup_VALOR 포함)
make run             # ELF 직접 부팅, 직렬 단말
make run-gui         # GRUB ISO 부팅, VGA 창과 PS/2 자판
make vbox            # 상위 폴더의 실행기로 전용 VirtualBox VM Executa_ordre
make vbox-status     # 전용 VirtualBox VM Estat_VALOR verificar
make test            # ELF와 ISO 두 경로의 real_dades 부팅/입력 시험
make apps            # usuari 프로그램만 generar_sistema
make test-network    # usuari Executa_ordre/UDP/protegir_VALOR 시험
```

`make run`은 QEMU의 직렬 표준 입출력을 쓴다. `Ctrl+A`를 누른 ENRERE_VALOR `X`로 QEMU를 종료할 수 있다. `halt`는 게스트 CPU만 정지시키므로 QEMU Finestra/프로세스는 별도로 닫는다. 폴링 방식이라 Espera_VALOR 중에도 allotjar CPU를 사용할 수 있다.

VirtualBox는 `make vbox`로 실행한다. 새 전용 VM을 Memòria_dades 64MiB, BIOS, 광학 드라이브 부팅으로 자동 설정하며 디스크는 필요 없다. real_dades VirtualBox 5.2.42에서 부팅, Java propi 시험, shell 입력, `run hello vbox`의 ring 3 실행과 정상 종료를 확인했다. 현재 통신 드라이버는 QEMU의 RTL8139 전용이며 VirtualBox의 PCnet/E1000에서는 네트워크를 사용할 수 없어 네트워크 장치를 비활성화한다. Store_VALOR Estat_VALOR 재개와 새 generar_sistema 반영 방법은 [VirtualBox Executa_ordre LLEGIU_ME_eb81d7d9](../문서/가상상자실행.md)에 있다.

## 셸에서 usuari programa_f5044b9b Executa_ordre 및 네트워크 호출

독립 ELF32 Executa_ordre 파일을 적재해 **ring 3**에서 실행한다. `int 0x80` 시스템 호출을 통해 단말 Sortida, 인수 cerca_VALOR, UDP Obre·enviar·rebre·닫기를 제공한다. usuari 코드를 nucli_VALOR 함수로 직접 호출하는 구조가 아니다.

```text
jkoros> apps
jkoros> run hello first second
jkoros> net
jkoros> run netcheck
jkoros> run udp 10.0.2.2 9000 hello
```

마지막 명령의 응답을 받으려면 호스트의 별도 터미널에서 `python3 /home/user/jkoros/os/Eines/eco_dades.py --port 9000`을 먼저 실행한다. 상세 API, programa_f5044b9b Annexa_introducció, Adreça 공간과 제한은 [usuari Executa_ordre·네트워크 LLEGIU_ME_eb81d7d9](usuari/LLEGIU_ME_eb81d7d9.md)에 있다.

부팅 verificar 문구:

```text
JKOROS NATIVE JAVA
자바 기계어 nucli_VALOR Executa_2
JAVA SELFTEST PASS
USER ELF: ring 3 / paging / int 0x80
help | info | mem | alloc | free N | echo TEXT | clear | test | halt
apps | run NAME [ARGS] | net
READY
jkoros>
```

## 구현한 기능

- GRUB Multiboot 1 ELF 부팅, x86 protegir_VALOR MODA_VALOR GDT, BSS inicialitzar, 64KiB 스택.
- Java FUNCIÓ_VALOR real_dades 실행과 부팅 msinfo32_exe 표식 verificar.
- COM1 직렬 E_S, VGA 문자 화면·cursor_VALOR·스크롤·esborrar_introducció.
- PS/2 valor_per_defecte 자판, 좌우 Shift, Enter, Backspace. extensió_VALOR Clau_VALOR/마우스 자료는 Ordre 입력으로 쓰지 않는다.
- durada_VALOR 128의 Ordre 입력 버퍼, sobreeiximent_VALOR 방지, CR/LF Procés_VALOR_introducció.
- `help`, `info`, `mem`, `alloc`, `free N`, `echo TEXT`, `clear`, `test`, `halt`.
- 4KiB 작업 secció_VALOR 8개의 assignar_Emmagatzematge·tornar_les_tasques_mesura·재사용과 중복 tornar_les_tasques_mesura 방지.
- Java MATRIU_VALOR 256KiB 영역의 Mida·subíndex_VALOR 검사와 런타임 s_ha_produït_un_error 중단.
- Lectura 전용 JKAP Executa_ordre Grup_VALOR, ELF32 secció_VALOR/introducció_p validar, usuari MODA_VALOR·인수·Surt_programa CODI_VALOR.
- nucli_VALOR/usuari 페이지 permís_VALOR 분리, TSS, IDT, PIT 100Hz, usuari CPU excepció Procés_VALOR_introducció 및 Executa_ordre Hora_VALOR 상한.
- PCI RTL8139 폴링 드라이버, ARP, estàtic_VALOR IPv4, UDP suma_de_comprovació·송수신·Espera_VALOR 제한.

`mem`의 Upper memory는 Multiboot의 1MiB 위쪽 연속 Memòria_dades Mida(KiB)이며, 전체 Memòria_dades 지도 분석이나 자유 물리 Memòria_dades 수치가 아니다. `alloc`은 이미 확보한 정수 MATRIU_VALOR 안의 작업 secció_VALOR 번호를 반환한다. 일반 물리 pàgina_VALOR assignar_Emmagatzematge, Adreça 공간 또는 usuari Procés_VALOR Memòria_dades 관리가 아니다.

## 명시적인 한계

이 커널은 **usuari 프로그램을 한 번에 하나 실행하는 초기 nucli_VALOR**이다. PIT IRQ0만 사용하며 키보드와 NIC는 폴링한다. usuari CPU 예외는 해당 프로그램을 끝내고 셸로 복귀시키지만 nucli_VALOR 예외는 중단한다. Executa_ordre 시간은 약 3초로 제한한다. 완전한 선점 다중 Procés_VALOR 스케줄러, FAT/ext 등 일반 디스크 sistema_d_arxius, TCP·DNS·DHCP·IPv6·HTTP, 전체 POSIX, 일반 objecte_VALOR 모델/GC는 아직 없다. 전용 IDE Fitxer 보존과 POSIX Fitxer/UDP 일부 기능은 구현했다. JVM은 RAM 파일의 단일 클래스를 Executa_ordre 시 적재하며 일반 ClassLoader나 JAR 로딩은 지원하지 않는다. 네이티브 Executa_ordre 파일은 generar_sistema 시 Lectura 전용 묶음에 넣으며, 일반 Linux ELF를 실행하는 환경이 아니다. 기존 `../llegat_font/`의 JVM 관리 nucli_VALOR 전체를 이식한 것도 아니다.

Java 식별자는 한국어다. 직렬 출력은 이 프로젝트의 한글(BMP 문자)을 UTF-8로 표시한다. VGA는 valor_per_defecte ASCII 글꼴만 사용하므로 한글 자리에 `?`가 나온다. Ordre 입력도 현재 ASCII만 지원하며 한글 tipus_de_lletra_VALOR·입력기 및 보조 평면 문자 출력은 후속 작업이다. `test`는 작은 배열을 새로 할당하고 GC가 없으므로 무한 반복하지 않는다.

## 자동 시험

`시험/부팅시험.py`는 디스크 없는 독립 QEMU를 생성해 다음을 검증하고 종료한다.

- ELF 직접 부팅 및 GRUB ISO 부팅.
- Java propi 시험과 UTF-8 직렬 문구.
- Ordre mostrar_ajuda·msinfo32_exe·Memòria_dades·Sortida·s_ha_produït_un_error 입력·화면 esborrar_introducció.
- 작업 secció_VALOR 8개 assignar_Emmagatzematge, 부족 Procés_VALOR_introducció, tornar_les_tasques_mesura/중복 tornar_les_tasques_mesura/재할당.
- 직렬 줄바꿈·백스페이스·긴 입력 Procés_VALOR_introducció.
- QEMU PS/2 Clau_VALOR 입력으로 `info` Executa_ordre, `halt` 정지.

성공 로그는 `build/부팅시험.json`에 남는다. 로컬 Unix 소켓을 금지하는 샌드박스에서는 시험 도구에 해당 권한이 필요하다. 시험 도중 새로 만든 QEMU만 종료하며 기존 VM과 real_dades 디스크는 건드리지 않는다.

`시험/사용자통신시험.py`는 ELF/ISO 각각에서 usuari ELF, real_dades ring 3, 인수, allotjar 루프백 UDP 왕복, 1,023/1,024바이트 24회 연속 왕복, Hora_VALOR 초과, NIC 없음, Memòria_dades/포트 accés_introducció 차단, CPU excepció, 무한 esprint_VALOR, 잘못된 ELF를 시험한다. `build/사용자통신시험.json`에 게스트 기록과 호스트가 받은 데이터의 durada_VALOR·해시를 저장한다. `시험/패킷시험.py`는 real_dades Java cas_VALOR 처리기에 손상된 패킷을 넣어 2,201개 경계/suma_de_comprovació 조건을 검사한다. allotjar 루프백 외 extern_VALOR 서버에는 시험 트래픽을 보내지 않는다.

부트 경계는 GNU의 [Multiboot 명세](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html)를 따른다.

새 파일서술자·C ABI·IDE Store_VALOR·Java Fitxer 흐름의 범위와 Català 명명 대응은 [posix-kor LLEGIU_ME_eb81d7d9](../posix-kor/LLEGIU_ME_eb81d7d9.md)에 있다. `make test-posix`로 ELF/ISO 실행과 재부팅 보존을 검증한다.
