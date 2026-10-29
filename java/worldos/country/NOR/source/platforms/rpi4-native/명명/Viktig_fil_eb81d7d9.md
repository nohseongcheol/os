# eget 커널과 번역기의 norsk Navn

대상은 `platforms/rpi4-native`의 eget Java kjerne_VERDI, bruker JVM, C maskin Koble_til,
TCP/UDP·FTP, C kompilator_verktøy 이식부, MicroPython 이식부, bygg_System·Utfør_kommando·시험 도구다.
`golang/worldos/Country_VERDI/KOR/KILDE`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 eget 선언도 명명 검사에 포함한다.
Linux 실행판의 vert Verktøy, OpenJDK 보조 Verktøy 및 ekstern_VERDI distribusjon_VERDI kilde_tre 전체를
한국어로 prøve_på_nytt_VERDI 작성했다는 뜻은 아니다.

## 명명 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `Fil_håndtak`, `node_portnummer`, `heap_lager`, `tastatur`.
- 함수는 행위를 나타낸다: `Les`, `Skriv`, `Åpne`, `Lukk`, `netto_BIND`, `kjøre_app`.
- TCP의 이어진 byte_VERDI 흐름과 UDP의 grense_VERDI 있는 자료를 `kontakt`와 `datagram_Kanal`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `lengde_VERDI`, `data_plassere`, `Oppslag_INDEKS`, `반환값`으로 풀어 쓴다.
  순번·임시 산술값처럼 여러 역할에 재사용되는 변수는 `순번`, `첫째값`, `SEKUND_VERDI`으로 구별한다.
- 이름이 같아도 ekstern_VERDI 구조체의 필드와 eget 변수는 별도로 분석한다.

`Kanal_oppføring(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 통신 연결에
적용했다. `port_VERDI(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [Kanal_oppføring](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[port_VERDI](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`datagram(電文)`은 전보에 담는 글이라는 기존 통신 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 datagram](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`strøm_VERDI`, `tråd_VERDI`, `쌓임`은 우리말의 움직임·이어짐·쌓이는 모양을 빌린 표현이다.
`inndataflyt`, `arbeider`, `stakk_lager` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 ordliste 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 OVERSETT_kilde·국어사 datagram 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 Navn | 이유 |
|---|---|---|
| TCP Socket | kontakt | 상대와 연결되어 ordre_VERDI 있는 바이트를 주고받음 |
| ServerSocket | motta_port | 새 연결이 들어오는 접점 |
| DatagramSocket | datagram_Kanal | 각 자료의 경계를 보존하는 통신 |
| InputStream / OutputStream | inndataflyt / utdataflyt | 들어오고 나가는 바이트의 ordre_VERDI |
| heap / stack | heap_lager / stakk_lager | tildele_lager 방식과 쌓고 꺼내는 구조 |
| thread / keyboard | arbeider / tastatur | 이어지는 실행과 글쇠의 MATRISE_VERDI |
| exception / timeout | unntak / vent_TIMEOUT_unntak | informasjonssystemer_normal 처리에서 벗어남과 그 구체적 이유 |

## 경로와 대응표

| 구현 | norsk Sti |
|---|---|
| kjerne_VERDI·Shell·Fil lag_VERDI | `KILDE/*.java` |
| bruker JVM | `bruker/자바/자바가상기계.java` |
| ARM64 maskin Koble_til | `maskin/*.c`, `부팅/` |
| TCP·UDP·FTP | `nettverk_stakk/nettverk_stakk.c`, `nettverk_stakk/filoverføring.c` |
| C kompilator_verktøy 이식 | `C_kompilator/` |
| MicroPython 이식 | `PYTHON_bro/` |
| bygg_System·Utfør_kommando·시험 | `Verktøy/`, `åpne_oppføring.mk` |
| Java bruker API | `한국어자바/norsk/eget/` |

[filnavn_tildeling.tsv](filnavn_tildeling.tsv), [자바이름대응.tsv](자바이름대응.tsv),
[C_navn_tildeling.tsv](C_navn_tildeling.tsv), [PYTHON_navn_tildeling.tsv](PYTHON_navn_tildeling.tsv)에
Forrige_vare 이름과 바뀐 이름이 있다. C/Java 대응표의 Fil·위치는 이행 당시 기준이다.
Sti 이동은 Fil 대응표를 함께 본다. 기존 `tools/*.py`는 norsk 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 SD Navn

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
betalt_vare 다섯 Java 예제는 `Kjør_2()`·`실행인수`·norsk skjermbilde/tråd_VERDI API를 사용해
예약어·리터럴 외의 식별자를 한국어로 작성한다. skjermbilde/가닥은 표준 객체를
감싸지 않고 eget JVM에 직접 구현했다. 자세한 계약은 [norsk Java API](../한국어자바/Viktig_fil_eb81d7d9.md)를 본다.

표준 javac는 streng_VERDI 리터럴에 `java.lang.String`, streng_VERDI 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 norsk 소스에서도 바이트코드에 남을 nummer 있다.
기존 표준 class를 실행하는 JVM의 tildeling_VERDI streng_VERDI, 아직 표준 라이브러리를 쓰는
통신·Fil 연결부까지 모두 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
서술자·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 FUNKSJON_VERDI·heltall_Type·POSIX ABI, CPU register_VERDI Navn, 어셈블리 Kommando, 링커 절 Navn,
TinyCC·lwIP·MicroPython이 요구하는 Innstillinger 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
eget C 함수의 kilde_tre 이름은 한국어이며, [기계연결이름.h](기계연결이름.h)가
기존 AOT·어셈블리·SDK에 공개한 maskin 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 modul_VERDI attributtverdi, 명령행 옵션과 JSON 키도
ekstern_VERDI 계약이다. `build/`, distribusjon_VERDI 바이너리 이름과 `/sdk`는 기존 Utfør_kommando 경로를 유지한다.
ekstern_VERDI 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Verktøy/명명검사.py
make bygg_System
make 시험
make test-examples test-ftp test-elf
python3 Verktøy/Utfør_kommando.py --desktop --network
```

`Verktøy/시언어이름분석.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`Verktøy/*이름반영.py`는 endre_VERDI 전 kilde_tre·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 prøve_på_nytt_VERDI 적용하여 대응표를 덮어쓰지 않는다.

## C 통신 구조체와 Python feil

C 통신에서 `갈래`는 e_post 체계를 구분하고 `portnummer`는 port, `e_post_VERDI`은
IPv4 주소의 32비트 값을 나타낸다. `datagram_protokoll`은 앞서 설명한 datagram(電文)과
kontraktverdi(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | norsk 직접 구현 |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 sky_serie / datagramsocket / datagram_protokoll |
| struct pk_sockaddr_in | struct sky_socket_e_post |
| sin_family / sin_port | e_post_serie / portnummer |
| sin_addr.s_addr | Internett_adresse.e_post_VERDI |
| OSError / feil.args[0] | systemfeil / feil.INDEKS |

norsk 구조체는 `#define` 치환이나 feltverdi 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 kjerne_VERDI SVC에서 byte_VERDI 복사로
검사한다. `åpne_deltaker`·`sende_datagram_data`와 Fil 함수는 statisk_VERDI 라이브러리에
faktisk_data norsk 이름의 FUNKSJON_VERDI 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
Forrige_vare 코드에서 norsk 통신 함수에 pk_sockaddr*를 전달했다면 norsk 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `systemfeil`는 OSError의 norsk 하위 클래스이며 연결부에서
feil 번호를 보존하여 변환한다. 일반 Python 문법과 ekstern_VERDI 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 klippe

`실행할일`은 수행할 내용을, `Kjør`는 그 수행을 나타낸다.
`동작받이`는 동작이 발생했다는 알림을 받는 역할, `Gjøremål_notice`은 전달되는 사건이다.
`Knapp`는 눌러 동작시키는 조작부, `Etikett`는 Viktig_fil_eb81d7d9 글의 posisjonsindeks,
`tekstfelt`은 글을 적는 posisjonsindeks, `arbeider`은 이어지는 Utfør_kommando 흐름을 뜻한다.
`Utfør_kommando(實行)`·`Handling(動作)`의 기존 뜻과 `받다`·`알리다`·`tråd_VERDI`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 처음 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 Verktøy/kilde_anmeldelse.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 hash_Fil,
ASCII 파일명과 Python의 영어 erklæring 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/자바도구/기계어미리번역.java`로 전환했다. `compiler/기계어미리번역.py`는 호환 진입점이다.
`compiler/arm64.py`는 Forrige_vare 경로와 `ARM64(...).generate(...)` 호출을 이어 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK 보조 Verktøy, Linux versjon_VERDI 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
예약어 외 100% 한국어라고 판정하지 않는다.
`Verktøy/명명검사.py --C_Språk`는 Aktiv ARM64 소스의 erklæring, C 의미 Analyser_VERDI,
x86 Java 커널과 공용 번역기의 eget erklæring, Java 예제 전체 identifikator_VERDI,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## betalt_vare 기능을 기준으로 보완한 Navn

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 norsk 이름을 달리 정한다.
Fil 이름은 주된 기능을 나타내고, FUNKSJON_VERDI 이름은 행동을, variabel_VERDI 이름은 담는 자료를 나타낸다.
예약어, 표준 API 및 ekstern_VERDI Koble_til 규약은 따로 기록한다.

| Forrige_vare Navn | 적용한 Navn | betalt_vare 기능 |
|---|---|---|
| `arm64.py`의 구현 | `compiler/자바도구/기계어미리번역.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 OVERSETT_kilde |
| `ARM64`, `generate` | `maskin_KODE_kompilator`, `generere` | OVERSETT_kilde 상태를 담는 객체와 C KILDE generere 행동 |
| `prototype`, `method` | `함수원형`, `metode_brødtekst` | 함수의 format_VERDI 선언과 faktisk_data Kommando KILDE |
| `profile`, `heap_words` | `kjøring_mål`, `heap_ord_ANTALL` | kjerne_VERDI·bruker 구분과 tildele_lager Minne_VERDI 공간의 maskin 낱말 nummer |
| `pc`, `op` | `kommando_plassere`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 INDEKS |
| `x`, `y`, `w`, `h` | `x_koordinat`, `Y_koordinat`, `영역너비`, `영역높이` | ekstern_VERDI_28edcfa1 화면의 위치와 직사각형 Størrelse |
| `p`, `n`, `i`, `j` | `data_plassere`, `VERDI`, `순번`, `안쪽순번` | ekstern_VERDI_28edcfa1 skjermbilde data·siffer_VERDI·sprint_VERDI posisjonsindeks; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `applikasjonsobjekttre_Minne_Oppslag`, `커널쌓임공간끝` | maskin Koble_til 규약을 유지하면서 eget 소스에서 사용하는 Navn |
| `앞캐리지` | `앞줄복귀` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[공용번역기이름대응.tsv](공용번역기이름대응.tsv)에 kompilator_verktøy 참조의 faktisk_data endre_VERDI 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[Standard_navn_Bevis.json](Standard_navn_Bevis.json)에 기록한다.
`C_kompilator/kompilator_verktøy.c`는 TinyCC ekstern_VERDI 원문을 포함하는 Koble_til 파일로 eget 선언이 없어서
C eget erklæring 분석에서는 제외한다. faktisk_data kjerne_VERDI 빌드에서는 계속 컴파일한다.

### 말의 뿌리와 새로운 복합 Navn

`Minne_VERDI(記憶)`과 `Oppslag_INDEKS(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 ordre_VERDI 있는 항목을 찾아 지정하는 기능에 적용한다.
ordliste 근거는 국립국어원 한국어기초사전의
[Minne_VERDI](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[Oppslag_INDEKS](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`stakk_lager`, `쌓기`, `POP_VERDI`는 자료를 포개고 마지막 자료부터 꺼내는 Utfør_kommando 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`미리번역`은 Utfør_kommando 전에 번역한다는 기능을 직접 나타낸다.
`maskin_ord`은 처리기의 data 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `maskin`를 붙였다.
`기계어미리번역`, `heap_ord_ANTALL` 같은 복합 이름은 betalt_vare 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 처음 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 bruk_VERDI 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 datatype·MATRISE_VERDI·FUNKSJON_VERDI·lokal_Omfang variabel_VERDI·gren 이름도 한국어로 바꾼다.
직접 한글 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 norsk 이름을
표준 C 범용 문자 표기로 출력한다. faktisk_data ARM64 빌드는 Clang으로 읽을 nummer 있는 한글 원문을 사용한다.
streng_VERDI, C 표준 FUNKSJON_VERDI, `java_entry` 같은 공개 Koble_til 이름은 바꾸지 않는다.

셸의 사용법·문법 feil·Fil 및 Minne_VERDI e_post_område 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 시험·Fil overføre_VERDI 도구가 읽는 tusj_VERDI,
명령행 옵션과 기존 명령어, JVM time_VERDI Navn·Fil format_VERDI·enhet_VERDI 이름은 호환 표기로 남는다.
x86 VGA 문자 화면은 한글을 표시하지 못하므로 norsk 문구는 UTF-8 직렬 단말에서 확인한다.
