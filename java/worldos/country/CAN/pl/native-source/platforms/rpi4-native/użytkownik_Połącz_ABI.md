# własny ARM64 przestrzeń_użytkownika Wykonaj_polecenie ABI v1

이 ABI는 `platforms/rpi4-native`의 제한된 freestanding Wykonaj_polecenie 환경이다. Linux AArch64 ABI나 POSIX 전체 구현이 아니다. **OpenJDK/JRE, CPython, libc, libstdc++는 아직 이식되지 않았다.**

ELF 로더는 nazwa_pliku 확장자 대신 rzeczywisty_dane ELF 헤더를 검사한다. 아래 własny ABI와 별도로 `run --linux FILE`에 제한된 Linux ARM64 statyczny_WARTOŚĆ Wykonaj_polecenie nazwa_pliku 경로를 추가했다. 두 시스템 호출 번호표를 혼합하지 않는다. [ELF·Linux ABI 매뉴얼](wykonywalny_ABI.md).

## ELF와 Wykonaj_polecenie 수명

- ELF64 little endian, ET_EXEC, EM_AARCH64, 버전 1, e_flags=0.
- program_f5044b9b 헤더 최대 16개. PT_LOAD는 Odczyt 가능, 4 KiB wyrównać_WARTOŚĆ, 페이지 간 zagnieżdżenie_WARTOŚĆ 없음, filesz≤memsz, BLD_OBRAZ Adres obcinać 안이어야 한다. W+X는 거부한다.
- 진입점은 nazwa_pliku 내용이 있는 Wykonaj_polecenie 세그먼트 안의 4바이트 wyrównać_WARTOŚĆ 주소다.
- PT_NOTE에 Nazwa `JKOROS\0`(namesz=7), type=1, descsz=4, 버전 1의 little endian uint32가 필요하다. SDK의 `start.o`가 넣는다.
- PT_DYNAMIC/PT_INTERP/PT_TLS 등은 거부한다. 동적 재배치·공유 biblioteka·TLS 로더가 없다.
- 커널에 포함한 ELF 묶음을 검증하고 별도 przestrzeń_użytkownika 메모리에 복사한 BACK_WARTOŚĆ EL0로 진입한다. 커널에 함수로 statyczny_WARTOŚĆ 링크해 호출하는 Wstecz_towar `cpp_test`와 다르다.
- 내장 프로그램은 `demo.elf`, `fault.elf`의 8개 chronić_WARTOŚĆ testy tryb_WARTOŚĆ, `network.elf`, własny Java narzędzia, MicroPython이다. 셸의 `load`/`run FILE`로 RAM의 16KiB 이하 ELF도 같은 walidować 경로로 실행한다.
- `_start`가 `user_start`를 호출하고 `.init_array` → `START_użytkownik_program(int)` → `.fini_array` 순서로 실행한 BACK_WARTOŚĆ exit 호출을 수행한다. 인수는 호출 15로 읽으며 표준 argc/argv/envp operand_Stos 배치는 없다.
- 한 번에 한 przestrzeń_użytkownika 프로그램이 CPU에서 실행된다. 네 터미널에 각 하나씩 interakcyjny 프로그램을 일시 정지해 보관할 identyfikator 있다. systemy_informacyjne_zwykła wyjść_program·wyjątek·wartość_czasu 초과 시 커널에 복귀하고 열린 nazwa_pliku/소켓을 닫으며 przestrzeń_użytkownika 페이지 권한을 제거한다.
- statyczny_WARTOŚĆ 생성자와 자동 객체의 RAII 소멸자를 시험했다. `__cxa_atexit`, 표준 C++ wyjątek/RTTI/STL, 일반적인 전역 obiekt_WARTOŚĆ wyjść_program 등록은 제공하지 않는다.

## 주소와 chronić_WARTOŚĆ

| 가상 Adres obcinać | 용도 |
|---|---|
| 0x02000000–0x02bfffff | ELF BLD_OBRAZ, 최대 12 MiB |
| 0x02c00000–0x02ecffff | brk sterta_WARTOŚĆ, 최대 2880 KiB |
| 0x02ed0000–0x02efffff | 미매핑 SMS_zakres/operand_Stos 아래 chronić_WARTOŚĆ SMS_zakres |
| 0x02f00000–0x02ffffff | 1 MiB przestrzeń_użytkownika operand_Stos |

własny JVM의 Klasa_WARTOŚĆ·obiekt_WARTOŚĆ 자료를 수용하도록 przestrzeń_użytkownika 창을 16 MiB로 확장했다. program_f5044b9b 헤더의 Zezwalaj_WARTOŚĆ obcinać, 페이지 pozwolenie_WARTOŚĆ 검사, SDK 링커 skrypt_WARTOŚĆ 및 chronić_WARTOŚĆ 시험이 같은 배치를 사용한다. 기존에 brk Uruchom_2 주소를 상수로 가정한 프로그램은 새 SDK로 다시 빌드한다. 일반 프로그램은 호출 8로 bieżący_towar brk를 조회한다.

Wykonaj_polecenie 코드는 EL0 Odczyt/실행만, dane·sterta_WARTOŚĆ·스택은 EL0 Odczyt/쓰기만 허용한다. 나머지 jądro_WARTOŚĆ RAM·urządzenie_WARTOŚĆ MMIO에는 EL0 권한을 주지 않는다. 이번 W^X 보장은 **przestrzeń_użytkownika 페이지에 대한 것**이다. kernel identity map의 전체 pozwolenie_WARTOŚĆ 분할이나 다중 프로세스 Adres ADRES_region 전환을 구현했다고 의미하지 않는다.

커널은 `-mgeneral-regs-only`로 빌드한다. przestrzeń_użytkownika C/C++는 FP/SIMD를 허용하고, przestrzeń_użytkownika punkt_wejścia_WARTOŚĆ 시 wektor_WARTOŚĆ 레지스터와 FPCR/FPSR를 초기화한다. jądro_WARTOŚĆ 복귀용 callee-saved FP 상태를 보관한다. syscall/IRQ의 C 처리부는 FP 레지스터를 사용하지 않는다. 향후 여러 przestrzeń_użytkownika 스레드를 전환할 때에는 각 스레드의 전체 FP kontekst_WARTOŚĆ 보존을 별도로 구현해야 한다.

GIC-400의 물리 타이머 IRQ로 약 2초의 Wykonaj_polecenie 기한을 적용한다. SVC 없는 무한 반복도 종료한다. 시스템 호출 Uruchom_2 시 기한을 검사하지만 EL1 Proces_WARTOŚĆ_wpis 중에는 IRQ를 마스킹하므로 긴 pozycja_wyjścia/그리기 호출의 종료는 지연될 identyfikator 있다. 이것은 program_f5044b9b Wykonaj_polecenie 기한이며 일반 선점 스케줄러가 아니다.

## 시스템 호출

`svc #0`, INDEKS x8, argumenty x0…x5, WYNIK x0. 실패는 negatywny_WARTOŚĆ błąd 번호다. `libposix-kor-user.a`는 이를 -1과 `numer_błędu`로 바꾼다. przestrzeń_użytkownika 프로그램의 errno는 bieżący_towar 단일 Wykonaj_polecenie 흐름용이며 pthread TLS가 아니다.

| INDEKS | 호출 | argumenty |
|---:|---|---|
| 0 | ABI 버전 | 없음, 1 Zwrot_KR |
| 1 | write | fd, buffer, count |
| 2 | read | fd, buffer, count |
| 3 | open | NUL wyjść_program ścieżka_2, flags; mode는 저장하지 않음 |
| 4 | close | nazwa_pliku 또는 루프백 gniazdo_WARTOŚĆ fd |
| 5 | lseek | fd, signed offset, origin |
| 6 | exit | 하위 8비트 wyjść_program Stan_WARTOŚĆ |
| 7 | 밀리초 | rozruch_maszyny 후 32비트 카운터; wrap 가능, POSIX clock_gettime 아님 |
| 8 | brk | 0이면 bieżący_towar 끝, 그 외 새 끝; 매핑 rozszerzenie_WARTOŚĆ 시 새 페이지 inicjuj |
| 9 | nazwa_pliku Rozmiar | fd; fstat ABI 아님 |
| 10 | ftruncate | fd, length |
| 11 | unlink | NUL wyjść_program ścieżka_2 |
| 12 | fsync | fd; RAM 파일은 ENOSYS |
| 13 | prostokąt | x, y, RGB32 WARTOŚĆ, width, height |
| 14 | UART bajt_WARTOŚĆ | wejście_WARTOŚĆ 없음은 -1, POSIX read와 별도 보조 호출 |
| 15 | Wykonaj_polecenie argumenty | index, buffer, capacity; index=UINTPTR_MAX이면 towar_ILE_LICZB, 나머지는 UTF-8 długość_WARTOŚĆ Zwrot_KR 및 NUL wyjść_program kopiować_WARTOŚĆ |
| 16 | interakcyjny tty | 0: Uruchom_2/bieżący_towar WIERSZ_WARTOŚĆ·kolumna_WARTOŚĆ Zwrot_KR, 1: wejście_WARTOŚĆ chwileczkę_WARTOŚĆ(dane 없음 -11), 2: wyjść_program, 3: bieżący_towar Rozmiar zapytanie_WARTOŚĆ(상위 16비트 WIERSZ_WARTOŚĆ, 하위 16비트 kolumna_WARTOŚĆ) |
| 17 | 협력 chwileczkę_WARTOŚĆ | 밀리초(0~100); komunikacja·FTP를 처리하며 CPU 기한 odświeżyć |
| 18 | ścieżka_2 작업 | NUL wyjść_program ścieżka_2, Akcja(0: Rodzaj_WARTOŚĆ, 1: mkdir, 2: rmdir); Rodzaj_WARTOŚĆ 0: 없음, 1: nazwa_pliku, 2: Katalog_WARTOŚĆ |
| 20 | GUI element_WARTOŚĆ | Akcja, element_WARTOŚĆ INDEKS, WARTOŚĆ 4개; własny Swing peer 전용 |
| 21 | GUI tekst | element_WARTOŚĆ INDEKS, uint32 코드포인트 TABLICA_WARTOŚĆ, długość_WARTOŚĆ(≤127) |
| 22 | 화면 Rozmiar | x0=0: rzeczywisty_dane 너비, x0=1: rzeczywisty_dane wysokość_WARTOŚĆ; 다른 값은 -EINVAL, 화면 없음은 -ENODEV |
| 32 | socket | domain, type, protocol |
| 33 | bind | fd, sockaddr, address length |
| 34 | sendto | fd, buffer, count, flags, sockaddr, address length |
| 35 | recvfrom | fd, buffer, count, flags, peer sockaddr, length pointer |
| 36 | getsockname | fd, sockaddr, length pointer |
| 37 | connect | 연결형 fd, sockaddr, address length |
| 38 | listen | 연결형 fd, backlog; rzeczywisty_dane chwileczkę_WARTOŚĆ 최대 4개 |
| 39 | accept | 연결형 fd, 0, 0; peer Adres 반환은 아직 없음 |

미지원 호출은 -ENOSYS이다. 모든 przestrzeń_użytkownika 포인터와 해당 페이지의 Odczyt/Zapis 권한을 확인한다. 파일은 3…18의 프로세스별 서술자를 jądro_WARTOŚĆ 서술자로 변환한다. 0은 bieżący_towar 셸의 표준 wejście_WARTOŚĆ(UART 또는 리다이렉션/파이프), 1은 표준 pozycja_wyjścia(UART/GUI 또는 리다이렉션/파이프), 2는 UART/GUI 진단 출력이다. UART에 읽을 자료가 없으면 -EAGAIN, nazwa_pliku/파이프 wejście_WARTOŚĆ 끝이면 read가 0을 반환한다. 출력은 nazwa_pliku/파이프에서 LF를 그대로 유지하고 UART에서만 CRLF로 표시한다. 파이프는 16 KiB 순차 버퍼이며 프로세스 간 동시 파이프/PTY는 아니다. read/write 요청은 65536바이트 이하이며, RAM 파일은 최대 64개, 각각 16384바이트다. nazwa_pliku 경로는 bieżący_towar powłoka 경로에 대한 węzeł_równorzędny_WARTOŚĆ ścieżka_2 또는 `/`로 시작하는 절대 경로이며 UTF-8 63바이트까지다. 디렉터리 generować·빈 Katalog_WARTOŚĆ usuń_wpis·Rodzaj_WARTOŚĆ 조회는 호출 18로도 제공한다. bieżący_towar ścieżka_2 변경은 powłoka 내장 cd가 담당한다. 그래픽 요청은 호출 22로 조회한 rzeczywisty_dane 화면 Rozmiar 안의 직사각형만 허용한다. 프레임버퍼 Adres 자체는 사용자에게 노출하지 않는다.

힙의 페이지 lekcja_WARTOŚĆ 축소·재확장에서 다시 노출하는 페이지는 0으로 만든다. 같은 페이지 안에서 brk만 줄였다 늘리는 경우에는 해당 페이지 내용이 남을 identyfikator 있다. malloc/free나 mmap/mprotect의 구현은 아니다.

인수는 최대 8개·각 255바이트다. 잘못된 번호는 -EINVAL, 작은 버퍼는 -ENAMETOOLONG, Zapis 불가능한 포인터는 -EFAULT다. `run FILE [ARGS]`는 파일명을 argumenty 0으로 포함한다. `javac`/`java`/`python`은 instrukcja_WARTOŚĆ 자체를 제외한 토큰을 전달한다. 인수는 jądro_WARTOŚĆ 보관 자료를 przestrzeń_użytkownika 버퍼로 복사하며 jądro_WARTOŚĆ 포인터를 반환하지 않는다.

## UDP 루프백의 계약

바깥 IPv4는 lwIP/SLIP로 확장했다. 기존 fd/구조체/wskaźnik 검사 규약을 유지하며 0.0.0.0 또는 10.0.2.15에 bind한 끝점을 바깥 통신에 연결한다. 127.0.0.1에 명시적으로 bind한 UDP는 루프백에 한정한다. zewnętrzny_WARTOŚĆ TCP connect는 비차단 -EINPROGRESS(-115)를 반환할 identyfikator 있으므로 같은 주소로 재시도하여 완료를 확인한다. [Wykonaj_polecenie/제한](파일전송과번역.md).

`chmura_Rodzina`, `gniazdo_do_przesyłania_datagramów`, transfer_protokół 0/`datagram_protokół`을 허용한다. `struct chmura_gniazdo_ADRES`는 16바이트이며 주소갈래는 urządzenie_WARTOŚĆ SEKWENCJA_WARTOŚĆ, 접속번호와 adres_internetowy.주소값은 sieć_WARTOŚĆ 차례다. 호환용 pk_sockaddr_in도 같은 배치지만 독립 자료형이다. polski 함수는 직접 SVC를 호출하는 rzeczywisty_dane 함수이며 표준 이름으로 치환하는 매크로가 아니다. host Linux 헤더를 섞지 않는다.

- 목적지는 127.0.0.1만 Zezwalaj_WARTOŚĆ. bind는 0.0.0.0 또는 127.0.0.1, port=0이면 49152…65535에서 빈 창구를 고른다.
- 미바인드 소켓의 첫 전송은 임시 창구를 바인드한다. 같은 창구의 중복 bind는 EADDRINUSE.
- 최대 8개 gniazdo_WARTOŚĆ, 각 큐 4개, 전문은 0…512바이트. 빈 전문도 소비된다.
- odbierać_WARTOŚĆ 버퍼가 작으면 복사할 부분만 반환하고 전문의 나머지는 버린다. peer Adres/창구를 반환한다.
- flags는 bieżący_towar 0만 wsparcie_WARTOŚĆ. 비차단 수신의 빈 큐 및 wysłać_WARTOŚĆ wartość_docelowa 큐 포화는 EAGAIN이다.
- wartość_docelowa port_WARTOŚĆ 없음은 ECONNREFUSED, 512바이트 초과는 EMSGSIZE, 루프백에 명시적으로 바인드한 UDP의 zewnętrzny_WARTOŚĆ IP는 ENETUNREACH, UDP 소켓에 잘못된 규약을 지정하면 EPROTONOSUPPORT. SOCK_STREAM은 별도 연결형 루프백에서 제공한다.
- zewnętrzny_WARTOŚĆ IPv4 TCP/UDP 헤더·체크섬·재전송은 lwIP가 처리한다. rzeczywisty_dane GENET/Wi-Fi NIC, poll/select, setsockopt는 아직 없다. 연결형 루프백의 connect/listen/accept는 아래 rozszerzenie_WARTOŚĆ ABI로 제공한다.

## 커널로 돌아오는 WYNIK

Java의 `Tablica.przebieg_użytkownik_program(index)`는 systemy_informacyjne_zwykła exit Stan_WARTOŚĆ 0…255 또는 Dalej_towar 값을 받는다. GUI는 실패를 표시하고 셸을 유지한다.

| WARTOŚĆ | 의미 |
|---:|---|
| -8 | ELF/ABI/Adres/pozwolenie_WARTOŚĆ walidować awaria_WARTOŚĆ |
| -16 | przestrzeń_użytkownika program_f5044b9b zagnieżdżenie_WARTOŚĆ Wykonaj_polecenie odrzucić_WARTOŚĆ |
| -22 | 등록되지 않은 program_f5044b9b INDEKS |
| -1001 | przestrzeń_użytkownika dane dostęp_wpis wyjątek |
| -1002 | przestrzeń_użytkownika instrukcja_WARTOŚĆ dostęp_wpis wyjątek |
| -1003 | 특권/미지원 polecenie 등 przestrzeń_użytkownika wyjątek |
| -1004 | przestrzeń_użytkownika Wykonaj_polecenie 기한 초과 |
| -1005 | interakcyjny przestrzeń_użytkownika program_f5044b9b 일시 정지; jądro_WARTOŚĆ powłoka 전용 WYNIK |

이는 완성된 POSIX signal/wait 상태가 아닌 bieżący_towar własny 실행기의 진단 규약이다.


## 여러 터미널의 przestrzeń_użytkownika kontekst_WARTOŚĆ

interakcyjny tty/GUI 대기를 명시적으로 시작한 프로그램은 wejście_WARTOŚĆ 대기에서 약 2초 기한을 갱신한다. chwileczkę_WARTOŚĆ 없이 무한 반복하면 타이머로 종료한다. 파이프/리다이렉션/복합 polecenie/스크립트에서 interakcyjny 시작은 -ENOTSUP로 거부한다. vi와 Swing의 이벤트 루프가 이 API를 사용한다.

다른 창으로 전환하면 Dalej_towar chwileczkę_WARTOŚĆ SVC에서 EL0 문맥을 저장하고 해당 SVC를 재실행할 위치에서 재개한다. x0…x30, SP/PC/PSTATE, v0…v31, FPCR/FPSR, 매핑·sterta_WARTOŚĆ·Wykonaj_polecenie argumenty·nazwa_pliku/gniazdo_WARTOŚĆ 소유권을 보관한다. 스냅샷은 jądro_WARTOŚĆ 전용 물리 Adres 0x04000000…0x07ffffff(네 gniazdo_WARTOŚĆ_ff41a4f1 ×16 MiB)에 저장한다. bieżący_towar Aktywny EL0 Adres 창은 종전 0x02000000…0x02ffffff를 사용한다. 스냅샷 저장소는 EL0에서 접근할 identyfikator 없다. fork/exec/wait, SMP 또는 일반 선점형 프로세스 스케줄러의 구현은 아니다.

SVC 40은 소유한 연결형 소켓의 węzeł_równorzędny_WARTOŚĆ sprzęt_port 번호를 반환한다(własny JVM용 liczba_całkowita zapytanie_WARTOŚĆ).

연결형 루프백 fd는 40…55, UDP fd는 32…39다. wyjść_program/interpretator_poleceń X 닫기에서 해당 프로그램의 nazwa_pliku·소켓을 회수한다. 연결형 읽기의 dane 없음은 -EAGAIN, 상대가 닫고 버퍼도 비면 0, 상대가 닫힌 BACK_WARTOŚĆ 쓰기는 -EPIPE다. 쓰기는 짧게 완료될 identyfikator 있다. 큐 용량은 끝점마다 1024바이트이고 한 시스템 호출은 최대 512바이트를 옮긴다. nadrzędny_WARTOŚĆ 리스너를 닫으면 아직 accept하지 않은 연결도 회수한다. zewnętrzny_WARTOŚĆ 연결은 lwIP TCP를 사용하며 zewnętrzny_WARTOŚĆ odbierać_WARTOŚĆ 버퍼는 4096바이트다. rzeczywisty_dane GENET NIC 드라이버는 없다.

협력 chwileczkę_WARTOŚĆ(17)는 일반 선점형 sleep/scheduler 구현이 아니다. 호출마다 최대 100 ms 동안 통신을 처리하고 przestrzeń_użytkownika Wykonaj_polecenie 기한을 갱신한다. pakiet 설치기의 비차단 TCP 대기에 사용한다.
