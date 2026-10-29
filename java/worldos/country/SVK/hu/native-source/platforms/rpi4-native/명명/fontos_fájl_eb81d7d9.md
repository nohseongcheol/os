# saját 커널과 번역기의 magyar Név

대상은 `platforms/rpi4-native`의 saját Java kernel_ÉRTÉK, felhasználó JVM, C gép Kapcsolódás,
TCP/UDP·FTP, C fordítóprogram_eszköz 이식부, MicroPython 이식부, épít_Rendszer·végrehajt_parancs·시험 도구다.
`golang/worldos/Country_ÉRTÉK/KOR/FORRÁS`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 saját 선언도 명명 검사에 포함한다.
Linux 실행판의 gazda Eszközök, OpenJDK 보조 Eszközök 및 külső_ÉRTÉK elosztás_ÉRTÉK forrás_fa 전체를
한국어로 újrapróbál_ÉRTÉK 작성했다는 뜻은 아니다.

## 명명 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `fájlleíró`, `társ_portszám`, `halommemória_tár`, `billentyűzet`.
- 함수는 행위를 나타낸다: `Olvasás`, `Írás`, `Megnyitás`, `Bezárás`, `NET_BIND`, `futtat_app`.
- TCP의 이어진 bájt_ÉRTÉK 흐름과 UDP의 határ_ÉRTÉK 있는 자료를 `ismerős`와 `datagram_Csatorna`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `hossz_ÉRTÉK`, `adat_pozíció`, `KERES_INDEX`, `반환값`으로 풀어 쓴다.
  순번·임시 산술값처럼 여러 역할에 재사용되는 변수는 `순번`, `첫째값`, `MPERC_ÉRTÉK`으로 구별한다.
- 이름이 같아도 külső_ÉRTÉK 구조체의 필드와 saját 변수는 별도로 분석한다.

`Csatorna_bejegyzés(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 kommunikáció 연결에
적용했다. `port_ÉRTÉK(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [Csatorna_bejegyzés](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[port_ÉRTÉK](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`datagram(電文)`은 전보에 담는 글이라는 기존 kommunikáció 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 datagram](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`Stream_ÉRTÉK`, `szál_ÉRTÉK`, `쌓임`은 우리말의 움직임·이어짐·쌓이는 모양을 빌린 표현이다.
`bemeneti_adatfolyam`, `dolgozó`, `Sor_tár` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 szótár 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 FORDÍTÁS_forrás·국어사 datagram 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 Név | 이유 |
|---|---|---|
| TCP Socket | ismerős | 상대와 연결되어 rendel_ÉRTÉK 있는 바이트를 주고받음 |
| ServerSocket | fogad_port | 새 연결이 들어오는 접점 |
| DatagramSocket | datagram_Csatorna | 각 자료의 경계를 보존하는 kommunikáció |
| InputStream / OutputStream | bemeneti_adatfolyam / kimeneti_adatfolyam | 들어오고 나가는 바이트의 rendel_ÉRTÉK |
| heap / stack | halommemória_tár / Sor_tár | kioszt_tár 방식과 쌓고 꺼내는 architektúra |
| thread / keyboard | dolgozó / billentyűzet | 이어지는 실행과 글쇠의 TÖMB_ÉRTÉK |
| exception / timeout | kivétel / várj_IDŐTÚLLÉPÉS_kivétel | informatikai_részleg_normál 처리에서 벗어남과 그 구체적 이유 |

## 경로와 대응표

| 구현 | magyar ÚTVONAL |
|---|---|
| kernel_ÉRTÉK·felület·Fájl réteg_ÉRTÉK | `FORRÁS/*.java` |
| felhasználó JVM | `felhasználó/자바/자바가상기계.java` |
| ARM64 gép Kapcsolódás | `gép/*.c`, `부팅/` |
| TCP·UDP·FTP | `hálózat_Sor/hálózat_Sor.c`, `hálózat_Sor/fájlátvitel.c` |
| C fordítóprogram_eszköz 이식 | `C_fordítóprogram/` |
| MicroPython 이식 | `PYTHON_híd/` |
| épít_Rendszer·végrehajt_parancs·시험 | `Eszközök/`, `készít_bejegyzés.mk` |
| Java felhasználó API | `한국어자바/magyar/saját/` |

[fájlnév_leképezés.tsv](fájlnév_leképezés.tsv), [자바이름대응.tsv](자바이름대응.tsv),
[C_név_leképezés.tsv](C_név_leképezés.tsv), [PYTHON_név_leképezés.tsv](PYTHON_név_leképezés.tsv)에
Előző_cikk 이름과 바뀐 이름이 있다. C/Java 대응표의 Fájl·위치는 이행 당시 기준이다.
ÚTVONAL 이동은 Fájl 대응표를 함께 본다. 기존 `tools/*.py`는 magyar 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 SD Név

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
aktuális_cikk 다섯 Java 예제는 `Futtatás()`·`실행인수`·magyar 화면/szál_ÉRTÉK API를 사용해
예약어·리터럴 외의 식별자를 한국어로 작성한다. 화면/가닥은 표준 객체를
감싸지 않고 saját JVM에 직접 구현했다. 자세한 계약은 [magyar Java API](../한국어자바/fontos_fájl_eb81d7d9.md)를 본다.

표준 javac는 sztring_ÉRTÉK 리터럴에 `java.lang.String`, sztring_ÉRTÉK 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 magyar 소스에서도 바이트코드에 남을 szám 있다.
기존 표준 class를 실행하는 JVM의 leképezés_ÉRTÉK sztring_ÉRTÉK, 아직 표준 라이브러리를 쓰는
kommunikáció·Fájl 연결부까지 모두 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
서술자·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 FÜGGVÉNY_ÉRTÉK·egész_szám_beír·POSIX ABI, CPU jegyzék_ÉRTÉK Név, 어셈블리 Parancs, 링커 절 Név,
TinyCC·lwIP·MicroPython이 요구하는 Beállítások 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
saját C 함수의 forrás_fa 이름은 한국어이며, [기계연결이름.h](기계연결이름.h)가
기존 AOT·어셈블리·SDK에 공개한 gép 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 modul_ÉRTÉK attribútum_ÉRTÉK, 명령행 옵션과 JSON 키도
külső_ÉRTÉK 계약이다. `build/`, elosztás_ÉRTÉK 바이너리 이름과 `/sdk`는 기존 végrehajt_parancs 경로를 유지한다.
külső_ÉRTÉK 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Eszközök/명명검사.py
make épít_Rendszer
make 시험
make test-examples test-ftp test-elf
python3 Eszközök/végrehajt_parancs.py --desktop --network
```

`Eszközök/시언어이름분석.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`Eszközök/*이름반영.py`는 módosítás_ÉRTÉK 전 forrás_fa·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 újrapróbál_ÉRTÉK 적용하여 대응표를 덮어쓰지 않는다.

## C kommunikáció 구조체와 Python HIBA

C 통신에서 `갈래`는 CÍM 체계를 구분하고 `portszám`는 port, `CÍM_ÉRTÉK`은
IPv4 주소의 32비트 값을 나타낸다. `datagram_protokoll`은 앞서 설명한 datagram(電文)과
szerződés_értéke(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | magyar 직접 구현 |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 háló_Család / datagram_szoftvercsatorna / datagram_protokoll |
| struct pk_sockaddr_in | struct háló_szoftvercsatorna_CÍM |
| sin_family / sin_port | CÍM_Család / portszám |
| sin_addr.s_addr | internetcím.CÍM_ÉRTÉK |
| OSError / HIBA.args[0] | rendszerhiba / HIBA.INDEX |

magyar 구조체는 `#define` 치환이나 mezőérték 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 kernel_ÉRTÉK SVC에서 bájt_ÉRTÉK 복사로
검사한다. `készít_végpont`·`küld_datagram_adat`와 Fájl 함수는 statikus_ÉRTÉK 라이브러리에
tényleges_adat magyar 이름의 FÜGGVÉNY_ÉRTÉK 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
Előző_cikk 코드에서 magyar kommunikáció 함수에 pk_sockaddr*를 전달했다면 magyar 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `rendszerhiba`는 OSError의 magyar 하위 클래스이며 연결부에서
HIBA 번호를 보존하여 변환한다. 일반 Python 문법과 külső_ÉRTÉK 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 klip

`실행할일`은 수행할 내용을, `Végrehajtás`는 그 수행을 나타낸다.
`동작받이`는 동작이 발생했다는 알림을 받는 역할, `Action_alapelv`은 전달되는 사건이다.
`gomb`는 눌러 동작시키는 조작부, `Címke`는 fontos_fájl_eb81d7d9 글의 helyzetindex,
`szövegmező`은 글을 적는 helyzetindex, `dolgozó`은 이어지는 végrehajt_parancs 흐름을 뜻한다.
`végrehajt_parancs(實行)`·`Művelet(動作)`의 기존 뜻과 `받다`·`알리다`·`szál_ÉRTÉK`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 처음 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 Eszközök/forrás_vélemény.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 kivonat_Fájl,
ASCII 파일명과 Python의 영어 bevallás 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/자바도구/기계어미리번역.java`로 전환했다. `compiler/기계어미리번역.py`는 호환 진입점이다.
`compiler/arm64.py`는 Előző_cikk 경로와 `ARM64(...).generate(...)` 호출을 이어 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK 보조 Eszközök, Linux verzió_ÉRTÉK 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
예약어 외 100% 한국어라고 판정하지 않는다.
`Eszközök/명명검사.py --C_Nyelv`는 Aktív ARM64 소스의 bevallás, C 의미 Elemzés_ÉRTÉK,
x86 Java 커널과 공용 번역기의 saját bevallás, Java 예제 전체 azonosító_ÉRTÉK,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## aktuális_cikk 기능을 기준으로 보완한 Név

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 magyar 이름을 달리 정한다.
Fájl 이름은 주된 기능을 나타내고, FÜGGVÉNY_ÉRTÉK 이름은 행동을, változó_ÉRTÉK 이름은 담는 자료를 나타낸다.
예약어, 표준 API 및 külső_ÉRTÉK Kapcsolódás 규약은 따로 기록한다.

| Előző_cikk Név | 적용한 Név | aktuális_cikk 기능 |
|---|---|---|
| `arm64.py`의 구현 | `compiler/자바도구/기계어미리번역.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 FORDÍTÁS_forrás |
| `ARM64`, `generate` | `gép_KÓD_fordítóprogram`, `generálás` | FORDÍTÁS_forrás 상태를 담는 객체와 C FORRÁS generálás 행동 |
| `prototype`, `method` | `함수원형`, `metódus_törzs` | 함수의 formáz_ÉRTÉK 선언과 tényleges_adat Parancs FORRÁS |
| `profile`, `heap_words` | `végrehajtás_cél`, `halommemória_szó_DARAB` | kernel_ÉRTÉK·felhasználó 구분과 kioszt_tár Memória_ÉRTÉK 공간의 gép 낱말 szám |
| `pc`, `op` | `parancs_pozíció`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 INDEX |
| `x`, `y`, `w`, `h` | `x_koordináta`, `Y_koordináta`, `영역너비`, `영역높이` | távoli_ÉRTÉK 화면의 위치와 직사각형 Méret |
| `p`, `n`, `i`, `j` | `adat_pozíció`, `ÉRTÉK`, `순번`, `안쪽순번` | távoli_ÉRTÉK 화면 adat·számjegy_ÉRTÉK·futam_ÉRTÉK helyzetindex; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `AOT_Memória_KERES`, `커널쌓임공간끝` | gép Kapcsolódás 규약을 유지하면서 saját 소스에서 사용하는 Név |
| `앞캐리지` | `앞줄복귀` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[공용번역기이름대응.tsv](공용번역기이름대응.tsv)에 fordítóprogram_eszköz 참조의 tényleges_adat módosítás_ÉRTÉK 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[Standard_név_evidence.json](Standard_név_evidence.json)에 기록한다.
`C_fordítóprogram/fordítóprogram_eszköz.c`는 TinyCC külső_ÉRTÉK 원문을 포함하는 Kapcsolódás 파일로 saját 선언이 없어서
C saját bevallás 분석에서는 제외한다. tényleges_adat kernel_ÉRTÉK 빌드에서는 계속 컴파일한다.

### 말의 뿌리와 새로운 복합 Név

`Memória_ÉRTÉK(記憶)`과 `KERES_INDEX(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 rendel_ÉRTÉK 있는 항목을 찾아 지정하는 기능에 적용한다.
szótár 근거는 국립국어원 한국어기초사전의
[Memória_ÉRTÉK](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[KERES_INDEX](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`Sor_tár`, `küldés_ÉRTÉK`, `POP_ÉRTÉK`는 자료를 포개고 마지막 자료부터 꺼내는 végrehajt_parancs 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`미리번역`은 végrehajt_parancs 전에 번역한다는 기능을 직접 나타낸다.
`gép_szó`은 처리기의 adat 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `gép`를 붙였다.
`기계어미리번역`, `halommemória_szó_DARAB` 같은 복합 이름은 aktuális_cikk 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 처음 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 használ_ÉRTÉK 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 adattípus·TÖMB_ÉRTÉK·FÜGGVÉNY_ÉRTÉK·helyi_hatókör változó_ÉRTÉK·ág 이름도 한국어로 바꾼다.
직접 한글 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 magyar 이름을
표준 C 범용 문자 표기로 출력한다. tényleges_adat ARM64 빌드는 Clang으로 읽을 szám 있는 한글 원문을 사용한다.
sztring_ÉRTÉK, C 표준 FÜGGVÉNY_ÉRTÉK, `java_entry` 같은 공개 Kapcsolódás 이름은 바꾸지 않는다.

셸의 사용법·문법 HIBA·Fájl 및 Memória_ÉRTÉK CÍM_régió 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 시험·Fájl átvisz_ÉRTÉK 도구가 읽는 jelölő_ÉRTÉK,
명령행 옵션과 기존 명령어, JVM tanóra_ÉRTÉK Név·Fájl formáz_ÉRTÉK·mobil_ÉRTÉK 이름은 호환 표기로 남는다.
x86 VGA 문자 화면은 한글을 표시하지 못하므로 magyar 문구는 UTF-8 직렬 단말에서 확인한다.
