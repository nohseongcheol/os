# 内蔵 ARM64 JVM 0.4와 日本語 ライブラリ

日本語 通信·例外 사용법은 [日本語 Java API](日本語Java/案内.md), 関数·変数値·ファイル 이름의 변경과 어원 근거는 [命名 案内](命名/案内.md)를 참고한다.

JAR 命令実行, 外部値 IPv4 TCP/UDP, 별도 静的値 부분집합 `jaot`와 게스트 C 컴파일은 [FTP·C·JAR·AOT 매뉴얼](ファイル転送論理積翻訳工程.md)에 설명한다. 下端値 オブジェクト値·Thread·Swing은 JVM 경로의 기능이며 AOT 支援値 범위와 같지 않다.

이 구현은 **Linux 없이 부팅한 Java AOT 커널의 EL0에서 命令実行**한다. JDK/JRE의 거의 모든 기능을 제공하는 단계는 아직 아니다. HotSpot·OpenJDK クラス値 ライブラリ 전체를 이식하거나 Java SE 인증/TCK를 통과한 구현도 아니다. 이번 확장은 단일 クラス値·静的値 メソッド値 중심이던 실행기를 オブジェクト値·ライブラリ 命令実行 기반으로 넓힌 것이다.

## 실행과 ソースコンパイル

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
# 内蔵 中核値 안에서 ソース木 ソースコンパイル → class 命令実行, 日本語 API 呼出
python3 道具/ファイル実行.py 試験/Java/ハングルソース.java

# オブジェクト値·例外 등은 ホスト JDK로 Java 8 class를 만든 後続側状況 内蔵 커널에서 命令実行
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java 試験/Java/ハングル試験.java
python3 道具/ファイル実行.py build/my-java/ハングル試験.class

# 의존 class 파일은 --include로 함께 転送値
javac --release 8 -encoding UTF-8 -d build/my-java 試験/Java/オブジェクト群試験.java
python3 道具/ファイル実行.py build/my-java/オブジェクト群試験.class \
  --include build/my-java/背景値.class --include build/my-java/分岐値.class \
  --include build/my-java/可能判定計算.class

make test-jvm
```

`--include DIR`는 그 디렉터리의 class 파일을 재귀적으로 읽어 `패키지.クラス値.class`라는 RAM ファイル 이름으로 전송한다. 주 클래스도 패키지가 있다면 `--class-name 패키지.クラス値`를 지정한다. 셸에서는 해당 이름으로 업로드하고 `java 패키지.クラス値`로 실행한다. JVM 0.4는 Main-Class가 있는 16 KiB 이하 JAR도 `java -jar ファイル.jar`로 실행한다. JAR 모드에서는 JAR 내부 클래스와 내장 日本語 클래스만 찾는다. 配布値 日本語 ライブラリ JAR는 ホスト javac의 classpath로 사용하며, 같은 클래스가 利用者 JVM ELF에도 読取 전용 자료로 포함된다. 일반 class 모드에서는 사용자가 같은 이름으로 올린 RAM class를 먼저 읽는다.

게스트 `javac`는 여전히 静的値 メソッド値, int/boolean/char/String, 条件·反復回値, 文字列 結合処理値一覧, 일부 ファイル 스트림 등의 **内蔵 부분집합 コンパイラ**第三被演算子. オブジェクト値 宣言·상속·try/catch·Thread 使用値 소스를 게스트 javac가 全体構築 컴파일하는 것은 아니다. 上端値 기능은 `javac --release 8`로 만든 class를 内蔵 JVM에서 실행한다. 日本語 API 중 出力·文字 스칼라 関数·ファイル 読取/쓰기는 게스트 컴파일러에도 연결했다. 다음처럼 전체 이름으로 호출한다.

```java
public class 挨拶例 {
    public static void main(String[] 引数) throws Exception {
        日本語.内蔵.出力.行書込("안녕하세요😀");
        日本語.内蔵.出力.番号書込(日本語.内蔵.文字.コード点個数("ハングル文字列😀"));
        日本語.内蔵.ファイル.書込("挨拶例.txt", "ハングル文字列 ファイル😀");
        日本語.内蔵.出力.行書込(日本語.内蔵.ファイル.読取("挨拶例.txt"));
    }
}
```

## 内蔵 JVM에서 구현한 切抜き

| 領域値 | 제공 切抜き |
|---|---|
| クラス値 | class 버전 45…52, 여러 クラス値 로딩, 인스턴스/静的値 フィールド値, 생성자, 상속, 가상 呼出, 인터페이스 呼出, 静的値 初期化 |
| 値·命令 | 32비트 int 계열, boolean/byte/char/short, 参照, 1차원 配列値, 分岐·switch·wide, instanceof/checkcast, category-1 被演算子スタック 命令 |
| 例外 | 지원하는 표준 例外 生成·throw·catch·finally, メソッド値 경계를 넘는 前方値, getMessage; 下端値 上限値 参照 |
| 記憶データ | 비이동 mark/sweep GC, 빈 領域値 병합, 被演算子スタック·静的値 フィールド値·컬렉션·スレッド値·모니터·文字列 상수의 参照 値維持 |
| 文字列 | UTF-16, length/charAt/equals/isEmpty/substring/concat/hashCode/toString, String.valueOf(int), StringBuilder의 既定値 生成·append(int/boolean/char/String)·toString |
| 数 | Integer.parseInt/valueOf/intValue/toString, 작은 Integer 캐시, Math.abs/min/max(int) |
| 표준 出力 | System.out/err, PrintStream.print/println의 int/boolean/char/String 및 빈 println |
| 配列値 | int/byte/boolean/char/short/参照 配列値, 長さ·切抜き 検査項目, 参照 配列値 項目要素 型値 検査項目, System.arraycopy의 重複範囲/切抜き/項目要素 型値 検査項目 |
| ファイル | FileInputStream(String), FileOutputStream(String[,boolean]); read()/read(byte[][,offset,len]), write(int)/write(byte[][,offset,len]), close, 出力 flush. EOF는 -1 |
| 컬렉션 | ArrayList/List: add(E), get, set, remove(int), size, isEmpty, clear. HashMap/Map: put/get/remove/containsKey/size/isEmpty/clear |
| スレッド値 | Thread(), Thread(Runnable), Thread 상속, start/join/isAlive/currentThread/yield; synchronized メソッド値·블록의 재진입·경합·例外 시 記憶装置解放 |
| UDP | DatagramSocket의 既定値/機器ポート 생성자, send/receive/close/getLocalPort/setSoTimeout; DatagramPacket의 byte[]/長さ 生成 및 番地·機器ポート ヘッダー 生成, getData/getLength/getAddress/getPort/setLength |
| 番地 | InetAddress.getByName은 localhost/桁値 IPv4 (DNS 判定未対応), getLoopbackAddress/getHostAddress |
| 描画 | 日本語 画面 API가 EL0 SVC를 통해 프레임버퍼에 사각형을 描画; 切抜き 検査項目 |

컬렉션은 지정한 메서드만 제공하며 iterator/stream/整列値·利用者 定義値 equals/hashCode 콜백은 없다. 사전의 열쇠는 String/Integer/null 사용을 시험했다. UTF-16 コード値 단위와 Unicode コード値 포인트 수는 구분한다. ハングル文字列 入力値 組合せ·値正規化·아랍어 조판·GUI 다국어 글꼴은 이 文字列 지원과 별개다.

예외는 Throwable/Exception/RuntimeException, ArithmeticException, NullPointerException, IndexOutOfBoundsException/ArrayIndexOutOfBoundsException/StringIndexOutOfBoundsException, IllegalArgumentException/NumberFormatException/IllegalThreadStateException, IOException/FileNotFoundException, IllegalStateException, ClassCastException, NegativeArraySizeException, ArrayStoreException, UnknownHostException, SocketTimeoutException의 제한된 生成·分類値·처리를 제공한다. 利用者 定義値 Throwable 상속, stack trace/cause/suppressed 例外, try-with-resources의 addSuppressed, 완전한 初期化 エラー 포장은 아직 없다. 잡히지 않은 예외는 現在項目 전체 Java 실행을 실패로 끝낸다.

## 日本語 API

독립 패키지 **`日本語.内蔵`**를 사용한다. Linux판 `日本語.Java`先頭位置被演算子 요구하는 NIO/Swing/HTTP API를 内蔵 커널에서 실행할 数 있다고 혼동하지 않도록 패키지를 나눴다. 이 라이브러리는 クラス値 名前·メソッド値·引数·フィールド値·ファイル 이름에 한국어를 사용한다. 표준 Java クラス値 이름은 호환성을 위해 보존한다.

| クラス値 | 공개 기능 | 이름의 의미 |
|---|---|---|
| 出力 | 書込, 行書込, 番号書込 | 出力(出力): 내용을 바깥으로 公開済み値 |
| 文字 | 長さ, 等価本文, 貼付け本文, 切断処理値, 整数値解析/整数値値書込, コード点個数, 符号化/データ復号化 | 文字(文字), 符号化状態値(符號): 글의 단위와 그 값을 바이트로 나타내는 規則値 |
| ファイル | 読取/書込(String 名前), バイト値読取/バイト値書込 | 널리 쓰는 利用者 용어를 보존; RAM 자료의 名前 |
| 入口一覧 | 値一覧追加, 読取, 値置換, 入口消去処理, 容量, 判定空値, 内容消去 | 入口一覧(目錄): 순서가 있는 入口値 모음 |
| 辞書 | 値格納, 入口探索, 実施判定存在, 入口消去処理, 容量, 内容消去 | 辞書(辭典): 찾는 말인 열쇠에 값을 対応付け値 |
| 作業 | 起動処理(実行可能処理作業), 待機(作業担当), 作業実行権譲渡, 判定稼働中 | 作業 スレッド値: 한 プログラム 안의 命令実行 ストリーム値 |
| 通信 | 開放, 送信, 受取, 待機期限, 閉鎖 | 通信(通信), データグラム(電文), ポート値: データ 교환·메시지·포트의 역할 |
| 画面 | 矩形, 入口消去処理 | 画面(畫面): 実際データ 그림을 표시하는 면 |
| 中核値 | ミリ秒, 矩形 | 内蔵 JVM의 고정 native 接続; 일반 JNI는 아님 |

이 명명은 現在項目 기능을 설명하는 용어 선택이다. 기존 한국어에 없던 역사적 어원을 만들어 주장하지 않는다. ファイル名前本文·식별자는 UTF-8 소스로 보관한다. `文字.データ復号化`는 잘못된 UTF-8에 IllegalArgumentException을 던지며, `符号化`는 짝이 없는 서로게이트를 `?`로 바꾼다. `ファイル.読取`는 엄격한 UTF-8 복호화를 적용한다. 画面 색은 `빨강 | (초록 << 8) | (파랑 << 16)` 형식이다.

## 命令実行 제한과 남은 作業

- 동시에 적재하는 class 最大値 16개(日本語 クラス値 ヘッダー), class당 16 KiB·定数値 풀 511항목, 전체 メソッド値/フィールド値 각각 512개. メソッド値 コード値 8 KiB, 局所有効範囲 変数値·피연산자 被演算子スタック 각각 128슬롯, 引数 最大値 16개(this ヘッダー).
- VM 가닥은 main ヘッダー **실행당 最大値 4개**, 가닥당 呼出 深さ値 32. 100개 명령마다 命令実行 대상을 바꾼다. 네이티브 呼出 도중에는 전환하지 않는다. pthread/SMP/OS 스레드가 아니며 Thread.sleep/interrupt/daemon/우선순위, Object.wait/notify, java.util.concurrent는 없다.
- オブジェクト値 힙은 32768개의 32비트 슬롯이다. 런타임의 AOT 배열은 実際データ 메모리에서 64비트 슬롯을 사용한다. GC가 있어도 대형 ファイル·대형 文字列·객체가 이 제한을 넘을 数 있다.
- 실행은 50만 バイトコード 命令 및 커널의 약 2초 EL0 기한으로 제한된다. Swing의 入力値 대기는 기한을 갱신하고 窓 切替方式 시 중단·재개한다. 일반 サーバー値·계산의 무제한 실행은 아직 없다. 判定未対応 命令·資源値 부족은 명시적인 오류로 종료한다.
- RAM ファイル 最大値 64개, 파일당 16384바이트, 経路 UTF-8 63바이트. RAM 디렉터리와 通信相手値/절대 경로를 제공하며 영속 저장은 아직 없다. 내장 日本語 class는 RAM ファイル 슬롯을 소비하지 않는다. 셸의 `cd`로 정한 現在項目 경로에서 ソース木·クラス値·データ 파일을 읽는다.
- UDP는 Java 루프백 및 lwIP/SLIP를 통한 外部値 IPv4를 제공한다. 実際データ GENET/Wi-Fi/DNS/TLS/HTTP 전체는 없다. データグラム 512바이트, ソケット値 8개, 소켓당 큐 4개. receive는 VM 가닥을 양보하며 대기하고 setSoTimeout을 적용하지만 전체 命令実行 기한은 여전히 적용된다.
- long/float/double, invokedynamic/람다, enum/annotation, 다차원 配列値, 완전한 配列値 공변성·인터페이스 階層値 検査項目, Reflection/JNI/JIT, NIO/ZIP API/Charset 전체, 보안/データ暗号化/국제화 전체, 전체 AWT/Swing/JavaFX는 미지원이다. Swing의 별도 支援値 부분집합은 下端値 및 開発 매뉴얼을 참고한다. クラス値 ファイル 전체 검증기·アクセス入口 許可値/보호된 멤버 검사는 아직 완전하지 않다. 손상된 입력은 EL0 値防護 境界位置値 내에서 종료되도록 한다.

전체 OpenJDK를 목표로 하려면 다음은 별도의 주요 実装 단계다: 완전한 JVM 値/妥当性検査/クラス値 로더와 例外 모델 → 영속 VFS·mmap·時計·원자 操作値·実際データ 스레드/同期化 ABI → OpenJDK java.base 및 native ライブラリ 移植 → 装置 네트워크·TCP/IP → 窓 시스템/書体値/입력기·java.desktop → Java SE 호환성 試験. 現在項目 内蔵 JVM의 일부 메서드를 더하는 것으로 이 작업이 완료되지는 않는다.

## 妥当性検査

`道具/JVM試験.py`는 같은 Java 8 class 파일의 출력을 ホスト OpenJDK `-Xverify:all`과 QEMU raspi4b 内蔵 커널에서 비교한다. オブジェクト値/상속/인터페이스·switch·配列値, 例外/finally, 컬렉션/GC, Thread/錠値, 日本語 UTF-8/ファイル/컬렉션, 実際データ UDP 루프백/時間値 초과, 게스트 ハングル文字列 ソース木 ソースコンパイル, 配列値 型値/値複写/ファイル 境界位置値·ハングル文字列 패키지의 9개 비교 시험과 잘못된 class 버전/切抜き済み値 ファイル 値却下 시험을 실행한다. UDP 計画根 실행에는 ホスト 루프백 ソケット値 권한이 필요하다.

`道具/起動試験.py`는 中核値 値防護/회귀 시험과 별도로 日本語 Java 画面 API가 実際データ 픽셀을 그렸는지도 QMP 画面 캡처로 검사한다. 보고서는 `build/verification/jvm/report.json`, `build/verification/report.json`이며 시험한 kernel8.img의 SHA-256을 기록한다. 実際データ Pi4 機器値 起動 시험과 전체 JDK 호환성 試験 결과는 아니다.


## JVM 0.3: 네트워크와 GUI 拡張子値

`Socket`/`ServerSocket` 生成·接続·accept·양방향 InputStream/OutputStream·close·EOF·時間値 제한과 UTF-8 `String.getBytes`를 추가했다. JVM 0.4에서는 外部値 桁値 IPv4 TCP도 lwIP/SLIP에 연결했다. 연결형 終端位置点 16개, Java 루프백 버퍼 1024바이트, 外部値 TCP 버퍼 4096바이트다. DNS·TLS는 없다.

`JFrame`, `JPanel`, `JLabel`, `JButton`, `JTextField`, `ActionListener`, `ActionEvent`, `SwingUtilities.invokeLater`의 문서화한 부분집합을 네이티브 GUI에 연결했다. `setLayout(null)`과 명시적 좌표를 사용한다. 전체 OpenJDK Swing 또는 Java SE 호환 구현은 아니다. 対話式 이벤트 대기는 命令実行 기한을 갱신하고 端末 切替方式 시 프로세스 상태를 格納値·복원한다. 이벤트 콜백 자체는 기존 バイトコード/CPU 기한을 따른다.

日本語 `窓`, `操作部品`, `接続状態輸送` 클래스를 配布値 JAR와 内蔵 JVM 내장 자원에 추가했다. 상세 メソッド値·上限値·ソース木·업로드 방법: [ハングル文字列 開発 매뉴얼](開発手引.md).

## 日本語 객체의 직접 命令実行

`窓`, `ラベル`, `本文フィールド`, `ボタン`, `イベント待ち行列`, `動作通知`, `作業担当`은
표준 GUI/Thread 객체를 보관하는 래퍼가 아니다. 内蔵 JVM의 オブジェクト値 生成,
書式値 検査項目, 画面 呼出, イベント 큐, スレッド値 스케줄러에 日本語 계약을 직접 구현했다.
표준 `javax.swing`·`Thread` 코드의 命令実行 경로도 유지한다.
日本語 단추와 표준 JButton은 서로 다른 형식이며, 해당 instanceof 검사도 검증한다.

内蔵 실행기의 日本語 진입점은 `public static void 起動処理()`이다.
표준 `main(String[])`도 지원하며 二値 第三被演算子 있으면 日本語 진입점을 우선한다.
명령행 인수는 `実行引数.項目個数()`와 `実行引数.文(序数添字)`으로 읽는다.
`example/java`의 다섯 예제는 이 규약을 사용한다. 静的値 ファイル 예제는 게스트
javac로도 컴파일하며, GUI/スレッド値 소스는 ホスト `javac --release 8`을 사용한다.
직접 GUI/スレッド値 API는 内蔵 JVM 전용이다. 기존 OpenJDK 비교 시험과 별도로
日本語 가닥의 命令実行·値待合·중복 起動処理 値却下, GUI イベント 原点値·番号·콜백을 검사한다.
전체 JDK 번역이나 모든 API의 jaot 지원을 뜻하지 않는다.

メソッド値 이름은 바이트코드에서도 유지된다. 이름과 참조를 같이 수정하면
日本語 클래스도 실행되지만, 文字列 리터럴·표준 ライブラリ 재정의·native
接続·진입점은 각각 컴파일러와 실행기의 계약을 맞춰야 한다.
[상세 계약과 用例](日本語Java/案内.md)를 참고한다.

## 端末 部分要素値 再読込

移動値·容量 변경은 새 窓 영역과 前回項目 자리에서 드러난 띠만 합성한다.
1920×32 画素(240 KiB)의 一時値 그림에서 배경·겹친 窓·文字値·GUI를 먼저
완성하고, 現在項目 値表示 메모리와 비교하여 달라진 화소만 기록한다.
32줄보다 큰 영역은 여러 띠로 처리하므로 전체 프레임을 원자적으로
교체하거나 수직 동기에 맞추는 방식은 아니다. 전체 배경을 먼저 지우는
중간 화면은 표시하지 않는다. 좌표가 같으면 再試行処理値 그리지 않는다.

`make test-redraw`는 実際データ C 塗装画面 코드를 호스트의 記憶データ 화면에 연결해
移動値 80회·容量 値変更 40회·겹친 窓 4개를 전체 합성 결과와 画素 단위로 대조한다.
領域値 밖 利用者 描画, 동일 画素 무기록, ポインタ 밑그림, 実際データ 画面 行 간격을
검사한다. 이 시험의 시간은 ホスト CPU 측정이며 Pi 4/QEMU 속도로 해석하지 않는다.
`make test-resize`는 QEMU/VNC의 640×480 및 1920×1080에서 左側面 隅値 引摺り値,
ハングル文字列 入力値·vi 미저장 内容物値·독립 窓 크기를 검사한다.
