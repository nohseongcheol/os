# Java 네이티브 operativsystem

이 문서는 기존 **x86 kärna_värde**을 설명한다. Raspberry Pi 4의 eget ARM64 starttillstånd 이식은 [별도 VIKTIGT_eb81d7d9](../platforms/rpi4-native/README.md)를 참고한다. 아래 x86 användarutrymme ELF·네트워크·IDE Store_värde 기능이 ARM64에 모두 이식된 상태는 아니다.

Java 원문을 eget AOT 후단으로 x86 기계어로 컴파일해 부팅하는 작은 운영체제다. 커널과 별도로 eget 제한형 Java kompilerare·JVM ELF를 användarutrymme 모드에 적재할 nummer 있다. Linux, engos, koros4와 extern_värde OpenJDK는 게스트에 적재하지 않는다. maskinstart 진입과 maskinvara_port/물리 Minne_område 접근은 어셈블리이며, 문자 단말·indata_värde Process_värde_post·kommando parsa_värde·작업 avsnitt_värde 관리는 `källfil/*.java`에 있다.

## 게스트 Java utveckling

`javac Hello.java`, `java Hello`로 부팅된 operativsystem 안에서 kompilera_källa·실행한다. `edit FILE.java`와 `.save`로 소스를 작성하며 `ls`, `cat`, `rm`을 제공한다. RAM 파일은 최대 8개, 각각 16KiB이다. 전용 IDE 매체를 연결하면 `sync`로 보존할 nummer 있다. 이 기능은 eget 제한형 구현이며 전체 OpenJDK/JDK 호환은 아니다. 사용법·stöd_värde 문법·filnamn 적재·교차 시험은 [Java utveckling miljö](../문서/Java_IDE.md)에 있다. `make test-java`로 검증한다.

## 빌드와 köra_kommando

`compiler/`가 요구하는 도구에 더해 ISO 생성에는 `grub-file`, `grub-mkrescue`, GRUB BIOS modul_värde, `xorriso`가 필요하다. 실행에는 QEMU 또는 VirtualBox가 필요하다. aktuellt_objekt 설치된 도구만 사용한다. `make run-store`는 새 전용 가상 Store_värde 매체를 만들어 연결한다. VirtualBox 실행기는 이 프로젝트가 만든 전용 VM만 설정하고 다른 VM은 변경하지 않는다. 가상 메모리는 standardvärde 64MiB이며 최소 16MiB가 필요하다.

```sh
cd /home/user/jkoros/os
make                 # build/kernel.elf
make iso             # build/kernel.iso (användarutrymme ELF grupp_värde deklarationer)
make run             # ELF 직접 maskinstart, 직렬 단말
make run-gui         # GRUB ISO maskinstart, VGA 창과 PS/2 자판
make vbox            # 상위 폴더의 실행기로 전용 VirtualBox VM köra_kommando
make vbox-status     # 전용 VirtualBox VM status_värde verifiera
make test            # ELF와 ISO 두 경로의 verklig_data maskinstart/indata_värde tester
make apps            # användarutrymme 프로그램만 version_System
make test-network    # användarutrymme köra_kommando/UDP/skydda_värde tester
```

`make run`은 QEMU의 직렬 표준 입출력을 쓴다. `Ctrl+A`를 누른 BACK_värde `X`로 QEMU를 종료할 nummer 있다. `halt`는 게스트 CPU만 정지시키므로 QEMU Fönster/프로세스는 별도로 닫는다. 폴링 방식이라 vänta_värde 중에도 värd CPU를 사용할 nummer 있다.

VirtualBox는 `make vbox`로 실행한다. 새 전용 VM을 Minne_data 64MiB, BIOS, 광학 드라이브 부팅으로 자동 설정하며 디스크는 필요 없다. verklig_data VirtualBox 5.2.42에서 maskinstart, Java eget tester, Shell indata_värde, `run hello vbox`의 ring 3 실행과 informationsteknik_normal 종료를 확인했다. aktuellt_objekt kommunikation 드라이버는 QEMU의 RTL8139 전용이며 VirtualBox의 PCnet/E1000에서는 네트워크를 사용할 nummer 없어 네트워크 장치를 비활성화한다. Store_värde status_värde 재개와 새 version_System 반영 방법은 [VirtualBox köra_kommando VIKTIGT_eb81d7d9](../문서/가상상자실행.md)에 있다.

## 셸에서 användarutrymme app_f5044b9b köra_kommando 및 네트워크 호출

독립 ELF32 köra_kommando 파일을 적재해 **ring 3**에서 실행한다. `int 0x80` 시스템 호출을 통해 단말 utmatningsposition, argument fråga_värde, UDP Öppna·skicka·få·닫기를 제공한다. användarutrymme 코드를 kärna_värde 함수로 직접 호출하는 구조가 아니다.

```text
jkoros> apps
jkoros> run hello first second
jkoros> net
jkoros> run netcheck
jkoros> run udp 10.0.2.2 9000 hello
```

마지막 명령의 응답을 받으려면 호스트의 별도 터미널에서 `python3 /home/user/jkoros/os/verktyg/UppdateraSkärm_data.py --port 9000`을 먼저 실행한다. 상세 API, app_f5044b9b Lägga_till_post, Adress 공간과 제한은 [användarutrymme köra_kommando·네트워크 VIKTIGT_eb81d7d9](användarutrymme/VIKTIGT_eb81d7d9.md)에 있다.

maskinstart verifiera 문구:

```text
JKOROS NATIVE JAVA
자바 기계어 kärna_värde Kör
JAVA SELFTEST PASS
USER ELF: ring 3 / paging / int 0x80
help | info | mem | alloc | free N | echo TEXT | clear | test | halt
apps | run NAME [ARGS] | net
READY
jkoros>
```

## 구현한 기능

- GRUB Multiboot 1 ELF maskinstart, x86 skydda_värde läge_värde GDT, BSS starta, 64KiB operand_Stack.
- Java FUNKTION_värde verklig_data 실행과 maskinstart msinfo32_exe markör_värde verifiera.
- COM1 직렬 indata_utleverans, VGA 문자 skärmbild·markör_värde_04ee3e20·스크롤·radera_post.
- PS/2 standardvärde 자판, 좌우 Shift, Enter, Backspace. tillägg_värde Nyckel_värde/마우스 자료는 kommando 입력으로 쓰지 않는다.
- längd_värde 128의 kommando indata_värde 버퍼, spill_värde 방지, CR/LF Process_värde_post.
- `help`, `info`, `mem`, `alloc`, `free N`, `echo TEXT`, `clear`, `test`, `halt`.
- 4KiB 작업 avsnitt_värde 8개의 allokera_minne·Retur_KR·재사용과 중복 Retur_KR 방지.
- Java MATRIS_värde 256KiB 영역의 Storlek·nedsänkt_text_värde 검사와 런타임 fel 중단.
- Läs 전용 JKAP köra_kommando grupp_värde, ELF32 avsnitt_värde/startpunkt validera, användarutrymme läge_värde·argument·Utgång_app KOD_värde.
- kärna_värde/användarutrymme 페이지 behörighet_värde 분리, TSS, IDT, PIT 100Hz, användarutrymme CPU fel_31f743d2 Process_värde_post 및 köra_kommando tid_värde 상한.
- PCI RTL8139 폴링 드라이버, ARP, statisk_värde IPv4, UDP kontrollsumma·송수신·vänta_värde 제한.

`mem`의 Upper memory는 Multiboot의 1MiB 위쪽 연속 Minne_data Storlek(KiB)이며, 전체 Minne_data 지도 분석이나 자유 물리 Minne_data 수치가 아니다. `alloc`은 이미 확보한 heltal MATRIS_värde 안의 작업 avsnitt_värde 번호를 반환한다. 일반 물리 page_värde allokera_minne, Adress ADRESS_område 또는 användarutrymme Process_värde Minne_data 관리가 아니다.

## 명시적인 한계

이 커널은 **användarutrymme 프로그램을 한 번에 하나 실행하는 starttillstånd kärna_värde**이다. PIT IRQ0만 사용하며 키보드와 NIC는 폴링한다. användarutrymme CPU 예외는 해당 프로그램을 끝내고 셸로 복귀시키지만 kärna_värde 예외는 중단한다. köra_kommando 시간은 약 3초로 제한한다. 완전한 선점 다중 Process_värde 스케줄러, FAT/ext 등 일반 디스크 filsystem, TCP·DNS·DHCP·IPv6·HTTP, 전체 POSIX, 일반 objekt_värde 모델/GC는 아직 없다. 전용 IDE filnamn 보존과 POSIX filnamn/UDP 일부 기능은 구현했다. JVM은 RAM 파일의 단일 클래스를 köra_kommando 시 적재하며 일반 ClassLoader나 JAR 로딩은 지원하지 않는다. 네이티브 köra_kommando 파일은 version_System 시 Läs 전용 묶음에 넣으며, 일반 Linux ELF를 실행하는 환경이 아니다. 기존 `../äldre_källa/`의 JVM 관리 kärna_värde 전체를 이식한 것도 아니다.

Java 식별자는 한국어다. 직렬 출력은 이 프로젝트의 한글(BMP 문자)을 UTF-8로 표시한다. VGA는 standardvärde ASCII 글꼴만 사용하므로 한글 자리에 `?`가 나온다. kommando 입력도 aktuellt_objekt ASCII만 지원하며 한글 teckensnitt_värde·입력기 및 보조 평면 문자 출력은 후속 작업이다. `test`는 작은 배열을 새로 할당하고 GC가 없으므로 무한 반복하지 않는다.

## 자동 tester

`tester/부팅시험.py`는 디스크 없는 독립 QEMU를 생성해 다음을 검증하고 종료한다.

- ELF 직접 maskinstart 및 GRUB ISO maskinstart.
- Java eget 시험과 UTF-8 직렬 문구.
- kommando visa_hjälp·msinfo32_exe·Minne_data·utmatningsposition·fel indata_värde·skärmbild radera_post.
- 작업 avsnitt_värde 8개 allokera_minne, 부족 Process_värde_post, Retur_KR/중복 Retur_KR/재할당.
- 직렬 줄바꿈·백스페이스·긴 indata_värde Process_värde_post.
- QEMU PS/2 Nyckel_värde 입력으로 `info` köra_kommando, `halt` 정지.

성공 로그는 `build/부팅시험.json`에 남는다. 로컬 Unix 소켓을 금지하는 샌드박스에서는 tester 도구에 해당 권한이 필요하다. tester 도중 새로 만든 QEMU만 종료하며 기존 VM과 verklig_data 디스크는 건드리지 않는다.

`tester/test_användare_nätverk.py`는 ELF/ISO 각각에서 användarutrymme ELF, verklig_data ring 3, argument, värd 루프백 UDP 왕복, 1,023/1,024바이트 24회 연속 왕복, tid_värde 초과, NIC 없음, Minne_data/maskinvara_port ansluta_post 차단, CPU fel_31f743d2, 무한 sprint_värde, 잘못된 ELF를 시험한다. `build/test_användare_nätverk.json`에 게스트 기록과 호스트가 받은 데이터의 längd_värde·해시를 저장한다. `tester/paket_test.py`는 verklig_data Java kontraktsvärde 처리기에 손상된 패킷을 넣어 2,201개 gräns_värde/kontrollsumma 조건을 검사한다. värd 루프백 외 extern_värde 서버에는 tester 트래픽을 보내지 않는다.

부트 경계는 GNU의 [Multiboot 명세](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html)를 따른다.

새 파일서술자·C ABI·IDE Store_värde·Java filnamn 흐름의 범위와 Svenska 명명 대응은 [posix-kor VIKTIGT_eb81d7d9](../posix-kor/VIKTIGT_eb81d7d9.md)에 있다. `make test-posix`로 ELF/ISO 실행과 재부팅 보존을 검증한다.
