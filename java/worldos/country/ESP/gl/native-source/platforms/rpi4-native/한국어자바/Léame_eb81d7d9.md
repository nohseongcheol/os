# Galego Java 통신·E_S·excepción API

패키지는 `Galego.자체`다. hospedar `javac --release 8`로 컴파일한 class를
자체 ARM64 커널의 JVM에서 실행한다. 통신·Ficheiro·excepción API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 tema_VALOR API는 자체 JVM 전용이다.
기존 표준 Java biblioteca 전체의 Galego 번역판은 아니다.

```java
import Galego.자체.*;

public class Rede {
    public static void main(String[] Argumentos) throws E_S_excepción {
        conexión Conectar = conexión.Abrir("10.0.2.2", 9000);
        try {
            Conectar.TIMEOUT(700);
            Conectar.Saída().Escritura(문자.부호화("안녕하세요\n"));
            입력흐름 입력 = Conectar.입력();
            Saída.수쓰기(입력.Lectura());
        } catch (agarda_TIMEOUT_excepción ERRO) {
            Saída.escribir_liña(ERRO.설명());
        } finally {
            Conectar.Pechar();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
usuario 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 cadea_VALOR 리터럴에 사용하는 표준 클래스다. 자체 실행기는 `public static void Executar_2()`도 진입점으로 받는다.

## 통신과 fluxo_VALOR

| Clase_VALOR | Galego 호출 |
|---|---|
| conexión | `Abrir(ENDEREZO, número_do_porto)`, `입력()`, `Saída()`, `TIMEOUT(밀리초)`, `número_do_porto()`, `local_número_do_porto()`, `연결됨()`, `닫힘()`, `Pechar()` |
| 수신창구 | `Abrir(número_do_porto)`, `받기()`, `número_do_porto()`, `TIMEOUT(밀리초)`, `닫힘()`, `Pechar()` |
| 입력흐름 | `Lectura()`, `Lectura(byte[])`, `Lectura(byte[], Executar_2, duración_VALOR)`, `Pechar()` |
| 출력흐름 | `Escritura(int)`, `Escritura(byte[])`, `Escritura(byte[], Executar_2, duración_VALOR)`, `내보내기()`, `Pechar()` |
| 전문통로 | `Abrir(número_do_porto)`, `enviar(ENDEREZO, número_do_porto, Texto)`, `받기()`, `TIMEOUT(밀리초)`, `número_do_porto()`, `닫힘()`, `Pechar()` |
| 연결통신 | `Abrir(...)`, `수신열기(...)`는 위 Galego 객체를 devolver_medida |
| 검사 | `참인지(condición, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Lectura()`의 Ficheiro 끝은 -1, MATRIZ_VALOR 읽기의 반환값은 real_datos 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. número_do_porto 0은 빈 번호를 자동 배정한다.
UDP 전문은 ao_corrente_elemento 자체 커널에서 512바이트까지 받으며, 주소는 díxito_VALOR IPv4를 사용한다.
`localhost` 루프백 외의 Nome 풀이(DNS)는 자체 커널에 아직 없다.

기존 `연결통신.Conectar/agardar_extremo/받기`, `통신.Abrir/enviar/받기`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `conexión`, `수신창구`, `전문통로`를 쓴다.

## Galego excepción

모든 아래 클래스는 valor_predefinido 생성자, `새예외("설명")` 형태의 cadea_VALOR 생성자와
`설명()`을 제공한다. real_datos xerar 문법은 `new agarda_TIMEOUT_excepción("agarda_Estado 끝")`이다.

| Galego excepción | 상위 Clase_VALOR / 용도 |
|---|---|
| excepción | `java.lang.Exception`, 직접 던지는 일반 검사 excepción |
| 실행예외 | `java.lang.RuntimeException` |
| E_S_excepción | `java.io.IOException`, Galego Ficheiro·통신 API의 검사 excepción |
| agarda_TIMEOUT_excepción | `E_S_excepción`, 통신 TIMEOUT 초과 |
| ENDEREZO_Busca_excepción | `E_S_excepción`, ENDEREZO verificar erro_VALOR |
| 파일없음예외 | `E_S_excepción`, Ficheiro Abrir erro_VALOR |
| 통신예외 | `E_S_excepción`, 표준 SocketException CONVERTER_VALOR |
| non_válido_argumento_excepción | `java.lang.IllegalArgumentException` |
| 숫자형식예외 | `non_válido_argumento_excepción` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| NULO_Material_de_referencia_excepción | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| Estado_excepción | `java.lang.IllegalStateException` |
| TIPO_conversión_excepción | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| MATRIZ_Store_erro | `java.lang.ArrayStoreException` |
| tema_Estado_excepción | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 agarda_VALOR 중단 |

`excepción`와 `실행예외`는 모든 Galego 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, Ficheiro·통신 전체를 잡으려면 `catch (E_S_excepción ERRO)`를 쓴다.
Galego API가 표준 E_S 오류를 Galego 예외로 변환한다.
기존 Galego 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`agarda_TIMEOUT_excepción`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
excepción 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
ao_corrente_elemento 자체 JVM에 이 20종을 추가했다. 임의의 usuario Throwable 하위 Clase_VALOR 전체를
지원하도록 확장했다는 뜻은 아니다.

## compilar_fonte·executar_comando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make compilar_sistema
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 시험/자바/한국어통신시험.java
python3 Ferramentas/executar_Ficheiro.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 usuario JVM ELF 안에 탑재된다. `.jar`는 hospedar javac의
Clase_VALOR 경로로 사용한다. fonte_árbore 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 Galego 예외의 `throws` 선언과 그 import를 인식한다.
자체 JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·obxecto_VALOR·소켓 예제 전체의 fonte_árbore 컴파일은 hospedar javac를 사용한다.
`/example/java/파일예제.java`는 게스트 javac로도 컴파일할 수 있다.

real_datos TCP/UDP 예제는 [네트워크예제.java](../../../example/java/네트워크예제.java),
executar_comando 절차는 [example Léame_eb81d7d9](../../../example/README.md),
fonte_árbore 명명 원칙은 [명명 Léame_eb81d7d9](../명명/Léame_eb81d7d9.md)에 있다.

## Swing Xanela 예제

`/example/java/창예제.java`와 컴파일된 `.class`가 부팅 시 준비된다.
`cd /example/java` Seguinte_elemento `java 창예제`로 연다. Nome 입력, 인사하기 버튼,
인사말과 clic_VALOR 횟수 actualizar, X 닫기를 지원한다.

| 기능 | Galego 직접 API |
|---|---|
| Runnable / run | `실행할일.Executar()` |
| ActionListener / actionPerformed | `동작받이.동작받기(동작알림 알림)` |
| ActionEvent | `동작알림.comando_SMS()`, `evento_fonte()`, `ÍNDICE()` |
| JFrame | `Xanela(ventá_Título, 폭, 높이)`, `engadir_elemento(화면구성요소)`, `mostrar_ventá()`, `Pechar()`, `보이는가()` |
| JButton | `botón(Texto, 가로, Vertical_cargo, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Etiqueta(...)`, `SMS_campo(...)` |
| 공통 화면 elemento_VALOR | `화면구성요소.글읽기()`, `escribir_SMS(Texto)`, `자리정하기(가로, Vertical_cargo, 폭, 높이)` |
| SwingUtilities.invokeLater | `evento_cola.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `작업가닥(실행할일)`, `START_tarefa()`, `기다리기()`, `살아있는가()`, `suspender_tarefa()` |
| 명령행 | `Executar_2()`, `실행인수.elemento_CONTAR()`, `실행인수.Texto(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
자체 JVM의 `한국어화면호출`, `Proceso_tema`가 Galego Clase_VALOR·메서드·서술자를
해석해 화면 요소와 executar_comando 가닥을 직접 만든다. Acción 알림도 자체 객체이며
콜백으로 `Executar`와 `동작받기`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 executar_comando 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 자체 JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 hospedar JVM에서 무동작 객체가 생기지 않도록 하는 rexeitar_VALOR_e3ecc00b 경로다.
자체 JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 구현 API를
실행할 수 없다. hospedar javac로 컴파일한 ATRÁS_VALOR 자체 JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import Galego.자체.*;
public class 가닥예제 implements 실행할일 {
    public void Executar() { Saída.escribir_liña("Galego 작업 executar_comando"); }
    public static void Executar_2() throws 대기중단예외 {
        작업가닥 tema_VALOR = 작업.Executar_2(new 가닥예제());
        작업.기다리기(tema_VALOR);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
MATRIZ_VALOR Argumentos 대신 `실행인수`, 길이는 `문자.byte_CONTAR`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
자체 실행기는 Argumentos 없는 `Executar_2()`을 우선한다.
기존 Galego 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Executar_2(Runnable)`을 사용하던 코드는 새 Galego 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API soporte_VALOR 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 Clase_VALOR·메서드 이름과 서술자가 남는다.
Galego Nome 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·메서드 재정의, native Conectar, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS 식별자](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS 메서드 Material_de_referencia](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
