# 셸에서 실행하는 përdorues 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java 개발 환경 LEXOMË_eb81d7d9](../../문서/자바개발환경.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 zbatoj_komandë

pritës Terminali 1:

```sh
cd /home/user/jkoros
python3 os/Mjete/자료되돌리기.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. 외부 연결을 받도록 방화벽이나 포트 전달을 변경하지 않는다. Ctrl+C로 종료한다.

pritës Terminali 2:

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

- `hello`: 독립 Java ELF 실행과 aktual_të_dhëna CPU leje_VALUE `ring 3`, Argumente 출력.
- `netcheck`: portë_VALUE 중복, 잘못된 dorezë_VALUE/tregues/gjatësi_VALUE, 비차단 받기와 Ora_VALUE_4692cef5 초과 verifikoj.
- `udp`: IPv4 email·vendmbërritje_VALUE portë_VALUE·한 Word_VALUE 메시지를 받아 UDP로 보내고 같은 응답을 verifikoj. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: pritës `10.0.2.2`의 cakto_VALUE 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. 수신 Loop_VALUE 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. 현재 주소는 게스트 `10.0.2.15/24`, portëkalimi_VALUE `10.0.2.2`로 고정돼 있다. QEMU përdorues 네트워크의 pritës qasem_futje 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 program_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java program_f5044b9b 추가

`예제/내프로그램.java`를 Tjetër_njësi 형식으로 만든다. 진입점은 Argumente 없는 `static int` 또는 `static void` 함수다. 인수는 përdorues API로 조회한다.

```java
public final class 내프로그램 {
    public static int Ekzekuto() {
        përdorues.Shkrimi("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/përdorues/program_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := përdorues/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.Ekzekuto
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `përdorues/deklarata/përdorues.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 zbatoj_komandë 중인 VM에는 ndërtoj_sistem 결과가 자동 반영되지 않는다. program_f5044b9b 이름은 현재 셸의 ASCII 입력 제한에 맞춘 1~15자의 소문자 이름이며 Java klasë_VALUE·FUNCTION_VALUE·변수에는 한국어를 쓴다. 최대 32개 program_f5044b9b, 한 zbatoj_komandë 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target user --entry 인사.Ekzekuto \
    -o os/build/apps/hello.elf os/përdorues/deklarata/përdorues.java os/përdorues/예제/인사.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 pritës 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 Mbështetje_VALUE fragment 안에서 실행한다. `.jar`와 일반 Linux zbatoj_komandë 파일은 지원하지 않는다.

## përdorues 네트워크 API

선언은 `deklarata/përdorues.java`에 있다. `dërgoj_të_dhëna`/`자료받기`의 `int[]` njësi_element 한 개는 bajt_VALUE 하나(0~255)를 나타낸다. 한 데이터그램의 최대 të_dhëna 길이는 1,024바이트다.

```java
int dorezë_VALUE = përdorues.hap_rrjet(0); // 0: 임시 lokal_fushë UDP portë_VALUE 자동 përzgjedhje_VALUE
int[] të_dhëna = new int[32];
të_dhëna[0] = 'H'; të_dhëna[1] = 'i';
int 보낸길이 = përdorues.dërgoj_të_dhëna(dorezë_VALUE, 0x0a000202, 9000, të_dhëna, 2);
int RECEIVED_gjatësi = përdorues.자료받기(dorezë_VALUE, të_dhëna, 1500);
përdorues.mbyll_rrjet(dorezë_VALUE);
```

aktual_të_dhëna 프로그램에서는 Hap·dërgoj·받기의 음수 반환값을 각각 검사한다. 완성된 예제는 `예제/자료통신.java`에 있다. `자료받기`의 Prit_VALUE 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 수신 대기열은 한 개뿐이므로 추가 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | dorezë_VALUE·Proces_VALUE_futje gjatësi_VALUE·성공 등 해당 함수의 llogaritje |
| -5 | pajisje_VALUE dërgoj_VALUE dështim_VALUE |
| -9 | 잘못되었거나 닫힌 통신 dorezë_VALUE |
| -11 | 비차단 받기에서 도착한 të_dhëna 없음 |
| -14 | përdorues tregues/ARRAY_VALUE fragment GABIM |
| -19 | Mbështetje_VALUE NIC 없음 |
| -22 | portë_VALUE/Prit_VALUE Ora_VALUE_4692cef5/Argumente VALUE GABIM |
| -24 | 열린 rrjet_portë 4개 한도 |
| -38 | 알 수 없는 시스템 호출 |
| -90 | të_dhëna 또는 수신 ARRAY_VALUE Madhësi 문제 |
| -98 | lokal_fushë portë_VALUE INDEX 중복 |
| -101 | 지원하지 않는 vendmbërritje_VALUE email |
| -110 | ARP·pajisje_VALUE·수신 Ora_VALUE_4692cef5 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 enkodim_VALUE 있는 Java `int`의 bit_VALUE 패턴을 사용하므로 상위 비트가 1인 정상 IP 주소가 음수로 보일 수 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## zbatoj_komandë 경계와 시스템 호출

```text
pasues run → JKAP에서 ELF vlerësoj·적재 → ring 3 përdorues program_f5044b9b
                                 ↓ int 0x80
                      tregues 검사 → Java bërthamë_VALUE API → RTL8139/UDP
                                 ↓ dal_program·përjashtim·Ora_VALUE_4692cef5 초과
                                pasues 복귀
```

시스템 호출 레지스터는 `EAX=INDEX`, `EBX,ECX,EDX,ESI,EDI=Argumente`, `EAX=llogaritje`다. Java 호출 스택 ABI는 컴파일러가 përdorues 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| INDEX | 호출 |
| --- | --- |
| 0 | dal_program(status_VALUE kod_VALUE) — Ekzekuto/GABIM 런타임에서 사용 |
| 1 | varg_VALUE Shkrimi |
| 2 / 3 | Argumente njësi_COUNT / Argumente varg_VALUE email |
| 10 | UDP Hap |
| 11 | UDP dërgoj(dorezë_VALUE, IP, vendmbërritje_VALUE portë_VALUE, ARRAY_VALUE email, gjatësi_VALUE) |
| 12 | UDP 받기(dorezë_VALUE, ARRAY_VALUE email, 제한 밀리초) |
| 13 | UDP Mbyll |
| 14 | lokal_fushë IP email |
| 15 / 16 | 마지막 homolog_VALUE IP / UDP portë_VALUE |
| 20 | RAM Kartelë Leximi(Emër int[] email, 출력 int[] email) |
| 21 | RAM Kartelë Shkrimi(Emër int[] email, 입력 int[] email, bajt_VALUE gjatësi_VALUE) |
| 22 | UTF-16 kod_VALUE mësim_VALUE 문자 출력(0~65535) |

Kartelë API는 `përdorues.파일읽기(int[] Emër, int[] të_dhëna)`와 `përdorues.shkruaj_skedar(int[] Emër, int[] të_dhëna, int gjatësi_VALUE)`다. 이름은 ASCII kod_VALUE ARRAY_VALUE(최대 64칸, 0 dal_program 또는 ARRAY_VALUE 끝), të_dhëna njësi_element 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 Kartelë 없음 `-2`, tregues GABIM `-14`, Emër/gjatësi_VALUE GABIM `-22`, Kartelë hapësirë_për_tekst_VALUE 부족 `-28`, Madhësi 초과 `-90`을 반환한다. 쓰기는 vlerësoj 후 Kartelë 전체를 대체한다. `përdorues.shkruaj_karakter_VALUE(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`실행권한()`은 시스템 호출이 아니라 përdorues 모드에서 CS의 하위 비트를 직접 읽으므로 aktual_të_dhëna zbatoj_komandë 권한을 확인한다. bërthamë_VALUE 포트 접근용 `pajisje_VALUE` native 함수는 përdorues objektiv 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 zbatoj_komandë, 파이프, 프로세스 간 통신은 없다. zbatoj_komandë 파일은 커널의 Leximi 전용 JKAP 묶음에서 적재한다. të_dhëna 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- përdorues 가상 email `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. zbatoj_komandë 영상은 e_përparme_VALUE 2MiB, 인수는 `0x04300000`부터, 스택은 영역 끝에서 시작한다. bërthamë_VALUE identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB përdorues 영역을 비우고 Kartelë 구역을 복사해 BSS·ARRAY_VALUE 영역을 초기화한다. përdorues GC는 없지만 dal_program 후 Tjetër_njësi zbatoj_komandë 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 Citim/이스케이프 파싱은 없다.
- përdorues 페이지의 kod_VALUE/të_dhëna 분리 Leximi 전용 Rregullime, NX, 스택 guard, ASLR은 아직 없다. 커널과 përdorues Memorie_të_dhëna·포트 leje_VALUE 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 zbatoj_komandë 상한을 두며 Ora_VALUE_4692cef5 초과는 `Exit: 124`다. përdorues CPU 예외는 `128 + përjashtim INDEX`(페이지 GABIM 142, 특권 위반 141), Java ARRAY_VALUE/계산 오류는 101~105다. bërthamë_VALUE 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, statik_VALUE IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP kontrolli_i_shumës 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- përdorues zbatoj_komandë·네트워크·mbroj_VALUE 경계 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 zbatoj_komandë·정상 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## vlerësoj 근거

`make test`는 컴파일러 14개 시험, Java 패킷 kusht 2,201개 검사, 기존 pasues ELF/ISO 부팅 시험, përdorues ELF/aktual_të_dhëna UDP/mbroj_VALUE 경계 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 gjatësi_VALUE·해시까지 `os/build/사용자통신시험.json`에 기록한다. 시험용 손상된 ELF·특권 Komanda·무한 përsëritje_VALUE 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 të_dhëna: [Intel 시스템 프로그래밍 명세](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 구현](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 LEXOMË_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
