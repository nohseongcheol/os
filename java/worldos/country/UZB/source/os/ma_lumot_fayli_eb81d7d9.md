# Java 네이티브 operatsion_tizim

이 문서는 기존 **x86 o_zak_VALUE**을 설명한다. Raspberry Pi 4의 자체 ARM64 초기 이식은 [별도 ma_lumot_fayli_eb81d7d9](../platforms/rpi4-native/README.md)를 참고한다. 아래 x86 foydalanuvchi ELF·네트워크·IDE Store_VALUE 기능이 ARM64에 모두 이식된 상태는 아니다.

Java 원문을 자체 AOT 후단으로 x86 기계어로 컴파일해 부팅하는 작은 운영체제다. 커널과 별도로 자체 제한형 Java 컴파일러·JVM ELF를 foydalanuvchi 모드에 적재할 수 있다. Linux, engos, koros4와 외부 OpenJDK는 게스트에 적재하지 않는다. 부팅 진입과 포트/물리 기억공간 접근은 어셈블리이며, 문자 단말·입력 Jarayon_VALUE_kiritish·Buyruq tahlil_qilmoq_VALUE·작업 bo_lim_VALUE_366e0bfa 관리는 `manba/*.java`에 있다.

## 게스트 Java 개발

`javac Hello.java`, `java Hello`로 부팅된 operatsion_tizim 안에서 yig_moq_manba·실행한다. `edit FILE.java`와 `.save`로 소스를 작성하며 `ls`, `cat`, `rm`을 제공한다. RAM 파일은 최대 8개, 각각 16KiB이다. 전용 IDE 매체를 연결하면 `sync`로 보존할 수 있다. 이 기능은 자체 제한형 구현이며 전체 OpenJDK/JDK 호환은 아니다. 사용법·madad_VALUE 문법·Fayl 적재·교차 시험은 [Java 개발 환경](../문서/자바개발환경.md)에 있다. `make test-java`로 검증한다.

## 빌드와 bajarmoq_buyruq

`compiler/`가 요구하는 도구에 더해 ISO 생성에는 `grub-file`, `grub-mkrescue`, GRUB BIOS modul_VALUE, `xorriso`가 필요하다. 실행에는 QEMU 또는 VirtualBox가 필요하다. 현재 설치된 도구만 사용한다. `make run-store`는 새 전용 가상 Store_VALUE 매체를 만들어 연결한다. VirtualBox 실행기는 이 프로젝트가 만든 전용 VM만 설정하고 다른 VM은 변경하지 않는다. 가상 메모리는 sukut_bo_yicha_qiymat 64MiB이며 최소 16MiB가 필요하다.

```sh
cd /home/user/jkoros/os
make                 # build/kernel.elf
make iso             # build/kernel.iso (foydalanuvchi ELF Guruh_VALUE 포함)
make run             # ELF 직접 부팅, 직렬 단말
make run-gui         # GRUB ISO 부팅, VGA 창과 PS/2 자판
make vbox            # 상위 폴더의 실행기로 전용 VirtualBox VM bajarmoq_buyruq
make vbox-status     # 전용 VirtualBox VM holat_VALUE_e10195a1 tasdiqlamoq
make test            # ELF와 ISO 두 경로의 real_ma_lumotlar 부팅/입력 시험
make apps            # foydalanuvchi 프로그램만 nashr_tizim
make test-network    # foydalanuvchi bajarmoq_buyruq/UDP/himoya_qilmoq_VALUE 시험
```

`make run`은 QEMU의 직렬 표준 입출력을 쓴다. `Ctrl+A`를 누른 Orqaga_VALUE `X`로 QEMU를 종료할 수 있다. `halt`는 게스트 CPU만 정지시키므로 QEMU oyna/프로세스는 별도로 닫는다. 폴링 방식이라 bir_daqiqa_VALUE 중에도 tashkilotchi CPU를 사용할 수 있다.

VirtualBox는 `make vbox`로 실행한다. 새 전용 VM을 Xotira_ma_lumotlar 64MiB, BIOS, 광학 드라이브 부팅으로 자동 설정하며 디스크는 필요 없다. real_ma_lumotlar VirtualBox 5.2.42에서 부팅, Java 자체 시험, qobiq 입력, `run hello vbox`의 ring 3 실행과 정상 종료를 확인했다. 현재 통신 드라이버는 QEMU의 RTL8139 전용이며 VirtualBox의 PCnet/E1000에서는 네트워크를 사용할 수 없어 네트워크 장치를 비활성화한다. Store_VALUE holat_VALUE_e10195a1 재개와 새 nashr_tizim 반영 방법은 [VirtualBox bajarmoq_buyruq ma_lumot_fayli_eb81d7d9](../문서/가상상자실행.md)에 있다.

## 셸에서 foydalanuvchi ilova_f5044b9b bajarmoq_buyruq 및 네트워크 호출

독립 ELF32 bajarmoq_buyruq 파일을 적재해 **ring 3**에서 실행한다. `int 0x80` 시스템 호출을 통해 단말 출력, 인수 so_rov_VALUE, UDP Ochish·yuborish·받기·닫기를 제공한다. foydalanuvchi 코드를 o_zak_VALUE 함수로 직접 호출하는 구조가 아니다.

```text
jkoros> apps
jkoros> run hello first second
jkoros> net
jkoros> run netcheck
jkoros> run udp 10.0.2.2 9000 hello
```

마지막 명령의 응답을 받으려면 호스트의 별도 터미널에서 `python3 /home/user/jkoros/os/Vositalar/자료되돌리기.py --port 9000`을 먼저 실행한다. 상세 API, ilova_f5044b9b 추가, manzil 공간과 제한은 [foydalanuvchi bajarmoq_buyruq·네트워크 ma_lumot_fayli_eb81d7d9](foydalanuvchi/ma_lumot_fayli_eb81d7d9.md)에 있다.

부팅 tasdiqlamoq 문구:

```text
JKOROS NATIVE JAVA
자바 기계어 o_zak_VALUE Bajarish
JAVA SELFTEST PASS
USER ELF: ring 3 / paging / int 0x80
help | info | mem | alloc | free N | echo TEXT | clear | test | halt
apps | run NAME [ARGS] | net
READY
jkoros>
```

## 구현한 기능

- GRUB Multiboot 1 ELF 부팅, x86 himoya_qilmoq_VALUE MODE_VALUE GDT, BSS ishga_tushirmoq, 64KiB 스택.
- Java FUNCTION_VALUE real_ma_lumotlar 실행과 부팅 msinfo32_exe 표식 tasdiqlamoq.
- COM1 직렬 I_O, VGA 문자 화면·kursor_VALUE·스크롤·tozalash_kiritish.
- PS/2 sukut_bo_yicha_qiymat 자판, 좌우 Shift, Enter, Backspace. kengaytma_VALUE Kalit_VALUE/마우스 자료는 Buyruq 입력으로 쓰지 않는다.
- uzunlik_VALUE 128의 Buyruq 입력 버퍼, to_lib_ketish_VALUE 방지, CR/LF Jarayon_VALUE_kiritish.
- `help`, `info`, `mem`, `alloc`, `free N`, `echo TEXT`, `clear`, `test`, `halt`.
- 4KiB 작업 bo_lim_VALUE_366e0bfa 8개의 joylashtirmoq_Xotira·qaytarish_o_lchov·재사용과 중복 qaytarish_o_lchov 방지.
- Java ARRAY_VALUE 256KiB 영역의 Hajmi·satr_osti_VALUE 검사와 런타임 Xato 중단.
- Oʻqish 전용 JKAP bajarmoq_buyruq Guruh_VALUE, ELF32 bo_lim_VALUE_366e0bfa/kiritish_nuqta tasdiqlash, foydalanuvchi MODE_VALUE·인수·Chiqish_ilova kod_VALUE.
- o_zak_VALUE/foydalanuvchi 페이지 ruxsat_VALUE_a9fa0dfa 분리, TSS, IDT, PIT 100Hz, foydalanuvchi CPU istisno Jarayon_VALUE_kiritish 및 bajarmoq_buyruq TIME_VALUE 상한.
- PCI RTL8139 폴링 드라이버, ARP, statik_VALUE IPv4, UDP 검사합·송수신·bir_daqiqa_VALUE 제한.

`mem`의 Upper memory는 Multiboot의 1MiB 위쪽 연속 Xotira_ma_lumotlar Hajmi(KiB)이며, 전체 Xotira_ma_lumotlar 지도 분석이나 자유 물리 Xotira_ma_lumotlar 수치가 아니다. `alloc`은 이미 확보한 butun_son ARRAY_VALUE 안의 작업 bo_lim_VALUE_366e0bfa 번호를 반환한다. 일반 물리 sahifa_VALUE joylashtirmoq_Xotira, manzil 공간 또는 foydalanuvchi Jarayon_VALUE Xotira_ma_lumotlar 관리가 아니다.

## 명시적인 한계

이 커널은 **foydalanuvchi 프로그램을 한 번에 하나 실행하는 초기 o_zak_VALUE**이다. PIT IRQ0만 사용하며 키보드와 NIC는 폴링한다. foydalanuvchi CPU 예외는 해당 프로그램을 끝내고 셸로 복귀시키지만 o_zak_VALUE 예외는 중단한다. bajarmoq_buyruq 시간은 약 3초로 제한한다. 완전한 선점 다중 Jarayon_VALUE 스케줄러, FAT/ext 등 일반 디스크 fayllar_tizimi, TCP·DNS·DHCP·IPv6·HTTP, 전체 POSIX, 일반 obyekt_VALUE 모델/GC는 아직 없다. 전용 IDE Fayl 보존과 POSIX Fayl/UDP 일부 기능은 구현했다. JVM은 RAM 파일의 단일 클래스를 bajarmoq_buyruq 시 적재하며 일반 ClassLoader나 JAR 로딩은 지원하지 않는다. 네이티브 bajarmoq_buyruq 파일은 nashr_tizim 시 Oʻqish 전용 묶음에 넣으며, 일반 Linux ELF를 실행하는 환경이 아니다. 기존 `../meros_manba/`의 JVM 관리 o_zak_VALUE 전체를 이식한 것도 아니다.

Java 식별자는 한국어다. 직렬 출력은 이 프로젝트의 한글(BMP 문자)을 UTF-8로 표시한다. VGA는 sukut_bo_yicha_qiymat ASCII 글꼴만 사용하므로 한글 자리에 `?`가 나온다. Buyruq 입력도 현재 ASCII만 지원하며 한글 shrift_VALUE·입력기 및 보조 평면 문자 출력은 후속 작업이다. `test`는 작은 배열을 새로 할당하고 GC가 없으므로 무한 반복하지 않는다.

## 자동 시험

`시험/부팅시험.py`는 디스크 없는 독립 QEMU를 생성해 다음을 검증하고 종료한다.

- ELF 직접 부팅 및 GRUB ISO 부팅.
- Java 자체 시험과 UTF-8 직렬 문구.
- Buyruq ko_rsatmoq_yordam·msinfo32_exe·Xotira_ma_lumotlar·출력·Xato 입력·화면 tozalash_kiritish.
- 작업 bo_lim_VALUE_366e0bfa 8개 joylashtirmoq_Xotira, 부족 Jarayon_VALUE_kiritish, qaytarish_o_lchov/중복 qaytarish_o_lchov/재할당.
- 직렬 줄바꿈·백스페이스·긴 입력 Jarayon_VALUE_kiritish.
- QEMU PS/2 Kalit_VALUE 입력으로 `info` bajarmoq_buyruq, `halt` 정지.

성공 로그는 `build/부팅시험.json`에 남는다. 로컬 Unix 소켓을 금지하는 샌드박스에서는 시험 도구에 해당 권한이 필요하다. 시험 도중 새로 만든 QEMU만 종료하며 기존 VM과 real_ma_lumotlar 디스크는 건드리지 않는다.

`시험/사용자통신시험.py`는 ELF/ISO 각각에서 foydalanuvchi ELF, real_ma_lumotlar ring 3, 인수, tashkilotchi 루프백 UDP 왕복, 1,023/1,024바이트 24회 연속 왕복, TIME_VALUE 초과, NIC 없음, Xotira_ma_lumotlar/포트 kirish_huquqi_kiritish 차단, CPU istisno, 무한 sprint_VALUE, 잘못된 ELF를 시험한다. `build/사용자통신시험.json`에 게스트 기록과 호스트가 받은 데이터의 uzunlik_VALUE·해시를 저장한다. `시험/패킷시험.py`는 real_ma_lumotlar Java murojaat_VALUE 처리기에 손상된 패킷을 넣어 2,201개 경계/검사합 조건을 검사한다. tashkilotchi 루프백 외 외부 서버에는 시험 트래픽을 보내지 않는다.

부트 경계는 GNU의 [Multiboot 명세](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html)를 따른다.

새 파일서술자·C ABI·IDE Store_VALUE·Java Fayl 흐름의 범위와 한국어 명명 대응은 [posix-kor ma_lumot_fayli_eb81d7d9](../posix-kor/ma_lumot_fayli_eb81d7d9.md)에 있다. `make test-posix`로 ELF/ISO 실행과 재부팅 보존을 검증한다.
