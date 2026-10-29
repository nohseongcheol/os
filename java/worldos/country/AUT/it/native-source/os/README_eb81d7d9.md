# Java 네이티브 sistema_operativo

이 문서는 기존 **x86 kernel_VALORE**을 설명한다. Raspberry Pi 4의 nativo ARM64 stato_iniziale 이식은 [별도 README_eb81d7d9](../platforms/rpi4-native/README.md)를 참고한다. 아래 x86 spazio_utente ELF·네트워크·IDE Store_VALORE 기능이 ARM64에 모두 이식된 상태는 아니다.

Java 원문을 nativo AOT 후단으로 x86 기계어로 컴파일해 부팅하는 작은 운영체제다. 커널과 별도로 nativo 제한형 Java compilatore·JVM ELF를 spazio_utente 모드에 적재할 numero 있다. Linux, engos, koros4와 esterno_VALORE OpenJDK는 게스트에 적재하지 않는다. avvio_macchina 진입과 hardware_porta/물리 Memoria_area 접근은 어셈블리이며, 문자 단말·input_VALORE Processi_VALORE_voce·comando analizzare_VALORE·작업 sezione_VALORE 관리는 `codiceSorgente/*.java`에 있다.

## 게스트 Java sviluppo

`javac Hello.java`, `java Hello`로 부팅된 sistema_operativo 안에서 compilare_fonte·실행한다. `edit FILE.java`와 `.save`로 소스를 작성하며 `ls`, `cat`, `rm`을 제공한다. RAM 파일은 최대 8개, 각각 16KiB이다. 전용 IDE 매체를 연결하면 `sync`로 보존할 numero 있다. 이 기능은 nativo 제한형 구현이며 전체 OpenJDK/JDK 호환은 아니다. 사용법·Supporto_VALORE 문법·file 적재·교차 시험은 [Java sviluppo ambiente](../Guides/ambiente_IDE_Java.md)에 있다. `make test-java`로 검증한다.

## 빌드와 Esegui_comando

`compiler/`가 요구하는 도구에 더해 ISO 생성에는 `grub-file`, `grub-mkrescue`, GRUB BIOS modulo_VALORE, `xorriso`가 필요하다. 실행에는 QEMU 또는 VirtualBox가 필요하다. Regolari_articolo 설치된 도구만 사용한다. `make run-store`는 새 전용 가상 Store_VALORE 매체를 만들어 연결한다. VirtualBox 실행기는 이 프로젝트가 만든 전용 VM만 설정하고 다른 VM은 변경하지 않는다. 가상 메모리는 valore_predefinito 64MiB이며 최소 16MiB가 필요하다.

```sh
cd /home/user/jkoros/os
make                 # build/kernel.elf
make iso             # build/kernel.iso (spazio_utente ELF gruppo_VALORE dichiarazioni)
make run             # ELF 직접 avvio_macchina, seriale_VALORE 단말
make run-gui         # GRUB ISO avvio_macchina, VGA 창과 PS/2 자판
make vbox            # 상위 폴더의 실행기로 전용 VirtualBox VM Esegui_comando
make vbox-status     # 전용 VirtualBox VM Stato_VALORE verificare
make test            # ELF와 ISO 두 경로의 effettivo_dati avvio_macchina/input_VALORE prove
make apps            # spazio_utente 프로그램만 costruire
make test-network    # spazio_utente Esegui_comando/UDP/proteggere_VALORE prove
```

`make run`은 QEMU의 seriale_VALORE 표준 입출력을 쓴다. `Ctrl+A`를 누른 BACK_VALORE `X`로 QEMU를 종료할 numero 있다. `halt`는 게스트 CPU만 정지시키므로 QEMU Finestra/프로세스는 별도로 닫는다. 폴링 방식이라 aspetta_VALORE 중에도 host CPU를 사용할 numero 있다.

VirtualBox는 `make vbox`로 실행한다. 새 전용 VM을 Memoria_dati 64MiB, BIOS, 광학 드라이브 부팅으로 자동 설정하며 디스크는 필요 없다. effettivo_dati VirtualBox 5.2.42에서 avvio_macchina, Java nativo prove, Shell input_VALORE, `run hello vbox`의 ring 3 실행과 reparto_IT_normale 종료를 확인했다. Regolari_articolo comunicazione 드라이버는 QEMU의 RTL8139 전용이며 VirtualBox의 PCnet/E1000에서는 네트워크를 사용할 numero 없어 네트워크 장치를 비활성화한다. Store_VALORE Stato_VALORE 재개와 새 costruire 반영 방법은 [VirtualBox Esegui_comando README_eb81d7d9](../Guides/가상상자실행.md)에 있다.

## 셸에서 spazio_utente app_f5044b9b Esegui_comando 및 네트워크 호출

독립 ELF32 Esegui_comando 파일을 적재해 **ring 3**에서 실행한다. `int 0x80` 시스템 호출을 통해 단말 uscitaTesto, argomenti query_VALORE, UDP Apri·inviare·ricevere·닫기를 제공한다. spazio_utente 코드를 kernel_VALORE 함수로 직접 호출하는 구조가 아니다.

```text
jkoros> apps
jkoros> run hello first second
jkoros> net
jkoros> run netcheck
jkoros> run udp 10.0.2.2 9000 hello
```

마지막 명령의 응답을 받으려면 호스트의 별도 터미널에서 `python3 /home/user/jkoros/os/strumenti/eco_schermo_dati.py --port 9000`을 먼저 실행한다. 상세 API, app_f5044b9b Aggiunta_voce, e_mail 공간과 제한은 [spazio_utente Esegui_comando·네트워크 README_eb81d7d9](spazio_utente/README_eb81d7d9.md)에 있다.

avvio_macchina verificare 문구:

```text
JKOROS NATIVE JAVA
자바 기계어 kernel_VALORE avvia
JAVA SELFTEST PASS
USER ELF: ring 3 / paging / int 0x80
help | info | mem | alloc | free N | echo TEXT | clear | test | halt
apps | run NAME [ARGS] | net
READY
jkoros>
```

## 구현한 기능

- GRUB Multiboot 1 ELF avvio_macchina, x86 proteggere_VALORE MODA_VALORE GDT, BSS inizializza, 64KiB operando_Pila.
- Java FUNZIONE_VALORE effettivo_dati 실행과 avvio_macchina msinfo32_exe marcatore_VALORE verificare.
- COM1 seriale_VALORE I_O, VGA 문자 schermata·cursore_VALORE·스크롤·cancellare_voce.
- PS/2 valore_predefinito 자판, 좌우 Shift, Enter, Backspace. estensione_VALORE tasto_VALORE/마우스 자료는 comando 입력으로 쓰지 않는다.
- durata_VALORE 128의 comando input_VALORE 버퍼, overflow_VALORE 방지, CR/LF Processi_VALORE_voce.
- `help`, `info`, `mem`, `alloc`, `free N`, `echo TEXT`, `clear`, `test`, `halt`.
- 4KiB 작업 sezione_VALORE 8개의 allocare_Memoria·Reso_KR·재사용과 중복 Reso_KR 방지.
- Java array_VALORE 256KiB 영역의 Dimensione·pedice_VALORE 검사와 런타임 errore 중단.
- Lettura 전용 JKAP Esegui_comando gruppo_VALORE, ELF32 sezione_VALORE/punto_di_ingresso convalidare, spazio_utente MODA_VALORE·argomenti·Esci_app CODICE_VALORE.
- kernel_VALORE/spazio_utente 페이지 privilegio_VALORE 분리, TSS, IDT, PIT 100Hz, spazio_utente CPU eccezione Processi_VALORE_voce 및 Esegui_comando valore 상한.
- PCI RTL8139 폴링 드라이버, ARP, statico_VALORE IPv4, UDP checksum·송수신·aspetta_VALORE 제한.

`mem`의 Upper memory는 Multiboot의 1MiB 위쪽 연속 Memoria_dati Dimensione(KiB)이며, 전체 Memoria_dati 지도 분석이나 자유 물리 Memoria_dati 수치가 아니다. `alloc`은 이미 확보한 intero array_VALORE 안의 작업 sezione_VALORE 번호를 반환한다. 일반 물리 pagina_VALORE allocare_Memoria, e_mail e_mail_area 또는 spazio_utente Processi_VALORE Memoria_dati 관리가 아니다.

## 명시적인 한계

이 커널은 **spazio_utente 프로그램을 한 번에 하나 실행하는 stato_iniziale kernel_VALORE**이다. PIT IRQ0만 사용하며 키보드와 NIC는 폴링한다. spazio_utente CPU 예외는 해당 프로그램을 끝내고 셸로 복귀시키지만 kernel_VALORE 예외는 중단한다. Esegui_comando 시간은 약 3초로 제한한다. 완전한 선점 다중 Processi_VALORE 스케줄러, FAT/ext 등 일반 디스크 file_system, TCP·DNS·DHCP·IPv6·HTTP, 전체 POSIX, 일반 oggetto_VALORE 모델/GC는 아직 없다. 전용 IDE file 보존과 POSIX file/UDP 일부 기능은 구현했다. JVM은 RAM 파일의 단일 클래스를 Esegui_comando 시 적재하며 일반 ClassLoader나 JAR 로딩은 지원하지 않는다. 네이티브 Esegui_comando 파일은 costruire 시 Lettura 전용 묶음에 넣으며, 일반 Linux ELF를 실행하는 환경이 아니다. 기존 `../legacy_fonte/`의 JVM 관리 kernel_VALORE 전체를 이식한 것도 아니다.

Java 식별자는 한국어다. seriale_VALORE 출력은 이 프로젝트의 한글(BMP 문자)을 UTF-8로 표시한다. VGA는 valore_predefinito ASCII 글꼴만 사용하므로 한글 자리에 `?`가 나온다. comando 입력도 Regolari_articolo ASCII만 지원하며 한글 tipo_di_carattere_VALORE·입력기 및 보조 평면 문자 출력은 후속 작업이다. `test`는 작은 배열을 새로 할당하고 GC가 없으므로 무한 반복하지 않는다.

## 자동 prove

`prove/부팅시험.py`는 디스크 없는 독립 QEMU를 생성해 다음을 검증하고 종료한다.

- ELF 직접 avvio_macchina 및 GRUB ISO avvio_macchina.
- Java nativo 시험과 UTF-8 seriale_VALORE 문구.
- comando mostra_aiuto·msinfo32_exe·Memoria_dati·uscitaTesto·errore input_VALORE·schermata cancellare_voce.
- 작업 sezione_VALORE 8개 allocare_Memoria, 부족 Processi_VALORE_voce, Reso_KR/중복 Reso_KR/재할당.
- seriale_VALORE 줄바꿈·백스페이스·긴 input_VALORE Processi_VALORE_voce.
- QEMU PS/2 tasto_VALORE 입력으로 `info` Esegui_comando, `halt` 정지.

성공 로그는 `build/부팅시험.json`에 남는다. 로컬 Unix 소켓을 금지하는 샌드박스에서는 prove 도구에 해당 권한이 필요하다. prove 도중 새로 만든 QEMU만 종료하며 기존 VM과 effettivo_dati 디스크는 건드리지 않는다.

`prove/test_Usenet.py`는 ELF/ISO 각각에서 spazio_utente ELF, effettivo_dati ring 3, argomenti, host 루프백 UDP 왕복, 1,023/1,024바이트 24회 연속 왕복, valore 초과, NIC 없음, Memoria_dati/hardware_porta accesso_voce 차단, CPU eccezione, 무한 sprint_VALORE, 잘못된 ELF를 시험한다. `build/test_Usenet.json`에 게스트 기록과 호스트가 받은 데이터의 durata_VALORE·해시를 저장한다. `prove/pacchetto_test.py`는 effettivo_dati Java valore_di_contratto 처리기에 손상된 패킷을 넣어 2,201개 limite_VALORE/checksum 조건을 검사한다. host 루프백 외 esterno_VALORE 서버에는 prove 트래픽을 보내지 않는다.

부트 경계는 GNU의 [Multiboot specifica](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html)를 따른다.

새 File_descrittore·C ABI·IDE Store_VALORE·Java file 흐름의 범위와 Italiano 명명 대응은 [posix-kor README_eb81d7d9](../posix-kor/README_eb81d7d9.md)에 있다. `make test-posix`로 ELF/ISO 실행과 재부팅 보존을 검증한다.
