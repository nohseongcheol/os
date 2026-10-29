# jkoros 안에서 Java ソースコンパイル·命令実行

이 문서의 起動·シェル·格納値 명령은 **x86 版値** 기준이다. 공유 Java コンパイラ/JVM은 [内蔵 ARM64 Pi4 版値](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART 入力値·ハングル文字列 ファイル名前本文, `edit`의 단독 `.` 格納値, 16개 RAM ファイル, 약 2초 命令実行 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 実際データ JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. ホスト ソースコンパイル 서버나 Linux 게스트는 사용하지 않는다.

**現在項目 구현은 内蔵 제한형 コンパイラ·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java プログラム 실행은 아직 지원하지 않는다.

## 바로 命令実行

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

ISO는 `os/build/kernel.iso`第三被演算子. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. 命令実行 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 起動 절차는 [VirtualBox 命令実行 案内](VirtualBox実行.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 ファイル 전체를 새 내용으로 작성한다. 기존 내용의 行 編集値 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

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

- `ls`: 파일과 バイト値 数 値表示.
- `cat FILE`: ファイル 内容物値 値表示. 텍스트 소스에 사용한다.
- `rm FILE`: 記憶データ ファイル 삭제.
- `edit FILE`: 전체 내용을 새로 入力値. 빈 파일도 저장할 数 있다.
- 구문·型値 検査項目 失敗値 시 기존 `.class`는 유지된다. 소스를 고친 後端値 컴파일이 실패했다면 前回項目 命令実行 파일이 남아 있으므로 ソースコンパイル 成功値 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 格納値 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 ソース木·クラス値·データ 파일을 보존할 数 있다. 最大値 8개, 파일마다 16KiB, ファイル 이름은 ASCII 1~63자다. ソース木 이름은 `.class` 확장자 番地領域 때문에 最大値 62자다. 編集値 입력은 ASCII이고 한 行 最大値 128자다. 行 또는 ファイル 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. 中核値/コンパイラ/JVM 구현의 Java 식별자는 한국어이며, 現在項目 게스트 入力値 上限値 때문에 利用者 用例 이름은 ASCII로 작성한다.

## 外部値 ファイル 적재

호스트에서 만든 소스나 支援値 切抜き 안의 `.class`를 起動 이미지에 포함할 数 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 実際データ 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# ホスト JDK로 컴파일한 클래스도 사용할 数 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 起動 後続側状況 `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 次回項目 빌드에서는 入口追記 파일을 포함하지 않는다. ファイル 内容物値 변경과 入口一覧 제거도 次回項目 빌드에 반영된다. 原本 ホスト 파일에는 쓰지 않는다. 既定値 `Hello.java`到達待ち 합해 8개이며, 같은 이름을 명시하면 既定値 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 クラス値 ファイル 버전을 맞추는 옵션이다. 사용하는 문법·バイトコード·라이브러리도 下端値 支援値 切抜き 안에 있어야 한다.

## 支援値 切抜き

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| クラス値 | 패키지 없는 단일 クラス値, 静的値 関数, 재귀, 引数/復帰結果 | 실행마다 단일 クラス値 적재, public static main(String[]) |
| 既定値 値 | int, boolean, char, String, main의 String[] 引数 | 整数値·参照 被演算子スタック, String, int[], String[], 내부 StringBuilder |
| 文値 | 初期値 있는 局所有効範囲 宣言, 代入状態値, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 整数値·参照 바이트코드와 条件 分岐 |
| 式値 | 십진 整数値, UTF-8 소스의 文字列/文字, + - * / %, 비교, ==/!=, !/&&/\|\|, 文字列 結合処理値一覧 | 整数値 操作値·ビット値 操作値·型値 値変換, 단락 평가, 配列値 アクセス入口 |
| ファイル | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | 実際データ 中核値 파일서술자와 接続, 生成·内容消去·継続状態追記·EOF |
| 出力 | System.out.print/println: int/boolean/char/String, println() | 동일 |
| 文字列/引数 | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), 文字列 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, 初期値 없는 局所有効範囲 宣言, 오버로드, 임의 型値 値変換, 配列値 生成 ソース, 8/16진 리터럴, Unicode ソース木 이스케이프 등은 미지원이다. `char`는 文字 리터럴로 초기화하며 일반 JDK의 모든 定数値 축소 변환을 구현하지 않는다. 外部値 `.class`의 `int[]` 生成/読取/쓰기는 지원하므로 ホスト `javac --release 8`로 만든 配列値 예제는 실행할 数 있다.

オブジェクト値 フィールド値·일반 オブジェクト値 生成·상속·인터페이스·여러 クラス値 接続, long/float/double, 例外 プロセス値入口, 스레드·모니터, 리플렉션, JNI, JIT, GC, 上端値 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java 例外 객체를 던지지 않고 診断値 後続側状況 現在項目 프로그램을 종료한다. 객체와 文字列 格納値 공간은 命令実行 終了点プログラム 시 利用者 領域値 전체와 함께 회수한다. 지속 命令実行 중 GC는 없다.

## 命令実行 한도와 エラー

| 資源値 | 容積上限 |
| --- | --- |
| ソース木/クラス値 ファイル | 각각 16KiB |
| コンパイラ | トークン値 2,047개, 生成 コード値 4KiB, 定数値 풀 4KiB |
| 関数/引数 | 클래스당 32함수, 함수당 16인수 |
| JVM 定数値 | 511개 |
| JVM 関数 コード値 | 함수당 8KiB |
| JVM 呼出/被演算子スタック/局所有効範囲 変数値 | 32프레임, 프레임당 被演算子スタック 128칸·局所有効範囲 128칸 |
| JVM オブジェクト値 格納値 番地領域 | 8,192개 32비트 槽入口, 헤더 ヘッダー 약 32KiB |
| 命令実行 | 最大値 500,000 命令, 기존 커널의 약 3초 CPU 命令実行 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 支援値 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM 辞書 검증기를 구현한 것은 아니다. ファイル/属性値 長さ, 定数値 参照, 命令·分岐 경계를 검사하고, 命令実行 중 被演算子スタック 書式値·局所有効範囲 初期化·配列値 添え字値·オブジェクト値 참조를 검사한다. 利用者 코드의 페이지·機器ポート 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, ソースコンパイル·JVM 오류는 `Exit: 1`, 命令 引数 오류는 `Exit: 2`第三被演算子. CPU 時間値 상한은 기존 `Exit: 124`이며, 利用者 ELF 자체의 CPU/런타임 오류는 기존 終了点プログラム 코드를 따른다. 失敗値 後続側状況 셸에서 다른 프로그램을 継続処理工程 실행할 数 있다.

## 実装 위치와 試験

- `os/利用者/Java/Javaコンパイラ.java`: 게스트 어휘·구문·型値 検査項目, 定数値 풀 및 バイトコード 生成.
- `os/利用者/Java/Java仮想機械.java`: クラス値 적재, 被演算子スタック·프레임·オブジェクト値 格納値, 命令 해석과 제한된 표준 呼出.
- `os/ソース/主記憶ファイル体系.java`: 記憶データ ファイルシステム, 編集値, 起動 ファイル 적재.
- `os/ソース/システム呼出.java`, `compiler/利用者プログラム開始処理.s`: ファイル/文字 出力 API와 利用者 ポインタ 検査項目.
- `os/道具/Javaファイル梱包.py`: ホスト 入力値 ファイル 妥当性検査·起動 集合値 生成.

```sh
make test-java
make test
```

`os/試験/Java試験.py`는 ELF/ISO 起動, 게스트 ソースコンパイル·命令実行, 利用者 入力値, 재귀·반복문·整数値 극값·文字列 結合処理値一覧·단락 평가, 재실행, ソース木 エラー 後続側状況 기존 クラス値 보존, 配列値/数 해독 エラー, 무한 反復回値 上限値, 編集値 넘침과 ファイル 부족을 검사한다. 게스트 生成 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 ホスト OpenJDK의 クラス値, 整数値 배열과 ハングル文字列 상수를 게스트에 적재하며, 손상된 ファイル 標識値·버전·定数値 数·分岐·스택을 거부하는지도 검사한다. 기록은 `os/build/Java試験.json`에 남는다. 디스크 없는 별도 試験 VM만 생성하고 종료한다.

実装 형식의 참고 データ: Oracle [JVM クラス値 ファイル 仕様](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM 命令 仕様](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java ファイル 入力出力

[FileDemo.java](../posix-kor/Java例/FileDemo.java)는 일반 Java 표준 クラス値 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 起動 이미지에 넣은 後端値 `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`第三被演算子. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. 既定値 出力 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. 例外 オブジェクト値·try/catch·try-with-resources는 지원하지 않으며 ファイル 오류를 진단하고 프로그램을 종료한다. 配列値 入力出力, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 ファイル 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 シェル `sync`先頭位置被演算子 필요하다. 예제의 ファイル 이름은 現在項目 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/試験/Javaファイル試験.py`는 実際データ 게스트 ソースコンパイル 결과를 OpenJDK `-Xverify:all`로 再試行処理値 실행해 ファイル 바이트와 출력을 대조한다. 범위와 格納値 媒体値 사용법은 [posix-kor 案内](../posix-kor/案内.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
