# własny 커널과 번역기의 polski Nazwa

대상은 `platforms/rpi4-native`의 własny Java jądro_WARTOŚĆ, przestrzeń_użytkownika JVM, C maszyna Połącz,
TCP/UDP·FTP, C kompilator_narzędzie 이식부, MicroPython 이식부, BLD_System·Wykonaj_polecenie·testy 도구다.
`golang/worldos/Country_WARTOŚĆ/KOR/plik_źródłowy`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 własny 선언도 명명 검사에 포함한다.
Linux 실행판의 host narzędzia, OpenJDK 보조 narzędzia 및 zewnętrzny_WARTOŚĆ dystrybucja_WARTOŚĆ źródło_drzewo 전체를
한국어로 다시 작성했다는 뜻은 아니다.

## 명명 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `dojście_do_pliku`, `węzeł_równorzędny_numer_portu`, `pamięć_dynamiczna`, `klawiatura`.
- 함수는 행위를 나타낸다: `Odczyt`, `Zapis`, `Otwórz`, `Zamknięte`, `NET_BIND`, `przebieg_program`.
- TCP의 이어진 bajt_WARTOŚĆ 흐름과 UDP의 granica_WARTOŚĆ 있는 자료를 `połączenie`와 `datagram_Kanał`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `długość_WARTOŚĆ`, `dane_stanowisko`, `WYSZUKAJ_INDEKS`, `반환값`으로 풀어 쓴다.
  순번·임시 산술값처럼 여러 역할에 재사용되는 변수는 `순번`, `첫째값`, `SEKUNDA_WARTOŚĆ`으로 구별한다.
- 이름이 같아도 zewnętrzny_WARTOŚĆ 구조체의 필드와 własny 변수는 별도로 분석한다.

`Kanał_wpis(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 komunikacja 연결에
적용했다. `port_WARTOŚĆ(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [Kanał_wpis](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[port_WARTOŚĆ](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`datagram(電文)`은 전보에 담는 글이라는 기존 komunikacja 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 datagram](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`Stream_WARTOŚĆ`, `wątek_WARTOŚĆ`, `쌓임`은 우리말의 움직임·이어짐·쌓이는 모양을 빌린 표현이다.
`strumień_wejściowy`, `pracownik`, `pamięć_stosu` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 słownik 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 TŁUMACZ_źródło·국어사 datagram 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 Nazwa | 이유 |
|---|---|---|
| TCP Socket | połączenie | 상대와 연결되어 zamówić_WARTOŚĆ 있는 바이트를 주고받음 |
| ServerSocket | odbierać_port | 새 연결이 들어오는 접점 |
| DatagramSocket | datagram_Kanał | 각 자료의 경계를 보존하는 komunikacja |
| InputStream / OutputStream | strumień_wejściowy / strumień_wyjściowy | 들어오고 나가는 바이트의 zamówić_WARTOŚĆ |
| heap / stack | pamięć_dynamiczna / pamięć_stosu | przydzielić_Pamięć 방식과 쌓고 꺼내는 architektura |
| thread / keyboard | pracownik / klawiatura | 이어지는 실행과 글쇠의 TABLICA_WARTOŚĆ |
| exception / timeout | wyjątek / chwileczkę_TIMEOUT_wyjątek | systemy_informacyjne_zwykła 처리에서 벗어남과 그 구체적 이유 |

## 경로와 대응표

| implementacja | polski ścieżka_2 |
|---|---|
| jądro_WARTOŚĆ·powłoka·nazwa_pliku warstwa_WARTOŚĆ | `plik_źródłowy/*.java` |
| przestrzeń_użytkownika JVM | `przestrzeń_użytkownika/자바/자바가상기계.java` |
| ARM64 maszyna Połącz | `maszyna/*.c`, `rozruch_maszyny/` |
| TCP·UDP·FTP | `sieć_Stos/sieć_Stos.c`, `sieć_Stos/transfer_plików.c` |
| C kompilator_narzędzie 이식 | `C_kompilator/` |
| MicroPython 이식 | `PYTHON_mostek/` |
| BLD_System·Wykonaj_polecenie·testy | `narzędzia/`, `Twórca_wpis.mk` |
| Java przestrzeń_użytkownika API | `한국어자바/polski/własny/` |

[nazwa_pliku_mapowanie.tsv](nazwa_pliku_mapowanie.tsv), [자바이름대응.tsv](자바이름대응.tsv),
[C_nazwa_mapowanie.tsv](C_nazwa_mapowanie.tsv), [PYTHON_nazwa_mapowanie.tsv](PYTHON_nazwa_mapowanie.tsv)에
Wstecz_towar 이름과 바뀐 이름이 있다. C/Java 대응표의 nazwa_pliku·위치는 이행 당시 기준이다.
ścieżka_2 이동은 nazwa_pliku 대응표를 함께 본다. 기존 `tools/*.py`는 polski 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 SD Nazwa

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
bieżący_towar 다섯 Java 예제는 `Uruchom_2()`·`실행인수`·polski 화면/wątek_WARTOŚĆ API를 사용해
예약어·리터럴 외의 식별자를 한국어로 작성한다. 화면/가닥은 표준 객체를
감싸지 않고 własny JVM에 직접 구현했다. 자세한 계약은 [polski Java API](../한국어자바/plik_README_eb81d7d9.md)를 본다.

표준 javac는 ciąg_WARTOŚĆ 리터럴에 `java.lang.String`, ciąg_WARTOŚĆ 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 polski 소스에서도 바이트코드에 남을 identyfikator 있다.
기존 표준 class를 실행하는 JVM의 mapowanie_WARTOŚĆ ciąg_WARTOŚĆ, 아직 표준 라이브러리를 쓰는
komunikacja·nazwa_pliku 연결부까지 모두 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
deskryptor_wpis·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 FUNKCJA_WARTOŚĆ·liczba_całkowita_TYP·POSIX ABI, CPU rejestr Nazwa, 어셈블리 polecenie, 링커 절 Nazwa,
TinyCC·lwIP·MicroPython이 요구하는 Ustawienia 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
własny C 함수의 źródło_drzewo 이름은 한국어이며, [기계연결이름.h](기계연결이름.h)가
기존 AOT·어셈블리·SDK에 공개한 maszyna 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 moduł_WARTOŚĆ wartość_atrybutu, 명령행 옵션과 JSON 키도
zewnętrzny_WARTOŚĆ 계약이다. `build/`, dystrybucja_WARTOŚĆ 바이너리 이름과 `/sdk`는 기존 Wykonaj_polecenie 경로를 유지한다.
zewnętrzny_WARTOŚĆ 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 narzędzia/명명검사.py
make BLD_System
make testy
make test-examples test-ftp test-elf
python3 narzędzia/Wykonaj_polecenie.py --desktop --network
```

`narzędzia/시언어이름분석.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`narzędzia/*이름반영.py`는 zmienić_WARTOŚĆ 전 źródło_drzewo·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 다시 적용하여 대응표를 덮어쓰지 않는다.

## C komunikacja 구조체와 Python błąd

C 통신에서 `갈래`는 Adres 체계를 구분하고 `numer_portu`는 port, `ADRES_WARTOŚĆ`은
IPv4 주소의 32비트 값을 나타낸다. `datagram_protokół`은 앞서 설명한 datagram(電文)과
wartość_kontraktu(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | polski 직접 implementacja |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 chmura_Rodzina / gniazdo_do_przesyłania_datagramów / datagram_protokół |
| struct pk_sockaddr_in | struct chmura_gniazdo_ADRES |
| sin_family / sin_port | ADRES_Rodzina / numer_portu |
| sin_addr.s_addr | adres_internetowy.ADRES_WARTOŚĆ |
| OSError / błąd.args[0] | błąd_systemu / błąd.INDEKS |

polski 구조체는 `#define` 치환이나 wartość_pola 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 jądro_WARTOŚĆ SVC에서 bajt_WARTOŚĆ 복사로
검사한다. `Twórca_uczestnik`·`wysłać_datagram_dane`와 nazwa_pliku 함수는 statyczny_WARTOŚĆ 라이브러리에
rzeczywisty_dane polski 이름의 FUNKCJA_WARTOŚĆ 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
Wstecz_towar 코드에서 polski komunikacja 함수에 pk_sockaddr*를 전달했다면 polski 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `błąd_systemu`는 OSError의 polski 하위 클래스이며 연결부에서
błąd 번호를 보존하여 변환한다. 일반 Python 문법과 zewnętrzny_WARTOŚĆ 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 obcinać

`실행할일`은 수행할 내용을, `Uruchom`는 그 수행을 나타낸다.
`동작받이`는 동작이 발생했다는 알림을 받는 역할, `akcja_powiadomienie`은 전달되는 사건이다.
`przycisk`는 눌러 동작시키는 조작부, `Etykieta`는 plik_README_eb81d7d9 글의 indeks_pozycji,
`pole_tekstowe`은 글을 적는 indeks_pozycji, `pracownik`은 이어지는 Wykonaj_polecenie 흐름을 뜻한다.
`Wykonaj_polecenie(實行)`·`Akcja(動作)`의 기존 뜻과 `받다`·`알리다`·`wątek_WARTOŚĆ`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 처음 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 narzędzia/źródło_przegląd.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 skrót_Plik,
ASCII 파일명과 Python의 영어 deklaracja 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/자바도구/기계어미리번역.java`로 전환했다. `compiler/기계어미리번역.py`는 호환 진입점이다.
`compiler/arm64.py`는 Wstecz_towar 경로와 `ARM64(...).generate(...)` 호출을 이어 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK 보조 narzędzia, Linux wersja_WARTOŚĆ 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
예약어 외 100% 한국어라고 판정하지 않는다.
`narzędzia/명명검사.py --C_Język`는 Aktywny ARM64 소스의 deklaracja, C 의미 Analiza_WARTOŚĆ,
x86 Java 커널과 공용 번역기의 własny deklaracja, Java 예제 전체 identyfikator_WARTOŚĆ,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## bieżący_towar 기능을 기준으로 보완한 Nazwa

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 polski 이름을 달리 정한다.
nazwa_pliku 이름은 주된 기능을 나타내고, FUNKCJA_WARTOŚĆ 이름은 행동을, zmienna_WARTOŚĆ 이름은 담는 자료를 나타낸다.
예약어, 표준 API 및 zewnętrzny_WARTOŚĆ Połącz 규약은 따로 기록한다.

| Wstecz_towar Nazwa | 적용한 Nazwa | bieżący_towar 기능 |
|---|---|---|
| `arm64.py`의 implementacja | `compiler/자바도구/기계어미리번역.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 TŁUMACZ_źródło |
| `ARM64`, `generate` | `maszyna_KOD_kompilator`, `generować` | TŁUMACZ_źródło 상태를 담는 객체와 C plik_źródłowy generować 행동 |
| `prototype`, `method` | `metoda_prototyp`, `treść_metody` | 함수의 format_WARTOŚĆ 선언과 rzeczywisty_dane polecenie plik_źródłowy |
| `profile`, `heap_words` | `wykonanie_cel`, `sterta_Word_ILE_LICZB` | jądro_WARTOŚĆ·przestrzeń_użytkownika 구분과 przydzielić_Pamięć Pamięć_WARTOŚĆ 공간의 maszyna 낱말 identyfikator |
| `pc`, `op` | `polecenie_stanowisko`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 INDEKS |
| `x`, `y`, `w`, `h` | `współrzędna_X`, `Y_współrzędna`, `영역너비`, `region_wysokość` | zdalny_WARTOŚĆ 화면의 위치와 직사각형 Rozmiar |
| `p`, `n`, `i`, `j` | `dane_stanowisko`, `WARTOŚĆ`, `순번`, `안쪽순번` | zdalny_WARTOŚĆ 화면 dane·cyfra_WARTOŚĆ·iteracja_WARTOŚĆ indeks_pozycji; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `drzewo_obiektów_aplikacji_Pamięć_WYSZUKAJ`, `커널쌓임공간끝` | maszyna Połącz 규약을 유지하면서 własny 소스에서 사용하는 Nazwa |
| `앞캐리지` | `앞줄복귀` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[공용번역기이름대응.tsv](공용번역기이름대응.tsv)에 kompilator_narzędzie 참조의 rzeczywisty_dane zmienić_WARTOŚĆ 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[Standard_nazwa_dowód.json](Standard_nazwa_dowód.json)에 기록한다.
`C_kompilator/kompilator_narzędzie.c`는 TinyCC zewnętrzny_WARTOŚĆ 원문을 포함하는 Połącz 파일로 własny 선언이 없어서
C własny deklaracja 분석에서는 제외한다. rzeczywisty_dane jądro_WARTOŚĆ 빌드에서는 계속 컴파일한다.

### 말의 뿌리와 새로운 복합 Nazwa

`Pamięć_WARTOŚĆ(記憶)`과 `WYSZUKAJ_INDEKS(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 zamówić_WARTOŚĆ 있는 항목을 찾아 지정하는 기능에 적용한다.
słownik 근거는 국립국어원 한국어기초사전의
[Pamięć_WARTOŚĆ](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[WYSZUKAJ_INDEKS](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`pamięć_stosu`, `Przekaż_WARTOŚĆ`, `POP_WARTOŚĆ`는 자료를 포개고 마지막 자료부터 꺼내는 Wykonaj_polecenie 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`미리번역`은 Wykonaj_polecenie 전에 번역한다는 기능을 직접 나타낸다.
`maszyna_Word`은 처리기의 dane 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `maszyna`를 붙였다.
`기계어미리번역`, `sterta_Word_ILE_LICZB` 같은 복합 이름은 bieżący_towar 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 처음 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 używać_WARTOŚĆ 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 typ_danych·TABLICA_WARTOŚĆ·FUNKCJA_WARTOŚĆ·lokalny_Scope zmienna_WARTOŚĆ·gałąź_22e01337 이름도 한국어로 바꾼다.
직접 한글 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 polski 이름을
표준 C 범용 문자 표기로 출력한다. rzeczywisty_dane ARM64 빌드는 Clang으로 읽을 identyfikator 있는 한글 원문을 사용한다.
ciąg_WARTOŚĆ, C 표준 FUNKCJA_WARTOŚĆ, `java_entry` 같은 공개 Połącz 이름은 바꾸지 않는다.

셸의 사용법·문법 błąd·nazwa_pliku 및 Pamięć_WARTOŚĆ ADRES_region 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 testy·nazwa_pliku transfer_WARTOŚĆ 도구가 읽는 pisak_WARTOŚĆ,
명령행 옵션과 기존 instrukcja_WARTOŚĆ, JVM Klasa_WARTOŚĆ Nazwa·nazwa_pliku format_WARTOŚĆ·urządzenie_WARTOŚĆ 이름은 호환 표기로 남는다.
x86 VGA 문자 화면은 한글을 표시하지 못하므로 polski 문구는 UTF-8 직렬 단말에서 확인한다.
