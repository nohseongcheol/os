# 셸에서 실행하는 mošomiši 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java 개발 환경 faele_ya_MPALE_eb81d7d9](../../문서/자바개발환경.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 phethagatša_taelo

go_nea_ditirelo 터미널 1:

```sh
cd /home/user/jkoros
python3 os/Ditholosi/자료되돌리기.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. 외부 연결을 받도록 방화벽이나 포트 전달을 변경하지 않는다. Ctrl+C로 종료한다.

go_nea_ditirelo 터미널 2:

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

- `hello`: 독립 Java ELF 실행과 kgonthe_data CPU tumelelo_boleng `ring 3`, 인수 출력.
- `netcheck`: phote_boleng 중복, 잘못된 tshwaro_boleng/sešupi/botelele_boleng, 비차단 받기와 시간 초과 kgonthiša.
- `udp`: IPv4 atrese·boyo_boleng phote_boleng·한 Thalokontšu_boleng 메시지를 받아 UDP로 보내고 같은 응답을 kgonthiša. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: go_nea_ditirelo `10.0.2.2`의 abela_boleng 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. 수신 ditaelopoeletšwa_boleng 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. 현재 주소는 게스트 `10.0.2.15/24`, tsela_ya_netweke_boleng `10.0.2.2`로 고정돼 있다. QEMU mošomiši 네트워크의 go_nea_ditirelo fihlelela_go_tsenya_tshedimošo 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 tirišo_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java tirišo_f5044b9b 추가

`예제/내프로그램.java`를 다음 형식으로 만든다. 진입점은 인수 없는 `static int` 또는 `static void` 함수다. 인수는 mošomiši API로 조회한다.

```java
public final class 내프로그램 {
    public static int Diriša() {
        mošomiši.Ngwala("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/mošomiši/tirišo_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := mošomiši/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.Diriša
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `mošomiši/선언/mošomiši.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 phethagatša_taelo 중인 VM에는 aga_lenaneo 결과가 자동 반영되지 않는다. tirišo_f5044b9b 이름은 현재 셸의 ASCII 입력 제한에 맞춘 1~15자의 소문자 이름이며 Java legoro_boleng_55654bf1·TIRO_boleng·변수에는 한국어를 쓴다. 최대 32개 tirišo_f5044b9b, 한 phethagatša_taelo 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target user --entry 인사.Diriša \
    -o os/build/apps/hello.elf os/mošomiši/선언/mošomiši.java os/mošomiši/예제/인사.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 go_nea_ditirelo 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 Thekgo_boleng setsopolwa 안에서 실행한다. `.jar`와 일반 Linux phethagatša_taelo 파일은 지원하지 않는다.

## mošomiši 네트워크 API

선언은 `선언/mošomiši.java`에 있다. `Romela_data`/`자료받기`의 `int[]` aetheme_elemente 한 개는 paete_boleng 하나(0~255)를 나타낸다. 한 데이터그램의 최대 data 길이는 1,024바이트다.

```java
int tshwaro_boleng = mošomiši.bula_Netweke(0); // 0: 임시 kgauswi_skoupo UDP phote_boleng 자동 kgetho_boleng
int[] data = new int[32];
data[0] = 'H'; data[1] = 'i';
int 보낸길이 = mošomiši.Romela_data(tshwaro_boleng, 0x0a000202, 9000, data, 2);
int 받은길이 = mošomiši.자료받기(tshwaro_boleng, data, 1500);
mošomiši.tswalela_Netweke(tshwaro_boleng);
```

kgonthe_data 프로그램에서는 Bula·Romela·받기의 음수 반환값을 각각 검사한다. 완성된 예제는 `예제/자료통신.java`에 있다. `자료받기`의 대기 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 수신 대기열은 한 개뿐이므로 추가 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | tshwaro_boleng·tiragalo_boleng_go_tsenya_tshedimošo botelele_boleng·성공 등 해당 함수의 결과 |
| -5 | sedirišwa_boleng Romela_boleng go_palelwa_boleng |
| -9 | 잘못되었거나 닫힌 통신 tshwaro_boleng |
| -11 | 비차단 받기에서 도착한 data 없음 |
| -14 | mošomiši sešupi/arei_boleng setsopolwa Phošo |
| -19 | Thekgo_boleng NIC 없음 |
| -22 | phote_boleng/대기 시간/인수 boleng Phošo |
| -24 | 열린 Netweke_phote 4개 한도 |
| -38 | 알 수 없는 시스템 호출 |
| -90 | data 또는 수신 arei_boleng Bogolo 문제 |
| -98 | kgauswi_skoupo phote_boleng lokela 중복 |
| -101 | 지원하지 않는 boyo_boleng atrese |
| -110 | ARP·sedirišwa_boleng·수신 시간 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 go_enkhouta_boleng 있는 Java `int`의 paente_boleng 패턴을 사용하므로 상위 비트가 1인 정상 IP 주소가 음수로 보일 수 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## phethagatša_taelo 경계와 시스템 호출

```text
šele run → JKAP에서 ELF kgonthiša_5fb2b747·적재 → ring 3 mošomiši tirišo_f5044b9b
                                 ↓ int 0x80
                      sešupi 검사 → Java khenele_boleng API → RTL8139/UDP
                                 ↓ Etšwa_tirišo·예외·시간 초과
                                šele 복귀
```

시스템 호출 레지스터는 `EAX=lokela`, `EBX,ECX,EDX,ESI,EDI=인수`, `EAX=결과`다. Java 호출 스택 ABI는 컴파일러가 mošomiši 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| lokela | 호출 |
| --- | --- |
| 0 | Etšwa_tirišo(boemo_boleng 코드) — Diriša/Phošo 런타임에서 사용 |
| 1 | molokoloko_boleng Ngwala |
| 2 / 3 | 인수 개수 / 인수 molokoloko_boleng atrese |
| 10 | UDP Bula |
| 11 | UDP Romela(tshwaro_boleng, IP, boyo_boleng phote_boleng, arei_boleng atrese, botelele_boleng) |
| 12 | UDP 받기(tshwaro_boleng, arei_boleng atrese, 제한 밀리초) |
| 13 | UDP Tswalela |
| 14 | kgauswi_skoupo IP atrese |
| 15 / 16 | 마지막 sedirišwa_sa_legoro_le_tee_boleng IP / UDP phote_boleng |
| 20 | RAM Faele Bala(Leina int[] atrese, 출력 int[] atrese) |
| 21 | RAM Faele Ngwala(Leina int[] atrese, 입력 int[] atrese, paete_boleng botelele_boleng) |
| 22 | UTF-16 코드 thutišo_boleng 문자 출력(0~65535) |

Faele API는 `mošomiši.파일읽기(int[] Leina, int[] data)`와 `mošomiši.ngwala_faele(int[] Leina, int[] data, int botelele_boleng)`다. 이름은 ASCII 코드 arei_boleng(최대 64칸, 0 Etšwa_tirišo 또는 arei_boleng 끝), data aetheme_elemente 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 Faele 없음 `-2`, sešupi Phošo `-14`, Leina/botelele_boleng Phošo `-22`, Faele sekgobana_boleng 부족 `-28`, Bogolo 초과 `-90`을 반환한다. 쓰기는 kgonthiša_5fb2b747 후 Faele 전체를 대체한다. `mošomiši.ngwala_tlhaka_boleng(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`실행권한()`은 시스템 호출이 아니라 mošomiši 모드에서 CS의 하위 비트를 직접 읽으므로 kgonthe_data phethagatša_taelo 권한을 확인한다. khenele_boleng 포트 접근용 `sedirišwa_boleng` native 함수는 mošomiši nepo 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 phethagatša_taelo, 파이프, 프로세스 간 통신은 없다. phethagatša_taelo 파일은 커널의 Bala 전용 JKAP 묶음에서 적재한다. data 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- mošomiši 가상 atrese `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. phethagatša_taelo 영상은 앞 2MiB, 인수는 `0x04300000`부터, 스택은 영역 끝에서 시작한다. khenele_boleng identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB mošomiši 영역을 비우고 Faele 구역을 복사해 BSS·arei_boleng 영역을 초기화한다. mošomiši GC는 없지만 Etšwa_tirišo 후 다음 phethagatša_taelo 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 따옴표/이스케이프 파싱은 없다.
- mošomiši 페이지의 코드/data 분리 Bala 전용 Dipeakanyo, NX, 스택 guard, ASLR은 아직 없다. 커널과 mošomiši memori_data·포트 tumelelo_boleng 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 phethagatša_taelo 상한을 두며 시간 초과는 `Exit: 124`다. mošomiši CPU 예외는 `128 + 예외 lokela`(페이지 Phošo 142, 특권 위반 141), Java arei_boleng/계산 오류는 101~105다. khenele_boleng 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, ya_go_se_fetoge_boleng_f430d3f5 IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP 검사합 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- mošomiši phethagatša_taelo·네트워크·šireletša_boleng 경계 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 phethagatša_taelo·정상 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## kgonthiša_5fb2b747 근거

`make test`는 컴파일러 14개 시험, Java 패킷 seemo 2,201개 검사, 기존 šele ELF/ISO 부팅 시험, mošomiši ELF/kgonthe_data UDP/šireletša_boleng 경계 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 botelele_boleng·해시까지 `os/build/사용자통신시험.json`에 기록한다. 시험용 손상된 ELF·특권 Taelo·무한 poeletšo_boleng 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 data: [Intel 시스템 프로그래밍 명세](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 구현](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 faele_ya_MPALE_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
