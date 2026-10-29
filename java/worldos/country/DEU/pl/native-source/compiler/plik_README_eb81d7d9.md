# Java 네이티브 kompilator

OpenJDK własny 소스를 빌드하는 **`--target openjdk-build`**와 własny jądro_WARTOŚĆ ABI 검사 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [BLD_System 방법·rzeczywisty_dane walidować·jądro_WARTOŚĆ 이식 obcinać](OpenJDK-źródło_BLD_ORAZ-natywny_jądro-이식.md)를 참고한다.

x86 직접 변환과 ARM64 C generować 후단은 모두 [기계어미리번역.java](자바도구/기계어미리번역.java)로 구현한다. `sh 미리번역.sh`로 직접 실행하며, [기계어미리번역.py](기계어미리번역.py)와 `kompilator.py`는 Wstecz_towar polecenie·API 및 OpenJDK 도구를 위한 호환 진입점이다. własny Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 Wstecz_towar 경로와 Python 호출을 위한 호환 진입점이다. FUNKCJA_WARTOŚĆ·zmienna_WARTOŚĆ·generować C 이름의 뜻과 예외는 [polski 명명 plik_README_eb81d7d9](../platforms/rpi4-native/명명/plik_README_eb81d7d9.md)를 참고한다. [ARM64 BLD_System·wsparcie_WARTOŚĆ obcinać](../platforms/rpi4-native/plik_README_eb81d7d9.md)에 Wykonaj_polecenie 조건이 있다. 전체 OpenJDK나 일반 Klasa_WARTOŚĆ 실행기는 아니다.

Wykonaj_polecenie 시 JVM이 필요 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java własny AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·dostęp_wpis kontrola_WARTOŚĆ·TYP_WARTOŚĆ 검사는 JDK의 `javac`에 맡기고, Java 8 Klasa_WARTOŚĆ 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 바이트코드 해석기를 커널에 넣지 않는다.

```text
Java plik_źródłowy → javac의 문법·TYP_WARTOŚĆ 검사 → 임시 .class
          → własny x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 Wykonaj_polecenie

BLD_System host: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. bieżący_towar 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. zewnętrzny_WARTOŚĆ Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/계산
echo $?                  # 0이면 예제 testy 성공

python3 kompilator.py --target linux --entry 계산.Uruchom_2 \
    -o build/계산 예제/계산.java

make test
```

`linux` 대상은 Linux의 32비트 Wykonaj_polecenie 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 identyfikator 있다. systemy_informacyjne_zwykła Linux host 또는 해당 실행을 허용한 testy 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int Uruchom_2()` 또는 `static void Uruchom_2()`처럼 인수가 없어야 한다. `--entry 패키지.Klasa_WARTOŚĆ.FUNKCJA_WARTOŚĆ`로 선택한다. `int` 반환값은 Linux 프로세스 wyjść_program 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` Wykonaj_polecenie 환경이나 표준 We_Wy 라이브러리는 제공하지 않는다.

`--target kernel`은 rozruch_maszyny 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/kompilator.py --target kernel --entry jądro.Uruchom_2 \
    --export kernel_dispatch=wywołanie_systemowe.Proces_WARTOŚĆ_wpis \
    -o os/build/java.o os/plik_źródłowy/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `przestrzeń_użytkownika` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `urządzenie_WARTOŚĆ` 클래스의 sprzęt_WARTOŚĆ 직접 접근은 거부한다. przestrzeń_użytkownika ELF는 Linux Wykonaj_polecenie nazwa_pliku ABI와 다르므로 호스트에서 실행하지 않는다. generować·rejestr_wpis 방법은 [przestrzeń_użytkownika Wykonaj_polecenie plik_README_eb81d7d9](../os/przestrzeń_użytkownika/plik_README_eb81d7d9.md)에 있다. `--export 외부기호=Klasa_WARTOŚĆ.FUNKCJA_WARTOŚĆ`는 오버로드되지 않은 statyczny_WARTOŚĆ 함수를 własny operand_Stos ABI로 노출한다. 커널의 시스템 호출 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. pozycja_wyjścia 옆의 `.s`는 생성된 어셈블리, `.json`은 plik_źródłowy SHA-256 및 네이티브 symbol↔Java FUNKCJA_WARTOŚĆ 대응표다. polski 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 maszyna 기호를 쓴다. kompilować_źródło·asemblować_WARTOŚĆ·Połącz 중 실패하면 기존 WYNIK 파일을 덮어쓰지 않는다.

## wsparcie_WARTOŚĆ obcinać

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 계산 및 TYP_WARTOŚĆ KONWERTUJ_WARTOŚĆ.
- statyczny_WARTOŚĆ 필드와 statyczny_WARTOŚĆ FUNKCJA_WARTOŚĆ, 매개변수·반환값, 재귀, 클래스별 지연 초기화와 inicjuj Cykl_WARTOŚĆ.
- 조건문, 반복문, 단락 평가, 삼항식, liczba_całkowita `switch`, 넓은 lokalny_Scope zmienna_WARTOŚĆ 인덱스.
- 덧셈·뺄셈·곱셈·나눗셈·나머지·bit_WARTOŚĆ 연산과 przenosić_WARTOŚĆ. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` generować·초기값 0·długość_WARTOŚĆ·Odczyt·Zapis·odwołanie 비교. 256KiB 고정 TABLICA_WARTOŚĆ region_WARTOŚĆ, 널/indeks_dolny_WARTOŚĆ/Rozmiar/ADRES_region 검사.
- ciąg_WARTOŚĆ 리터럴과 `String` odwołanie, `length()` 및 `charAt()`. 문자열은 UTF-16 KOD_WARTOŚĆ 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- polski Klasa_WARTOŚĆ·FUNKCJA_WARTOŚĆ·zmienna_WARTOŚĆ·nazwa_pliku Nazwa.

`new Object`, 인스턴스 wartość_pola/FUNKCJA_WARTOŚĆ, 상속/인터페이스, `long/float/double` Wykonaj_polecenie zabieg_WARTOŚĆ, `int[]` 이외 TABLICA_WARTOŚĆ, ciąg_WARTOŚĆ 동적 결합, Java 표준 biblioteka, wyjątek Proces_WARTOŚĆ_wpis, 스레드·synchronizować·GC는 미지원이다. 실행에 필요한 미지원 바이트코드나 zewnętrzny_WARTOŚĆ 호출을 발견하면 실패한다. 사용되지 않는 wartość_domyślna 생성자는 Wykonaj_polecenie 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 identyfikator 있다는 뜻은 아니다.

wyjątek obiekt_WARTOŚĆ 대신 런타임 błąd 번호로 중단한다. Linux와 jkoros przestrzeń_użytkownika 대상에서는 `100 + INDEKS`로 종료하고 jądro_WARTOŚĆ 대상에서는 `JKOROS PANIC INDEKS`를 출력하고 정지한다. przestrzeń_użytkownika 프로그램만 종료한 경우 셸은 계속 실행된다.

| INDEKS | 원인 |
| --- | --- |
| 1 | 0으로 Dywizja_KR |
| 2 | 널 odwołanie |
| 3 | TABLICA_WARTOŚĆ/ciąg_WARTOŚĆ indeks_dolny_WARTOŚĆ obcinać 초과 |
| 4 | negatywny_WARTOŚĆ TABLICA_WARTOŚĆ Rozmiar |
| 5 | TABLICA_WARTOŚĆ region_WARTOŚĆ 부족 |

TABLICA_WARTOŚĆ 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 granica_WARTOŚĆ 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 jądro_WARTOŚĆ 및 신뢰할 identyfikator 있는 작은 프로그램용 stan_początkowy 구현이다.

## native 경계와 ABI

jądro_WARTOŚĆ 대상에서는 `os/plik_źródłowy/urządzenie_WARTOŚĆ.java`, przestrzeń_użytkownika 대상에서는 `os/przestrzeń_użytkownika/deklaracja/przestrzeń_użytkownika.java`의 정확한 metoda_nazwa_SMS·서술만 허용한다. 임의의 `native` 함수와 Linux/przestrzeń_użytkownika 대상의 sprzęt_WARTOŚĆ 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java plik_źródłowy 또는 `.class` 입력을 받는다. 전체 JVM 바이트코드 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 Klasa_WARTOŚĆ ścieżka_2/plik_źródłowy 경로에서 명시한 소스만 컴파일한다.

## 검증과 implementacja 근거

`testy/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 zabieg_WARTOŚĆ WYNIK 대조, Klasa_WARTOŚĆ inicjuj, liczba_całkowita 극값, ciąg_WARTOŚĆ/TABLICA_WARTOŚĆ, 재귀·switch·wide, 런타임 오류와 미지원 기능 odrzucić_WARTOŚĆ, awaria_WARTOŚĆ 시 pozycja_wyjścia 보존, przestrzeń_użytkownika ELF/pozwolenie_WARTOŚĆ granica_WARTOŚĆ 및 내보내기 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

polecenie 의미와 Klasa_WARTOŚĆ nazwa_pliku 형식은 Oracle의 [JVM polecenie 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [Klasa_WARTOŚĆ nazwa_pliku 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
