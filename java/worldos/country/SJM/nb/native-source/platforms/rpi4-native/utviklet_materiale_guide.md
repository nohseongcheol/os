# eget 커널에서 vi·여러 Terminal·한글 프로그래밍 사용하기

norsk 통신·unntak 사용법은 [norsk Java API](한국어자바/Viktig_fil_eb81d7d9.md), FUNKSJON_VERDI·variabel_VERDI·Fil 이름의 변경과 어원 근거는 [명명 Viktig_fil_eb81d7d9](명명/Viktig_fil_eb81d7d9.md)를 참고한다.

대상은 `platforms/rpi4-native`의 eget AArch64 Java 커널이다. vi와 Java/Python/C/C++ 프로그램은 EL0에서 실행한다. Linux 실행판과 별도이며 아래 støtte_VERDI 목록은 전체 OpenJDK·Vim·POSIX 구현을 뜻하지 않는다.

게스트 `cc`/`jaot`, JAR 직접 Utfør_kommando, ekstern_VERDI TCP/UDP와 FTP는 [새 Utfør_kommando 매뉴얼](파일전송과번역.md)을 참고한다.

## GUI와 여러 Terminal

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, e_post **127.0.0.1:5902**로 연결한다. skjermbilde 위 **+ New terminal**, **Ctrl+Shift+T**로 터미널을 추가한다. 최대 네 개다. 위쪽 Terminal 버튼 또는 창을 클릭해 선택하고 **F6**으로 순환한다. 제목줄을 끌어서 옮기고 **HØYRE 위 X**를 클릭하면 닫힌다. 마지막 창을 닫아도 위쪽 Utfør_kommando 버튼으로 prøve_på_nytt_VERDI spalte_VERDI nummer 있다. 기존 `terminal`, `exit`, F12도 사용할 nummer 있다.

창마다 betalt_vare 디렉터리, Shell variabel_VERDI, Kommando LOG_POST, inndata_VERDI 중인 명령과 app_f5044b9b Utfør_kommando 상태를 보관한다. Fil 저장소는 공유한다. vi와 Swing의 이벤트 vent_VERDI 중에 다른 터미널로 전환하면 bruker Minne_data·레지스터·Fil/socket_VERDI 연결을 보존했다가 돌아올 때 재개한다. **betalt_vare 네 프로그램이 동시에 CPU에서 실행되는 선점형 스케줄러는 아니다.** 계산 중인 프로그램은 Neste_vare inndata_VERDI vent_VERDI 또는 기존 Utfør_kommando 기한까지 전환이 지연될 nummer 있다.

X로 터미널을 닫으면 그 터미널의 Utfør_kommando 중인 프로그램도 종료하며 서술자·소켓을 회수한다. 저장하지 않은 Rediger_VERDI 내용은 사라진다. 종료한 슬롯은 새 창에서 재사용한다. betalt_vare 모든 파일은 RAM에 있으며 VM 재시작 후에는 남지 않는다.

화면과 Vindu 판단은 게스트 커널이 처리한다. QEMU Utfør_kommando 도구는 VNC 키와 마우스 좌표를 UART 패킷으로 전달한다. faktisk_data Pi4 USB 입력기와 실물 부팅은 아직 검증하지 않았다. 일반 UART 셸은 `make run`, GUI Verktøy 종료는 vert 터미널의 Ctrl+C다.

## vi bruk_VERDI

```text
mkdir 작업
cd 작업
vi 인사.py
```

`vi`는 새로 구현한 **vi Kommando 부분집합** 편집기다. 내장 `build/user/vi.elf`를 보호된 bruker 영역에 적재한다. Fil 크기는 UTF-8 byte_VERDI speile_rot 16 KiB, 경로는 63바이트까지다. 디스크에 설치한 Vim/Neovim 바이너리를 실행하는 것이 아니다.

| tast_VERDI/Kommando | Handling |
|---|---|
| `i`, `a`, `I`, `A` | betalt_vare/Neste_vare Posisjon 또는 Linje 처음/끝에서 inndata_VERDI |
| `o`, `O` | 아래/위에 새 줄을 만들고 inndata_VERDI |
| Esc | 일반 MODUS_VERDI |
| `h j k l`, 방향키 | UTF-8 문자/Linje flytte_VERDI_83b651b8 |
| `0`, `$`, Home, End | Linje 처음/끝 |
| `gg`, `G`, `:INDEKS` | Fil 처음/마지막 Linje/overdra_VERDI Linje |
| PgUp, PgDn | skjermbilde enhet_VERDI_7c611f50 flytte_VERDI_83b651b8 |
| `x`, Delete | betalt_vare 문자 삭제 |
| `dd`, `yy`, `p` | Linje 삭제/kopiere_VERDI/lime_inn_SMS |
| `u` | 마지막 편집을 return_bro; 한 fase_VERDI 토글 |
| `/streng_VERDI`, `n` | 단순 streng_VERDI 검색/Neste_vare 일치; 정규식 없음 |
| `:w`, `:w 다른이름` | RAM Fil Store_VERDI/다른 경로로 Store_VERDI |
| `:q` | 변경이 없을 때 Utgang_app |
| `:q!` | 변경을 버리고 Utgang_app |
| `:wq`, `ZZ` | 저장하고 Utgang_app |

붙여 넣은 한글을 문자 경계에 맞춰 flytte_VERDI_83b651b8·삭제한다. 일반 vi의 수량 접두사, makro_VERDI, Innstillinger Fil, 플러그인, 정규식, 여러 버퍼/분할 Vindu, 문법 강조 등은 아직 없다. `--desktop`에서는 F9·Shift+Space·한/null_operand 키로 두벌식 조합을 전환한다. PC 입력기를 영어로 두고 Vindu vindu_Tittel `[KO]`에서 입력하며, `help ko`에 단축키를 표시한다. 완성된 Unicode 문자와 VNC의 명시적 붙여넣기도 전달한다.

vi와 Swing 프로그램은 **단독 Kommando**으로 실행한다. 파이프·리다이렉션·skript_VERDI·`;`/`&&`/`||`로 연결한 실행에서 interaktiv 대기를 시작하면 거부한다. inndata_VERDI 대기는 약 2초 CPU 기한을 갱신하지만 inndata_VERDI vent_VERDI 없이 무한 반복하는 프로그램은 기존처럼 종료한다.

## 한글 Java

vi에서 다음을 `인사.java`에 입력하고 Esc → `:wq`로 저장한다.

```java
public class 인사 {
    static int 더하기(int 첫째, int 둘째) { return 첫째 + 둘째; }
    public static void main(String[] Argumenter) {
        int total_VERDI = 더하기(20, 22);
        System.out.println("안녕하세요 · total_VERDI=" + total_VERDI);
    }
}
```

게스트 셸에서 실행한다.

```text
javac 인사.java
java 인사
```

한글 filnavn_SMS·klassenavn·metode_navn_SMS·변수명·문자열을 사용할 nummer 있다. **게스트 javac는 statisk_VERDI Java 부분집합**이다. objekt_VERDI·리스너·Swing·소켓을 사용하는 소스는 betalt_vare vert JDK에서 `javac --release 8 -encoding UTF-8`로 컴파일하고 eget JVM에 class를 올린다. eget JVM에서 지원하는 바이트코드/API 범위는 [자바실행환경.md](자바실행환경.md)를 따른다.

```sh
# vert
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java 시험/자바/Swing_test.java
python3 Verktøy/Upload_Filer.py build/my-java/Swing_test.class
```

`upload.py`는 게스트 `load`에 붙여 넣을 16진수 명령을 생성한다. Utgang 전체를 GUI 터미널에 보내면 업로드한다. 업로드 후 **별도로** `java Swing_test`을 실행한다. 종속 class가 있으면 각각 업로드한다. 패키지 class의 파일명은 `패키지.time_VERDI.class` 형식이다. 내장 norsk 라이브러리는 별도 업로드가 필요 없다. norsk Vindu API의 예제는 [한글창시험.java](시험/자바/한글창시험.java)이며 같은 방법으로 kompilere_kilde·업로드해 `java 한글창시험`으로 실행한다.

GUI가 필요 없는 단일 kilde_tre/클래스는 호스트의 `python3 Verktøy/Utfør_Fil.py Sti/인사.java`로 별도 QEMU에 업로드·Utfør_kommando·종료할 nummer 있다. interaktiv Swing에는 Utfør_kommando 후 bruker 입력을 유지하는 `make desktop`을 사용한다.

## eget JVM의 Swing klippe

실제로 제공하는 것은 **표준 패키지 이름으로 호출하는 eget Swing API 부분집합**이다. OpenJDK `java.desktop` 모듈이나 AWT 전체를 이식한 것은 아니다.

| API | Handling |
|---|---|
| `JFrame` | vindu_Tittel, Størrelse·Posisjon, vise_vindu, Lukk 정책, dispose |
| `JPanel` | barn_VERDI 요소를 담는 패널 |
| `JLabel` | 한글을 포함한 streng_VERDI vise_VERDI_487749b8·endre_VERDI |
| `JButton` | 버튼과 ActionListener klikk_VERDI Prosess_VERDI_oppføring |
| `JTextField` | 한 Linje UTF-8 inndata_VERDI, 삭제, getText/setText, Enter 이벤트 |
| 공통 | setBounds, setSize, add, getContentPane, repaint, validate |
| `SwingUtilities` | invokeLater, isEventDispatchThread |
| `ActionEvent` | getSource, getActionCommand, getID |

`setLayout(null)`과 `setBounds`로 배치한다. FlowLayout/BorderLayout/GridLayout, pack, 폰트·스타일 전체, 메뉴·테이블·트리·스크롤 패널, Java2D, 네이티브 AWT peer/JNI, 복잡한 문자 조판은 아직 없다. 이벤트 콜백은 eget JVM의 단일 이벤트 Utfør_kommando 흐름에서 처리하며 OpenJDK EDT 구현과 동일하지 않다. Vindu·요소는 Utfør_kommando 하나당 total_VERDI 32개, element_VERDI 글자는 최대 127 코드포인트다. standardverdi 서체와 색은 커널이 제공한다.

[Swing_test.java](시험/자바/Swing_test.java)는 Vindu·한글 kode_VERDI·tekstfelt·버튼·이벤트 처리의 Utfør_kommando 가능한 예제다. [eget Swing skjermbilde](build/verification/swing/native-swing.png)을 참고한다.

norsk 라이브러리에는 다음을 추가했다. vert kompilere_kilde 시 `dist/jkoros-native-korean.jar`를 classpath에 넣는다.

- `norsk.eget.Vindu`: `Legg_til_element`, `vise_vindu`, `Lukk`.
- `norsk.eget.miniprogram`: `kode_VERDI`, `Knapp`, `tekstfelt` generere.
- `norsk.eget.kontakt_transport`: `Koble_til`, `듣기`, `motta`.
- 기존 `Utgang`, `문자`, `Fil`, `작업`, `oppføring_Liste`, `ordliste`, `통신`, `skjermbilde`, `kjerne_VERDI`도 유지한다.

## Java 네트워크

기존 `DatagramSocket`/`DatagramPacket`의 UDP 루프백에 `Socket`/`ServerSocket`의 **kjerne_VERDI 내부 연결형 byte_VERDI strøm_VERDI**을 추가했다. Fil/소켓과 마찬가지로 SVC를 통해 Java 커널이 전송한다. 물리 NIC의 TCP/IP 패킷 스택은 아니다.

```java
java.net.ServerSocket server_VERDI = new java.net.ServerSocket(9250);
java.net.Socket gjest_VERDI = new java.net.Socket("localhost", 9250);
java.net.Socket Koble_til = server_VERDI.accept();
gjest_VERDI.getOutputStream().write("안녕하세요".getBytes("UTF-8"));
byte[] MOTTATT_AVKAST_vare = new byte[64];
int lengde_VERDI = Koble_til.getInputStream().read(MOTTATT_AVKAST_vare);
Koble_til.close(); gjest_VERDI.close(); server_VERDI.close();
```

generere·Koble_til·accept·양방향 byte_VERDI/MATRISE_VERDI I_U·close·EOF·setSoTimeout을 지원한다. `String.getBytes()`와 UTF-8 이름을 지정한 getBytes도 제공한다. 루프백 주소는 `localhost`/`127.0.0.1`이다. 연결형 avslutte_en_samtale_peke 16개, motta_VERDI 버퍼당 1024바이트, vent_VERDI Koble_til 최대 4개이며 Java의 대기는 내부 가닥에 실행을 양보한다. standardverdi TID_VERDI 제한 0은 별도 socket_VERDI 기한을 설정하지 않지만 JVM Kommando nummer/kjerne_VERDI Utfør_kommando 기한은 여전히 적용된다.

ekstern_VERDI siffer_VERDI IPv4 TCP/UDP는 lwIP/SLIP로 지원한다. faktisk_data Ethernet/Wi-Fi 드라이버, DNS·TLS·HTTP bibliotek 전체는 미지원이다. `java.net`의 모든 메서드와 옵션, `SocketChannel`/select, SSL, shutdownInput/Output는 아직 없다. [test_strøm.java](시험/자바/test_strøm.java)는 faktisk_data 송수신·EOF·기한·Koble_til 회수의 시험 예제다.

## 한글 Python

게스트 vi에서 한글 이름을 사용해 작성한다.

```python
VERDI = 21

def 두배(siffer_VERDI):
    return siffer_VERDI * 2

print("KR:", 두배(VERDI))
```

Store_VERDI 후 `python 인사.py`로 실행한다. 실행기는 MicroPython 1.24.1이다. Python 문법 키워드는 그대로 사용하며 FUNKSJON_VERDI·variabel_VERDI·Fil 이름과 문자열을 한글로 쓴다.

[norsk.py](예제/한글코딩/norsk.py)를 같은 디렉터리에 두면 Neste_vare 별칭을 사용할 nummer 있다.

```python
import norsk
norsk.skrive_Fil("인사.txt", "안녕하세요")
norsk.Utgang(norsk.파일읽기("인사.txt").decode())
```

Utgang·Fil Les/Skriv/삭제·표준 inndata_VERDI·rektangel·TID_VERDI·UDP를 연결한다. 기존 `udp_send`는 루프백, 새 `udp_sendto(fd, "10.0.2.2", port, data)`는 siffer_VERDI IPv4 e_post 전송이다. `wait_key()`는 화면을 확인할 때 interaktiv 입력을 기다린다. Python 함수는 `jkoros` 내장 모듈을 통해 SVC를 사용한다. C ABI인 posix-kor statisk_VERDI 라이브러리를 Python이 직접 링크하는 구성은 아니다. CPython과 일반 filtype_VERDI 모듈은 아직 없다. 제한형 `pip`의 kilde_tre 설치는 [Python bunt Viktig_fil_eb81d7d9](PYTHON_bunt.md)를 따른다. [세 언어의 faktisk_data 예제](../../example/README.md).

## C·C++에서 posix-kor 호출

두 Språk 모두 norsk 헤더와 FUNKSJON_VERDI 이름을 직접 사용한다. [인사.c](예제/한글코딩/인사.c), [인사.cpp](예제/한글코딩/인사.cpp)가 faktisk_data EL0 Utfør_kommando 시험 대상이다.

```c
#include "파일규약.h"
#ifdef __cplusplus
extern "C"
#endif
int START_bruker_app(int Argumenter) {
    (void)Argumenter;
    const char 인사말[] = "안녕하세요\n";
    int 문서 = åpen_Fil("인사.txt", lese_og_skrive | 없으면만들기 | avkorte_Innhold, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = skrive_Fil_data(문서, 인사말, sizeof(인사말) - 1);
    Lukk_Fil(문서);
    skrive_Fil_data(1, 인사말, sizeof(인사말) - 1); /* betalt_vare Terminal stdout */
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
```

파일은 게스트 vi로 작성할 nummer 있다. C는 게스트 `cc` 또는 vert SDK, C++는 vert SDK의 Clang++로 컴파일한다. 아래 예제는 기존 vert SDK 경로다. 게스트 내부 GCC/Clang·libc/libstdc++ 전체를 탑재한 것은 아니다. SDK가 `.c`에는 C11, `.cpp`에는 C++11을 선택한다.

```sh
# 호스트에서 SDK generere·pakke_ut
make sdk
mkdir -p build/sdk-work
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build/sdk-work
cd build/sdk-work/jkoros-native-sdk
python3 compile.py examples/인사.c -o 인사-c.elf
python3 compile.py examples/인사.cpp -o 인사-cpp.elf

# 프로젝트로 돌아와 별도 QEMU에서 faktisk_data Utfør_kommando
cd /home/user/jkoros/platforms/rpi4-native
python3 Verktøy/Utfør_Fil.py build/sdk-work/jkoros-native-sdk/인사-c.elf
python3 Verktøy/Utfør_Fil.py build/sdk-work/jkoros-native-sdk/인사-cpp.elf
```

betalt_vare GUI VM에서 실행하려면 `python3 Verktøy/Upload_Filer.py Sti/인사-c.elf`의 출력을 게스트에 보내고 `run 인사-c.elf`를 입력한다. 게스트에서 작성한 소스의 전송은 `hex filnavn_SMS`으로 내용을 얻어 호스트에서 `bytes.fromhex(...)`로 복원할 nummer 있다. 호스트와 게스트의 Fil 시스템은 별개다.

| norsk Navn | C symbol | klippe |
|---|---|---|
| åpen_Fil/Lukk_Fil | pk_open/pk_close | RAM Fil, node_VERDI_6a3b6fa7/절대 Sti |
| 파일자료읽기/skrive_Fil_data | pk_read/pk_write | Fil, fd 0/1/2 표준 I_U, 연결형 socket_VERDI |
| søk_Fil | pk_lseek | 처음기준/betalt_rot/avslutte_en_samtale_origo |
| filstørrelse/sett_Fil_lengde | pk_size/pk_ftruncate | lengde_VERDI spørre_VERDI/endre_VERDI |
| fjerne_Fil_oppføring_navn | pk_unlink | Fil Navn 삭제 |
| 파일저장확정 | pk_fsync | RAM이므로 -1, feilnummer=ENOSYS |
| åpne_deltaker/BIND_e_post | pk_socket/pk_bind | AF_INET, SOCK_DGRAM 또는 SOCK_STREAM |
| sende_datagram_data/motta_datagram_data | pk_sendto/pk_recvfrom | UDP 루프백 |
| KOBLE_TIL_nettverk | pk_connect | 연결형 루프백 |
| 통신연결기다리기 | pk_listen | vent_VERDI Koble_til 최대 4개 |
| godta_nettverkstilkobling | pk_accept | betalt_vare e_post 인수는 NULL/NULL만 støtte_VERDI |
| 통신주소읽기 | pk_getsockname | 로컬 e_post/port_VERDI |

`통신규약.h`의 eget `pk_sockaddr_in`을 사용하며 port_VERDI·주소는 `망차례짧은수`/`nettverk_heltall`로 변환한다. C socket_VERDI 호출은 비차단이며 data/연결이 없으면 -1과 `feilnummer=11`(EAGAIN)을 반환한다. 양수 I_U 결과가 요청보다 작을 nummer 있으므로 sprint_VERDI 처리한다. feil_VERDI 후에만 오류번호를 확인한다.

[strøm_VERDI.c](예제/한글코딩/strøm_VERDI.c)는 C에서 norsk 이름으로 Koble_til·accept·부분 Les/Skriv·큐 포화·EOF를 처리하는 Utfør_kommando 예제다. SDK의 `examples/strøm_VERDI.c`를 같은 `compile.py`로 컴파일한다.

SDK는 **libposix-kor-user.a**를 링크한다. 호출 흐름은 C/C++ → faktisk_data norsk C FUNKSJON_VERDI 또는 호환용 `pk_*` → `svc #0` → 커널의 소유권·peker 검사 → Java RAM Fil/루프백 또는 ekstern_VERDI lwIP TCP/UDP 구현이다. `libposix-kor-arm64.a`는 kjerne_VERDI 내부용이므로 EL0 프로그램에 링크하지 않는다. Linux 헤더나 Linux ELF와 혼합하지 않는다. 동적 Koble_til, 표준 C printf, libstdc++/STL, unntak·RTTI는 제공하지 않으며 C++의 statisk_VERDI 생성자·lokal_Omfang objekt_VERDI 소멸자는 지원한다. 상세 INDEKS·Minne_data 범위는 [사용자호출규약.md](사용자호출규약.md)를 참고한다.

## bekrefte_5fb2b747

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`으로 새 기능을 각각 시험한다. `make test`는 기존 Shell·VNC·JVM·AOT·kjerne_VERDI beskytte_VERDI 시험까지 포함한다. faktisk_data Tavle 대신 QEMU raspi4b에서 수행한다. 결과는 [Forrige_vare GUI filtype_VERDI bekrefte_5fb2b747 LOG_POST](build/verification/release.json)과 [betalt_vare CLR bekrefte_5fb2b747 LOG_POST](build/verification/native-runtime-summary.json), [여러 Terminal skjermbilde](build/verification/windows/four-terminals.png), [Swing skjermbilde](build/verification/swing/native-swing.png)을 참고한다.

구현 시 참고한 표준 API: [Socket](https://docs.oracle.com/javase/8/docs/api/java/net/Socket.html), [JFrame](https://docs.oracle.com/javase/8/docs/api/javax/swing/JFrame.html), [JButton](https://docs.oracle.com/javase/8/docs/api/javax/swing/JButton.html). 이 문서의 구현 범위가 위 표준 전체를 지원한다는 뜻은 아니다.

## norsk 이름으로 직접 작성하는 창과 tråd_VERDI

`example/java/Vinduseksempel.java`는 `실행할일.Kjør`,
`동작받이.motta_Gjøremål(Gjøremål_notice)`, `Knapp`, `hendelse_kø.나중에실행`, `Kjør_2()`을 쓴다.
eget JVM에 이 이름들의 objekt_VERDI·metode_VERDI·콜백을 직접 구현했으며 영어 Swing 객체를
보관하는 래퍼가 아니다. `arbeider`도 eget 스케줄러와 직접 연결된다.
세부 메서드와 기존 norsk API에서의 변경은 [norsk API 문서](한국어자바/Viktig_fil_eb81d7d9.md)를 본다.

vert javac는 distribusjon_VERDI JAR를 time_VERDI 경로로 사용한다.

```sh
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 ../../example/java/Vinduseksempel.java
python3 Verktøy/Utfør_kommando.py --desktop --network --resolution 1920x1080
```

게스트에는 빌드한 예제가 `/example/java`에 설치된다.

```text
cd /example/java
java Vinduseksempel
```

직접 skjermbilde/tråd_VERDI API와 `Kjør_2()` 진입점은 eget JVM 전용이다.
전체 OpenJDK·Swing 재구현이나 일반 OpenJDK에서 같은 API의 실행을 보장하지 않는다.
기존 표준 `main(String[])` 프로그램은 계속 실행할 nummer 있다.
