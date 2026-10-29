# Català Java 통신·E_S·excepció API

패키지는 `Català.propi`다. allotjar `javac --release 8`로 컴파일한 class를
propi ARM64 커널의 JVM에서 실행한다. 통신·Fitxer·excepció API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 fil_VALOR API는 propi JVM 전용이다.
기존 표준 Java biblioteca 전체의 Català 번역판은 아니다.

```java
import Català.propi.*;

public class xarxa {
    public static void main(String[] 인수) throws E_S_excepció {
        connexió Connecta = connexió.Obre("10.0.2.2", 9000);
        try {
            Connecta.TIMEOUT(700);
            Connecta.Sortida().Escriptura(문자.부호화("안녕하세요\n"));
            입력흐름 입력 = Connecta.입력();
            Sortida.수쓰기(입력.Lectura());
        } catch (Espera_TIMEOUT_excepció s_ha_produït_un_error) {
            Sortida.escriure_línia(s_ha_produït_un_error.설명());
        } finally {
            Connecta.Tanca();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
usuari 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 cadena_VALOR 리터럴에 사용하는 표준 클래스다. propi 실행기는 `public static void Executa_2()`도 진입점으로 받는다.

## 통신과 flux_VALOR

| Classe_VALOR | Català 호출 |
|---|---|
| connexió | `Obre(Adreça, número_de_port)`, `입력()`, `Sortida()`, `TIMEOUT(밀리초)`, `número_de_port()`, `local_número_de_port()`, `연결됨()`, `닫힘()`, `Tanca()` |
| rebre_port | `Obre(número_de_port)`, `rebre()`, `número_de_port()`, `TIMEOUT(밀리초)`, `닫힘()`, `Tanca()` |
| 입력흐름 | `Lectura()`, `Lectura(byte[])`, `Lectura(byte[], Executa_2, durada_VALOR)`, `Tanca()` |
| 출력흐름 | `Escriptura(int)`, `Escriptura(byte[])`, `Escriptura(byte[], Executa_2, durada_VALOR)`, `내보내기()`, `Tanca()` |
| 전문통로 | `Obre(número_de_port)`, `enviar(Adreça, número_de_port, SMS)`, `rebre()`, `TIMEOUT(밀리초)`, `número_de_port()`, `닫힘()`, `Tanca()` |
| 연결통신 | `Obre(...)`, `수신열기(...)`는 위 Català 객체를 tornar_les_tasques_mesura |
| 검사 | `참인지(condició, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Lectura()`의 Fitxer 끝은 -1, MATRIU_VALOR 읽기의 반환값은 real_dades 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. número_de_port 0은 빈 번호를 자동 배정한다.
UDP 전문은 현재 propi 커널에서 512바이트까지 받으며, 주소는 dígit_VALOR IPv4를 사용한다.
`localhost` 루프백 외의 Nom 풀이(DNS)는 propi 커널에 아직 없다.

기존 `연결통신.Connecta/escoltar_extrem/rebre`, `통신.Obre/enviar/rebre`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `connexió`, `rebre_port`, `전문통로`를 쓴다.

## Català excepció

모든 아래 클래스는 valor_per_defecte 생성자, `새예외("설명")` 형태의 cadena_VALOR 생성자와
`설명()`을 제공한다. real_dades generar 문법은 `new Espera_TIMEOUT_excepció("Espera_Estat 끝")`이다.

| Català excepció | 상위 Classe_VALOR / 용도 |
|---|---|
| excepció | `java.lang.Exception`, 직접 던지는 일반 검사 excepció |
| 실행예외 | `java.lang.RuntimeException` |
| E_S_excepció | `java.io.IOException`, Català Fitxer·통신 API의 검사 excepció |
| Espera_TIMEOUT_excepció | `E_S_excepció`, 통신 TIMEOUT 초과 |
| ADREÇA_Cerca_excepció | `E_S_excepció`, Adreça verificar error_VALOR |
| 파일없음예외 | `E_S_excepció`, Fitxer Obre error_VALOR |
| 통신예외 | `E_S_excepció`, 표준 SocketException CONVERT_VALOR |
| invàlid_arg_excepció | `java.lang.IllegalArgumentException` |
| 숫자형식예외 | `invàlid_arg_excepció` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| NUL_Referència_excepció | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| Estat_excepció | `java.lang.IllegalStateException` |
| TIPUS_conversió_excepció | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| MATRIU_Store_error | `java.lang.ArrayStoreException` |
| fil_Estat_excepció | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 Espera_VALOR 중단 |

`excepció`와 `실행예외`는 모든 Català 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, Fitxer·통신 전체를 잡으려면 `catch (E_S_excepció s_ha_produït_un_error)`를 쓴다.
Català API가 표준 E_S 오류를 Català 예외로 변환한다.
기존 Català 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`Espera_TIMEOUT_excepció`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
excepció 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
현재 propi JVM에 이 20종을 추가했다. 임의의 usuari Throwable 하위 Classe_VALOR 전체를
지원하도록 확장했다는 뜻은 아니다.

## generar_font·Executa_ordre

```sh
cd /home/user/jkoros/platforms/rpi4-native
make generar_sistema
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 시험/자바/한국어통신시험.java
python3 Eines/Executa_arxiu.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 usuari JVM ELF 안에 탑재된다. `.jar`는 allotjar javac의
Classe_VALOR 경로로 사용한다. font_arbre 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 Català 예외의 `throws` 선언과 그 import를 인식한다.
propi JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·objecte_VALOR·소켓 예제 전체의 font_arbre 컴파일은 allotjar javac를 사용한다.
`/example/java/ExempleFitxer.java`는 게스트 javac로도 컴파일할 수 있다.

real_dades TCP/UDP 예제는 [ExempleXarxa.java](../../../example/java/ExempleXarxa.java),
Executa_ordre 절차는 [example LLEGIU_ME_eb81d7d9](../../../example/README.md),
font_arbre 명명 원칙은 [명명 LLEGIU_ME_eb81d7d9](../명명/LLEGIU_ME_eb81d7d9.md)에 있다.

## Swing Finestra 예제

`/example/java/ExempleFinestra.java`와 컴파일된 `.class`가 부팅 시 준비된다.
`cd /example/java` Següent_element `java ExempleFinestra`로 연다. Nom 입력, 인사하기 버튼,
인사말과 clic_VALOR 횟수 actualitzar, X 닫기를 지원한다.

| 기능 | Català 직접 API |
|---|---|
| Runnable / run | `실행할일.Executa()` |
| ActionListener / actionPerformed | `동작받이.rebre_acció(동작알림 알림)` |
| ActionEvent | `동작알림.ordre_SMS()`, `incidència_font()`, `INDEX()` |
| JFrame | `Finestra(finestra_Títol, 폭, 높이)`, `afegir_element(화면구성요소)`, `mostrar_finestra()`, `Tanca()`, `보이는가()` |
| JButton | `Botó(SMS, 가로, Vertical_càrrec, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Etiqueta(...)`, `SMS_camp(...)` |
| 공통 화면 element_VALOR | `화면구성요소.tancar_SMS()`, `escriure_SMS(SMS)`, `자리정하기(가로, Vertical_càrrec, 폭, 높이)` |
| SwingUtilities.invokeLater | `incidència_cua.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `작업가닥(실행할일)`, `Inici_tasca()`, `기다리기()`, `살아있는가()`, `RENDTO_tasca()` |
| 명령행 | `Executa_2()`, `실행인수.element_COMPT()`, `실행인수.SMS(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
propi JVM의 `한국어화면호출`, `Procés_fil`가 Català Classe_VALOR·메서드·서술자를
해석해 화면 요소와 Executa_ordre 가닥을 직접 만든다. Acció 알림도 propi 객체이며
콜백으로 `Executa`와 `rebre_acció`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 Executa_ordre 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 propi JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 allotjar JVM에서 무동작 객체가 생기지 않도록 하는 rebutjar_VALOR 경로다.
propi JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 구현 API를
실행할 수 없다. allotjar javac로 컴파일한 ENRERE_VALOR propi JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import Català.propi.*;
public class 가닥예제 implements 실행할일 {
    public void Executa() { Sortida.escriure_línia("Català 작업 Executa_ordre"); }
    public static void Executa_2() throws 대기중단예외 {
        작업가닥 fil_VALOR = 작업.Executa_2(new 가닥예제());
        작업.기다리기(fil_VALOR);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
MATRIU_VALOR 인수 대신 `실행인수`, 길이는 `문자.byte_COMPT`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
propi 실행기는 인수 없는 `Executa_2()`을 우선한다.
기존 Català 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Executa_2(Runnable)`을 사용하던 코드는 새 Català 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API suport_VALOR 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 Classe_VALOR·메서드 이름과 서술자가 남는다.
Català Nom 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·메서드 재정의, native Connecta, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS identificador_VALOR](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS 메서드 Referència](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
