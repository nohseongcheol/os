# Raspberry Pi 4 Asli Java kernel_VALUE — ruang_pengguna laksanakan_perintah 기반

현재 Asli 코드의 COSL 상업 syarat, 제3자 고지 및 LGPL 재연결 자료는 [COSL 배포 README_eb81d7d9](COSL배포안내.md)를 참고한다. tukar_mod 전 GPL 구성의 판단은 [이전 라이선스 검토](lesenkan_ulasan.md)에 기록했다.

Melayu 통신·pengecualian 사용법은 [Melayu Java API](한국어자바/README_eb81d7d9.md), fungsi_VALUE·pemboleh_ubah_VALUE·Fail 이름의 변경과 어원 근거는 [명명 README_eb81d7d9](명명/README_eb81d7d9.md)를 참고한다.

Linux 없이 부팅하는 Asli AArch64 커널이다. Java AOT kernel_VALUE 위에 **baris_perintah cangkerang, 게스트 Java 컴파일러·JVM, MicroPython, EL0 C++ laksanakan_perintah, Fail·UDP 루프백 시스템 호출, 여러 한글 GUI Terminal·vi Editor·Swing 부분집합**을 제공한다. 커널의 Fail data/정책·루프백 pindah_VALUE·cangkerang 상태는 Java, 화면 합성·pel ubah_VALUE·penuding·클리핑도 Java로 구현하며, CPU/MMU/peranti_VALUE 경계와 Terminal·aksara_VALUE 그리기 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 Asli 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 laksanakan_perintah, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](파일전송과번역.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, 실물 Pi4의 berwayar_VALUE 송수신은 아직 미검증이다.** laksanakan_perintah·hubungan_e05f319b·kata_laluan_VALUE 확인은 [외부 hubungan_e05f319b README_eb81d7d9](외부접속안내.md)에 정리했다.

셸은 EL1 kernel_VALUE, `java` 등 ruang_pengguna laksanakan_perintah 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 제한, QEMU 네트워크 laksanakan_perintah·hubungan_e05f319b 방법 및 sebenar_data 검증은
[laksanakan_perintah 계층과 외부 통신 점검](실행계층과외부통신점검.md)을 참고한다.

ELF는 확장자가 아닌 sebenar_data laksanakan_perintah 형식으로 검사한다. `./인사`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 statik_VALUE ELF는 `run --linux nama_fail_SMS`으로 실행한다. [ELF·Linux ABI Sokongan_VALUE 범위와 동일 바이너리 ujian](실행파일규약.md).

GUI와 네트워크는 `python3 alat/laksanakan_perintah.py --desktop --network`로 함께 사용한다. Java·C·Python의 Melayu 예제 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 permulaan_mesin 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 수 있다. Remmina에서 **F9/Shift+Space/한·영 Kunci_VALUE**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·sebenar_data TCP/UDP·Fail bait_VALUE·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` 후 `java ContohTetingkap`로 Melayu Swing 예제를 실행한다. Terminal 모서리에 마우스를 대고 **왼쪽 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 현재 lajur_VALUE·ROW_VALUE 수를 보여 준다.

## 현재 Sokongan_VALUE klip

| 기능 | pelaksanaan·시험한 klip | 아직 미지원 |
|---|---|---|
| permulaan_mesin | Pi4 AArch64 EL1, UART, SD용 bina_imej, QEMU raspi4b permulaan_mesin | sebenar_data Pi4 보드에서의 펌웨어 permulaan_mesin ujian |
| Java kernel_VALUE | statik_VALUE Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java objek_VALUE/pengecualian/GC/JVM/표준 pustaka |
| Java 개발 alat | 게스트 Asli `javac`/`java`, JVM 0.4/JAR: 다중 Kelas_VALUE·objek_VALUE·상속·pengecualian·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, Melayu pustaka. 게스트 컴파일러는 statik_VALUE Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | sebenar_data MicroPython 1.24.1 EL0 이식, sumber_pepohon bina_sumber/laksanakan_perintah, Kelas_VALUE·pengecualian·GC·큰 integer·Unicode·Fail·UDP/화면 Sambung | CPython, pip, C sambungan_VALUE, 부동소수점, 일반 OS/스레드/소켓 modul_VALUE, interaktif REPL |
| cangkerang | UTF-8 edit_VALUE·LOG_baris·Selesai_VALUE, 디렉터리·Fail Perintah, pemboleh_ubah_VALUE·syarat·skrip_VALUE, 16 KiB 순차 파이프·리다이렉션, ELF laksanakan_perintah | 전체 POSIX sh/Bash, 작업 kawalan_VALUE·동시 프로세스·PTY |
| C/AOT bina_sumber | 게스트 TinyCC 및 statik_VALUE Java 부분집합 `jaot` → Asli ARM64 ELF | 전체 libc·모든 Java Kelas_VALUE AOT |
| C++ | 독립 ELF64를 EL0에서 laksanakan_perintah; statik_VALUE 생성자, RAII 소멸자, FP/SIMD, Melayu Fail/루프백 호출 | libc/libstdc++, STL, C++ pengecualian·RTTI·동적 Sambung |
| ruang_pengguna lindung_VALUE | 4 KiB 페이지, kod_VALUE RX/data RW·NX, kernel_VALUE·MMIO 차단, guard page, 잘못된 penuding 검사 | 다중 ruang_pengguna keizinan_VALUE, 일반 프로세스/스레드 스케줄러 |
| laksanakan_perintah nilai_masa 제한 | GIC-400 타이머로 무한 lelaran_VALUE Keluar_aplikasi; interaktif 입력 대기는 기한 segar_semula, 터미널별 EL0 aplikasi_f5044b9b 중단·재개 | 일반적인 선점형 다중작업. 긴 kernel_VALUE 호출 도중에는 종료가 지연될 수 있음 |
| Fail | Java RAM Fail 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, rakan_VALUE/절대 LALUAN 63바이트, 서술자 16개 | keizinan_VALUE, 디스크/SD 영속 stor_VALUE |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP pelaksanaan, 게스트 FTP·SSH·VNC | GENET 실물 sahkan, Wi-Fi, DNS, 일반 TLS 소켓, RDP |
| GUI | 최대 네 Terminal Tetingkap, pilihan_VALUE·alih_VALUE·X Tutup, 한글 fon_VALUE, Swing 부분집합; 게스트 VNC 화면·입력·두벌식 | 실물 USB 입력, 전체 AWT/Swing·Java2D·Tetingkap 관리 정책 |
| 작업 urutan_VALUE | kernel_VALUE 작업 2개와 주 작업; JVM 내부 urutan_VALUE 최대 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, 한글·일본어·아랍어·이모지, UTF-8 nama_fail_SMS/전문 | GUI의 일반 다국어 조판 |

laksanakan_perintah 버튼 화면은 5×7 영문 글꼴을 쓰며, Terminal 창은 Noto CJK/DejaVu에서 생성한 한글·Unicode 비트맵 글꼴을 쓴다. UART와 sebenar_data 프레임버퍼의 한글 표시를 시험한다. 루프백은 동일 kernel_VALUE 내부의 전문 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 보조 UART SLIP 경로를 사용한다. `python3 alat/laksanakan_perintah.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·laksanakan_perintah 제한과 Melayu 사용법은 [Asli JVM과 Melayu pustaka](자바실행환경.md)에 정리했다. Kelas_VALUE Fail/JAR 배포는 [한국어자바](한국어자바) 소스에서 재현한다. 기존 Linux판 `Melayu.자바`와 별도인 `Melayu.Asli` 패키지다.

**vi·여러 Tetingkap·Swing·한글 Java/Python/C/C++·posix-kor 예제는 [한글 개발 매뉴얼](개발안내.md)에 정리했다.**

GUI Terminal laksanakan_perintah·단축키·cangkerang Perintah·제한은 [셸과 Terminal 사용법](cangkerang_AND_Terminal.md)에 정리했다.

## 현재 컴퓨터에서 laksanakan_perintah

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

Keluar_aplikasi: **Ctrl+A Seterusnya_item X**. 게스트 C/AOT alat 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc 산술 보조 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. hos 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 이식·링크한 것은 아니다. 컴파일러 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/LALUAN/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` Sokongan_VALUE 여부를 확인한 후 실행한다.

명령은 **Enter를 눌러 laksanakan_perintah**한다. 기존 한 aksara_VALUE 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "한글 인수 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| Perintah | Aksi |
|---|---|
| `help` / `info` | Perintah·sebenar_data pelaksanaan status_VALUE |
| `ls` / `cat FILE` / `rm FILE` | RAM Fail pemasukan_Senarai·Kandungan_VALUE·삭제 |
| `vi FILE` | ruang_pengguna rantau_VALUE vi 부분집합, 한글 edit_VALUE·stor_VALUE·검색·되돌리기 |
| `edit FILE` | Fail 전체를 새로 입력; 단독 `.` 줄로 stor_VALUE, Ctrl-C로 Batal_operasi |
| `javac FILE.java` / `java CLASS [ARGS]` | Asli 제한형 Java bina_sumber·laksanakan_perintah |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython bina_sumber·laksanakan_perintah |
| `load FILE` / `hex FILE` | 16진수 바이너리 입력/출력; 입력은 단독 `.` 줄로 stor_VALUE |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 Asli ABI ELF / 내장 C++ 예제 |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 작업 / EL0 lindung_VALUE ujian |
| `gui` / `terminal` | laksanakan_perintah 화면 / 한글 GUI Terminal; F12로 Terminal Buka·Tutup |
| `samples` | 삭제한 nilai_lalai 예제 pulih_status; 기존 파일은 보존 |

예를 들어 `edit 인사.java`를 입력한 Seterusnya_item 아래 소스를 입력한다.

```java
public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }
```

그다음 단독 `.` 줄로 저장하고 `javac 인사.java`, `java 인사`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. Batal_operasi·잘못된 16진수·kapasiti_VALUE 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, laksanakan_perintah 인수는 최대 8개·각각 UTF-8 255바이트다. 일반 Perintah 인수는 최대 32개다. Petikan·백슬래시·cangkerang pemboleh_ubah_VALUE·파이프·리다이렉션 범위는 [cangkerang 설명](cangkerang_AND_Terminal.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, e_mel **127.0.0.1:5902**로 연결한다. 키보드·한글 Unicode 입력·명시적 tampal_VALUE·laksanakan_perintah 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 alat/laksanakan_perintah.py --desktop --network
# 다른 포트: python3 alat/laksanakan_perintah.py --desktop --port 5903
```

종료는 실행한 hos 터미널에서 Ctrl+C다. 기존 `python3 alat/laksanakan_perintah.py --vnc 127.0.0.1:2`는 화면 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. sebenar_data Pi4 USB 입력기는 아직 없으며, VNC Sambung 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 sebenar_data C++/UDP ELF laksanakan_perintah, `Hello.java` bina_sumber 후 JVM laksanakan_perintah, `hello.py` laksanakan_perintah, GUI Terminal 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 interaktif 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 Memori_data·CPU 문맥을 보관한다. cangkerang·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## sebenar_data 산출물과 Pi4 SD bina_imej

```sh
make image   # kernel_VALUE, SD bina_imej, permulaan_mesin ZIP, 사용자용 SDK
make sdk     # SDK만 다시 jana
```

| LALUAN | 용도 |
|---|---|
| `build/kernel8.img` | Asli kernel_VALUE 기계어, 적재 e_mel 0x80000 |
| `build/kernel.elf`, `kernel.map` | kernel_VALUE simbol_VALUE·susun_atur_pautan |
| `build/user/demo.elf` | ruang_pengguna mod_VALUE C++ Fail/timbunan_VALUE/실수/그래픽 예제 |
| `build/user/network.elf` | ruang_pengguna mod_VALUE C++ UDP 루프백 예제 |
| `build/user/java-tools.elf` | Asli Java 부분집합 컴파일러/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | hos javac용 Melayu API Kelas_VALUE; 같은 클래스가 Asli JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | Melayu API Java SUMBER |
| `build/user/vi.elf` | Asli UTF-8 vi Perintah 부분집합 Editor |
| `build/user/python.elf` | Asli ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 lindung_VALUE ujian 전용 |
| `build/libposix-kor-arm64.a` | **kernel_VALUE 내부**에서 Java Fail 구현을 직접 부르는 기존 Sambung |
| `build/libposix-kor-user.a` | **EL0 ruang_pengguna aplikasi_f5044b9b**에서 SVC로 Fail/루프백을 호출하는 새 Sambung |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD bina_imej |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 permulaan_mesin 파티션에 복사할 Fail Kumpulan_VALUE |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·Jalan kod_VALUE·pustaka·링커 skrip_VALUE·예제 |
| `dist/manifest.json`, `build/build.json` | SHA256과 sebenar_data Sokongan_VALUE status_VALUE |

이미지는 확인된 공식 Pi permulaan_mesin 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·Terminal fon_VALUE 라이선스와 fon_VALUE 출처 해시도 동봉한다. Fail jana 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 bina_imej LOG_baris 도구로 `.img`를 기록하거나 FAT32 permulaan_mesin 파티션 최상위에 ZIP 내용을 푼다. bina_imej 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 nilai_lalai EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**실물 Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD Fail 구성·kernel_VALUE 체크섬 검사와 물리 Papan permulaan_mesin 검증은 별개다. MMU 사용 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 permulaan_mesin 조건을 전제로 한다. 세 보조 코어는 대기시키며 한 코어만 사용한다.

## C++와 Melayu API 사용

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/ContohFail.cpp -o demo.elf
python3 compile.py examples/통신예제.cpp -o network.elf
```

진입점은 `extern "C" int Mula_pengguna_aplikasi(int)`이다. ruang_pengguna C++는 FP/SIMD를 사용할 수 있다. kernel_VALUE C/Java AOT는 일반 레지스터만 사용하므로 pengecualian Proses_VALUE_pemasukan 중 ruang_pengguna FP 상태를 건드리지 않는다. ruang_pengguna titik_permulaan_VALUE 시 FP 상태를 초기화하고 kernel_VALUE 복귀에 필요한 상태를 보존한다.

```cpp
#include "파일규약.h"
extern "C" int Mula_pengguna_aplikasi(int) {
    int Fail = buka_fail("인사.txt", baca_tulis | 없으면만들기 | potong_TOC, 0600);
    if (Fail < 0) return 1;
    const char Kandungan_VALUE[] = "안녕하세요";
    int ukuran = tulis_fail_data(Fail, Kandungan_VALUE, sizeof(Kandungan_VALUE) - 1);
    Tutup_fail(Fail);
    return ukuran == sizeof(Kandungan_VALUE) - 1 ? 0 : 2;
}
```

[Fail 예제](ruang_pengguna/ContohFail.cpp)와 [통신 예제](ruang_pengguna/통신예제.cpp)가 sebenar_data permulaan_mesin ujian 대상이다. `파일규약.h`의 이름은 커널용/사용자용 모두 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 Fail Proses_VALUE_pemasukan 및 루프백 전달은 Java 커널에서 실행한다. `통신규약.h`의 소켓 함수는 현재 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 kernel_VALUE 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 Seterusnya_item 도구를 사용하면 **새 QEMU를 부팅해 업로드한 sebenar_data 바이트를 재확인한 BACK_VALUE 게스트에서 laksanakan_perintah**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 alat/laksanakan_fail.py build/jkoros-native-sdk/demo.elf
python3 alat/laksanakan_fail.py 예제/Hello.java "한글 인수"
python3 alat/laksanakan_fail.py 예제/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 kernel_VALUE 묶음에 포함되어 이 Fail 한도를 적용받지 않는다. **C++ 컴파일러는 hos SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 pustaka, PT_TLS, PT_INTERP, PT_DYNAMIC, laksanakan_perintah·Tulis 겸용 세그먼트는 로더가 거부한다. 구체적인 호출 INDEX·e_mel klip·오류는 [ruang_pengguna ABI](사용자호출규약.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `lakukan_storan_fail`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 keizinan_VALUE·dup/fcntl은 없다. 디렉터리와 rakan_VALUE/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 최대 512바이트, 소켓은 8개, 수신 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. ruang_pengguna Keluar_aplikasi 시 열린 Fail 서술자와 소켓을 회수한다.

## sahkan ukuran

`make test-jvm`은 9개 프로그램을 OpenJDK와 sebenar_data Asli 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `alat/부팅시험.py`는 Java segi_empat_tepat API의 sebenar_data 화면 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 sebenar_data VNC 입력·한글 Terminal 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT operasi_VALUE ukuran 비교, 런타임 RALAT 중단, 미지원 Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java kernel_VALUE 계산·UTF-8·C++ 직접 호출·협력식 작업 및 프레임버퍼.
- 손상/잘못된 ABI/e_mel 초과/겹친 페이지/W+X 등 ELF tolak_VALUE 사례 22개.
- EL0 C++ 생성자·RAII·실수 operasi_VALUE·Fail·timbunan_VALUE 및 잘못된 시스템 호출 penuding.
- kernel_VALUE/kod_VALUE/MMIO Tulis·capai_pemasukan, NX 스택·NULL laksanakan_perintah, guard page, 특권 Perintah 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 후 정상 aplikasi_f5044b9b 재실행.
- lelaran_VALUE laksanakan_perintah 시 Fail/소켓 누수 방지, UDP 왕복·보낸 e_mel·잘린 수신·큐 포화·빈 전문·미지원 통신 RALAT.
- cangkerang edit_VALUE·Batal_operasi·16진수 업로드/다운로드·ruang_pengguna ELF 실행과 잘못된 ELF tolak_VALUE.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 laksanakan_perintah, 한글 Kelas_VALUE·pemboleh_ubah_VALUE·nama_fail_SMS.
- 여러 Tetingkap·vi stor_VALUE·edit_VALUE·kembalikan_penghubung·ruang_pengguna status_VALUE 중단/재개, Swing 한글 입력·이벤트·X Tutup, 연결형 루프백, C/C++ 한글 SDK 예제.
- MicroPython Unicode·큰 integer·Kelas_VALUE·GC lelaran_VALUE·Fail import·pengecualian·Fail·UDP 왕복·nilai_masa 초과 후 복귀.
- GUI pilihan_VALUE alih_VALUE, C++/UDP/Java/MicroPython 버튼 laksanakan_perintah, 콘솔 복귀 및 sebenar_data 프레임버퍼 픽셀/fon_VALUE.
- 디렉터리·pemboleh_ubah_VALUE·syarat·Fail Perintah·skrip_VALUE·순차 파이프·리다이렉션·kapasiti_VALUE 초과 pulih_status, Python stdin/EOF와 Java/Python stdout.
- Perintah LOG_baris·긴 한글 입력 edit_VALUE·Selesai_VALUE·Terminal 스크롤, 그래픽 aplikasi_f5044b9b Keluar_aplikasi 후 Tetingkap 복원, sebenar_data VNC Unicode Kunci_VALUE·tampal_VALUE·마우스.

[kernel_VALUE ujian LOG_baris](build/verification/implementation-test.log), [cangkerang ujian](build/verification/shell/report.json), [VNC ujian](build/verification/desktop/report.json), [mesin 판독 ukuran](build/verification/report.json), [직렬 LOG_VALUE](build/verification/serial.log), [GUI 화면](build/verification/gui-python.png)을 확인할 수 있다. VNC RFB 3.8 Sambung 및 640×480 화면 정보도 검사한다. [SDK 재컴파일 ukuran](build/verification/sdk.json)는 두 예제의 titik_permulaan·적재 세그먼트·ABI note가 permulaan_mesin 시험한 ELF와 일치함을 확인한다. simbol_VALUE 등 비적재 메타데이터를 포함한 Fail 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 klip

Asli `javac`는 버전 49 `.class`를 생성하며 JVM은 Sokongan_VALUE 명령으로 구성된 버전 45–52 클래스를 실행한다. statik_VALUE fungsi_VALUE·재귀·int/boolean/char/String·syarat/lelaran_VALUE·rentetan_VALUE 결합과 일부 Fail 스트림을 지원한다. UTF-8 문자열과 문자 리터럴, ASCII 및 현대 한글 음절/조합 자모 식별자를 처리한다. Unicode 식별자 전체 Carian_jadual·Unicode sumber_pepohon 이스케이프는 구현하지 않았다. 게스트 sumber_pepohon 컴파일러는 일반 objek_VALUE·pengecualian·Thread 구문을 아직 컴파일하지 못한다. hos `javac --release 8`로 만든 Sokongan_VALUE 부분집합 클래스는 Asli JVM 0.4의 objek_VALUE·pengecualian·Thread·UDP와 Melayu API를 사용할 수 있다. Swing은 문서화한 Asli API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [Asli JVM 설명](자바실행환경.md)이 기준이다. 상세 Bahasa 범위는 [공유 Java alat 설명](../../문서/자바개발환경.md)을 참고하되, 그 문서의 x86 cangkerang/stor_VALUE/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 sumber_pepohon**를 Asli AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 fungsi_VALUE·Kelas_VALUE·pengecualian·리스트/kamus·Unicode·GC·가변 kepersisan_VALUE 정수를 제공한다. 현재 구성은 integer 빌드로 `float`, `complex`, `math`가 없으며 CPython 전체 표준 pustaka, pip, subprocess, threading, 일반 socket과 nilai_lalai `open()` Fail 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 objek_VALUE·모듈은 Keluar_aplikasi 시 회수되고 RAM 파일만 Seterusnya_item 실행에 남는다.

`import jkoros`로 Seterusnya_item 시스템 연결을 쓴다. 모두 SVC를 통해 Asli Java 커널에 접근한다.

| fungsi_VALUE | Aksi |
|---|---|
| `stdin(limit)` | 현재 표준 입력에서 최대 limit바이트(0…16384)를 bytes로 읽음; EOF는 빈 bytes, UART data 없음은 OSError(11) |
| `read(name)` | rakan_VALUE/절대 RAM 경로의 Fail 전체를 bytes로 읽음 |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 stor_VALUE, 쓴 bait_VALUE 수 kembalikan_ukuran |
| `remove(name)` | RAM Fail 삭제 |
| `rect(x, y, w, h, color)` | 선택한 sebenar_data 화면 Saiz 안의 segi_empat_tepat lukisan_VALUE; 기존 보드의 RGB32 VALUE |
| `ticks_ms()` | permulaan_mesin 후 밀리초, 32비트 Kitaran_VALUE |
| `udp_open(port)` | 127.0.0.1의 UDP 소켓 Buka/ikat_peserta; 0은 자동 포트 |
| `udp_send(fd, port, data)` | 루프백 destinasi_VALUE 포트에 str/bytes 버퍼 pindah_VALUE |
| `udp_recv(fd)` | `(bytes, 보낸포트)` kembalikan_ukuran; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | 소켓 Tutup |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

이식 kod_VALUE: [python/](PYTHON_penghubung/), [ruang_pengguna Java Sambung](ruang_pengguna/자바연결.c). 공식 [MicroPython 이식 README_eb81d7d9](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. sumber_pepohon URL·cincangan_fail·라이선스는 [vendor README_eb81d7d9](vendor/README.md)에 기록했다.

## 남은 작업

| Seterusnya_item pentas_VALUE | 완료 projek_akar |
|---|---|
| 영속 stor_VALUE·laksanakan_perintah Fail 입력 | SD/MMC 및 디스크 Fail 시스템, 시스템/ruang_pengguna 볼륨; 현재 ELF Fail 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 e_mel e_mel_rantau, 선점 스케줄러, TLS, segerak/tunggu_VALUE, 신호, mmap/mprotect |
| libc와 C++ 런타임 | Asli ABI용 libc, malloc/free, 표준 I_O·Jam·persekitaran·locale, libstdc++/pengecualian Proses_VALUE_pemasukan sahkan |
| CPython | 해당 libc와 OS API 대상으로 이식·교차 빌드하고 Fail/Unicode/스레드/소켓 ujian |
| OpenJDK/JRE | HotSpot OS lapisan_VALUE, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 pustaka 이식; javac/java sebenar_data laksanakan_perintah |
| 외부 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 sebenar_data Papan 송수신 sahkan, DNS·Wi-Fi |
| GUI sambungan_VALUE | USB HID, 게스트 입력기·문자 조판, Swing Tetingkap Saiz 조절·클리핑 sambungan_VALUE, 전체 AWT/Swing 이식 |

이 표는 남은 작업이며 pelaksanaan 완료 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 외부 네트워크 드라이버는 실물 검증도 필요하다. [QEMU peranti_VALUE 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

하드웨어 및 ABI 참고: [BCM2711 aksesori](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC e_mel](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox kes_VALUE](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP kawalan_VALUE 레지스터 Takrif_VALUE](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## Melayu C jenis_data·Python RALAT·pakej pasang_VALUE

C 네트워크 API는 `struct 인터넷통신주소`, enum 상수와 sebenar_data Melayu 함수로
구현한다. makro_VALUE 별칭을 사용하지 않으며 이전 pk_* ABI도 유지한다.
Python 예제는 `sistem_ralat`, `RALAT.INDEX`, `RALAT.설명`을 사용한다.

`python3 alat/laksanakan_perintah.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 수 있다. 현재는 hos 중계를
이용하는 제한형 MicroPython sumber_pepohon 설치기이며 CPython pip·자동 의존성 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 제한](PYTHON_pakej.md).

## 화면 Saiz pilihan_VALUE

`python3 alat/laksanakan_perintah.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. Terminal alih_VALUE, Swing 가운데 susun_atur_pautan, Java·C·Python 그리기도 sebenar_data 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [Tetapan·Melayu API·sahkan README_eb81d7d9](화면해상도.md).

## Melayu 직접 API와 화면 segar_semula

`example/java`는 `실행할일`, `동작받이`, `동작알림`, `Butang`, `acara_baris`,
`작업가닥`, `Jalan()`을 사용할 수 있다. Melayu GUI/가닥을 Asli JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. rentetan_VALUE 등 javac의 표준
계약과 전체 sumber_pepohon 검토 범위는 [명명 README_eb81d7d9](명명/README_eb81d7d9.md), 사용법과 호환성 변경은
[Melayu Java API](한국어자바/README_eb81d7d9.md)를 본다.

Terminal alih_VALUE·Saiz 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[화면 segar_semula 설명](자바실행환경.md#Terminal-부분-segar_semula),
[부분 segar_semula 검사](build/verification/redraw/report.json)를 참고한다.
