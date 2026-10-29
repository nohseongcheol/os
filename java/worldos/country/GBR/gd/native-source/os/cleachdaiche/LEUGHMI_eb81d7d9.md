# 셸에서 실행하는 cleachdaiche 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java 개발 환경 LEUGHMI_eb81d7d9](../../문서/자바개발환경.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 gnìomhaich_àithne

òstair tèirmineal 1:

```sh
cd /home/user/jkoros
python3 os/innealan/자료되돌리기.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. 외부 연결을 받도록 방화벽이나 포트 전달을 변경하지 않는다. Ctrl+C로 종료한다.

òstair tèirmineal 2:

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

- `hello`: 독립 Java ELF 실행과 dearbh_dàta CPU cead_VALUE `ring 3`, 인수 출력.
- `netcheck`: port_VALUE 중복, 잘못된 làmhrachan_VALUE/tomhaire/faid_VALUE, 비차단 받기와 TIME_VALUE 초과 dearbh.
- `udp`: IPv4 ADDRESS·ceann_uidhe_VALUE port_VALUE·한 Word_VALUE 메시지를 받아 UDP로 보내고 같은 응답을 dearbh. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: òstair `10.0.2.2`의 지정 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. 수신 lùb_VALUE 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. 현재 주소는 게스트 `10.0.2.15/24`, 관문 `10.0.2.2`로 고정돼 있다. QEMU cleachdaiche 네트워크의 òstair inntrigeadh_cur_a_steach 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 ap_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java ap_f5044b9b 추가

`예제/내프로그램.java`를 air_adhart_nì 형식으로 만든다. 진입점은 인수 없는 `static int` 또는 `static void` 함수다. 인수는 cleachdaiche API로 조회한다.

```java
public final class 내프로그램 {
    public static int ruith() {
        cleachdaiche.sgrìobh("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/cleachdaiche/ap_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := cleachdaiche/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.ruith
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `cleachdaiche/선언/cleachdaiche.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 gnìomhaich_àithne 중인 VM에는 tog_siostam 결과가 자동 반영되지 않는다. ap_f5044b9b 이름은 현재 셸의 ASCII 입력 제한에 맞춘 1~15자의 소문자 이름이며 Java clas_VALUE·FUNCTION_VALUE·변수에는 한국어를 쓴다. 최대 32개 ap_f5044b9b, 한 gnìomhaich_àithne 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target user --entry 인사.ruith \
    -o os/build/apps/hello.elf os/cleachdaiche/선언/cleachdaiche.java os/cleachdaiche/예제/인사.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 òstair 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 taic_VALUE cliop 안에서 실행한다. `.jar`와 일반 Linux gnìomhaich_àithne 파일은 지원하지 않는다.

## cleachdaiche 네트워크 API

선언은 `선언/cleachdaiche.java`에 있다. `cuir_dàta`/`자료받기`의 `int[]` nì_eileamaid 한 개는 baidht_VALUE 하나(0~255)를 나타낸다. 한 데이터그램의 최대 dàta 길이는 1,024바이트다.

```java
int làmhrachan_VALUE = cleachdaiche.fosgail_lìonra(0); // 0: 임시 ionadail_sgòp UDP port_VALUE 자동 taghadh_VALUE
int[] dàta = new int[32];
dàta[0] = 'H'; dàta[1] = 'i';
int 보낸길이 = cleachdaiche.cuir_dàta(làmhrachan_VALUE, 0x0a000202, 9000, dàta, 2);
int RECEIVED_faid = cleachdaiche.자료받기(làmhrachan_VALUE, dàta, 1500);
cleachdaiche.dùin_lìonra(làmhrachan_VALUE);
```

dearbh_dàta 프로그램에서는 fosgail·cuir·받기의 음수 반환값을 각각 검사한다. 완성된 예제는 `예제/자료통신.java`에 있다. `자료받기`의 fuirich_VALUE 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 수신 대기열은 한 개뿐이므로 추가 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | làmhrachan_VALUE·Pròiseas_VALUE_cur_a_steach faid_VALUE·성공 등 해당 함수의 tomhas |
| -5 | uidheam_VALUE cuir_VALUE fàilligeadh_VALUE |
| -9 | 잘못되었거나 닫힌 통신 làmhrachan_VALUE |
| -11 | 비차단 받기에서 도착한 dàta 없음 |
| -14 | cleachdaiche tomhaire/ARRAY_VALUE cliop Mearachd |
| -19 | taic_VALUE NIC 없음 |
| -22 | port_VALUE/fuirich_VALUE TIME_VALUE/인수 VALUE Mearachd |
| -24 | 열린 lìonra_port 4개 한도 |
| -38 | 알 수 없는 시스템 호출 |
| -90 | dàta 또는 수신 ARRAY_VALUE atharraich_am_meud 문제 |
| -98 | ionadail_sgòp port_VALUE INDEX 중복 |
| -101 | 지원하지 않는 ceann_uidhe_VALUE ADDRESS |
| -110 | ARP·uidheam_VALUE·수신 TIME_VALUE 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 còdachadh_VALUE 있는 Java `int`의 biot_VALUE 패턴을 사용하므로 상위 비트가 1인 정상 IP 주소가 음수로 보일 수 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## gnìomhaich_àithne 경계와 시스템 호출

```text
slige run → JKAP에서 ELF dearbh_5fb2b747·적재 → ring 3 cleachdaiche ap_f5044b9b
                                 ↓ int 0x80
                      tomhaire 검사 → Java eitean_VALUE API → RTL8139/UDP
                                 ↓ fàg_ap·예외·TIME_VALUE 초과
                                slige 복귀
```

시스템 호출 레지스터는 `EAX=INDEX`, `EBX,ECX,EDX,ESI,EDI=인수`, `EAX=tomhas`다. Java 호출 스택 ABI는 컴파일러가 cleachdaiche 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| INDEX | 호출 |
| --- | --- |
| 0 | fàg_ap(cor_VALUE CODE_VALUE) — ruith/Mearachd 런타임에서 사용 |
| 1 | sreang_VALUE sgrìobh |
| 2 / 3 | 인수 nì_COUNT / 인수 sreang_VALUE ADDRESS |
| 10 | UDP fosgail |
| 11 | UDP cuir(làmhrachan_VALUE, IP, ceann_uidhe_VALUE port_VALUE, ARRAY_VALUE ADDRESS, faid_VALUE) |
| 12 | UDP 받기(làmhrachan_VALUE, ARRAY_VALUE ADDRESS, 제한 밀리초) |
| 13 | UDP dùin |
| 14 | ionadail_sgòp IP ADDRESS |
| 15 / 16 | 마지막 seise_VALUE IP / UDP port_VALUE |
| 20 | RAM faidhle 읽기(Ainm int[] ADDRESS, 출력 int[] ADDRESS) |
| 21 | RAM faidhle sgrìobh(Ainm int[] ADDRESS, 입력 int[] ADDRESS, baidht_VALUE faid_VALUE) |
| 22 | UTF-16 CODE_VALUE leasan_VALUE 문자 출력(0~65535) |

faidhle API는 `cleachdaiche.파일읽기(int[] Ainm, int[] dàta)`와 `cleachdaiche.sgrìobh_faidhle(int[] Ainm, int[] dàta, int faid_VALUE)`다. 이름은 ASCII CODE_VALUE ARRAY_VALUE(최대 64칸, 0 fàg_ap 또는 ARRAY_VALUE 끝), dàta nì_eileamaid 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 faidhle 없음 `-2`, tomhaire Mearachd `-14`, Ainm/faid_VALUE Mearachd `-22`, faidhle slot_VALUE 부족 `-28`, atharraich_am_meud 초과 `-90`을 반환한다. 쓰기는 dearbh_5fb2b747 후 faidhle 전체를 대체한다. `cleachdaiche.sgrìobh_caractar_VALUE(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`실행권한()`은 시스템 호출이 아니라 cleachdaiche 모드에서 CS의 하위 비트를 직접 읽으므로 dearbh_dàta gnìomhaich_àithne 권한을 확인한다. eitean_VALUE 포트 접근용 `uidheam_VALUE` native 함수는 cleachdaiche targaid 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 gnìomhaich_àithne, 파이프, 프로세스 간 통신은 없다. gnìomhaich_àithne 파일은 커널의 읽기 전용 JKAP 묶음에서 적재한다. dàta 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- cleachdaiche 가상 ADDRESS `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. gnìomhaich_àithne 영상은 앞 2MiB, 인수는 `0x04300000`부터, 스택은 영역 끝에서 시작한다. eitean_VALUE identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB cleachdaiche 영역을 비우고 faidhle 구역을 복사해 BSS·ARRAY_VALUE 영역을 초기화한다. cleachdaiche GC는 없지만 fàg_ap 후 air_adhart_nì gnìomhaich_àithne 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 comharran_labhairt/이스케이프 파싱은 없다.
- cleachdaiche 페이지의 CODE_VALUE/dàta 분리 읽기 전용 roghainnean, NX, 스택 guard, ASLR은 아직 없다. 커널과 cleachdaiche cuimhne_dàta·포트 cead_VALUE 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 gnìomhaich_àithne 상한을 두며 TIME_VALUE 초과는 `Exit: 124`다. cleachdaiche CPU 예외는 `128 + 예외 INDEX`(페이지 Mearachd 142, 특권 위반 141), Java ARRAY_VALUE/계산 오류는 101~105다. eitean_VALUE 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, stadaigeach_VALUE IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP 검사합 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- cleachdaiche gnìomhaich_àithne·네트워크·dìon_VALUE 경계 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 gnìomhaich_àithne·정상 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## dearbh_5fb2b747 근거

`make test`는 컴파일러 14개 시험, Java 패킷 cumha 2,201개 검사, 기존 slige ELF/ISO 부팅 시험, cleachdaiche ELF/dearbh_dàta UDP/dìon_VALUE 경계 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 faid_VALUE·해시까지 `os/build/사용자통신시험.json`에 기록한다. 시험용 손상된 ELF·특권 àithne·무한 ath_thriall_VALUE 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 dàta: [Intel 시스템 프로그래밍 명세](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 구현](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 LEUGHMI_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
