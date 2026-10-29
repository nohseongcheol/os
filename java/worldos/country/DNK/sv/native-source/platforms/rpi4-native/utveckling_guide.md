# eget 커널에서 vi·여러 kommandotolk·한글 프로그래밍 사용하기

Svenska kommunikation·fel_31f743d2 사용법은 [Svenska Java API](한국어자바/VIKTIGT_eb81d7d9.md), FUNKTION_värde·variabel_värde·filnamn 이름의 변경과 어원 근거는 [명명 VIKTIGT_eb81d7d9](명명/VIKTIGT_eb81d7d9.md)를 참고한다.

대상은 `platforms/rpi4-native`의 eget AArch64 Java 커널이다. vi와 Java/Python/C/C++ 프로그램은 EL0에서 실행한다. Linux 실행판과 별도이며 아래 stöd_värde 목록은 전체 OpenJDK·Vim·POSIX 구현을 뜻하지 않는다.

게스트 `cc`/`jaot`, JAR 직접 köra_kommando, extern_värde TCP/UDP와 FTP는 [새 köra_kommando 매뉴얼](파일전송과번역.md)을 참고한다.

## GUI와 여러 kommandotolk

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, Adress **127.0.0.1:5902**로 연결한다. skärmbild 위 **+ New terminal**, **Ctrl+Shift+T**로 터미널을 추가한다. 최대 네 개다. 위쪽 kommandotolk 버튼 또는 창을 클릭해 선택하고 **F6**으로 순환한다. 제목줄을 끌어서 옮기고 **HÖGER 위 X**를 클릭하면 닫힌다. 마지막 창을 닫아도 위쪽 köra_kommando 버튼으로 försöka_igen_värde spalt_värde nummer 있다. 기존 `terminal`, `exit`, F12도 사용할 nummer 있다.

창마다 aktuellt_objekt 디렉터리, Shell variabel_värde, kommando LOG_POST, indata_värde 중인 명령과 app_f5044b9b köra_kommando 상태를 보관한다. filnamn 저장소는 공유한다. vi와 Swing의 이벤트 vänta_värde 중에 다른 터미널로 전환하면 användarutrymme Minne_data·레지스터·filnamn/socket_värde 연결을 보존했다가 돌아올 때 재개한다. **aktuellt_objekt 네 프로그램이 동시에 CPU에서 실행되는 선점형 스케줄러는 아니다.** 계산 중인 프로그램은 Nästa_objekt indata_värde vänta_värde 또는 기존 köra_kommando 기한까지 전환이 지연될 nummer 있다.

X로 터미널을 닫으면 그 터미널의 köra_kommando 중인 프로그램도 종료하며 서술자·소켓을 회수한다. 저장하지 않은 ändring_värde 내용은 사라진다. 종료한 슬롯은 새 창에서 재사용한다. aktuellt_objekt 모든 파일은 RAM에 있으며 VM 재시작 후에는 남지 않는다.

화면과 Fönster 판단은 게스트 커널이 처리한다. QEMU köra_kommando 도구는 VNC 키와 마우스 좌표를 UART 패킷으로 전달한다. verklig_data Pi4 USB 입력기와 실물 부팅은 아직 검증하지 않았다. 일반 UART 셸은 `make run`, GUI verktyg 종료는 värd 터미널의 Ctrl+C다.

## vi använda_värde

```text
mkdir 작업
cd 작업
vi 인사.py
```

`vi`는 새로 구현한 **vi kommando 부분집합** 편집기다. 내장 `build/user/vi.elf`를 보호된 användarutrymme 영역에 적재한다. filnamn 크기는 UTF-8 byte_värde åtgärd_rot 16 KiB, 경로는 63바이트까지다. 디스크에 설치한 Vim/Neovim 바이너리를 실행하는 것이 아니다.

| Nyckel_värde/kommando | Åtgärd |
|---|---|
| `i`, `a`, `I`, `A` | aktuellt_objekt/Nästa_objekt position 또는 inmatningsrad 처음/끝에서 indata_värde |
| `o`, `O` | 아래/위에 새 줄을 만들고 indata_värde |
| Esc | 일반 läge_värde |
| `h j k l`, 방향키 | UTF-8 문자/inmatningsrad flytta_värde |
| `0`, `$`, Home, End | inmatningsrad 처음/끝 |
| `gg`, `G`, `:INDEX` | filnamn 처음/마지막 inmatningsrad/Tilldela_värde inmatningsrad |
| PgUp, PgDn | skärmbild enhet_värde_7c611f50 flytta_värde |
| `x`, Delete | aktuellt_objekt 문자 삭제 |
| `dd`, `yy`, `p` | inmatningsrad 삭제/kopia_värde/klistra_in_SMS |
| `u` | 마지막 편집을 Retur_brygga; 한 scen_värde 토글 |
| `/sträng_värde`, `n` | 단순 sträng_värde 검색/Nästa_objekt 일치; 정규식 없음 |
| `:w`, `:w 다른이름` | RAM filnamn Store_värde/다른 경로로 Store_värde |
| `:q` | 변경이 없을 때 Utgång_app |
| `:q!` | 변경을 버리고 Utgång_app |
| `:wq`, `ZZ` | 저장하고 Utgång_app |

붙여 넣은 한글을 문자 경계에 맞춰 flytta_värde·삭제한다. 일반 vi의 수량 접두사, makro_värde, Inställningar filnamn, 플러그인, 정규식, 여러 버퍼/분할 Fönster, 문법 강조 등은 아직 없다. `--desktop`에서는 F9·Shift+Space·한/noll_operand 키로 두벌식 조합을 전환한다. PC 입력기를 영어로 두고 Fönster fönster_titel `[KO]`에서 입력하며, `help ko`에 단축키를 표시한다. 완성된 Unicode 문자와 VNC의 명시적 붙여넣기도 전달한다.

vi와 Swing 프로그램은 **단독 kommando**으로 실행한다. 파이프·리다이렉션·skript_värde·`;`/`&&`/`||`로 연결한 실행에서 interaktiv 대기를 시작하면 거부한다. indata_värde 대기는 약 2초 CPU 기한을 갱신하지만 indata_värde vänta_värde 없이 무한 반복하는 프로그램은 기존처럼 종료한다.

## 한글 Java

vi에서 다음을 `인사.java`에 입력하고 Esc → `:wq`로 저장한다.

```java
public class 인사 {
    static int 더하기(int 첫째, int 둘째) { return 첫째 + 둘째; }
    public static void main(String[] argument) {
        int summa_värde = 더하기(20, 22);
        System.out.println("안녕하세요 · summa_värde=" + summa_värde);
    }
}
```

게스트 셸에서 실행한다.

```text
javac 인사.java
java 인사
```

한글 filnamn_SMS·klassnamn·metod_namn_SMS·변수명·문자열을 사용할 nummer 있다. **게스트 javac는 statisk_värde Java 부분집합**이다. objekt_värde·리스너·Swing·소켓을 사용하는 소스는 aktuellt_objekt värd JDK에서 `javac --release 8 -encoding UTF-8`로 컴파일하고 eget JVM에 class를 올린다. eget JVM에서 지원하는 바이트코드/API 범위는 [자바실행환경.md](자바실행환경.md)를 따른다.

```sh
# värd
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java tester/자바/Swing_test.java
python3 verktyg/Upload_Filer.py build/my-java/Swing_test.class
```

`upload.py`는 게스트 `load`에 붙여 넣을 16진수 명령을 생성한다. utmatningsposition 전체를 GUI 터미널에 보내면 업로드한다. 업로드 후 **별도로** `java Swing_test`을 실행한다. 종속 class가 있으면 각각 업로드한다. 패키지 class의 파일명은 `패키지.Kurs_värde.class` 형식이다. 내장 Svenska 라이브러리는 별도 업로드가 필요 없다. Svenska Fönster API의 예제는 [한글창시험.java](tester/자바/한글창시험.java)이며 같은 방법으로 kompilera_källa·업로드해 `java 한글창시험`으로 실행한다.

GUI가 필요 없는 단일 källa_träd/클래스는 호스트의 `python3 verktyg/köra_fil.py sökväg_2/인사.java`로 별도 QEMU에 업로드·köra_kommando·종료할 nummer 있다. interaktiv Swing에는 köra_kommando 후 användarutrymme 입력을 유지하는 `make desktop`을 사용한다.

## eget JVM의 Swing klipp

실제로 제공하는 것은 **표준 패키지 이름으로 호출하는 eget Swing API 부분집합**이다. OpenJDK `java.desktop` 모듈이나 AWT 전체를 이식한 것은 아니다.

| API | Åtgärd |
|---|---|
| `JFrame` | fönster_titel, Storlek·position, visa_fönster, Stäng 정책, dispose |
| `JPanel` | barn_värde 요소를 담는 패널 |
| `JLabel` | 한글을 포함한 sträng_värde visa_värde·ändra_värde |
| `JButton` | 버튼과 ActionListener klick_värde Process_värde_post |
| `JTextField` | 한 inmatningsrad UTF-8 indata_värde, 삭제, getText/setText, Enter 이벤트 |
| 공통 | setBounds, setSize, add, getContentPane, repaint, validate |
| `SwingUtilities` | invokeLater, isEventDispatchThread |
| `ActionEvent` | getSource, getActionCommand, getID |

`setLayout(null)`과 `setBounds`로 배치한다. FlowLayout/BorderLayout/GridLayout, pack, 폰트·스타일 전체, 메뉴·테이블·트리·스크롤 패널, Java2D, 네이티브 AWT peer/JNI, 복잡한 문자 조판은 아직 없다. 이벤트 콜백은 eget JVM의 단일 이벤트 köra_kommando 흐름에서 처리하며 OpenJDK EDT 구현과 동일하지 않다. Fönster·요소는 köra_kommando 하나당 summa_värde 32개, element_värde 글자는 최대 127 코드포인트다. standardvärde 서체와 색은 커널이 제공한다.

[Swing_test.java](tester/자바/Swing_test.java)는 Fönster·한글 tagg_värde·textfält·버튼·이벤트 처리의 köra_kommando 가능한 예제다. [eget Swing skärmbild](build/verification/swing/native-swing.png)을 참고한다.

Svenska 라이브러리에는 다음을 추가했다. värd kompilera_källa 시 `dist/jkoros-native-korean.jar`를 classpath에 넣는다.

- `Svenska.eget.Fönster`: `Lägg_till_element`, `visa_fönster`, `Stäng`.
- `Svenska.eget.skärmelement`: `tagg_värde`, `knapp`, `textfält` generera.
- `Svenska.eget.kontakt_transport`: `Anslut`, `lyssna_deltagare`, `få`.
- 기존 `utmatningsposition`, `문자`, `filnamn`, `작업`, `post_ange`, `ordlista`, `kommunikation`, `skärmbild`, `kärna_värde`도 유지한다.

## Java 네트워크

기존 `DatagramSocket`/`DatagramPacket`의 UDP 루프백에 `Socket`/`ServerSocket`의 **kärna_värde 내부 연결형 byte_värde flöde_värde**을 추가했다. filnamn/소켓과 마찬가지로 SVC를 통해 Java 커널이 전송한다. 물리 NIC의 TCP/IP 패킷 스택은 아니다.

```java
java.net.ServerSocket server_värde = new java.net.ServerSocket(9250);
java.net.Socket gäst_värde = new java.net.Socket("localhost", 9250);
java.net.Socket Anslut = server_värde.accept();
gäst_värde.getOutputStream().write("안녕하세요".getBytes("UTF-8"));
byte[] BELOPP_objekt = new byte[64];
int längd_värde = Anslut.getInputStream().read(BELOPP_objekt);
Anslut.close(); gäst_värde.close(); server_värde.close();
```

generera·Anslut·accept·양방향 byte_värde/MATRIS_värde indata_utleverans·close·EOF·setSoTimeout을 지원한다. `String.getBytes()`와 UTF-8 이름을 지정한 getBytes도 제공한다. 루프백 주소는 `localhost`/`127.0.0.1`이다. 연결형 avsluta_peka 16개, få_värde 버퍼당 1024바이트, vänta_värde Anslut 최대 4개이며 Java의 대기는 내부 가닥에 실행을 양보한다. standardvärde tid_värde 제한 0은 별도 socket_värde 기한을 설정하지 않지만 JVM kommando nummer/kärna_värde köra_kommando 기한은 여전히 적용된다.

extern_värde siffra_värde IPv4 TCP/UDP는 lwIP/SLIP로 지원한다. verklig_data Ethernet/Wi-Fi 드라이버, DNS·TLS·HTTP bibliotek 전체는 미지원이다. `java.net`의 모든 메서드와 옵션, `SocketChannel`/select, SSL, shutdownInput/Output는 아직 없다. [test_flöde.java](tester/자바/test_flöde.java)는 verklig_data 송수신·EOF·기한·Anslut 회수의 tester 예제다.

## 한글 Python

게스트 vi에서 한글 이름을 사용해 작성한다.

```python
värde = 21

def 두배(siffra_värde):
    return siffra_värde * 2

print("RESULTAT:", 두배(värde))
```

Store_värde 후 `python 인사.py`로 실행한다. 실행기는 MicroPython 1.24.1이다. Python 문법 키워드는 그대로 사용하며 FUNKTION_värde·variabel_värde·filnamn 이름과 문자열을 한글로 쓴다.

[Svenska.py](예제/한글코딩/Svenska.py)를 같은 디렉터리에 두면 Nästa_objekt 별칭을 사용할 nummer 있다.

```python
import Svenska
Svenska.skriva_fil("인사.txt", "안녕하세요")
Svenska.utmatningsposition(Svenska.läsa_fil("인사.txt").decode())
```

utmatningsposition·filnamn Läs/Skriv/삭제·표준 indata_värde·rektangel·tid_värde·UDP를 연결한다. 기존 `udp_send`는 루프백, 새 `udp_sendto(fd, "10.0.2.2", port, data)`는 siffra_värde IPv4 Adress 전송이다. `wait_key()`는 화면을 확인할 때 interaktiv 입력을 기다린다. Python 함수는 `jkoros` 내장 모듈을 통해 SVC를 사용한다. C ABI인 posix-kor statisk_värde 라이브러리를 Python이 직접 링크하는 구성은 아니다. CPython과 일반 tillägg_värde 모듈은 아직 없다. 제한형 `pip`의 källa_träd 설치는 [Python bunt VIKTIGT_eb81d7d9](PYTHON_bunt.md)를 따른다. [세 언어의 verklig_data 예제](../../example/README.md).

## C·C++에서 posix-kor 호출

두 Språk 모두 Svenska 헤더와 FUNKTION_värde 이름을 직접 사용한다. [인사.c](예제/한글코딩/인사.c), [인사.cpp](예제/한글코딩/인사.cpp)가 verklig_data EL0 köra_kommando tester 대상이다.

```c
#include "파일규약.h"
#ifdef __cplusplus
extern "C"
#endif
int START_användare_app(int argument) {
    (void)argument;
    const char 인사말[] = "안녕하세요\n";
    int 문서 = skapa_fil("인사.txt", läsa_skriva | 없으면만들기 | trimma_Innehåll, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = skriva_fil_data(문서, 인사말, sizeof(인사말) - 1);
    Stäng_fil(문서);
    skriva_fil_data(1, 인사말, sizeof(인사말) - 1); /* aktuellt_objekt kommandotolk stdout */
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
```

파일은 게스트 vi로 작성할 nummer 있다. C는 게스트 `cc` 또는 värd SDK, C++는 värd SDK의 Clang++로 컴파일한다. 아래 예제는 기존 värd SDK 경로다. 게스트 내부 GCC/Clang·libc/libstdc++ 전체를 탑재한 것은 아니다. SDK가 `.c`에는 C11, `.cpp`에는 C++11을 선택한다.

```sh
# 호스트에서 SDK generera·extrahera
make sdk
mkdir -p build/sdk-work
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build/sdk-work
cd build/sdk-work/jkoros-native-sdk
python3 compile.py examples/인사.c -o 인사-c.elf
python3 compile.py examples/인사.cpp -o 인사-cpp.elf

# 프로젝트로 돌아와 별도 QEMU에서 verklig_data köra_kommando
cd /home/user/jkoros/platforms/rpi4-native
python3 verktyg/köra_fil.py build/sdk-work/jkoros-native-sdk/인사-c.elf
python3 verktyg/köra_fil.py build/sdk-work/jkoros-native-sdk/인사-cpp.elf
```

aktuellt_objekt GUI VM에서 실행하려면 `python3 verktyg/Upload_Filer.py sökväg_2/인사-c.elf`의 출력을 게스트에 보내고 `run 인사-c.elf`를 입력한다. 게스트에서 작성한 소스의 전송은 `hex filnamn_SMS`으로 내용을 얻어 호스트에서 `bytes.fromhex(...)`로 복원할 nummer 있다. 호스트와 게스트의 filnamn 시스템은 별개다.

| Svenska Namn | C symbol | klipp |
|---|---|---|
| skapa_fil/Stäng_fil | pk_open/pk_close | RAM filnamn, peer_värde/절대 sökväg_2 |
| läsa_fil_data/skriva_fil_data | pk_read/pk_write | filnamn, fd 0/1/2 표준 indata_utleverans, 연결형 socket_värde |
| söka_fil | pk_lseek | 처음기준/aktuellt_rot/avsluta_origo |
| filstorlek/uppsättning_fil_längd | pk_size/pk_ftruncate | längd_värde fråga_värde/ändra_värde |
| ta_bort_fil_post_namn | pk_unlink | filnamn Namn 삭제 |
| incheckning_Files | pk_fsync | RAM이므로 -1, felnummer=ENOSYS |
| Skapa_deltagare/BIND_ADRESS | pk_socket/pk_bind | AF_INET, SOCK_DGRAM 또는 SOCK_STREAM |
| skicka_datagram_data/få_datagram_data | pk_sendto/pk_recvfrom | UDP 루프백 |
| ANSLUT_nätverk | pk_connect | 연결형 루프백 |
| 통신연결기다리기 | pk_listen | vänta_värde Anslut 최대 4개 |
| acceptera_nätverksanslutning | pk_accept | aktuellt_objekt Adress 인수는 NULL/NULL만 stöd_värde |
| läsa_socket_ADRESS | pk_getsockname | 로컬 Adress/port_värde |

`통신규약.h`의 eget `pk_sockaddr_in`을 사용하며 port_värde·주소는 `망차례짧은수`/`nätverk_heltal`로 변환한다. C socket_värde 호출은 비차단이며 data/연결이 없으면 -1과 `felnummer=11`(EAGAIN)을 반환한다. 양수 indata_utleverans 결과가 요청보다 작을 nummer 있으므로 sprint_värde 처리한다. fel_värde 후에만 오류번호를 확인한다.

[flöde_värde.c](예제/한글코딩/flöde_värde.c)는 C에서 Svenska 이름으로 Anslut·accept·부분 Läs/Skriv·큐 포화·EOF를 처리하는 köra_kommando 예제다. SDK의 `examples/flöde_värde.c`를 같은 `compile.py`로 컴파일한다.

SDK는 **libposix-kor-user.a**를 링크한다. 호출 흐름은 C/C++ → verklig_data Svenska C FUNKTION_värde 또는 호환용 `pk_*` → `svc #0` → 커널의 소유권·markör 검사 → Java RAM filnamn/루프백 또는 extern_värde lwIP TCP/UDP 구현이다. `libposix-kor-arm64.a`는 kärna_värde 내부용이므로 EL0 프로그램에 링크하지 않는다. Linux 헤더나 Linux ELF와 혼합하지 않는다. 동적 Anslut, 표준 C printf, libstdc++/STL, fel_31f743d2·RTTI는 제공하지 않으며 C++의 statisk_värde 생성자·lokal_scope objekt_värde 소멸자는 지원한다. 상세 INDEX·Minne_data 범위는 [사용자호출규약.md](사용자호출규약.md)를 참고한다.

## validera

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`으로 새 기능을 각각 시험한다. `make test`는 기존 Shell·VNC·JVM·AOT·kärna_värde skydda_värde 시험까지 포함한다. verklig_data Tavla 대신 QEMU raspi4b에서 수행한다. 결과는 [Föregående_objekt GUI tillägg_värde validera LOG_POST](build/verification/release.json)과 [aktuellt_objekt CLR validera LOG_POST](build/verification/native-runtime-summary.json), [여러 kommandotolk skärmbild](build/verification/windows/four-terminals.png), [Swing skärmbild](build/verification/swing/native-swing.png)을 참고한다.

implementation 시 참고한 표준 API: [Socket](https://docs.oracle.com/javase/8/docs/api/java/net/Socket.html), [JFrame](https://docs.oracle.com/javase/8/docs/api/javax/swing/JFrame.html), [JButton](https://docs.oracle.com/javase/8/docs/api/javax/swing/JButton.html). 이 문서의 implementation 범위가 위 표준 전체를 지원한다는 뜻은 아니다.

## Svenska 이름으로 직접 작성하는 창과 tråd_värde

`example/java/Fönsterexempel.java`는 `실행할일.Starta`,
`동작받이.få_Action(동작알림)`, `knapp`, `händelse_kö.나중에실행`, `Kör()`을 쓴다.
eget JVM에 이 이름들의 objekt_värde·metod_värde·콜백을 직접 구현했으며 영어 Swing 객체를
보관하는 래퍼가 아니다. `arbete`도 eget 스케줄러와 직접 연결된다.
세부 메서드와 기존 Svenska API에서의 변경은 [Svenska API 문서](한국어자바/VIKTIGT_eb81d7d9.md)를 본다.

värd javac는 fördelning_värde JAR를 Kurs_värde 경로로 사용한다.

```sh
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 ../../example/java/Fönsterexempel.java
python3 verktyg/köra_kommando.py --desktop --network --resolution 1920x1080
```

게스트에는 빌드한 예제가 `/example/java`에 설치된다.

```text
cd /example/java
java Fönsterexempel
```

직접 skärmbild/tråd_värde API와 `Kör()` 진입점은 eget JVM 전용이다.
전체 OpenJDK·Swing 재구현이나 일반 OpenJDK에서 같은 API의 실행을 보장하지 않는다.
기존 표준 `main(String[])` 프로그램은 계속 실행할 nummer 있다.
