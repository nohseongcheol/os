# Java 네이티브 compilatore

OpenJDK nativo 소스를 빌드하는 **`--target openjdk-build`**와 nativo kernel_VALORE ABI 검사 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [costruire 방법·effettivo_dati convalidare·kernel_VALORE 이식 ritagliare](OpenJDK-fonte_BLD_E-nativo_kernel-이식.md)를 참고한다.

x86 직접 변환과 ARM64 C generare 후단은 모두 [기계어미리번역.java](자바도구/기계어미리번역.java)로 구현한다. `sh 미리번역.sh`로 직접 실행하며, [기계어미리번역.py](기계어미리번역.py)와 `compilatore.py`는 Indietro_articolo comando·API 및 OpenJDK 도구를 위한 호환 진입점이다. nativo Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 Indietro_articolo 경로와 Python 호출을 위한 호환 진입점이다. FUNZIONE_VALORE·variabile_VALORE·generare C 이름의 뜻과 예외는 [Italiano 명명 README_eb81d7d9](../platforms/rpi4-native/명명/README_eb81d7d9.md)를 참고한다. [ARM64 costruire·Supporto_VALORE ritagliare](../platforms/rpi4-native/README_eb81d7d9.md)에 Esegui_comando 조건이 있다. 전체 OpenJDK나 일반 Corso_VALORE 실행기는 아니다.

Esegui_comando 시 JVM이 필요 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java nativo AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·accesso_voce controllo_VALORE·TIPO_VALORE 검사는 JDK의 `javac`에 맡기고, Java 8 Corso_VALORE 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 바이트코드 해석기를 커널에 넣지 않는다.

```text
Java codiceSorgente → javac의 문법·TIPO_VALORE 검사 → 임시 .class
          → nativo x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 Esegui_comando

costruire host: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. Regolari_articolo 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. esterno_VALORE Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/계산
echo $?                  # 0이면 예제 prove 성공

python3 compilatore.py --target linux --entry 계산.avvia \
    -o build/계산 예제/계산.java

make test
```

`linux` 대상은 Linux의 32비트 Esegui_comando 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 numero 있다. reparto_IT_normale Linux host 또는 해당 실행을 허용한 prove 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int avvia()` 또는 `static void avvia()`처럼 인수가 없어야 한다. `--entry 패키지.Corso_VALORE.FUNZIONE_VALORE`로 선택한다. `int` 반환값은 Linux 프로세스 Esci_app 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` Esegui_comando 환경이나 표준 I_O 라이브러리는 제공하지 않는다.

`--target kernel`은 avvio_macchina 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/compilatore.py --target kernel --entry Nucleo.avvia \
    --export kernel_dispatch=chiamata_di_sistema.Processi_VALORE_voce \
    -o os/build/java.o os/codiceSorgente/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `spazio_utente` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `cellulare_VALORE` 클래스의 hardware_VALORE 직접 접근은 거부한다. spazio_utente ELF는 Linux Esegui_comando file ABI와 다르므로 호스트에서 실행하지 않는다. generare·registro_voce 방법은 [spazio_utente Esegui_comando README_eb81d7d9](../os/spazio_utente/README_eb81d7d9.md)에 있다. `--export 외부기호=Corso_VALORE.FUNZIONE_VALORE`는 오버로드되지 않은 statico_VALORE 함수를 nativo operando_Pila ABI로 노출한다. 커널의 시스템 호출 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. uscitaTesto 옆의 `.s`는 생성된 어셈블리, `.json`은 codiceSorgente SHA-256 및 네이티브 simbolo↔Java FUNZIONE_VALORE 대응표다. Italiano 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 computer 기호를 쓴다. compilare_fonte·assemblare_VALORE·Connetti 중 실패하면 기존 risultato 파일을 덮어쓰지 않는다.

## Supporto_VALORE ritagliare

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 계산 및 TIPO_VALORE CONVERTI_VALORE.
- statico_VALORE 필드와 statico_VALORE FUNZIONE_VALORE, 매개변수·반환값, 재귀, 클래스별 지연 초기화와 inizializza Cicli_VALORE.
- 조건문, 반복문, 단락 평가, 삼항식, intero `switch`, 넓은 locale_Scope variabile_VALORE 인덱스.
- 덧셈·뺄셈·곱셈·나눗셈·나머지·bit_VALORE 연산과 spostare_VALORE. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` generare·초기값 0·durata_VALORE·Lettura·Scrittura·fonti 비교. 256KiB 고정 array_VALORE area_VALORE, 널/pedice_VALORE/Dimensione/e_mail_area 검사.
- stringa_VALORE 리터럴과 `String` fonti, `length()` 및 `charAt()`. 문자열은 UTF-16 CODICE_VALORE 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- Italiano Corso_VALORE·FUNZIONE_VALORE·variabile_VALORE·file Nome.

`new Object`, 인스턴스 valore_del_campo/FUNZIONE_VALORE, 상속/인터페이스, `long/float/double` Esegui_comando operazione_VALORE, `int[]` 이외 array_VALORE, stringa_VALORE 동적 결합, Java 표준 Catalogo, eccezione Processi_VALORE_voce, 스레드·sincronizzare·GC는 미지원이다. 실행에 필요한 미지원 바이트코드나 esterno_VALORE 호출을 발견하면 실패한다. 사용되지 않는 valore_predefinito 생성자는 Esegui_comando 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 numero 있다는 뜻은 아니다.

eccezione oggetto_VALORE 대신 런타임 errore 번호로 중단한다. Linux와 jkoros spazio_utente 대상에서는 `100 + INDICE`로 종료하고 kernel_VALORE 대상에서는 `JKOROS PANIC INDICE`를 출력하고 정지한다. spazio_utente 프로그램만 종료한 경우 셸은 계속 실행된다.

| INDICE | 원인 |
| --- | --- |
| 1 | 0으로 Divisione_KR |
| 2 | 널 fonti |
| 3 | array_VALORE/stringa_VALORE pedice_VALORE ritagliare 초과 |
| 4 | negativo_VALORE array_VALORE Dimensione |
| 5 | array_VALORE area_VALORE 부족 |

array_VALORE 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 limite_VALORE 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 kernel_VALORE 및 신뢰할 numero 있는 작은 프로그램용 stato_iniziale 구현이다.

## native 경계와 ABI

kernel_VALORE 대상에서는 `os/codiceSorgente/cellulare_VALORE.java`, spazio_utente 대상에서는 `os/spazio_utente/dichiarazione/spazio_utente.java`의 정확한 metodo_nome_SMS·서술만 허용한다. 임의의 `native` 함수와 Linux/spazio_utente 대상의 hardware_VALORE 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java codiceSorgente 또는 `.class` 입력을 받는다. 전체 JVM 바이트코드 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 Corso_VALORE percorso/codiceSorgente 경로에서 명시한 소스만 컴파일한다.

## 검증과 implementazione 근거

`prove/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 operazione_VALORE risultato 대조, Corso_VALORE inizializza, intero 극값, stringa_VALORE/array_VALORE, 재귀·switch·wide, 런타임 오류와 미지원 기능 rifiutare_VALORE, errore_VALORE 시 uscitaTesto 보존, spazio_utente ELF/privilegio_VALORE limite_VALORE 및 내보내기 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

comando 의미와 Corso_VALORE file 형식은 Oracle의 [JVM comando specifica](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [Corso_VALORE file specifica](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
