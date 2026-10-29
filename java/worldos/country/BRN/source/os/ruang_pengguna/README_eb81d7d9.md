# 셸에서 실행하는 ruang_pengguna 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java 개발 persekitaran README_eb81d7d9](../../문서/자바개발환경.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 laksanakan_perintah

hos Terminal 1:

```sh
cd /home/user/jkoros
python3 os/alat/자료되돌리기.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. 외부 연결을 받도록 방화벽이나 포트 전달을 변경하지 않는다. Ctrl+C로 종료한다.

hos Terminal 2:

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

- `hello`: 독립 Java ELF 실행과 sebenar_data CPU keizinan_VALUE `ring 3`, 인수 출력.
- `netcheck`: port_VALUE 중복, 잘못된 pemegang_VALUE/penuding/kepanjangan_VALUE, 비차단 받기와 nilai_masa 초과 tentu_sahkan.
- `udp`: IPv4 e_mel·destinasi_VALUE port_VALUE·한 Word_VALUE 메시지를 받아 UDP로 보내고 같은 응답을 tentu_sahkan. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: hos `10.0.2.2`의 Tugaskan_VALUE 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. 수신 Loop_VALUE 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. 현재 주소는 게스트 `10.0.2.15/24`, get_laluan_VALUE `10.0.2.2`로 고정돼 있다. QEMU ruang_pengguna 네트워크의 hos capai_pemasukan 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 aplikasi_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java aplikasi_f5044b9b Tambah_pemasukan

`예제/내프로그램.java`를 Seterusnya_item 형식으로 만든다. 진입점은 인수 없는 `static int` 또는 `static void` 함수다. 인수는 ruang_pengguna API로 조회한다.

```java
public final class 내프로그램 {
    public static int Jalan() {
        ruang_pengguna.Tulis("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/ruang_pengguna/aplikasi_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := ruang_pengguna/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.Jalan
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `ruang_pengguna/pengisytiharan_4f4f026b/ruang_pengguna.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 laksanakan_perintah 중인 VM에는 bina_sistem 결과가 자동 반영되지 않는다. aplikasi_f5044b9b 이름은 현재 셸의 ASCII 입력 제한에 맞춘 1~15자의 소문자 이름이며 Java Kelas_VALUE·fungsi_VALUE·변수에는 한국어를 쓴다. 최대 32개 aplikasi_f5044b9b, 한 laksanakan_perintah 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target user --entry 인사.Jalan \
    -o os/build/apps/hello.elf os/ruang_pengguna/pengisytiharan_4f4f026b/ruang_pengguna.java os/ruang_pengguna/예제/인사.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 hos 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 Sokongan_VALUE klip 안에서 실행한다. `.jar`와 일반 Linux laksanakan_perintah 파일은 지원하지 않는다.

## ruang_pengguna 네트워크 API

선언은 `pengisytiharan_4f4f026b/ruang_pengguna.java`에 있다. `e_mel_data_5b5410b2`/`자료받기`의 `int[]` item_unsur 한 개는 bait_VALUE 하나(0~255)를 나타낸다. 한 데이터그램의 최대 data 길이는 1,024바이트다.

```java
int pemegang_VALUE = ruang_pengguna.buka_rangkaian(0); // 0: 임시 setempat_Skop UDP port_VALUE 자동 pilihan_VALUE
int[] data = new int[32];
data[0] = 'H'; data[1] = 'i';
int 보낸길이 = ruang_pengguna.e_mel_data_5b5410b2(pemegang_VALUE, 0x0a000202, 9000, data, 2);
int RECEIVED_kepanjangan = ruang_pengguna.자료받기(pemegang_VALUE, data, 1500);
ruang_pengguna.Tutup_rangkaian(pemegang_VALUE);
```

sebenar_data 프로그램에서는 Buka·e_mel_9aee63bd·받기의 음수 반환값을 각각 검사한다. 완성된 예제는 `예제/자료통신.java`에 있다. `자료받기`의 tunggu_VALUE 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 수신 대기열은 한 개뿐이므로 Tambah_pemasukan 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | pemegang_VALUE·Proses_VALUE_pemasukan kepanjangan_VALUE·성공 등 해당 함수의 ukuran |
| -5 | peranti_VALUE e_mel_VALUE_f993dacd kegagalan_VALUE |
| -9 | 잘못되었거나 닫힌 통신 pemegang_VALUE |
| -11 | 비차단 받기에서 도착한 data 없음 |
| -14 | ruang_pengguna penuding/ARRAY_VALUE klip RALAT |
| -19 | Sokongan_VALUE NIC 없음 |
| -22 | port_VALUE/tunggu_VALUE nilai_masa/인수 VALUE RALAT |
| -24 | 열린 rangkaian_port 4개 한도 |
| -38 | 알 수 없는 시스템 호출 |
| -90 | data 또는 수신 ARRAY_VALUE Saiz 문제 |
| -98 | setempat_Skop port_VALUE INDEX 중복 |
| -101 | 지원하지 않는 destinasi_VALUE e_mel |
| -110 | ARP·peranti_VALUE·수신 nilai_masa 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 pengekodan_VALUE 있는 Java `int`의 bit_VALUE 패턴을 사용하므로 상위 비트가 1인 정상 IP 주소가 음수로 보일 수 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## laksanakan_perintah 경계와 시스템 호출

```text
cangkerang run → JKAP에서 ELF sahkan·적재 → ring 3 ruang_pengguna aplikasi_f5044b9b
                                 ↓ int 0x80
                      penuding 검사 → Java kernel_VALUE API → RTL8139/UDP
                                 ↓ Keluar_aplikasi·pengecualian·nilai_masa 초과
                                cangkerang 복귀
```

시스템 호출 레지스터는 `EAX=INDEX`, `EBX,ECX,EDX,ESI,EDI=인수`, `EAX=ukuran`다. Java 호출 스택 ABI는 컴파일러가 ruang_pengguna 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| INDEX | 호출 |
| --- | --- |
| 0 | Keluar_aplikasi(status_VALUE kod_VALUE) — Jalan/RALAT 런타임에서 사용 |
| 1 | rentetan_VALUE Tulis |
| 2 / 3 | 인수 item_COUNT / 인수 rentetan_VALUE e_mel |
| 10 | UDP Buka |
| 11 | UDP e_mel_9aee63bd(pemegang_VALUE, IP, destinasi_VALUE port_VALUE, ARRAY_VALUE e_mel, kepanjangan_VALUE) |
| 12 | UDP 받기(pemegang_VALUE, ARRAY_VALUE e_mel, 제한 밀리초) |
| 13 | UDP Tutup |
| 14 | setempat_Skop IP e_mel |
| 15 / 16 | 마지막 rakan_VALUE IP / UDP port_VALUE |
| 20 | RAM Fail Baca(Nama int[] e_mel, 출력 int[] e_mel) |
| 21 | RAM Fail Tulis(Nama int[] e_mel, 입력 int[] e_mel, bait_VALUE kepanjangan_VALUE) |
| 22 | UTF-16 kod_VALUE unit_VALUE 문자 출력(0~65535) |

Fail API는 `ruang_pengguna.파일읽기(int[] Nama, int[] data)`와 `ruang_pengguna.tulis_fail(int[] Nama, int[] data, int kepanjangan_VALUE)`다. 이름은 ASCII kod_VALUE ARRAY_VALUE(최대 64칸, 0 Keluar_aplikasi 또는 ARRAY_VALUE 끝), data item_unsur 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 Fail 없음 `-2`, penuding RALAT `-14`, Nama/kepanjangan_VALUE RALAT `-22`, Fail 슬롯 부족 `-28`, Saiz 초과 `-90`을 반환한다. 쓰기는 sahkan 후 Fail 전체를 대체한다. `ruang_pengguna.tulis_aksara_VALUE(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`실행권한()`은 시스템 호출이 아니라 ruang_pengguna 모드에서 CS의 하위 비트를 직접 읽으므로 sebenar_data laksanakan_perintah 권한을 확인한다. kernel_VALUE 포트 접근용 `peranti_VALUE` native 함수는 ruang_pengguna sasaran 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 laksanakan_perintah, 파이프, 프로세스 간 통신은 없다. laksanakan_perintah 파일은 커널의 Baca 전용 JKAP 묶음에서 적재한다. data 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- ruang_pengguna 가상 e_mel `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. laksanakan_perintah 영상은 hadapan_VALUE 2MiB, 인수는 `0x04300000`부터, 스택은 rantau_VALUE 끝에서 시작한다. kernel_VALUE identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB ruang_pengguna 영역을 비우고 Fail 구역을 복사해 BSS·ARRAY_VALUE 영역을 초기화한다. ruang_pengguna GC는 없지만 Keluar_aplikasi 후 Seterusnya_item laksanakan_perintah 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 Petikan/이스케이프 파싱은 없다.
- ruang_pengguna 페이지의 kod_VALUE/data 분리 Baca 전용 Tetapan, NX, 스택 guard, ASLR은 아직 없다. 커널과 ruang_pengguna Memori_data·포트 keizinan_VALUE 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 laksanakan_perintah 상한을 두며 nilai_masa 초과는 `Exit: 124`다. ruang_pengguna CPU 예외는 `128 + pengecualian INDEX`(페이지 RALAT 142, 특권 위반 141), Java ARRAY_VALUE/계산 오류는 101~105다. kernel_VALUE 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, statik_VALUE IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP hasil_tambah_semak 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- ruang_pengguna laksanakan_perintah·네트워크·lindung_VALUE 경계 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 laksanakan_perintah·정상 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## sahkan 근거

`make test`는 컴파일러 14개 ujian, Java 패킷 syarat 2,201개 검사, 기존 cangkerang ELF/ISO permulaan_mesin ujian, ruang_pengguna ELF/sebenar_data UDP/lindung_VALUE 경계 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 kepanjangan_VALUE·해시까지 `os/build/ujian_pengguna_rangkaian.json`에 기록한다. 시험용 손상된 ELF·특권 Perintah·무한 lelaran_VALUE 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 data: [Intel 시스템 프로그래밍 명세](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 pelaksanaan](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 README_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
