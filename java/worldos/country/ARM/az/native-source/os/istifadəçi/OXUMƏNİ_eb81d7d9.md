# 셸에서 실행하는 istifadəçi 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java 개발 환경 OXUMƏNİ_eb81d7d9](../../문서/자바개발환경.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 icra_etmək_əmr

host Terminal 1:

```sh
cd /home/user/jkoros
python3 os/Alətlər/자료되돌리기.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. 외부 연결을 받도록 방화벽이나 포트 전달을 변경하지 않는다. Ctrl+C로 종료한다.

host Terminal 2:

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

- `hello`: 독립 Java ELF 실행과 faktiki_verilənlər CPU icazə_VALUE `ring 3`, 인수 출력.
- `netcheck`: port_VALUE 중복, 잘못된 tutacaq_VALUE/göstərici/uzunluq_VALUE, 비차단 받기와 TIME_VALUE 초과 yoxlamaq.
- `udp`: IPv4 ünvan·təyinat_VALUE_a0fbc067 port_VALUE·한 Söz_VALUE 메시지를 받아 UDP로 보내고 같은 응답을 yoxlamaq. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: host `10.0.2.2`의 təyin_et_VALUE 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. 수신 Loop_VALUE 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. 현재 주소는 게스트 `10.0.2.15/24`, şlüz_VALUE `10.0.2.2`로 고정돼 있다. QEMU istifadəçi 네트워크의 host müraciət_daxiletmə 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 proqram_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java proqram_f5044b9b 추가

`예제/내프로그램.java`를 Sonrakı_element 형식으로 만든다. 진입점은 인수 없는 `static int` 또는 `static void` 함수다. 인수는 istifadəçi API로 조회한다.

```java
public final class 내프로그램 {
    public static int İcra_Et() {
        istifadəçi.Yazma("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/istifadəçi/proqram_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := istifadəçi/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.İcra_Et
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `istifadəçi/bəyannamə/istifadəçi.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 icra_etmək_əmr 중인 VM에는 qurmaq_sistem 결과가 자동 반영되지 않는다. proqram_f5044b9b 이름은 현재 셸의 ASCII 입력 제한에 맞춘 1~15자의 소문자 이름이며 Java Sinif_VALUE·FUNCTION_VALUE·변수에는 한국어를 쓴다. 최대 32개 proqram_f5044b9b, 한 icra_etmək_əmr 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target user --entry 인사.İcra_Et \
    -o os/build/apps/hello.elf os/istifadəçi/bəyannamə/istifadəçi.java os/istifadəçi/예제/인사.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 host 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 Dəstək_VALUE klip 안에서 실행한다. `.jar`와 일반 Linux icra_etmək_əmr 파일은 지원하지 않는다.

## istifadəçi 네트워크 API

선언은 `bəyannamə/istifadəçi.java`에 있다. `göndərmək_verilənlər`/`자료받기`의 `int[]` element_element 한 개는 bayt_VALUE 하나(0~255)를 나타낸다. 한 데이터그램의 최대 verilənlər 길이는 1,024바이트다.

```java
int tutacaq_VALUE = istifadəçi.açmaq_Şəbəkə(0); // 0: 임시 lokal_miqyas UDP port_VALUE 자동 seçilmiş_sahə_VALUE
int[] verilənlər = new int[32];
verilənlər[0] = 'H'; verilənlər[1] = 'i';
int 보낸길이 = istifadəçi.göndərmək_verilənlər(tutacaq_VALUE, 0x0a000202, 9000, verilənlər, 2);
int RECEIVED_uzunluq = istifadəçi.자료받기(tutacaq_VALUE, verilənlər, 1500);
istifadəçi.bağlamaq_Şəbəkə(tutacaq_VALUE);
```

faktiki_verilənlər 프로그램에서는 Aç·göndərmək·받기의 음수 반환값을 각각 검사한다. 완성된 예제는 `예제/자료통신.java`에 있다. `자료받기`의 gözlə_VALUE 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 수신 대기열은 한 개뿐이므로 추가 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | tutacaq_VALUE·Proses_VALUE_daxiletmə uzunluq_VALUE·성공 등 해당 함수의 ölçü |
| -5 | cihaz_VALUE göndərmək_VALUE xəta_VALUE |
| -9 | 잘못되었거나 닫힌 통신 tutacaq_VALUE |
| -11 | 비차단 받기에서 도착한 verilənlər 없음 |
| -14 | istifadəçi göstərici/ARRAY_VALUE klip XƏTA |
| -19 | Dəstək_VALUE NIC 없음 |
| -22 | port_VALUE/gözlə_VALUE TIME_VALUE/인수 VALUE XƏTA |
| -24 | 열린 Şəbəkə_port 4개 한도 |
| -38 | 알 수 없는 시스템 호출 |
| -90 | verilənlər 또는 수신 ARRAY_VALUE Böyüklük 문제 |
| -98 | lokal_miqyas port_VALUE INDEX 중복 |
| -101 | 지원하지 않는 təyinat_VALUE_a0fbc067 ünvan |
| -110 | ARP·cihaz_VALUE·수신 TIME_VALUE 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 kodlaşdırma_VALUE 있는 Java `int`의 bit_VALUE 패턴을 사용하므로 상위 비트가 1인 정상 IP 주소가 음수로 보일 수 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## icra_etmək_əmr 경계와 시스템 호출

```text
örtük run → JKAP에서 ELF təsdiqlə·적재 → ring 3 istifadəçi proqram_f5044b9b
                                 ↓ int 0x80
                      göstərici 검사 → Java nüvə_VALUE API → RTL8139/UDP
                                 ↓ Çıxış_proqram·istisna·TIME_VALUE 초과
                                örtük 복귀
```

시스템 호출 레지스터는 `EAX=INDEX`, `EBX,ECX,EDX,ESI,EDI=인수`, `EAX=ölçü`다. Java 호출 스택 ABI는 컴파일러가 istifadəçi 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| INDEX | 호출 |
| --- | --- |
| 0 | Çıxış_proqram(vəziyyət_VALUE kod_VALUE) — İcra_Et/XƏTA 런타임에서 사용 |
| 1 | sətir_VALUE Yazma |
| 2 / 3 | 인수 element_COUNT / 인수 sətir_VALUE ünvan |
| 10 | UDP Aç |
| 11 | UDP göndərmək(tutacaq_VALUE, IP, təyinat_VALUE_a0fbc067 port_VALUE, ARRAY_VALUE ünvan, uzunluq_VALUE) |
| 12 | UDP 받기(tutacaq_VALUE, ARRAY_VALUE ünvan, 제한 밀리초) |
| 13 | UDP Bağla |
| 14 | lokal_miqyas IP ünvan |
| 15 / 16 | 마지막 eynisəviyyəli_VALUE IP / UDP port_VALUE |
| 20 | RAM FAYL Oxuma(Ad int[] ünvan, 출력 int[] ünvan) |
| 21 | RAM FAYL Yazma(Ad int[] ünvan, 입력 int[] ünvan, bayt_VALUE uzunluq_VALUE) |
| 22 | UTF-16 kod_VALUE dərs_VALUE 문자 출력(0~65535) |

FAYL API는 `istifadəçi.파일읽기(int[] Ad, int[] verilənlər)`와 `istifadəçi.yazmaq_fayl(int[] Ad, int[] verilənlər, int uzunluq_VALUE)`다. 이름은 ASCII kod_VALUE ARRAY_VALUE(최대 64칸, 0 Çıxış_proqram 또는 ARRAY_VALUE 끝), verilənlər element_element 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 FAYL 없음 `-2`, göstərici XƏTA `-14`, Ad/uzunluq_VALUE XƏTA `-22`, FAYL slot_VALUE 부족 `-28`, Böyüklük 초과 `-90`을 반환한다. 쓰기는 təsdiqlə 후 FAYL 전체를 대체한다. `istifadəçi.yazmaq_simvol_VALUE(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`실행권한()`은 시스템 호출이 아니라 istifadəçi 모드에서 CS의 하위 비트를 직접 읽으므로 faktiki_verilənlər icra_etmək_əmr 권한을 확인한다. nüvə_VALUE 포트 접근용 `cihaz_VALUE` native 함수는 istifadəçi hədəf 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 icra_etmək_əmr, 파이프, 프로세스 간 통신은 없다. icra_etmək_əmr 파일은 커널의 Oxuma 전용 JKAP 묶음에서 적재한다. verilənlər 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- istifadəçi 가상 ünvan `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. icra_etmək_əmr 영상은 ön_VALUE 2MiB, 인수는 `0x04300000`부터, 스택은 영역 끝에서 시작한다. nüvə_VALUE identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB istifadəçi 영역을 비우고 FAYL 구역을 복사해 BSS·ARRAY_VALUE 영역을 초기화한다. istifadəçi GC는 없지만 Çıxış_proqram 후 Sonrakı_element icra_etmək_əmr 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 Dırnaqarası/이스케이프 파싱은 없다.
- istifadəçi 페이지의 kod_VALUE/verilənlər 분리 Oxuma 전용 Sazlama, NX, 스택 guard, ASLR은 아직 없다. 커널과 istifadəçi Yaddaş_verilənlər·포트 icazə_VALUE 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 icra_etmək_əmr 상한을 두며 TIME_VALUE 초과는 `Exit: 124`다. istifadəçi CPU 예외는 `128 + istisna INDEX`(페이지 XƏTA 142, 특권 위반 141), Java ARRAY_VALUE/계산 오류는 101~105다. nüvə_VALUE 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, statik_VALUE IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP 검사합 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- istifadəçi icra_etmək_əmr·네트워크·qorumaq_VALUE 경계 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 icra_etmək_əmr·정상 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## təsdiqlə 근거

`make test`는 컴파일러 14개 시험, Java 패킷 şərt 2,201개 검사, 기존 örtük ELF/ISO 부팅 시험, istifadəçi ELF/faktiki_verilənlər UDP/qorumaq_VALUE 경계 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 uzunluq_VALUE·해시까지 `os/build/사용자통신시험.json`에 기록한다. 시험용 손상된 ELF·특권 Əmr·무한 iterasiya_VALUE 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 verilənlər: [Intel 시스템 프로그래밍 명세](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 구현](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 OXUMƏNİ_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
