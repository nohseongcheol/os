# eigen 커널에서 vi·여러 terminal·HangulText 프로그래밍 사용하기

Deutsch Kommunikation·ausnahme 사용법은 [Deutsch Java API](DeutschJava/Anleitung.md), Funktion·variableWert·Datei 이름의 변경과 어원 근거는 [benennung Anleitung](benennung/Anleitung.md)를 참고한다.

대상은 `platforms/rpi4-native`의 eigen AArch64 Java 커널이다. vi와 Java/Python/C/C++ 프로그램은 EL0에서 실행한다. Linux 실행판과 별도이며 unterkanteWert unterstützungWert 목록은 전체 OpenJDK·Vim·POSIX 구현을 뜻하지 않는다.

게스트 `cc`/`jaot`, JAR 직접 befehlAusführen, externWert TCP/UDP와 FTP는 [새 befehlAusführen 매뉴얼](DateiÜbertragungUndÜbersetzungsvorgang.md)을 참고한다.

## GUI와 여러 terminal

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, adresse **127.0.0.1:5902**로 연결한다. Bildschirm oberkanteWert **+ New terminal**, **Ctrl+Shift+T**로 터미널을 추가한다. höchstwertWert 네 개다. obererSeiteRand terminal 버튼 또는 창을 클릭해 선택하고 **F6**으로 순환한다. 제목줄을 끌어서 옮기고 **rechts oberkanteWert X**를 클릭하면 닫힌다. letzterElementeintrag 창을 닫아도 obererSeiteRand befehlAusführen 버튼으로 erneutVersuchenWert spalteWert Zahl 있다. 기존 `terminal`, `exit`, F12도 사용할 Zahl 있다.

창마다 aktuellElementeintrag 디렉터리, befehlshülle variableWert, befehl protokolldateiAufzeichnung, Eingabewert 중인 명령과 Programm befehlAusführen 상태를 보관한다. Datei 저장소는 공유한다. vi와 Swing의 이벤트 wertWarten 중에 다른 터미널로 전환하면 Benutzer speicherDaten·레지스터·Datei/netzbuchseWert 연결을 보존했다가 돌아올 때 재개한다. **aktuellElementeintrag 네 프로그램이 동시에 CPU에서 실행되는 선점형 스케줄러는 아니다.** berechnung 중인 프로그램은 nächsterElementeintrag Eingabewert wertWarten 또는 기존 befehlAusführen 기한까지 전환이 지연될 Zahl 있다.

X로 터미널을 닫으면 그 터미널의 befehlAusführen 중인 프로그램도 종료하며 deskriptorEintrag·소켓을 회수한다. 저장하지 않은 bearbeitenWert 내용은 사라진다. 종료한 슬롯은 새 창에서 재사용한다. aktuellElementeintrag 모든 파일은 RAM에 있으며 VM 재시작 후에는 남지 않는다.

화면과 fenster 판단은 게스트 커널이 처리한다. QEMU befehlAusführen 도구는 VNC 키와 마우스 좌표를 UART 패킷으로 전달한다. tatsächlichDaten Pi4 USB 입력기와 physischHardware 부팅은 아직 검증하지 않았다. 일반 UART 셸은 `make run`, GUI Werkzeuge 종료는 Wirtssystem 터미널의 Ctrl+C다.

## vi benutzenWert

```text
mkdir Aufgabe
cd Aufgabe
vi Gruß.py
```

`vi`는 새로 구현한 **vi befehl 부분집합** 편집기다. 내장 `build/user/vi.elf`를 보호된 Benutzer 영역에 적재한다. Datei 크기는 UTF-8 byteWert projektWurzel 16 KiB, 경로는 63바이트까지다. 디스크에 설치한 Vim/Neovim 바이너리를 실행하는 것이 아니다.

| tasteWert/befehl | aktion |
|---|---|
| `i`, `a`, `I`, `A` | aktuellElementeintrag/nächsterElementeintrag position 또는 zeile anfänglichElementeintrag/끝에서 Eingabewert |
| `o`, `O` | unterkanteWert/위에 새 줄을 만들고 Eingabewert |
| Esc | 일반 betriebsartWert |
| `h j k l`, 방향키 | UTF-8 Zeichen/zeile bewegenWert |
| `0`, `$`, Home, End | zeile anfänglichElementeintrag/endung |
| `gg`, `G`, `:Nummer` | Datei anfänglichElementeintrag/letzterElementeintrag zeile/zuweisenWert zeile |
| PgUp, PgDn | Bildschirm einheitWert bewegenWert |
| `x`, Delete | aktuellElementeintrag Zeichen 삭제 |
| `dd`, `yy`, `p` | zeile 삭제/wertKopieren/einsetzenText |
| `u` | letzterElementeintrag 편집을 zurückkehrenBrücke; 한 stufeWert 토글 |
| `/Zeichenkette`, `n` | 단순 Zeichenkette 검색/nächsterElementeintrag istGleich; 정규식 fehlendMethode |
| `:w`, `:w 다른이름` | RAM Datei ablegenDatenWert/다른 경로로 ablegenDatenWert |
| `:q` | 변경이 없을 때 verlassenProzessProgramm |
| `:q!` | 변경을 버리고 verlassenProzessProgramm |
| `:wq`, `ZZ` | 저장하고 verlassenProzessProgramm |

붙여 넣은 한글을 Zeichen 경계에 맞춰 bewegenWert·삭제한다. 일반 vi의 수량 접두사, makroWert, einstellungen Datei, 플러그인, 정규식, 여러 버퍼/분할 fenster, 문법 강조 등은 아직 없다. `--desktop`에서는 F9·Shift+Space·한/nullwertOperand 키로 두벌식 조합을 전환한다. PC 입력기를 영어로 두고 fenster fensterTitel `[KO]`에서 입력하며, `help ko`에 단축키를 표시한다. 완성된 Unicode 문자와 VNC의 명시적 붙여넣기도 전달한다.

vi와 Swing 프로그램은 **단독 befehl**으로 실행한다. 파이프·리다이렉션·skriptWert·`;`/`&&`/`||`로 연결한 실행에서 interaktiv 대기를 시작하면 거부한다. Eingabewert 대기는 약 2초 CPU 기한을 갱신하지만 Eingabewert wertWarten 없이 무한 반복하는 프로그램은 기존처럼 종료한다.

## HangulText Java

vi에서 다음을 `Gruß.java`에 입력하고 Esc → `:wq`로 저장한다.

```java
public class Gruß {
    static int werteHinzufügen(int ersterOrdnungszahl, int zweiterOrdnungszahl) { return ersterOrdnungszahl + zweiterOrdnungszahl; }
    public static void main(String[] argumente) {
        int gesamtwertWert = werteHinzufügen(20, 22);
        System.out.println("안녕하세요 · gesamtwertWert=" + gesamtwertWert);
    }
}
```

게스트 셸에서 실행한다.

```text
javac Gruß.java
java Gruß
```

HangulText dateiNameText·klasseName·methodeNameText·변수명·문자열을 사용할 Zahl 있다. **게스트 javac는 statischWert Java 부분집합**이다. objektWert·리스너·Swing·소켓을 사용하는 소스는 aktuellElementeintrag Wirtssystem JDK에서 `javac --release 8 -encoding UTF-8`로 컴파일하고 eigen JVM에 class를 올린다. eigen JVM에서 지원하는 bytecode/API 범위는 [JavaLaufzeitUmgebung.md](JavaLaufzeitUmgebung.md)를 따른다.

```sh
# Wirtssystem
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java Prüfungen/Java/SwingPrüfung.java
python3 Werkzeuge/hochladenDateien.py build/my-java/SwingPrüfung.class
```

`upload.py`는 게스트 `load`에 붙여 넣을 16진수 명령을 생성한다. Ausgabe 전체를 GUI 터미널에 보내면 업로드한다. 업로드 danachStatuswert **별도로** `java SwingPrüfung`을 실행한다. 종속 class가 있으면 각각 업로드한다. 패키지 class의 파일명은 `패키지.klasseWert.class` 형식이다. 내장 Deutsch 라이브러리는 별도 업로드가 benötigtWert 없다. Deutsch fenster API의 예제는 [hangulFensterPrüfung.java](Prüfungen/Java/hangulFensterPrüfung.java)이며 같은 방법으로 quelltextÜbersetzen·업로드해 `java hangulFensterPrüfung`으로 실행한다.

GUI가 benötigtWert 없는 단일 quelltextBaum/클래스는 호스트의 `python3 Werkzeuge/dateiAusführen.py pfad/Gruß.java`로 별도 QEMU에 업로드·befehlAusführen·종료할 Zahl 있다. interaktiv Swing에는 befehlAusführen danachStatuswert Benutzer 입력을 유지하는 `make desktop`을 사용한다.

## eigen JVM의 Swing beschneiden

실제로 제공하는 것은 **표준 패키지 이름으로 호출하는 eigen Swing API 부분집합**이다. OpenJDK `java.desktop` 모듈이나 AWT 전체를 이식한 것은 아니다.

| API | aktion |
|---|---|
| `JFrame` | fensterTitel, größe·position, fensterAnzeigen, schließen 정책, dispose |
| `JPanel` | kindWert 요소를 담는 패널 |
| `JLabel` | 한글을 포함한 Zeichenkette wertAnzeigen·wertÄndern |
| `JButton` | 버튼과 ActionListener klickenWert prozessWertEintrag |
| `JTextField` | 한 zeile UTF-8 Eingabewert, 삭제, getText/setText, Enter 이벤트 |
| gemeinsamWert | setBounds, setSize, add, getContentPane, repaint, validate |
| `SwingUtilities` | invokeLater, isEventDispatchThread |
| `ActionEvent` | getSource, getActionCommand, getID |

`setLayout(null)`과 `setBounds`로 배치한다. FlowLayout/BorderLayout/GridLayout, pack, 폰트·스타일 전체, 메뉴·테이블·트리·스크롤 패널, Java2D, 네이티브 AWT peer/JNI, 복잡한 Zeichen 조판은 아직 없다. 이벤트 콜백은 eigen JVM의 단일 이벤트 befehlAusführen 흐름에서 처리하며 OpenJDK EDT 구현과 동일하지 않다. fenster·요소는 befehlAusführen 하나당 gesamtwertWert 32개, elementWert 글자는 höchstwertWert 127 코드포인트다. standardwertWert 서체와 색은 커널이 제공한다.

[SwingPrüfung.java](Prüfungen/Java/SwingPrüfung.java)는 fenster·HangulText kennzeichenWert·TextFeld·버튼·이벤트 처리의 befehlAusführen 가능한 예제다. [eigen Swing Bildschirm](build/verification/swing/native-swing.png)을 참고한다.

Deutsch 라이브러리에는 다음을 추가했다. Wirtssystem quelltextÜbersetzen 시 `dist/jkoros-native-korean.jar`를 classpath에 넣는다.

- `Deutsch.eigen.fenster`: `elementHinzufügen`, `fensterAnzeigen`, `schließen`.
- `Deutsch.eigen.Bedienelement`: `kennzeichenWert`, `schaltfläche`, `TextFeld` generieren.
- `Deutsch.eigen.verbindungBeförderung`: `verbinden`, `endpunktLauschen`, `empfangen`.
- 기존 `Ausgabe`, `Zeichen`, `Datei`, `Aufgabe`, `eintragListe`, `Wörterbuch`, `Kommunikation`, `Bildschirm`, `betriebskernWert`도 유지한다.

## Java 네트워크

기존 `DatagramSocket`/`DatagramPacket`의 UDP 루프백에 `Socket`/`ServerSocket`의 **betriebskernWert 내부 연결형 byteWert datenstromWert**을 추가했다. Datei/소켓과 마찬가지로 SVC를 통해 Java 커널이 전송한다. 물리 NIC의 TCP/IP 패킷 스택은 아니다.

```java
java.net.ServerSocket dienstanbieterWert = new java.net.ServerSocket(9250);
java.net.Socket gastWert = new java.net.Socket("localhost", 9250);
java.net.Socket verbinden = dienstanbieterWert.accept();
gastWert.getOutputStream().write("안녕하세요".getBytes("UTF-8"));
byte[] empfangenWertElementeintrag = new byte[64];
int Länge = verbinden.getInputStream().read(empfangenWertElementeintrag);
verbinden.close(); gastWert.close(); dienstanbieterWert.close();
```

generieren·verbinden·accept·양방향 byteWert/datenfeldWert eingabeAusgabe·close·EOF·setSoTimeout을 지원한다. `String.getBytes()`와 UTF-8 이름을 지정한 getBytes도 제공한다. 루프백 주소는 `localhost`/`127.0.0.1`이다. 연결형 endePunkt 16개, wertEmpfangen 버퍼당 1024바이트, wertWarten verbinden höchstwertWert 4개이며 Java의 대기는 내부 가닥에 실행을 양보한다. standardwertWert zeitWert grenzwertWert 0은 별도 netzbuchseWert 기한을 설정하지 않지만 JVM befehl Zahl/betriebskernWert befehlAusführen 기한은 여전히 적용된다.

externWert zifferWert IPv4 TCP/UDP는 lwIP/SLIP로 지원한다. tatsächlichDaten Ethernet/Wi-Fi 드라이버, DNS·TLS·HTTP bibliothek 전체는 미지원이다. `java.net`의 모든 메서드와 옵션, `SocketChannel`/select, SSL, shutdownInput/Output는 아직 없다. [datenstromPrüfung.java](Prüfungen/Java/datenstromPrüfung.java)는 tatsächlichDaten 송수신·EOF·기한·verbinden 회수의 Prüfungen 예제다.

## HangulText Python

게스트 vi에서 HangulText 이름을 사용해 작성한다.

```python
Wert = 21

def 두배(zifferWert):
    return zifferWert * 2

print("ergebnis:", 두배(Wert))
```

ablegenDatenWert danachStatuswert `python Gruß.py`로 실행한다. 실행기는 MicroPython 1.24.1이다. Python 문법 키워드는 그대로 사용하며 Funktion·variableWert·Datei 이름과 문자열을 한글로 쓴다.

[Deutsch.py](Beispiele/HangulKodierweise/Deutsch.py)를 같은 디렉터리에 두면 nächsterElementeintrag 별칭을 사용할 Zahl 있다.

```python
import Deutsch
Deutsch.dateiSchreiben("Gruß.txt", "안녕하세요")
Deutsch.Ausgabe(Deutsch.dateiLesen("Gruß.txt").decode())
```

Ausgabe·Datei lesen/schreiben/삭제·표준 Eingabewert·rechteck·zeitWert·UDP를 연결한다. 기존 `udp_send`는 루프백, 새 `udp_sendto(fd, "10.0.2.2", port, data)`는 zifferWert IPv4 adresse 전송이다. `wait_key()`는 화면을 확인할 때 interaktiv 입력을 기다린다. Python 함수는 `jkoros` 내장 모듈을 통해 SVC를 사용한다. C ABI인 posix-kor statischWert 라이브러리를 Python이 직접 링크하는 구성은 아니다. CPython과 일반 erweiterungWert 모듈은 아직 없다. 제한형 `pip`의 quelltextBaum 설치는 [Python Paket Anleitung](PythonBündel.md)를 따른다. [dreiWert 언어의 tatsächlichDaten Beispiele](../../example/README.md).

## C·C++에서 posix-kor aufrufen

두 Sprache alleErzeugenAbbild Deutsch 헤더와 Funktion 이름을 직접 사용한다. [Gruß.c](Beispiele/HangulKodierweise/Gruß.c), [Gruß.cpp](Beispiele/HangulKodierweise/Gruß.cpp)ersterOperand tatsächlichDaten EL0 befehlAusführen Prüfungen 대상이다.

```c
#include "DateiABI.h"
#ifdef __cplusplus
extern "C"
#endif
int benutzerProgrammStarten(int argumente) {
    (void)argumente;
    const char gruß[] = "안녕하세요\n";
    int Dokumentation = dateiÖffnen("Gruß.txt", LesenSchreiben | ErstellenFallsFehlend | KürzenInhalt, 0600);
    if (Dokumentation < 0) return 1;
    einAusgabeErgebnisTyp aufgezeichnetAnzahl = dateiDatenSchreiben(Dokumentation, gruß, sizeof(gruß) - 1);
    dateiSchließen(Dokumentation);
    dateiDatenSchreiben(1, gruß, sizeof(gruß) - 1); /* aktuellElementeintrag terminal stdout */
    return aufgezeichnetAnzahl == sizeof(gruß) - 1 ? 0 : 2;
}
```

파일은 게스트 vi로 작성할 Zahl 있다. C는 게스트 `cc` 또는 Wirtssystem SDK, C++는 Wirtssystem SDK의 Clang++로 컴파일한다. unterkanteWert 예제는 기존 Wirtssystem SDK 경로다. 게스트 내부 GCC/Clang·libc/libstdc++ 전체를 탑재한 것은 아니다. SDK가 `.c`에는 C11, `.cpp`에는 C++11을 선택한다.

```sh
# 호스트에서 SDK generieren·extrahieren
make sdk
mkdir -p build/sdk-work
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build/sdk-work
cd build/sdk-work/jkoros-native-sdk
python3 compile.py examples/Gruß.c -o Gruß-c.elf
python3 compile.py examples/Gruß.cpp -o Gruß-cpp.elf

# 프로젝트로 돌아와 별도 QEMU에서 tatsächlichDaten befehlAusführen
cd /home/user/jkoros/platforms/rpi4-native
python3 Werkzeuge/dateiAusführen.py build/sdk-work/jkoros-native-sdk/Gruß-c.elf
python3 Werkzeuge/dateiAusführen.py build/sdk-work/jkoros-native-sdk/Gruß-cpp.elf
```

aktuellElementeintrag GUI VM에서 실행하려면 `python3 Werkzeuge/hochladenDateien.py pfad/Gruß-c.elf`의 출력을 게스트에 보내고 `run Gruß-c.elf`를 입력한다. 게스트에서 작성한 소스의 전송은 `hex dateiNameText`으로 내용을 얻어 호스트에서 `bytes.fromhex(...)`로 복원할 Zahl 있다. 호스트와 게스트의 Datei 시스템은 별개다.

| Deutsch Name | C symbol | beschneiden |
|---|---|---|
| dateiÖffnen/dateiSchließen | pk_open/pk_close | RAM Datei, gegenstelleWert/절대 pfad |
| dateiDatenLesen/dateiDatenSchreiben | pk_read/pk_write | Datei, fd 0/1/2 표준 eingabeAusgabe, 연결형 netzbuchseWert |
| dateiPositionieren | pk_lseek | VonAnfang/aktuellWurzel/endeUrsprung |
| dateiGröße/dateiLängeSetzen | pk_size/pk_ftruncate | Länge abfragenWert/wertÄndern |
| dateiEintragNameEntfernen | pk_unlink | Datei Name 삭제 |
| bestätigenDateiSpeichergerät | pk_fsync | RAM이므로 -1, fehlerNummer=ENOSYS |
| endpunktErstellen/adresseZuordnen | pk_socket/pk_bind | AF_INET, SOCK_DGRAM 또는 SOCK_STREAM |
| datagrammDatenSenden/datagrammDatenEmpfangen | pk_sendto/pk_recvfrom | UDP 루프백 |
| netzwerkVerbinden | pk_connect | 연결형 루프백 |
| fürNetzwerkVerbindungWarten | pk_listen | wertWarten verbinden höchstwertWert 4개 |
| netzwerkVerbindungAnnehmen | pk_accept | aktuellElementeintrag adresse 인수는 NULL/NULL만 unterstützungWert |
| netzbuchseAdresseLesen | pk_getsockname | 로컬 adresse/portWert |

`NetzwerkABI.h`의 eigen `pk_sockaddr_in`을 사용하며 portWert·주소는 `netzwerkKurz`/`netzwerkGanzzahl`로 변환한다. C netzbuchseWert 호출은 비차단이며 Daten/연결이 없으면 -1과 `fehlerNummer=11`(EAGAIN)을 반환한다. 양수 eingabeAusgabe 결과가 요청보다 작을 Zahl 있으므로 wiederholungsschrittWert 처리한다. fehlschlagWert 후에만 오류번호를 확인한다.

[datenstromWert.c](Beispiele/HangulKodierweise/datenstromWert.c)는 C에서 Deutsch 이름으로 verbinden·accept·unterteilWert lesen/schreiben·큐 포화·EOF를 처리하는 befehlAusführen 예제다. SDK의 `examples/datenstromWert.c`를 같은 `compile.py`로 컴파일한다.

SDK는 **libposix-kor-user.a**를 링크한다. aufrufen 흐름은 C/C++ → tatsächlichDaten Deutsch C Funktion 또는 호환용 `pk_*` → `svc #0` → 커널의 소유권·zeiger Prüfpunkte → Java RAM Datei/루프백 또는 externWert lwIP TCP/UDP 구현이다. `libposix-kor-arm64.a`는 betriebskernWert 내부용이므로 EL0 프로그램에 링크하지 않는다. Linux 헤더나 Linux ELF와 혼합하지 않는다. 동적 verbinden, 표준 C printf, libstdc++/STL, ausnahme·RTTI는 제공하지 않으며 C++의 statischWert 생성자·lokalGültigkeitsbereich objektWert 소멸자는 지원한다. 상세 Nummer·speicherDaten 범위는 [BenutzerAufrufVorgangABI.md](BenutzerAufrufVorgangABI.md)를 참고한다.

## validieren

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`으로 새 기능을 각각 시험한다. `make test`는 기존 befehlshülle·VNC·JVM·AOT·betriebskernWert wertSchützen 시험까지 포함한다. tatsächlichDaten Platine 대신 QEMU raspi4b에서 수행한다. 결과는 [vorherigElementeintrag GUI erweiterungWert validieren protokolldateiAufzeichnung](build/verification/release.json)과 [aktuellElementeintrag Laufzeit validieren protokolldateiAufzeichnung](build/verification/native-runtime-summary.json), [여러 terminal Bildschirm](build/verification/windows/four-terminals.png), [Swing Bildschirm](build/verification/swing/native-swing.png)을 참고한다.

umsetzung 시 참고한 표준 API: [Socket](https://docs.oracle.com/javase/8/docs/api/java/net/Socket.html), [JFrame](https://docs.oracle.com/javase/8/docs/api/javax/swing/JFrame.html), [JButton](https://docs.oracle.com/javase/8/docs/api/javax/swing/JButton.html). 이 문서의 umsetzung 범위가 oberkanteWert 표준 전체를 지원한다는 뜻은 아니다.

## Deutsch 이름으로 직접 작성하는 창과 ausführungsfadenWert

`example/java/Fensterbeispiel.java`는 `AusführbarAufgabe.aufgabeAusführen`,
`AktionEmpfänger.aktionEmpfangen(AktionMitteilung)`, `schaltfläche`, `EreignisWarteschlange.späterAufrufen`, `ausführenVorgang()`을 쓴다.
eigen JVM에 이 이름들의 objektWert·methodeWert·콜백을 직접 구현했으며 영어 Swing 객체를
보관하는 래퍼가 아니다. `hintergrundarbeiter`도 eigen 스케줄러와 직접 연결된다.
세부 메서드와 기존 Deutsch API에서의 변경은 [Deutsch API Dokumentation](DeutschJava/Anleitung.md)를 본다.

Wirtssystem javac는 verteilungWert JAR를 klasseWert 경로로 사용한다.

```sh
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 ../../example/java/Fensterbeispiel.java
python3 Werkzeuge/befehlAusführen.py --desktop --network --resolution 1920x1080
```

게스트에는 빌드한 예제가 `/example/java`에 설치된다.

```text
cd /example/java
java Fensterbeispiel
```

직접 Bildschirm/ausführungsfadenWert API와 `ausführenVorgang()` 진입점은 eigen JVM 전용이다.
전체 OpenJDK·Swing 재구현이나 일반 OpenJDK에서 같은 API의 실행을 보장하지 않는다.
기존 표준 `main(String[])` 프로그램은 fortsetzenVerarbeitung 실행할 Zahl 있다.
