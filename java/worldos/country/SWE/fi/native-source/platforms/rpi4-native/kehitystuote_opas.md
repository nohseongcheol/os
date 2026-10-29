# oma 커널에서 vi·여러 komentotulkki·한글 프로그래밍 사용하기

suomi 통신·poikkeus 사용법은 [suomi Java API](한국어자바/Lueminut_eb81d7d9.md), funktio_ARVO·muuttuja_ARVO·tiedoston_nimi 이름의 변경과 어원 근거는 [명명 Lueminut_eb81d7d9](명명/Lueminut_eb81d7d9.md)를 참고한다.

대상은 `platforms/rpi4-native`의 oma AArch64 Java 커널이다. vi와 Java/Python/C/C++ 프로그램은 EL0에서 실행한다. Linux 실행판과 별도이며 아래 Tuki_ARVO 목록은 전체 OpenJDK·Vim·POSIX 구현을 뜻하지 않는다.

게스트 `cc`/`jaot`, JAR 직접 Suorita_komento, ulkoinen_ARVO TCP/UDP와 FTP는 [새 Suorita_komento 매뉴얼](파일전송과번역.md)을 참고한다.

## GUI와 여러 komentotulkki

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, OSOITE **127.0.0.1:5902**로 연결한다. 화면 위 **+ New terminal**, **Ctrl+Shift+T**로 터미널을 추가한다. 최대 네 개다. 위쪽 komentotulkki 버튼 또는 창을 클릭해 선택하고 **F6**으로 순환한다. 제목줄을 끌어서 옮기고 **OIKEA 위 X**를 클릭하면 닫힌다. 마지막 창을 닫아도 위쪽 Suorita_komento 버튼으로 yrittää_uudelleen_ARVO SARAKE_ARVO numero 있다. 기존 `terminal`, `exit`, F12도 사용할 numero 있다.

창마다 nykyinen_kohde 디렉터리, liittymä muuttuja_ARVO, komento LOG_TIETUE, syöte_ARVO 중인 명령과 ohjelma_f5044b9b Suorita_komento 상태를 보관한다. tiedoston_nimi 저장소는 공유한다. vi와 Swing의 이벤트 odottaa_ARVO 중에 다른 터미널로 전환하면 käyttäjätila Muisti_data·레지스터·tiedoston_nimi/vastake_ARVO 연결을 보존했다가 돌아올 때 재개한다. **nykyinen_kohde 네 프로그램이 동시에 CPU에서 실행되는 선점형 스케줄러는 아니다.** 계산 중인 프로그램은 Seuraava_kohde syöte_ARVO odottaa_ARVO 또는 기존 Suorita_komento 기한까지 전환이 지연될 numero 있다.

X로 터미널을 닫으면 그 터미널의 Suorita_komento 중인 프로그램도 종료하며 서술자·소켓을 회수한다. 저장하지 않은 muutos_ARVO 내용은 사라진다. 종료한 슬롯은 새 창에서 재사용한다. nykyinen_kohde 모든 파일은 RAM에 있으며 VM 재시작 후에는 남지 않는다.

화면과 Ikkuna 판단은 게스트 커널이 처리한다. QEMU Suorita_komento 도구는 VNC 키와 마우스 좌표를 UART 패킷으로 전달한다. todellinen_data Pi4 USB 입력기와 실물 부팅은 아직 검증하지 않았다. 일반 UART 셸은 `make run`, GUI työkalut 종료는 isäntä 터미널의 Ctrl+C다.

## vi käyttö_ARVO

```text
mkdir 작업
cd 작업
vi 인사.py
```

`vi`는 새로 구현한 **vi komento 부분집합** 편집기다. 내장 `build/user/vi.elf`를 보호된 käyttäjätila 영역에 적재한다. tiedoston_nimi 크기는 UTF-8 tavu_ARVO aloite_juuri 16 KiB, 경로는 63바이트까지다. 디스크에 설치한 Vim/Neovim 바이너리를 실행하는 것이 아니다.

| Avain_ARVO/komento | Toiminto |
|---|---|
| `i`, `a`, `I`, `A` | nykyinen_kohde/Seuraava_kohde paikka 또는 syöterivi 처음/끝에서 syöte_ARVO |
| `o`, `O` | 아래/위에 새 줄을 만들고 syöte_ARVO |
| Esc | 일반 tila_ARVO |
| `h j k l`, 방향키 | UTF-8 문자/syöterivi siirrä_ARVO_83b651b8 |
| `0`, `$`, Home, End | syöterivi 처음/끝 |
| `gg`, `G`, `:INDEKSI` | tiedoston_nimi 처음/마지막 syöterivi/Määritä_ARVO syöterivi |
| PgUp, PgDn | 화면 osio_ARVO_7c611f50 siirrä_ARVO_83b651b8 |
| `x`, Delete | nykyinen_kohde 문자 삭제 |
| `dd`, `yy`, `p` | syöterivi 삭제/kopioida_ARVO/liitä_SMS_ea0cc186 |
| `u` | 마지막 편집을 palauttaa_silta; 한 vaihe_ARVO 토글 |
| `/merkkijono_ARVO`, `n` | 단순 merkkijono_ARVO 검색/Seuraava_kohde 일치; 정규식 없음 |
| `:w`, `:w 다른이름` | RAM tiedoston_nimi Store_ARVO/다른 경로로 Store_ARVO |
| `:q` | 변경이 없을 때 Lopeta_ohjelma |
| `:q!` | 변경을 버리고 Lopeta_ohjelma |
| `:wq`, `ZZ` | 저장하고 Lopeta_ohjelma |

붙여 넣은 한글을 문자 경계에 맞춰 siirrä_ARVO_83b651b8·삭제한다. 일반 vi의 수량 접두사, makro_ARVO, Asetukset tiedoston_nimi, 플러그인, 정규식, 여러 버퍼/분할 Ikkuna, 문법 강조 등은 아직 없다. `--desktop`에서는 F9·Shift+Space·한/nolla_operandi 키로 두벌식 조합을 전환한다. PC 입력기를 영어로 두고 Ikkuna ikkuna_nimi `[KO]`에서 입력하며, `help ko`에 단축키를 표시한다. 완성된 Unicode 문자와 VNC의 명시적 붙여넣기도 전달한다.

vi와 Swing 프로그램은 **단독 komento**으로 실행한다. 파이프·리다이렉션·komentosarja_ARVO·`;`/`&&`/`||`로 연결한 실행에서 vuorovaikutteinen 대기를 시작하면 거부한다. syöte_ARVO 대기는 약 2초 CPU 기한을 갱신하지만 syöte_ARVO odottaa_ARVO 없이 무한 반복하는 프로그램은 기존처럼 종료한다.

## 한글 Java

vi에서 다음을 `인사.java`에 입력하고 Esc → `:wq`로 저장한다.

```java
public class 인사 {
    static int 더하기(int 첫째, int 둘째) { return 첫째 + 둘째; }
    public static void main(String[] argumentit) {
        int summa_ARVO = 더하기(20, 22);
        System.out.println("안녕하세요 · summa_ARVO=" + summa_ARVO);
    }
}
```

게스트 셸에서 실행한다.

```text
javac 인사.java
java 인사
```

한글 tiedostonimi_SMS·luokan_nimi·menetelmä_nimi_SMS·변수명·문자열을 사용할 numero 있다. **게스트 javac는 staattinen_ARVO Java 부분집합**이다. objekti_ARVO·리스너·Swing·소켓을 사용하는 소스는 nykyinen_kohde isäntä JDK에서 `javac --release 8 -encoding UTF-8`로 컴파일하고 oma JVM에 class를 올린다. oma JVM에서 지원하는 바이트코드/API 범위는 [자바실행환경.md](자바실행환경.md)를 따른다.

```sh
# isäntä
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java testit/자바/swing_testi.java
python3 työkalut/Upload_Files.py build/my-java/swing_testi.class
```

`upload.py`는 게스트 `load`에 붙여 넣을 16진수 명령을 생성한다. tulostuspaikka 전체를 GUI 터미널에 보내면 업로드한다. 업로드 후 **별도로** `java swing_testi`을 실행한다. 종속 class가 있으면 각각 업로드한다. 패키지 class의 파일명은 `패키지.Luokka_ARVO.class` 형식이다. 내장 suomi 라이브러리는 별도 업로드가 필요 없다. suomi Ikkuna API의 예제는 [한글창시험.java](testit/자바/한글창시험.java)이며 같은 방법으로 kääntää_lähde·업로드해 `java 한글창시험`으로 실행한다.

GUI가 필요 없는 단일 lähde_puu/클래스는 호스트의 `python3 työkalut/Suorita_Tiedosto.py polku_2/인사.java`로 별도 QEMU에 업로드·Suorita_komento·종료할 numero 있다. vuorovaikutteinen Swing에는 Suorita_komento 후 käyttäjätila 입력을 유지하는 `make desktop`을 사용한다.

## oma JVM의 Swing leikata

실제로 제공하는 것은 **표준 패키지 이름으로 호출하는 oma Swing API 부분집합**이다. OpenJDK `java.desktop` 모듈이나 AWT 전체를 이식한 것은 아니다.

| API | Toiminto |
|---|---|
| `JFrame` | ikkuna_nimi, Koko·paikka, näyttää_ikkuna, Sulje 정책, dispose |
| `JPanel` | ali_ARVO 요소를 담는 패널 |
| `JLabel` | 한글을 포함한 merkkijono_ARVO näyttää_ARVO·muuttaa_ARVO |
| `JButton` | 버튼과 ActionListener osoittaa_ARVO prosessi_ARVO_merkintä |
| `JTextField` | 한 syöterivi UTF-8 syöte_ARVO, 삭제, getText/setText, Enter 이벤트 |
| 공통 | setBounds, setSize, add, getContentPane, repaint, validate |
| `SwingUtilities` | invokeLater, isEventDispatchThread |
| `ActionEvent` | getSource, getActionCommand, getID |

`setLayout(null)`과 `setBounds`로 배치한다. FlowLayout/BorderLayout/GridLayout, pack, 폰트·스타일 전체, 메뉴·테이블·트리·스크롤 패널, Java2D, 네이티브 AWT peer/JNI, 복잡한 문자 조판은 아직 없다. 이벤트 콜백은 oma JVM의 단일 이벤트 Suorita_komento 흐름에서 처리하며 OpenJDK EDT 구현과 동일하지 않다. Ikkuna·요소는 Suorita_komento 하나당 summa_ARVO 32개, elementti_ARVO 글자는 최대 127 코드포인트다. oletusarvo 서체와 색은 커널이 제공한다.

[swing_testi.java](testit/자바/swing_testi.java)는 Ikkuna·한글 tunnus_ARVO·tekstikenttä·버튼·이벤트 처리의 Suorita_komento 가능한 예제다. [oma Swing 화면](build/verification/swing/native-swing.png)을 참고한다.

suomi 라이브러리에는 다음을 추가했다. isäntä kääntää_lähde 시 `dist/jkoros-native-korean.jar`를 classpath에 넣는다.

- `suomi.oma.Ikkuna`: `Lisää_elementti`, `näyttää_ikkuna`, `Sulje`.
- `suomi.oma.näyttöelementti`: `tunnus_ARVO`, `painike`, `tekstikenttä` generoida.
- `suomi.oma.yhteys_välitys`: `Yhdistä`, `kuunnella_päätepiste`, `saada`.
- 기존 `tulostuspaikka`, `문자`, `tiedoston_nimi`, `작업`, `merkintä_luettelo`, `sanakirja`, `통신`, `화면`, `ydin_ARVO`도 유지한다.

## Java 네트워크

기존 `DatagramSocket`/`DatagramPacket`의 UDP 루프백에 `Socket`/`ServerSocket`의 **ydin_ARVO 내부 연결형 tavu_ARVO virta_ARVO**을 추가했다. tiedoston_nimi/소켓과 마찬가지로 SVC를 통해 Java 커널이 전송한다. 물리 NIC의 TCP/IP 패킷 스택은 아니다.

```java
java.net.ServerSocket palvelin_ARVO = new java.net.ServerSocket(9250);
java.net.Socket vieras_ARVO = new java.net.Socket("localhost", 9250);
java.net.Socket Yhdistä = palvelin_ARVO.accept();
vieras_ARVO.getOutputStream().write("안녕하세요".getBytes("UTF-8"));
byte[] SAATU_HINTA_kohde = new byte[64];
int kesto_ARVO = Yhdistä.getInputStream().read(SAATU_HINTA_kohde);
Yhdistä.close(); vieras_ARVO.close(); palvelin_ARVO.close();
```

generoida·Yhdistä·accept·양방향 tavu_ARVO/MATRIISI_ARVO I_O·close·EOF·setSoTimeout을 지원한다. `String.getBytes()`와 UTF-8 이름을 지정한 getBytes도 제공한다. 루프백 주소는 `localhost`/`127.0.0.1`이다. 연결형 lopettaa_puhelu_piste 16개, saada_ARVO 버퍼당 1024바이트, odottaa_ARVO Yhdistä 최대 4개이며 Java의 대기는 내부 가닥에 실행을 양보한다. oletusarvo AIKA_ARVO 제한 0은 별도 vastake_ARVO 기한을 설정하지 않지만 JVM komento numero/ydin_ARVO Suorita_komento 기한은 여전히 적용된다.

ulkoinen_ARVO numero_ARVO IPv4 TCP/UDP는 lwIP/SLIP로 지원한다. todellinen_data Ethernet/Wi-Fi 드라이버, DNS·TLS·HTTP kirjasto 전체는 미지원이다. `java.net`의 모든 메서드와 옵션, `SocketChannel`/select, SSL, shutdownInput/Output는 아직 없다. [testi_virta.java](testit/자바/testi_virta.java)는 todellinen_data 송수신·EOF·기한·Yhdistä 회수의 testit 예제다.

## 한글 Python

게스트 vi에서 한글 이름을 사용해 작성한다.

```python
ARVO = 21

def 두배(numero_ARVO):
    return numero_ARVO * 2

print("TULOS:", 두배(ARVO))
```

Store_ARVO 후 `python 인사.py`로 실행한다. 실행기는 MicroPython 1.24.1이다. Python 문법 키워드는 그대로 사용하며 funktio_ARVO·muuttuja_ARVO·tiedoston_nimi 이름과 문자열을 한글로 쓴다.

[suomi.py](예제/한글코딩/suomi.py)를 같은 디렉터리에 두면 Seuraava_kohde 별칭을 사용할 numero 있다.

```python
import suomi
suomi.kirjoitus_Tiedosto("인사.txt", "안녕하세요")
suomi.tulostuspaikka(suomi.lukea_Tiedosto("인사.txt").decode())
```

tulostuspaikka·tiedoston_nimi Luku/Kirjoitus/삭제·표준 syöte_ARVO·suorakulmio·AIKA_ARVO·UDP를 연결한다. 기존 `udp_send`는 루프백, 새 `udp_sendto(fd, "10.0.2.2", port, data)`는 numero_ARVO IPv4 OSOITE 전송이다. `wait_key()`는 화면을 확인할 때 vuorovaikutteinen 입력을 기다린다. Python 함수는 `jkoros` 내장 모듈을 통해 SVC를 사용한다. C ABI인 posix-kor staattinen_ARVO 라이브러리를 Python이 직접 링크하는 구성은 아니다. CPython과 일반 tarkenne_ARVO 모듈은 아직 없다. 제한형 `pip`의 lähde_puu 설치는 [Python nippu Lueminut_eb81d7d9](PYTHON_nippu.md)를 따른다. [세 언어의 todellinen_data 예제](../../example/README.md).

## C·C++에서 posix-kor 호출

두 Kieli 모두 suomi 헤더와 funktio_ARVO 이름을 직접 사용한다. [인사.c](예제/한글코딩/인사.c), [인사.cpp](예제/한글코딩/인사.cpp)가 todellinen_data EL0 Suorita_komento testit 대상이다.

```c
#include "파일규약.h"
#ifdef __cplusplus
extern "C"
#endif
int alku_käyttäjä_ohjelma(int argumentit) {
    (void)argumentit;
    const char 인사말[] = "안녕하세요\n";
    int 문서 = avata_Tiedosto("인사.txt", luku_ja_kirjoitus | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = kirjoitus_Tiedosto_data(문서, 인사말, sizeof(인사말) - 1);
    Sulje_Tiedosto(문서);
    kirjoitus_Tiedosto_data(1, 인사말, sizeof(인사말) - 1); /* nykyinen_kohde komentotulkki stdout */
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
```

파일은 게스트 vi로 작성할 numero 있다. C는 게스트 `cc` 또는 isäntä SDK, C++는 isäntä SDK의 Clang++로 컴파일한다. 아래 예제는 기존 isäntä SDK 경로다. 게스트 내부 GCC/Clang·libc/libstdc++ 전체를 탑재한 것은 아니다. SDK가 `.c`에는 C11, `.cpp`에는 C++11을 선택한다.

```sh
# 호스트에서 SDK generoida·purkaa
make sdk
mkdir -p build/sdk-work
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build/sdk-work
cd build/sdk-work/jkoros-native-sdk
python3 compile.py examples/인사.c -o 인사-c.elf
python3 compile.py examples/인사.cpp -o 인사-cpp.elf

# 프로젝트로 돌아와 별도 QEMU에서 todellinen_data Suorita_komento
cd /home/user/jkoros/platforms/rpi4-native
python3 työkalut/Suorita_Tiedosto.py build/sdk-work/jkoros-native-sdk/인사-c.elf
python3 työkalut/Suorita_Tiedosto.py build/sdk-work/jkoros-native-sdk/인사-cpp.elf
```

nykyinen_kohde GUI VM에서 실행하려면 `python3 työkalut/Upload_Files.py polku_2/인사-c.elf`의 출력을 게스트에 보내고 `run 인사-c.elf`를 입력한다. 게스트에서 작성한 소스의 전송은 `hex tiedostonimi_SMS`으로 내용을 얻어 호스트에서 `bytes.fromhex(...)`로 복원할 numero 있다. 호스트와 게스트의 tiedoston_nimi 시스템은 별개다.

| suomi Nimi | C symboli | leikata |
|---|---|---|
| avata_Tiedosto/Sulje_Tiedosto | pk_open/pk_close | RAM tiedoston_nimi, vertaissolmu_ARVO/절대 polku_2 |
| lukea_Tiedosto_data/kirjoitus_Tiedosto_data | pk_read/pk_write | tiedoston_nimi, fd 0/1/2 표준 I_O, 연결형 vastake_ARVO |
| hae_Tiedosto | pk_lseek | 처음기준/nykyinen_juuri/lopettaa_puhelu_origo |
| tiedostokoko/ryhmä_Tiedosto_kesto | pk_size/pk_ftruncate | kesto_ARVO kysely_ARVO/muuttaa_ARVO |
| poistaa_Tiedosto_merkintä_nimi | pk_unlink | tiedoston_nimi Nimi 삭제 |
| vahvistaa_muutokset_Files | pk_fsync | RAM이므로 -1, virhenumero=ENOSYS |
| Luo_päätepiste/BIND_OSOITE | pk_socket/pk_bind | AF_INET, SOCK_DGRAM 또는 SOCK_STREAM |
| lähettää_datagrammi_data/saada_datagrammi_data | pk_sendto/pk_recvfrom | UDP 루프백 |
| YHDISTÄ_verkko | pk_connect | 연결형 루프백 |
| 통신연결기다리기 | pk_listen | odottaa_ARVO Yhdistä 최대 4개 |
| hyväksyä_verkkoyhteys | pk_accept | nykyinen_kohde OSOITE 인수는 NULL/NULL만 Tuki_ARVO |
| lukea_vastake_OSOITE | pk_getsockname | 로컬 OSOITE/portti_ARVO |

`통신규약.h`의 oma `pk_sockaddr_in`을 사용하며 portti_ARVO·주소는 `망차례짧은수`/`verkko_kokonaisluku`로 변환한다. C vastake_ARVO 호출은 비차단이며 data/연결이 없으면 -1과 `virhenumero=11`(EAGAIN)을 반환한다. 양수 I_O 결과가 요청보다 작을 numero 있으므로 sprintti_ARVO 처리한다. virhe_ARVO 후에만 오류번호를 확인한다.

[virta_ARVO.c](예제/한글코딩/virta_ARVO.c)는 C에서 suomi 이름으로 Yhdistä·accept·부분 Luku/Kirjoitus·큐 포화·EOF를 처리하는 Suorita_komento 예제다. SDK의 `examples/virta_ARVO.c`를 같은 `compile.py`로 컴파일한다.

SDK는 **libposix-kor-user.a**를 링크한다. 호출 흐름은 C/C++ → todellinen_data suomi C funktio_ARVO 또는 호환용 `pk_*` → `svc #0` → 커널의 소유권·osoitin 검사 → Java RAM tiedoston_nimi/루프백 또는 ulkoinen_ARVO lwIP TCP/UDP 구현이다. `libposix-kor-arm64.a`는 ydin_ARVO 내부용이므로 EL0 프로그램에 링크하지 않는다. Linux 헤더나 Linux ELF와 혼합하지 않는다. 동적 Yhdistä, 표준 C printf, libstdc++/STL, poikkeus·RTTI는 제공하지 않으며 C++의 staattinen_ARVO 생성자·paikallinen_laajuus objekti_ARVO 소멸자는 지원한다. 상세 INDEKSI·Muisti_data 범위는 [사용자호출규약.md](사용자호출규약.md)를 참고한다.

## vahvista

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`으로 새 기능을 각각 시험한다. `make test`는 기존 liittymä·VNC·JVM·AOT·ydin_ARVO suojata_ARVO 시험까지 포함한다. todellinen_data Taulu 대신 QEMU raspi4b에서 수행한다. 결과는 [Edellinen_kohde GUI tarkenne_ARVO vahvista LOG_TIETUE](build/verification/release.json)과 [nykyinen_kohde CLR vahvista LOG_TIETUE](build/verification/native-runtime-summary.json), [여러 komentotulkki 화면](build/verification/windows/four-terminals.png), [Swing 화면](build/verification/swing/native-swing.png)을 참고한다.

toteutus 시 참고한 표준 API: [Socket](https://docs.oracle.com/javase/8/docs/api/java/net/Socket.html), [JFrame](https://docs.oracle.com/javase/8/docs/api/javax/swing/JFrame.html), [JButton](https://docs.oracle.com/javase/8/docs/api/javax/swing/JButton.html). 이 문서의 toteutus 범위가 위 표준 전체를 지원한다는 뜻은 아니다.

## suomi 이름으로 직접 작성하는 창과 säie_ARVO

`example/java/Ikkunaesimerkki.java`는 `실행할일.Suorita`,
`동작받이.saada_toimi(동작알림)`, `painike`, `tapahtuma_jono.나중에실행`, `Suorita_2()`을 쓴다.
oma JVM에 이 이름들의 objekti_ARVO·menetelmä_ARVO·콜백을 직접 구현했으며 영어 Swing 객체를
보관하는 래퍼가 아니다. `työntekijä`도 oma 스케줄러와 직접 연결된다.
세부 메서드와 기존 suomi API에서의 변경은 [suomi API 문서](한국어자바/Lueminut_eb81d7d9.md)를 본다.

isäntä javac는 jakelu_ARVO JAR를 Luokka_ARVO 경로로 사용한다.

```sh
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 ../../example/java/Ikkunaesimerkki.java
python3 työkalut/Suorita_komento.py --desktop --network --resolution 1920x1080
```

게스트에는 빌드한 예제가 `/example/java`에 설치된다.

```text
cd /example/java
java Ikkunaesimerkki
```

직접 화면/säie_ARVO API와 `Suorita_2()` 진입점은 oma JVM 전용이다.
전체 OpenJDK·Swing 재구현이나 일반 OpenJDK에서 같은 API의 실행을 보장하지 않는다.
기존 표준 `main(String[])` 프로그램은 계속 실행할 numero 있다.
