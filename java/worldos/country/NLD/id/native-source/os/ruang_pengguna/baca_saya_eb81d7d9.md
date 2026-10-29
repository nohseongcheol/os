# 셸에서 실행하는 ruang_pengguna 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java 개발 lingkungan baca_saya_eb81d7d9](../../문서/자바개발환경.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 Jalankan_perintah

host terminal 1:

```sh
cd /home/user/jkoros
python3 os/alat/echo_data.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. eksternal_VALUE 연결을 받도록 방화벽이나 포트 전달을 변경하지 않는다. Ctrl+C로 종료한다.

host terminal 2:

```sh
cd /home/user/jkoros
make run
```

게스트의 `jkoros>` 프롬프트에 입력:

```text
apps
run hello first second
net
run netcheck
run udp 10.0.2.2 9000 hello
run stress 9000
```

- `hello`: 독립 Java ELF 실행과 aktual_data CPU izin_VALUE `ring 3`, argumen keluaranTeks.
- `netcheck`: port_VALUE 중복, 잘못된 handel_VALUE/pointer/panjang_VALUE, 비차단 받기와 TIME_VALUE 초과 periksa.
- `udp`: IPv4 surel·tujuan_VALUE port_VALUE·한 Kata_VALUE 메시지를 받아 UDP로 보내고 같은 응답을 periksa. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: host `10.0.2.2`의 Tugaskan_VALUE 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. terima_VALUE Loop_VALUE 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. saat_ini_item 주소는 게스트 `10.0.2.15/24`, gateway_VALUE `10.0.2.2`로 고정돼 있다. QEMU ruang_pengguna 네트워크의 host akses_entri 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 apl_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java apl_f5044b9b tambah_entri

`예제/내프로그램.java`를 Berikutnya_item 형식으로 만든다. 진입점은 argumen 없는 `static int` 또는 `static void` 함수다. 인수는 ruang_pengguna API로 조회한다.

```java
public final class 내프로그램 {
    public static int jalankan() {
        ruang_pengguna.Tulis("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/ruang_pengguna/apl_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := ruang_pengguna/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.jalankan
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `ruang_pengguna/deklarasi_4f4f026b/ruang_pengguna.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 Jalankan_perintah 중인 VM에는 bangun 결과가 자동 반영되지 않는다. apl_f5044b9b 이름은 saat_ini_item 셸의 ASCII 입력 제한에 맞춘 1~15자의 소문자 이름이며 Java Kelas_VALUE·fungsi_VALUE·변수에는 한국어를 쓴다. 최대 32개 apl_f5044b9b, 한 Jalankan_perintah 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target user --entry 인사.jalankan \
    -o os/build/apps/hello.elf os/ruang_pengguna/deklarasi_4f4f026b/ruang_pengguna.java os/ruang_pengguna/예제/인사.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 host 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 dukung_VALUE klip 안에서 실행한다. `.jar`와 일반 Linux Jalankan_perintah 파일은 지원하지 않는다.

## ruang_pengguna 네트워크 API

선언은 `deklarasi_4f4f026b/ruang_pengguna.java`에 있다. `kirim_data`/`Data_Penerimaan`의 `int[]` item_elemen 한 개는 byte_VALUE 하나(0~255)를 나타낸다. 한 데이터그램의 최대 data 길이는 1,024바이트다.

```java
int handel_VALUE = ruang_pengguna.buat_jaringan(0); // 0: 임시 lokal_Cakupan UDP port_VALUE 자동 pilihan_VALUE
int[] data = new int[32];
data[0] = 'H'; data[1] = 'i';
int 보낸길이 = ruang_pengguna.kirim_data(handel_VALUE, 0x0a000202, 9000, data, 2);
int RECEIVED_panjang = ruang_pengguna.Data_Penerimaan(handel_VALUE, data, 1500);
ruang_pengguna.Tutup_jaringan(handel_VALUE);
```

aktual_data 프로그램에서는 Buka·kirim·받기의 음수 반환값을 각각 검사한다. 완성된 예제는 `예제/data_komunikasi.java`에 있다. `Data_Penerimaan`의 tunggu_VALUE 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 terima_VALUE 대기열은 한 개뿐이므로 tambah_entri 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | handel_VALUE·Proses_VALUE_entri panjang_VALUE·성공 등 해당 함수의 hasil |
| -5 | Ponsel_VALUE kirim_VALUE kegagalan_VALUE |
| -9 | 잘못되었거나 닫힌 komunikasi handel_VALUE |
| -11 | 비차단 받기에서 도착한 data 없음 |
| -14 | ruang_pengguna pointer/ARRAY_VALUE klip galat |
| -19 | dukung_VALUE NIC 없음 |
| -22 | port_VALUE/tunggu_VALUE TIME_VALUE/argumen VALUE galat |
| -24 | 열린 jaringan_port 4개 한도 |
| -38 | 알 수 없는 시스템 호출 |
| -90 | data 또는 terima_VALUE ARRAY_VALUE Ukuran 문제 |
| -98 | lokal_Cakupan port_VALUE INDEX 중복 |
| -101 | 지원하지 않는 tujuan_VALUE surel |
| -110 | ARP·Ponsel_VALUE·terima_VALUE TIME_VALUE 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 pengodean_VALUE 있는 Java `int`의 bit_VALUE 패턴을 사용하므로 상위 비트가 1인 정상 IP 주소가 음수로 보일 수 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## Jalankan_perintah 경계와 시스템 호출

```text
shell run → JKAP에서 ELF validasi·적재 → ring 3 ruang_pengguna apl_f5044b9b
                                 ↓ int 0x80
                      pointer 검사 → Java kernel_VALUE API → RTL8139/UDP
                                 ↓ Keluar_apl·pengecualian·TIME_VALUE 초과
                                shell 복귀
```

시스템 호출 레지스터는 `EAX=INDEX`, `EBX,ECX,EDX,ESI,EDI=argumen`, `EAX=hasil`다. Java 호출 operand_tumpuk ABI는 컴파일러가 ruang_pengguna 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| INDEX | 호출 |
| --- | --- |
| 0 | Keluar_apl(Status_VALUE CODE_VALUE) — jalankan/galat 런타임에서 gunakan_VALUE |
| 1 | string_VALUE Tulis |
| 2 / 3 | argumen item_COUNT / argumen string_VALUE surel |
| 10 | UDP Buka |
| 11 | UDP kirim(handel_VALUE, IP, tujuan_VALUE port_VALUE, ARRAY_VALUE surel, panjang_VALUE) |
| 12 | UDP terima(handel_VALUE, ARRAY_VALUE surel, 제한 밀리초) |
| 13 | UDP Tutup |
| 14 | lokal_Cakupan IP surel |
| 15 / 16 | 마지막 serekan_VALUE IP / UDP port_VALUE |
| 20 | RAM berkas Baca(Nama_2 int[] surel, keluaranTeks int[] surel) |
| 21 | RAM berkas Tulis(Nama_2 int[] surel, 입력 int[] surel, byte_VALUE panjang_VALUE) |
| 22 | UTF-16 CODE_VALUE unit_VALUE 문자 keluaranTeks(0~65535) |

berkas API는 `ruang_pengguna.파일읽기(int[] Nama_2, int[] data)`와 `ruang_pengguna.tulis_file(int[] Nama_2, int[] data, int panjang_VALUE)`다. 이름은 ASCII CODE_VALUE ARRAY_VALUE(최대 64칸, 0 Keluar_apl 또는 ARRAY_VALUE 끝), data item_elemen 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 berkas 없음 `-2`, pointer galat `-14`, Nama_2/panjang_VALUE galat `-22`, berkas slot_VALUE 부족 `-28`, Ukuran 초과 `-90`을 반환한다. 쓰기는 validasi 후 berkas 전체를 대체한다. `ruang_pengguna.tulis_karakter_VALUE(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`실행권한()`은 시스템 호출이 아니라 ruang_pengguna 모드에서 CS의 하위 비트를 직접 읽으므로 aktual_data Jalankan_perintah 권한을 확인한다. kernel_VALUE 포트 접근용 `Ponsel_VALUE` native 함수는 ruang_pengguna target 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 Jalankan_perintah, 파이프, 프로세스 간 통신은 없다. Jalankan_perintah 파일은 커널의 Baca 전용 JKAP 묶음에서 적재한다. data 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- ruang_pengguna 가상 surel `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. Jalankan_perintah 영상은 depan_VALUE 2MiB, 인수는 `0x04300000`부터, 스택은 wilayah_VALUE 끝에서 시작한다. kernel_VALUE identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB ruang_pengguna 영역을 비우고 berkas 구역을 복사해 BSS·ARRAY_VALUE 영역을 초기화한다. ruang_pengguna GC는 없지만 Keluar_apl 후 Berikutnya_item Jalankan_perintah 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 Kutipan/이스케이프 파싱은 없다.
- ruang_pengguna 페이지의 CODE_VALUE/data 분리 Baca 전용 Konfigurasi, NX, operand_tumpuk guard, ASLR은 아직 없다. 커널과 ruang_pengguna Memori_data·포트 izin_VALUE 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 Jalankan_perintah 상한을 두며 TIME_VALUE 초과는 `Exit: 124`다. ruang_pengguna CPU 예외는 `128 + pengecualian INDEX`(페이지 galat 142, 특권 위반 141), Java ARRAY_VALUE/계산 오류는 101~105다. kernel_VALUE 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, statik_VALUE IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP checksum 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- ruang_pengguna Jalankan_perintah·네트워크·amankan_VALUE 경계 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 Jalankan_perintah·정상 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## validasi 근거

`make test`는 컴파일러 14개 pengujian, Java 패킷 kondisi 2,201개 검사, 기존 shell ELF/ISO awal_mesin pengujian, ruang_pengguna ELF/aktual_data UDP/amankan_VALUE 경계 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 panjang_VALUE·해시까지 `os/build/사용자통신시험.json`에 기록한다. 시험용 손상된 ELF·특권 perintah·무한 sprint_VALUE 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 data: [Intel 시스템 프로그래밍 spes](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 implementasi](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 baca_saya_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
