# eigen ARM64 betriebskernWert: FTP, C, JAR와 AOT befehlAusführen

대상은 **Linux를 적재하지 않는 Raspberry Pi 4용 Java AOT betriebskernWert**이다. CPU·Gerät 경계는 C/어셈블리, Datei 체계와 셸은 Java이며, 이번 TCP/IP 스택은 C로 작성된 lwIP 2.2.0을 이식했다. 게스트 TinyCC와 `jaot`도 EL0에서 실행한다. 호스트에 컴파일을 요청하거나 Wirtssystem JVM으로 대신 실행하지 않는다.

## 먼저 알아둘 unterstützungWert grenzstelleWert

| anfrage | 이번 umsetzung | 남은 beschneiden |
|---|---|---|
| JAR를 befehlAusführen 파일처럼 befehlAusführen | `java -jar Datei.jar`, `./Datei.jar argumente`; Main-Class와 ablegenDatenWert/DEFLATE ZIP, CRC Prüfpunkte | 전체 Java SE, 임의의 모든 JAR 호환성 |
| 게스트 AOT | `jaot Datei.class -o Datei.elf`, `jaot Datei.jar -o Datei.elf`; tatsächlichDaten ARM64 기계어 generieren | objektWert·ausnahme·Thread·Swing·Socket의 AOT wertUmwandeln, 여러 애플리케이션 klasseWert verbinden |
| C quelltextÜbersetzen | 게스트 `cc`/`tcc`, TinyCC C 전처리기·ARM64 생성기·링커; Deutsch 식별자와 posix-kor | 전체 libc, 일반 Linux befehlAusführen Datei, 게스트 C++ Übersetzer |
| 업로드한 ELF befehlAusführen | ELF64/AArch64 헤더 Prüfpunkte, 확장자 없는 `./Datei`; eigen ABI 및 명시적인 제한형 Linux ABI | 일반 Linux 바이너리 호환, 동적 링커, 공유 bibliothek |
| externWert TCP/UDP | 게스트 lwIP IPv4 operandStapel, POSIX 소켓과 JVM의 zifferWert IPv4 adresse | GENET/Wi-Fi 드라이버, DHCP·DNS·TLS, physischHardware Platine 네트워크 Prüfungen |
| FTP | 게스트 서비스, 패시브 übertragungWert, UTF-8 Name, STOR/RETR/SIZE/LIST/NLST/MLSD/DELE | TLS·사용자별 erlaubnisWert·하위 디렉터리·영속 ablegenDatenWert |
| HangulText Java | 기존 `Deutsch.eigen` 클래스와 externWert adresse UDP 오버로드 | 전체 JDK의 일대일 Deutsch zuordnungWert API |

JVM은 klasseWert 버전 45…52의 문서화한 부분집합이다. `java`는 bytecode 실행기이고, `jaot`ersterOperand 별도의 네이티브 befehlAusführen 파일을 만든다. **JAR archivWert 해제나 JVM을 함께 묶는 것을 AOT라고 표시하지 않는다.** 지원하지 않는 bytecode/API는 `jaot`ersterOperand 진단하고 출력을 만들지 않는다. 기존 Ausgabe ELF도 quelltextÜbersetzen fehlschlagWert 때 보존한다.

Android의 Dalvik/ART는 일반 JVM klasseWert/JAR가 아닌 **DEX**를 실행한다. ART의 AOT에는 GC, klasseWert 로딩, JNI 등 befehlAusführen 기반도 필요하다. 따라서 ART처럼 기계어로 바꾸는 기능만으로 임의의 OpenJDK JAR 및 Swing이 자동 호환되지는 않는다. [Android 공식 런타임 beschreibung](https://source.android.com/docs/core/runtime)

## aktuellElementeintrag 컴퓨터에서 FTP verbindung

Wirtssystem terminal 1:

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
python3 Werkzeuge/befehlAusführen.py --network
```

Remmina GUI에서도 같은 네트워크를 사용하려면 befehlAusführen 명령을
`python3 Werkzeuge/befehlAusführen.py --desktop --network`로 바꾸고 VNC `127.0.0.1:5902`에
접속한다. FTP와 네트워크는 같은 게스트 안에서 동작한다.

부팅한 **jkoros befehlshülle**:

```text
ftpd start
```

Wirtssystem terminal 2:

제공한 예제로 작은 befehlAusführen JAR를 먼저 만든다. Deutsch 라이브러리는 게스트에 내장되어 있어 이 Beispiele JAR에 중복해서 넣지 않는다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
mkdir -p build/upload
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/upload Beispiele/verteilungWert/Farbe.java
jar cfe build/upload/Gruß.jar Farbe -C build/upload Farbe.class
```

```sh
python3 - <<'PY'
from ftplib import FTP
ftp = FTP()
ftp.encoding = 'utf-8'
ftp.connect('127.0.0.1', 2121)
ftp.login()                         # anonymous; jkoros도 같은 Aufgabe adresseGebiet
with open('build/upload/Gruß.jar', 'rb') as f:
    ftp.storbinary('STOR Gruß.jar', f)
print(ftp.nlst())
ftp.quit()
PY
```

erneutVersuchenWert **jkoros befehlshülle**:

```text
java -jar /Gruß.jar
/Gruß.jar
ftpd status
ftpd stop
```

FTP는 루트 RAM 파일만 공개한다. 익명 로그인이며 비밀번호로 권한을 구분하지 않는다. standardwertWert Wirtssystem 바인딩은 `127.0.0.1`이고, steuerungWert 포트는 2121, 데이터 포트는 50000…50007이다. `--ftp-port 2122`로 steuerungWert 포트를 바꿀 Zahl 있다. 동시에 한 FTP 세션을 제공하며 명령이 없는 세션은 60초 danachStatuswert 닫는다. TYPE A도 바이트를 변경하지 않으므로 프로그램은 바이너리 전송한다.

파일은 **64개, 각각 16 KiB**, 경로는 UTF-8 63바이트이다. Startvorgang 시 준비되는 `/example`도 이 한도를 공유한다. 초과/끊어진 STOR는 기존 파일에 반영하지 않는다. FTP 업로드는 RAM에만 저장되며 재부팅하면 사라진다. 이 grenzwertWert 때문에 일반적인 대형 JAR 배포판을 그대로 올릴 Zahl 없다.

QEMU의 raspi4b에는 GENET Ethernet 장치가 없다. 따라서 `network_bridge.py`ersterOperand QEMU NAT의 Ethernet과 hilfsWert UART의 SLIP를 변환한다. **TCP verbinden prozessWertEintrag·체크섬·재전송·FTP 명령과 Datei 저장은 게스트 안에서 수행한다.** Wirtssystem 브리지는 FTP 서버가 아니다. [QEMU 공식 Gerät unterstützungWert eintragListe](https://www.qemu.org/docs/master/system/arm/raspi.html)

이 경로는 QEMU에서 검증했다. hilfsWert UART의 tatsächlichDaten Pi 4 핀/클럭 설정과 내장 RJ45 GENET 드라이버는 umsetzung·검증하지 않았으므로, SD 이미지에 커널이 포함되어 있다는 사실을 tatsächlichDaten 보드의 LAN/FTP aktion 보장으로 해석하면 안 된다.

## Deutsch Java를 게스트에서 컴파일하고 AOT befehlAusführen

게스트 `vi Farbe.java`로 nächsterElementeintrag 소스를 작성한다.

```java
public class Farbe {
    public static void main(String[] argumente) throws Exception {
        int summeWert = 0;
        int Zahl = 1;
        while (Zahl <= 10) {
            summeWert = summeWert + Zahl;
            Zahl = Zahl + 1;
        }
        Deutsch.eigen.Ausgabe.nummerSchreiben(summeWert);
        Deutsch.eigen.Datei.schreiben("aot.txt", "HangulText AOT Datei 😀");
        Deutsch.eigen.Ausgabe.zeileSchreiben(Deutsch.eigen.Datei.lesen("aot.txt"));
    }
}
```

```text
javac Farbe.java
java Farbe
jaot Farbe.class -o Farbe.elf
run Farbe.elf
```

`jaot`은 클래스의 바이트코드를 C로 변환하고, **게스트 TinyCC**ersterOperand ARM64 명령어를 generieren·연결한다. befehlAusführen 때 JVM 인터프리터를 호출하지 않는다. JAR의 Main-Class가 같은 unterstützungWert 범위이면 다음도 가능하다.

```text
jaot Farbe.jar -o Farbe.elf
run Farbe.elf
```

AOT 지원은 한 애플리케이션 클래스의 statischWert methodeWert/feldWert, int 계열, Ganzzahl 배열과 verweis, argumente datenfeldWert, bedingung·verzweigung·wiederholungsschrittWert, Zeichenkette 리터럴, `System.out.print/println`의 int/String, Deutsch Ausgabe·Datei lesen/쓰기로 제한된다. klasseWert/methodeWert 수와 operandStapel 등에도 고정 상한이 있다. Java ausnahme prozessWertEintrag, objektWert generieren, 가상 methodeWert 일반, switch/wide, long/float/double, invokedynamic, Zeichenkette 결합용 StringBuilder, 일반 JDK·Socket·Thread·Swing은 이 AOT 백엔드에서 미지원이다. 내장 NUL/고립된 서로게이트 문자열도 거부한다. 잘못된 datenfeldWert zugriffEintrag/0으로 teilenWerte 등은 네이티브 런타임 오류로 종료하며 Java ausnahme 객체로 전달하지 않는다.

Eingabewert 클래스뿐 아니라 **생성된 ELF도 16 KiB 이하**여야 한다. 기계어 확장과 ELF 페이지 ausrichtenWert 때문에 짧은 클래스도 이 한도를 넘을 Zahl 있으며, 이 경우 오류를 내고 기존 출력을 보존한다.

게스트 `javac`도 부분집합이다. 일반적인 objektWert·Thread·Swing 소스는 호스트에서 `javac --release 8`로 컴파일하고, **기존 JVM의 unterstützungWert beschneiden 안에서** `java`/`java -jar`로 실행한다. 정확한 API는 [JVM 매뉴얼](JavaLaufzeitUmgebung.md)과 [HangulText entwicklung 매뉴얼](EntwicklungLeitfaden.md)을 참고한다.

JAR는 하나의 애플리케이션 klasseWert 경로다. 내부 Name `Paket/Programm.class`와 점으로 구분한 Main-Class를 지원한다. 내부 클래스는 파일로 풀어 VFS 슬롯을 소비하지 않는다. 내장 Deutsch 클래스를 추가로 찾지만 aktuellElementeintrag Aufgabe 폴더의 다른 클래스는 자동 혼합하지 않는다. ZIP64·datenVerschlüsseln ZIP·manifest Class-Path·서명 검증은 지원하지 않는다. JAR 하나가 16 KiB 이하이어도 클래스당/적재 Zahl/VM speicherhaldeWert 제한은 그대로 적용된다.

## C에서 Deutsch POSIX aufrufen

게스트에서 `vi Gruß.c`로 작성하거나 FTP로 소스를 업로드한다.

```c
#include <DateiABI.h>

int main(void) {
    const char gruß[] = "eigen ARM64 C에서 HangulText POSIX aufrufen\n";
    int Dokumentation = dateiÖffnen("Gruß.txt", LesenSchreiben | ErstellenFallsFehlend | KürzenInhalt, 0600);
    if (Dokumentation < 0) return 1;
    einAusgabeErgebnisTyp aufgezeichnetAnzahl = dateiDatenSchreiben(Dokumentation, gruß, sizeof(gruß) - 1);
    dateiSchließen(Dokumentation);
    dateiDatenSchreiben(1, gruß, sizeof(gruß) - 1);
    return aufgezeichnetAnzahl == sizeof(gruß) - 1 ? 0 : 2;
}
```

```text
cc Gruß.c -o Gruß.elf
run Gruß.elf
cat Gruß.txt
```

TinyCC의 표준 C eintragPunkt `main`을 사용한다. 기존 Wirtssystem C/C++ SDK의 `benutzerProgrammStarten(int)` 진입점과 구분한다. Kopfdateien Datei·ausführenVorgang objektWert·`libposix-kor-user.a`는 Übersetzer 내부의 lesen 전용 SDK에 들어 있다. C 전처리기/구조체/Funktion/재귀/zeiger/부동소수점 generieren 등을 사용하되 **일반 libc/libstdc++를 제공한다는 뜻은 아니다**. 제공하지 않는 함수는 verbinden 오류가 난다. Übersetzer 자체의 Zeichen/zifferWert wertUmwandeln 지원도 완전한 libc 대체품이 아니다.

`dateiÖffnen` 등은 별도의 모의 호출이 아닌 기존 `pk_open` 등의 Deutsch 매크로이며, ELF의 SVC를 통해 tatsächlichDaten Java Datei 체계에 도달한다. Datei/netzbuchseWert aufrufen 목록은 [Benutzer ABI](BenutzerAufrufVorgangABI.md)에 있다. C/C++ Wirtssystem SDK befehlAusführen 파일도 FTP로 업로드 danachStatuswert `run` 또는 `./Datei`로 실행하며 확장자는 benötigtWert 없다. Linux ARM64 statischWert ELF에는 별도의 제한된 호환 pfad `run --linux Datei`을 추가했다. [ELF·Linux ABI 매뉴얼](ausführdateiABI.md)에 정확한 formatWert·시스템 aufrufen·adresse 제한을 정리했다.

## Deutsch 네트워크·Aufgabe·Bildschirm API

| klasseWert | aufrufen 예 | befehlAusführen pfad |
|---|---|---|
| `Ausgabe` | `zeileSchreiben("안녕")`, `nummerSchreiben(42)` | JVM 및 제한형 AOT |
| `Datei` | `schreiben("Dokumentation.txt", "inhaltswertWert")`, `lesen("Dokumentation.txt")` | JVM 및 제한형 AOT |
| `Kommunikation` | `öffnen(0)`, `senden(endpunkt, "10.0.2.2", 9000, "HangulText")`, `empfangen(endpunkt)` | JVM의 UDP |
| `verbindungBeförderung` | `verbinden("10.0.2.2", 9000)`, `endpunktLauschen(9000)`, `empfangen(dienstanbieterWert)` | JVM의 Socket/ServerSocket |
| `Aufgabe` | `ausführenVorgang(Runnable)`, `abwarten(Thread)`, `aufgabeAbgeben()` | JVM의 협력식 ausführungsfadenWert |
| `fenster`, `Bedienelement` | fenster·버튼·zeichenWert·TextFeld·ereignis verbinden | JVM의 Swing 부분집합 |

명명에서는 표준 영어 API를 보존하고 Deutsch aufrufen 계층을 추가한다. `Kommunikation(通信)`, `verbinden(連結)`, `Ausgabe(出力)`은 기존 단어의 뜻을 사용한다. `Aufgabe ausführungsfadenWert`은 한 befehlAusführen 흐름을 가닥에 빗댄 deskriptorWert 표현, `portWert`는 포트의 접점을 설명하는 표현이다. 새 deskriptorWert 결합어를 고대에 이미 존재한 용어처럼 설명하지 않는다. 전체 JDK의 번역을 완료했다고 표시하지 않는다.

externWert 주소는 zifferWert IPv4이며 QEMU 호스트는 `10.0.2.2`, 게스트는 `10.0.2.15`dritterOperand. UDP 전문은 512바이트까지다. 소켓은 비차단 eigen ABI이며 JVM이 제한된 wertWarten/재시도를 제공한다. TCP connect 대기는 höchstwertWert 1초, Benutzer Programm 전체에는 기존 약 2초 CPU 기한이 적용된다. 일반적인 장기 befehlAusführen Benutzer 서버와 pthread는 아직 없다. FTP는 Benutzer Programm 기한과 별개인 betriebskernWert 서비스다.

게스트의 Benutzer TCP/UDP 서버로 들어오는 연결은 NAT 포트를 추가한다. 예를 들어 `python3 Werkzeuge/befehlAusführen.py --network --forward tcp:9300:9300 --forward udp:9301:9301`로 실행하면 호스트의 localhost 9300/TCP·9301/UDP를 게스트의 같은 포트로 전달한다. FTP의 standardwertWert steuerungWert/데이터 포트와 겹치면 befehlAusführen 전에 거부한다.

## 시험과 systemErzeugenAbbild 재현

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test-ftp
make test
make image
```

`build/verification/ftp/report.json`은 tatsächlichDaten FTP übertragungWert, HangulText Datei, größe 초과 보존, archivWert JAR befehlAusführen, 게스트 C quelltextÜbersetzen/ELF 재업로드, externWert Java TCP/UDP, 게스트 javac/AOT 실행을 기록한다. `serial.log`에서 게스트 명령과 결과를 확인할 Zahl 있다. 보고서의 betriebskernWert SHA-256과 verteilungWert 이미지의 커널을 비교한다.

빌드는 기존 JDK/Clang/AArch64 binutils와 함께 `../rpi4/build/rootfs`의 ARM64 SDK Deklarationen 헤더와 libgcc arithmetikWert hilfsWert 함수를 사용한다(`make rpi-prepare`). **musl libc, Linux betriebskernWert, 동적 로더를 게스트에 링크하지 않는다.** TinyCC/lwIP/uzlib 원본과 라이선스·버전 정보는 `vendor/`, Portierung 코드는 `ccompiler/`, `network/`, `Benutzer/Paket.c`에 있다.

전체 JDK/AOT JVM으로 확장하려면 타입 validieren·objektWert/ausnahme/GC·동적 로딩·JNI, 영속 Datei betriebSystemWert·mmap/TLS/시그널·스레드 ABI, OpenJDK native bibliothek, GUI peer/폰트/입력기, GENET 및 physischHardware Gerät 검증이 더 필요하다. 이 문서의 befehlAusführen 시험은 그 전체 이식을 대신하지 않는다.
