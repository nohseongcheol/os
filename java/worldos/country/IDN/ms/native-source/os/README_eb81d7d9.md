# Java 네이티브 sistem_pengendalian

이 문서는 기존 **x86 kernel_VALUE**을 설명한다. Raspberry Pi 4의 Asli ARM64 초기 이식은 [별도 README_eb81d7d9](../platforms/rpi4-native/README.md)를 참고한다. 아래 x86 ruang_pengguna ELF·네트워크·IDE stor_VALUE 기능이 ARM64에 모두 이식된 상태는 아니다.

Java 원문을 Asli AOT 후단으로 x86 기계어로 컴파일해 부팅하는 작은 운영체제다. 커널과 별도로 Asli 제한형 Java 컴파일러·JVM ELF를 ruang_pengguna 모드에 적재할 수 있다. Linux, engos, koros4와 외부 OpenJDK는 게스트에 적재하지 않는다. permulaan_mesin 진입과 포트/물리 Memori_rantau 접근은 어셈블리이며, 문자 단말·입력 Proses_VALUE_pemasukan·Perintah hurai_VALUE·작업 seksyen_VALUE 관리는 `SUMBER/*.java`에 있다.

## 게스트 Java 개발

`javac Hello.java`, `java Hello`로 부팅된 sistem_pengendalian 안에서 bina_sumber·실행한다. `edit FILE.java`와 `.save`로 소스를 작성하며 `ls`, `cat`, `rm`을 제공한다. RAM 파일은 최대 8개, 각각 16KiB이다. 전용 IDE 매체를 연결하면 `sync`로 보존할 수 있다. 이 기능은 Asli 제한형 구현이며 전체 OpenJDK/JDK 호환은 아니다. 사용법·Sokongan_VALUE 문법·Fail 적재·교차 시험은 [Java 개발 persekitaran](../문서/자바개발환경.md)에 있다. `make test-java`로 검증한다.

## 빌드와 laksanakan_perintah

`compiler/`가 요구하는 도구에 더해 ISO 생성에는 `grub-file`, `grub-mkrescue`, GRUB BIOS modul_VALUE, `xorriso`가 필요하다. 실행에는 QEMU 또는 VirtualBox가 필요하다. 현재 설치된 도구만 사용한다. `make run-store`는 새 전용 가상 stor_VALUE 매체를 만들어 연결한다. VirtualBox 실행기는 이 프로젝트가 만든 전용 VM만 설정하고 다른 VM은 변경하지 않는다. 가상 메모리는 nilai_lalai 64MiB이며 최소 16MiB가 필요하다.

```sh
cd /home/user/jkoros/os
make                 # build/kernel.elf
make iso             # build/kernel.iso (ruang_pengguna ELF Kumpulan_VALUE pengisytiharan)
make run             # ELF 직접 permulaan_mesin, 직렬 단말
make run-gui         # GRUB ISO permulaan_mesin, VGA 창과 PS/2 자판
make vbox            # 상위 폴더의 실행기로 전용 VirtualBox VM laksanakan_perintah
make vbox-status     # 전용 VirtualBox VM status_VALUE tentu_sahkan
make test            # ELF와 ISO 두 경로의 sebenar_data permulaan_mesin/입력 ujian
make apps            # ruang_pengguna 프로그램만 bina_sistem
make test-network    # ruang_pengguna laksanakan_perintah/UDP/lindung_VALUE ujian
```

`make run`은 QEMU의 직렬 표준 입출력을 쓴다. `Ctrl+A`를 누른 BACK_VALUE `X`로 QEMU를 종료할 수 있다. `halt`는 게스트 CPU만 정지시키므로 QEMU Tetingkap/프로세스는 별도로 닫는다. 폴링 방식이라 tunggu_VALUE 중에도 hos CPU를 사용할 수 있다.

VirtualBox는 `make vbox`로 실행한다. 새 전용 VM을 Memori_data 64MiB, BIOS, 광학 드라이브 부팅으로 자동 설정하며 디스크는 필요 없다. sebenar_data VirtualBox 5.2.42에서 permulaan_mesin, Java Asli ujian, cangkerang 입력, `run hello vbox`의 ring 3 실행과 정상 종료를 확인했다. 현재 통신 드라이버는 QEMU의 RTL8139 전용이며 VirtualBox의 PCnet/E1000에서는 네트워크를 사용할 수 없어 네트워크 장치를 비활성화한다. stor_VALUE status_VALUE 재개와 새 bina_sistem 반영 방법은 [VirtualBox laksanakan_perintah README_eb81d7d9](../문서/가상상자실행.md)에 있다.

## 셸에서 ruang_pengguna aplikasi_f5044b9b laksanakan_perintah 및 네트워크 호출

독립 ELF32 laksanakan_perintah 파일을 적재해 **ring 3**에서 실행한다. `int 0x80` 시스템 호출을 통해 단말 출력, 인수 pertanyaan_VALUE, UDP Buka·e_mel_9aee63bd·받기·닫기를 제공한다. ruang_pengguna 코드를 kernel_VALUE 함수로 직접 호출하는 구조가 아니다.

```text
jkoros> apps
jkoros> run hello first second
jkoros> net
jkoros> run netcheck
jkoros> run udp 10.0.2.2 9000 hello
```

마지막 명령의 응답을 받으려면 호스트의 별도 터미널에서 `python3 /home/user/jkoros/os/alat/자료되돌리기.py --port 9000`을 먼저 실행한다. 상세 API, aplikasi_f5044b9b Tambah_pemasukan, e_mel 공간과 제한은 [ruang_pengguna laksanakan_perintah·네트워크 README_eb81d7d9](ruang_pengguna/README_eb81d7d9.md)에 있다.

permulaan_mesin tentu_sahkan 문구:

```text
JKOROS NATIVE JAVA
자바 기계어 kernel_VALUE Jalan
JAVA SELFTEST PASS
USER ELF: ring 3 / paging / int 0x80
help | info | mem | alloc | free N | echo TEXT | clear | test | halt
apps | run NAME [ARGS] | net
READY
jkoros>
```

## 구현한 기능

- GRUB Multiboot 1 ELF permulaan_mesin, x86 lindung_VALUE mod_VALUE GDT, BSS mengasal, 64KiB 스택.
- Java fungsi_VALUE sebenar_data 실행과 permulaan_mesin msinfo32_exe penanda_VALUE tentu_sahkan.
- COM1 직렬 I_O, VGA 문자 화면·kursor_VALUE·스크롤·padam_pemasukan.
- PS/2 nilai_lalai 자판, 좌우 Shift, Enter, Backspace. sambungan_VALUE Kunci_VALUE/마우스 자료는 Perintah 입력으로 쓰지 않는다.
- kepanjangan_VALUE 128의 Perintah 입력 버퍼, limpahan_VALUE 방지, CR/LF Proses_VALUE_pemasukan.
- `help`, `info`, `mem`, `alloc`, `free N`, `echo TEXT`, `clear`, `test`, `halt`.
- 4KiB 작업 seksyen_VALUE 8개의 peruntuk_Storan·kembalikan_ukuran·재사용과 중복 kembalikan_ukuran 방지.
- Java ARRAY_VALUE 256KiB 영역의 Saiz·subskrip_VALUE 검사와 런타임 RALAT 중단.
- Baca 전용 JKAP laksanakan_perintah Kumpulan_VALUE, ELF32 seksyen_VALUE/titik_permulaan sahkan, ruang_pengguna mod_VALUE·인수·Keluar_aplikasi kod_VALUE.
- kernel_VALUE/ruang_pengguna 페이지 keizinan_VALUE 분리, TSS, IDT, PIT 100Hz, ruang_pengguna CPU pengecualian Proses_VALUE_pemasukan 및 laksanakan_perintah nilai_masa 상한.
- PCI RTL8139 폴링 드라이버, ARP, statik_VALUE IPv4, UDP hasil_tambah_semak·송수신·tunggu_VALUE 제한.

`mem`의 Upper memory는 Multiboot의 1MiB 위쪽 연속 Memori_data Saiz(KiB)이며, 전체 Memori_data 지도 분석이나 자유 물리 Memori_data 수치가 아니다. `alloc`은 이미 확보한 integer ARRAY_VALUE 안의 작업 seksyen_VALUE 번호를 반환한다. 일반 물리 halaman_VALUE peruntuk_Storan, e_mel e_mel_rantau 또는 ruang_pengguna Proses_VALUE Memori_data 관리가 아니다.

## 명시적인 한계

이 커널은 **ruang_pengguna 프로그램을 한 번에 하나 실행하는 초기 kernel_VALUE**이다. PIT IRQ0만 사용하며 키보드와 NIC는 폴링한다. ruang_pengguna CPU 예외는 해당 프로그램을 끝내고 셸로 복귀시키지만 kernel_VALUE 예외는 중단한다. laksanakan_perintah 시간은 약 3초로 제한한다. 완전한 선점 다중 Proses_VALUE 스케줄러, FAT/ext 등 일반 디스크 sistem_fail, TCP·DNS·DHCP·IPv6·HTTP, 전체 POSIX, 일반 objek_VALUE 모델/GC는 아직 없다. 전용 IDE Fail 보존과 POSIX Fail/UDP 일부 기능은 구현했다. JVM은 RAM 파일의 단일 클래스를 laksanakan_perintah 시 적재하며 일반 ClassLoader나 JAR 로딩은 지원하지 않는다. 네이티브 laksanakan_perintah 파일은 bina_sistem 시 Baca 전용 묶음에 넣으며, 일반 Linux ELF를 실행하는 환경이 아니다. 기존 `../legasi_sumber/`의 JVM 관리 kernel_VALUE 전체를 이식한 것도 아니다.

Java 식별자는 한국어다. 직렬 출력은 이 프로젝트의 한글(BMP 문자)을 UTF-8로 표시한다. VGA는 nilai_lalai ASCII 글꼴만 사용하므로 한글 자리에 `?`가 나온다. Perintah 입력도 현재 ASCII만 지원하며 한글 fon_VALUE·입력기 및 보조 평면 문자 출력은 후속 작업이다. `test`는 작은 배열을 새로 할당하고 GC가 없으므로 무한 반복하지 않는다.

## 자동 ujian

`ujian/부팅시험.py`는 디스크 없는 독립 QEMU를 생성해 다음을 검증하고 종료한다.

- ELF 직접 permulaan_mesin 및 GRUB ISO permulaan_mesin.
- Java Asli 시험과 UTF-8 직렬 문구.
- Perintah paparkan_bantuan·msinfo32_exe·Memori_data·출력·RALAT 입력·화면 padam_pemasukan.
- 작업 seksyen_VALUE 8개 peruntuk_Storan, 부족 Proses_VALUE_pemasukan, kembalikan_ukuran/중복 kembalikan_ukuran/재할당.
- 직렬 줄바꿈·백스페이스·긴 입력 Proses_VALUE_pemasukan.
- QEMU PS/2 Kunci_VALUE 입력으로 `info` laksanakan_perintah, `halt` 정지.

성공 로그는 `build/부팅시험.json`에 남는다. 로컬 Unix 소켓을 금지하는 샌드박스에서는 ujian 도구에 해당 권한이 필요하다. ujian 도중 새로 만든 QEMU만 종료하며 기존 VM과 sebenar_data 디스크는 건드리지 않는다.

`ujian/ujian_pengguna_rangkaian.py`는 ELF/ISO 각각에서 ruang_pengguna ELF, sebenar_data ring 3, 인수, hos 루프백 UDP 왕복, 1,023/1,024바이트 24회 연속 왕복, nilai_masa 초과, NIC 없음, Memori_data/포트 capai_pemasukan 차단, CPU pengecualian, 무한 lelaran_VALUE, 잘못된 ELF를 시험한다. `build/ujian_pengguna_rangkaian.json`에 게스트 기록과 호스트가 받은 데이터의 kepanjangan_VALUE·해시를 저장한다. `ujian/paket_ujian.py`는 sebenar_data Java kes_VALUE 처리기에 손상된 패킷을 넣어 2,201개 경계/hasil_tambah_semak 조건을 검사한다. hos 루프백 외 외부 서버에는 ujian 트래픽을 보내지 않는다.

부트 경계는 GNU의 [Multiboot 명세](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html)를 따른다.

새 파일서술자·C ABI·IDE stor_VALUE·Java Fail 흐름의 범위와 Melayu 명명 대응은 [posix-kor README_eb81d7d9](../posix-kor/README_eb81d7d9.md)에 있다. `make test-posix`로 ELF/ISO 실행과 재부팅 보존을 검증한다.
