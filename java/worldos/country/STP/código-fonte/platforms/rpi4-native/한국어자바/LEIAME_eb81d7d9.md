# Português Java comunicação·E_S·exceção API

패키지는 `Português.nativo`다. host `javac --release 8`로 컴파일한 class를
nativo ARM64 커널의 JVM에서 실행한다. comunicação·ficheiro·exceção API는 OpenJDK와 대조한다. 아래의 직접 구현한 tela·작업 thread_VALOR API는 nativo JVM 전용이다.
기존 표준 Java biblioteca 전체의 Português 번역판은 아니다.

```java
import Português.nativo.*;

public class rede {
    public static void main(String[] argumentos) throws E_S_exceção {
        conexão Ligar = conexão.Abrir("10.0.2.2", 9000);
        try {
            Ligar.TEMPOLIMITE(700);
            Ligar.saídaTexto().Escrita(문자.codificar("안녕하세요\n"));
            fluxo_de_entrada entrada_VALOR = Ligar.entrada_VALOR();
            saídaTexto.gravar_número(entrada_VALOR.Leitura());
        } catch (aguarde_TEMPOLIMITE_exceção erro) {
            saídaTexto.gravar_linha(erro.설명());
        } finally {
            Ligar.Fechar();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
espaço_do_utilizador 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 cadeia_VALOR 리터럴에 사용하는 표준 클래스다. nativo 실행기는 `public static void iniciar()`도 진입점으로 받는다.

## 통신과 fluxo_VALOR

| aula_VALOR | Português 호출 |
|---|---|
| conexão | `Abrir(Endereço, número_da_porta)`, `entrada_VALOR()`, `saídaTexto()`, `TEMPOLIMITE(밀리초)`, `número_da_porta()`, `local_número_da_porta()`, `연결됨()`, `TI_fechado()`, `Fechar()` |
| porta_de_recepção | `Abrir(número_da_porta)`, `receber()`, `número_da_porta()`, `TEMPOLIMITE(밀리초)`, `TI_fechado()`, `Fechar()` |
| fluxo_de_entrada | `Leitura()`, `Leitura(byte[])`, `Leitura(byte[], iniciar, duração_VALOR)`, `Fechar()` |
| fluxo_de_saída | `Escrita(int)`, `Escrita(byte[])`, `Escrita(byte[], iniciar, duração_VALOR)`, `내보내기()`, `Fechar()` |
| datagrama_Canal | `Abrir(número_da_porta)`, `enviar(Endereço, número_da_porta, texto)`, `receber()`, `TEMPOLIMITE(밀리초)`, `número_da_porta()`, `TI_fechado()`, `Fechar()` |
| conexão_transporte | `Abrir(...)`, `수신열기(...)`는 위 Português 객체를 devolver_RC |
| 검사 | `참인지(doença, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Leitura()`의 ficheiro 끝은 -1, MATRIZ_VALOR 읽기의 반환값은 real_dados 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. número_da_porta 0은 빈 번호를 자동 배정한다.
UDP 전문은 em_dia_item nativo 커널에서 512바이트까지 받으며, 주소는 dígito_VALOR IPv4를 사용한다.
`localhost` 루프백 외의 Nome 풀이(DNS)는 nativo 커널에 아직 없다.

기존 `conexão_transporte.Ligar/escutar_empresa/receber`, `comunicação.Abrir/enviar/receber`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `conexão`, `porta_de_recepção`, `datagrama_Canal`를 쓴다.

## Português exceção

모든 아래 클래스는 valor_padrão 생성자, `새예외("설명")` 형태의 cadeia_VALOR 생성자와
`설명()`을 제공한다. real_dados gerar 문법은 `new aguarde_TEMPOLIMITE_exceção("estado_de_espera 끝")`이다.

| Português exceção | 상위 aula_VALOR / 용도 |
|---|---|
| exceção | `java.lang.Exception`, 직접 던지는 일반 검사 exceção |
| execução_exceção | `java.lang.RuntimeException` |
| E_S_exceção | `java.io.IOException`, Português ficheiro·comunicação API의 검사 exceção |
| aguarde_TEMPOLIMITE_exceção | `E_S_exceção`, comunicação TEMPOLIMITE 초과 |
| email_PROC_exceção | `E_S_exceção`, Endereço verificar falha_VALOR |
| 파일없음예외 | `E_S_exceção`, ficheiro Abrir falha_VALOR |
| comunicação_exceção | `E_S_exceção`, 표준 SocketException CONVERTER_VALOR |
| inválido_argumento_exceção | `java.lang.IllegalArgumentException` |
| número_formato_falha | `inválido_argumento_exceção` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| limites_da_matriz_exceção / 문자열범위예외 | `범위예외` |
| referência_nula_exceção | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| Estado_exceção | `java.lang.IllegalStateException` |
| TIPO_coerção_exceção | `java.lang.ClassCastException` |
| negativo_MATRIZ_dimensionar_falha | `java.lang.NegativeArraySizeException` |
| MATRIZ_Store_falha | `java.lang.ArrayStoreException` |
| thread_Estado_exceção | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 aguarde_VALOR 중단 |

`exceção`와 `execução_exceção`는 모든 Português 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, ficheiro·comunicação 전체를 잡으려면 `catch (E_S_exceção erro)`를 쓴다.
Português API가 표준 E_S 오류를 Português 예외로 변환한다.
기존 Português comunicação 호출에서 `SocketTimeoutException`을 잡던 코드는
`aguarde_TEMPOLIMITE_exceção`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
exceção 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
em_dia_item nativo JVM에 이 20종을 추가했다. 임의의 espaço_do_utilizador Throwable 하위 aula_VALOR 전체를
지원하도록 확장했다는 뜻은 아니다.

## compilar_fonte·Executar_comando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make construir
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 testes/자바/한국어통신시험.java
python3 ferramentas/Executar_Arquivo.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 espaço_do_utilizador JVM ELF 안에 탑재된다. `.jar`는 host javac의
aula_VALOR 경로로 사용한다. fonte_árvore 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 Português 예외의 `throws` 선언과 그 import를 인식한다.
nativo JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·objeto_VALOR·soquete_VALOR 예제 전체의 fonte_árvore 컴파일은 host javac를 사용한다.
`/example/java/ExemploFicheiro.java`는 게스트 javac로도 컴파일할 número 있다.

real_dados TCP/UDP 예제는 [ExemploRede.java](../../../example/java/ExemploRede.java),
Executar_comando 절차는 [example LEIAME_eb81d7d9](../../../example/README.md),
fonte_árvore 명명 원칙은 [명명 LEIAME_eb81d7d9](../명명/LEIAME_eb81d7d9.md)에 있다.

## Swing Janela 예제

`/example/java/ExemploJanela.java`와 컴파일된 `.class`가 arranque_da_máquina 시 준비된다.
`cd /example/java` Avançar_item `java ExemploJanela`로 연다. Nome entrada_VALOR, 인사하기 버튼,
인사말과 clicar_VALOR repetição_CONT_NÚM renovar, X 닫기를 지원한다.

| 기능 | Português 직접 API |
|---|---|
| Runnable / run | `실행할일.Executar()` |
| ActionListener / actionPerformed | `동작받이.receber_Ação(Ação_aviso aviso)` |
| ActionEvent | `Ação_aviso.comando_SMS()`, `origem_do_evento()`, `ÍNDICE()` |
| JFrame | `Janela(janela_Título, 폭, altura_VALOR)`, `Adicionar_elemento(tela_elemento)`, `mostrar_janela()`, `Fechar()`, `보이는가()` |
| JButton | `botão(texto, 가로, Vertical_cargo, 폭, altura_VALOR, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Etiqueta(...)`, `campo_de_texto(...)` |
| 공통 tela elemento_VALOR | `tela_elemento.leitura_SMS()`, `gravar_SMS(texto)`, `자리정하기(가로, Vertical_cargo, 폭, altura_VALOR)` |
| SwingUtilities.invokeLater | `Evento_Fila.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `tarefaSegundoPlano(실행할일)`, `START_Tarefa()`, `기다리기()`, `살아있는가()`, `LUCRO_Tarefa()` |
| 명령행 | `iniciar()`, `실행인수.item_CONT_NÚM()`, `실행인수.texto(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
nativo JVM의 `한국어화면호출`, `Processo_thread`가 Português aula_VALOR·método_VALOR·서술자를
해석해 tela 요소와 Executar_comando 가닥을 직접 만든다. Acção 알림도 nativo 객체이며
콜백으로 `Executar`와 `receber_Ação`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 Executar_comando 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 nativo JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 host JVM에서 무동작 객체가 생기지 않도록 하는 rejeitar_VALOR 경로다.
nativo JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 implementação API를
실행할 número 없다. host javac로 컴파일한 BACK_VALOR nativo JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, tela 큐 기능은 `SwingUtilities`에 해당한다.

```java
import Português.nativo.*;
public class 가닥예제 implements 실행할일 {
    public void Executar() { saídaTexto.gravar_linha("Português 작업 Executar_comando"); }
    public static void iniciar() throws 대기중단예외 {
        tarefaSegundoPlano thread_VALOR = 작업.iniciar(new 가닥예제());
        작업.기다리기(thread_VALOR);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
MATRIZ_VALOR argumentos 대신 `실행인수`, 길이는 `문자.byte_CONT_NÚM`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
nativo 실행기는 argumentos 없는 `iniciar()`을 우선한다.
기존 Português tela 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.iniciar(Runnable)`을 사용하던 코드는 새 Português 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API Suporte_VALOR 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 aula_VALOR·método_VALOR 이름과 서술자가 남는다.
Português Nome 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·método_VALOR 재정의, native Ligar, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS identificador_VALOR](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS método_VALOR Referência](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
