# Italiano Java comunicazione·I_O·eccezione API

패키지는 `Italiano.nativo`다. host `javac --release 8`로 컴파일한 class를
nativo ARM64 커널의 JVM에서 실행한다. comunicazione·file·eccezione API는 OpenJDK와 대조한다. 아래의 직접 구현한 schermata·작업 thread_VALORE API는 nativo JVM 전용이다.
기존 표준 Java Catalogo 전체의 Italiano 번역판은 아니다.

```java
import Italiano.nativo.*;

public class rete {
    public static void main(String[] argomenti) throws I_O_eccezione {
        connessione Connetti = connessione.Apri("10.0.2.2", 9000);
        try {
            Connetti.TIMEOUT(700);
            Connetti.uscitaTesto().Scrittura(문자.codificare("안녕하세요\n"));
            flusso_di_input input_VALORE = Connetti.input_VALORE();
            uscitaTesto.scrivere_numero(input_VALORE.Lettura());
        } catch (aspetta_TIMEOUT_eccezione errore) {
            uscitaTesto.scrivere_riga(errore.설명());
        } finally {
            Connetti.Chiudi();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
spazio_utente 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 stringa_VALORE 리터럴에 사용하는 표준 클래스다. nativo 실행기는 `public static void avvia()`도 진입점으로 받는다.

## 통신과 Stream_VALORE

| Corso_VALORE | Italiano 호출 |
|---|---|
| connessione | `Apri(e_mail, numero_di_porta)`, `input_VALORE()`, `uscitaTesto()`, `TIMEOUT(밀리초)`, `numero_di_porta()`, `locale_numero_di_porta()`, `연결됨()`, `reparto_IT_chiusa()`, `Chiudi()` |
| porta_di_ricezione | `Apri(numero_di_porta)`, `ricevere()`, `numero_di_porta()`, `TIMEOUT(밀리초)`, `reparto_IT_chiusa()`, `Chiudi()` |
| flusso_di_input | `Lettura()`, `Lettura(byte[])`, `Lettura(byte[], avvia, durata_VALORE)`, `Chiudi()` |
| flusso_di_output | `Scrittura(int)`, `Scrittura(byte[])`, `Scrittura(byte[], avvia, durata_VALORE)`, `내보내기()`, `Chiudi()` |
| datagramma_Canale | `Apri(numero_di_porta)`, `inviare(e_mail, numero_di_porta, testo)`, `ricevere()`, `TIMEOUT(밀리초)`, `numero_di_porta()`, `reparto_IT_chiusa()`, `Chiudi()` |
| connessione_trasporto | `Apri(...)`, `수신열기(...)`는 위 Italiano 객체를 Reso_KR |
| 검사 | `참인지(condizione, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Lettura()`의 file 끝은 -1, array_VALORE 읽기의 반환값은 effettivo_dati 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. numero_di_porta 0은 빈 번호를 자동 배정한다.
UDP 전문은 Regolari_articolo nativo 커널에서 512바이트까지 받으며, 주소는 cifra_VALORE IPv4를 사용한다.
`localhost` 루프백 외의 Nome 풀이(DNS)는 nativo 커널에 아직 없다.

기존 `connessione_trasporto.Connetti/essere_in_ascolto_endpoint/ricevere`, `comunicazione.Apri/inviare/ricevere`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `connessione`, `porta_di_ricezione`, `datagramma_Canale`를 쓴다.

## Italiano eccezione

모든 아래 클래스는 valore_predefinito 생성자, `새예외("설명")` 형태의 stringa_VALORE 생성자와
`설명()`을 제공한다. effettivo_dati generare 문법은 `new aspetta_TIMEOUT_eccezione("stato_di_attesa 끝")`이다.

| Italiano eccezione | 상위 Corso_VALORE / 용도 |
|---|---|
| eccezione | `java.lang.Exception`, 직접 던지는 일반 검사 eccezione |
| esecuzione_eccezione | `java.lang.RuntimeException` |
| I_O_eccezione | `java.io.IOException`, Italiano file·comunicazione API의 검사 eccezione |
| aspetta_TIMEOUT_eccezione | `I_O_eccezione`, comunicazione TIMEOUT 초과 |
| e_mail_CERCA_eccezione | `I_O_eccezione`, e_mail verificare errore_VALORE |
| 파일없음예외 | `I_O_eccezione`, file Apri errore_VALORE |
| comunicazione_eccezione | `I_O_eccezione`, 표준 SocketException CONVERTI_VALORE |
| non_valida_argomento_eccezione | `java.lang.IllegalArgumentException` |
| numero_formato_errore | `non_valida_argomento_eccezione` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| riferimento_Null_eccezione | `java.lang.NullPointerException` |
| aritmetico_errore | `java.lang.ArithmeticException` |
| Stato_eccezione | `java.lang.IllegalStateException` |
| TIPO_cast_eccezione | `java.lang.ClassCastException` |
| negativo_array_ridimensionare_errore | `java.lang.NegativeArraySizeException` |
| array_Store_errore | `java.lang.ArrayStoreException` |
| thread_Stato_eccezione | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 aspetta_VALORE 중단 |

`eccezione`와 `esecuzione_eccezione`는 모든 Italiano 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, file·comunicazione 전체를 잡으려면 `catch (I_O_eccezione errore)`를 쓴다.
Italiano API가 표준 I_O 오류를 Italiano 예외로 변환한다.
기존 Italiano comunicazione 호출에서 `SocketTimeoutException`을 잡던 코드는
`aspetta_TIMEOUT_eccezione`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
eccezione 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
Regolari_articolo nativo JVM에 이 20종을 추가했다. 임의의 spazio_utente Throwable 하위 Corso_VALORE 전체를
지원하도록 확장했다는 뜻은 아니다.

## compilare_fonte·Esegui_comando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make costruire
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 prove/자바/한국어통신시험.java
python3 strumenti/Esegui_File.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 spazio_utente JVM ELF 안에 탑재된다. `.jar`는 host javac의
Corso_VALORE 경로로 사용한다. fonte_albero 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 Italiano 예외의 `throws` 선언과 그 import를 인식한다.
nativo JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·oggetto_VALORE·socket_VALORE 예제 전체의 fonte_albero 컴파일은 host javac를 사용한다.
`/example/java/EsempioFile.java`는 게스트 javac로도 컴파일할 numero 있다.

effettivo_dati TCP/UDP 예제는 [EsempioRete.java](../../../example/java/EsempioRete.java),
Esegui_comando 절차는 [example README_eb81d7d9](../../../example/README.md),
fonte_albero 명명 원칙은 [명명 README_eb81d7d9](../명명/README_eb81d7d9.md)에 있다.

## Swing Finestra 예제

`/example/java/EsempioFinestra.java`와 컴파일된 `.class`가 avvio_macchina 시 준비된다.
`cd /example/java` Avanti_articolo `java EsempioFinestra`로 연다. Nome input_VALORE, 인사하기 버튼,
인사말과 clic_VALORE ripetizione_CONTA_NUMERI aggiornare, X 닫기를 지원한다.

| 기능 | Italiano 직접 API |
|---|---|
| Runnable / run | `실행할일.Esegui()` |
| ActionListener / actionPerformed | `동작받이.ricevere_Action(Action_informativa informativa)` |
| ActionEvent | `Action_informativa.comando_SMS()`, `origine_evento()`, `INDICE()` |
| JFrame | `Finestra(finestra_titolo, 폭, altezza_VALORE)`, `Aggiungi_elemento(schermata_elemento)`, `mostrare_finestra()`, `Chiudi()`, `보이는가()` |
| JButton | `pulsante(testo, 가로, Verticale_funzione, 폭, altezza_VALORE, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Etichetta(...)`, `campo_di_testo(...)` |
| 공통 schermata elemento_VALORE | `schermata_elemento.글읽기()`, `scrivere_SMS(testo)`, `자리정하기(가로, Verticale_funzione, 폭, altezza_VALORE)` |
| SwingUtilities.invokeLater | `evento_coda.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `esecutoreAsincrono(실행할일)`, `START_task()`, `기다리기()`, `살아있는가()`, `REND_task()` |
| 명령행 | `avvia()`, `실행인수.articolo_CONTA_NUMERI()`, `실행인수.testo(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
nativo JVM의 `한국어화면호출`, `Processi_thread`가 Italiano Corso_VALORE·metodo_VALORE·서술자를
해석해 schermata 요소와 Esegui_comando 가닥을 직접 만든다. Azione 알림도 nativo 객체이며
콜백으로 `Esegui`와 `ricevere_Action`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 Esegui_comando 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 nativo JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 host JVM에서 무동작 객체가 생기지 않도록 하는 rifiutare_VALORE 경로다.
nativo JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 implementazione API를
실행할 numero 없다. host javac로 컴파일한 BACK_VALORE nativo JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, schermata 큐 기능은 `SwingUtilities`에 해당한다.

```java
import Italiano.nativo.*;
public class 가닥예제 implements 실행할일 {
    public void Esegui() { uscitaTesto.scrivere_riga("Italiano 작업 Esegui_comando"); }
    public static void avvia() throws 대기중단예외 {
        esecutoreAsincrono thread_VALORE = 작업.avvia(new 가닥예제());
        작업.기다리기(thread_VALORE);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
array_VALORE argomenti 대신 `실행인수`, 길이는 `문자.byte_CONTA_NUMERI`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
nativo 실행기는 argomenti 없는 `avvia()`을 우선한다.
기존 Italiano schermata 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.avvia(Runnable)`을 사용하던 코드는 새 Italiano 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API Supporto_VALORE 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 Corso_VALORE·metodo_VALORE 이름과 서술자가 남는다.
Italiano Nome 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·metodo_VALORE 재정의, native Connetti, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS identificatore_VALORE](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS metodo_VALORE fonti](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
