# eget 커널과 번역기의 Svenska Namn

대상은 `platforms/rpi4-native`의 eget Java kärna_värde, användarutrymme JVM, C dator Anslut,
TCP/UDP·FTP, C kompilerare_verktyg 이식부, MicroPython 이식부, version_System·köra_kommando·tester 도구다.
`golang/worldos/Country_värde/KOR/källfil`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 eget 선언도 명명 검사에 포함한다.
Linux 실행판의 värd verktyg, OpenJDK 보조 verktyg 및 extern_värde fördelning_värde källa_träd 전체를
한국어로 försöka_igen_värde 작성했다는 뜻은 아니다.

## 명명 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `filreferens`, `peer_portnummer`, `dynamiskt_minne`, `tangentbord`.
- 함수는 행위를 나타낸다: `Läs`, `Skriv`, `Öppna`, `Stäng`, `NET_BIND`, `köra_app`.
- TCP의 이어진 byte_värde 흐름과 UDP의 gräns_värde 있는 자료를 `kontakt`와 `datagram_Kanal`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `längd_värde`, `data_placera`, `LETAUPP_INDEX`, `반환값`으로 풀어 쓴다.
  순번·임시 산술값처럼 여러 역할에 재사용되는 변수는 `순번`, `첫째값`, `SEKUND_värde`으로 구별한다.
- 이름이 같아도 extern_värde 구조체의 필드와 eget 변수는 별도로 분석한다.

`Kanal_post(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 kommunikation 연결에
적용했다. `port_värde(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [Kanal_post](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[port_värde](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`datagram(電文)`은 전보에 담는 글이라는 기존 kommunikation 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 datagram](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`flöde_värde`, `tråd_värde`, `쌓임`은 우리말의 움직임·이어짐·쌓이는 모양을 빌린 표현이다.
`indataström`, `arbete`, `stackminne` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 ordlista 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 ÖVERSÄTT_källa·국어사 datagram 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 Namn | 이유 |
|---|---|---|
| TCP Socket | kontakt | 상대와 연결되어 order_värde 있는 바이트를 주고받음 |
| ServerSocket | få_port | 새 연결이 들어오는 접점 |
| DatagramSocket | datagram_Kanal | 각 자료의 경계를 보존하는 kommunikation |
| InputStream / OutputStream | indataström / utdataström | 들어오고 나가는 바이트의 order_värde |
| heap / stack | dynamiskt_minne / stackminne | allokera_minne 방식과 쌓고 꺼내는 arkitektur |
| thread / keyboard | arbete / tangentbord | 이어지는 실행과 글쇠의 MATRIS_värde |
| exception / timeout | fel_31f743d2 / vänta_TIMEOUT_fel | informationsteknik_normal 처리에서 벗어남과 그 구체적 이유 |

## 경로와 대응표

| implementation | Svenska sökväg_2 |
|---|---|
| kärna_värde·Shell·filnamn nivå_värde | `källfil/*.java` |
| användarutrymme JVM | `användarutrymme/자바/자바가상기계.java` |
| ARM64 dator Anslut | `dator/*.c`, `maskinstart/` |
| TCP·UDP·FTP | `nätverk_Stack/nätverk_Stack.c`, `nätverk_Stack/filöverföring.c` |
| C kompilerare_verktyg 이식 | `C_kompilerare/` |
| MicroPython 이식 | `PYTHON_brygga/` |
| version_System·köra_kommando·tester | `verktyg/`, `Skapa_post.mk` |
| Java användarutrymme API | `한국어자바/Svenska/eget/` |

[filnamn_mappning.tsv](filnamn_mappning.tsv), [자바이름대응.tsv](자바이름대응.tsv),
[C_namn_mappning.tsv](C_namn_mappning.tsv), [PYTHON_namn_mappning.tsv](PYTHON_namn_mappning.tsv)에
Föregående_objekt 이름과 바뀐 이름이 있다. C/Java 대응표의 filnamn·위치는 이행 당시 기준이다.
sökväg_2 이동은 filnamn 대응표를 함께 본다. 기존 `tools/*.py`는 Svenska 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 SD Namn

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
aktuellt_objekt 다섯 Java 예제는 `Kör()`·`실행인수`·Svenska skärmbild/tråd_värde API를 사용해
예약어·리터럴 외의 식별자를 한국어로 작성한다. skärmbild/가닥은 표준 객체를
감싸지 않고 eget JVM에 직접 구현했다. 자세한 계약은 [Svenska Java API](../한국어자바/VIKTIGT_eb81d7d9.md)를 본다.

표준 javac는 sträng_värde 리터럴에 `java.lang.String`, sträng_värde 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 Svenska 소스에서도 바이트코드에 남을 nummer 있다.
기존 표준 class를 실행하는 JVM의 mappning_värde sträng_värde, 아직 표준 라이브러리를 쓰는
kommunikation·filnamn 연결부까지 모두 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
서술자·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 FUNKTION_värde·heltal_Typ·POSIX ABI, CPU register Namn, 어셈블리 kommando, 링커 절 Namn,
TinyCC·lwIP·MicroPython이 요구하는 Inställningar 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
eget C 함수의 källa_träd 이름은 한국어이며, [기계연결이름.h](기계연결이름.h)가
기존 AOT·어셈블리·SDK에 공개한 dator 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 modul_värde attribut_värde, 명령행 옵션과 JSON 키도
extern_värde 계약이다. `build/`, fördelning_värde 바이너리 이름과 `/sdk`는 기존 köra_kommando 경로를 유지한다.
extern_värde 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 verktyg/명명검사.py
make version_System
make tester
make test-examples test-ftp test-elf
python3 verktyg/köra_kommando.py --desktop --network
```

`verktyg/시언어이름분석.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`verktyg/*이름반영.py`는 ändra_värde 전 källa_träd·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 försöka_igen_värde 적용하여 대응표를 덮어쓰지 않는다.

## C kommunikation 구조체와 Python fel

C 통신에서 `갈래`는 Adress 체계를 구분하고 `portnummer`는 port, `ADRESS_värde`은
IPv4 주소의 32비트 값을 나타낸다. `datagram_protokoll`은 앞서 설명한 datagram(電文)과
kontraktsvärde(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | Svenska 직접 implementation |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 nät_serie / datagramsocket / datagram_protokoll |
| struct pk_sockaddr_in | struct nät_socket_ADRESS |
| sin_family / sin_port | ADRESS_serie / portnummer |
| sin_addr.s_addr | Internetadress.ADRESS_värde |
| OSError / fel.args[0] | systemfel / fel.INDEX |

Svenska 구조체는 `#define` 치환이나 fältvärde 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 kärna_värde SVC에서 byte_värde 복사로
검사한다. `Skapa_deltagare`·`skicka_datagram_data`와 filnamn 함수는 statisk_värde 라이브러리에
verklig_data Svenska 이름의 FUNKTION_värde 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
Föregående_objekt 코드에서 Svenska kommunikation 함수에 pk_sockaddr*를 전달했다면 Svenska 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `systemfel`는 OSError의 Svenska 하위 클래스이며 연결부에서
fel 번호를 보존하여 변환한다. 일반 Python 문법과 extern_värde 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 klipp

`실행할일`은 수행할 내용을, `Starta`는 그 수행을 나타낸다.
`동작받이`는 동작이 발생했다는 알림을 받는 역할, `동작알림`은 전달되는 사건이다.
`knapp`는 눌러 동작시키는 조작부, `Etikett`는 VIKTIGT_eb81d7d9 글의 positionsindex,
`textfält`은 글을 적는 positionsindex, `arbete`은 이어지는 köra_kommando 흐름을 뜻한다.
`köra_kommando(實行)`·`Åtgärd(動作)`의 기존 뜻과 `받다`·`알리다`·`tråd_värde`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 처음 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 verktyg/källa_granska.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 hash_fil,
ASCII 파일명과 Python의 영어 deklaration 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/자바도구/기계어미리번역.java`로 전환했다. `compiler/기계어미리번역.py`는 호환 진입점이다.
`compiler/arm64.py`는 Föregående_objekt 경로와 `ARM64(...).generate(...)` 호출을 이어 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK 보조 verktyg, Linux version_värde 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
예약어 외 100% 한국어라고 판정하지 않는다.
`verktyg/명명검사.py --C_Språk`는 Aktiv ARM64 소스의 deklaration, C 의미 Analysera_värde,
x86 Java 커널과 공용 번역기의 eget deklaration, Java 예제 전체 identifierare_värde,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## aktuellt_objekt 기능을 기준으로 보완한 Namn

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 Svenska 이름을 달리 정한다.
filnamn 이름은 주된 기능을 나타내고, FUNKTION_värde 이름은 행동을, variabel_värde 이름은 담는 자료를 나타낸다.
예약어, 표준 API 및 extern_värde Anslut 규약은 따로 기록한다.

| Föregående_objekt Namn | 적용한 Namn | aktuellt_objekt 기능 |
|---|---|---|
| `arm64.py`의 implementation | `compiler/자바도구/기계어미리번역.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 ÖVERSÄTT_källa |
| `ARM64`, `generate` | `dator_KOD_kompilerare`, `generera` | ÖVERSÄTT_källa 상태를 담는 객체와 C källfil generera 행동 |
| `prototype`, `method` | `함수원형`, `metod_brödtext` | 함수의 format_värde 선언과 verklig_data kommando källfil |
| `profile`, `heap_words` | `körning_mål`, `heap_Ord_ANTAL` | kärna_värde·användarutrymme 구분과 allokera_minne Minne_värde 공간의 dator 낱말 nummer |
| `pc`, `op` | `kommando_placera`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 INDEX |
| `x`, `y`, `w`, `h` | `x_koordinat`, `Y_koordinat`, `영역너비`, `영역높이` | fjärr_värde 화면의 위치와 직사각형 Storlek |
| `p`, `n`, `i`, `j` | `data_placera`, `värde`, `순번`, `안쪽순번` | fjärr_värde skärmbild data·siffra_värde·sprint_värde positionsindex; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `AOT_Minne_LETAUPP`, `커널쌓임공간끝` | dator Anslut 규약을 유지하면서 eget 소스에서 사용하는 Namn |
| `앞캐리지` | `앞줄복귀` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[공용번역기이름대응.tsv](공용번역기이름대응.tsv)에 kompilerare_verktyg 참조의 verklig_data ändra_värde 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[Standard_namn_Bevis.json](Standard_namn_Bevis.json)에 기록한다.
`C_kompilerare/kompilerare_verktyg.c`는 TinyCC extern_värde 원문을 포함하는 Anslut 파일로 eget 선언이 없어서
C eget deklaration 분석에서는 제외한다. verklig_data kärna_värde 빌드에서는 계속 컴파일한다.

### 말의 뿌리와 새로운 복합 Namn

`Minne_värde(記憶)`과 `LETAUPP_INDEX(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 order_värde 있는 항목을 찾아 지정하는 기능에 적용한다.
ordlista 근거는 국립국어원 한국어기초사전의
[Minne_värde](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[LETAUPP_INDEX](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`stackminne`, `Koppla_värde`, `POP_värde`는 자료를 포개고 마지막 자료부터 꺼내는 köra_kommando 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`미리번역`은 köra_kommando 전에 번역한다는 기능을 직접 나타낸다.
`dator_Ord`은 처리기의 data 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `dator`를 붙였다.
`기계어미리번역`, `heap_Ord_ANTAL` 같은 복합 이름은 aktuellt_objekt 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 처음 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 använda_värde 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 datatyp·MATRIS_värde·FUNKTION_värde·lokal_scope variabel_värde·gren 이름도 한국어로 바꾼다.
직접 한글 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 Svenska 이름을
표준 C 범용 문자 표기로 출력한다. verklig_data ARM64 빌드는 Clang으로 읽을 nummer 있는 한글 원문을 사용한다.
sträng_värde, C 표준 FUNKTION_värde, `java_entry` 같은 공개 Anslut 이름은 바꾸지 않는다.

셸의 사용법·문법 fel·filnamn 및 Minne_värde ADRESS_område 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 tester·filnamn Överför_värde 도구가 읽는 markör_värde,
명령행 옵션과 기존 instruktion_värde, JVM Kurs_värde Namn·filnamn format_värde·enhet_värde 이름은 호환 표기로 남는다.
x86 VGA 문자 화면은 한글을 표시하지 못하므로 Svenska 문구는 UTF-8 직렬 단말에서 확인한다.
