# 셸에서 실행하는 przestrzeń_użytkownika 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java materiał_pochodny środowisko plik_README_eb81d7d9](../../문서/IDE_Java.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 Wykonaj_polecenie

host interpretator_poleceń 1:

```sh
cd /home/user/jkoros
python3 os/narzędzia/echo_dane.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. zewnętrzny_WARTOŚĆ 연결을 받도록 방화벽이나 sprzęt_port 전달을 변경하지 않는다. Ctrl+C로 종료한다.

host interpretator_poleceń 2:

```sh
cd /home/user/jkoros
make run
```

게스트의 `jkoros>` 프롬프트에 wejście_WARTOŚĆ:

```text
apps
run hello first second
net
run netcheck
run udp 10.0.2.2 9000 hello
run stress 9000
```

- `hello`: 독립 Java ELF 실행과 rzeczywisty_dane CPU pozwolenie_WARTOŚĆ `ring 3`, argumenty pozycja_wyjścia.
- `netcheck`: port_WARTOŚĆ 중복, 잘못된 uchwyt_WARTOŚĆ/wskaźnik/długość_WARTOŚĆ, 비차단 받기와 wartość_czasu 초과 확인.
- `udp`: IPv4 Adres·cel_WARTOŚĆ port_WARTOŚĆ·한 Word_WARTOŚĆ 메시지를 받아 UDP로 보내고 같은 응답을 확인. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: host `10.0.2.2`의 Przypisz_WARTOŚĆ 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. odbierać_WARTOŚĆ Loop_WARTOŚĆ 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. bieżący_towar 주소는 게스트 `10.0.2.15/24`, brama_WARTOŚĆ `10.0.2.2`로 고정돼 있다. QEMU przestrzeń_użytkownika 네트워크의 host dostęp_wpis 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 program_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java program_f5044b9b dołączać_wpis

`예제/내프로그램.java`를 Dalej_towar 형식으로 만든다. 진입점은 argumenty 없는 `static int` 또는 `static void` 함수다. 인수는 przestrzeń_użytkownika API로 조회한다.

```java
public final class 내프로그램 {
    public static int Uruchom_2() {
        przestrzeń_użytkownika.Zapis("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/przestrzeń_użytkownika/program_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := przestrzeń_użytkownika/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.Uruchom_2
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `przestrzeń_użytkownika/deklaracja/przestrzeń_użytkownika.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 Wykonaj_polecenie 중인 VM에는 BLD_System 결과가 자동 반영되지 않는다. program_f5044b9b 이름은 bieżący_towar 셸의 ASCII wejście_WARTOŚĆ 제한에 맞춘 1~15자의 소문자 이름이며 Java Klasa_WARTOŚĆ·FUNKCJA_WARTOŚĆ·변수에는 한국어를 쓴다. 최대 32개 program_f5044b9b, 한 Wykonaj_polecenie 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/kompilator.py --target user --entry 인사.Uruchom_2 \
    -o os/build/apps/hello.elf os/przestrzeń_użytkownika/deklaracja/przestrzeń_użytkownika.java os/przestrzeń_użytkownika/예제/인사.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 host 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 wsparcie_WARTOŚĆ obcinać 안에서 실행한다. `.jar`와 일반 Linux Wykonaj_polecenie 파일은 지원하지 않는다.

## przestrzeń_użytkownika 네트워크 API

선언은 `deklaracja/przestrzeń_użytkownika.java`에 있다. `wysłać_dane`/`odbierać_dane`의 `int[]` towar_element 한 개는 bajt_WARTOŚĆ 하나(0~255)를 나타낸다. 한 데이터그램의 최대 dane 길이는 1,024바이트다.

```java
int uchwyt_WARTOŚĆ = przestrzeń_użytkownika.otwarty_sieć(0); // 0: 임시 lokalny_Scope UDP port_WARTOŚĆ 자동 zaznaczenie_WARTOŚĆ
int[] dane = new int[32];
dane[0] = 'H'; dane[1] = 'i';
int 보낸길이 = przestrzeń_użytkownika.wysłać_dane(uchwyt_WARTOŚĆ, 0x0a000202, 9000, dane, 2);
int KWOTA_WYKUP_długość = przestrzeń_użytkownika.odbierać_dane(uchwyt_WARTOŚĆ, dane, 1500);
przestrzeń_użytkownika.Zamknij_sieć(uchwyt_WARTOŚĆ);
```

rzeczywisty_dane 프로그램에서는 Otwórz·wysłać·받기의 negatywny_WARTOŚĆ 반환값을 각각 검사한다. 완성된 예제는 `예제/dane_komunikacja.java`에 있다. `odbierać_dane`의 chwileczkę_WARTOŚĆ 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 odbierać_WARTOŚĆ 대기열은 한 개뿐이므로 dołączać_wpis 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | uchwyt_WARTOŚĆ·Proces_WARTOŚĆ_wpis długość_WARTOŚĆ·성공 등 해당 함수의 WYNIK |
| -5 | urządzenie_WARTOŚĆ wysłać_WARTOŚĆ awaria_WARTOŚĆ |
| -9 | 잘못되었거나 닫힌 komunikacja uchwyt_WARTOŚĆ |
| -11 | 비차단 받기에서 도착한 dane 없음 |
| -14 | przestrzeń_użytkownika wskaźnik/TABLICA_WARTOŚĆ obcinać błąd |
| -19 | wsparcie_WARTOŚĆ NIC 없음 |
| -22 | port_WARTOŚĆ/chwileczkę_WARTOŚĆ wartość_czasu/argumenty WARTOŚĆ błąd |
| -24 | 열린 sieć_port 4개 한도 |
| -38 | 알 identyfikator 없는 시스템 호출 |
| -90 | dane 또는 odbierać_WARTOŚĆ TABLICA_WARTOŚĆ Rozmiar 문제 |
| -98 | lokalny_Scope port_WARTOŚĆ INDEKS 중복 |
| -101 | 지원하지 않는 cel_WARTOŚĆ Adres |
| -110 | ARP·urządzenie_WARTOŚĆ·odbierać_WARTOŚĆ wartość_czasu 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 Encoding_WARTOŚĆ 있는 Java `int`의 bit_WARTOŚĆ 패턴을 사용하므로 상위 비트가 1인 systemy_informacyjne_zwykła IP 주소가 음수로 보일 identyfikator 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## Wykonaj_polecenie 경계와 시스템 호출

```text
powłoka run → JKAP에서 ELF walidować·적재 → ring 3 przestrzeń_użytkownika program_f5044b9b
                                 ↓ int 0x80
                      wskaźnik 검사 → Java jądro_WARTOŚĆ API → RTL8139/UDP
                                 ↓ wyjść_program·wyjątek·wartość_czasu 초과
                                powłoka 복귀
```

시스템 호출 레지스터는 `EAX=INDEKS`, `EBX,ECX,EDX,ESI,EDI=argumenty`, `EAX=WYNIK`다. Java 호출 operand_Stos ABI는 컴파일러가 przestrzeń_użytkownika 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| INDEKS | 호출 |
| --- | --- |
| 0 | wyjść_program(Stan_WARTOŚĆ KOD_WARTOŚĆ) — Uruchom_2/błąd 런타임에서 używać_WARTOŚĆ |
| 1 | ciąg_WARTOŚĆ Zapis |
| 2 / 3 | argumenty towar_ILE_LICZB / argumenty ciąg_WARTOŚĆ Adres |
| 10 | UDP Otwórz |
| 11 | UDP wysłać(uchwyt_WARTOŚĆ, IP, cel_WARTOŚĆ port_WARTOŚĆ, TABLICA_WARTOŚĆ Adres, długość_WARTOŚĆ) |
| 12 | UDP odbierać(uchwyt_WARTOŚĆ, TABLICA_WARTOŚĆ Adres, 제한 밀리초) |
| 13 | UDP Zamknięte |
| 14 | lokalny_Scope IP Adres |
| 15 / 16 | 마지막 węzeł_równorzędny_WARTOŚĆ IP / UDP port_WARTOŚĆ |
| 20 | RAM nazwa_pliku Odczyt(Nazwa int[] Adres, pozycja_wyjścia int[] Adres) |
| 21 | RAM nazwa_pliku Zapis(Nazwa int[] Adres, wejście_WARTOŚĆ int[] Adres, bajt_WARTOŚĆ długość_WARTOŚĆ) |
| 22 | UTF-16 KOD_WARTOŚĆ lekcja_WARTOŚĆ 문자 pozycja_wyjścia(0~65535) |

nazwa_pliku API는 `przestrzeń_użytkownika.파일읽기(int[] Nazwa, int[] dane)`와 `przestrzeń_użytkownika.zapis_Plik(int[] Nazwa, int[] dane, int długość_WARTOŚĆ)`다. 이름은 ASCII KOD_WARTOŚĆ TABLICA_WARTOŚĆ(최대 64칸, 0 wyjść_program 또는 TABLICA_WARTOŚĆ 끝), dane towar_element 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 nazwa_pliku 없음 `-2`, wskaźnik błąd `-14`, Nazwa/długość_WARTOŚĆ błąd `-22`, nazwa_pliku gniazdo_WARTOŚĆ_ff41a4f1 부족 `-28`, Rozmiar 초과 `-90`을 반환한다. 쓰기는 walidować 후 nazwa_pliku 전체를 대체한다. `przestrzeń_użytkownika.zapis_znak_WARTOŚĆ(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`wykonanie_pozwolenie()`은 시스템 호출이 아니라 przestrzeń_użytkownika 모드에서 CS의 하위 비트를 직접 읽으므로 rzeczywisty_dane Wykonaj_polecenie 권한을 확인한다. jądro_WARTOŚĆ sprzęt_port 접근용 `urządzenie_WARTOŚĆ` native 함수는 przestrzeń_użytkownika wartość_docelowa 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 Wykonaj_polecenie, 파이프, 프로세스 간 통신은 없다. Wykonaj_polecenie 파일은 커널의 Odczyt 전용 JKAP 묶음에서 적재한다. dane 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- przestrzeń_użytkownika 가상 Adres `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. Wykonaj_polecenie 영상은 przód_WARTOŚĆ 2MiB, 인수는 `0x04300000`부터, 스택은 region_WARTOŚĆ 끝에서 시작한다. jądro_WARTOŚĆ identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB przestrzeń_użytkownika 영역을 비우고 nazwa_pliku 구역을 복사해 BSS·TABLICA_WARTOŚĆ 영역을 초기화한다. przestrzeń_użytkownika GC는 없지만 wyjść_program 후 Dalej_towar Wykonaj_polecenie 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 Cytat/이스케이프 파싱은 없다.
- przestrzeń_użytkownika 페이지의 KOD_WARTOŚĆ/dane 분리 Odczyt 전용 Ustawienia, NX, operand_Stos guard, ASLR은 아직 없다. 커널과 przestrzeń_użytkownika Pamięć_dane·sprzęt_port pozwolenie_WARTOŚĆ 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 Wykonaj_polecenie 상한을 두며 wartość_czasu 초과는 `Exit: 124`다. przestrzeń_użytkownika CPU 예외는 `128 + wyjątek INDEKS`(페이지 błąd 142, 특권 위반 141), Java TABLICA_WARTOŚĆ/계산 오류는 101~105다. jądro_WARTOŚĆ 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, statyczny_WARTOŚĆ IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP suma_kontrolna 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- przestrzeń_użytkownika Wykonaj_polecenie·네트워크·chronić_WARTOŚĆ granica_WARTOŚĆ 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 Wykonaj_polecenie·systemy_informacyjne_zwykła 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## walidować 근거

`make test`는 kompilator 14개 testy, Java 패킷 choroba 2,201개 검사, 기존 powłoka ELF/ISO rozruch_maszyny testy, przestrzeń_użytkownika ELF/rzeczywisty_dane UDP/chronić_WARTOŚĆ granica_WARTOŚĆ 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 długość_WARTOŚĆ·해시까지 `os/build/test_użytkownik_sieć.json`에 기록한다. 시험용 손상된 ELF·특권 polecenie·무한 iteracja_WARTOŚĆ 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 dane: [Intel 시스템 프로그래밍 명세](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 implementacja](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 plik_README_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
