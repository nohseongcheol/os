# eigin 커널과 번역기의 Íslenska Heiti

대상은 `platforms/rpi4-native`의 eigin Java kjarni_VALUE, notandi JVM, C vél Tengjast,
TCP/UDP·FTP, C 번역기 이식부, MicroPython 이식부, smíð_kerfi·keyra_skipun·시험 도구다.
`golang/worldos/나라/KOR/Uppruni`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 eigin 선언도 명명 검사에 포함한다.
Linux 실행판의 hýsa Verkfæri, OpenJDK 보조 Verkfæri 및 외부 dreifing_VALUE uppruni_tré 전체를
한국어로 다시 작성했다는 뜻은 아니다.

## 명명 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `skrá_hald`, `jafningi_tengisnúmer`, `동적기억공간`, `lyklaborð`.
- 함수는 행위를 나타낸다: `Lestur`, `Skrift`, `Opna`, `Loka`, `nettó_BIND`, `runa_forrit`.
- TCP의 이어진 bæti_VALUE 흐름과 UDP의 경계 있는 자료를 `tenging`와 `전문통로`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `lengd_VALUE`, `gögn_staða`, `LOOKUP_INDEX`, `반환값`으로 풀어 쓴다.
  순번·임시 산술값처럼 여러 역할에 재사용되는 변수는 `순번`, `첫째값`, `SECOND_VALUE`으로 구별한다.
- 이름이 같아도 외부 구조체의 필드와 eigin 변수는 별도로 분석한다.

`rás_færsla(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 통신 연결에
적용했다. `gátt_VALUE(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [rás_færsla](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[gátt_VALUE](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`전문(電文)`은 전보에 담는 글이라는 기존 통신 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 전문](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`Stream_VALUE`, `þráður_VALUE`, `쌓임`은 우리말의 움직임·이어짐·쌓이는 모양을 빌린 표현이다.
`입력흐름`, `starfskraftur`, `bunki_geymsla` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 orðabók 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 Þýða_uppruni·국어사 전문 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 Heiti | 이유 |
|---|---|---|
| TCP Socket | tenging | 상대와 연결되어 röð_VALUE 있는 바이트를 주고받음 |
| ServerSocket | 수신창구 | 새 연결이 들어오는 접점 |
| DatagramSocket | 전문통로 | 각 자료의 경계를 보존하는 통신 |
| InputStream / OutputStream | 입력흐름 / úttak_Stream | 들어오고 나가는 바이트의 röð_VALUE |
| heap / stack | 동적기억공간 / bunki_geymsla | úthluta_geymsla 방식과 쌓고 꺼내는 구조 |
| thread / keyboard | starfskraftur / lyklaborð | 이어지는 실행과 글쇠의 ARRAY_VALUE |
| exception / timeout | undantekning / Bíddu_TIMEOUT_undantekning | 정상 처리에서 벗어남과 그 구체적 이유 |

## 경로와 대응표

| 구현 | Íslenska SLÓÐ |
|---|---|
| kjarni_VALUE·skel·Skrá lag_VALUE | `Uppruni/*.java` |
| notandi JVM | `notandi/자바/자바가상기계.java` |
| ARM64 vél Tengjast | `vél/*.c`, `부팅/` |
| TCP·UDP·FTP | `Net_bunki/Net_bunki.c`, `Net_bunki/skrá_flytja.c` |
| C 번역기 이식 | `시언어번역기/` |
| MicroPython 이식 | `PYTHON_brú/` |
| smíð_kerfi·keyra_skipun·시험 | `Verkfæri/`, `stofna_færsla.mk` |
| Java notandi API | `한국어자바/Íslenska/eigin/` |

[skrá_heiti_vörpun.tsv](skrá_heiti_vörpun.tsv), [자바이름대응.tsv](자바이름대응.tsv),
[시언어이름대응.tsv](시언어이름대응.tsv), [PYTHON_heiti_vörpun.tsv](PYTHON_heiti_vörpun.tsv)에
이전 이름과 바뀐 이름이 있다. C/Java 대응표의 Skrá·위치는 이행 당시 기준이다.
SLÓÐ 이동은 Skrá 대응표를 함께 본다. 기존 `tools/*.py`는 Íslenska 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 SD Heiti

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
현재 다섯 Java 예제는 `Keyra_2()`·`실행인수`·Íslenska 화면/þráður_VALUE API를 사용해
예약어·리터럴 외의 식별자를 한국어로 작성한다. 화면/가닥은 표준 객체를
감싸지 않고 eigin JVM에 직접 구현했다. 자세한 계약은 [Íslenska Java API](../한국어자바/LESTUMIG_eb81d7d9.md)를 본다.

표준 javac는 strengur_VALUE 리터럴에 `java.lang.String`, strengur_VALUE 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 Íslenska 소스에서도 바이트코드에 남을 númer 있다.
기존 표준 class를 실행하는 JVM의 vörpun_VALUE strengur_VALUE, 아직 표준 라이브러리를 쓰는
통신·Skrá 연결부까지 모두 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
서술자·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 fall_VALUE·heiltala_TYPE·POSIX ABI, CPU skrá_VALUE Heiti, 어셈블리 Skipun, 링커 절 Heiti,
TinyCC·lwIP·MicroPython이 요구하는 Stillingar 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
eigin C 함수의 uppruni_tré 이름은 한국어이며, [기계연결이름.h](기계연결이름.h)가
기존 AOT·어셈블리·SDK에 공개한 vél 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 eining_VALUE_6d2d8bf4 eigind_VALUE, 명령행 옵션과 JSON 키도
외부 계약이다. `build/`, dreifing_VALUE 바이너리 이름과 `/sdk`는 기존 keyra_skipun 경로를 유지한다.
외부 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Verkfæri/명명검사.py
make smíð_kerfi
make 시험
make test-examples test-ftp test-elf
python3 Verkfæri/keyra_skipun.py --desktop --network
```

`Verkfæri/시언어이름분석.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`Verkfæri/*이름반영.py`는 breyta_VALUE_16f64fe4 전 uppruni_tré·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 다시 적용하여 대응표를 덮어쓰지 않는다.

## C 통신 구조체와 Python Villa

C 통신에서 `갈래`는 slóð 체계를 구분하고 `tengisnúmer`는 port, `slóð_VALUE`은
IPv4 주소의 32비트 값을 나타낸다. `전문전송규약`은 앞서 설명한 전문(電文)과
samningsvirði(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | Íslenska 직접 구현 |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 skýið_Fjölskylda / 전문통신 / 전문전송규약 |
| struct pk_sockaddr_in | struct 인터넷통신주소 |
| sin_family / sin_port | slóð_Fjölskylda / tengisnúmer |
| sin_addr.s_addr | veffang.slóð_VALUE |
| OSError / Villa.args[0] | kerfi_villa / Villa.INDEX |

Íslenska 구조체는 `#define` 치환이나 reitur_VALUE 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 kjarni_VALUE SVC에서 bæti_VALUE 복사로
검사한다. `stofna_endastöð`·`자료전문보내기`와 Skrá 함수는 fast_VALUE 라이브러리에
raun_gögn Íslenska 이름의 fall_VALUE 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
이전 코드에서 Íslenska 통신 함수에 pk_sockaddr*를 전달했다면 Íslenska 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `kerfi_villa`는 OSError의 Íslenska 하위 클래스이며 연결부에서
Villa 번호를 보존하여 변환한다. 일반 Python 문법과 외부 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 miðlaskrá

`실행할일`은 수행할 내용을, `Keyra`는 그 수행을 나타낸다.
`동작받이`는 동작이 발생했다는 알림을 받는 역할, `동작알림`은 전달되는 사건이다.
`hnappur`는 눌러 동작시키는 조작부, `Skýring`는 LESTUMIG_eb81d7d9 글의 staða_INDEX,
`SMS_reitur`은 글을 적는 staða_INDEX, `starfskraftur`은 이어지는 keyra_skipun 흐름을 뜻한다.
`keyra_skipun(實行)`·`Aðgerð(動作)`의 기존 뜻과 `받다`·`알리다`·`þráður_VALUE`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 처음 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 Verkfæri/uppruni_umsögn.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 tæting_skrá,
ASCII 파일명과 Python의 영어 skýrsla 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/자바도구/기계어미리번역.java`로 전환했다. `compiler/기계어미리번역.py`는 호환 진입점이다.
`compiler/arm64.py`는 이전 경로와 `ARM64(...).generate(...)` 호출을 이어 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK 보조 Verkfæri, Linux útgáfa_VALUE 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
예약어 외 100% 한국어라고 판정하지 않는다.
`Verkfæri/명명검사.py --시언어`는 Laus ARM64 소스의 skýrsla, C 의미 분석,
x86 Java 커널과 공용 번역기의 eigin skýrsla, Java 예제 전체 auðkenni_VALUE,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## 현재 기능을 기준으로 보완한 Heiti

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 Íslenska 이름을 달리 정한다.
Skrá 이름은 주된 기능을 나타내고, fall_VALUE 이름은 행동을, 변수 이름은 담는 자료를 나타낸다.
예약어, 표준 API 및 외부 Tengjast 규약은 따로 기록한다.

| 이전 Heiti | 적용한 Heiti | 현재 기능 |
|---|---|---|
| `arm64.py`의 구현 | `compiler/자바도구/기계어미리번역.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 Þýða_uppruni |
| `ARM64`, `generate` | `기계어번역기`, `skapa` | Þýða_uppruni 상태를 담는 객체와 C Uppruni skapa 행동 |
| `prototype`, `method` | `함수원형`, `aðferð_meginmál` | 함수의 snið_VALUE 선언과 raun_gögn Skipun Uppruni |
| `profile`, `heap_words` | `실행대상`, `동적기억낱말수` | kjarni_VALUE·notandi 구분과 úthluta_geymsla Minni_VALUE 공간의 vél 낱말 númer |
| `pc`, `op` | `skipun_staða`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 INDEX |
| `x`, `y`, `w`, `h` | `x_hnit`, `Y_hnit`, `영역너비`, `영역높이` | fjartengdur_VALUE 화면의 위치와 직사각형 Stærð |
| `p`, `n`, `i`, `j` | `gögn_staða`, `VALUE`, `순번`, `안쪽순번` | fjartengdur_VALUE 화면 gögn·tölustafur_VALUE·ítrekun_VALUE staða_INDEX; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `AOT_Minni_LOOKUP`, `커널쌓임공간끝` | vél Tengjast 규약을 유지하면서 eigin 소스에서 사용하는 Heiti |
| `앞캐리지` | `앞줄복귀` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[공용번역기이름대응.tsv](공용번역기이름대응.tsv)에 번역기 참조의 raun_gögn breyta_VALUE_16f64fe4 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[규격이름근거.json](규격이름근거.json)에 기록한다.
`시언어번역기/번역기.c`는 TinyCC 외부 원문을 포함하는 Tengjast 파일로 eigin 선언이 없어서
C eigin skýrsla 분석에서는 제외한다. raun_gögn kjarni_VALUE 빌드에서는 계속 컴파일한다.

### 말의 뿌리와 새로운 복합 Heiti

`Minni_VALUE(記憶)`과 `LOOKUP_INDEX(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 röð_VALUE 있는 항목을 찾아 지정하는 기능에 적용한다.
orðabók 근거는 국립국어원 한국어기초사전의
[Minni_VALUE](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[LOOKUP_INDEX](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`bunki_geymsla`, `쌓기`, `POP_VALUE`는 자료를 포개고 마지막 자료부터 꺼내는 keyra_skipun 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`미리번역`은 keyra_skipun 전에 번역한다는 기능을 직접 나타낸다.
`vél_Word`은 처리기의 gögn 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `vél`를 붙였다.
`기계어미리번역`, `동적기억낱말수` 같은 복합 이름은 현재 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 처음 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 사용 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 gagnagerð·ARRAY_VALUE·fall_VALUE·staðbundið_umfang 변수·grein 이름도 한국어로 바꾼다.
직접 한글 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 Íslenska 이름을
표준 C 범용 문자 표기로 출력한다. raun_gögn ARM64 빌드는 Clang으로 읽을 númer 있는 한글 원문을 사용한다.
strengur_VALUE, C 표준 fall_VALUE, `java_entry` 같은 공개 Tengjast 이름은 바꾸지 않는다.

셸의 사용법·문법 Villa·Skrá 및 Minni_VALUE 공간 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 시험·Skrá flytja_VALUE 도구가 읽는 표식,
명령행 옵션과 기존 skipun_VALUE, JVM klasi_VALUE Heiti·Skrá snið_VALUE·tæki_VALUE 이름은 호환 표기로 남는다.
x86 VGA 문자 화면은 한글을 표시하지 못하므로 Íslenska 문구는 UTF-8 직렬 단말에서 확인한다.
