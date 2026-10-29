# 셸에서 실행하는 defnyddiwr 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java 개발 환경 GWYBODAETH_eb81d7d9](../../문서/자바개발환경.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 Gweithredu_gorchymyn

lletya Terfynell 1:

```sh
cd /home/user/jkoros
python3 os/Offer/자료되돌리기.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. 외부 연결을 받도록 방화벽이나 포트 전달을 변경하지 않는다. Ctrl+C로 종료한다.

lletya Terfynell 2:

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

- `hello`: 독립 Java ELF 실행과 go_iawn_data CPU hawl_VALUE `ring 3`, 인수 Allbwn.
- `netcheck`: porth_VALUE 중복, 잘못된 dolen_VALUE/pwyntydd/hyd_VALUE, 비차단 받기와 TIME_VALUE 초과 dilysu.
- `udp`: IPv4 ADDRESS·cyrchfan_VALUE porth_VALUE·한 Word_VALUE 메시지를 받아 UDP로 보내고 같은 응답을 dilysu. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: lletya `10.0.2.2`의 지정 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. 수신 Loop_VALUE 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. 현재 주소는 게스트 `10.0.2.15/24`, adwy_VALUE `10.0.2.2`로 고정돼 있다. QEMU defnyddiwr 네트워크의 lletya mynediad_cofnod 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 Rhaglen_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java Rhaglen_f5044b9b 추가

`예제/내프로그램.java`를 Nesaf_eitem 형식으로 만든다. 진입점은 인수 없는 `static int` 또는 `static void` 함수다. 인수는 defnyddiwr API로 조회한다.

```java
public final class 내프로그램 {
    public static int Gweithredu_2() {
        defnyddiwr.Ysgrifennu("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/defnyddiwr/Rhaglen_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := defnyddiwr/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.Gweithredu_2
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `defnyddiwr/선언/defnyddiwr.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 Gweithredu_gorchymyn 중인 VM에는 llunio_system 결과가 자동 반영되지 않는다. Rhaglen_f5044b9b 이름은 현재 셸의 ASCII 입력 제한에 맞춘 1~15자의 소문자 이름이며 Java Dosbarth_VALUE·SWYDDOGAETH_VALUE·변수에는 한국어를 쓴다. 최대 32개 Rhaglen_f5044b9b, 한 Gweithredu_gorchymyn 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target user --entry 인사.Gweithredu_2 \
    -o os/build/apps/hello.elf os/defnyddiwr/선언/defnyddiwr.java os/defnyddiwr/예제/인사.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 lletya 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 Cymorth_VALUE clip 안에서 실행한다. `.jar`와 일반 Linux Gweithredu_gorchymyn 파일은 지원하지 않는다.

## defnyddiwr 네트워크 API

선언은 `선언/defnyddiwr.java`에 있다. `anfon_data`/`자료받기`의 `int[]` eitem_elfen 한 개는 beit_VALUE 하나(0~255)를 나타낸다. 한 데이터그램의 최대 data 길이는 1,024바이트다.

```java
int dolen_VALUE = defnyddiwr.agor_Rhwydwaith(0); // 0: 임시 lleol_cwmpas UDP porth_VALUE 자동 dewisiad_VALUE
int[] data = new int[32];
data[0] = 'H'; data[1] = 'i';
int 보낸길이 = defnyddiwr.anfon_data(dolen_VALUE, 0x0a000202, 9000, data, 2);
int RECEIVED_hyd = defnyddiwr.자료받기(dolen_VALUE, data, 1500);
defnyddiwr.cau_Rhwydwaith(dolen_VALUE);
```

go_iawn_data 프로그램에서는 Agor·anfon·받기의 음수 반환값을 각각 검사한다. 완성된 예제는 `예제/자료통신.java`에 있다. `자료받기`의 aros_VALUE 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 수신 대기열은 한 개뿐이므로 추가 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | dolen_VALUE·Proses_VALUE_cofnod hyd_VALUE·성공 등 해당 함수의 mesur |
| -5 | dyfais_VALUE anfon_VALUE methiant_VALUE |
| -9 | 잘못되었거나 닫힌 통신 dolen_VALUE |
| -11 | 비차단 받기에서 도착한 data 없음 |
| -14 | defnyddiwr pwyntydd/ARAE_VALUE clip Gwall |
| -19 | Cymorth_VALUE NIC 없음 |
| -22 | porth_VALUE/aros_VALUE TIME_VALUE/인수 VALUE Gwall |
| -24 | 열린 Rhwydwaith_porth 4개 한도 |
| -38 | 알 수 없는 시스템 호출 |
| -90 | data 또는 수신 ARAE_VALUE Maint 문제 |
| -98 | lleol_cwmpas porth_VALUE INDEX 중복 |
| -101 | 지원하지 않는 cyrchfan_VALUE ADDRESS |
| -110 | ARP·dyfais_VALUE·수신 TIME_VALUE 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 amgodio_VALUE 있는 Java `int`의 did_VALUE 패턴을 사용하므로 상위 비트가 1인 technoleg_gwybodaeth_normal IP 주소가 음수로 보일 수 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## Gweithredu_gorchymyn 경계와 시스템 호출

```text
cragen run → JKAP에서 ELF dilysu_5fb2b747·적재 → ring 3 defnyddiwr Rhaglen_f5044b9b
                                 ↓ int 0x80
                      pwyntydd 검사 → Java cnewyllyn_VALUE API → RTL8139/UDP
                                 ↓ gadael_Rhaglen·eithriad·TIME_VALUE 초과
                                cragen 복귀
```

시스템 호출 레지스터는 `EAX=INDEX`, `EBX,ECX,EDX,ESI,EDI=인수`, `EAX=mesur`다. Java 호출 스택 ABI는 컴파일러가 defnyddiwr 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| INDEX | 호출 |
| --- | --- |
| 0 | gadael_Rhaglen(cyflwr_VALUE cod_VALUE) — Gweithredu_2/Gwall 런타임에서 사용 |
| 1 | testun_VALUE Ysgrifennu |
| 2 / 3 | 인수 eitem_COUNT / 인수 testun_VALUE ADDRESS |
| 10 | UDP Agor |
| 11 | UDP anfon(dolen_VALUE, IP, cyrchfan_VALUE porth_VALUE, ARAE_VALUE ADDRESS, hyd_VALUE) |
| 12 | UDP 받기(dolen_VALUE, ARAE_VALUE ADDRESS, 제한 밀리초) |
| 13 | UDP Cau |
| 14 | lleol_cwmpas IP ADDRESS |
| 15 / 16 | 마지막 cymar_VALUE IP / UDP porth_VALUE |
| 20 | RAM Ffeil Darllen(Enw int[] ADDRESS, Allbwn int[] ADDRESS) |
| 21 | RAM Ffeil Ysgrifennu(Enw int[] ADDRESS, 입력 int[] ADDRESS, beit_VALUE hyd_VALUE) |
| 22 | UTF-16 cod_VALUE gwers_VALUE 문자 Allbwn(0~65535) |

Ffeil API는 `defnyddiwr.파일읽기(int[] Enw, int[] data)`와 `defnyddiwr.ysgrifennu_ffeil(int[] Enw, int[] data, int hyd_VALUE)`다. 이름은 ASCII cod_VALUE ARAE_VALUE(최대 64칸, 0 gadael_Rhaglen 또는 ARAE_VALUE 끝), data eitem_elfen 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 Ffeil 없음 `-2`, pwyntydd Gwall `-14`, Enw/hyd_VALUE Gwall `-22`, Ffeil slot_VALUE 부족 `-28`, Maint 초과 `-90`을 반환한다. 쓰기는 dilysu_5fb2b747 후 Ffeil 전체를 대체한다. `defnyddiwr.ysgrifennu_nod_VALUE(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`실행권한()`은 시스템 호출이 아니라 defnyddiwr 모드에서 CS의 하위 비트를 직접 읽으므로 go_iawn_data Gweithredu_gorchymyn 권한을 확인한다. cnewyllyn_VALUE 포트 접근용 `dyfais_VALUE` native 함수는 defnyddiwr targed 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 Gweithredu_gorchymyn, 파이프, 프로세스 간 통신은 없다. Gweithredu_gorchymyn 파일은 커널의 Darllen 전용 JKAP 묶음에서 적재한다. data 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- defnyddiwr 가상 ADDRESS `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. Gweithredu_gorchymyn 영상은 앞 2MiB, 인수는 `0x04300000`부터, 스택은 영역 끝에서 시작한다. cnewyllyn_VALUE identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB defnyddiwr 영역을 비우고 Ffeil 구역을 복사해 BSS·ARAE_VALUE 영역을 초기화한다. defnyddiwr GC는 없지만 gadael_Rhaglen 후 Nesaf_eitem Gweithredu_gorchymyn 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 Dyfyniad/이스케이프 파싱은 없다.
- defnyddiwr 페이지의 cod_VALUE/data 분리 Darllen 전용 Gosodiadau, NX, 스택 guard, ASLR은 아직 없다. 커널과 defnyddiwr Cof_data·포트 hawl_VALUE 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 Gweithredu_gorchymyn 상한을 두며 TIME_VALUE 초과는 `Exit: 124`다. defnyddiwr CPU 예외는 `128 + eithriad INDEX`(페이지 Gwall 142, 특권 위반 141), Java ARAE_VALUE/계산 오류는 101~105다. cnewyllyn_VALUE 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, statig_VALUE IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP prawfswm 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- defnyddiwr Gweithredu_gorchymyn·네트워크·diogelu_VALUE 경계 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 Gweithredu_gorchymyn·technoleg_gwybodaeth_normal 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## dilysu_5fb2b747 근거

`make test`는 컴파일러 14개 시험, Java 패킷 cyflwr 2,201개 검사, 기존 cragen ELF/ISO 부팅 시험, defnyddiwr ELF/go_iawn_data UDP/diogelu_VALUE 경계 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 hyd_VALUE·해시까지 `os/build/사용자통신시험.json`에 기록한다. 시험용 손상된 ELF·특권 Gorchymyn·무한 iteriad_VALUE 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 data: [Intel 시스템 프로그래밍 명세](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 구현](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 GWYBODAETH_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
