# Melayu Java 통신·I_O·pengecualian API

패키지는 `Melayu.Asli`다. hos `javac --release 8`로 컴파일한 class를
Asli ARM64 커널의 JVM에서 실행한다. 통신·Fail·pengecualian API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 urutan_VALUE API는 Asli JVM 전용이다.
기존 표준 Java pustaka 전체의 Melayu 번역판은 아니다.

```java
import Melayu.Asli.*;

public class rangkaian {
    public static void main(String[] 인수) throws I_O_pengecualian {
        hubungan Sambung = hubungan.Buka("10.0.2.2", 9000);
        try {
            Sambung.TIMEOUT(700);
            Sambung.출력().Tulis(문자.부호화("안녕하세요\n"));
            strim_input 입력 = Sambung.입력();
            출력.수쓰기(입력.Baca());
        } catch (tunggu_TIMEOUT_pengecualian RALAT) {
            출력.tulis_baris(RALAT.설명());
        } finally {
            Sambung.Tutup();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
ruang_pengguna 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 rentetan_VALUE 리터럴에 사용하는 표준 클래스다. Asli 실행기는 `public static void Jalan()`도 진입점으로 받는다.

## 통신과 strim_VALUE

| Kelas_VALUE | Melayu 호출 |
|---|---|
| hubungan | `Buka(e_mel, nombor_port)`, `입력()`, `출력()`, `TIMEOUT(밀리초)`, `nombor_port()`, `setempat_nombor_port()`, `연결됨()`, `닫힘()`, `Tutup()` |
| 수신창구 | `Buka(nombor_port)`, `받기()`, `nombor_port()`, `TIMEOUT(밀리초)`, `닫힘()`, `Tutup()` |
| strim_input | `Baca()`, `Baca(byte[])`, `Baca(byte[], Jalan, kepanjangan_VALUE)`, `Tutup()` |
| strim_output | `Tulis(int)`, `Tulis(byte[])`, `Tulis(byte[], Jalan, kepanjangan_VALUE)`, `내보내기()`, `Tutup()` |
| 전문통로 | `Buka(nombor_port)`, `e_mel_9aee63bd(e_mel, nombor_port, Teks)`, `받기()`, `TIMEOUT(밀리초)`, `nombor_port()`, `닫힘()`, `Tutup()` |
| 연결통신 | `Buka(...)`, `수신열기(...)`는 위 Melayu 객체를 kembalikan_ukuran |
| 검사 | `참인지(syarat, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Baca()`의 Fail 끝은 -1, ARRAY_VALUE 읽기의 반환값은 sebenar_data 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. nombor_port 0은 빈 번호를 자동 배정한다.
UDP 전문은 현재 Asli 커널에서 512바이트까지 받으며, 주소는 digit_VALUE IPv4를 사용한다.
`localhost` 루프백 외의 Nama 풀이(DNS)는 Asli 커널에 아직 없다.

기존 `연결통신.Sambung/dengar_peserta/받기`, `통신.Buka/e_mel_9aee63bd/받기`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `hubungan`, `수신창구`, `전문통로`를 쓴다.

## Melayu pengecualian

모든 아래 클래스는 nilai_lalai 생성자, `새예외("설명")` 형태의 rentetan_VALUE 생성자와
`설명()`을 제공한다. sebenar_data jana 문법은 `new tunggu_TIMEOUT_pengecualian("keadaan_tunggu 끝")`이다.

| Melayu pengecualian | 상위 Kelas_VALUE / 용도 |
|---|---|
| pengecualian | `java.lang.Exception`, 직접 던지는 일반 검사 pengecualian |
| 실행예외 | `java.lang.RuntimeException` |
| I_O_pengecualian | `java.io.IOException`, Melayu Fail·통신 API의 검사 pengecualian |
| tunggu_TIMEOUT_pengecualian | `I_O_pengecualian`, 통신 TIMEOUT 초과 |
| e_mel_Carian_pengecualian | `I_O_pengecualian`, e_mel tentu_sahkan kegagalan_VALUE |
| 파일없음예외 | `I_O_pengecualian`, Fail Buka kegagalan_VALUE |
| 통신예외 | `I_O_pengecualian`, 표준 SocketException tukar_VALUE |
| tak_sah_argumen_pengecualian | `java.lang.IllegalArgumentException` |
| 숫자형식예외 | `tak_sah_argumen_pengecualian` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| rujukan_nol_pengecualian | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| status_pengecualian | `java.lang.IllegalStateException` |
| TYPE_siar_pengecualian | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| ARRAY_stor_kegagalan | `java.lang.ArrayStoreException` |
| urutan_status_pengecualian | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 tunggu_VALUE 중단 |

`pengecualian`와 `실행예외`는 모든 Melayu 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, Fail·통신 전체를 잡으려면 `catch (I_O_pengecualian RALAT)`를 쓴다.
Melayu API가 표준 I_O 오류를 Melayu 예외로 변환한다.
기존 Melayu 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`tunggu_TIMEOUT_pengecualian`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
pengecualian 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
현재 Asli JVM에 이 20종을 추가했다. 임의의 ruang_pengguna Throwable 하위 Kelas_VALUE 전체를
지원하도록 확장했다는 뜻은 아니다.

## bina_sumber·laksanakan_perintah

```sh
cd /home/user/jkoros/platforms/rpi4-native
make bina_sistem
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 ujian/자바/한국어통신시험.java
python3 alat/laksanakan_fail.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 ruang_pengguna JVM ELF 안에 탑재된다. `.jar`는 hos javac의
Kelas_VALUE 경로로 사용한다. sumber_pepohon 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 Melayu 예외의 `throws` 선언과 그 import를 인식한다.
Asli JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·objek_VALUE·소켓 예제 전체의 sumber_pepohon 컴파일은 hos javac를 사용한다.
`/example/java/ContohFail.java`는 게스트 javac로도 컴파일할 수 있다.

sebenar_data TCP/UDP 예제는 [ContohRangkaian.java](../../../example/java/ContohRangkaian.java),
laksanakan_perintah 절차는 [example README_eb81d7d9](../../../example/README.md),
sumber_pepohon 명명 원칙은 [명명 README_eb81d7d9](../명명/README_eb81d7d9.md)에 있다.

## Swing Tetingkap 예제

`/example/java/ContohTetingkap.java`와 컴파일된 `.class`가 permulaan_mesin 시 준비된다.
`cd /example/java` Seterusnya_item `java ContohTetingkap`로 연다. Nama 입력, 인사하기 버튼,
인사말과 klik_VALUE 횟수 segar_semula, X 닫기를 지원한다.

| 기능 | Melayu 직접 API |
|---|---|
| Runnable / run | `실행할일.Lakukan()` |
| ActionListener / actionPerformed | `동작받이.동작받기(동작알림 알림)` |
| ActionEvent | `동작알림.perintah_SMS()`, `sumber_peristiwa()`, `INDEX()` |
| JFrame | `Tetingkap(tetingkap_Tajuk, 폭, 높이)`, `tambah_unsur(화면구성요소)`, `tayang_tetingkap()`, `Tutup()`, `보이는가()` |
| JButton | `Butang(Teks, 가로, Menegak_jawatan, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `label(...)`, `medan_teks(...)` |
| 공통 화면 unsur_VALUE | `화면구성요소.글읽기()`, `tulis_SMS(Teks)`, `자리정하기(가로, Menegak_jawatan, 폭, 높이)` |
| SwingUtilities.invokeLater | `acara_baris.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `작업가닥(실행할일)`, `Mula_tugas()`, `기다리기()`, `살아있는가()`, `YIELD_tugas()` |
| 명령행 | `Jalan()`, `실행인수.item_COUNT()`, `실행인수.Teks(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
Asli JVM의 `한국어화면호출`, `Proses_urutan`가 Melayu Kelas_VALUE·kaedah_VALUE·서술자를
해석해 화면 요소와 laksanakan_perintah 가닥을 직접 만든다. Aksi 알림도 Asli 객체이며
콜백으로 `Lakukan`와 `동작받기`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 laksanakan_perintah 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 Asli JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 hos JVM에서 무동작 객체가 생기지 않도록 하는 tolak_VALUE 경로다.
Asli JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 pelaksanaan API를
실행할 수 없다. hos javac로 컴파일한 BACK_VALUE Asli JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import Melayu.Asli.*;
public class 가닥예제 implements 실행할일 {
    public void Lakukan() { 출력.tulis_baris("Melayu 작업 laksanakan_perintah"); }
    public static void Jalan() throws 대기중단예외 {
        작업가닥 urutan_VALUE = 작업.Jalan(new 가닥예제());
        작업.기다리기(urutan_VALUE);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
ARRAY_VALUE 인수 대신 `실행인수`, 길이는 `문자.bait_COUNT`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
Asli 실행기는 인수 없는 `Jalan()`을 우선한다.
기존 Melayu 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Jalan(Runnable)`을 사용하던 코드는 새 Melayu 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API Sokongan_VALUE 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 Kelas_VALUE·kaedah_VALUE 이름과 서술자가 남는다.
Melayu Nama 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·kaedah_VALUE 재정의, native Sambung, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS 식별자](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS kaedah_VALUE Rujukan](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
