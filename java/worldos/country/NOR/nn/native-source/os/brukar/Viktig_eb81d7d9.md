# 셸에서 실행하는 brukar 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java 개발 환경 Viktig_eb81d7d9](../../문서/자바개발환경.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 Utfør_kommando

vert Terminal 1:

```sh
cd /home/user/jkoros
python3 os/Verktøy/자료되돌리기.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. ekstern_VALUE 연결을 받도록 방화벽이나 포트 전달을 변경하지 않는다. Ctrl+C로 종료한다.

vert Terminal 2:

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

- `hello`: 독립 Java ELF 실행과 faktisk_data CPU løyve_VALUE `ring 3`, Argument Utdata.
- `netcheck`: port_VALUE 중복, 잘못된 handtak_VALUE/peikar/lengd_VALUE, 비차단 받기와 TIME_VALUE 초과 stadfeste.
- `udp`: IPv4 ADDRESS·mål_VALUE port_VALUE·한 Word_VALUE 메시지를 받아 UDP로 보내고 같은 응답을 stadfeste. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: vert `10.0.2.2`의 Tilordne_VALUE 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. 수신 Loop_VALUE 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. betalt_vare 주소는 게스트 `10.0.2.15/24`, gateway_VALUE `10.0.2.2`로 고정돼 있다. QEMU brukar 네트워크의 vert tilgang_oppføring 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 app_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java app_f5044b9b 추가

`예제/내프로그램.java`를 Neste_vare 형식으로 만든다. 진입점은 Argument 없는 `static int` 또는 `static void` 함수다. 인수는 brukar API로 조회한다.

```java
public final class 내프로그램 {
    public static int Køyr_2() {
        brukar.Skriv("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/brukar/app_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := brukar/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.Køyr_2
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `brukar/erklæring/brukar.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 Utfør_kommando 중인 VM에는 bygg_system 결과가 자동 반영되지 않는다. app_f5044b9b 이름은 betalt_vare 셸의 ASCII 입력 제한에 맞춘 1~15자의 소문자 이름이며 Java time_VALUE·FUNCTION_VALUE·변수에는 한국어를 쓴다. 최대 32개 app_f5044b9b, 한 Utfør_kommando 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target user --entry 인사.Køyr_2 \
    -o os/build/apps/hello.elf os/brukar/erklæring/brukar.java os/brukar/예제/인사.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 vert 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 støtte_VALUE klipp 안에서 실행한다. `.jar`와 일반 Linux Utfør_kommando 파일은 지원하지 않는다.

## brukar 네트워크 API

선언은 `erklæring/brukar.java`에 있다. `sende_data`/`자료받기`의 `int[]` vare_element 한 개는 byte_VALUE 하나(0~255)를 나타낸다. 한 데이터그램의 최대 data 길이는 1,024바이트다.

```java
int handtak_VALUE = brukar.opne_Nettverk(0); // 0: 임시 lokal_område UDP port_VALUE 자동 merkt_område_VALUE
int[] data = new int[32];
data[0] = 'H'; data[1] = 'i';
int 보낸길이 = brukar.sende_data(handtak_VALUE, 0x0a000202, 9000, data, 2);
int RECEIVED_lengd = brukar.자료받기(handtak_VALUE, data, 1500);
brukar.Lukk_Nettverk(handtak_VALUE);
```

faktisk_data 프로그램에서는 Opna·sende·받기의 음수 반환값을 각각 검사한다. 완성된 예제는 `예제/자료통신.java`에 있다. `자료받기`의 vent_VALUE 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 수신 대기열은 한 개뿐이므로 추가 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | handtak_VALUE·Prosess_VALUE_oppføring lengd_VALUE·성공 등 해당 함수의 forretningsmål |
| -5 | mobil_VALUE sende_VALUE_f993dacd feil_VALUE |
| -9 | 잘못되었거나 닫힌 통신 handtak_VALUE |
| -11 | 비차단 받기에서 도착한 data 없음 |
| -14 | brukar peikar/ARRAY_VALUE klipp FEIL |
| -19 | støtte_VALUE NIC 없음 |
| -22 | port_VALUE/vent_VALUE TIME_VALUE/Argument VALUE FEIL |
| -24 | 열린 Nettverk_port 4개 한도 |
| -38 | 알 수 없는 시스템 호출 |
| -90 | data 또는 수신 ARRAY_VALUE Storleik 문제 |
| -98 | lokal_område port_VALUE INDEX 중복 |
| -101 | 지원하지 않는 mål_VALUE ADDRESS |
| -110 | ARP·mobil_VALUE·수신 TIME_VALUE 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 koding_VALUE 있는 Java `int`의 bit_VALUE 패턴을 사용하므로 상위 비트가 1인 informasjonsteknologi_normal IP 주소가 음수로 보일 수 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## Utfør_kommando 경계와 시스템 호출

```text
grensesnitt run → JKAP에서 ELF bekrefte·적재 → ring 3 brukar app_f5044b9b
                                 ↓ int 0x80
                      peikar 검사 → Java kjerne_VALUE API → RTL8139/UDP
                                 ↓ Utgang_app·unntak·TIME_VALUE 초과
                                grensesnitt 복귀
```

시스템 호출 레지스터는 `EAX=INDEX`, `EBX,ECX,EDX,ESI,EDI=Argument`, `EAX=forretningsmål`다. Java 호출 스택 ABI는 컴파일러가 brukar 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| INDEX | 호출 |
| --- | --- |
| 0 | Utgang_app(status_VALUE CODE_VALUE) — Køyr_2/FEIL 런타임에서 사용 |
| 1 | streng_VALUE Skriv |
| 2 / 3 | Argument vare_COUNT / Argument streng_VALUE ADDRESS |
| 10 | UDP Opna |
| 11 | UDP sende(handtak_VALUE, IP, mål_VALUE port_VALUE, ARRAY_VALUE ADDRESS, lengd_VALUE) |
| 12 | UDP 받기(handtak_VALUE, ARRAY_VALUE ADDRESS, 제한 밀리초) |
| 13 | UDP Lukk |
| 14 | lokal_område IP ADDRESS |
| 15 / 16 | 마지막 node_VALUE_6a3b6fa7 IP / UDP port_VALUE |
| 20 | RAM Fil Les(Namn int[] ADDRESS, Utdata int[] ADDRESS) |
| 21 | RAM Fil Skriv(Namn int[] ADDRESS, 입력 int[] ADDRESS, byte_VALUE lengd_VALUE) |
| 22 | UTF-16 CODE_VALUE leksjon_VALUE 문자 Utdata(0~65535) |

Fil API는 `brukar.파일읽기(int[] Namn, int[] data)`와 `brukar.skrive_fil(int[] Namn, int[] data, int lengd_VALUE)`다. 이름은 ASCII CODE_VALUE ARRAY_VALUE(최대 64칸, 0 Utgang_app 또는 ARRAY_VALUE 끝), data vare_element 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 Fil 없음 `-2`, peikar FEIL `-14`, Namn/lengd_VALUE FEIL `-22`, Fil felt_VALUE 부족 `-28`, Storleik 초과 `-90`을 반환한다. 쓰기는 bekrefte 후 Fil 전체를 대체한다. `brukar.skrive_teikn_VALUE(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`실행권한()`은 시스템 호출이 아니라 brukar 모드에서 CS의 하위 비트를 직접 읽으므로 faktisk_data Utfør_kommando 권한을 확인한다. kjerne_VALUE 포트 접근용 `mobil_VALUE` native 함수는 brukar mål 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 Utfør_kommando, 파이프, 프로세스 간 통신은 없다. Utfør_kommando 파일은 커널의 Les 전용 JKAP 묶음에서 적재한다. data 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- brukar 가상 ADDRESS `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. Utfør_kommando 영상은 앞 2MiB, 인수는 `0x04300000`부터, 스택은 영역 끝에서 시작한다. kjerne_VALUE identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB brukar 영역을 비우고 Fil 구역을 복사해 BSS·ARRAY_VALUE 영역을 초기화한다. brukar GC는 없지만 Utgang_app 후 Neste_vare Utfør_kommando 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 Sitat/이스케이프 파싱은 없다.
- brukar 페이지의 CODE_VALUE/data 분리 Les 전용 Innstillingar, NX, 스택 guard, ASLR은 아직 없다. 커널과 brukar Minne_data·포트 løyve_VALUE 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 Utfør_kommando 상한을 두며 TIME_VALUE 초과는 `Exit: 124`다. brukar CPU 예외는 `128 + unntak INDEX`(페이지 FEIL 142, 특권 위반 141), Java ARRAY_VALUE/계산 오류는 101~105다. kjerne_VALUE 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, statisk_VALUE IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP kontrollsum 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- brukar Utfør_kommando·네트워크·verne_VALUE 경계 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 Utfør_kommando·informasjonsteknologi_normal 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## bekrefte 근거

`make test`는 컴파일러 14개 시험, Java 패킷 tilstand 2,201개 검사, 기존 grensesnitt ELF/ISO 부팅 시험, brukar ELF/faktisk_data UDP/verne_VALUE 경계 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 lengd_VALUE·해시까지 `os/build/사용자통신시험.json`에 기록한다. 시험용 손상된 ELF·특권 Kommando·무한 gjentaking_VALUE 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 data: [Intel 시스템 프로그래밍 명세](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 구현](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 Viktig_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
