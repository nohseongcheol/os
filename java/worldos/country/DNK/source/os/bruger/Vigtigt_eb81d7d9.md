# 셸에서 실행하는 bruger 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java udvikling miljø Vigtigt_eb81d7d9](../../문서/Java_IDE.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 Udfør_kommando

vært Terminal 1:

```sh
cd /home/user/jkoros
python3 os/Værktøjer/ekko_data.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. ekstern_VÆRDI 연결을 받도록 방화벽이나 hardware_port 전달을 변경하지 않는다. Ctrl+C로 종료한다.

vært Terminal 2:

```sh
cd /home/user/jkoros
make run
```

게스트의 `jkoros>` 프롬프트에 input_VÆRDI:

```text
apps
run hello first second
net
run netcheck
run udp 10.0.2.2 9000 hello
run stress 9000
```

- `hello`: 독립 Java ELF 실행과 faktisk_data CPU rettighed_VÆRDI `ring 3`, Argumenter Udgang.
- `netcheck`: port_VÆRDI 중복, 잘못된 handle_VÆRDI/markør/varighed_VÆRDI, 비차단 받기와 TID_VÆRDI 초과 bekræfte.
- `udp`: IPv4 mail·destination_VÆRDI port_VÆRDI·한 Ord_VÆRDI 메시지를 받아 UDP로 보내고 같은 응답을 bekræfte. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: vært `10.0.2.2`의 Tildel_VÆRDI 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. modtage_VÆRDI Loop_VÆRDI 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. aktuel_vare 주소는 게스트 `10.0.2.15/24`, gateway_VÆRDI `10.0.2.2`로 고정돼 있다. QEMU bruger 네트워크의 vært åbne_post 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 app_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java app_f5044b9b tilføj_post

`예제/내프로그램.java`를 Næste_vare 형식으로 만든다. 진입점은 Argumenter 없는 `static int` 또는 `static void` 함수다. 인수는 bruger API로 조회한다.

```java
public final class 내프로그램 {
    public static int Kør_2() {
        bruger.Skrive("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/bruger/app_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := bruger/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.Kør_2
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `bruger/erklæring/bruger.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 Udfør_kommando 중인 VM에는 build_System 결과가 자동 반영되지 않는다. app_f5044b9b 이름은 aktuel_vare 셸의 ASCII input_VÆRDI 제한에 맞춘 1~15자의 소문자 이름이며 Java Hold_VÆRDI·FUNKTION_VÆRDI·변수에는 한국어를 쓴다. 최대 32개 app_f5044b9b, 한 Udfør_kommando 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/compiler.py --target user --entry 인사.Kør_2 \
    -o os/build/apps/hello.elf os/bruger/erklæring/bruger.java os/bruger/예제/인사.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 vært 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 støtte_VÆRDI klippe 안에서 실행한다. `.jar`와 일반 Linux Udfør_kommando 파일은 지원하지 않는다.

## bruger 네트워크 API

선언은 `erklæring/bruger.java`에 있다. `maile_data`/`modtage_data`의 `int[]` vare_element 한 개는 byte_VÆRDI 하나(0~255)를 나타낸다. 한 데이터그램의 최대 data 길이는 1,024바이트다.

```java
int handle_VÆRDI = bruger.åben_netværk(0); // 0: 임시 lokal_Omfang UDP port_VÆRDI 자동 markering_VÆRDI
int[] data = new int[32];
data[0] = 'H'; data[1] = 'i';
int 보낸길이 = bruger.maile_data(handle_VÆRDI, 0x0a000202, 9000, data, 2);
int MODTAGET_VED_UDLØB_varighed = bruger.modtage_data(handle_VÆRDI, data, 1500);
bruger.Luk_netværk(handle_VÆRDI);
```

faktisk_data 프로그램에서는 Åbn·maile·받기의 음수 반환값을 각각 검사한다. 완성된 예제는 `예제/자료통신.java`에 있다. `modtage_data`의 vent_VÆRDI 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 modtage_VÆRDI 대기열은 한 개뿐이므로 tilføj_post 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | handle_VÆRDI·Proces_VÆRDI_post varighed_VÆRDI·성공 등 해당 함수의 KR |
| -5 | enhed_VÆRDI maile_VÆRDI fejl_VÆRDI |
| -9 | 잘못되었거나 닫힌 통신 handle_VÆRDI |
| -11 | 비차단 받기에서 도착한 data 없음 |
| -14 | bruger markør/MATRIX_VÆRDI klippe fejl |
| -19 | støtte_VÆRDI NIC 없음 |
| -22 | port_VÆRDI/vent_VÆRDI TID_VÆRDI/Argumenter VÆRDI fejl |
| -24 | 열린 netværk_port 4개 한도 |
| -38 | 알 tal 없는 시스템 호출 |
| -90 | data 또는 modtage_VÆRDI MATRIX_VÆRDI Størrelse 문제 |
| -98 | lokal_Omfang port_VÆRDI INDEKS 중복 |
| -101 | 지원하지 않는 destination_VÆRDI mail |
| -110 | ARP·enhed_VÆRDI·modtage_VÆRDI TID_VÆRDI 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 kodning_VÆRDI 있는 Java `int`의 bit_VÆRDI 패턴을 사용하므로 상위 비트가 1인 it_normal IP 주소가 음수로 보일 tal 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## Udfør_kommando 경계와 시스템 호출

```text
Shell run → JKAP에서 ELF bekræfte_5fb2b747·적재 → ring 3 bruger app_f5044b9b
                                 ↓ int 0x80
                      markør 검사 → Java kerne_VÆRDI API → RTL8139/UDP
                                 ↓ Afslut_app·undtagelse·TID_VÆRDI 초과
                                Shell 복귀
```

시스템 호출 레지스터는 `EAX=INDEKS`, `EBX,ECX,EDX,ESI,EDI=Argumenter`, `EAX=KR`다. Java 호출 operand_Stak ABI는 컴파일러가 bruger 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| INDEKS | 호출 |
| --- | --- |
| 0 | Afslut_app(status_VÆRDI KODE_VÆRDI) — Kør_2/fejl 런타임에서 brug_VÆRDI |
| 1 | streng_VÆRDI Skrive |
| 2 / 3 | Argumenter vare_TÆL / Argumenter streng_VÆRDI mail |
| 10 | UDP Åbn |
| 11 | UDP maile(handle_VÆRDI, IP, destination_VÆRDI port_VÆRDI, MATRIX_VÆRDI mail, varighed_VÆRDI) |
| 12 | UDP modtage(handle_VÆRDI, MATRIX_VÆRDI mail, 제한 밀리초) |
| 13 | UDP Luk |
| 14 | lokal_Omfang IP mail |
| 15 / 16 | 마지막 peer_VÆRDI IP / UDP port_VÆRDI |
| 20 | RAM Fil Læse(Navn int[] mail, Udgang int[] mail) |
| 21 | RAM Fil Skrive(Navn int[] mail, input_VÆRDI int[] mail, byte_VÆRDI varighed_VÆRDI) |
| 22 | UTF-16 KODE_VÆRDI enhed_VÆRDI_7c611f50 문자 Udgang(0~65535) |

Fil API는 `bruger.파일읽기(int[] Navn, int[] data)`와 `bruger.skrive_fil(int[] Navn, int[] data, int varighed_VÆRDI)`다. 이름은 ASCII KODE_VÆRDI MATRIX_VÆRDI(최대 64칸, 0 Afslut_app 또는 MATRIX_VÆRDI 끝), data vare_element 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 Fil 없음 `-2`, markør fejl `-14`, Navn/varighed_VÆRDI fejl `-22`, Fil udvidelsesstik_VÆRDI 부족 `-28`, Størrelse 초과 `-90`을 반환한다. 쓰기는 bekræfte_5fb2b747 후 Fil 전체를 대체한다. `bruger.skrive_tegn_VÆRDI(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`udførelse_rettighed()`은 시스템 호출이 아니라 bruger 모드에서 CS의 하위 비트를 직접 읽으므로 faktisk_data Udfør_kommando 권한을 확인한다. kerne_VÆRDI hardware_port 접근용 `enhed_VÆRDI` native 함수는 bruger mål 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 Udfør_kommando, 파이프, 프로세스 간 통신은 없다. Udfør_kommando 파일은 커널의 Læse 전용 JKAP 묶음에서 적재한다. data 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- bruger 가상 mail `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. Udfør_kommando 영상은 frontvendt_VÆRDI 2MiB, 인수는 `0x04300000`부터, 스택은 område_VÆRDI_0e9a97ab 끝에서 시작한다. kerne_VÆRDI identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB bruger 영역을 비우고 Fil 구역을 복사해 BSS·MATRIX_VÆRDI 영역을 초기화한다. bruger GC는 없지만 Afslut_app 후 Næste_vare Udfør_kommando 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 Citat/이스케이프 파싱은 없다.
- bruger 페이지의 KODE_VÆRDI/data 분리 Læse 전용 Indstillinger, NX, operand_Stak guard, ASLR은 아직 없다. 커널과 bruger Hukommelse_data·hardware_port rettighed_VÆRDI 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 Udfør_kommando 상한을 두며 TID_VÆRDI 초과는 `Exit: 124`다. bruger CPU 예외는 `128 + undtagelse INDEKS`(페이지 fejl 142, 특권 위반 141), Java MATRIX_VÆRDI/계산 오류는 101~105다. kerne_VÆRDI 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, statisk_VÆRDI IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP kontrolsum 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- bruger Udfør_kommando·네트워크·beskytte_VÆRDI grænse_VÆRDI 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 Udfør_kommando·it_normal 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## bekræfte_5fb2b747 근거

`make test`는 compiler 14개 시험, Java 패킷 lidelse 2,201개 검사, 기존 Shell ELF/ISO 부팅 시험, bruger ELF/faktisk_data UDP/beskytte_VÆRDI grænse_VÆRDI 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 varighed_VÆRDI·해시까지 `os/build/test_bruger_netværk.json`에 기록한다. 시험용 손상된 ELF·특권 Kommando·무한 sprint_VÆRDI 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 data: [Intel 시스템 프로그래밍 명세](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 구현](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 Vigtigt_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
