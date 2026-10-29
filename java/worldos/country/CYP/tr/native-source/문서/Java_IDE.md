# jkoros 안에서 Java derlemek_kaynak·yürütmek_komut

이 문서의 makine_başlatma·kabuk·depo_değer 명령은 **x86 sürüm_değer** 기준이다. 공유 Java derleyici/JVM은 [Öz ARM64 Pi4 sürüm_değer](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART artış_değer·한글 dosya_adı_SMS, `edit`의 단독 `.` depo_değer, 16개 RAM dosya, 약 2초 yürütmek_komut 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 fiili_veri JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. konak derlemek_kaynak 서버나 Linux 게스트는 사용하지 않는다.

**geçerli_öğe 구현은 Öz 제한형 derleyici·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java program_f5044b9b 실행은 아직 지원하지 않는다.

## 바로 yürütmek_komut

호스트에서:

```sh
cd /home/user/jkoros
make iso
make run
```

게스트에서:

```text
jkoros> javac -version
jkoros> java -version
jkoros> ls
jkoros> cat Hello.java
jkoros> javac Hello.java
Compiled: Hello.class (JVM class version 49)
Exit: 0
jkoros> java Hello
Hello from jkoros JVM!
55
Exit: 0
```

ISO는 `os/build/kernel.iso`다. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. yürütmek_komut 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 makine_başlatma 절차는 [VirtualBox yürütmek_komut 안내](가상상자실행.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 dosya 전체를 새 내용으로 작성한다. 기존 내용의 girdi_satırı Düzenle_değer 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

```text
jkoros> edit Demo.java
...> public class Demo {
...>  public static int square(int n) { return n * n; }
...>  public static void main(String[] args) {
...>   int n = Integer.parseInt(args[0]);
...>   System.out.println("square=" + square(n));
...>  }
...> }
...> .save
jkoros> javac Demo.java
jkoros> java Demo 12
square=144
Exit: 0
```

- `ls`: 파일과 bayt_değer 수 şov_değer.
- `cat FILE`: dosya içerik_değer şov_değer. 텍스트 소스에 사용한다.
- `rm FILE`: Bellek_veri dosya 삭제.
- `edit FILE`: 전체 내용을 새로 artış_değer. 빈 파일도 저장할 수 있다.
- 구문·TÜR_değer 검사 hata_değer 시 기존 `.class`는 유지된다. 소스를 고친 BACK_değer 컴파일이 실패했다면 Önceki_öğe yürütmek_komut 파일이 남아 있으므로 derlemek_kaynak 성공 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 depo_değer 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 kaynak_ağaç·Sınıf_değer·veri 파일을 보존할 수 있다. 최대 8개, 파일마다 16KiB, dosya 이름은 ASCII 1~63자다. kaynak_ağaç 이름은 `.class` 확장자 ADRES_bölge 때문에 최대 62자다. Düzenle_değer 입력은 ASCII이고 한 girdi_satırı 최대 128자다. girdi_satırı 또는 dosya 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. çekirdek_değer/derleyici/JVM 구현의 Java 식별자는 한국어이며, geçerli_öğe 게스트 artış_değer 제한 때문에 kullanıcı_alanı 예제 이름은 ASCII로 작성한다.

## dış_değer dosya 적재

호스트에서 만든 소스나 Destek_değer klip 안의 `.class`를 makine_başlatma 이미지에 포함할 수 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 fiili_veri 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# konak JDK로 컴파일한 클래스도 사용할 수 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 makine_başlatma 후 `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 Sonraki_öğe 빌드에서는 Ekleme_girdi 파일을 포함하지 않는다. dosya içerik_değer 변경과 girdi_Liste 제거도 Sonraki_öğe 빌드에 반영된다. 원본 konak 파일에는 쓰지 않는다. varsayılan_değer `Hello.java`까지 합해 8개이며, 같은 이름을 명시하면 varsayılan_değer 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 Sınıf_değer dosya 버전을 맞추는 옵션이다. 사용하는 문법·바이트코드·라이브러리도 아래 Destek_değer klip 안에 있어야 한다.

## Destek_değer klip

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| Sınıf_değer | 패키지 없는 단일 Sınıf_değer, statik_değer işlev_değer, 재귀, bağımsız_değişkenler/İade_KR | 실행마다 단일 Sınıf_değer 적재, public static main(String[]) |
| varsayılan_değer değer | int, boolean, char, String, main의 String[] bağımsız_değişkenler | bilgi·Başvuru işlenen_Yığın, String, int[], String[], 내부 StringBuilder |
| deyim_değer | 초기값 있는 yerel_Scope bildirim, ödev_değer, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 bilgi·Başvuru 바이트코드와 koşul dal |
| ifade_değer | 십진 bilgi, UTF-8 소스의 dize_değer/문자, + - * / %, 비교, ==/!=, !/&&/\|\|, dize_değer 결합 | bilgi işlem_değer_c96707fb·bit_değer işlem_değer_c96707fb·TÜR_değer ÇEVİR_değer, 단락 평가, DİZİ_değer erişim_girdi |
| dosya | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | fiili_veri çekirdek_değer 파일서술자와 Bağlan, oluşturmak·takas_içindekiler·이어쓰기·EOF |
| metinÇıktısı | System.out.print/println: int/boolean/char/String, println() | 동일 |
| dize_değer/bağımsız_değişkenler | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), dize_değer 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, 초기값 없는 yerel_Scope bildirim, 오버로드, 임의 TÜR_değer ÇEVİR_değer, DİZİ_değer oluşturmak kaynakKod, 8/16진 리터럴, Unicode kaynak_ağaç 이스케이프 등은 미지원이다. `char`는 문자 리터럴로 초기화하며 일반 JDK의 모든 sabit_değer 축소 변환을 구현하지 않는다. dış_değer `.class`의 `int[]` oluşturmak/Okuma/쓰기는 지원하므로 konak `javac --release 8`로 만든 DİZİ_değer 예제는 실행할 수 있다.

nesne_değer alan_değeri·일반 nesne_değer oluşturmak·상속·인터페이스·여러 Sınıf_değer Bağlan, long/float/double, özel_durum işlem_değer_girdi, 스레드·모니터, 리플렉션, JNI, JIT, GC, 위 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java özel_durum 객체를 던지지 않고 진단 후 geçerli_öğe 프로그램을 종료한다. 객체와 dize_değer depo_değer 공간은 yürütmek_komut Çıkış_program 시 kullanıcı_alanı bölge_değer 전체와 함께 회수한다. 지속 yürütmek_komut 중 GC는 없다.

## yürütmek_komut 한도와 hata

| kaynak_değer | 한도 |
| --- | --- |
| kaynak_ağaç/Sınıf_değer dosya | 각각 16KiB |
| derleyici | belirteç_değer 2,047개, oluşturmak KOD_değer 4KiB, sabit_değer 풀 4KiB |
| işlev_değer/bağımsız_değişkenler | 클래스당 32함수, 함수당 16인수 |
| JVM sabit_değer | 511개 |
| JVM işlev_değer KOD_değer | 함수당 8KiB |
| JVM 호출/işlenen_Yığın/yerel_Scope değişken_değer | 32프레임, 프레임당 işlenen_Yığın 128칸·yerel_Scope 128칸 |
| JVM nesne_değer depo_değer ADRES_bölge | 8,192개 32비트 yuva_girdi, 헤더 bildirimler 약 32KiB |
| yürütmek_komut | 최대 500,000 komut, 기존 커널의 약 3초 CPU yürütmek_komut 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 Destek_değer 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM sözlük 검증기를 구현한 것은 아니다. dosya/öznitelik_değer süre_değer, sabit_değer Başvuru, komut·dal 경계를 검사하고, yürütmek_komut 중 işlenen_Yığın biçim_değer·yerel_Scope başlat·DİZİ_değer alt_simge_değer·nesne_değer 참조를 검사한다. kullanıcı_alanı 코드의 페이지·donanım_taşımak 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, derlemek_kaynak·JVM 오류는 `Exit: 1`, komut bağımsız_değişkenler 오류는 `Exit: 2`다. CPU zaman_değeri 상한은 기존 `Exit: 124`이며, kullanıcı_alanı ELF 자체의 CPU/런타임 오류는 기존 Çıkış_program 코드를 따른다. hata_değer 후 셸에서 다른 프로그램을 계속 실행할 수 있다.

## gerçekleme 위치와 sınamalar

- `os/kullanıcı_alanı/자바/자바컴파일러.java`: 게스트 어휘·구문·TÜR_değer 검사, sabit_değer 풀 및 바이트코드 oluşturmak.
- `os/kullanıcı_alanı/자바/자바가상기계.java`: Sınıf_değer 적재, işlenen_Yığın·프레임·nesne_değer depo_değer, komut 해석과 제한된 표준 호출.
- `os/kaynakKod/Bellek_dosya_sistemi.java`: Bellek_veri dosya_sistemi, Düzenle_değer, makine_başlatma dosya 적재.
- `os/kaynakKod/sistem_çağrısı.java`, `compiler/Start_kullanıcı_program.s`: dosya/문자 metinÇıktısı API와 kullanıcı_alanı işaretçi 검사.
- `os/araçlar/자바파일묶기.py`: konak artış_değer dosya doğrulamak_5fb2b747·makine_başlatma Grup_değer oluşturmak.

```sh
make test-java
make test
```

`os/sınamalar/자바시험.py`는 ELF/ISO makine_başlatma, 게스트 derlemek_kaynak·yürütmek_komut, kullanıcı_alanı artış_değer, 재귀·반복문·bilgi 극값·dize_değer 결합·단락 평가, 재실행, kaynak_ağaç hata 후 기존 Sınıf_değer 보존, DİZİ_değer/수 해독 hata, 무한 öğe_değer_58902391 제한, Düzenle_değer 넘침과 dosya 부족을 검사한다. 게스트 oluşturmak 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 konak OpenJDK의 Sınıf_değer, bilgi 배열과 한글 상수를 게스트에 적재하며, 손상된 dosya işaret_değer·버전·sabit_değer 수·dal·스택을 거부하는지도 검사한다. 기록은 `os/build/자바시험.json`에 남는다. 디스크 없는 별도 sınamalar VM만 생성하고 종료한다.

gerçekleme 형식의 참고 veri: Oracle [JVM Sınıf_değer dosya 명세](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM komut 명세](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java dosya G_Ç

[FileDemo.java](../posix-kor/자바예제/FileDemo.java)는 일반 Java 표준 Sınıf_değer 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 makine_başlatma 이미지에 넣은 BACK_değer `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`다. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. varsayılan_değer metinÇıktısı 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. özel_durum nesne_değer·try/catch·try-with-resources는 지원하지 않으며 dosya 오류를 진단하고 프로그램을 종료한다. DİZİ_değer G_Ç, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 dosya 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 kabuk `sync`가 필요하다. 예제의 dosya 이름은 geçerli_öğe 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/sınamalar/자바파일시험.py`는 fiili_veri 게스트 derlemek_kaynak 결과를 OpenJDK `-Xverify:all`로 yeniden_denemek_değer 실행해 dosya 바이트와 출력을 대조한다. 범위와 depo_değer Medya_değer 사용법은 [posix-kor 안내](../posix-kor/안내.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
