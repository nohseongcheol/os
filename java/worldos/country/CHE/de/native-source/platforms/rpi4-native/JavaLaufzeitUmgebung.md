# eigen ARM64 JVM 0.4와 Deutsch bibliothek

Deutsch Kommunikation·ausnahme 사용법은 [Deutsch Java API](DeutschJava/Anleitung.md), Funktion·variableWert·Datei 이름의 변경과 어원 근거는 [benennung Anleitung](benennung/Anleitung.md)를 참고한다.

JAR befehlAusführen, externWert IPv4 TCP/UDP, 별도 statischWert 부분집합 `jaot`와 게스트 C 컴파일은 [FTP·C·JAR·AOT 매뉴얼](DateiÜbertragungUndÜbersetzungsvorgang.md)에 설명한다. unterkanteWert objektWert·Thread·Swing은 JVM 경로의 기능이며 AOT unterstützungWert 범위와 같지 않다.

이 구현은 **Linux 없이 부팅한 Java AOT 커널의 EL0에서 befehlAusführen**한다. JDK/JRE의 거의 모든 기능을 제공하는 단계는 아직 아니다. HotSpot·OpenJDK klasseWert bibliothek 전체를 이식하거나 Java SE 인증/TCK를 통과한 구현도 아니다. 이번 확장은 단일 klasseWert·statischWert methodeWert 중심이던 실행기를 objektWert·bibliothek befehlAusführen 기반으로 넓힌 것이다.

## 실행과 quelltextÜbersetzen

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
# eigen betriebskernWert 안에서 quelltextBaum quelltextÜbersetzen → class befehlAusführen, Deutsch API aufrufen
python3 Werkzeuge/dateiAusführen.py Prüfungen/Java/hangulQuelltext.java

# objektWert·ausnahme 등은 Wirtssystem JDK로 Java 8 class를 만든 danachStatuswert eigen 커널에서 befehlAusführen
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java Prüfungen/Java/hangulPrüfung.java
python3 Werkzeuge/dateiAusführen.py build/my-java/hangulPrüfung.class

# 의존 class 파일은 --include로 함께 übertragungWert
javac --release 8 -encoding UTF-8 -d build/my-java Prüfungen/Java/objektePrüfung.java
python3 Werkzeuge/dateiAusführen.py build/my-java/objektePrüfung.class \
  --include build/my-java/hintergrundWert.class --include build/my-java/verzweigungWert.class \
  --include build/my-java/kannBerechnen.class

make test-jvm
```

`--include DIR`는 그 디렉터리의 class 파일을 재귀적으로 읽어 `패키지.klasseWert.class`라는 RAM Datei 이름으로 전송한다. 주 클래스도 패키지가 있다면 `--class-name 패키지.klasseWert`를 지정한다. 셸에서는 해당 이름으로 업로드하고 `java 패키지.klasseWert`로 실행한다. JVM 0.4는 Main-Class가 있는 16 KiB 이하 JAR도 `java -jar Datei.jar`로 실행한다. JAR 모드에서는 JAR 내부 클래스와 내장 Deutsch 클래스만 찾는다. verteilungWert Deutsch bibliothek JAR는 Wirtssystem javac의 classpath로 사용하며, 같은 클래스가 Benutzer JVM ELF에도 lesen 전용 자료로 포함된다. 일반 class 모드에서는 사용자가 같은 이름으로 올린 RAM class를 먼저 읽는다.

게스트 `javac`는 여전히 statischWert methodeWert, int/boolean/char/String, bedingung·wiederholungsschrittWert, Zeichenkette zusammenfügenWerte, 일부 Datei 스트림 등의 **eigen 부분집합 Übersetzer**dritterOperand. objektWert Deklarationen·상속·try/catch·Thread benutzenWert 소스를 게스트 javac가 alleErzeugenAbbild 컴파일하는 것은 아니다. oberkanteWert 기능은 `javac --release 8`로 만든 class를 eigen JVM에서 실행한다. Deutsch API 중 Ausgabe·Zeichen 스칼라 Funktion·Datei lesen/쓰기는 게스트 컴파일러에도 연결했다. 다음처럼 전체 이름으로 호출한다.

```java
public class Gruß {
    public static void main(String[] argumente) throws Exception {
        Deutsch.eigen.Ausgabe.zeileSchreiben("안녕하세요😀");
        Deutsch.eigen.Ausgabe.nummerSchreiben(Deutsch.eigen.Zeichen.kodePunktAnzahl("HangulText😀"));
        Deutsch.eigen.Datei.schreiben("Gruß.txt", "HangulText Datei😀");
        Deutsch.eigen.Ausgabe.zeileSchreiben(Deutsch.eigen.Datei.lesen("Gruß.txt"));
    }
}
```

## eigen JVM에서 구현한 beschneiden

| gebietWert | 제공 beschneiden |
|---|---|
| klasseWert | class 버전 45…52, 여러 klasseWert 로딩, 인스턴스/statischWert feldWert, 생성자, 상속, 가상 aufrufen, 인터페이스 aufrufen, statischWert initialisieren |
| Wert·befehl | 32비트 int 계열, boolean/byte/char/short, verweis, 1차원 datenfeldWert, verzweigung·switch·wide, instanceof/checkcast, category-1 operandStapel befehl |
| ausnahme | 지원하는 표준 ausnahme generieren·throw·catch·finally, methodeWert 경계를 넘는 vorwärtsWert, getMessage; unterkanteWert grenzwertWert verweis |
| speicherDaten | 비이동 mark/sweep GC, 빈 gebietWert 병합, operandStapel·statischWert feldWert·컬렉션·ausführungsfadenWert·모니터·Zeichenkette 상수의 verweis wertBeibehalten |
| Zeichenkette | UTF-16, length/charAt/equals/isEmpty/substring/concat/hashCode/toString, String.valueOf(int), StringBuilder의 standardwertWert generieren·append(int/boolean/char/String)·toString |
| Zahl | Integer.parseInt/valueOf/intValue/toString, 작은 Integer 캐시, Math.abs/min/max(int) |
| 표준 Ausgabe | System.out/err, PrintStream.print/println의 int/boolean/char/String 및 빈 println |
| datenfeldWert | int/byte/boolean/char/short/verweis datenfeldWert, Länge·beschneiden Prüfpunkte, verweis datenfeldWert elementeintragElement typWert Prüfpunkte, System.arraycopy의 überlappungen/beschneiden/elementeintragElement typWert Prüfpunkte |
| Datei | FileInputStream(String), FileOutputStream(String[,boolean]); read()/read(byte[][,offset,len]), write(int)/write(byte[][,offset,len]), close, Ausgabe flush. EOF는 -1 |
| 컬렉션 | ArrayList/List: add(E), get, set, remove(int), size, isEmpty, clear. HashMap/Map: put/get/remove/containsKey/size/isEmpty/clear |
| ausführungsfadenWert | Thread(), Thread(Runnable), Thread 상속, start/join/isAlive/currentThread/yield; synchronized methodeWert·블록의 재진입·경합·ausnahme 시 speichergerätFreigeben |
| UDP | DatagramSocket의 standardwertWert/hardwarePort 생성자, send/receive/close/getLocalPort/setSoTimeout; DatagramPacket의 byte[]/Länge generieren 및 adresse·hardwarePort Kopfdateien generieren, getData/getLength/getAddress/getPort/setLength |
| adresse | InetAddress.getByName은 localhost/zifferWert IPv4 (DNS istNichtUnterstützt), getLoopbackAddress/getHostAddress |
| Zeichnung | Deutsch Bildschirm API가 EL0 SVC를 통해 프레임버퍼에 사각형을 Zeichnung; beschneiden Prüfpunkte |

컬렉션은 지정한 메서드만 제공하며 iterator/stream/ausrichtenWert·Benutzer definitionWert equals/hashCode 콜백은 없다. 사전의 열쇠는 String/Integer/null 사용을 시험했다. UTF-16 kodeWert 단위와 Unicode kodeWert 포인트 수는 구분한다. HangulText Eingabewert Zusammenstellung·wertNormalisieren·아랍어 조판·GUI 다국어 글꼴은 이 Zeichenkette 지원과 별개다.

예외는 Throwable/Exception/RuntimeException, ArithmeticException, NullPointerException, IndexOutOfBoundsException/ArrayIndexOutOfBoundsException/StringIndexOutOfBoundsException, IllegalArgumentException/NumberFormatException/IllegalThreadStateException, IOException/FileNotFoundException, IllegalStateException, ClassCastException, NegativeArraySizeException, ArrayStoreException, UnknownHostException, SocketTimeoutException의 제한된 generieren·kategorieWert·처리를 제공한다. Benutzer definitionWert Throwable 상속, stack trace/cause/suppressed ausnahme, try-with-resources의 addSuppressed, 완전한 initialisieren fehler 포장은 아직 없다. 잡히지 않은 예외는 aktuellElementeintrag 전체 Java 실행을 실패로 끝낸다.

## Deutsch API

독립 패키지 **`Deutsch.eigen`**를 사용한다. Linux판 `Deutsch.Java`ersterOperand 요구하는 NIO/Swing/HTTP API를 eigen 커널에서 실행할 Zahl 있다고 혼동하지 않도록 패키지를 나눴다. 이 라이브러리는 klasseWert Name·methodeWert·argumente·feldWert·Datei 이름에 한국어를 사용한다. 표준 Java klasseWert 이름은 호환성을 위해 보존한다.

| klasseWert | 공개 기능 | 이름의 의미 |
|---|---|---|
| Ausgabe | schreiben, zeileSchreiben, nummerSchreiben | Ausgabe(出力): 내용을 바깥으로 exportiertWert |
| Zeichen | Länge, gleichText, einsetzenText, schneidenWert, ganzzahlAnalysieren/ganzzahlWertSchreiben, kodePunktAnzahl, kodieren/datenEntschlüsseln | Zeichen(文字), kodierungWert(符號): 글의 단위와 그 값을 바이트로 나타내는 regelWert |
| Datei | lesen/schreiben(String Name), byteWertLesen/byteWertSchreiben | 널리 쓰는 Benutzer 용어를 보존; RAM 자료의 Name |
| eintragListe | werteHinzufügen, lesen, wertErsetzen, eintragTilgen, größe, istLeerwertWert, inhaltLöschenInhalt | eintragListe(目錄): 순서가 있는 eintragWert 모음 |
| Wörterbuch | wertAblegen, eintragFinden, führtAusVorhanden, eintragTilgen, größe, inhaltLöschenInhalt | Wörterbuch(辭典): 찾는 말인 열쇠에 값을 zuordnungWert |
| Aufgabe | ausführenVorgang(AusführbarAufgabe), abwarten(hintergrundarbeiter), aufgabeAbgeben, istLebendig | Aufgabe ausführungsfadenWert: 한 Programm 안의 befehlAusführen datenstromWert |
| Kommunikation | öffnen, senden, empfangen, zeitüberschreitung, schließen | Kommunikation(通信), datagramm(電文), portWert: Daten 교환·메시지·포트의 역할 |
| Bildschirm | rechteck, eintragTilgen | Bildschirm(畫面): tatsächlichDaten 그림을 표시하는 면 |
| betriebskernWert | millisekunden, rechteck | eigen JVM의 고정 native verbinden; 일반 JNI는 아님 |

이 명명은 aktuellElementeintrag 기능을 설명하는 용어 선택이다. 기존 한국어에 없던 역사적 어원을 만들어 주장하지 않는다. dateiNameText·식별자는 UTF-8 소스로 보관한다. `Zeichen.datenEntschlüsseln`는 잘못된 UTF-8에 IllegalArgumentException을 던지며, `kodieren`는 짝이 없는 서로게이트를 `?`로 바꾼다. `Datei.lesen`는 엄격한 UTF-8 복호화를 적용한다. Bildschirm 색은 `빨강 | (초록 << 8) | (파랑 << 16)` 형식이다.

## befehlAusführen 제한과 남은 Aufgabe

- 동시에 적재하는 class höchstwertWert 16개(Deutsch klasseWert Kopfdateien), class당 16 KiB·konstanteWert 풀 511항목, 전체 methodeWert/feldWert 각각 512개. methodeWert kodeWert 8 KiB, lokalGültigkeitsbereich variableWert·피연산자 operandStapel 각각 128슬롯, argumente höchstwertWert 16개(this Kopfdateien).
- VM 가닥은 main Kopfdateien **실행당 höchstwertWert 4개**, 가닥당 aufrufen tiefeWert 32. 100개 명령마다 befehlAusführen 대상을 바꾼다. 네이티브 aufrufen 도중에는 전환하지 않는다. pthread/SMP/OS 스레드가 아니며 Thread.sleep/interrupt/daemon/우선순위, Object.wait/notify, java.util.concurrent는 없다.
- objektWert 힙은 32768개의 32비트 슬롯이다. 런타임의 AOT 배열은 tatsächlichDaten 메모리에서 64비트 슬롯을 사용한다. GC가 있어도 대형 Datei·대형 Zeichenkette·객체가 이 제한을 넘을 Zahl 있다.
- 실행은 50만 bytecode befehl 및 커널의 약 2초 EL0 기한으로 제한된다. Swing의 Eingabewert 대기는 기한을 갱신하고 fenster umschaltenBetriebsart 시 중단·재개한다. 일반 dienstanbieterWert·계산의 무제한 실행은 아직 없다. istNichtUnterstützt befehl·betriebsmittelEintragWert 부족은 명시적인 오류로 종료한다.
- RAM Datei höchstwertWert 64개, 파일당 16384바이트, pfad UTF-8 63바이트. RAM 디렉터리와 gegenstelleWert/절대 경로를 제공하며 영속 저장은 아직 없다. 내장 Deutsch class는 RAM Datei 슬롯을 소비하지 않는다. 셸의 `cd`로 정한 aktuellElementeintrag 경로에서 quelltextBaum·klasseWert·Daten 파일을 읽는다.
- UDP는 Java 루프백 및 lwIP/SLIP를 통한 externWert IPv4를 제공한다. tatsächlichDaten GENET/Wi-Fi/DNS/TLS/HTTP 전체는 없다. datagramm 512바이트, netzbuchseWert 8개, 소켓당 큐 4개. receive는 VM 가닥을 양보하며 대기하고 setSoTimeout을 적용하지만 전체 befehlAusführen 기한은 여전히 적용된다.
- long/float/double, invokedynamic/람다, enum/annotation, 다차원 datenfeldWert, 완전한 datenfeldWert 공변성·인터페이스 schichtWert Prüfpunkte, Reflection/JNI/JIT, NIO/ZIP API/Charset 전체, 보안/datenVerschlüsseln/국제화 전체, 전체 AWT/Swing/JavaFX는 미지원이다. Swing의 별도 unterstützungWert 부분집합은 unterkanteWert 및 entwicklung 매뉴얼을 참고한다. klasseWert Datei 전체 검증기·zugriffEintrag erlaubnisWert/보호된 멤버 검사는 아직 완전하지 않다. 손상된 입력은 EL0 wertSchützen grenzstelleWert 내에서 종료되도록 한다.

전체 OpenJDK를 목표로 하려면 다음은 별도의 주요 umsetzung 단계다: 완전한 JVM Wert/validieren/klasseWert 로더와 ausnahme 모델 → 영속 VFS·mmap·Uhr·원자 vorgangWert·tatsächlichDaten 스레드/synchronisieren ABI → OpenJDK java.base 및 native bibliothek Portierung → Gerät 네트워크·TCP/IP → fenster 시스템/schriftartWert/입력기·java.desktop → Java SE 호환성 Prüfungen. aktuellElementeintrag eigen JVM의 일부 메서드를 더하는 것으로 이 작업이 완료되지는 않는다.

## validieren

`Werkzeuge/jVMPrüfung.py`는 같은 Java 8 class 파일의 출력을 Wirtssystem OpenJDK `-Xverify:all`과 QEMU raspi4b eigen 커널에서 비교한다. objektWert/상속/인터페이스·switch·datenfeldWert, ausnahme/finally, 컬렉션/GC, Thread/sperreWert, Deutsch UTF-8/Datei/컬렉션, tatsächlichDaten UDP 루프백/zeitWert 초과, 게스트 HangulText quelltextBaum quelltextÜbersetzen, datenfeldWert typWert/wertKopieren/Datei grenzstelleWert·HangulText 패키지의 9개 비교 시험과 잘못된 class 버전/beschnittenWert Datei wertZurückweisen 시험을 실행한다. UDP projektWurzel 실행에는 Wirtssystem 루프백 netzbuchseWert 권한이 필요하다.

`Werkzeuge/Startprüfung.py`는 betriebskernWert wertSchützen/회귀 시험과 별도로 Deutsch Java Bildschirm API가 tatsächlichDaten 픽셀을 그렸는지도 QMP Bildschirm 캡처로 검사한다. 보고서는 `build/verification/jvm/report.json`, `build/verification/report.json`이며 시험한 kernel8.img의 SHA-256을 기록한다. tatsächlichDaten Pi4 hardwareWert Startvorgang 시험과 전체 JDK 호환성 Prüfungen 결과는 아니다.


## JVM 0.3: 네트워크와 GUI erweiterungWert

`Socket`/`ServerSocket` generieren·verbinden·accept·양방향 InputStream/OutputStream·close·EOF·zeitWert 제한과 UTF-8 `String.getBytes`를 추가했다. JVM 0.4에서는 externWert zifferWert IPv4 TCP도 lwIP/SLIP에 연결했다. 연결형 endePunkt 16개, Java 루프백 버퍼 1024바이트, externWert TCP 버퍼 4096바이트다. DNS·TLS는 없다.

`JFrame`, `JPanel`, `JLabel`, `JButton`, `JTextField`, `ActionListener`, `ActionEvent`, `SwingUtilities.invokeLater`의 문서화한 부분집합을 네이티브 GUI에 연결했다. `setLayout(null)`과 명시적 좌표를 사용한다. 전체 OpenJDK Swing 또는 Java SE 호환 구현은 아니다. interaktiv 이벤트 대기는 befehlAusführen 기한을 갱신하고 terminal umschaltenBetriebsart 시 프로세스 상태를 ablegenDatenWert·복원한다. 이벤트 콜백 자체는 기존 bytecode/CPU 기한을 따른다.

Deutsch `fenster`, `Bedienelement`, `verbindungBeförderung` 클래스를 verteilungWert JAR와 eigen JVM 내장 자원에 추가했다. 상세 methodeWert·grenzwertWert·quelltextBaum·업로드 방법: [HangulText entwicklung 매뉴얼](EntwicklungLeitfaden.md).

## Deutsch 객체의 직접 befehlAusführen

`fenster`, `beschriftung`, `TextFeld`, `schaltfläche`, `EreignisWarteschlange`, `AktionMitteilung`, `hintergrundarbeiter`은
표준 GUI/Thread 객체를 보관하는 래퍼가 아니다. eigen JVM의 objektWert generieren,
formatWert Prüfpunkte, Bildschirm aufrufen, ereignis 큐, ausführungsfadenWert 스케줄러에 Deutsch 계약을 직접 구현했다.
표준 `javax.swing`·`Thread` 코드의 befehlAusführen 경로도 유지한다.
Deutsch 단추와 표준 JButton은 서로 다른 형식이며, 해당 instanceof 검사도 검증한다.

eigen 실행기의 Deutsch 진입점은 `public static void ausführenVorgang()`이다.
표준 `main(String[])`도 지원하며 zweiWert dritterOperand 있으면 Deutsch 진입점을 우선한다.
명령행 인수는 `Argumente.elementeintragAnzahl()`와 `Argumente.Text(ordnungszahlIndex)`으로 읽는다.
`example/java`의 다섯 예제는 이 규약을 사용한다. statischWert Datei 예제는 게스트
javac로도 컴파일하며, GUI/ausführungsfadenWert 소스는 Wirtssystem `javac --release 8`을 사용한다.
직접 GUI/ausführungsfadenWert API는 eigen JVM 전용이다. 기존 OpenJDK 비교 시험과 별도로
Deutsch 가닥의 befehlAusführen·wertWarten·중복 ausführenVorgang wertZurückweisen, GUI ereignis ursprungWert·Nummer·콜백을 검사한다.
전체 JDK 번역이나 모든 API의 jaot 지원을 뜻하지 않는다.

methodeWert 이름은 바이트코드에서도 유지된다. 이름과 참조를 같이 수정하면
Deutsch 클래스도 실행되지만, Zeichenkette 리터럴·표준 bibliothek 재정의·native
verbinden·진입점은 각각 컴파일러와 실행기의 계약을 맞춰야 한다.
[상세 계약과 Beispiele](DeutschJava/Anleitung.md)를 참고한다.

## terminal unterteilWert auffrischen

bewegenWert·größe 변경은 새 fenster 영역과 vorherigElementeintrag 자리에서 드러난 띠만 합성한다.
1920×32 bildpunkt(240 KiB)의 vorläufigWert 그림에서 배경·겹친 fenster·zeichenWert·GUI를 먼저
완성하고, aktuellElementeintrag wertAnzeigen 메모리와 비교하여 달라진 화소만 기록한다.
32줄보다 큰 영역은 여러 띠로 처리하므로 전체 프레임을 원자적으로
교체하거나 수직 동기에 맞추는 방식은 아니다. 전체 배경을 먼저 지우는
중간 화면은 표시하지 않는다. 좌표가 같으면 erneutVersuchenWert 그리지 않는다.

`make test-redraw`는 tatsächlichDaten C malenBildschirm 코드를 호스트의 speicherDaten 화면에 연결해
bewegenWert 80회·größe wertÄndern 40회·겹친 fenster 4개를 전체 합성 결과와 bildpunkt 단위로 대조한다.
gebietWert 밖 Benutzer Zeichnung, 동일 bildpunkt 무기록, zeiger 밑그림, tatsächlichDaten Bildschirm zeile 간격을
검사한다. 이 시험의 시간은 Wirtssystem CPU 측정이며 Pi 4/QEMU 속도로 해석하지 않는다.
`make test-resize`는 QEMU/VNC의 640×480 및 1920×1080에서 linksSeiteRand eckeWert ziehenWert,
HangulText Eingabewert·vi 미저장 inhaltswertWert·독립 fenster 크기를 검사한다.
