# własny 커널에서 vi·여러 interpretator_poleceń·한글 프로그래밍 사용하기

polski komunikacja·wyjątek 사용법은 [polski Java API](한국어자바/plik_README_eb81d7d9.md), FUNKCJA_WARTOŚĆ·zmienna_WARTOŚĆ·nazwa_pliku 이름의 변경과 어원 근거는 [명명 plik_README_eb81d7d9](명명/plik_README_eb81d7d9.md)를 참고한다.

대상은 `platforms/rpi4-native`의 własny AArch64 Java 커널이다. vi와 Java/Python/C/C++ 프로그램은 EL0에서 실행한다. Linux 실행판과 별도이며 아래 wsparcie_WARTOŚĆ 목록은 전체 OpenJDK·Vim·POSIX 구현을 뜻하지 않는다.

게스트 `cc`/`jaot`, JAR 직접 Wykonaj_polecenie, zewnętrzny_WARTOŚĆ TCP/UDP와 FTP는 [새 Wykonaj_polecenie 매뉴얼](파일전송과번역.md)을 참고한다.

## GUI와 여러 interpretator_poleceń

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, Adres **127.0.0.1:5902**로 연결한다. 화면 위 **+ New terminal**, **Ctrl+Shift+T**로 터미널을 추가한다. 최대 네 개다. 위쪽 interpretator_poleceń 버튼 또는 창을 클릭해 선택하고 **F6**으로 순환한다. 제목줄을 끌어서 옮기고 **PRAWY 위 X**를 클릭하면 닫힌다. 마지막 창을 닫아도 위쪽 Wykonaj_polecenie 버튼으로 다시 kolumna_WARTOŚĆ identyfikator 있다. 기존 `terminal`, `exit`, F12도 사용할 identyfikator 있다.

창마다 bieżący_towar 디렉터리, powłoka zmienna_WARTOŚĆ, polecenie LOG_zapis, wejście_WARTOŚĆ 중인 명령과 program_f5044b9b Wykonaj_polecenie 상태를 보관한다. nazwa_pliku 저장소는 공유한다. vi와 Swing의 이벤트 chwileczkę_WARTOŚĆ 중에 다른 터미널로 전환하면 przestrzeń_użytkownika Pamięć_dane·레지스터·nazwa_pliku/gniazdo_WARTOŚĆ 연결을 보존했다가 돌아올 때 재개한다. **bieżący_towar 네 프로그램이 동시에 CPU에서 실행되는 선점형 스케줄러는 아니다.** 계산 중인 프로그램은 Dalej_towar wejście_WARTOŚĆ chwileczkę_WARTOŚĆ 또는 기존 Wykonaj_polecenie 기한까지 전환이 지연될 identyfikator 있다.

X로 터미널을 닫으면 그 터미널의 Wykonaj_polecenie 중인 프로그램도 종료하며 deskryptor_wpis·소켓을 회수한다. 저장하지 않은 Edytuj_WARTOŚĆ 내용은 사라진다. 종료한 슬롯은 새 창에서 재사용한다. bieżący_towar 모든 파일은 RAM에 있으며 VM 재시작 후에는 남지 않는다.

화면과 Okno 판단은 게스트 커널이 처리한다. QEMU Wykonaj_polecenie 도구는 VNC 키와 마우스 좌표를 UART 패킷으로 전달한다. rzeczywisty_dane Pi4 USB 입력기와 실물 부팅은 아직 검증하지 않았다. 일반 UART 셸은 `make run`, GUI narzędzia 종료는 host 터미널의 Ctrl+C다.

## vi używać_WARTOŚĆ

```text
mkdir 작업
cd 작업
vi 인사.py
```

`vi`는 새로 구현한 **vi polecenie 부분집합** 편집기다. 내장 `build/user/vi.elf`를 보호된 przestrzeń_użytkownika 영역에 적재한다. nazwa_pliku 크기는 UTF-8 bajt_WARTOŚĆ Project_korzeń 16 KiB, 경로는 63바이트까지다. 디스크에 설치한 Vim/Neovim 바이너리를 실행하는 것이 아니다.

| Klucz_WARTOŚĆ/polecenie | Akcja |
|---|---|
| `i`, `a`, `I`, `A` | bieżący_towar/Dalej_towar pozycja 또는 wiersz_wejścia 처음/끝에서 wejście_WARTOŚĆ |
| `o`, `O` | 아래/위에 새 줄을 만들고 wejście_WARTOŚĆ |
| Esc | 일반 tryb_WARTOŚĆ |
| `h j k l`, 방향키 | UTF-8 문자/wiersz_wejścia przenosić_WARTOŚĆ |
| `0`, `$`, Home, End | wiersz_wejścia 처음/끝 |
| `gg`, `G`, `:INDEKS` | nazwa_pliku 처음/마지막 wiersz_wejścia/Przypisz_WARTOŚĆ wiersz_wejścia |
| PgUp, PgDn | 화면 lekcja_WARTOŚĆ przenosić_WARTOŚĆ |
| `x`, Delete | bieżący_towar 문자 삭제 |
| `dd`, `yy`, `p` | wiersz_wejścia 삭제/kopiować_WARTOŚĆ/wkleić_SMS |
| `u` | 마지막 편집을 Zwrot_mostek; 한 etap_WARTOŚĆ 토글 |
| `/ciąg_WARTOŚĆ`, `n` | 단순 ciąg_WARTOŚĆ 검색/Dalej_towar 일치; 정규식 없음 |
| `:w`, `:w 다른이름` | RAM nazwa_pliku Store_WARTOŚĆ/다른 경로로 Store_WARTOŚĆ |
| `:q` | 변경이 없을 때 wyjść_program |
| `:q!` | 변경을 버리고 wyjść_program |
| `:wq`, `ZZ` | 저장하고 wyjść_program |

붙여 넣은 한글을 문자 경계에 맞춰 przenosić_WARTOŚĆ·삭제한다. 일반 vi의 수량 접두사, makro_WARTOŚĆ, Ustawienia nazwa_pliku, 플러그인, 정규식, 여러 버퍼/분할 Okno, 문법 강조 등은 아직 없다. `--desktop`에서는 F9·Shift+Space·한/zero_operand 키로 두벌식 조합을 전환한다. PC 입력기를 영어로 두고 Okno okno_Tytuł `[KO]`에서 입력하며, `help ko`에 단축키를 표시한다. 완성된 Unicode 문자와 VNC의 명시적 붙여넣기도 전달한다.

vi와 Swing 프로그램은 **단독 polecenie**으로 실행한다. 파이프·리다이렉션·skrypt_WARTOŚĆ·`;`/`&&`/`||`로 연결한 실행에서 interakcyjny 대기를 시작하면 거부한다. wejście_WARTOŚĆ 대기는 약 2초 CPU 기한을 갱신하지만 wejście_WARTOŚĆ chwileczkę_WARTOŚĆ 없이 무한 반복하는 프로그램은 기존처럼 종료한다.

## 한글 Java

vi에서 다음을 `인사.java`에 입력하고 Esc → `:wq`로 저장한다.

```java
public class 인사 {
    static int 더하기(int 첫째, int 둘째) { return 첫째 + 둘째; }
    public static void main(String[] argumenty) {
        int suma_WARTOŚĆ = 더하기(20, 22);
        System.out.println("안녕하세요 · suma_WARTOŚĆ=" + suma_WARTOŚĆ);
    }
}
```

게스트 셸에서 실행한다.

```text
javac 인사.java
java 인사
```

한글 nazwa_pliku_SMS·nazwa_klasy·metoda_nazwa_SMS·변수명·문자열을 사용할 identyfikator 있다. **게스트 javac는 statyczny_WARTOŚĆ Java 부분집합**이다. obiekt_WARTOŚĆ·리스너·Swing·소켓을 사용하는 소스는 bieżący_towar host JDK에서 `javac --release 8 -encoding UTF-8`로 컴파일하고 własny JVM에 class를 올린다. własny JVM에서 지원하는 바이트코드/API 범위는 [자바실행환경.md](자바실행환경.md)를 따른다.

```sh
# host
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java testy/자바/Swing_test.java
python3 narzędzia/Upload_Files.py build/my-java/Swing_test.class
```

`upload.py`는 게스트 `load`에 붙여 넣을 16진수 명령을 생성한다. pozycja_wyjścia 전체를 GUI 터미널에 보내면 업로드한다. 업로드 후 **별도로** `java Swing_test`을 실행한다. 종속 class가 있으면 각각 업로드한다. 패키지 class의 파일명은 `패키지.Klasa_WARTOŚĆ.class` 형식이다. 내장 polski 라이브러리는 별도 업로드가 필요 없다. polski Okno API의 예제는 [한글창시험.java](testy/자바/한글창시험.java)이며 같은 방법으로 kompilować_źródło·업로드해 `java 한글창시험`으로 실행한다.

GUI가 필요 없는 단일 źródło_drzewo/클래스는 호스트의 `python3 narzędzia/Wykonaj_Plik.py ścieżka_2/인사.java`로 별도 QEMU에 업로드·Wykonaj_polecenie·종료할 identyfikator 있다. interakcyjny Swing에는 Wykonaj_polecenie 후 przestrzeń_użytkownika 입력을 유지하는 `make desktop`을 사용한다.

## własny JVM의 Swing obcinać

실제로 제공하는 것은 **표준 패키지 이름으로 호출하는 własny Swing API 부분집합**이다. OpenJDK `java.desktop` 모듈이나 AWT 전체를 이식한 것은 아니다.

| API | Akcja |
|---|---|
| `JFrame` | okno_Tytuł, Rozmiar·pozycja, program_okno, Zamknięte 정책, dispose |
| `JPanel` | dziecko_WARTOŚĆ 요소를 담는 패널 |
| `JLabel` | 한글을 포함한 ciąg_WARTOŚĆ program_WARTOŚĆ·zmienić_WARTOŚĆ |
| `JButton` | 버튼과 ActionListener klikać_WARTOŚĆ Proces_WARTOŚĆ_wpis |
| `JTextField` | 한 wiersz_wejścia UTF-8 wejście_WARTOŚĆ, 삭제, getText/setText, Enter 이벤트 |
| 공통 | setBounds, setSize, add, getContentPane, repaint, validate |
| `SwingUtilities` | invokeLater, isEventDispatchThread |
| `ActionEvent` | getSource, getActionCommand, getID |

`setLayout(null)`과 `setBounds`로 배치한다. FlowLayout/BorderLayout/GridLayout, pack, 폰트·스타일 전체, 메뉴·테이블·트리·스크롤 패널, Java2D, 네이티브 AWT peer/JNI, 복잡한 문자 조판은 아직 없다. 이벤트 콜백은 własny JVM의 단일 이벤트 Wykonaj_polecenie 흐름에서 처리하며 OpenJDK EDT 구현과 동일하지 않다. Okno·요소는 Wykonaj_polecenie 하나당 suma_WARTOŚĆ 32개, element_WARTOŚĆ 글자는 최대 127 코드포인트다. wartość_domyślna 서체와 색은 커널이 제공한다.

[Swing_test.java](testy/자바/Swing_test.java)는 Okno·한글 tag_WARTOŚĆ·pole_tekstowe·버튼·이벤트 처리의 Wykonaj_polecenie 가능한 예제다. [własny Swing 화면](build/verification/swing/native-swing.png)을 참고한다.

polski 라이브러리에는 다음을 추가했다. host kompilować_źródło 시 `dist/jkoros-native-korean.jar`를 classpath에 넣는다.

- `polski.własny.Okno`: `Dodaj_element`, `program_okno`, `Zamknięte`.
- `polski.własny.element_ekranu`: `tag_WARTOŚĆ`, `przycisk`, `pole_tekstowe` generować.
- `polski.własny.połączenie_transport`: `Połącz`, `nasłuchiwać_uczestnik`, `odbierać`.
- 기존 `pozycja_wyjścia`, `문자`, `nazwa_pliku`, `작업`, `wpis_Lista`, `słownik`, `komunikacja`, `화면`, `jądro_WARTOŚĆ`도 유지한다.

## Java 네트워크

기존 `DatagramSocket`/`DatagramPacket`의 UDP 루프백에 `Socket`/`ServerSocket`의 **jądro_WARTOŚĆ 내부 연결형 bajt_WARTOŚĆ Stream_WARTOŚĆ**을 추가했다. nazwa_pliku/소켓과 마찬가지로 SVC를 통해 Java 커널이 전송한다. 물리 NIC의 TCP/IP 패킷 스택은 아니다.

```java
java.net.ServerSocket serwer_WARTOŚĆ = new java.net.ServerSocket(9250);
java.net.Socket gość_WARTOŚĆ = new java.net.Socket("localhost", 9250);
java.net.Socket Połącz = serwer_WARTOŚĆ.accept();
gość_WARTOŚĆ.getOutputStream().write("안녕하세요".getBytes("UTF-8"));
byte[] KWOTA_WYKUP_towar = new byte[64];
int długość_WARTOŚĆ = Połącz.getInputStream().read(KWOTA_WYKUP_towar);
Połącz.close(); gość_WARTOŚĆ.close(); serwer_WARTOŚĆ.close();
```

generować·Połącz·accept·양방향 bajt_WARTOŚĆ/TABLICA_WARTOŚĆ We_Wy·close·EOF·setSoTimeout을 지원한다. `String.getBytes()`와 UTF-8 이름을 지정한 getBytes도 제공한다. 루프백 주소는 `localhost`/`127.0.0.1`이다. 연결형 Koniec_punkt 16개, odbierać_WARTOŚĆ 버퍼당 1024바이트, chwileczkę_WARTOŚĆ Połącz 최대 4개이며 Java의 대기는 내부 가닥에 실행을 양보한다. wartość_domyślna wartość_czasu 제한 0은 별도 gniazdo_WARTOŚĆ 기한을 설정하지 않지만 JVM polecenie identyfikator/jądro_WARTOŚĆ Wykonaj_polecenie 기한은 여전히 적용된다.

zewnętrzny_WARTOŚĆ cyfra_WARTOŚĆ IPv4 TCP/UDP는 lwIP/SLIP로 지원한다. rzeczywisty_dane Ethernet/Wi-Fi 드라이버, DNS·TLS·HTTP biblioteka 전체는 미지원이다. `java.net`의 모든 메서드와 옵션, `SocketChannel`/select, SSL, shutdownInput/Output는 아직 없다. [test_Stream.java](testy/자바/test_Stream.java)는 rzeczywisty_dane 송수신·EOF·기한·Połącz 회수의 testy 예제다.

## 한글 Python

게스트 vi에서 한글 이름을 사용해 작성한다.

```python
WARTOŚĆ = 21

def 두배(cyfra_WARTOŚĆ):
    return cyfra_WARTOŚĆ * 2

print("WYNIK:", 두배(WARTOŚĆ))
```

Store_WARTOŚĆ 후 `python 인사.py`로 실행한다. 실행기는 MicroPython 1.24.1이다. Python 문법 키워드는 그대로 사용하며 FUNKCJA_WARTOŚĆ·zmienna_WARTOŚĆ·nazwa_pliku 이름과 문자열을 한글로 쓴다.

[polski.py](예제/한글코딩/polski.py)를 같은 디렉터리에 두면 Dalej_towar 별칭을 사용할 identyfikator 있다.

```python
import polski
polski.zapis_Plik("인사.txt", "안녕하세요")
polski.pozycja_wyjścia(polski.파일읽기("인사.txt").decode())
```

pozycja_wyjścia·nazwa_pliku Odczyt/Zapis/삭제·표준 wejście_WARTOŚĆ·prostokąt·wartość_czasu·UDP를 연결한다. 기존 `udp_send`는 루프백, 새 `udp_sendto(fd, "10.0.2.2", port, data)`는 cyfra_WARTOŚĆ IPv4 Adres 전송이다. `wait_key()`는 화면을 확인할 때 interakcyjny 입력을 기다린다. Python 함수는 `jkoros` 내장 모듈을 통해 SVC를 사용한다. C ABI인 posix-kor statyczny_WARTOŚĆ 라이브러리를 Python이 직접 링크하는 구성은 아니다. CPython과 일반 rozszerzenie_WARTOŚĆ 모듈은 아직 없다. 제한형 `pip`의 źródło_drzewo 설치는 [Python pakiet plik_README_eb81d7d9](PYTHON_pakiet.md)를 따른다. [세 언어의 rzeczywisty_dane 예제](../../example/README.md).

## C·C++에서 posix-kor 호출

두 Język 모두 polski 헤더와 FUNKCJA_WARTOŚĆ 이름을 직접 사용한다. [인사.c](예제/한글코딩/인사.c), [인사.cpp](예제/한글코딩/인사.cpp)가 rzeczywisty_dane EL0 Wykonaj_polecenie testy 대상이다.

```c
#include "Plik_ABI.h"
#ifdef __cplusplus
extern "C"
#endif
int START_użytkownik_program(int argumenty) {
    (void)argumenty;
    const char 인사말[] = "안녕하세요\n";
    int 문서 = otwarty_Plik("인사.txt", R_W | 없으면만들기 | obcinać_Spis_treści, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = zapis_Plik_dane(문서, 인사말, sizeof(인사말) - 1);
    Zamknij_Plik(문서);
    zapis_Plik_dane(1, 인사말, sizeof(인사말) - 1); /* bieżący_towar interpretator_poleceń stdout */
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
```

파일은 게스트 vi로 작성할 identyfikator 있다. C는 게스트 `cc` 또는 host SDK, C++는 host SDK의 Clang++로 컴파일한다. 아래 예제는 기존 host SDK 경로다. 게스트 내부 GCC/Clang·libc/libstdc++ 전체를 탑재한 것은 아니다. SDK가 `.c`에는 C11, `.cpp`에는 C++11을 선택한다.

```sh
# 호스트에서 SDK generować·wyodrębnić
make sdk
mkdir -p build/sdk-work
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build/sdk-work
cd build/sdk-work/jkoros-native-sdk
python3 compile.py examples/인사.c -o 인사-c.elf
python3 compile.py examples/인사.cpp -o 인사-cpp.elf

# 프로젝트로 돌아와 별도 QEMU에서 rzeczywisty_dane Wykonaj_polecenie
cd /home/user/jkoros/platforms/rpi4-native
python3 narzędzia/Wykonaj_Plik.py build/sdk-work/jkoros-native-sdk/인사-c.elf
python3 narzędzia/Wykonaj_Plik.py build/sdk-work/jkoros-native-sdk/인사-cpp.elf
```

bieżący_towar GUI VM에서 실행하려면 `python3 narzędzia/Upload_Files.py ścieżka_2/인사-c.elf`의 출력을 게스트에 보내고 `run 인사-c.elf`를 입력한다. 게스트에서 작성한 소스의 전송은 `hex nazwa_pliku_SMS`으로 내용을 얻어 호스트에서 `bytes.fromhex(...)`로 복원할 identyfikator 있다. 호스트와 게스트의 nazwa_pliku 시스템은 별개다.

| polski Nazwa | C symbol | obcinać |
|---|---|---|
| otwarty_Plik/Zamknij_Plik | pk_open/pk_close | RAM nazwa_pliku, węzeł_równorzędny_WARTOŚĆ/절대 ścieżka_2 |
| 파일자료읽기/zapis_Plik_dane | pk_read/pk_write | nazwa_pliku, fd 0/1/2 표준 We_Wy, 연결형 gniazdo_WARTOŚĆ |
| szukać_Plik | pk_lseek | 처음기준/bieżący_korzeń/Koniec_źródło |
| rozmiar_pliku/set_Plik_długość | pk_size/pk_ftruncate | długość_WARTOŚĆ zapytanie_WARTOŚĆ/zmienić_WARTOŚĆ |
| usuń_Plik_wpis_nazwa | pk_unlink | nazwa_pliku Nazwa 삭제 |
| przekazywać_Files | pk_fsync | RAM이므로 -1, numer_błędu=ENOSYS |
| Twórca_uczestnik/BIND_ADRES | pk_socket/pk_bind | AF_INET, SOCK_DGRAM 또는 SOCK_STREAM |
| wysłać_datagram_dane/odbierać_datagram_dane | pk_sendto/pk_recvfrom | UDP 루프백 |
| POŁĄCZ_sieć | pk_connect | 연결형 루프백 |
| 통신연결기다리기 | pk_listen | chwileczkę_WARTOŚĆ Połącz 최대 4개 |
| akceptować_połączenie_sieciowe | pk_accept | bieżący_towar Adres 인수는 NULL/NULL만 wsparcie_WARTOŚĆ |
| 통신주소읽기 | pk_getsockname | 로컬 Adres/port_WARTOŚĆ |

`sieć_ABI.h`의 własny `pk_sockaddr_in`을 사용하며 port_WARTOŚĆ·주소는 `망차례짧은수`/`sieć_liczba_całkowita`로 변환한다. C gniazdo_WARTOŚĆ 호출은 비차단이며 dane/연결이 없으면 -1과 `numer_błędu=11`(EAGAIN)을 반환한다. 양수 We_Wy 결과가 요청보다 작을 identyfikator 있으므로 iteracja_WARTOŚĆ 처리한다. awaria_WARTOŚĆ 후에만 오류번호를 확인한다.

[Stream_WARTOŚĆ.c](예제/한글코딩/Stream_WARTOŚĆ.c)는 C에서 polski 이름으로 Połącz·accept·부분 Odczyt/Zapis·큐 포화·EOF를 처리하는 Wykonaj_polecenie 예제다. SDK의 `examples/Stream_WARTOŚĆ.c`를 같은 `compile.py`로 컴파일한다.

SDK는 **libposix-kor-user.a**를 링크한다. 호출 흐름은 C/C++ → rzeczywisty_dane polski C FUNKCJA_WARTOŚĆ 또는 호환용 `pk_*` → `svc #0` → 커널의 소유권·wskaźnik 검사 → Java RAM nazwa_pliku/루프백 또는 zewnętrzny_WARTOŚĆ lwIP TCP/UDP 구현이다. `libposix-kor-arm64.a`는 jądro_WARTOŚĆ 내부용이므로 EL0 프로그램에 링크하지 않는다. Linux 헤더나 Linux ELF와 혼합하지 않는다. 동적 Połącz, 표준 C printf, libstdc++/STL, wyjątek·RTTI는 제공하지 않으며 C++의 statyczny_WARTOŚĆ 생성자·lokalny_Scope obiekt_WARTOŚĆ 소멸자는 지원한다. 상세 INDEKS·Pamięć_dane 범위는 [użytkownik_Połącz_ABI.md](użytkownik_Połącz_ABI.md)를 참고한다.

## walidować

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`으로 새 기능을 각각 시험한다. `make test`는 기존 powłoka·VNC·JVM·AOT·jądro_WARTOŚĆ chronić_WARTOŚĆ 시험까지 포함한다. rzeczywisty_dane Tablica 대신 QEMU raspi4b에서 수행한다. 결과는 [Wstecz_towar GUI rozszerzenie_WARTOŚĆ walidować LOG_zapis](build/verification/release.json)과 [bieżący_towar CLR walidować LOG_zapis](build/verification/native-runtime-summary.json), [여러 interpretator_poleceń 화면](build/verification/windows/four-terminals.png), [Swing 화면](build/verification/swing/native-swing.png)을 참고한다.

implementacja 시 참고한 표준 API: [Socket](https://docs.oracle.com/javase/8/docs/api/java/net/Socket.html), [JFrame](https://docs.oracle.com/javase/8/docs/api/javax/swing/JFrame.html), [JButton](https://docs.oracle.com/javase/8/docs/api/javax/swing/JButton.html). 이 문서의 implementacja 범위가 위 표준 전체를 지원한다는 뜻은 아니다.

## polski 이름으로 직접 작성하는 창과 wątek_WARTOŚĆ

`example/java/PrzykładOkna.java`는 `실행할일.Uruchom`,
`동작받이.odbierać_akcja(akcja_powiadomienie)`, `przycisk`, `konkurs_kolejka.나중에실행`, `Uruchom_2()`을 쓴다.
własny JVM에 이 이름들의 obiekt_WARTOŚĆ·metoda_WARTOŚĆ·콜백을 직접 구현했으며 영어 Swing 객체를
보관하는 래퍼가 아니다. `pracownik`도 własny 스케줄러와 직접 연결된다.
세부 메서드와 기존 polski API에서의 변경은 [polski API 문서](한국어자바/plik_README_eb81d7d9.md)를 본다.

host javac는 dystrybucja_WARTOŚĆ JAR를 Klasa_WARTOŚĆ 경로로 사용한다.

```sh
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 ../../example/java/PrzykładOkna.java
python3 narzędzia/Wykonaj_polecenie.py --desktop --network --resolution 1920x1080
```

게스트에는 빌드한 예제가 `/example/java`에 설치된다.

```text
cd /example/java
java PrzykładOkna
```

직접 화면/wątek_WARTOŚĆ API와 `Uruchom_2()` 진입점은 własny JVM 전용이다.
전체 OpenJDK·Swing 재구현이나 일반 OpenJDK에서 같은 API의 실행을 보장하지 않는다.
기존 표준 `main(String[])` 프로그램은 계속 실행할 identyfikator 있다.
