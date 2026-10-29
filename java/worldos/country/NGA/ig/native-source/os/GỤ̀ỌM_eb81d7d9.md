# Java 네이티브 OS

이 문서는 기존 **x86 mkpụrụobī_kọmpùta_valuu**을 설명한다. Raspberry Pi 4의 자체 ARM64 초기 이식은 [별도 GỤ̀ỌM_eb81d7d9](../platforms/rpi4-native/README.md)를 참고한다. 아래 x86 òjìàrụ ELF·네트워크·IDE Store_valuu 기능이 ARM64에 모두 이식된 상태는 아니다.

Java 원문을 자체 AOT 후단으로 x86 기계어로 컴파일해 부팅하는 작은 운영체제다. 커널과 별도로 자체 제한형 Java 컴파일러·JVM ELF를 òjìàrụ 모드에 적재할 수 있다. Linux, engos, koros4와 외부 OpenJDK는 게스트에 적재하지 않는다. 부팅 진입과 ngwaike_pọọt/물리 기억공간 접근은 어셈블리이며, 문자 단말·입력 ùsòrò_valuu_ndebà·Ntiiwu kerìsịa_valuu·작업 nkebì_valuu 관리는 `ebensìbịa/*.java`에 있다.

## 게스트 Java 개발

`javac Hello.java`, `java Hello`로 부팅된 OS 안에서 wue_ebensìbịa·실행한다. `edit FILE.java`와 `.save`로 소스를 작성하며 `ls`, `cat`, `rm`을 제공한다. RAM 파일은 최대 8개, 각각 16KiB이다. 전용 IDE 매체를 연결하면 `sync`로 보존할 수 있다. 이 기능은 자체 제한형 구현이며 전체 OpenJDK/JDK 호환은 아니다. 사용법·nkwado_valuu 문법·Faịlụ 적재·교차 시험은 [Java 개발 환경](../문서/자바개발환경.md)에 있다. `make test-java`로 검증한다.

## 빌드와 mee_nnyemiwu

`compiler/`가 요구하는 도구에 더해 ISO 생성에는 `grub-file`, `grub-mkrescue`, GRUB BIOS 모듈, `xorriso`가 필요하다. 실행에는 QEMU 또는 VirtualBox가 필요하다. 현재 설치된 도구만 사용한다. `make run-store`는 새 전용 가상 Store_valuu 매체를 만들어 연결한다. VirtualBox 실행기는 이 프로젝트가 만든 전용 VM만 설정하고 다른 VM은 변경하지 않는다. 가상 메모리는 Ngwa_ihe_dịadị 64MiB이며 최소 16MiB가 필요하다.

```sh
cd /home/user/jkoros/os
make                 # build/kernel.elf
make iso             # build/kernel.iso (òjìàrụ ELF otu_valuu 포함)
make run             # ELF 직접 부팅, 직렬 단말
make run-gui         # GRUB ISO 부팅, VGA 창과 PS/2 자판
make vbox            # 상위 폴더의 실행기로 전용 VirtualBox VM mee_nnyemiwu
make vbox-status     # 전용 VirtualBox VM ọnọdụ_valuu nkwàdo_eziokwū
make test            # ELF와 ISO 두 경로의 ǹdịnezie_datà 부팅/입력 시험
make apps            # òjìàrụ 프로그램만 wue_sistèm
make test-network    # òjìàrụ mee_nnyemiwu/UDP/nchedo_valuu 시험
```

`make run`은 QEMU의 직렬 표준 입출력을 쓴다. `Ctrl+A`를 누른 Àzụ_valuu `X`로 QEMU를 종료할 수 있다. `halt`는 게스트 CPU만 정지시키므로 QEMU windò/프로세스는 별도로 닫는다. 폴링 방식이라 대기 중에도 usu CPU를 사용할 수 있다.

VirtualBox는 `make vbox`로 실행한다. 새 전용 VM을 memọrị_datà 64MiB, BIOS, 광학 드라이브 부팅으로 자동 설정하며 디스크는 필요 없다. ǹdịnezie_datà VirtualBox 5.2.42에서 부팅, Java 자체 시험, nkọwannyemiwu 입력, `run hello vbox`의 ring 3 실행과 정상 종료를 확인했다. 현재 통신 드라이버는 QEMU의 RTL8139 전용이며 VirtualBox의 PCnet/E1000에서는 네트워크를 사용할 수 없어 네트워크 장치를 비활성화한다. Store_valuu ọnọdụ_valuu 재개와 새 wue_sistèm 반영 방법은 [VirtualBox mee_nnyemiwu GỤ̀ỌM_eb81d7d9](../문서/가상상자실행.md)에 있다.

## 셸에서 òjìàrụ app_f5044b9b mee_nnyemiwu 및 네트워크 호출

독립 ELF32 mee_nnyemiwu 파일을 적재해 **ring 3**에서 실행한다. `int 0x80` 시스템 호출을 통해 단말 출력, 인수 mgbaajụjụ_valuu, UDP Mepee·zìga·받기·닫기를 제공한다. òjìàrụ 코드를 mkpụrụobī_kọmpùta_valuu 함수로 직접 호출하는 구조가 아니다.

```text
jkoros> apps
jkoros> run hello first second
jkoros> net
jkoros> run netcheck
jkoros> run udp 10.0.2.2 9000 hello
```

마지막 명령의 응답을 받으려면 호스트의 별도 터미널에서 `python3 /home/user/jkoros/os/Ngwaọrụ/자료되돌리기.py --port 9000`을 먼저 실행한다. 상세 API, app_f5044b9b 추가, àdreèsì 공간과 제한은 [òjìàrụ mee_nnyemiwu·네트워크 GỤ̀ỌM_eb81d7d9](òjìàrụ/GỤ̀ỌM_eb81d7d9.md)에 있다.

부팅 nkwàdo_eziokwū 문구:

```text
JKOROS NATIVE JAVA
자바 기계어 mkpụrụobī_kọmpùta_valuu Bido
JAVA SELFTEST PASS
USER ELF: ring 3 / paging / int 0x80
help | info | mem | alloc | free N | echo TEXT | clear | test | halt
apps | run NAME [ARGS] | net
READY
jkoros>
```

## 구현한 기능

- GRUB Multiboot 1 ELF 부팅, x86 nchedo_valuu moòdù_valuu GDT, BSS kwàdo_mmàlite, 64KiB 스택.
- Java ọrụ_valuu ǹdịnezie_datà 실행과 부팅 Ozi_Sistèm 표식 nkwàdo_eziokwū.
- COM1 직렬 I_O, VGA 문자 화면·akàran̄ziebe_valuu·스크롤·지우기.
- PS/2 Ngwa_ihe_dịadị 자판, 좌우 Shift, Enter, Backspace. mgbatị_valuu ọtụgwo_valuu/마우스 자료는 Ntiiwu 입력으로 쓰지 않는다.
- ogologo_valuu 128의 Ntiiwu 입력 버퍼, njubigaoke_valuu 방지, CR/LF ùsòrò_valuu_ndebà.
- `help`, `info`, `mem`, `alloc`, `free N`, `echo TEXT`, `clear`, `test`, `halt`.
- 4KiB 작업 nkebì_valuu 8개의 kepụta_Nchekwa·반환·재사용과 중복 반환 방지.
- Java MKPOKỌTA_valuu 256KiB 영역의 Ụhara·ntụkwàsa_n_akụkụ_n_àlà_valuu 검사와 런타임 mmejọ 중단.
- Wepụta_ọzi 전용 JKAP mee_nnyemiwu otu_valuu, ELF32 nkebì_valuu/ndebà_akara mee_ịbanihe, òjìàrụ moòdù_valuu·인수·pụọ_app 코드.
- mkpụrụobī_kọmpùta_valuu/òjìàrụ 페이지 ikikere_valuu 분리, TSS, IDT, PIT 100Hz, òjìàrụ CPU 예외 ùsòrò_valuu_ndebà 및 mee_nnyemiwu 시간 상한.
- PCI RTL8139 폴링 드라이버, ARP, adịmgbanwò_valuu IPv4, UDP 검사합·송수신·대기 제한.

`mem`의 Upper memory는 Multiboot의 1MiB 위쪽 연속 memọrị_datà Ụhara(KiB)이며, 전체 memọrị_datà 지도 분석이나 자유 물리 memọrị_datà 수치가 아니다. `alloc`은 이미 확보한 ọnụọgụ_nzùrùòkè MKPOKỌTA_valuu 안의 작업 nkebì_valuu 번호를 반환한다. 일반 물리 ihuakwụkwọ_valuu kepụta_Nchekwa, àdreèsì 공간 또는 òjìàrụ ùsòrò_valuu_6712bde7 memọrị_datà 관리가 아니다.

## 명시적인 한계

이 커널은 **òjìàrụ 프로그램을 한 번에 하나 실행하는 초기 mkpụrụobī_kọmpùta_valuu**이다. PIT IRQ0만 사용하며 키보드와 NIC는 폴링한다. òjìàrụ CPU 예외는 해당 프로그램을 끝내고 셸로 복귀시키지만 mkpụrụobī_kọmpùta_valuu 예외는 중단한다. mee_nnyemiwu 시간은 약 3초로 제한한다. 완전한 선점 다중 ùsòrò_valuu_6712bde7 스케줄러, FAT/ext 등 일반 디스크 sistèm_ọbọakwụkwo, TCP·DNS·DHCP·IPv6·HTTP, 전체 POSIX, 일반 ihe_valuu 모델/GC는 아직 없다. 전용 IDE Faịlụ 보존과 POSIX Faịlụ/UDP 일부 기능은 구현했다. JVM은 RAM 파일의 단일 클래스를 mee_nnyemiwu 시 적재하며 일반 ClassLoader나 JAR 로딩은 지원하지 않는다. 네이티브 mee_nnyemiwu 파일은 wue_sistèm 시 Wepụta_ọzi 전용 묶음에 넣으며, 일반 Linux ELF를 실행하는 환경이 아니다. 기존 `../ekpe_ebensìbịa/`의 JVM 관리 mkpụrụobī_kọmpùta_valuu 전체를 이식한 것도 아니다.

Java 식별자는 한국어다. 직렬 출력은 이 프로젝트의 한글(BMP 문자)을 UTF-8로 표시한다. VGA는 Ngwa_ihe_dịadị ASCII 글꼴만 사용하므로 한글 자리에 `?`가 나온다. Ntiiwu 입력도 현재 ASCII만 지원하며 한글 ọnụndèe_valuu·입력기 및 보조 평면 문자 출력은 후속 작업이다. `test`는 작은 배열을 새로 할당하고 GC가 없으므로 무한 반복하지 않는다.

## 자동 시험

`시험/부팅시험.py`는 디스크 없는 독립 QEMU를 생성해 다음을 검증하고 종료한다.

- ELF 직접 부팅 및 GRUB ISO 부팅.
- Java 자체 시험과 UTF-8 직렬 문구.
- Ntiiwu gòsi_ènyèmaka·Ozi_Sistèm·memọrị_datà·출력·mmejọ 입력·화면 지우기.
- 작업 nkebì_valuu 8개 kepụta_Nchekwa, 부족 ùsòrò_valuu_ndebà, 반환/중복 반환/재할당.
- 직렬 줄바꿈·백스페이스·긴 입력 ùsòrò_valuu_ndebà.
- QEMU PS/2 ọtụgwo_valuu 입력으로 `info` mee_nnyemiwu, `halt` 정지.

성공 로그는 `build/부팅시험.json`에 남는다. 로컬 Unix 소켓을 금지하는 샌드박스에서는 시험 도구에 해당 권한이 필요하다. 시험 도중 새로 만든 QEMU만 종료하며 기존 VM과 ǹdịnezie_datà 디스크는 건드리지 않는다.

`시험/사용자통신시험.py`는 ELF/ISO 각각에서 òjìàrụ ELF, ǹdịnezie_datà ring 3, 인수, usu 루프백 UDP 왕복, 1,023/1,024바이트 24회 연속 왕복, 시간 초과, NIC 없음, memọrị_datà/ngwaike_pọọt òhèrè_ndebà 차단, CPU 예외, 무한 memmekwa_valuu, 잘못된 ELF를 시험한다. `build/사용자통신시험.json`에 게스트 기록과 호스트가 받은 데이터의 ogologo_valuu·해시를 저장한다. `시험/패킷시험.py`는 ǹdịnezie_datà Java ngō_valuu 처리기에 손상된 패킷을 넣어 2,201개 경계/검사합 조건을 검사한다. usu 루프백 외 외부 서버에는 시험 트래픽을 보내지 않는다.

부트 경계는 GNU의 [Multiboot 명세](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html)를 따른다.

새 파일서술자·C ABI·IDE Store_valuu·Java Faịlụ 흐름의 범위와 한국어 명명 대응은 [posix-kor GỤ̀ỌM_eb81d7d9](../posix-kor/GỤ̀ỌM_eb81d7d9.md)에 있다. `make test-posix`로 ELF/ISO 실행과 재부팅 보존을 검증한다.
