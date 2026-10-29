# 셸에서 실행하는 användarutrymme 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java utveckling miljö VIKTIGT_eb81d7d9](../../문서/Java_IDE.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 köra_kommando

värd kommandotolk 1:

```sh
cd /home/user/jkoros
python3 os/verktyg/UppdateraSkärm_data.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. extern_värde 연결을 받도록 방화벽이나 maskinvara_port 전달을 변경하지 않는다. Ctrl+C로 종료한다.

värd kommandotolk 2:

```sh
cd /home/user/jkoros
make run
```

게스트의 `jkoros>` 프롬프트에 indata_värde:

```text
apps
run hello first second
net
run netcheck
run udp 10.0.2.2 9000 hello
run stress 9000
```

- `hello`: 독립 Java ELF 실행과 verklig_data CPU behörighet_värde `ring 3`, argument utmatningsposition.
- `netcheck`: port_värde 중복, 잘못된 handtag_värde/markör/längd_värde, 비차단 받기와 tid_värde 초과 verifiera.
- `udp`: IPv4 Adress·mål_värde port_värde·한 Ord_värde 메시지를 받아 UDP로 보내고 같은 응답을 verifiera. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: värd `10.0.2.2`의 Tilldela_värde 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. få_värde Loop_värde 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. aktuellt_objekt 주소는 게스트 `10.0.2.15/24`, gateway_värde `10.0.2.2`로 고정돼 있다. QEMU användarutrymme 네트워크의 värd ansluta_post 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 app_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java app_f5044b9b Lägga_till_post

`예제/내프로그램.java`를 Nästa_objekt 형식으로 만든다. 진입점은 argument 없는 `static int` 또는 `static void` 함수다. 인수는 användarutrymme API로 조회한다.

```java
public final class 내프로그램 {
    public static int Kör() {
        användarutrymme.Skriv("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/användarutrymme/app_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := användarutrymme/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.Kör
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `användarutrymme/deklaration/användarutrymme.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 köra_kommando 중인 VM에는 version_System 결과가 자동 반영되지 않는다. app_f5044b9b 이름은 aktuellt_objekt 셸의 ASCII indata_värde 제한에 맞춘 1~15자의 소문자 이름이며 Java Kurs_värde·FUNKTION_värde·변수에는 한국어를 쓴다. 최대 32개 app_f5044b9b, 한 köra_kommando 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/kompilerare.py --target user --entry 인사.Kör \
    -o os/build/apps/hello.elf os/användarutrymme/deklaration/användarutrymme.java os/användarutrymme/예제/인사.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 värd 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 stöd_värde klipp 안에서 실행한다. `.jar`와 일반 Linux köra_kommando 파일은 지원하지 않는다.

## användarutrymme 네트워크 API

선언은 `deklaration/användarutrymme.java`에 있다. `skicka_data`/`få_data`의 `int[]` objekt_element 한 개는 byte_värde 하나(0~255)를 나타낸다. 한 데이터그램의 최대 data 길이는 1,024바이트다.

```java
int handtag_värde = användarutrymme.skapa_nätverk(0); // 0: 임시 lokal_scope UDP port_värde 자동 markering_värde
int[] data = new int[32];
data[0] = 'H'; data[1] = 'i';
int 보낸길이 = användarutrymme.skicka_data(handtag_värde, 0x0a000202, 9000, data, 2);
int BELOPP_längd = användarutrymme.få_data(handtag_värde, data, 1500);
användarutrymme.Stäng_nätverk(handtag_värde);
```

verklig_data 프로그램에서는 Öppna·skicka·받기의 음수 반환값을 각각 검사한다. 완성된 예제는 `예제/data_kommunikation.java`에 있다. `få_data`의 vänta_värde 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 få_värde 대기열은 한 개뿐이므로 Lägga_till_post 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | handtag_värde·Process_värde_post längd_värde·성공 등 해당 함수의 RESULTAT |
| -5 | enhet_värde skicka_värde_f993dacd fel_värde |
| -9 | 잘못되었거나 닫힌 kommunikation handtag_värde |
| -11 | 비차단 받기에서 도착한 data 없음 |
| -14 | användarutrymme markör/MATRIS_värde klipp fel |
| -19 | stöd_värde NIC 없음 |
| -22 | port_värde/vänta_värde tid_värde/argument värde fel |
| -24 | 열린 nätverk_port 4개 한도 |
| -38 | 알 nummer 없는 시스템 호출 |
| -90 | data 또는 få_värde MATRIS_värde Storlek 문제 |
| -98 | lokal_scope port_värde INDEX 중복 |
| -101 | 지원하지 않는 mål_värde Adress |
| -110 | ARP·enhet_värde·få_värde tid_värde 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 kodning_värde 있는 Java `int`의 bit_värde 패턴을 사용하므로 상위 비트가 1인 informationsteknik_normal IP 주소가 음수로 보일 nummer 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## köra_kommando 경계와 시스템 호출

```text
Shell run → JKAP에서 ELF validera·적재 → ring 3 användarutrymme app_f5044b9b
                                 ↓ int 0x80
                      markör 검사 → Java kärna_värde API → RTL8139/UDP
                                 ↓ Utgång_app·fel_31f743d2·tid_värde 초과
                                Shell 복귀
```

시스템 호출 레지스터는 `EAX=INDEX`, `EBX,ECX,EDX,ESI,EDI=argument`, `EAX=RESULTAT`다. Java 호출 operand_Stack ABI는 컴파일러가 användarutrymme 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| INDEX | 호출 |
| --- | --- |
| 0 | Utgång_app(status_värde KOD_värde) — Kör/fel 런타임에서 använda_värde |
| 1 | sträng_värde Skriv |
| 2 / 3 | argument objekt_ANTAL / argument sträng_värde Adress |
| 10 | UDP Öppna |
| 11 | UDP skicka(handtag_värde, IP, mål_värde port_värde, MATRIS_värde Adress, längd_värde) |
| 12 | UDP få(handtag_värde, MATRIS_värde Adress, 제한 밀리초) |
| 13 | UDP Stäng |
| 14 | lokal_scope IP Adress |
| 15 / 16 | 마지막 peer_värde IP / UDP port_värde |
| 20 | RAM filnamn Läs(Namn int[] Adress, utmatningsposition int[] Adress) |
| 21 | RAM filnamn Skriv(Namn int[] Adress, indata_värde int[] Adress, byte_värde längd_värde) |
| 22 | UTF-16 KOD_värde enhet_värde_7c611f50 문자 utmatningsposition(0~65535) |

filnamn API는 `användarutrymme.läsa_fil(int[] Namn, int[] data)`와 `användarutrymme.skriva_fil(int[] Namn, int[] data, int längd_värde)`다. 이름은 ASCII KOD_värde MATRIS_värde(최대 64칸, 0 Utgång_app 또는 MATRIS_värde 끝), data objekt_element 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 filnamn 없음 `-2`, markör fel `-14`, Namn/längd_värde fel `-22`, filnamn fack_värde 부족 `-28`, Storlek 초과 `-90`을 반환한다. 쓰기는 validera 후 filnamn 전체를 대체한다. `användarutrymme.skriva_tecken_värde(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`körning_behörighet()`은 시스템 호출이 아니라 användarutrymme 모드에서 CS의 하위 비트를 직접 읽으므로 verklig_data köra_kommando 권한을 확인한다. kärna_värde maskinvara_port 접근용 `enhet_värde` native 함수는 användarutrymme mål 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 köra_kommando, 파이프, 프로세스 간 통신은 없다. köra_kommando 파일은 커널의 Läs 전용 JKAP 묶음에서 적재한다. data 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- användarutrymme 가상 Adress `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. köra_kommando 영상은 framåtvänd_värde 2MiB, 인수는 `0x04300000`부터, 스택은 område_värde_0e9a97ab 끝에서 시작한다. kärna_värde identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB användarutrymme 영역을 비우고 filnamn 구역을 복사해 BSS·MATRIS_värde 영역을 초기화한다. användarutrymme GC는 없지만 Utgång_app 후 Nästa_objekt köra_kommando 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 Citat/이스케이프 파싱은 없다.
- användarutrymme 페이지의 KOD_värde/data 분리 Läs 전용 Inställningar, NX, operand_Stack guard, ASLR은 아직 없다. 커널과 användarutrymme Minne_data·maskinvara_port behörighet_värde 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 köra_kommando 상한을 두며 tid_värde 초과는 `Exit: 124`다. användarutrymme CPU 예외는 `128 + fel_31f743d2 INDEX`(페이지 fel 142, 특권 위반 141), Java MATRIS_värde/계산 오류는 101~105다. kärna_värde 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, statisk_värde IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP kontrollsumma 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- användarutrymme köra_kommando·네트워크·skydda_värde gräns_värde 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 köra_kommando·informationsteknik_normal 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## validera 근거

`make test`는 kompilerare 14개 tester, Java 패킷 villkor 2,201개 검사, 기존 Shell ELF/ISO maskinstart tester, användarutrymme ELF/verklig_data UDP/skydda_värde gräns_värde 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 längd_värde·해시까지 `os/build/test_användare_nätverk.json`에 기록한다. 시험용 손상된 ELF·특권 kommando·무한 sprint_värde 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 data: [Intel 시스템 프로그래밍 명세](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 implementation](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 VIKTIGT_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
