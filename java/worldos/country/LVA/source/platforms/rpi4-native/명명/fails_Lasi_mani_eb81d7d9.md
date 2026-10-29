# savs 커널과 번역기의 Latviešu Nosaukums

대상은 `platforms/rpi4-native`의 savs Java kodols_VALUE, lietotājs JVM, C mašīna Savienoties,
TCP/UDP·FTP, C kompilators_rīks 이식부, MicroPython 이식부, būvējums_sistēma·Izpildīt_komanda·시험 도구다.
`golang/worldos/Kantri_VALUE/KOR/AVOTS`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 savs 선언도 명명 검사에 포함한다.
Linux 실행판의 viesot Rīki, OpenJDK 보조 Rīki 및 ārējs_VALUE sadale_VALUE avots_koks 전체를
한국어로 mēģināt_vēlreiz_VALUE 작성했다는 뜻은 아니다.

## 명명 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `Fails_turis`, `vienranga_porta_numurs`, `kaudze_Krātuve`, `tastatūra`.
- 함수는 행위를 나타낸다: `Lasīt`, `Rakstīt`, `Atvērt`, `Aizvērt`, `NET_BIND`, `virkne_programma`.
- TCP의 이어진 byte_VALUE 흐름과 UDP의 경계 있는 자료를 `paziņa`와 `datogramma_Kanāls`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `길이`, `dati_amats`, `LOOKUP_INDEX`, `반환값`으로 풀어 쓴다.
  순번·임시 산술값처럼 여러 역할에 재사용되는 변수는 `순번`, `첫째값`, `SECOND_VALUE`으로 구별한다.
- 이름이 같아도 ārējs_VALUE 구조체의 필드와 savs 변수는 별도로 분석한다.

`Kanāls_ievade(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 통신 연결에
적용했다. `ports_VALUE(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [Kanāls_ievade](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[ports_VALUE](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`datogramma(電文)`은 전보에 담는 글이라는 기존 통신 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 datogramma](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`Stream_VALUE`, `saruna_VALUE`, `쌓임`은 우리말의 움직임·이어짐·쌓이는 모양을 빌린 표현이다.
`ievades_straume`, `nodarbinātais`, `kopa_Krātuve` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 vārdnīca 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 translēt_avots·국어사 datogramma 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 Nosaukums | 이유 |
|---|---|---|
| TCP Socket | paziņa | 상대와 연결되어 secība_VALUE 있는 바이트를 주고받음 |
| ServerSocket | saņemt_ports | 새 연결이 들어오는 접점 |
| DatagramSocket | datogramma_Kanāls | 각 자료의 경계를 보존하는 통신 |
| InputStream / OutputStream | ievades_straume / ražojums_Stream | 들어오고 나가는 바이트의 secība_VALUE |
| heap / stack | kaudze_Krātuve / kopa_Krātuve | piešķirt_Krātuve 방식과 쌓고 꺼내는 구조 |
| thread / keyboard | nodarbinātais / tastatūra | 이어지는 실행과 글쇠의 ARRAY_VALUE |
| exception / timeout | izņēmums / pagaidi_NOILGUMS_izņēmums | 정상 처리에서 벗어남과 그 구체적 이유 |

## 경로와 대응표

| 구현 | Latviešu CEĻŠ |
|---|---|
| kodols_VALUE·čaula·Fails slānis_VALUE | `AVOTS/*.java` |
| lietotājs JVM | `lietotājs/자바/자바가상기계.java` |
| ARM64 mašīna Savienoties | `mašīna/*.c`, `부팅/` |
| TCP·UDP·FTP | `tīkls_kopa/tīkls_kopa.c`, `tīkls_kopa/faila_pārsūtīšana.c` |
| C kompilators_rīks 이식 | `C_kompilators/` |
| MicroPython 이식 | `PYTHON_tilts/` |
| būvējums_sistēma·Izpildīt_komanda·시험 | `Rīki/`, `atvērt_ievade.mk` |
| Java lietotājs API | `한국어자바/Latviešu/savs/` |

[faila_nosaukums_kartēšana.tsv](faila_nosaukums_kartēšana.tsv), [자바이름대응.tsv](자바이름대응.tsv),
[C_nosaukums_kartēšana.tsv](C_nosaukums_kartēšana.tsv), [PYTHON_nosaukums_kartēšana.tsv](PYTHON_nosaukums_kartēšana.tsv)에
이전 이름과 바뀐 이름이 있다. C/Java 대응표의 Fails·위치는 이행 당시 기준이다.
CEĻŠ 이동은 Fails 대응표를 함께 본다. 기존 `tools/*.py`는 Latviešu 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 SD Nosaukums

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
pašreizējais_krājums 다섯 Java 예제는 `Palaist()`·`실행인수`·Latviešu 화면/saruna_VALUE API를 사용해
예약어·리터럴 외의 식별자를 한국어로 작성한다. 화면/가닥은 표준 객체를
감싸지 않고 savs JVM에 직접 구현했다. 자세한 계약은 [Latviešu Java API](../한국어자바/fails_Lasi_mani_eb81d7d9.md)를 본다.

표준 javac는 virkne_VALUE 리터럴에 `java.lang.String`, virkne_VALUE 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 Latviešu 소스에서도 바이트코드에 남을 numurs 있다.
기존 표준 class를 실행하는 JVM의 kartēšana_VALUE virkne_VALUE, 아직 표준 라이브러리를 쓰는
통신·Fails 연결부까지 모두 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
서술자·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 FUNCTION_VALUE·vesels_skaitlis_TYPE·POSIX ABI, CPU reģistrs_VALUE Nosaukums, 어셈블리 Komanda, 링커 절 Nosaukums,
TinyCC·lwIP·MicroPython이 요구하는 Uzstādījumi 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
savs C 함수의 avots_koks 이름은 한국어이며, [기계연결이름.h](기계연결이름.h)가
기존 AOT·어셈블리·SDK에 공개한 mašīna 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 modulis_VALUE atribūts_VALUE, 명령행 옵션과 JSON 키도
ārējs_VALUE 계약이다. `build/`, sadale_VALUE 바이너리 이름과 `/sdk`는 기존 Izpildīt_komanda 경로를 유지한다.
ārējs_VALUE 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Rīki/명명검사.py
make būvējums_sistēma
make 시험
make test-examples test-ftp test-elf
python3 Rīki/Izpildīt_komanda.py --desktop --network
```

`Rīki/시언어이름분석.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`Rīki/*이름반영.py`는 mainīt_VALUE 전 avots_koks·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 mēģināt_vēlreiz_VALUE 적용하여 대응표를 덮어쓰지 않는다.

## C 통신 구조체와 Python Kļūda

C 통신에서 `갈래`는 adrese 체계를 구분하고 `porta_numurs`는 port, `adrese_VALUE`은
IPv4 주소의 32비트 값을 나타낸다. `datogramma_protokols`은 앞서 설명한 datogramma(電文)과
līguma_vērtība(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | Latviešu 직접 구현 |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 mākonis_saime / datogrammas_ligzda / datogramma_protokols |
| struct pk_sockaddr_in | struct 인터넷통신주소 |
| sin_family / sin_port | adrese_saime / porta_numurs |
| sin_addr.s_addr | interneta_adrese.adrese_VALUE |
| OSError / Kļūda.args[0] | sistēma_kļūda / Kļūda.INDEX |

Latviešu 구조체는 `#define` 치환이나 lauka_vērtība 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 kodols_VALUE SVC에서 byte_VALUE 복사로
검사한다. `atvērt_dalībnieks`·`sūtīt_datogramma_dati`와 Fails 함수는 정적 라이브러리에
faktisks_dati Latviešu 이름의 FUNCTION_VALUE 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
이전 코드에서 Latviešu 통신 함수에 pk_sockaddr*를 전달했다면 Latviešu 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `sistēma_kļūda`는 OSError의 Latviešu 하위 클래스이며 연결부에서
Kļūda 번호를 보존하여 변환한다. 일반 Python 문법과 ārējs_VALUE 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 klips

`실행할일`은 수행할 내용을, `Izpildīt`는 그 수행을 나타낸다.
`동작받이`는 동작이 발생했다는 알림을 받는 역할, `darbība_informēšana`은 전달되는 사건이다.
`Pogas`는 눌러 동작시키는 조작부, `Etiķete`는 fails_Lasi_mani_eb81d7d9 글의 pozīcijas_indekss,
`teksta_lauks`은 글을 적는 pozīcijas_indekss, `nodarbinātais`은 이어지는 Izpildīt_komanda 흐름을 뜻한다.
`Izpildīt_komanda(實行)`·`Darbība(動作)`의 기존 뜻과 `받다`·`알리다`·`saruna_VALUE`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 처음 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 Rīki/avots_atsauksme.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 jaukšana_Fails,
ASCII 파일명과 Python의 영어 deklarācija 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/자바도구/기계어미리번역.java`로 전환했다. `compiler/기계어미리번역.py`는 호환 진입점이다.
`compiler/arm64.py`는 이전 경로와 `ARM64(...).generate(...)` 호출을 이어 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK 보조 Rīki, Linux versija_VALUE 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
예약어 외 100% 한국어라고 판정하지 않는다.
`Rīki/명명검사.py --C_Valodas`는 Aktīvs ARM64 소스의 deklarācija, C 의미 analīze_VALUE,
x86 Java 커널과 공용 번역기의 savs deklarācija, Java 예제 전체 identifikators_VALUE,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## pašreizējais_krājums 기능을 기준으로 보완한 Nosaukums

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 Latviešu 이름을 달리 정한다.
Fails 이름은 주된 기능을 나타내고, FUNCTION_VALUE 이름은 행동을, mainīgais_VALUE 이름은 담는 자료를 나타낸다.
예약어, 표준 API 및 ārējs_VALUE Savienoties 규약은 따로 기록한다.

| 이전 Nosaukums | 적용한 Nosaukums | pašreizējais_krājums 기능 |
|---|---|---|
| `arm64.py`의 구현 | `compiler/자바도구/기계어미리번역.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 translēt_avots |
| `ARM64`, `generate` | `mašīna_CODE_kompilators`, `ģenerēt` | translēt_avots 상태를 담는 객체와 C AVOTS ģenerēt 행동 |
| `prototype`, `method` | `함수원형`, `metode_pamatteksts` | 함수의 formāts_VALUE 선언과 faktisks_dati Komanda AVOTS |
| `profile`, `heap_words` | `실행대상`, `kaudze_Word_COUNT` | kodols_VALUE·lietotājs 구분과 piešķirt_Krātuve atmiņa_VALUE 공간의 mašīna 낱말 numurs |
| `pc`, `op` | `komanda_amats`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 INDEX |
| `x`, `y`, `w`, `h` | `x_koordināta`, `세로좌표`, `영역너비`, `영역높이` | attāls_VALUE 화면의 위치와 직사각형 Izmērs |
| `p`, `n`, `i`, `j` | `dati_amats`, `VALUE`, `순번`, `안쪽순번` | attāls_VALUE 화면 dati·cipars_VALUE·sprints_VALUE pozīcijas_indekss; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `AOT_atmiņa_LOOKUP`, `커널쌓임공간끝` | mašīna Savienoties 규약을 유지하면서 savs 소스에서 사용하는 Nosaukums |
| `앞캐리지` | `앞줄복귀` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[공용번역기이름대응.tsv](공용번역기이름대응.tsv)에 kompilators_rīks 참조의 faktisks_dati mainīt_VALUE 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[규격이름근거.json](규격이름근거.json)에 기록한다.
`C_kompilators/kompilators_rīks.c`는 TinyCC ārējs_VALUE 원문을 포함하는 Savienoties 파일로 savs 선언이 없어서
C savs deklarācija 분석에서는 제외한다. faktisks_dati kodols_VALUE 빌드에서는 계속 컴파일한다.

### 말의 뿌리와 새로운 복합 Nosaukums

`atmiņa_VALUE(記憶)`과 `LOOKUP_INDEX(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 secība_VALUE 있는 항목을 찾아 지정하는 기능에 적용한다.
vārdnīca 근거는 국립국어원 한국어기초사전의
[atmiņa_VALUE](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[LOOKUP_INDEX](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`kopa_Krātuve`, `stumšana_VALUE`, `POP_VALUE`는 자료를 포개고 마지막 자료부터 꺼내는 Izpildīt_komanda 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`미리번역`은 Izpildīt_komanda 전에 번역한다는 기능을 직접 나타낸다.
`mašīna_Word`은 처리기의 dati 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `mašīna`를 붙였다.
`기계어미리번역`, `kaudze_Word_COUNT` 같은 복합 이름은 pašreizējais_krājums 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 처음 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 lietot_VALUE 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 datu_tips·ARRAY_VALUE·FUNCTION_VALUE·vietējs_Tvērums mainīgais_VALUE·zars 이름도 한국어로 바꾼다.
직접 한글 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 Latviešu 이름을
표준 C 범용 문자 표기로 출력한다. faktisks_dati ARM64 빌드는 Clang으로 읽을 numurs 있는 한글 원문을 사용한다.
virkne_VALUE, C 표준 FUNCTION_VALUE, `java_entry` 같은 공개 Savienoties 이름은 바꾸지 않는다.

셸의 사용법·문법 Kļūda·Fails 및 atmiņa_VALUE adrese_reģions 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 시험·Fails nodot_VALUE_630ba093 도구가 읽는 marķieris_VALUE,
명령행 옵션과 기존 명령어, JVM klase_VALUE Nosaukums·Fails formāts_VALUE·ierīce_VALUE 이름은 호환 표기로 남는다.
x86 VGA 문자 화면은 한글을 표시하지 못하므로 Latviešu 문구는 UTF-8 직렬 단말에서 확인한다.
