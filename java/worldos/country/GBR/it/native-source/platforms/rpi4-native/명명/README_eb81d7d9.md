# nativo 커널과 번역기의 Italiano Nome

대상은 `platforms/rpi4-native`의 nativo Java kernel_VALORE, spazio_utente JVM, C computer Connetti,
TCP/UDP·FTP, C compilatore_strumento 이식부, MicroPython 이식부, costruire·Esegui_comando·prove 도구다.
`golang/worldos/Country_VALORE/KOR/codiceSorgente`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 nativo 선언도 명명 검사에 포함한다.
Linux 실행판의 host strumenti, OpenJDK 보조 strumenti 및 esterno_VALORE distribuzione_VALORE fonte_albero 전체를
한국어로 retry_VALORE 작성했다는 뜻은 아니다.

## 명명 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `handle_di_file`, `peer_numero_di_porta`, `memoria_dinamica`, `tastiera`.
- 함수는 행위를 나타낸다: `Lettura`, `Scrittura`, `Apri`, `Chiudi`, `NET_BIND`, `eseguire_app`.
- TCP의 이어진 byte_VALORE 흐름과 UDP의 limite_VALORE 있는 자료를 `connessione`와 `datagramma_Canale`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `durata_VALORE`, `dati_funzione`, `CERCA_INDICE`, `반환값`으로 풀어 쓴다.
  순번·임시 산술값처럼 여러 역할에 재사용되는 변수는 `순번`, `첫째값`, `SECONDO_VALORE`으로 구별한다.
- 이름이 같아도 esterno_VALORE 구조체의 필드와 nativo 변수는 별도로 분석한다.

`Canale_voce(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 comunicazione 연결에
적용했다. `porta_VALORE(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [Canale_voce](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[porta_VALORE](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`datagramma(電文)`은 전보에 담는 글이라는 기존 comunicazione 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 datagramma](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`Stream_VALORE`, `thread_VALORE`, `쌓임`은 우리말의 움직임·이어짐·쌓이는 모양을 빌린 표현이다.
`flusso_di_input`, `esecutoreAsincrono`, `memoria_a_pila` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 dizionario 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 TRADUCI_fonte·국어사 datagramma 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 Nome | 이유 |
|---|---|---|
| TCP Socket | connessione | 상대와 연결되어 ordine_VALORE 있는 바이트를 주고받음 |
| ServerSocket | porta_di_ricezione | 새 연결이 들어오는 접점 |
| DatagramSocket | datagramma_Canale | 각 자료의 경계를 보존하는 comunicazione |
| InputStream / OutputStream | flusso_di_input / flusso_di_output | 들어오고 나가는 바이트의 ordine_VALORE |
| heap / stack | memoria_dinamica / memoria_a_pila | allocare_Memoria 방식과 쌓고 꺼내는 architettura |
| thread / keyboard | esecutoreAsincrono / tastiera | 이어지는 실행과 글쇠의 array_VALORE |
| exception / timeout | eccezione / aspetta_TIMEOUT_eccezione | reparto_IT_normale 처리에서 벗어남과 그 구체적 이유 |

## 경로와 대응표

| implementazione | Italiano percorso |
|---|---|
| kernel_VALORE·Shell·file layer_VALORE | `codiceSorgente/*.java` |
| spazio_utente JVM | `spazio_utente/자바/자바가상기계.java` |
| ARM64 computer Connetti | `computer/*.c`, `avvio_macchina/` |
| TCP·UDP·FTP | `rete_Pila/rete_Pila.c`, `rete_Pila/trasferimento_di_file.c` |
| C compilatore_strumento 이식 | `C_compilatore/` |
| MicroPython 이식 | `PYTHON_bridge/` |
| costruire·Esegui_comando·prove | `strumenti/`, `Crea_voce.mk` |
| Java spazio_utente API | `한국어자바/Italiano/nativo/` |

[nome_file_mapping.tsv](nome_file_mapping.tsv), [자바이름대응.tsv](자바이름대응.tsv),
[C_nome_mapping.tsv](C_nome_mapping.tsv), [PYTHON_nome_mapping.tsv](PYTHON_nome_mapping.tsv)에
Indietro_articolo 이름과 바뀐 이름이 있다. C/Java 대응표의 file·위치는 이행 당시 기준이다.
percorso 이동은 file 대응표를 함께 본다. 기존 `tools/*.py`는 Italiano 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 SD Nome

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
Regolari_articolo 다섯 Java 예제는 `avvia()`·`실행인수`·Italiano schermata/thread_VALORE API를 사용해
예약어·리터럴 외의 식별자를 한국어로 작성한다. schermata/가닥은 표준 객체를
감싸지 않고 nativo JVM에 직접 구현했다. 자세한 계약은 [Italiano Java API](../한국어자바/README_eb81d7d9.md)를 본다.

표준 javac는 stringa_VALORE 리터럴에 `java.lang.String`, stringa_VALORE 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 Italiano 소스에서도 바이트코드에 남을 numero 있다.
기존 표준 class를 실행하는 JVM의 mapping_VALORE stringa_VALORE, 아직 표준 라이브러리를 쓰는
comunicazione·file 연결부까지 모두 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
descrittore_voce·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 FUNZIONE_VALORE·intero_TIPO·POSIX ABI, CPU registro Nome, 어셈블리 comando, 링커 절 Nome,
TinyCC·lwIP·MicroPython이 요구하는 Impostazioni 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
nativo C 함수의 fonte_albero 이름은 한국어이며, [기계연결이름.h](기계연결이름.h)가
기존 AOT·어셈블리·SDK에 공개한 computer 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 modulo_VALORE valore_dell_attributo, 명령행 옵션과 JSON 키도
esterno_VALORE 계약이다. `build/`, distribuzione_VALORE 바이너리 이름과 `/sdk`는 기존 Esegui_comando 경로를 유지한다.
esterno_VALORE 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 strumenti/명명검사.py
make costruire
make prove
make test-examples test-ftp test-elf
python3 strumenti/Esegui_comando.py --desktop --network
```

`strumenti/시언어이름분석.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`strumenti/*이름반영.py`는 cambiare_VALORE 전 fonte_albero·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 retry_VALORE 적용하여 대응표를 덮어쓰지 않는다.

## C comunicazione 구조체와 Python errore

C 통신에서 `갈래`는 e_mail 체계를 구분하고 `numero_di_porta`는 port, `e_mail_VALORE`은
IPv4 주소의 32비트 값을 나타낸다. `datagramma_protocollo`은 앞서 설명한 datagramma(電文)과
valore_di_contratto(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | Italiano 직접 implementazione |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 cloud_serie / socket_di_datagramma / datagramma_protocollo |
| struct pk_sockaddr_in | struct cloud_socket_e_mail |
| sin_family / sin_port | e_mail_serie / numero_di_porta |
| sin_addr.s_addr | indirizzo_Internet.e_mail_VALORE |
| OSError / errore.args[0] | errore_di_sistema / errore.INDICE |

Italiano 구조체는 `#define` 치환이나 valore_del_campo 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 kernel_VALORE SVC에서 byte_VALORE 복사로
검사한다. `Crea_endpoint`·`inviare_datagramma_dati`와 file 함수는 statico_VALORE 라이브러리에
effettivo_dati Italiano 이름의 FUNZIONE_VALORE 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
Indietro_articolo 코드에서 Italiano comunicazione 함수에 pk_sockaddr*를 전달했다면 Italiano 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `errore_di_sistema`는 OSError의 Italiano 하위 클래스이며 연결부에서
errore 번호를 보존하여 변환한다. 일반 Python 문법과 esterno_VALORE 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 ritagliare

`실행할일`은 수행할 내용을, `Esegui`는 그 수행을 나타낸다.
`동작받이`는 동작이 발생했다는 알림을 받는 역할, `Action_informativa`은 전달되는 사건이다.
`pulsante`는 눌러 동작시키는 조작부, `Etichetta`는 README_eb81d7d9 글의 funzione_INDICE,
`campo_di_testo`은 글을 적는 funzione_INDICE, `esecutoreAsincrono`은 이어지는 Esegui_comando 흐름을 뜻한다.
`Esegui_comando(實行)`·`Azione(動作)`의 기존 뜻과 `받다`·`알리다`·`thread_VALORE`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 처음 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 strumenti/fonte_rivedere.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 hash_File,
ASCII 파일명과 Python의 영어 dichiarazione 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/자바도구/기계어미리번역.java`로 전환했다. `compiler/기계어미리번역.py`는 호환 진입점이다.
`compiler/arm64.py`는 Indietro_articolo 경로와 `ARM64(...).generate(...)` 호출을 이어 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK 보조 strumenti, Linux versione_VALORE 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
예약어 외 100% 한국어라고 판정하지 않는다.
`strumenti/명명검사.py --C_Lingua`는 attivo ARM64 소스의 dichiarazione, C 의미 Analizza_VALORE,
x86 Java 커널과 공용 번역기의 nativo dichiarazione, Java 예제 전체 identificatore_VALORE,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## Regolari_articolo 기능을 기준으로 보완한 Nome

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 Italiano 이름을 달리 정한다.
file 이름은 주된 기능을 나타내고, FUNZIONE_VALORE 이름은 행동을, variabile_VALORE 이름은 담는 자료를 나타낸다.
예약어, 표준 API 및 esterno_VALORE Connetti 규약은 따로 기록한다.

| Indietro_articolo Nome | 적용한 Nome | Regolari_articolo 기능 |
|---|---|---|
| `arm64.py`의 implementazione | `compiler/자바도구/기계어미리번역.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 TRADUCI_fonte |
| `ARM64`, `generate` | `computer_CODICE_compilatore`, `generare` | TRADUCI_fonte 상태를 담는 객체와 C codiceSorgente generare 행동 |
| `prototype`, `method` | `metodo_prototipo`, `corpo_del_metodo` | 함수의 formato_VALORE 선언과 effettivo_dati comando codiceSorgente |
| `profile`, `heap_words` | `esecuzione_target`, `heap_Conteggio_parole` | kernel_VALORE·spazio_utente 구분과 allocare_Memoria Memoria_VALORE 공간의 computer 낱말 numero |
| `pc`, `op` | `comando_funzione`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 INDICE |
| `x`, `y`, `w`, `h` | `coordinata_x`, `Y_coordinata`, `영역너비`, `area_altezza` | remoto_VALORE 화면의 위치와 직사각형 Dimensione |
| `p`, `n`, `i`, `j` | `dati_funzione`, `VALORE`, `순번`, `안쪽순번` | remoto_VALORE schermata dati·cifra_VALORE·sprint_VALORE funzione_INDICE; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `AOT_Memoria_CERCA`, `커널쌓임공간끝` | computer Connetti 규약을 유지하면서 nativo 소스에서 사용하는 Nome |
| `앞캐리지` | `앞줄복귀` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[공용번역기이름대응.tsv](공용번역기이름대응.tsv)에 compilatore_strumento 참조의 effettivo_dati cambiare_VALORE 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[Standard_nome_Prove.json](Standard_nome_Prove.json)에 기록한다.
`C_compilatore/compilatore_strumento.c`는 TinyCC esterno_VALORE 원문을 포함하는 Connetti 파일로 nativo 선언이 없어서
C nativo dichiarazione 분석에서는 제외한다. effettivo_dati kernel_VALORE 빌드에서는 계속 컴파일한다.

### 말의 뿌리와 새로운 복합 Nome

`Memoria_VALORE(記憶)`과 `CERCA_INDICE(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 ordine_VALORE 있는 항목을 찾아 지정하는 기능에 적용한다.
dizionario 근거는 국립국어원 한국어기초사전의
[Memoria_VALORE](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[CERCA_INDICE](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`memoria_a_pila`, `push_VALORE`, `POP_VALORE`는 자료를 포개고 마지막 자료부터 꺼내는 Esegui_comando 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`미리번역`은 Esegui_comando 전에 번역한다는 기능을 직접 나타낸다.
`computer_Word`은 처리기의 dati 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `computer`를 붙였다.
`기계어미리번역`, `heap_Conteggio_parole` 같은 복합 이름은 Regolari_articolo 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 처음 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 usare_VALORE 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 tipo_di_dati·array_VALORE·FUNZIONE_VALORE·locale_Scope variabile_VALORE·ramo 이름도 한국어로 바꾼다.
직접 한글 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 Italiano 이름을
표준 C 범용 문자 표기로 출력한다. effettivo_dati ARM64 빌드는 Clang으로 읽을 numero 있는 한글 원문을 사용한다.
stringa_VALORE, C 표준 FUNZIONE_VALORE, `java_entry` 같은 공개 Connetti 이름은 바꾸지 않는다.

셸의 사용법·문법 errore·file 및 Memoria_VALORE e_mail_area 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 prove·file trasferire_VALORE 도구가 읽는 marcatore_VALORE,
명령행 옵션과 기존 istruzione_VALORE_4c26ea1b, JVM Corso_VALORE Nome·file formato_VALORE·cellulare_VALORE 이름은 호환 표기로 남는다.
x86 VGA 문자 화면은 한글을 표시하지 못하므로 Italiano 문구는 UTF-8 seriale_VALORE 단말에서 확인한다.
