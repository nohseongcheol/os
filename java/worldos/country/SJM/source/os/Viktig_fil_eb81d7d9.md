# Java 네이티브 operativsystem

이 문서는 기존 **x86 kjerne_VERDI**을 설명한다. Raspberry Pi 4의 eget ARM64 opprinnelig_tilstand 이식은 [별도 Viktig_fil_eb81d7d9](../platforms/rpi4-native/README.md)를 참고한다. 아래 x86 bruker ELF·네트워크·IDE Store_VERDI 기능이 ARM64에 모두 이식된 상태는 아니다.

Java 원문을 eget AOT 후단으로 x86 기계어로 컴파일해 부팅하는 작은 운영체제다. 커널과 별도로 eget 제한형 Java kompilator·JVM ELF를 bruker 모드에 적재할 nummer 있다. Linux, engos, koros4와 ekstern_VERDI OpenJDK는 게스트에 적재하지 않는다. 부팅 진입과 maskinvare_port/물리 Minne_område 접근은 어셈블리이며, 문자 단말·inndata_VERDI Prosess_VERDI_oppføring·Kommando dele_opp_VERDI·작업 inndeling_VERDI 관리는 `KILDE/*.java`에 있다.

## 게스트 Java utviklet_materiale

`javac Hello.java`, `java Hello`로 부팅된 operativsystem 안에서 kompilere_kilde·실행한다. `edit FILE.java`와 `.save`로 소스를 작성하며 `ls`, `cat`, `rm`을 제공한다. RAM 파일은 최대 8개, 각각 16KiB이다. 전용 IDE 매체를 연결하면 `sync`로 보존할 nummer 있다. 이 기능은 eget 제한형 구현이며 전체 OpenJDK/JDK 호환은 아니다. 사용법·støtte_VERDI 문법·Fil 적재·교차 시험은 [Java utviklet_materiale miljø](../문서/Java_IDE.md)에 있다. `make test-java`로 검증한다.

## 빌드와 Utfør_kommando

`compiler/`가 요구하는 도구에 더해 ISO 생성에는 `grub-file`, `grub-mkrescue`, GRUB BIOS modul_VERDI, `xorriso`가 필요하다. 실행에는 QEMU 또는 VirtualBox가 필요하다. betalt_vare 설치된 도구만 사용한다. `make run-store`는 새 전용 가상 Store_VERDI 매체를 만들어 연결한다. VirtualBox 실행기는 이 프로젝트가 만든 전용 VM만 설정하고 다른 VM은 변경하지 않는다. 가상 메모리는 standardverdi 64MiB이며 최소 16MiB가 필요하다.

```sh
cd /home/user/jkoros/os
make                 # build/kernel.elf
make iso             # build/kernel.iso (bruker ELF gruppe_VERDI 포함)
make run             # ELF 직접 부팅, 직렬 단말
make run-gui         # GRUB ISO 부팅, VGA 창과 PS/2 자판
make vbox            # 상위 폴더의 실행기로 전용 VirtualBox VM Utfør_kommando
make vbox-status     # 전용 VirtualBox VM status_VERDI bekrefte
make test            # ELF와 ISO 두 경로의 faktisk_data 부팅/inndata_VERDI 시험
make apps            # bruker 프로그램만 bygg_System
make test-network    # bruker Utfør_kommando/UDP/beskytte_VERDI 시험
```

`make run`은 QEMU의 직렬 표준 입출력을 쓴다. `Ctrl+A`를 누른 TILBAKE_VERDI `X`로 QEMU를 종료할 nummer 있다. `halt`는 게스트 CPU만 정지시키므로 QEMU Vindu/프로세스는 별도로 닫는다. 폴링 방식이라 vent_VERDI 중에도 vert CPU를 사용할 nummer 있다.

VirtualBox는 `make vbox`로 실행한다. 새 전용 VM을 Minne_data 64MiB, BIOS, 광학 드라이브 부팅으로 자동 설정하며 디스크는 필요 없다. faktisk_data VirtualBox 5.2.42에서 부팅, Java eget 시험, Shell inndata_VERDI, `run hello vbox`의 ring 3 실행과 informasjonssystemer_normal 종료를 확인했다. betalt_vare 통신 드라이버는 QEMU의 RTL8139 전용이며 VirtualBox의 PCnet/E1000에서는 네트워크를 사용할 nummer 없어 네트워크 장치를 비활성화한다. Store_VERDI status_VERDI 재개와 새 bygg_System 반영 방법은 [VirtualBox Utfør_kommando Viktig_fil_eb81d7d9](../문서/가상상자실행.md)에 있다.

## 셸에서 bruker app_f5044b9b Utfør_kommando 및 네트워크 호출

독립 ELF32 Utfør_kommando 파일을 적재해 **ring 3**에서 실행한다. `int 0x80` 시스템 호출을 통해 단말 Utgang, Argumenter spørre_VERDI, UDP Åpne·sende·motta·닫기를 제공한다. bruker 코드를 kjerne_VERDI 함수로 직접 호출하는 구조가 아니다.

```text
jkoros> apps
jkoros> run hello first second
jkoros> net
jkoros> run netcheck
jkoros> run udp 10.0.2.2 9000 hello
```

마지막 명령의 응답을 받으려면 호스트의 별도 터미널에서 `python3 /home/user/jkoros/os/Verktøy/oppdatere_skjerm_data.py --port 9000`을 먼저 실행한다. 상세 API, app_f5044b9b Tilføye_oppføring, e_post 공간과 제한은 [bruker Utfør_kommando·네트워크 Viktig_fil_eb81d7d9](bruker/Viktig_fil_eb81d7d9.md)에 있다.

부팅 bekrefte 문구:

```text
JKOROS NATIVE JAVA
자바 기계어 kjerne_VERDI Kjør_2
JAVA SELFTEST PASS
USER ELF: ring 3 / paging / int 0x80
help | info | mem | alloc | free N | echo TEXT | clear | test | halt
apps | run NAME [ARGS] | net
READY
jkoros>
```

## 구현한 기능

- GRUB Multiboot 1 ELF 부팅, x86 beskytte_VERDI MODUS_VERDI GDT, BSS starte, 64KiB operand_stakk.
- Java FUNKSJON_VERDI faktisk_data 실행과 부팅 msinfo32_exe tusj_VERDI bekrefte.
- COM1 직렬 I_U, VGA 문자 skjermbilde·markør_VERDI·스크롤·slette_oppføring.
- PS/2 standardverdi 자판, 좌우 Shift, Enter, Backspace. filtype_VERDI tast_VERDI/마우스 자료는 Kommando 입력으로 쓰지 않는다.
- lengde_VERDI 128의 Kommando inndata_VERDI 버퍼, overløp_VERDI 방지, CR/LF Prosess_VERDI_oppføring.
- `help`, `info`, `mem`, `alloc`, `free N`, `echo TEXT`, `clear`, `test`, `halt`.
- 4KiB 작업 inndeling_VERDI 8개의 tildele_lager·return_KR·재사용과 중복 return_KR 방지.
- Java MATRISE_VERDI 256KiB 영역의 Størrelse·senket_skrift_VERDI 검사와 런타임 feil 중단.
- Les 전용 JKAP Utfør_kommando gruppe_VERDI, ELF32 inndeling_VERDI/inngangspunkt bekrefte_5fb2b747, bruker MODUS_VERDI·Argumenter·Utgang_app KODE_VERDI.
- kjerne_VERDI/bruker 페이지 tillatelse_VERDI 분리, TSS, IDT, PIT 100Hz, bruker CPU unntak Prosess_VERDI_oppføring 및 Utfør_kommando TID_VERDI 상한.
- PCI RTL8139 폴링 드라이버, ARP, statisk_VERDI IPv4, UDP kontrollsum·송수신·vent_VERDI 제한.

`mem`의 Upper memory는 Multiboot의 1MiB 위쪽 연속 Minne_data Størrelse(KiB)이며, 전체 Minne_data 지도 분석이나 자유 물리 Minne_data 수치가 아니다. `alloc`은 이미 확보한 heltall MATRISE_VERDI 안의 작업 inndeling_VERDI 번호를 반환한다. 일반 물리 page_VERDI tildele_lager, e_post e_post_område 또는 bruker Prosess_VERDI Minne_data 관리가 아니다.

## 명시적인 한계

이 커널은 **bruker 프로그램을 한 번에 하나 실행하는 opprinnelig_tilstand kjerne_VERDI**이다. PIT IRQ0만 사용하며 키보드와 NIC는 폴링한다. bruker CPU 예외는 해당 프로그램을 끝내고 셸로 복귀시키지만 kjerne_VERDI 예외는 중단한다. Utfør_kommando 시간은 약 3초로 제한한다. 완전한 선점 다중 Prosess_VERDI 스케줄러, FAT/ext 등 일반 디스크 filsystem, TCP·DNS·DHCP·IPv6·HTTP, 전체 POSIX, 일반 objekt_VERDI 모델/GC는 아직 없다. 전용 IDE Fil 보존과 POSIX Fil/UDP 일부 기능은 구현했다. JVM은 RAM 파일의 단일 클래스를 Utfør_kommando 시 적재하며 일반 ClassLoader나 JAR 로딩은 지원하지 않는다. 네이티브 Utfør_kommando 파일은 bygg_System 시 Les 전용 묶음에 넣으며, 일반 Linux ELF를 실행하는 환경이 아니다. 기존 `../eldre_kilde/`의 JVM 관리 kjerne_VERDI 전체를 이식한 것도 아니다.

Java 식별자는 한국어다. 직렬 출력은 이 프로젝트의 한글(BMP 문자)을 UTF-8로 표시한다. VGA는 standardverdi ASCII 글꼴만 사용하므로 한글 자리에 `?`가 나온다. Kommando 입력도 betalt_vare ASCII만 지원하며 한글 skrift_VERDI·입력기 및 보조 평면 문자 출력은 후속 작업이다. `test`는 작은 배열을 새로 할당하고 GC가 없으므로 무한 반복하지 않는다.

## 자동 시험

`시험/부팅시험.py`는 디스크 없는 독립 QEMU를 생성해 다음을 검증하고 종료한다.

- ELF 직접 부팅 및 GRUB ISO 부팅.
- Java eget 시험과 UTF-8 직렬 문구.
- Kommando vise_hjelp·msinfo32_exe·Minne_data·Utgang·feil inndata_VERDI·skjermbilde slette_oppføring.
- 작업 inndeling_VERDI 8개 tildele_lager, 부족 Prosess_VERDI_oppføring, return_KR/중복 return_KR/재할당.
- 직렬 줄바꿈·백스페이스·긴 inndata_VERDI Prosess_VERDI_oppføring.
- QEMU PS/2 tast_VERDI 입력으로 `info` Utfør_kommando, `halt` 정지.

성공 로그는 `build/부팅시험.json`에 남는다. 로컬 Unix 소켓을 금지하는 샌드박스에서는 시험 도구에 해당 권한이 필요하다. 시험 도중 새로 만든 QEMU만 종료하며 기존 VM과 faktisk_data 디스크는 건드리지 않는다.

`시험/test_bruker_nettverk.py`는 ELF/ISO 각각에서 bruker ELF, faktisk_data ring 3, Argumenter, vert 루프백 UDP 왕복, 1,023/1,024바이트 24회 연속 왕복, TID_VERDI 초과, NIC 없음, Minne_data/maskinvare_port tilgang_oppføring 차단, CPU unntak, 무한 sprint_VERDI, 잘못된 ELF를 시험한다. `build/test_bruker_nettverk.json`에 게스트 기록과 호스트가 받은 데이터의 lengde_VERDI·해시를 저장한다. `시험/pakke_test.py`는 faktisk_data Java kontraktverdi 처리기에 손상된 패킷을 넣어 2,201개 grense_VERDI/kontrollsum 조건을 검사한다. vert 루프백 외 ekstern_VERDI 서버에는 시험 트래픽을 보내지 않는다.

부트 경계는 GNU의 [Multiboot 명세](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html)를 따른다.

새 파일서술자·C ABI·IDE Store_VERDI·Java Fil 흐름의 범위와 norsk 명명 대응은 [posix-kor Viktig_fil_eb81d7d9](../posix-kor/Viktig_fil_eb81d7d9.md)에 있다. `make test-posix`로 ELF/ISO 실행과 재부팅 보존을 검증한다.
