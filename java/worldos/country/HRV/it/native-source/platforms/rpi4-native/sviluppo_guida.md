# nativo 커널에서 vi·여러 terminale·한글 프로그래밍 사용하기

Italiano comunicazione·eccezione 사용법은 [Italiano Java API](한국어자바/README_eb81d7d9.md), FUNZIONE_VALORE·variabile_VALORE·file 이름의 변경과 어원 근거는 [명명 README_eb81d7d9](명명/README_eb81d7d9.md)를 참고한다.

대상은 `platforms/rpi4-native`의 nativo AArch64 Java 커널이다. vi와 Java/Python/C/C++ 프로그램은 EL0에서 실행한다. Linux 실행판과 별도이며 아래 Supporto_VALORE 목록은 전체 OpenJDK·Vim·POSIX 구현을 뜻하지 않는다.

게스트 `cc`/`jaot`, JAR 직접 Esegui_comando, esterno_VALORE TCP/UDP와 FTP는 [새 Esegui_comando 매뉴얼](파일전송과번역.md)을 참고한다.

## GUI와 여러 terminale

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, e_mail **127.0.0.1:5902**로 연결한다. schermata 위 **+ New terminal**, **Ctrl+Shift+T**로 터미널을 추가한다. 최대 네 개다. 위쪽 terminale 버튼 또는 창을 클릭해 선택하고 **F6**으로 순환한다. 제목줄을 끌어서 옮기고 **DESTRA 위 X**를 클릭하면 닫힌다. 마지막 창을 닫아도 위쪽 Esegui_comando 버튼으로 retry_VALORE colonna_VALORE numero 있다. 기존 `terminal`, `exit`, F12도 사용할 numero 있다.

창마다 Regolari_articolo 디렉터리, Shell variabile_VALORE, comando LOG_riga, input_VALORE 중인 명령과 app_f5044b9b Esegui_comando 상태를 보관한다. file 저장소는 공유한다. vi와 Swing의 이벤트 aspetta_VALORE 중에 다른 터미널로 전환하면 spazio_utente Memoria_dati·레지스터·file/socket_VALORE 연결을 보존했다가 돌아올 때 재개한다. **Regolari_articolo 네 프로그램이 동시에 CPU에서 실행되는 선점형 스케줄러는 아니다.** 계산 중인 프로그램은 Avanti_articolo input_VALORE aspetta_VALORE 또는 기존 Esegui_comando 기한까지 전환이 지연될 numero 있다.

X로 터미널을 닫으면 그 터미널의 Esegui_comando 중인 프로그램도 종료하며 descrittore_voce·소켓을 회수한다. 저장하지 않은 Modifica_VALORE 내용은 사라진다. 종료한 슬롯은 새 창에서 재사용한다. Regolari_articolo 모든 파일은 RAM에 있으며 VM 재시작 후에는 남지 않는다.

화면과 Finestra 판단은 게스트 커널이 처리한다. QEMU Esegui_comando 도구는 VNC 키와 마우스 좌표를 UART 패킷으로 전달한다. effettivo_dati Pi4 USB 입력기와 fisico_hardware 부팅은 아직 검증하지 않았다. 일반 UART 셸은 `make run`, GUI strumenti 종료는 host 터미널의 Ctrl+C다.

## vi usare_VALORE

```text
mkdir 작업
cd 작업
vi messaggio_di_saluto_ae353e94.py
```

`vi`는 새로 구현한 **vi comando 부분집합** 편집기다. 내장 `build/user/vi.elf`를 보호된 spazio_utente 영역에 적재한다. file 크기는 UTF-8 byte_VALORE azione_radice 16 KiB, 경로는 63바이트까지다. 디스크에 설치한 Vim/Neovim 바이너리를 실행하는 것이 아니다.

| tasto_VALORE/comando | Azione |
|---|---|
| `i`, `a`, `I`, `A` | Regolari_articolo/Avanti_articolo posizione 또는 riga_di_ingresso 처음/끝에서 input_VALORE |
| `o`, `O` | 아래/위에 새 줄을 만들고 input_VALORE |
| Esc | 일반 MODA_VALORE |
| `h j k l`, 방향키 | UTF-8 문자/riga_di_ingresso spostare_VALORE |
| `0`, `$`, Home, End | riga_di_ingresso 처음/끝 |
| `gg`, `G`, `:INDICE` | file 처음/마지막 riga_di_ingresso/Assegna_VALORE riga_di_ingresso |
| PgUp, PgDn | schermata unità_VALORE spostare_VALORE |
| `x`, Delete | Regolari_articolo 문자 삭제 |
| `dd`, `yy`, `p` | riga_di_ingresso 삭제/copiare_VALORE/incollare_SMS |
| `u` | 마지막 편집을 Reso_bridge; 한 area_VALORE_29ee1bb7 토글 |
| `/stringa_VALORE`, `n` | 단순 stringa_VALORE 검색/Avanti_articolo 일치; 정규식 없음 |
| `:w`, `:w 다른이름` | RAM file Store_VALORE/다른 경로로 Store_VALORE |
| `:q` | 변경이 없을 때 Esci_app |
| `:q!` | 변경을 버리고 Esci_app |
| `:wq`, `ZZ` | 저장하고 Esci_app |

붙여 넣은 한글을 문자 경계에 맞춰 spostare_VALORE·삭제한다. 일반 vi의 수량 접두사, macro_VALORE, Impostazioni file, 플러그인, 정규식, 여러 버퍼/분할 Finestra, 문법 강조 등은 아직 없다. `--desktop`에서는 F9·Shift+Space·한/zero_operando 키로 두벌식 조합을 전환한다. PC 입력기를 영어로 두고 Finestra finestra_titolo `[KO]`에서 입력하며, `help ko`에 단축키를 표시한다. 완성된 Unicode 문자와 VNC의 명시적 붙여넣기도 전달한다.

vi와 Swing 프로그램은 **단독 comando**으로 실행한다. 파이프·리다이렉션·script_VALORE·`;`/`&&`/`||`로 연결한 실행에서 interattivo 대기를 시작하면 거부한다. input_VALORE 대기는 약 2초 CPU 기한을 갱신하지만 input_VALORE aspetta_VALORE 없이 무한 반복하는 프로그램은 기존처럼 종료한다.

## 한글 Java

vi에서 다음을 `messaggio_di_saluto_ae353e94.java`에 입력하고 Esc → `:wq`로 저장한다.

```java
public class messaggio_di_saluto_ae353e94 {
    static int 더하기(int 첫째, int 둘째) { return 첫째 + 둘째; }
    public static void main(String[] argomenti) {
        int totale_VALORE = 더하기(20, 22);
        System.out.println("안녕하세요 · totale_VALORE=" + totale_VALORE);
    }
}
```

게스트 셸에서 실행한다.

```text
javac messaggio_di_saluto_ae353e94.java
java messaggio_di_saluto_ae353e94
```

한글 nome_file_SMS·nome_della_classe·metodo_nome_SMS·변수명·문자열을 사용할 numero 있다. **게스트 javac는 statico_VALORE Java 부분집합**이다. oggetto_VALORE·리스너·Swing·소켓을 사용하는 소스는 Regolari_articolo host JDK에서 `javac --release 8 -encoding UTF-8`로 컴파일하고 nativo JVM에 class를 올린다. nativo JVM에서 지원하는 바이트코드/API 범위는 [자바실행환경.md](자바실행환경.md)를 따른다.

```sh
# host
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java prove/자바/Swing_test.java
python3 strumenti/Upload_File.py build/my-java/Swing_test.class
```

`upload.py`는 게스트 `load`에 붙여 넣을 16진수 명령을 생성한다. uscitaTesto 전체를 GUI 터미널에 보내면 업로드한다. 업로드 후 **별도로** `java Swing_test`을 실행한다. 종속 class가 있으면 각각 업로드한다. 패키지 class의 파일명은 `패키지.Corso_VALORE.class` 형식이다. 내장 Italiano 라이브러리는 별도 업로드가 필요 없다. Italiano Finestra API의 예제는 [한글창시험.java](prove/자바/한글창시험.java)이며 같은 방법으로 compilare_fonte·업로드해 `java 한글창시험`으로 실행한다.

GUI가 필요 없는 단일 fonte_albero/클래스는 호스트의 `python3 strumenti/Esegui_File.py percorso/messaggio_di_saluto_ae353e94.java`로 별도 QEMU에 업로드·Esegui_comando·종료할 numero 있다. interattivo Swing에는 Esegui_comando 후 spazio_utente 입력을 유지하는 `make desktop`을 사용한다.

## nativo JVM의 Swing ritagliare

실제로 제공하는 것은 **표준 패키지 이름으로 호출하는 nativo Swing API 부분집합**이다. OpenJDK `java.desktop` 모듈이나 AWT 전체를 이식한 것은 아니다.

| API | Azione |
|---|---|
| `JFrame` | finestra_titolo, Dimensione·posizione, mostrare_finestra, Chiudi 정책, dispose |
| `JPanel` | figlio_VALORE 요소를 담는 패널 |
| `JLabel` | 한글을 포함한 stringa_VALORE mostrare_VALORE·cambiare_VALORE |
| `JButton` | 버튼과 ActionListener clic_VALORE Processi_VALORE_voce |
| `JTextField` | 한 riga_di_ingresso UTF-8 input_VALORE, 삭제, getText/setText, Enter 이벤트 |
| 공통 | setBounds, setSize, add, getContentPane, repaint, validate |
| `SwingUtilities` | invokeLater, isEventDispatchThread |
| `ActionEvent` | getSource, getActionCommand, getID |

`setLayout(null)`과 `setBounds`로 배치한다. FlowLayout/BorderLayout/GridLayout, pack, 폰트·스타일 전체, 메뉴·테이블·트리·스크롤 패널, Java2D, 네이티브 AWT peer/JNI, 복잡한 문자 조판은 아직 없다. 이벤트 콜백은 nativo JVM의 단일 이벤트 Esegui_comando 흐름에서 처리하며 OpenJDK EDT 구현과 동일하지 않다. Finestra·요소는 Esegui_comando 하나당 totale_VALORE 32개, elemento_VALORE 글자는 최대 127 코드포인트다. valore_predefinito 서체와 색은 커널이 제공한다.

[Swing_test.java](prove/자바/Swing_test.java)는 Finestra·한글 tag_VALORE·campo_di_testo·버튼·이벤트 처리의 Esegui_comando 가능한 예제다. [nativo Swing schermata](build/verification/swing/native-swing.png)을 참고한다.

Italiano 라이브러리에는 다음을 추가했다. host compilare_fonte 시 `dist/jkoros-native-korean.jar`를 classpath에 넣는다.

- `Italiano.nativo.Finestra`: `Aggiungi_elemento`, `mostrare_finestra`, `Chiudi`.
- `Italiano.nativo.elemento_grafico`: `tag_VALORE`, `pulsante`, `campo_di_testo` generare.
- `Italiano.nativo.connessione_trasporto`: `Connetti`, `essere_in_ascolto_endpoint`, `ricevere`.
- 기존 `uscitaTesto`, `문자`, `file`, `작업`, `voce_elenco`, `dizionario`, `comunicazione`, `schermata`, `kernel_VALORE`도 유지한다.

## Java 네트워크

기존 `DatagramSocket`/`DatagramPacket`의 UDP 루프백에 `Socket`/`ServerSocket`의 **kernel_VALORE 내부 연결형 byte_VALORE Stream_VALORE**을 추가했다. file/소켓과 마찬가지로 SVC를 통해 Java 커널이 전송한다. 물리 NIC의 TCP/IP 패킷 스택은 아니다.

```java
java.net.ServerSocket server_VALORE = new java.net.ServerSocket(9250);
java.net.Socket guest_VALORE = new java.net.Socket("localhost", 9250);
java.net.Socket Connetti = server_VALORE.accept();
guest_VALORE.getOutputStream().write("안녕하세요".getBytes("UTF-8"));
byte[] RICEV_SCAD_articolo = new byte[64];
int durata_VALORE = Connetti.getInputStream().read(RICEV_SCAD_articolo);
Connetti.close(); guest_VALORE.close(); server_VALORE.close();
```

generare·Connetti·accept·양방향 byte_VALORE/array_VALORE I_O·close·EOF·setSoTimeout을 지원한다. `String.getBytes()`와 UTF-8 이름을 지정한 getBytes도 제공한다. 루프백 주소는 `localhost`/`127.0.0.1`이다. 연결형 chiudere_p 16개, ricevere_VALORE 버퍼당 1024바이트, aspetta_VALORE Connetti 최대 4개이며 Java의 대기는 내부 가닥에 실행을 양보한다. valore_predefinito valore 제한 0은 별도 socket_VALORE 기한을 설정하지 않지만 JVM comando numero/kernel_VALORE Esegui_comando 기한은 여전히 적용된다.

esterno_VALORE cifra_VALORE IPv4 TCP/UDP는 lwIP/SLIP로 지원한다. effettivo_dati Ethernet/Wi-Fi 드라이버, DNS·TLS·HTTP Catalogo 전체는 미지원이다. `java.net`의 모든 메서드와 옵션, `SocketChannel`/select, SSL, shutdownInput/Output는 아직 없다. [test_Stream.java](prove/자바/test_Stream.java)는 effettivo_dati 송수신·EOF·기한·Connetti 회수의 prove 예제다.

## 한글 Python

게스트 vi에서 한글 이름을 사용해 작성한다.

```python
VALORE = 21

def 두배(cifra_VALORE):
    return cifra_VALORE * 2

print("risultato:", 두배(VALORE))
```

Store_VALORE 후 `python messaggio_di_saluto_ae353e94.py`로 실행한다. 실행기는 MicroPython 1.24.1이다. Python 문법 키워드는 그대로 사용하며 FUNZIONE_VALORE·variabile_VALORE·file 이름과 문자열을 한글로 쓴다.

[Italiano.py](예제/한글코딩/Italiano.py)를 같은 디렉터리에 두면 Avanti_articolo 별칭을 사용할 numero 있다.

```python
import Italiano
Italiano.scrivere_File("messaggio_di_saluto_ae353e94.txt", "안녕하세요")
Italiano.uscitaTesto(Italiano.파일읽기("messaggio_di_saluto_ae353e94.txt").decode())
```

uscitaTesto·file Lettura/Scrittura/삭제·표준 input_VALORE·rettangolo·valore·UDP를 연결한다. 기존 `udp_send`는 루프백, 새 `udp_sendto(fd, "10.0.2.2", port, data)`는 cifra_VALORE IPv4 e_mail 전송이다. `wait_key()`는 화면을 확인할 때 interattivo 입력을 기다린다. Python 함수는 `jkoros` 내장 모듈을 통해 SVC를 사용한다. C ABI인 posix-kor statico_VALORE 라이브러리를 Python이 직접 링크하는 구성은 아니다. CPython과 일반 estensione_VALORE 모듈은 아직 없다. 제한형 `pip`의 fonte_albero 설치는 [Python aggregare README_eb81d7d9](PYTHON_aggregare.md)를 따른다. [세 언어의 effettivo_dati 예제](../../example/README.md).

## C·C++에서 posix-kor 호출

두 Lingua 모두 Italiano 헤더와 FUNZIONE_VALORE 이름을 직접 사용한다. [messaggio_di_saluto_ae353e94.c](예제/한글코딩/messaggio_di_saluto_ae353e94.c), [messaggio_di_saluto_ae353e94.cpp](예제/한글코딩/messaggio_di_saluto_ae353e94.cpp)가 effettivo_dati EL0 Esegui_comando prove 대상이다.

```c
#include "File_ABI.h"
#ifdef __cplusplus
extern "C"
#endif
int START_USER_app(int argomenti) {
    (void)argomenti;
    const char messaggio_di_saluto[] = "안녕하세요\n";
    int Guides = aperto_File("messaggio_di_saluto_ae353e94.txt", in_lettura_scrittura | 없으면만들기 | tagliare_Sommario, 0600);
    if (Guides < 0) return 1;
    입출력결과형 기록한수 = scrivere_File_dati(Guides, messaggio_di_saluto, sizeof(messaggio_di_saluto) - 1);
    Chiudi_File(Guides);
    scrivere_File_dati(1, messaggio_di_saluto, sizeof(messaggio_di_saluto) - 1); /* Regolari_articolo terminale stdout */
    return 기록한수 == sizeof(messaggio_di_saluto) - 1 ? 0 : 2;
}
```

파일은 게스트 vi로 작성할 numero 있다. C는 게스트 `cc` 또는 host SDK, C++는 host SDK의 Clang++로 컴파일한다. 아래 예제는 기존 host SDK 경로다. 게스트 내부 GCC/Clang·libc/libstdc++ 전체를 탑재한 것은 아니다. SDK가 `.c`에는 C11, `.cpp`에는 C++11을 선택한다.

```sh
# 호스트에서 SDK generare·estrarre
make sdk
mkdir -p build/sdk-work
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build/sdk-work
cd build/sdk-work/jkoros-native-sdk
python3 compile.py examples/messaggio_di_saluto_ae353e94.c -o messaggio_di_saluto_ae353e94-c.elf
python3 compile.py examples/messaggio_di_saluto_ae353e94.cpp -o messaggio_di_saluto_ae353e94-cpp.elf

# 프로젝트로 돌아와 별도 QEMU에서 effettivo_dati Esegui_comando
cd /home/user/jkoros/platforms/rpi4-native
python3 strumenti/Esegui_File.py build/sdk-work/jkoros-native-sdk/messaggio_di_saluto_ae353e94-c.elf
python3 strumenti/Esegui_File.py build/sdk-work/jkoros-native-sdk/messaggio_di_saluto_ae353e94-cpp.elf
```

Regolari_articolo GUI VM에서 실행하려면 `python3 strumenti/Upload_File.py percorso/messaggio_di_saluto_ae353e94-c.elf`의 출력을 게스트에 보내고 `run messaggio_di_saluto_ae353e94-c.elf`를 입력한다. 게스트에서 작성한 소스의 전송은 `hex nome_file_SMS`으로 내용을 얻어 호스트에서 `bytes.fromhex(...)`로 복원할 numero 있다. 호스트와 게스트의 file 시스템은 별개다.

| Italiano Nome | C simbolo | ritagliare |
|---|---|---|
| aperto_File/Chiudi_File | pk_open/pk_close | RAM file, peer_VALORE/절대 percorso |
| 파일자료읽기/scrivere_File_dati | pk_read/pk_write | file, fd 0/1/2 표준 I_O, 연결형 socket_VALORE |
| cercare_File | pk_lseek | 처음기준/Regolari_radice/chiudere_origine |
| dimensioni_del_file/set_File_durata | pk_size/pk_ftruncate | durata_VALORE query_VALORE/cambiare_VALORE |
| rimuovere_File_voce_nome | pk_unlink | file Nome 삭제 |
| commit_File | pk_fsync | RAM이므로 -1, numero_errore=ENOSYS |
| Crea_endpoint/BIND_e_mail | pk_socket/pk_bind | AF_INET, SOCK_DGRAM 또는 SOCK_STREAM |
| inviare_datagramma_dati/ricevere_datagramma_dati | pk_sendto/pk_recvfrom | UDP 루프백 |
| CONNETTI_rete | pk_connect | 연결형 루프백 |
| 통신연결기다리기 | pk_listen | aspetta_VALORE Connetti 최대 4개 |
| accettare_connessione_di_rete | pk_accept | Regolari_articolo e_mail 인수는 NULL/NULL만 Supporto_VALORE |
| 통신주소읽기 | pk_getsockname | 로컬 e_mail/porta_VALORE |

`rete_ABI.h`의 nativo `pk_sockaddr_in`을 사용하며 porta_VALORE·주소는 `망차례짧은수`/`rete_intero`로 변환한다. C socket_VALORE 호출은 비차단이며 dati/연결이 없으면 -1과 `numero_errore=11`(EAGAIN)을 반환한다. 양수 I_O 결과가 요청보다 작을 numero 있으므로 sprint_VALORE 처리한다. errore_VALORE 후에만 오류번호를 확인한다.

[Stream_VALORE.c](예제/한글코딩/Stream_VALORE.c)는 C에서 Italiano 이름으로 Connetti·accept·부분 Lettura/Scrittura·큐 포화·EOF를 처리하는 Esegui_comando 예제다. SDK의 `examples/Stream_VALORE.c`를 같은 `compile.py`로 컴파일한다.

SDK는 **libposix-kor-user.a**를 링크한다. 호출 흐름은 C/C++ → effettivo_dati Italiano C FUNZIONE_VALORE 또는 호환용 `pk_*` → `svc #0` → 커널의 소유권·puntatore 검사 → Java RAM file/루프백 또는 esterno_VALORE lwIP TCP/UDP 구현이다. `libposix-kor-arm64.a`는 kernel_VALORE 내부용이므로 EL0 프로그램에 링크하지 않는다. Linux 헤더나 Linux ELF와 혼합하지 않는다. 동적 Connetti, 표준 C printf, libstdc++/STL, eccezione·RTTI는 제공하지 않으며 C++의 statico_VALORE 생성자·locale_Scope oggetto_VALORE 소멸자는 지원한다. 상세 INDICE·Memoria_dati 범위는 [USER_Chiama_ABI.md](USER_Chiama_ABI.md)를 참고한다.

## convalidare

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`으로 새 기능을 각각 시험한다. `make test`는 기존 Shell·VNC·JVM·AOT·kernel_VALORE proteggere_VALORE 시험까지 포함한다. effettivo_dati scheda 대신 QEMU raspi4b에서 수행한다. 결과는 [Indietro_articolo GUI estensione_VALORE convalidare LOG_riga](build/verification/release.json)과 [Regolari_articolo CLR convalidare LOG_riga](build/verification/native-runtime-summary.json), [여러 terminale schermata](build/verification/windows/four-terminals.png), [Swing schermata](build/verification/swing/native-swing.png)을 참고한다.

implementazione 시 참고한 표준 API: [Socket](https://docs.oracle.com/javase/8/docs/api/java/net/Socket.html), [JFrame](https://docs.oracle.com/javase/8/docs/api/javax/swing/JFrame.html), [JButton](https://docs.oracle.com/javase/8/docs/api/javax/swing/JButton.html). 이 문서의 implementazione 범위가 위 표준 전체를 지원한다는 뜻은 아니다.

## Italiano 이름으로 직접 작성하는 창과 thread_VALORE

`example/java/EsempioFinestra.java`는 `실행할일.Esegui`,
`동작받이.ricevere_Action(Action_informativa)`, `pulsante`, `evento_coda.나중에실행`, `avvia()`을 쓴다.
nativo JVM에 이 이름들의 oggetto_VALORE·metodo_VALORE·콜백을 직접 구현했으며 영어 Swing 객체를
보관하는 래퍼가 아니다. `esecutoreAsincrono`도 nativo 스케줄러와 직접 연결된다.
세부 메서드와 기존 Italiano API에서의 변경은 [Italiano API Guides](한국어자바/README_eb81d7d9.md)를 본다.

host javac는 distribuzione_VALORE JAR를 Corso_VALORE 경로로 사용한다.

```sh
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 ../../example/java/EsempioFinestra.java
python3 strumenti/Esegui_comando.py --desktop --network --resolution 1920x1080
```

게스트에는 빌드한 예제가 `/example/java`에 설치된다.

```text
cd /example/java
java EsempioFinestra
```

직접 schermata/thread_VALORE API와 `avvia()` 진입점은 nativo JVM 전용이다.
전체 OpenJDK·Swing 재구현이나 일반 OpenJDK에서 같은 API의 실행을 보장하지 않는다.
기존 표준 `main(String[])` 프로그램은 계속 실행할 numero 있다.
