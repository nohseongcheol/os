# 셸에서 실행하는 NgườiDùng 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java phátTriển môiTrường HướngDẫn](../../TàiLiệu/MôiTrườngPhátTriểnJava.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 thựcThiLệnh

Chủ thiếtBịCuối 1:

```sh
cd /home/user/jkoros
python3 os/CôngCụ/PhụcHồiDữLiệu.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. giáTrịBênNgoài 연결을 받도록 방화벽이나 cổngPhầnCứng 전달을 변경하지 않는다. Ctrl+C로 종료한다.

Chủ thiếtBịCuối 2:

```sh
cd /home/user/jkoros
make run
```

게스트의 `jkoros>` 프롬프트에 giáTrịVào:

```text
apps
run hello first second
net
run netcheck
run udp 10.0.2.2 9000 hello
run stress 9000
```

- `hello`: 독립 Java ELF 실행과 dữLiệuThựcTế CPU giáTrịQuyền `ring 3`, cácĐốiSố ĐầuRa.
- `netcheck`: giáTrịCổng 중복, 잘못된 giáTrịThẻXửLý/conTrỏ/độDài, 비차단 받기와 giáTrịThờiGian 초과 xácMinh.
- `udp`: IPv4 địaChỉ·giáTrịĐích giáTrịCổng·한 giáTrịTừ 메시지를 받아 UDP로 보내고 같은 응답을 xácMinh. `UDP ECHO PASS`, `Exit: 0`이면 giáTrịThànhCông.
- `stress`: Chủ `10.0.2.2`의 giáTrịGán 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. nhậnGiáTrị giáTrịVòngLặp 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. phầnMụcHiệnTại 주소는 게스트 `10.0.2.15/24`, giáTrịCổngNối `10.0.2.2`로 고정돼 있다. QEMU NgườiDùng 네트워크의 Chủ mụcTruyCập 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 ChươngTrình 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java ChươngTrình thêmCuốiMục

`VíDụ/내프로그램.java`를 phầnMụcKếTiếp 형식으로 만든다. 진입점은 cácĐốiSố 없는 `static int` 또는 `static void` 함수다. 인수는 NgườiDùng API로 조회한다.

```java
public final class 내프로그램 {
    public static int chạy() {
        NgườiDùng.ghi("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/NgườiDùng/ChươngTrình.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := NgườiDùng/VíDụ/내프로그램.java
APP_ENTRY_mine := 내프로그램.chạy
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 xâyDựngTấtCả 나열한다. `NgườiDùng/KhaiBáo/NgườiDùng.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 thựcThiLệnh 중인 VM에는 xâyDựngHệThống 결과가 자동 반영되지 않는다. ChươngTrình 이름은 phầnMụcHiệnTại 셸의 ASCII giáTrịVào 제한에 맞춘 1~15자의 소문자 이름이며 Java giáTrịLớp·Hàm·변수에는 한국어를 쓴다. giáTrịTốiĐa 32개 ChươngTrình, 한 thựcThiLệnh 파일은 giáTrịTốiĐa 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/TrìnhBiênDịch.py --target user --entry LờiChào.chạy \
    -o os/build/apps/hello.elf os/NgườiDùng/KhaiBáo/NgườiDùng.java os/NgườiDùng/VíDụ/LờiChào.java
```

`--target user`는 **jkoros 전용 ABI**toánHạngThứBa. Linux 대상과 시스템 gọiThựcHiện 번호가 다르므로 Chủ 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 giáTrịHỗTrợ cắtXén 안에서 실행한다. `.jar`와 일반 Linux thựcThiLệnh 파일은 지원하지 않는다.

## NgườiDùng 네트워크 API

선언은 `KhaiBáo/NgườiDùng.java`에 있다. `gửiDữLiệu`/`nhậnDữLiệu`의 `int[]` phầnTửPhầnMục 한 개는 giáTrịByte giáTrịMột(0~255)를 나타낸다. 한 데이터그램의 giáTrịTốiĐa DữLiệu 길이는 1,024바이트다.

```java
int giáTrịThẻXửLý = NgườiDùng.mởMạng(0); // 0: giáTrịTạm phạmViCụcBộ UDP giáTrịCổng 자동 giáTrịViệcChọn
int[] DữLiệu = new int[32];
DữLiệu[0] = 'H'; DữLiệu[1] = 'i';
int 보낸길이 = NgườiDùng.gửiDữLiệu(giáTrịThẻXửLý, 0x0a000202, 9000, DữLiệu, 2);
int độDàiĐãNhận = NgườiDùng.nhậnDữLiệu(giáTrịThẻXửLý, DữLiệu, 1500);
NgườiDùng.đóngMạng(giáTrịThẻXửLý);
```

dữLiệuThựcTế 프로그램에서는 mở·gửi·받기의 giáTrịÂm 반환값을 각각 검사한다. 완성된 예제는 `VíDụ/TruyềnThôngDữLiệu.java`에 있다. `nhậnDữLiệu`의 chờGiáTrị 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 nhậnGiáTrị 대기열은 한 개뿐이므로 thêmCuốiMục 도착분은 버린다. `địaChỉĐãGửi`와 `cổngĐãGửi`로 마지막으로 받은 상대를 조회한다.

| giáTrịĐãTrảVề | 의미 |
| --- | --- |
| 0 이상 | giáTrịThẻXửLý·mụcGiáTrịTiếnTrình độDài·giáTrịThànhCông 등 해당 함수의 kếtQuả |
| -5 | ThiếtBị gửiGiáTrị giáTrịSựThấtBại |
| -9 | 잘못되었거나 닫힌 TruyềnThông giáTrịThẻXửLý |
| -11 | 비차단 받기에서 도착한 DữLiệu phươngThứcThiếu |
| -14 | NgườiDùng conTrỏ/giáTrịMảng cắtXén lỗi |
| -19 | giáTrịHỗTrợ NIC phươngThứcThiếu |
| -22 | giáTrịCổng/chờGiáTrị giáTrịThờiGian/cácĐốiSố giáTrị lỗi |
| -24 | 열린 cổngMạng 4개 giớiHạnSứcChứa |
| -38 | 알 trịSố 없는 시스템 gọiThựcHiện |
| -90 | DữLiệu 또는 nhậnGiáTrị giáTrịMảng cỡ 문제 |
| -98 | phạmViCụcBộ giáTrịCổng sốHiệu 중복 |
| -101 | 지원하지 않는 giáTrịĐích địaChỉ |
| -110 | ARP·ThiếtBị·nhậnGiáTrị giáTrịThờiGian 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 giáTrịBảngMã 있는 Java `int`의 giáTrịBit 패턴을 사용하므로 상위 비트가 1인 làBìnhThường IP 주소가 음수로 보일 trịSố 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## thựcThiLệnh 경계와 시스템 gọiThựcHiện

```text
vỏLệnh run → JKAP에서 ELF thẩmĐịnh·적재 → ring 3 NgườiDùng ChươngTrình
                                 ↓ int 0x80
                      conTrỏ CácPhépKiểmTra → Java giáTrịNhân API → RTL8139/UDP
                                 ↓ chươngTrìnhRa·ngoạiLệ·giáTrịThờiGian 초과
                                vỏLệnh 복귀
```

시스템 gọiThựcHiện 레지스터는 `EAX=sốHiệu`, `EBX,ECX,EDX,ESI,EDI=cácĐốiSố`, `EAX=kếtQuả`toánHạngThứBa. Java gọiThựcHiện ngănXếpToánHạng ABI는 컴파일러가 NgườiDùng 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| sốHiệu | gọiThựcHiện |
| --- | --- |
| 0 | chươngTrìnhRa(giáTrịTrạngThái giáTrịMã) — chạy/lỗi 런타임에서 giáTrịDùng |
| 1 | ChuỗiKýTự ghi |
| 2 / 3 | cácĐốiSố sốLượngPhầnMục / cácĐốiSố ChuỗiKýTự địaChỉ |
| 10 | UDP mở |
| 11 | UDP gửi(giáTrịThẻXửLý, IP, giáTrịĐích giáTrịCổng, giáTrịMảng địaChỉ, độDài) |
| 12 | UDP nhận(giáTrịThẻXửLý, giáTrịMảng địaChỉ, giáTrịGiớiHạn miliGiây) |
| 13 | UDP đóng |
| 14 | phạmViCụcBộ IP địaChỉ |
| 15 / 16 | phầnMụcCuối giáTrịĐốiTác IP / UDP giáTrịCổng |
| 20 | RAM Tệp đọc(tên int[] địaChỉ, ĐầuRa int[] địaChỉ) |
| 21 | RAM Tệp ghi(tên int[] địaChỉ, giáTrịVào int[] địaChỉ, giáTrịByte độDài) |
| 22 | UTF-16 giáTrịMã giáTrịĐơnVị KýTự ĐầuRa(0~65535) |

Tệp API는 `NgườiDùng.đọcTệp(int[] tên, int[] DữLiệu)`와 `NgườiDùng.ghiTệp(int[] tên, int[] DữLiệu, int độDài)`toánHạngThứBa. 이름은 ASCII giáTrịMã giáTrịMảng(giáTrịTốiĐa 64칸, 0 chươngTrìnhRa 또는 giáTrịMảng phầnKết), DữLiệu phầnTửPhầnMục 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 Tệp phươngThứcThiếu `-2`, conTrỏ lỗi `-14`, tên/độDài lỗi `-22`, Tệp giáTrịÔ 부족 `-28`, cỡ 초과 `-90`을 반환한다. 쓰기는 thẩmĐịnh trạngTháiSau Tệp 전체를 대체한다. `NgườiDùng.ghiGiáTrịKýTự(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`quyềnViệcThựcThi()`은 시스템 호출이 아니라 NgườiDùng 모드에서 CS의 하위 비트를 직접 읽으므로 dữLiệuThựcTế thựcThiLệnh 권한을 확인한다. giáTrịNhân cổngPhầnCứng 접근용 `ThiếtBị` native 함수는 NgườiDùng giáTrịĐốiĐích 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 giáTrịGiớiHạn

- 한 번에 한 프로그램만 실행하며 làĐầyĐủ trạngTháiSau 셸로 돌아온다. 백그라운드 thựcThiLệnh, 파이프, 프로세스 간 통신은 없다. thựcThiLệnh 파일은 커널의 đọc 전용 JKAP 묶음에서 적재한다. DữLiệu 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- NgườiDùng 가상 địaChỉ `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. thựcThiLệnh 영상은 giáTrịPhíaTrước 2MiB, 인수는 `0x04300000`부터, 스택은 giáTrịMiền 끝에서 시작한다. giáTrịNhân identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB NgườiDùng 영역을 비우고 Tệp 구역을 복사해 BSS·giáTrịMảng 영역을 초기화한다. NgườiDùng GC는 없지만 chươngTrìnhRa trạngTháiSau phầnMụcKếTiếp thựcThiLệnh 때 영역을 재사용한다. 인수는 공백으로 분리한 giáTrịTốiĐa 16개이며 dấuTrích/이스케이프 파싱은 없다.
- NgườiDùng 페이지의 giáTrịMã/DữLiệu 분리 đọc 전용 cácThiếtLập, NX, ngănXếpToánHạng guard, ASLR은 아직 없다. 커널과 NgườiDùng dữLiệuBộNhớ·cổngPhầnCứng giáTrịQuyền 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 thựcThiLệnh 상한을 두며 giáTrịThờiGian 초과는 `Exit: 124`toánHạngThứBa. NgườiDùng CPU 예외는 `128 + ngoạiLệ sốHiệu`(페이지 lỗi 142, 특권 위반 141), Java giáTrịMảng/phépTính 오류는 101~105다. giáTrịNhân 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, giáTrịTĩnh IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP tổngKiểm 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- NgườiDùng thựcThiLệnh·네트워크·bảoVệGiáTrị giáTrịRanhGiới 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 thựcThiLệnh·làBìnhThường 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## thẩmĐịnh 근거

`make test`는 TrìnhBiênDịch 14개 KiểmThử, Java 패킷 điềuKiện 2,201개 CácPhépKiểmTra, 기존 vỏLệnh ELF/ISO KhởiĐộng KiểmThử, NgườiDùng ELF/dữLiệuThựcTế UDP/bảoVệGiáTrị giáTrịRanhGiới 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 độDài·해시까지 `os/build/thửMạngNgườiDùng.json`에 기록한다. 시험용 손상된 ELF·특권 lệnh·무한 giáTrịLầnLặp 프로그램은 giáTrịTạm 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 DữLiệu: [Intel 시스템 프로그래밍 đặcTả](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 phầnCàiĐặt](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 HướngDẫn](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
