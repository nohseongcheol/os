# Java 네이티브 besturingssysteem

이 문서는 기존 **x86 kernel_WAARDE**을 설명한다. Raspberry Pi 4의 Eigen ARM64 begintoestand 이식은 [별도 LEESMIJ_eb81d7d9](../platforms/rpi4-native/README.md)를 참고한다. 아래 x86 gebruikersruimte ELF·네트워크·IDE Store_WAARDE 기능이 ARM64에 모두 이식된 상태는 아니다.

Java 원문을 Eigen AOT 후단으로 x86 기계어로 컴파일해 부팅하는 작은 운영체제다. 커널과 별도로 Eigen 제한형 Java compiler·JVM ELF를 gebruikersruimte 모드에 적재할 nummer 있다. Linux, engos, koros4와 extern_WAARDE OpenJDK는 게스트에 적재하지 않는다. machineopstart 진입과 hardware_poort/물리 Geheugen_regio 접근은 어셈블리이며, 문자 단말·invoer_WAARDE Proces_WAARDE_invoer·opdracht parseren_WAARDE·작업 sectie_WAARDE 관리는 `broncode/*.java`에 있다.

## 게스트 Java ontwikkeling

`javac Hello.java`, `java Hello`로 부팅된 besturingssysteem 안에서 compileren_bron·실행한다. `edit FILE.java`와 `.save`로 소스를 작성하며 `ls`, `cat`, `rm`을 제공한다. RAM 파일은 최대 8개, 각각 16KiB이다. 전용 IDE 매체를 연결하면 `sync`로 보존할 nummer 있다. 이 기능은 Eigen 제한형 구현이며 전체 OpenJDK/JDK 호환은 아니다. 사용법·steun_WAARDE 문법·bestand 적재·교차 시험은 [Java ontwikkeling omgeving](../Guides/Java_IDE.md)에 있다. `make test-java`로 검증한다.

## 빌드와 Uitvoeren_opdracht

`compiler/`가 요구하는 도구에 더해 ISO 생성에는 `grub-file`, `grub-mkrescue`, GRUB BIOS module_WAARDE, `xorriso`가 필요하다. 실행에는 QEMU 또는 VirtualBox가 필요하다. actueel_item 설치된 도구만 사용한다. `make run-store`는 새 전용 가상 Store_WAARDE 매체를 만들어 연결한다. VirtualBox 실행기는 이 프로젝트가 만든 전용 VM만 설정하고 다른 VM은 변경하지 않는다. 가상 메모리는 standaardwaarde 64MiB이며 최소 16MiB가 필요하다.

```sh
cd /home/user/jkoros/os
make                 # build/kernel.elf
make iso             # build/kernel.iso (gebruikersruimte ELF Groep_WAARDE declaraties)
make run             # ELF 직접 machineopstart, 직렬 단말
make run-gui         # GRUB ISO machineopstart, VGA 창과 PS/2 자판
make vbox            # 상위 폴더의 실행기로 전용 VirtualBox VM Uitvoeren_opdracht
make vbox-status     # 전용 VirtualBox VM Status_WAARDE bevestigen
make test            # ELF와 ISO 두 경로의 werkelijk_gegevens machineopstart/invoer_WAARDE tests
make apps            # gebruikersruimte 프로그램만 bouwen
make test-network    # gebruikersruimte Uitvoeren_opdracht/UDP/beschermen_WAARDE tests
```

`make run`은 QEMU의 직렬 표준 입출력을 쓴다. `Ctrl+A`를 누른 BACK_WAARDE `X`로 QEMU를 종료할 nummer 있다. `halt`는 게스트 CPU만 정지시키므로 QEMU Venster/프로세스는 별도로 닫는다. 폴링 방식이라 wachten_WAARDE 중에도 host CPU를 사용할 nummer 있다.

VirtualBox는 `make vbox`로 실행한다. 새 전용 VM을 Geheugen_gegevens 64MiB, BIOS, 광학 드라이브 부팅으로 자동 설정하며 디스크는 필요 없다. werkelijk_gegevens VirtualBox 5.2.42에서 machineopstart, Java Eigen tests, Shell invoer_WAARDE, `run hello vbox`의 ring 3 실행과 informatie_normaal 종료를 확인했다. actueel_item communicatie 드라이버는 QEMU의 RTL8139 전용이며 VirtualBox의 PCnet/E1000에서는 네트워크를 사용할 nummer 없어 네트워크 장치를 비활성화한다. Store_WAARDE Status_WAARDE 재개와 새 bouwen 반영 방법은 [VirtualBox Uitvoeren_opdracht LEESMIJ_eb81d7d9](../Guides/가상상자실행.md)에 있다.

## 셸에서 gebruikersruimte app_f5044b9b Uitvoeren_opdracht 및 네트워크 호출

독립 ELF32 Uitvoeren_opdracht 파일을 적재해 **ring 3**에서 실행한다. `int 0x80` 시스템 호출을 통해 단말 tekstuitvoer, argumenten query_WAARDE, UDP Openen·e_mailen·ontvangen·닫기를 제공한다. gebruikersruimte 코드를 kernel_WAARDE 함수로 직접 호출하는 구조가 아니다.

```text
jkoros> apps
jkoros> run hello first second
jkoros> net
jkoros> run netcheck
jkoros> run udp 10.0.2.2 9000 hello
```

마지막 명령의 응답을 받으려면 호스트의 별도 터미널에서 `python3 /home/user/jkoros/os/hulpmiddelen/echo_gegevens.py --port 9000`을 먼저 실행한다. 상세 API, app_f5044b9b toevoegen_invoer, ADRES 공간과 제한은 [gebruikersruimte Uitvoeren_opdracht·네트워크 LEESMIJ_eb81d7d9](gebruikersruimte/LEESMIJ_eb81d7d9.md)에 있다.

machineopstart bevestigen 문구:

```text
JKOROS NATIVE JAVA
자바 기계어 kernel_WAARDE starten
JAVA SELFTEST PASS
USER ELF: ring 3 / paging / int 0x80
help | info | mem | alloc | free N | echo TEXT | clear | test | halt
apps | run NAME [ARGS] | net
READY
jkoros>
```

## 구현한 기능

- GRUB Multiboot 1 ELF machineopstart, x86 beschermen_WAARDE MODUS_WAARDE GDT, BSS initialiseren, 64KiB operand_stack.
- Java FUNCTIE_WAARDE werkelijk_gegevens 실행과 machineopstart msinfo32_exe markering_WAARDE bevestigen.
- COM1 직렬 I_O, VGA 문자 scherm·cursor_WAARDE·스크롤·wissen_invoer.
- PS/2 standaardwaarde 자판, 좌우 Shift, Enter, Backspace. extensie_WAARDE toets_WAARDE/마우스 자료는 opdracht 입력으로 쓰지 않는다.
- tijdsduur_WAARDE 128의 opdracht invoer_WAARDE 버퍼, overloop_WAARDE 방지, CR/LF Proces_WAARDE_invoer.
- `help`, `info`, `mem`, `alloc`, `free N`, `echo TEXT`, `clear`, `test`, `halt`.
- 4KiB 작업 sectie_WAARDE 8개의 toewijzen_Opslag·Retour_HR·재사용과 중복 Retour_HR 방지.
- Java MATRIX_WAARDE 256KiB 영역의 Grootte·subscript_WAARDE 검사와 런타임 fout 중단.
- Lezen 전용 JKAP Uitvoeren_opdracht Groep_WAARDE, ELF32 sectie_WAARDE/beginpunt valideren, gebruikersruimte MODUS_WAARDE·argumenten·Einde_app CODE_WAARDE.
- kernel_WAARDE/gebruikersruimte 페이지 machtiging_WAARDE 분리, TSS, IDT, PIT 100Hz, gebruikersruimte CPU uitzondering Proces_WAARDE_invoer 및 Uitvoeren_opdracht TIJD_WAARDE 상한.
- PCI RTL8139 폴링 드라이버, ARP, statisch_WAARDE IPv4, UDP controlesom·송수신·wachten_WAARDE 제한.

`mem`의 Upper memory는 Multiboot의 1MiB 위쪽 연속 Geheugen_gegevens Grootte(KiB)이며, 전체 Geheugen_gegevens 지도 분석이나 자유 물리 Geheugen_gegevens 수치가 아니다. `alloc`은 이미 확보한 geheel_getal MATRIX_WAARDE 안의 작업 sectie_WAARDE 번호를 반환한다. 일반 물리 page_WAARDE toewijzen_Opslag, ADRES ADRES_regio 또는 gebruikersruimte Proces_WAARDE Geheugen_gegevens 관리가 아니다.

## 명시적인 한계

이 커널은 **gebruikersruimte 프로그램을 한 번에 하나 실행하는 begintoestand kernel_WAARDE**이다. PIT IRQ0만 사용하며 키보드와 NIC는 폴링한다. gebruikersruimte CPU 예외는 해당 프로그램을 끝내고 셸로 복귀시키지만 kernel_WAARDE 예외는 중단한다. Uitvoeren_opdracht 시간은 약 3초로 제한한다. 완전한 선점 다중 Proces_WAARDE 스케줄러, FAT/ext 등 일반 디스크 bestandssysteem, TCP·DNS·DHCP·IPv6·HTTP, 전체 POSIX, 일반 object_WAARDE 모델/GC는 아직 없다. 전용 IDE bestand 보존과 POSIX bestand/UDP 일부 기능은 구현했다. JVM은 RAM 파일의 단일 클래스를 Uitvoeren_opdracht 시 적재하며 일반 ClassLoader나 JAR 로딩은 지원하지 않는다. 네이티브 Uitvoeren_opdracht 파일은 bouwen 시 Lezen 전용 묶음에 넣으며, 일반 Linux ELF를 실행하는 환경이 아니다. 기존 `../verouderd_bron/`의 JVM 관리 kernel_WAARDE 전체를 이식한 것도 아니다.

Java 식별자는 한국어다. 직렬 출력은 이 프로젝트의 한글(BMP 문자)을 UTF-8로 표시한다. VGA는 standaardwaarde ASCII 글꼴만 사용하므로 한글 자리에 `?`가 나온다. opdracht 입력도 actueel_item ASCII만 지원하며 한글 lettertype_WAARDE·입력기 및 보조 평면 문자 출력은 후속 작업이다. `test`는 작은 배열을 새로 할당하고 GC가 없으므로 무한 반복하지 않는다.

## 자동 tests

`tests/부팅시험.py`는 디스크 없는 독립 QEMU를 생성해 다음을 검증하고 종료한다.

- ELF 직접 machineopstart 및 GRUB ISO machineopstart.
- Java Eigen 시험과 UTF-8 직렬 문구.
- opdracht hulp_tonen·msinfo32_exe·Geheugen_gegevens·tekstuitvoer·fout invoer_WAARDE·scherm wissen_invoer.
- 작업 sectie_WAARDE 8개 toewijzen_Opslag, 부족 Proces_WAARDE_invoer, Retour_HR/중복 Retour_HR/재할당.
- 직렬 줄바꿈·백스페이스·긴 invoer_WAARDE Proces_WAARDE_invoer.
- QEMU PS/2 toets_WAARDE 입력으로 `info` Uitvoeren_opdracht, `halt` 정지.

성공 로그는 `build/부팅시험.json`에 남는다. 로컬 Unix 소켓을 금지하는 샌드박스에서는 tests 도구에 해당 권한이 필요하다. tests 도중 새로 만든 QEMU만 종료하며 기존 VM과 werkelijk_gegevens 디스크는 건드리지 않는다.

`tests/test_gebruiker_net.py`는 ELF/ISO 각각에서 gebruikersruimte ELF, werkelijk_gegevens ring 3, argumenten, host 루프백 UDP 왕복, 1,023/1,024바이트 24회 연속 왕복, TIJD_WAARDE 초과, NIC 없음, Geheugen_gegevens/hardware_poort toegang_invoer 차단, CPU uitzondering, 무한 sprint_WAARDE, 잘못된 ELF를 시험한다. `build/test_gebruiker_net.json`에 게스트 기록과 호스트가 받은 데이터의 tijdsduur_WAARDE·해시를 저장한다. `tests/pakket_test.py`는 werkelijk_gegevens Java contractwaarde 처리기에 손상된 패킷을 넣어 2,201개 grens_WAARDE/controlesom 조건을 검사한다. host 루프백 외 extern_WAARDE 서버에는 tests 트래픽을 보내지 않는다.

부트 경계는 GNU의 [Multiboot specificatie](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html)를 따른다.

새 파일서술자·C ABI·IDE Store_WAARDE·Java bestand 흐름의 범위와 Nederlands 명명 대응은 [posix-kor LEESMIJ_eb81d7d9](../posix-kor/LEESMIJ_eb81d7d9.md)에 있다. `make test-posix`로 ELF/ISO 실행과 재부팅 보존을 검증한다.
