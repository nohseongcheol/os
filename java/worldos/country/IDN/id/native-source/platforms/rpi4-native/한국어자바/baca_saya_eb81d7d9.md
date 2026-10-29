# Indonesia Java komunikasi·I_O·pengecualian API

패키지는 `Indonesia.Asli`다. host `javac --release 8`로 컴파일한 class를
Asli ARM64 커널의 JVM에서 실행한다. komunikasi·berkas·pengecualian API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 alur_VALUE API는 Asli JVM 전용이다.
기존 표준 Java pustaka 전체의 Indonesia 번역판은 아니다.

```java
import Indonesia.Asli.*;

public class jaringan {
    public static void main(String[] argumen) throws I_O_pengecualian {
        koneksi Sambung = koneksi.Buka("10.0.2.2", 9000);
        try {
            Sambung.TIMEOUT(700);
            Sambung.keluaranTeks().Tulis(문자.부호화("안녕하세요\n"));
            aliran_input 입력 = Sambung.입력();
            keluaranTeks.수쓰기(입력.Baca());
        } catch (tunggu_TIMEOUT_pengecualian galat) {
            keluaranTeks.tulis_baris(galat.설명());
        } finally {
            Sambung.Tutup();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
ruang_pengguna 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 string_VALUE 리터럴에 사용하는 표준 클래스다. Asli 실행기는 `public static void jalankan()`도 진입점으로 받는다.

## 통신과 Stream_VALUE

| Kelas_VALUE | Indonesia 호출 |
|---|---|
| koneksi | `Buka(surel, nomor_port)`, `입력()`, `keluaranTeks()`, `TIMEOUT(밀리초)`, `nomor_port()`, `lokal_nomor_port()`, `연결됨()`, `닫힘()`, `Tutup()` |
| terima_port | `Buka(nomor_port)`, `terima()`, `nomor_port()`, `TIMEOUT(밀리초)`, `닫힘()`, `Tutup()` |
| aliran_input | `Baca()`, `Baca(byte[])`, `Baca(byte[], jalankan, panjang_VALUE)`, `Tutup()` |
| aliran_output | `Tulis(int)`, `Tulis(byte[])`, `Tulis(byte[], jalankan, panjang_VALUE)`, `내보내기()`, `Tutup()` |
| 전문통로 | `Buka(nomor_port)`, `kirim(surel, nomor_port, teks)`, `terima()`, `TIMEOUT(밀리초)`, `nomor_port()`, `닫힘()`, `Tutup()` |
| 연결통신 | `Buka(...)`, `수신열기(...)`는 위 Indonesia 객체를 kembalikan_KR |
| 검사 | `참인지(kondisi, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Baca()`의 berkas 끝은 -1, ARRAY_VALUE 읽기의 반환값은 aktual_data 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. nomor_port 0은 빈 번호를 자동 배정한다.
UDP 전문은 saat_ini_item Asli 커널에서 512바이트까지 받으며, 주소는 angka_VALUE IPv4를 사용한다.
`localhost` 루프백 외의 Nama_2 풀이(DNS)는 Asli 커널에 아직 없다.

기존 `연결통신.Sambung/mendengarkan_peserta/terima`, `komunikasi.Buka/kirim/terima`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `koneksi`, `terima_port`, `전문통로`를 쓴다.

## Indonesia pengecualian

모든 아래 클래스는 nilai_default 생성자, `새예외("설명")` 형태의 string_VALUE 생성자와
`설명()`을 제공한다. aktual_data buat 문법은 `new tunggu_TIMEOUT_pengecualian("tunggu_Status 끝")`이다.

| Indonesia pengecualian | 상위 Kelas_VALUE / 용도 |
|---|---|
| pengecualian | `java.lang.Exception`, 직접 던지는 일반 검사 pengecualian |
| 실행예외 | `java.lang.RuntimeException` |
| I_O_pengecualian | `java.io.IOException`, Indonesia berkas·komunikasi API의 검사 pengecualian |
| tunggu_TIMEOUT_pengecualian | `I_O_pengecualian`, komunikasi TIMEOUT 초과 |
| surel_LOOKUP_pengecualian | `I_O_pengecualian`, surel periksa kegagalan_VALUE |
| 파일없음예외 | `I_O_pengecualian`, berkas Buka kegagalan_VALUE |
| komunikasi_pengecualian | `I_O_pengecualian`, 표준 SocketException CONVERT_VALUE |
| tidak_sahih_argumen_pengecualian | `java.lang.IllegalArgumentException` |
| 숫자형식예외 | `tidak_sahih_argumen_pengecualian` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| NULL_Referensi_pengecualian | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| Status_pengecualian | `java.lang.IllegalStateException` |
| TYPE_Transmisi_pengecualian | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| ARRAY_Store_kegagalan | `java.lang.ArrayStoreException` |
| alur_Status_pengecualian | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 tunggu_VALUE 중단 |

`pengecualian`와 `실행예외`는 모든 Indonesia 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, berkas·komunikasi 전체를 잡으려면 `catch (I_O_pengecualian galat)`를 쓴다.
Indonesia API가 표준 I_O 오류를 Indonesia 예외로 변환한다.
기존 Indonesia komunikasi 호출에서 `SocketTimeoutException`을 잡던 코드는
`tunggu_TIMEOUT_pengecualian`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
pengecualian 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
saat_ini_item Asli JVM에 이 20종을 추가했다. 임의의 ruang_pengguna Throwable 하위 Kelas_VALUE 전체를
지원하도록 확장했다는 뜻은 아니다.

## bangun_sumber·Jalankan_perintah

```sh
cd /home/user/jkoros/platforms/rpi4-native
make bangun
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 pengujian/자바/한국어통신시험.java
python3 alat/Jalankan_file.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 ruang_pengguna JVM ELF 안에 탑재된다. `.jar`는 host javac의
Kelas_VALUE 경로로 사용한다. sumber_pohon 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 Indonesia 예외의 `throws` 선언과 그 import를 인식한다.
Asli JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·objek_VALUE·소켓 예제 전체의 sumber_pohon 컴파일은 host javac를 사용한다.
`/example/java/ContohBerkas.java`는 게스트 javac로도 컴파일할 수 있다.

aktual_data TCP/UDP 예제는 [ContohJaringan.java](../../../example/java/ContohJaringan.java),
Jalankan_perintah 절차는 [example baca_saya_eb81d7d9](../../../example/README.md),
sumber_pohon 명명 원칙은 [명명 baca_saya_eb81d7d9](../명명/baca_saya_eb81d7d9.md)에 있다.

## Swing Jendela 예제

`/example/java/ContohJendela.java`와 컴파일된 `.class`가 awal_mesin 시 준비된다.
`cd /example/java` Berikutnya_item `java ContohJendela`로 연다. Nama_2 입력, 인사하기 버튼,
인사말과 klik_VALUE pengulangan_COUNT refresh, X 닫기를 지원한다.

| 기능 | Indonesia 직접 API |
|---|---|
| Runnable / run | `실행할일.Eksekusi()` |
| ActionListener / actionPerformed | `동작받이.terima_Tugas(동작알림 알림)` |
| ActionEvent | `동작알림.perintah_SMS()`, `sumber_kejadian()`, `INDEX()` |
| JFrame | `Jendela(jendela_Judul, 폭, 높이)`, `tambah_elemen(화면구성요소)`, `show_jendela()`, `Tutup()`, `보이는가()` |
| JButton | `tombol(teks, 가로, Vertikal_posisi, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Nama(...)`, `bidang_teks(...)` |
| 공통 화면 elemen_VALUE | `화면구성요소.글읽기()`, `tulis_SMS(teks)`, `자리정하기(가로, Vertikal_posisi, 폭, 높이)` |
| SwingUtilities.invokeLater | `acara_antrean.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `tugasLatar(실행할일)`, `Mulai_tugas()`, `기다리기()`, `살아있는가()`, `YIELD_tugas()` |
| 명령행 | `jalankan()`, `실행인수.item_COUNT()`, `실행인수.teks(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
Asli JVM의 `한국어화면호출`, `Proses_alur`가 Indonesia Kelas_VALUE·metode_VALUE·서술자를
해석해 화면 요소와 Jalankan_perintah 가닥을 직접 만든다. Aksi 알림도 Asli 객체이며
콜백으로 `Eksekusi`와 `terima_Tugas`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 Jalankan_perintah 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 Asli JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 host JVM에서 무동작 객체가 생기지 않도록 하는 tolak_VALUE 경로다.
Asli JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 implementasi API를
실행할 수 없다. host javac로 컴파일한 BACK_VALUE Asli JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import Indonesia.Asli.*;
public class 가닥예제 implements 실행할일 {
    public void Eksekusi() { keluaranTeks.tulis_baris("Indonesia 작업 Jalankan_perintah"); }
    public static void jalankan() throws 대기중단예외 {
        tugasLatar alur_VALUE = 작업.jalankan(new 가닥예제());
        작업.기다리기(alur_VALUE);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
ARRAY_VALUE argumen 대신 `실행인수`, 길이는 `문자.byte_COUNT`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
Asli 실행기는 argumen 없는 `jalankan()`을 우선한다.
기존 Indonesia 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.jalankan(Runnable)`을 사용하던 코드는 새 Indonesia 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API dukung_VALUE 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 Kelas_VALUE·metode_VALUE 이름과 서술자가 남는다.
Indonesia Nama_2 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·metode_VALUE 재정의, native Sambung, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS pengidentifikasi_VALUE](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS metode_VALUE Referensi](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
