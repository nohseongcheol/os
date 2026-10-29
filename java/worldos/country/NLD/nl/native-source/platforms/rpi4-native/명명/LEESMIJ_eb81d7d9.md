# Eigen 커널과 번역기의 Nederlands Naam

대상은 `platforms/rpi4-native`의 Eigen Java kernel_WAARDE, gebruikersruimte JVM, C machine Verbinden,
TCP/UDP·FTP, C compiler_hulpmiddel 이식부, MicroPython 이식부, bouwen·Uitvoeren_opdracht·tests 도구다.
`golang/worldos/Country_WAARDE/KOR/broncode`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 Eigen 선언도 명명 검사에 포함한다.
Linux 실행판의 host hulpmiddelen, OpenJDK 보조 hulpmiddelen 및 extern_WAARDE distributie_WAARDE bron_structuur 전체를
한국어로 opnieuw_proberen_WAARDE 작성했다는 뜻은 아니다.

## 명명 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `bestandsingang`, `peer_poortnummer`, `dynamisch_geheugen`, `toetsenbord`.
- 함수는 행위를 나타낸다: `Lezen`, `Schrijven`, `Openen`, `Sluiten`, `NET_BIND`, `uitvoeren_app`.
- TCP의 이어진 byte_WAARDE 흐름과 UDP의 grens_WAARDE 있는 자료를 `verbinding`와 `datagram_Kanaal`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `tijdsduur_WAARDE`, `gegevens_functie`, `ZOEKEN_INDEX`, `반환값`으로 풀어 쓴다.
  순번·임시 산술값처럼 여러 역할에 재사용되는 변수는 `순번`, `첫째값`, `SECONDE_WAARDE`으로 구별한다.
- 이름이 같아도 extern_WAARDE 구조체의 필드와 Eigen 변수는 별도로 분석한다.

`Kanaal_invoer(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 communicatie 연결에
적용했다. `poort_WAARDE(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [Kanaal_invoer](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[poort_WAARDE](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`datagram(電文)`은 전보에 담는 글이라는 기존 communicatie 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 datagram](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`Stream_WAARDE`, `thread_WAARDE`, `쌓임`은 우리말의 움직임·이어짐·쌓이는 모양을 빌린 표현이다.
`invoerstroom`, `achtergrondwerker`, `stapelgeheugen` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 woordenlijst 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 VERTALEN_bron·국어사 datagram 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 Naam | 이유 |
|---|---|---|
| TCP Socket | verbinding | 상대와 연결되어 order_WAARDE 있는 바이트를 주고받음 |
| ServerSocket | ontvangen_poort | 새 연결이 들어오는 접점 |
| DatagramSocket | datagram_Kanaal | 각 자료의 경계를 보존하는 communicatie |
| InputStream / OutputStream | invoerstroom / uitvoerstroom | 들어오고 나가는 바이트의 order_WAARDE |
| heap / stack | dynamisch_geheugen / stapelgeheugen | toewijzen_Opslag 방식과 쌓고 꺼내는 architectuur |
| thread / keyboard | achtergrondwerker / toetsenbord | 이어지는 실행과 글쇠의 MATRIX_WAARDE |
| exception / timeout | uitzondering / wachten_TIMEOUT_uitzondering | informatie_normaal 처리에서 벗어남과 그 구체적 이유 |

## 경로와 대응표

| implementatie | Nederlands pad |
|---|---|
| kernel_WAARDE·Shell·bestand laag_WAARDE | `broncode/*.java` |
| gebruikersruimte JVM | `gebruikersruimte/자바/자바가상기계.java` |
| ARM64 machine Verbinden | `machine/*.c`, `machineopstart/` |
| TCP·UDP·FTP | `net_stack/net_stack.c`, `net_stack/bestandsoverdracht.c` |
| C compiler_hulpmiddel 이식 | `C_compiler/` |
| MicroPython 이식 | `PYTHON_brug/` |
| bouwen·Uitvoeren_opdracht·tests | `hulpmiddelen/`, `maken_invoer.mk` |
| Java gebruikersruimte API | `한국어자바/Nederlands/Eigen/` |

[bestandsnaam_toewijzing.tsv](bestandsnaam_toewijzing.tsv), [자바이름대응.tsv](자바이름대응.tsv),
[C_naam_toewijzing.tsv](C_naam_toewijzing.tsv), [PYTHON_naam_toewijzing.tsv](PYTHON_naam_toewijzing.tsv)에
Vorige_item 이름과 바뀐 이름이 있다. C/Java 대응표의 bestand·위치는 이행 당시 기준이다.
pad 이동은 bestand 대응표를 함께 본다. 기존 `tools/*.py`는 Nederlands 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 SD Naam

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
actueel_item 다섯 Java 예제는 `starten()`·`실행인수`·Nederlands scherm/thread_WAARDE API를 사용해
예약어·리터럴 외의 식별자를 한국어로 작성한다. scherm/가닥은 표준 객체를
감싸지 않고 Eigen JVM에 직접 구현했다. 자세한 계약은 [Nederlands Java API](../한국어자바/LEESMIJ_eb81d7d9.md)를 본다.

표준 javac는 tekenreeks_WAARDE 리터럴에 `java.lang.String`, tekenreeks_WAARDE 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 Nederlands 소스에서도 바이트코드에 남을 nummer 있다.
기존 표준 class를 실행하는 JVM의 toewijzing_WAARDE tekenreeks_WAARDE, 아직 표준 라이브러리를 쓰는
communicatie·bestand 연결부까지 모두 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
서술자·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 FUNCTIE_WAARDE·geheel_getal_TYPE·POSIX ABI, CPU register Naam, 어셈블리 opdracht, 링커 절 Naam,
TinyCC·lwIP·MicroPython이 요구하는 Instellingen 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
Eigen C 함수의 bron_structuur 이름은 한국어이며, [기계연결이름.h](기계연결이름.h)가
기존 AOT·어셈블리·SDK에 공개한 machine 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 module_WAARDE kenmerkwaarde, 명령행 옵션과 JSON 키도
extern_WAARDE 계약이다. `build/`, distributie_WAARDE 바이너리 이름과 `/sdk`는 기존 Uitvoeren_opdracht 경로를 유지한다.
extern_WAARDE 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 hulpmiddelen/명명검사.py
make bouwen
make tests
make test-examples test-ftp test-elf
python3 hulpmiddelen/Uitvoeren_opdracht.py --desktop --network
```

`hulpmiddelen/시언어이름분석.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`hulpmiddelen/*이름반영.py`는 wijzigen_WAARDE 전 bron_structuur·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 opnieuw_proberen_WAARDE 적용하여 대응표를 덮어쓰지 않는다.

## C communicatie 구조체와 Python fout

C 통신에서 `갈래`는 ADRES 체계를 구분하고 `poortnummer`는 port, `ADRES_WAARDE`은
IPv4 주소의 32비트 값을 나타낸다. `datagram_protocol`은 앞서 설명한 datagram(電文)과
contractwaarde(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | Nederlands 직접 implementatie |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 mesh_Gezin / datagramsocket / datagram_protocol |
| struct pk_sockaddr_in | struct mesh_socket_ADRES |
| sin_family / sin_port | ADRES_Gezin / poortnummer |
| sin_addr.s_addr | internetadres.ADRES_WAARDE |
| OSError / fout.args[0] | systeemfout / fout.INDEX |

Nederlands 구조체는 `#define` 치환이나 veldwaarde 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 kernel_WAARDE SVC에서 byte_WAARDE 복사로
검사한다. `maken_eindpunt`·`e_mailen_datagram_gegevens`와 bestand 함수는 statisch_WAARDE 라이브러리에
werkelijk_gegevens Nederlands 이름의 FUNCTIE_WAARDE 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
Vorige_item 코드에서 Nederlands communicatie 함수에 pk_sockaddr*를 전달했다면 Nederlands 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `systeemfout`는 OSError의 Nederlands 하위 클래스이며 연결부에서
fout 번호를 보존하여 변환한다. 일반 Python 문법과 extern_WAARDE 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 clip

`실행할일`은 수행할 내용을, `Uitvoeren`는 그 수행을 나타낸다.
`동작받이`는 동작이 발생했다는 알림을 받는 역할, `Actie_kennisgeving`은 전달되는 사건이다.
`knop`는 눌러 동작시키는 조작부, `Etiket`는 LEESMIJ_eb81d7d9 글의 plaatsingsindex,
`tekstveld`은 글을 적는 plaatsingsindex, `achtergrondwerker`은 이어지는 Uitvoeren_opdracht 흐름을 뜻한다.
`Uitvoeren_opdracht(實行)`·`Actie(動作)`의 기존 뜻과 `받다`·`알리다`·`thread_WAARDE`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 처음 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 hulpmiddelen/bron_beoordeling.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 hash_Bestand,
ASCII 파일명과 Python의 영어 aangifte 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/자바도구/기계어미리번역.java`로 전환했다. `compiler/기계어미리번역.py`는 호환 진입점이다.
`compiler/arm64.py`는 Vorige_item 경로와 `ARM64(...).generate(...)` 호출을 이어 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK 보조 hulpmiddelen, Linux versie_WAARDE 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
예약어 외 100% 한국어라고 판정하지 않는다.
`hulpmiddelen/명명검사.py --C_Taal`는 Actief ARM64 소스의 aangifte, C 의미 Analyseren_WAARDE,
x86 Java 커널과 공용 번역기의 Eigen aangifte, Java 예제 전체 id_WAARDE,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## actueel_item 기능을 기준으로 보완한 Naam

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 Nederlands 이름을 달리 정한다.
bestand 이름은 주된 기능을 나타내고, FUNCTIE_WAARDE 이름은 행동을, variabele_WAARDE 이름은 담는 자료를 나타낸다.
예약어, 표준 API 및 extern_WAARDE Verbinden 규약은 따로 기록한다.

| Vorige_item Naam | 적용한 Naam | actueel_item 기능 |
|---|---|---|
| `arm64.py`의 implementatie | `compiler/자바도구/기계어미리번역.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 VERTALEN_bron |
| `ARM64`, `generate` | `machine_CODE_compiler`, `genereren` | VERTALEN_bron 상태를 담는 객체와 C broncode genereren 행동 |
| `prototype`, `method` | `함수원형`, `methode_hoofdtekst` | 함수의 opmaak_WAARDE 선언과 werkelijk_gegevens opdracht broncode |
| `profile`, `heap_words` | `uitvoerbewerking_doel`, `heap_Aantal_woorden` | kernel_WAARDE·gebruikersruimte 구분과 toewijzen_Opslag Geheugen_WAARDE 공간의 machine 낱말 nummer |
| `pc`, `op` | `opdracht_functie`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 INDEX |
| `x`, `y`, `w`, `h` | `x_coördinaat`, `Y_coördinaat`, `영역너비`, `regio_hoogte` | extern_WAARDE_28edcfa1 화면의 위치와 직사각형 Grootte |
| `p`, `n`, `i`, `j` | `gegevens_functie`, `WAARDE`, `순번`, `안쪽순번` | extern_WAARDE_28edcfa1 scherm gegevens·cijfer_WAARDE·sprint_WAARDE plaatsingsindex; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `AOT_Geheugen_ZOEKEN`, `커널쌓임공간끝` | machine Verbinden 규약을 유지하면서 Eigen 소스에서 사용하는 Naam |
| `앞캐리지` | `앞줄복귀` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[공용번역기이름대응.tsv](공용번역기이름대응.tsv)에 compiler_hulpmiddel 참조의 werkelijk_gegevens wijzigen_WAARDE 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[Standard_naam_Bewijs.json](Standard_naam_Bewijs.json)에 기록한다.
`C_compiler/compiler_hulpmiddel.c`는 TinyCC extern_WAARDE 원문을 포함하는 Verbinden 파일로 Eigen 선언이 없어서
C Eigen aangifte 분석에서는 제외한다. werkelijk_gegevens kernel_WAARDE 빌드에서는 계속 컴파일한다.

### 말의 뿌리와 새로운 복합 Naam

`Geheugen_WAARDE(記憶)`과 `ZOEKEN_INDEX(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 order_WAARDE 있는 항목을 찾아 지정하는 기능에 적용한다.
woordenlijst 근거는 국립국어원 한국어기초사전의
[Geheugen_WAARDE](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[ZOEKEN_INDEX](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`stapelgeheugen`, `push_WAARDE`, `POP_WAARDE`는 자료를 포개고 마지막 자료부터 꺼내는 Uitvoeren_opdracht 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`미리번역`은 Uitvoeren_opdracht 전에 번역한다는 기능을 직접 나타낸다.
`machine_Word`은 처리기의 gegevens 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `machine`를 붙였다.
`기계어미리번역`, `heap_Aantal_woorden` 같은 복합 이름은 actueel_item 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 처음 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 gebruik_WAARDE 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 gegevenstype·MATRIX_WAARDE·FUNCTIE_WAARDE·lokaal_scope variabele_WAARDE·branch 이름도 한국어로 바꾼다.
직접 한글 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 Nederlands 이름을
표준 C 범용 문자 표기로 출력한다. werkelijk_gegevens ARM64 빌드는 Clang으로 읽을 nummer 있는 한글 원문을 사용한다.
tekenreeks_WAARDE, C 표준 FUNCTIE_WAARDE, `java_entry` 같은 공개 Verbinden 이름은 바꾸지 않는다.

셸의 사용법·문법 fout·bestand 및 Geheugen_WAARDE ADRES_regio 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 tests·bestand transfer_WAARDE 도구가 읽는 markering_WAARDE,
명령행 옵션과 기존 instructie_WAARDE, JVM les_WAARDE Naam·bestand opmaak_WAARDE·mobiel_WAARDE 이름은 호환 표기로 남는다.
x86 VGA 문자 화면은 한글을 표시하지 못하므로 Nederlands 문구는 UTF-8 직렬 단말에서 확인한다.
