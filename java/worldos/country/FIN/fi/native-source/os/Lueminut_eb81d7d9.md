# Java 네이티브 käyttöjärjestelmä

이 문서는 기존 **x86 ydin_ARVO**을 설명한다. Raspberry Pi 4의 oma ARM64 alkutila 이식은 [별도 Lueminut_eb81d7d9](../platforms/rpi4-native/README.md)를 참고한다. 아래 x86 käyttäjätila ELF·네트워크·IDE Store_ARVO 기능이 ARM64에 모두 이식된 상태는 아니다.

Java 원문을 oma AOT 후단으로 x86 기계어로 컴파일해 부팅하는 작은 운영체제다. 커널과 별도로 oma 제한형 Java kääntäjä·JVM ELF를 käyttäjätila 모드에 적재할 numero 있다. Linux, engos, koros4와 ulkoinen_ARVO OpenJDK는 게스트에 적재하지 않는다. koneen_käynnistys 진입과 laitteisto_portti/물리 Muisti_alue 접근은 어셈블리이며, 문자 단말·syöte_ARVO prosessi_ARVO_merkintä·komento jäsentää_ARVO·작업 osa_ARVO 관리는 `lähdetiedosto/*.java`에 있다.

## 게스트 Java kehitystuote

`javac Hello.java`, `java Hello`로 부팅된 käyttöjärjestelmä 안에서 kääntää_lähde·실행한다. `edit FILE.java`와 `.save`로 소스를 작성하며 `ls`, `cat`, `rm`을 제공한다. RAM 파일은 최대 8개, 각각 16KiB이다. 전용 IDE 매체를 연결하면 `sync`로 보존할 numero 있다. 이 기능은 oma 제한형 구현이며 전체 OpenJDK/JDK 호환은 아니다. 사용법·Tuki_ARVO 문법·tiedoston_nimi 적재·교차 시험은 [Java kehitystuote ympäristö](../문서/Java_kehitysympäristö.md)에 있다. `make test-java`로 검증한다.

## 빌드와 Suorita_komento

`compiler/`가 요구하는 도구에 더해 ISO 생성에는 `grub-file`, `grub-mkrescue`, GRUB BIOS moduuli_ARVO, `xorriso`가 필요하다. 실행에는 QEMU 또는 VirtualBox가 필요하다. nykyinen_kohde 설치된 도구만 사용한다. `make run-store`는 새 전용 가상 Store_ARVO 매체를 만들어 연결한다. VirtualBox 실행기는 이 프로젝트가 만든 전용 VM만 설정하고 다른 VM은 변경하지 않는다. 가상 메모리는 oletusarvo 64MiB이며 최소 16MiB가 필요하다.

```sh
cd /home/user/jkoros/os
make                 # build/kernel.elf
make iso             # build/kernel.iso (käyttäjätila ELF Ryhmä_ARVO esittelyt)
make run             # ELF 직접 koneen_käynnistys, 직렬 단말
make run-gui         # GRUB ISO koneen_käynnistys, VGA 창과 PS/2 자판
make vbox            # 상위 폴더의 실행기로 전용 VirtualBox VM Suorita_komento
make vbox-status     # 전용 VirtualBox VM Tila_ARVO tarkistaa
make test            # ELF와 ISO 두 경로의 todellinen_data koneen_käynnistys/syöte_ARVO testit
make apps            # käyttäjätila 프로그램만 kääntää_Järjestelmä
make test-network    # käyttäjätila Suorita_komento/UDP/suojata_ARVO testit
```

`make run`은 QEMU의 직렬 표준 입출력을 쓴다. `Ctrl+A`를 누른 BACK_ARVO `X`로 QEMU를 종료할 numero 있다. `halt`는 게스트 CPU만 정지시키므로 QEMU Ikkuna/프로세스는 별도로 닫는다. 폴링 방식이라 odottaa_ARVO 중에도 isäntä CPU를 사용할 numero 있다.

VirtualBox는 `make vbox`로 실행한다. 새 전용 VM을 Muisti_data 64MiB, BIOS, 광학 드라이브 부팅으로 자동 설정하며 디스크는 필요 없다. todellinen_data VirtualBox 5.2.42에서 koneen_käynnistys, Java oma testit, liittymä syöte_ARVO, `run hello vbox`의 ring 3 실행과 tietojärjestelmät_normaali 종료를 확인했다. nykyinen_kohde 통신 드라이버는 QEMU의 RTL8139 전용이며 VirtualBox의 PCnet/E1000에서는 네트워크를 사용할 numero 없어 네트워크 장치를 비활성화한다. Store_ARVO Tila_ARVO 재개와 새 kääntää_Järjestelmä 반영 방법은 [VirtualBox Suorita_komento Lueminut_eb81d7d9](../문서/가상상자실행.md)에 있다.

## 셸에서 käyttäjätila ohjelma_f5044b9b Suorita_komento 및 네트워크 호출

독립 ELF32 Suorita_komento 파일을 적재해 **ring 3**에서 실행한다. `int 0x80` 시스템 호출을 통해 단말 tulostuspaikka, argumentit kysely_ARVO, UDP Avaa·lähettää·saada·닫기를 제공한다. käyttäjätila 코드를 ydin_ARVO 함수로 직접 호출하는 구조가 아니다.

```text
jkoros> apps
jkoros> run hello first second
jkoros> net
jkoros> run netcheck
jkoros> run udp 10.0.2.2 9000 hello
```

마지막 명령의 응답을 받으려면 호스트의 별도 터미널에서 `python3 /home/user/jkoros/os/työkalut/päivitys_data.py --port 9000`을 먼저 실행한다. 상세 API, ohjelma_f5044b9b liitä_merkintä, OSOITE 공간과 제한은 [käyttäjätila Suorita_komento·네트워크 Lueminut_eb81d7d9](käyttäjätila/Lueminut_eb81d7d9.md)에 있다.

koneen_käynnistys tarkistaa 문구:

```text
JKOROS NATIVE JAVA
자바 기계어 ydin_ARVO Suorita_2
JAVA SELFTEST PASS
USER ELF: ring 3 / paging / int 0x80
help | info | mem | alloc | free N | echo TEXT | clear | test | halt
apps | run NAME [ARGS] | net
READY
jkoros>
```

## 구현한 기능

- GRUB Multiboot 1 ELF koneen_käynnistys, x86 suojata_ARVO tila_ARVO GDT, BSS alustaa, 64KiB operandi_Pino.
- Java funktio_ARVO todellinen_data 실행과 koneen_käynnistys msinfo32_exe merkintä_ARVO tarkistaa.
- COM1 직렬 I_O, VGA 문자 화면·kohdistin_ARVO·스크롤·poistaa_merkintä_c8dbc399.
- PS/2 oletusarvo 자판, 좌우 Shift, Enter, Backspace. tarkenne_ARVO Avain_ARVO/마우스 자료는 komento 입력으로 쓰지 않는다.
- kesto_ARVO 128의 komento syöte_ARVO 버퍼, ylivuoto_ARVO 방지, CR/LF prosessi_ARVO_merkintä.
- `help`, `info`, `mem`, `alloc`, `free N`, `echo TEXT`, `clear`, `test`, `halt`.
- 4KiB 작업 osa_ARVO 8개의 jakaa_Tallennus·palauttaa_KR·재사용과 중복 palauttaa_KR 방지.
- Java MATRIISI_ARVO 256KiB 영역의 Koko·alaindeksi_ARVO 검사와 런타임 VIRHE 중단.
- Luku 전용 JKAP Suorita_komento Ryhmä_ARVO, ELF32 osa_ARVO/aloituskohta vahvista, käyttäjätila tila_ARVO·argumentit·Lopeta_ohjelma KOODI_ARVO.
- ydin_ARVO/käyttäjätila 페이지 lupa_ARVO 분리, TSS, IDT, PIT 100Hz, käyttäjätila CPU poikkeus prosessi_ARVO_merkintä 및 Suorita_komento AIKA_ARVO 상한.
- PCI RTL8139 폴링 드라이버, ARP, staattinen_ARVO IPv4, UDP tarkistussumma·송수신·odottaa_ARVO 제한.

`mem`의 Upper memory는 Multiboot의 1MiB 위쪽 연속 Muisti_data Koko(KiB)이며, 전체 Muisti_data 지도 분석이나 자유 물리 Muisti_data 수치가 아니다. `alloc`은 이미 확보한 kokonaisluku MATRIISI_ARVO 안의 작업 osa_ARVO 번호를 반환한다. 일반 물리 page_ARVO jakaa_Tallennus, OSOITE OSOITE_alue 또는 käyttäjätila prosessi_ARVO Muisti_data 관리가 아니다.

## 명시적인 한계

이 커널은 **käyttäjätila 프로그램을 한 번에 하나 실행하는 alkutila ydin_ARVO**이다. PIT IRQ0만 사용하며 키보드와 NIC는 폴링한다. käyttäjätila CPU 예외는 해당 프로그램을 끝내고 셸로 복귀시키지만 ydin_ARVO 예외는 중단한다. Suorita_komento 시간은 약 3초로 제한한다. 완전한 선점 다중 prosessi_ARVO 스케줄러, FAT/ext 등 일반 디스크 tiedostojärjestelmä, TCP·DNS·DHCP·IPv6·HTTP, 전체 POSIX, 일반 objekti_ARVO 모델/GC는 아직 없다. 전용 IDE tiedoston_nimi 보존과 POSIX tiedoston_nimi/UDP 일부 기능은 구현했다. JVM은 RAM 파일의 단일 클래스를 Suorita_komento 시 적재하며 일반 ClassLoader나 JAR 로딩은 지원하지 않는다. 네이티브 Suorita_komento 파일은 kääntää_Järjestelmä 시 Luku 전용 묶음에 넣으며, 일반 Linux ELF를 실행하는 환경이 아니다. 기존 `../vanha_lähde/`의 JVM 관리 ydin_ARVO 전체를 이식한 것도 아니다.

Java 식별자는 한국어다. 직렬 출력은 이 프로젝트의 한글(BMP 문자)을 UTF-8로 표시한다. VGA는 oletusarvo ASCII 글꼴만 사용하므로 한글 자리에 `?`가 나온다. komento 입력도 nykyinen_kohde ASCII만 지원하며 한글 fontti_ARVO·입력기 및 보조 평면 문자 출력은 후속 작업이다. `test`는 작은 배열을 새로 할당하고 GC가 없으므로 무한 반복하지 않는다.

## 자동 testit

`testit/부팅시험.py`는 디스크 없는 독립 QEMU를 생성해 다음을 검증하고 종료한다.

- ELF 직접 koneen_käynnistys 및 GRUB ISO koneen_käynnistys.
- Java oma 시험과 UTF-8 직렬 문구.
- komento näytä_ohje·msinfo32_exe·Muisti_data·tulostuspaikka·VIRHE syöte_ARVO·화면 poistaa_merkintä_c8dbc399.
- 작업 osa_ARVO 8개 jakaa_Tallennus, 부족 prosessi_ARVO_merkintä, palauttaa_KR/중복 palauttaa_KR/재할당.
- 직렬 줄바꿈·백스페이스·긴 syöte_ARVO prosessi_ARVO_merkintä.
- QEMU PS/2 Avain_ARVO 입력으로 `info` Suorita_komento, `halt` 정지.

성공 로그는 `build/부팅시험.json`에 남는다. 로컬 Unix 소켓을 금지하는 샌드박스에서는 testit 도구에 해당 권한이 필요하다. testit 도중 새로 만든 QEMU만 종료하며 기존 VM과 todellinen_data 디스크는 건드리지 않는다.

`testit/testi_käyttäjä_verkko.py`는 ELF/ISO 각각에서 käyttäjätila ELF, todellinen_data ring 3, argumentit, isäntä 루프백 UDP 왕복, 1,023/1,024바이트 24회 연속 왕복, AIKA_ARVO 초과, NIC 없음, Muisti_data/laitteisto_portti pääsy_merkintä_68aed533 차단, CPU poikkeus, 무한 sprintti_ARVO, 잘못된 ELF를 시험한다. `build/testi_käyttäjä_verkko.json`에 게스트 기록과 호스트가 받은 데이터의 kesto_ARVO·해시를 저장한다. `testit/paketti_testi.py`는 todellinen_data Java sopimuksen_arvo 처리기에 손상된 패킷을 넣어 2,201개 rajattu_alue_ARVO/tarkistussumma 조건을 검사한다. isäntä 루프백 외 ulkoinen_ARVO 서버에는 testit 트래픽을 보내지 않는다.

부트 경계는 GNU의 [Multiboot määritys](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html)를 따른다.

새 파일서술자·C ABI·IDE Store_ARVO·Java tiedoston_nimi 흐름의 범위와 suomi 명명 대응은 [posix-kor Lueminut_eb81d7d9](../posix-kor/Lueminut_eb81d7d9.md)에 있다. `make test-posix`로 ELF/ISO 실행과 재부팅 보존을 검증한다.
