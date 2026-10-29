# Eigen 커널에서 vi·여러 terminal·한글 프로그래밍 사용하기

Nederlands communicatie·uitzondering 사용법은 [Nederlands Java API](한국어자바/LEESMIJ_eb81d7d9.md), FUNCTIE_WAARDE·variabele_WAARDE·bestand 이름의 변경과 어원 근거는 [명명 LEESMIJ_eb81d7d9](명명/LEESMIJ_eb81d7d9.md)를 참고한다.

대상은 `platforms/rpi4-native`의 Eigen AArch64 Java 커널이다. vi와 Java/Python/C/C++ 프로그램은 EL0에서 실행한다. Linux 실행판과 별도이며 아래 steun_WAARDE 목록은 전체 OpenJDK·Vim·POSIX 구현을 뜻하지 않는다.

게스트 `cc`/`jaot`, JAR 직접 Uitvoeren_opdracht, extern_WAARDE TCP/UDP와 FTP는 [새 Uitvoeren_opdracht 매뉴얼](파일전송과번역.md)을 참고한다.

## GUI와 여러 terminal

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, ADRES **127.0.0.1:5902**로 연결한다. scherm 위 **+ New terminal**, **Ctrl+Shift+T**로 터미널을 추가한다. 최대 네 개다. 위쪽 terminal 버튼 또는 창을 클릭해 선택하고 **F6**으로 순환한다. 제목줄을 끌어서 옮기고 **recht 위 X**를 클릭하면 닫힌다. 마지막 창을 닫아도 위쪽 Uitvoeren_opdracht 버튼으로 opnieuw_proberen_WAARDE KOLOM_WAARDE nummer 있다. 기존 `terminal`, `exit`, F12도 사용할 nummer 있다.

창마다 actueel_item 디렉터리, Shell variabele_WAARDE, opdracht LOG_RECORD, invoer_WAARDE 중인 명령과 app_f5044b9b Uitvoeren_opdracht 상태를 보관한다. bestand 저장소는 공유한다. vi와 Swing의 이벤트 wachten_WAARDE 중에 다른 터미널로 전환하면 gebruikersruimte Geheugen_gegevens·레지스터·bestand/socket_WAARDE 연결을 보존했다가 돌아올 때 재개한다. **actueel_item 네 프로그램이 동시에 CPU에서 실행되는 선점형 스케줄러는 아니다.** 계산 중인 프로그램은 Volgende_item invoer_WAARDE wachten_WAARDE 또는 기존 Uitvoeren_opdracht 기한까지 전환이 지연될 nummer 있다.

X로 터미널을 닫으면 그 터미널의 Uitvoeren_opdracht 중인 프로그램도 종료하며 서술자·소켓을 회수한다. 저장하지 않은 Bewerk_WAARDE 내용은 사라진다. 종료한 슬롯은 새 창에서 재사용한다. actueel_item 모든 파일은 RAM에 있으며 VM 재시작 후에는 남지 않는다.

화면과 Venster 판단은 게스트 커널이 처리한다. QEMU Uitvoeren_opdracht 도구는 VNC 키와 마우스 좌표를 UART 패킷으로 전달한다. werkelijk_gegevens Pi4 USB 입력기와 실물 부팅은 아직 검증하지 않았다. 일반 UART 셸은 `make run`, GUI hulpmiddelen 종료는 host 터미널의 Ctrl+C다.

## vi gebruik_WAARDE

```text
mkdir 작업
cd 작업
vi 인사.py
```

`vi`는 새로 구현한 **vi opdracht 부분집합** 편집기다. 내장 `build/user/vi.elf`를 보호된 gebruikersruimte 영역에 적재한다. bestand 크기는 UTF-8 byte_WAARDE Taken_wortel 16 KiB, 경로는 63바이트까지다. 디스크에 설치한 Vim/Neovim 바이너리를 실행하는 것이 아니다.

| toets_WAARDE/opdracht | Actie |
|---|---|
| `i`, `a`, `I`, `A` | actueel_item/Volgende_item positie 또는 invoerregel 처음/끝에서 invoer_WAARDE |
| `o`, `O` | 아래/위에 새 줄을 만들고 invoer_WAARDE |
| Esc | 일반 MODUS_WAARDE |
| `h j k l`, 방향키 | UTF-8 문자/invoerregel verplaatsen_WAARDE_83b651b8 |
| `0`, `$`, Home, End | invoerregel 처음/끝 |
| `gg`, `G`, `:INDEX` | bestand 처음/마지막 invoerregel/Toewijzen_WAARDE invoerregel |
| PgUp, PgDn | scherm les_WAARDE_7c611f50 verplaatsen_WAARDE_83b651b8 |
| `x`, Delete | actueel_item 문자 삭제 |
| `dd`, `yy`, `p` | invoerregel 삭제/kopiëren_WAARDE/plakken_sms |
| `u` | 마지막 편집을 Retour_brug; 한 fase_WAARDE 토글 |
| `/tekenreeks_WAARDE`, `n` | 단순 tekenreeks_WAARDE 검색/Volgende_item 일치; 정규식 없음 |
| `:w`, `:w 다른이름` | RAM bestand Store_WAARDE/다른 경로로 Store_WAARDE |
| `:q` | 변경이 없을 때 Einde_app |
| `:q!` | 변경을 버리고 Einde_app |
| `:wq`, `ZZ` | 저장하고 Einde_app |

붙여 넣은 한글을 문자 경계에 맞춰 verplaatsen_WAARDE_83b651b8·삭제한다. 일반 vi의 수량 접두사, macro_WAARDE, Instellingen bestand, 플러그인, 정규식, 여러 버퍼/분할 Venster, 문법 강조 등은 아직 없다. `--desktop`에서는 F9·Shift+Space·한/nul_operand 키로 두벌식 조합을 전환한다. PC 입력기를 영어로 두고 Venster venster_Titel `[KO]`에서 입력하며, `help ko`에 단축키를 표시한다. 완성된 Unicode 문자와 VNC의 명시적 붙여넣기도 전달한다.

vi와 Swing 프로그램은 **단독 opdracht**으로 실행한다. 파이프·리다이렉션·script_WAARDE·`;`/`&&`/`||`로 연결한 실행에서 interactief 대기를 시작하면 거부한다. invoer_WAARDE 대기는 약 2초 CPU 기한을 갱신하지만 invoer_WAARDE wachten_WAARDE 없이 무한 반복하는 프로그램은 기존처럼 종료한다.

## 한글 Java

vi에서 다음을 `인사.java`에 입력하고 Esc → `:wq`로 저장한다.

```java
public class 인사 {
    static int 더하기(int 첫째, int 둘째) { return 첫째 + 둘째; }
    public static void main(String[] argumenten) {
        int totaal_WAARDE = 더하기(20, 22);
        System.out.println("안녕하세요 · totaal_WAARDE=" + totaal_WAARDE);
    }
}
```

게스트 셸에서 실행한다.

```text
javac 인사.java
java 인사
```

한글 bestandsnaam_sms·klassenaam·methode_naam_sms·변수명·문자열을 사용할 nummer 있다. **게스트 javac는 statisch_WAARDE Java 부분집합**이다. object_WAARDE·리스너·Swing·소켓을 사용하는 소스는 actueel_item host JDK에서 `javac --release 8 -encoding UTF-8`로 컴파일하고 Eigen JVM에 class를 올린다. Eigen JVM에서 지원하는 바이트코드/API 범위는 [자바실행환경.md](자바실행환경.md)를 따른다.

```sh
# host
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java tests/자바/Swing_test.java
python3 hulpmiddelen/Upload_Files.py build/my-java/Swing_test.class
```

`upload.py`는 게스트 `load`에 붙여 넣을 16진수 명령을 생성한다. tekstuitvoer 전체를 GUI 터미널에 보내면 업로드한다. 업로드 후 **별도로** `java Swing_test`을 실행한다. 종속 class가 있으면 각각 업로드한다. 패키지 class의 파일명은 `패키지.les_WAARDE.class` 형식이다. 내장 Nederlands 라이브러리는 별도 업로드가 필요 없다. Nederlands Venster API의 예제는 [한글창시험.java](tests/자바/한글창시험.java)이며 같은 방법으로 compileren_bron·업로드해 `java 한글창시험`으로 실행한다.

GUI가 필요 없는 단일 bron_structuur/클래스는 호스트의 `python3 hulpmiddelen/Uitvoeren_Bestand.py pad/인사.java`로 별도 QEMU에 업로드·Uitvoeren_opdracht·종료할 nummer 있다. interactief Swing에는 Uitvoeren_opdracht 후 gebruikersruimte 입력을 유지하는 `make desktop`을 사용한다.

## Eigen JVM의 Swing clip

실제로 제공하는 것은 **표준 패키지 이름으로 호출하는 Eigen Swing API 부분집합**이다. OpenJDK `java.desktop` 모듈이나 AWT 전체를 이식한 것은 아니다.

| API | Actie |
|---|---|
| `JFrame` | venster_Titel, Grootte·positie, weergeven_venster, Sluiten 정책, dispose |
| `JPanel` | kind_WAARDE 요소를 담는 패널 |
| `JLabel` | 한글을 포함한 tekenreeks_WAARDE weergeven_WAARDE·wijzigen_WAARDE |
| `JButton` | 버튼과 ActionListener click_WAARDE Proces_WAARDE_invoer |
| `JTextField` | 한 invoerregel UTF-8 invoer_WAARDE, 삭제, getText/setText, Enter 이벤트 |
| 공통 | setBounds, setSize, add, getContentPane, repaint, validate |
| `SwingUtilities` | invokeLater, isEventDispatchThread |
| `ActionEvent` | getSource, getActionCommand, getID |

`setLayout(null)`과 `setBounds`로 배치한다. FlowLayout/BorderLayout/GridLayout, pack, 폰트·스타일 전체, 메뉴·테이블·트리·스크롤 패널, Java2D, 네이티브 AWT peer/JNI, 복잡한 문자 조판은 아직 없다. 이벤트 콜백은 Eigen JVM의 단일 이벤트 Uitvoeren_opdracht 흐름에서 처리하며 OpenJDK EDT 구현과 동일하지 않다. Venster·요소는 Uitvoeren_opdracht 하나당 totaal_WAARDE 32개, element_WAARDE 글자는 최대 127 코드포인트다. standaardwaarde 서체와 색은 커널이 제공한다.

[Swing_test.java](tests/자바/Swing_test.java)는 Venster·한글 tag_WAARDE·tekstveld·버튼·이벤트 처리의 Uitvoeren_opdracht 가능한 예제다. [Eigen Swing scherm](build/verification/swing/native-swing.png)을 참고한다.

Nederlands 라이브러리에는 다음을 추가했다. host compileren_bron 시 `dist/jkoros-native-korean.jar`를 classpath에 넣는다.

- `Nederlands.Eigen.Venster`: `Toevoegen_element`, `weergeven_venster`, `Sluiten`.
- `Nederlands.Eigen.schermelement`: `tag_WAARDE`, `knop`, `tekstveld` genereren.
- `Nederlands.Eigen.verbinding_transport`: `Verbinden`, `듣기`, `ontvangen`.
- 기존 `tekstuitvoer`, `문자`, `bestand`, `작업`, `invoer_Lijst_f07b3200`, `woordenlijst`, `communicatie`, `scherm`, `kernel_WAARDE`도 유지한다.

## Java 네트워크

기존 `DatagramSocket`/`DatagramPacket`의 UDP 루프백에 `Socket`/`ServerSocket`의 **kernel_WAARDE 내부 연결형 byte_WAARDE Stream_WAARDE**을 추가했다. bestand/소켓과 마찬가지로 SVC를 통해 Java 커널이 전송한다. 물리 NIC의 TCP/IP 패킷 스택은 아니다.

```java
java.net.ServerSocket server_WAARDE = new java.net.ServerSocket(9250);
java.net.Socket gast_WAARDE = new java.net.Socket("localhost", 9250);
java.net.Socket Verbinden = server_WAARDE.accept();
gast_WAARDE.getOutputStream().write("안녕하세요".getBytes("UTF-8"));
byte[] OPBRENGST_item = new byte[64];
int tijdsduur_WAARDE = Verbinden.getInputStream().read(OPBRENGST_item);
Verbinden.close(); gast_WAARDE.close(); server_WAARDE.close();
```

genereren·Verbinden·accept·양방향 byte_WAARDE/MATRIX_WAARDE I_O·close·EOF·setSoTimeout을 지원한다. `String.getBytes()`와 UTF-8 이름을 지정한 getBytes도 제공한다. 루프백 주소는 `localhost`/`127.0.0.1`이다. 연결형 beëindigen_punt 16개, ontvangen_WAARDE 버퍼당 1024바이트, wachten_WAARDE Verbinden 최대 4개이며 Java의 대기는 내부 가닥에 실행을 양보한다. standaardwaarde TIJD_WAARDE 제한 0은 별도 socket_WAARDE 기한을 설정하지 않지만 JVM opdracht nummer/kernel_WAARDE Uitvoeren_opdracht 기한은 여전히 적용된다.

extern_WAARDE cijfer_WAARDE IPv4 TCP/UDP는 lwIP/SLIP로 지원한다. werkelijk_gegevens Ethernet/Wi-Fi 드라이버, DNS·TLS·HTTP bibliotheek 전체는 미지원이다. `java.net`의 모든 메서드와 옵션, `SocketChannel`/select, SSL, shutdownInput/Output는 아직 없다. [test_Stream.java](tests/자바/test_Stream.java)는 werkelijk_gegevens 송수신·EOF·기한·Verbinden 회수의 tests 예제다.

## 한글 Python

게스트 vi에서 한글 이름을 사용해 작성한다.

```python
WAARDE = 21

def 두배(cijfer_WAARDE):
    return cijfer_WAARDE * 2

print("resultaat:", 두배(WAARDE))
```

Store_WAARDE 후 `python 인사.py`로 실행한다. 실행기는 MicroPython 1.24.1이다. Python 문법 키워드는 그대로 사용하며 FUNCTIE_WAARDE·variabele_WAARDE·bestand 이름과 문자열을 한글로 쓴다.

[Nederlands.py](예제/한글코딩/Nederlands.py)를 같은 디렉터리에 두면 Volgende_item 별칭을 사용할 nummer 있다.

```python
import Nederlands
Nederlands.schrijven_Bestand("인사.txt", "안녕하세요")
Nederlands.tekstuitvoer(Nederlands.파일읽기("인사.txt").decode())
```

tekstuitvoer·bestand Lezen/Schrijven/삭제·표준 invoer_WAARDE·rechthoek·TIJD_WAARDE·UDP를 연결한다. 기존 `udp_send`는 루프백, 새 `udp_sendto(fd, "10.0.2.2", port, data)`는 cijfer_WAARDE IPv4 ADRES 전송이다. `wait_key()`는 화면을 확인할 때 interactief 입력을 기다린다. Python 함수는 `jkoros` 내장 모듈을 통해 SVC를 사용한다. C ABI인 posix-kor statisch_WAARDE 라이브러리를 Python이 직접 링크하는 구성은 아니다. CPython과 일반 extensie_WAARDE 모듈은 아직 없다. 제한형 `pip`의 bron_structuur 설치는 [Python bundel LEESMIJ_eb81d7d9](PYTHON_bundel.md)를 따른다. [세 언어의 werkelijk_gegevens 예제](../../example/README.md).

## C·C++에서 posix-kor 호출

두 Taal 모두 Nederlands 헤더와 FUNCTIE_WAARDE 이름을 직접 사용한다. [인사.c](예제/한글코딩/인사.c), [인사.cpp](예제/한글코딩/인사.cpp)가 werkelijk_gegevens EL0 Uitvoeren_opdracht tests 대상이다.

```c
#include "파일규약.h"
#ifdef __cplusplus
extern "C"
#endif
int START_gebruiker_app(int argumenten) {
    (void)argumenten;
    const char 인사말[] = "안녕하세요\n";
    int Guides = open_Bestand("인사.txt", lezen_schrijven | 없으면만들기 | afkappen_Inhoud, 0600);
    if (Guides < 0) return 1;
    입출력결과형 기록한수 = schrijven_Bestand_gegevens(Guides, 인사말, sizeof(인사말) - 1);
    Sluiten_Bestand(Guides);
    schrijven_Bestand_gegevens(1, 인사말, sizeof(인사말) - 1); /* actueel_item terminal stdout */
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
```

파일은 게스트 vi로 작성할 nummer 있다. C는 게스트 `cc` 또는 host SDK, C++는 host SDK의 Clang++로 컴파일한다. 아래 예제는 기존 host SDK 경로다. 게스트 내부 GCC/Clang·libc/libstdc++ 전체를 탑재한 것은 아니다. SDK가 `.c`에는 C11, `.cpp`에는 C++11을 선택한다.

```sh
# 호스트에서 SDK genereren·uitpakken
make sdk
mkdir -p build/sdk-work
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build/sdk-work
cd build/sdk-work/jkoros-native-sdk
python3 compile.py examples/인사.c -o 인사-c.elf
python3 compile.py examples/인사.cpp -o 인사-cpp.elf

# 프로젝트로 돌아와 별도 QEMU에서 werkelijk_gegevens Uitvoeren_opdracht
cd /home/user/jkoros/platforms/rpi4-native
python3 hulpmiddelen/Uitvoeren_Bestand.py build/sdk-work/jkoros-native-sdk/인사-c.elf
python3 hulpmiddelen/Uitvoeren_Bestand.py build/sdk-work/jkoros-native-sdk/인사-cpp.elf
```

actueel_item GUI VM에서 실행하려면 `python3 hulpmiddelen/Upload_Files.py pad/인사-c.elf`의 출력을 게스트에 보내고 `run 인사-c.elf`를 입력한다. 게스트에서 작성한 소스의 전송은 `hex bestandsnaam_sms`으로 내용을 얻어 호스트에서 `bytes.fromhex(...)`로 복원할 nummer 있다. 호스트와 게스트의 bestand 시스템은 별개다.

| Nederlands Naam | C symbool | clip |
|---|---|---|
| open_Bestand/Sluiten_Bestand | pk_open/pk_close | RAM bestand, peer_WAARDE/절대 pad |
| 파일자료읽기/schrijven_Bestand_gegevens | pk_read/pk_write | bestand, fd 0/1/2 표준 I_O, 연결형 socket_WAARDE |
| zoeken_Bestand | pk_lseek | 처음기준/actueel_wortel/beëindigen_oorsprong |
| bestandsgrootte/set_Bestand_tijdsduur | pk_size/pk_ftruncate | tijdsduur_WAARDE query_WAARDE/wijzigen_WAARDE |
| verwijderen_Bestand_invoer_naam | pk_unlink | bestand Naam 삭제 |
| doorvoeren_Files | pk_fsync | RAM이므로 -1, foutnummer=ENOSYS |
| maken_eindpunt/BIND_ADRES | pk_socket/pk_bind | AF_INET, SOCK_DGRAM 또는 SOCK_STREAM |
| e_mailen_datagram_gegevens/ontvangen_datagram_gegevens | pk_sendto/pk_recvfrom | UDP 루프백 |
| VERBINDEN_net | pk_connect | 연결형 루프백 |
| 통신연결기다리기 | pk_listen | wachten_WAARDE Verbinden 최대 4개 |
| accepteren_netwerkverbinding | pk_accept | actueel_item ADRES 인수는 NULL/NULL만 steun_WAARDE |
| 통신주소읽기 | pk_getsockname | 로컬 ADRES/poort_WAARDE |

`통신규약.h`의 Eigen `pk_sockaddr_in`을 사용하며 poort_WAARDE·주소는 `망차례짧은수`/`net_geheel_getal`로 변환한다. C socket_WAARDE 호출은 비차단이며 gegevens/연결이 없으면 -1과 `foutnummer=11`(EAGAIN)을 반환한다. 양수 I_O 결과가 요청보다 작을 nummer 있으므로 sprint_WAARDE 처리한다. fout_WAARDE 후에만 오류번호를 확인한다.

[Stream_WAARDE.c](예제/한글코딩/Stream_WAARDE.c)는 C에서 Nederlands 이름으로 Verbinden·accept·부분 Lezen/Schrijven·큐 포화·EOF를 처리하는 Uitvoeren_opdracht 예제다. SDK의 `examples/Stream_WAARDE.c`를 같은 `compile.py`로 컴파일한다.

SDK는 **libposix-kor-user.a**를 링크한다. 호출 흐름은 C/C++ → werkelijk_gegevens Nederlands C FUNCTIE_WAARDE 또는 호환용 `pk_*` → `svc #0` → 커널의 소유권·wijzer 검사 → Java RAM bestand/루프백 또는 extern_WAARDE lwIP TCP/UDP 구현이다. `libposix-kor-arm64.a`는 kernel_WAARDE 내부용이므로 EL0 프로그램에 링크하지 않는다. Linux 헤더나 Linux ELF와 혼합하지 않는다. 동적 Verbinden, 표준 C printf, libstdc++/STL, uitzondering·RTTI는 제공하지 않으며 C++의 statisch_WAARDE 생성자·lokaal_scope object_WAARDE 소멸자는 지원한다. 상세 INDEX·Geheugen_gegevens 범위는 [사용자호출규약.md](사용자호출규약.md)를 참고한다.

## valideren

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`으로 새 기능을 각각 시험한다. `make test`는 기존 Shell·VNC·JVM·AOT·kernel_WAARDE beschermen_WAARDE 시험까지 포함한다. werkelijk_gegevens Bord 대신 QEMU raspi4b에서 수행한다. 결과는 [Vorige_item GUI extensie_WAARDE valideren LOG_RECORD](build/verification/release.json)과 [actueel_item CLR valideren LOG_RECORD](build/verification/native-runtime-summary.json), [여러 terminal scherm](build/verification/windows/four-terminals.png), [Swing scherm](build/verification/swing/native-swing.png)을 참고한다.

implementatie 시 참고한 표준 API: [Socket](https://docs.oracle.com/javase/8/docs/api/java/net/Socket.html), [JFrame](https://docs.oracle.com/javase/8/docs/api/javax/swing/JFrame.html), [JButton](https://docs.oracle.com/javase/8/docs/api/javax/swing/JButton.html). 이 문서의 implementatie 범위가 위 표준 전체를 지원한다는 뜻은 아니다.

## Nederlands 이름으로 직접 작성하는 창과 thread_WAARDE

`example/java/Venstervoorbeeld.java`는 `실행할일.Uitvoeren`,
`동작받이.ontvangen_Actie(Actie_kennisgeving)`, `knop`, `gebeurtenis_wachtrij.나중에실행`, `starten()`을 쓴다.
Eigen JVM에 이 이름들의 object_WAARDE·methode_WAARDE·콜백을 직접 구현했으며 영어 Swing 객체를
보관하는 래퍼가 아니다. `achtergrondwerker`도 Eigen 스케줄러와 직접 연결된다.
세부 메서드와 기존 Nederlands API에서의 변경은 [Nederlands API Guides](한국어자바/LEESMIJ_eb81d7d9.md)를 본다.

host javac는 distributie_WAARDE JAR를 les_WAARDE 경로로 사용한다.

```sh
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 ../../example/java/Venstervoorbeeld.java
python3 hulpmiddelen/Uitvoeren_opdracht.py --desktop --network --resolution 1920x1080
```

게스트에는 빌드한 예제가 `/example/java`에 설치된다.

```text
cd /example/java
java Venstervoorbeeld
```

직접 scherm/thread_WAARDE API와 `starten()` 진입점은 Eigen JVM 전용이다.
전체 OpenJDK·Swing 재구현이나 일반 OpenJDK에서 같은 API의 실행을 보장하지 않는다.
기존 표준 `main(String[])` 프로그램은 계속 실행할 nummer 있다.
