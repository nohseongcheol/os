# Java 네이티브 Compilador

OpenJDK propio 소스를 빌드하는 **`--target openjdk-build`**와 propio valorNúcleo ABI Comprobaciones 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [construirSistema 방법·datosEfectivo validar·valorNúcleo AdaptaciónPlataforma recortar](OpenJDK-YConstruirFuente-NúcleoNativo-AdaptaciónPlataforma.md)를 참고한다.

x86 직접 변환과 ARM64 C generar 후단은 construirTodos [CompilaciónAnticipada.java](HerramientaJava/CompilaciónAnticipada.java)로 구현한다. `sh tiempoDeAnticipado.sh`로 직접 실행하며, [CompilaciónAnticipada.py](CompilaciónAnticipada.py)와 `Compilador.py`는 elementoListaElementoPrevio comando·API 및 OpenJDK 도구를 위한 호환 진입점이다. propio Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 elementoListaElementoPrevio 경로와 Python 호출을 위한 호환 진입점이다. Función·valorVariable·generar C 이름의 뜻과 예외는 [español denominación Guía](../platforms/rpi4-native/denominación/Guía.md)를 참고한다. [ARM64 construirSistema·valorSoporte recortar](../platforms/rpi4-native/Guía.md)에 ejecutarComando 조건이 있다. 전체 OpenJDK나 일반 valorClase 실행기는 아니다.

ejecutarComando 시 JVM이 valorNecesario 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java propio AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·entradaElementoAcceso valorControl·valorTipo 검사는 JDK의 `javac`에 맡기고, Java 8 valorClase 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 códigoBytes 해석기를 커널에 넣지 않는다.

```text
Java fuente → javac의 문법·valorTipo Comprobaciones → valorTemporal .class
          → propio x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 ejecutarComando

construirSistema Anfitrión: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. elementoListaActual 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. valorExterno Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/resultadoCálculo
echo $?                  # 0이면 Ejemplos Pruebas valorÉxito

python3 Compilador.py --target linux --entry resultadoCálculo.ponerEnMarcha \
    -o build/resultadoCálculo Ejemplos/resultadoCálculo.java

make test
```

`linux` 대상은 Linux의 32비트 ejecutarComando 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 númeroValor 있다. esNormal Linux Anfitrión 또는 해당 실행을 허용한 Pruebas 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int ponerEnMarcha()` 또는 `static void ponerEnMarcha()`처럼 인수가 없어야 한다. `--entry 패키지.valorClase.Función`로 선택한다. `int` 반환값은 Linux 프로세스 programaSalir 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` ejecutarComando 환경이나 표준 salidaEntrada 라이브러리는 제공하지 않는다.

`--target kernel`은 Arranque 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/Compilador.py --target kernel --entry Núcleo.ponerEnMarcha \
    --export kernel_dispatch=LlamadaSistema.entradaElementoValorProceso \
    -o os/build/java.o os/fuente/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `Usuario` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `Dispositivo` 클래스의 valorEquipoFísico 직접 접근은 거부한다. Usuario ELF는 Linux ejecutarComando Archivo ABI와 다르므로 호스트에서 실행하지 않는다. generar·registroEntradaElemento 방법은 [Usuario ejecutarComando Guía](../os/Usuario/Guía.md)에 있다. `--export 외부기호=valorClase.Función`는 오버로드되지 않은 valorEstático 함수를 propio pilaOperando ABI로 노출한다. 커널의 시스템 invocar 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. Salida 옆의 `.s`는 생성된 어셈블리, `.json`은 fuente SHA-256 및 네이티브 símbolo↔Java Función 대응표다. español 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 máquina 기호를 쓴다. compilarFuente·ensamblarValor·conectar 중 실패하면 기존 resultado 파일을 덮어쓰지 않는다.

## valorSoporte recortar

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 resultadoCálculo 및 valorTipo convertirValor.
- valorEstático 필드와 valorEstático Función, 매개변수·valorDevuelto, 재귀, 클래스별 지연 초기화와 inicializar valorCiclo.
- 조건문, 반복문, 단락 평가, 삼항식, EnteroValor `switch`, 넓은 ámbitoLocal valorVariable 인덱스.
- resultadoSuma·resultadoResta·곱셈·나눗셈·valorRestoDivisión·valorBit 연산과 valorMover. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` generar·valorInicialValor 0·longitud·leer·escribir·referencia 비교. 256KiB 고정 valorArreglo valorRegión, 널/valorÍndiceArreglo/tamaño/regiónDirección Comprobaciones.
- Cadena 리터럴과 `String` referencia, `length()` 및 `charAt()`. 문자열은 UTF-16 valorCódigo 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- español valorClase·Función·valorVariable·Archivo nombre.

`new Object`, 인스턴스 valorCampo/Función, 상속/인터페이스, `long/float/double` ejecutarComando valorOperación, `int[]` 이외 valorArreglo, Cadena 동적 valoresCombinar, Java 표준 biblioteca, excepción entradaElementoValorProceso, 스레드·sincronizar·GC는 미지원이다. 실행에 필요한 esNoAdmitido 바이트코드나 valorExterno 호출을 발견하면 실패한다. 사용되지 않는 valorPredeterminado 생성자는 ejecutarComando 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 númeroValor 있다는 뜻은 아니다.

excepción valorObjeto 대신 런타임 error 번호로 중단한다. Linux와 jkoros Usuario 대상에서는 `100 + número`로 종료하고 valorNúcleo 대상에서는 `JKOROS PANIC número`를 출력하고 정지한다. Usuario 프로그램만 종료한 경우 셸은 procesamientoContinuar 실행된다.

| número | 원인 |
| --- | --- |
| 1 | 0으로 resultadoDivisión |
| 2 | 널 referencia |
| 3 | valorArreglo/Cadena valorÍndiceArreglo recortar 초과 |
| 4 | valorNegativo valorArreglo tamaño |
| 5 | valorArreglo valorRegión 부족 |

valorArreglo 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 valorFrontera 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 valorNúcleo 및 신뢰할 númeroValor 있는 작은 프로그램용 estadoValorInicialValor 구현이다.

## native 경계와 ABI

valorNúcleo 대상에서는 `os/fuente/Dispositivo.java`, Usuario 대상에서는 `os/Usuario/Declaraciones/Usuario.java`의 정확한 textoNombreMétodo·서술만 허용한다. 임의의 `native` 함수와 Linux/Usuario 대상의 valorEquipoFísico 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java fuente 또는 `.class` 입력을 받는다. 전체 JVM códigoBytes 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 valorClase ruta/fuente 경로에서 명시한 소스만 컴파일한다.

## 검증과 implementación 근거

`Pruebas/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 valorOperación resultado 대조, valorClase inicializar, EnteroValor 극값, Cadena/valorArreglo, 재귀·switch·wide, 런타임 오류와 esNoAdmitido 기능 rechazarValor, valorFallo 시 Salida 보존, Usuario ELF/valorPermiso valorFrontera 및 emitirValor 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

comando 의미와 valorClase Archivo 형식은 Oracle의 [JVM comando especificación](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [valorClase Archivo especificación](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
