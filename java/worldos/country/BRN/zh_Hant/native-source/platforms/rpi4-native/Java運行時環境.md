# 內建 ARM64 JVM 0.4와 中文 庫

中文 通信·異常 사용법은 [中文 Java API](中文Java/指南.md), 函數·變量值·檔案 이름의 변경과 어원 근거는 [命名 指南](命名/指南.md)를 참고한다.

JAR 執行命令, 外部值 IPv4 TCP/UDP, 별도 靜態值 부분집합 `jaot`와 게스트 C 컴파일은 [FTP·C·JAR·AOT 매뉴얼](檔案傳送與編譯過程.md)에 설명한다. 底端值 物件值·Thread·Swing은 JVM 경로의 기능이며 AOT 支持值 범위와 같지 않다.

이 구현은 **Linux 없이 부팅한 Java AOT 커널의 EL0에서 執行命令**한다. JDK/JRE의 거의 모든 기능을 제공하는 단계는 아직 아니다. HotSpot·OpenJDK 類別值 庫 전체를 이식하거나 Java SE 인증/TCK를 통과한 구현도 아니다. 이번 확장은 단일 類別值·靜態值 方法值 중심이던 실행기를 物件值·庫 執行命令 기반으로 넓힌 것이다.

## 실행과 編譯原始碼

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
# 內建 內核值 안에서 原始碼樹 編譯原始碼 → class 執行命令, 中文 API 調用
python3 工具集/執行檔案.py 測試/Java/韓文字母原始碼.java

# 物件值·異常 등은 宿主 JDK로 Java 8 class를 만든 之後狀態 內建 커널에서 執行命令
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java 測試/Java/測試韓文字母.java
python3 工具集/執行檔案.py build/my-java/測試韓文字母.class

# 의존 class 파일은 --include로 함께 傳送值
javac --release 8 -encoding UTF-8 -d build/my-java 測試/Java/測試物件集.java
python3 工具集/執行檔案.py build/my-java/測試物件集.class \
  --include build/my-java/背景值.class --include build/my-java/分支值.class \
  --include build/my-java/能夠計算.class

make test-jvm
```

`--include DIR`는 그 디렉터리의 class 파일을 재귀적으로 읽어 `패키지.類別值.class`라는 RAM 檔案 이름으로 전송한다. 주 클래스도 패키지가 있다면 `--class-name 패키지.類別值`를 지정한다. 셸에서는 해당 이름으로 업로드하고 `java 패키지.類別值`로 실행한다. JVM 0.4는 Main-Class가 있는 16 KiB 이하 JAR도 `java -jar 檔案.jar`로 실행한다. JAR 모드에서는 JAR 내부 클래스와 내장 中文 클래스만 찾는다. 分發值 中文 庫 JAR는 宿主 javac의 classpath로 사용하며, 같은 클래스가 使用者 JVM ELF에도 讀取 전용 자료로 포함된다. 일반 class 모드에서는 사용자가 같은 이름으로 올린 RAM class를 먼저 읽는다.

게스트 `javac`는 여전히 靜態值 方法值, int/boolean/char/String, 條件·迭代值, 字符串 合併值列, 일부 檔案 스트림 등의 **內建 부분집합 編譯器**第三操作數. 物件值 聲明·상속·try/catch·Thread 使用值 소스를 게스트 javac가 構建全部 컴파일하는 것은 아니다. 頂端值 기능은 `javac --release 8`로 만든 class를 內建 JVM에서 실행한다. 中文 API 중 輸出·字元 스칼라 函數·檔案 讀取/쓰기는 게스트 컴파일러에도 연결했다. 다음처럼 전체 이름으로 호출한다.

```java
public class 問候例 {
    public static void main(String[] 實參) throws Exception {
        中文.內建.輸出.寫入行("안녕하세요😀");
        中文.內建.輸出.寫入編號(中文.內建.字元.程式碼分個數("韓文文本😀"));
        中文.內建.檔案.寫入("問候例.txt", "韓文文本 檔案😀");
        中文.內建.輸出.寫入行(中文.內建.檔案.讀取("問候例.txt"));
    }
}
```

## 內建 JVM에서 구현한 裁剪

| 區域值 | 제공 裁剪 |
|---|---|
| 類別值 | class 버전 45…52, 여러 類別值 로딩, 인스턴스/靜態值 字段值, 생성자, 상속, 가상 調用, 인터페이스 調用, 靜態值 初始化 |
| 值·命令 | 32비트 int 계열, boolean/byte/char/short, 引用, 1차원 陣列值, 分支·switch·wide, instanceof/checkcast, category-1 操作數棧 命令 |
| 異常 | 지원하는 표준 異常 生成·throw·catch·finally, 方法值 경계를 넘는 前向值, getMessage; 底端值 限制值 引用 |
| 記憶體資料 | 비이동 mark/sweep GC, 빈 區域值 병합, 操作數棧·靜態值 字段值·컬렉션·執行緒值·모니터·字符串 상수의 引用 保持值 |
| 字符串 | UTF-16, length/charAt/equals/isEmpty/substring/concat/hashCode/toString, String.valueOf(int), StringBuilder의 默認值 生成·append(int/boolean/char/String)·toString |
| 數 | Integer.parseInt/valueOf/intValue/toString, 작은 Integer 캐시, Math.abs/min/max(int) |
| 표준 輸出 | System.out/err, PrintStream.print/println의 int/boolean/char/String 및 빈 println |
| 陣列值 | int/byte/boolean/char/short/引用 陣列值, 長度·裁剪 檢查項, 引用 陣列值 項目元素 類型值 檢查項, System.arraycopy의 重疊區列/裁剪/項目元素 類型值 檢查項 |
| 檔案 | FileInputStream(String), FileOutputStream(String[,boolean]); read()/read(byte[][,offset,len]), write(int)/write(byte[][,offset,len]), close, 輸出 flush. EOF는 -1 |
| 컬렉션 | ArrayList/List: add(E), get, set, remove(int), size, isEmpty, clear. HashMap/Map: put/get/remove/containsKey/size/isEmpty/clear |
| 執行緒值 | Thread(), Thread(Runnable), Thread 상속, start/join/isAlive/currentThread/yield; synchronized 方法值·블록의 재진입·경합·異常 시 釋放存儲裝置 |
| UDP | DatagramSocket의 默認值/硬件埠 생성자, send/receive/close/getLocalPort/setSoTimeout; DatagramPacket의 byte[]/長度 生成 및 地址·硬件埠 頭文件 生成, getData/getLength/getAddress/getPort/setLength |
| 地址 | InetAddress.getByName은 localhost/數字值 IPv4 (DNS 是否不支持), getLoopbackAddress/getHostAddress |
| 繪圖 | 中文 屏幕 API가 EL0 SVC를 통해 프레임버퍼에 사각형을 繪圖; 裁剪 檢查項 |

컬렉션은 지정한 메서드만 제공하며 iterator/stream/對齊值·使用者 定義值 equals/hashCode 콜백은 없다. 사전의 열쇠는 String/Integer/null 사용을 시험했다. UTF-16 程式碼值 단위와 Unicode 程式碼值 포인트 수는 구분한다. 韓文文本 輸入值 組合·正規化值·아랍어 조판·GUI 다국어 글꼴은 이 字符串 지원과 별개다.

예외는 Throwable/Exception/RuntimeException, ArithmeticException, NullPointerException, IndexOutOfBoundsException/ArrayIndexOutOfBoundsException/StringIndexOutOfBoundsException, IllegalArgumentException/NumberFormatException/IllegalThreadStateException, IOException/FileNotFoundException, IllegalStateException, ClassCastException, NegativeArraySizeException, ArrayStoreException, UnknownHostException, SocketTimeoutException의 제한된 生成·分類值·처리를 제공한다. 使用者 定義值 Throwable 상속, stack trace/cause/suppressed 異常, try-with-resources의 addSuppressed, 완전한 初始化 錯誤 포장은 아직 없다. 잡히지 않은 예외는 當前項目 전체 Java 실행을 실패로 끝낸다.

## 中文 API

독립 패키지 **`中文.內建`**를 사용한다. Linux판 `中文.Java`首位操作數 요구하는 NIO/Swing/HTTP API를 內建 커널에서 실행할 數 있다고 혼동하지 않도록 패키지를 나눴다. 이 라이브러리는 類別值 名稱·方法值·實參·字段值·檔案 이름에 한국어를 사용한다. 표준 Java 類別值 이름은 호환성을 위해 보존한다.

| 類別值 | 공개 기능 | 이름의 의미 |
|---|---|---|
| 輸出 | 寫入, 寫入行, 寫入編號 | 輸出(出力): 내용을 바깥으로 已導出值 |
| 字元 | 長度, 相等文本, 粘貼文本, 剪切值, 解析整數/寫入整數值, 程式碼分個數, 編碼/解密資料 | 字元(文本), 編碼狀態值(符號): 글의 단위와 그 값을 바이트로 나타내는 規則值 |
| 檔案 | 讀取/寫入(String 名稱), 讀取位元組值/寫入位元組值 | 널리 쓰는 使用者 용어를 보존; RAM 자료의 名稱 |
| 條目列表 | 添加值列, 讀取, 替換值, 擦除條目, 大小, 是否空值, 清空內容 | 條目列表(目錄): 순서가 있는 條目值 모음 |
| 字典 | 放入值, 查找條目, 是否執行存在, 擦除條目, 大小, 清空內容 | 字典(辭典): 찾는 말인 열쇠에 값을 映射值 |
| 任務 | 運行(可運行任務任務), 等待(後臺任務), 掛起任務, 是否存活 | 任務 執行緒值: 한 程式 안의 執行命令 流值 |
| 通信 | 打開, 發送, 接收, 超時, 關閉 | 通信(通信), 數據報(電文), 埠值: 資料 교환·메시지·포트의 역할 |
| 屏幕 | 矩形, 擦除條目 | 屏幕(畫面): 實際資料 그림을 표시하는 면 |
| 內核值 | 毫秒, 矩形 | 內建 JVM의 고정 native 連接; 일반 JNI는 아님 |

이 명명은 當前項目 기능을 설명하는 용어 선택이다. 기존 한국어에 없던 역사적 어원을 만들어 주장하지 않는다. 檔案名稱文本·식별자는 UTF-8 소스로 보관한다. `字元.解密資料`는 잘못된 UTF-8에 IllegalArgumentException을 던지며, `編碼`는 짝이 없는 서로게이트를 `?`로 바꾼다. `檔案.讀取`는 엄격한 UTF-8 복호화를 적용한다. 屏幕 색은 `빨강 | (초록 << 8) | (파랑 << 16)` 형식이다.

## 執行命令 제한과 남은 任務

- 동시에 적재하는 class 最大值 16개(中文 類別值 頭文件), class당 16 KiB·常量值 풀 511항목, 전체 方法值/字段值 각각 512개. 方法值 程式碼值 8 KiB, 局部作用域 變量值·피연산자 操作數棧 각각 128슬롯, 實參 最大值 16개(this 頭文件).
- VM 가닥은 main 頭文件 **실행당 最大值 4개**, 가닥당 調用 深度值 32. 100개 명령마다 執行命令 대상을 바꾼다. 네이티브 調用 도중에는 전환하지 않는다. pthread/SMP/OS 스레드가 아니며 Thread.sleep/interrupt/daemon/우선순위, Object.wait/notify, java.util.concurrent는 없다.
- 物件值 힙은 32768개의 32비트 슬롯이다. 런타임의 AOT 배열은 實際資料 메모리에서 64비트 슬롯을 사용한다. GC가 있어도 대형 檔案·대형 字符串·객체가 이 제한을 넘을 數 있다.
- 실행은 50만 字節碼 命令 및 커널의 약 2초 EL0 기한으로 제한된다. Swing의 輸入值 대기는 기한을 갱신하고 窗口 切換模式 시 중단·재개한다. 일반 服務器值·계산의 무제한 실행은 아직 없다. 是否不支持 命令·資源值 부족은 명시적인 오류로 종료한다.
- RAM 檔案 最大值 64개, 파일당 16384바이트, 路徑 UTF-8 63바이트. RAM 디렉터리와 對端值/절대 경로를 제공하며 영속 저장은 아직 없다. 내장 中文 class는 RAM 檔案 슬롯을 소비하지 않는다. 셸의 `cd`로 정한 當前項目 경로에서 原始碼樹·類別值·資料 파일을 읽는다.
- UDP는 Java 루프백 및 lwIP/SLIP를 통한 外部值 IPv4를 제공한다. 實際資料 GENET/Wi-Fi/DNS/TLS/HTTP 전체는 없다. 數據報 512바이트, 通訊端值 8개, 소켓당 큐 4개. receive는 VM 가닥을 양보하며 대기하고 setSoTimeout을 적용하지만 전체 執行命令 기한은 여전히 적용된다.
- long/float/double, invokedynamic/람다, enum/annotation, 다차원 陣列值, 완전한 陣列值 공변성·인터페이스 層值 檢查項, Reflection/JNI/JIT, NIO/ZIP API/Charset 전체, 보안/加密資料/국제화 전체, 전체 AWT/Swing/JavaFX는 미지원이다. Swing의 별도 支持值 부분집합은 底端值 및 開發 매뉴얼을 참고한다. 類別值 檔案 전체 검증기·存取條目 權限值/보호된 멤버 검사는 아직 완전하지 않다. 손상된 입력은 EL0 保護值 邊界位置值 내에서 종료되도록 한다.

전체 OpenJDK를 목표로 하려면 다음은 별도의 주요 實現 단계다: 완전한 JVM 值/有效性校驗/類別值 로더와 異常 모델 → 영속 VFS·mmap·時鐘·원자 操作值·實際資料 스레드/同步化 ABI → OpenJDK java.base 및 native 庫 移植 → 設備 네트워크·TCP/IP → 窗口 시스템/字體值/입력기·java.desktop → Java SE 호환성 測試. 當前項目 內建 JVM의 일부 메서드를 더하는 것으로 이 작업이 완료되지는 않는다.

## 有效性校驗

`工具集/測試JVM.py`는 같은 Java 8 class 파일의 출력을 宿主 OpenJDK `-Xverify:all`과 QEMU raspi4b 內建 커널에서 비교한다. 物件值/상속/인터페이스·switch·陣列值, 異常/finally, 컬렉션/GC, Thread/鎖值, 中文 UTF-8/檔案/컬렉션, 實際資料 UDP 루프백/時間值 초과, 게스트 韓文文本 原始碼樹 編譯原始碼, 陣列值 類型值/複製值/檔案 邊界位置值·韓文文本 패키지의 9개 비교 시험과 잘못된 class 버전/已裁剪值 檔案 拒絕值 시험을 실행한다. UDP 項目根 실행에는 宿主 루프백 通訊端值 권한이 필요하다.

`工具集/啓動測試.py`는 內核值 保護值/회귀 시험과 별도로 中文 Java 屏幕 API가 實際資料 픽셀을 그렸는지도 QMP 屏幕 캡처로 검사한다. 보고서는 `build/verification/jvm/report.json`, `build/verification/report.json`이며 시험한 kernel8.img의 SHA-256을 기록한다. 實際資料 Pi4 硬件值 啓動 시험과 전체 JDK 호환성 測試 결과는 아니다.


## JVM 0.3: 네트워크와 GUI 擴展名值

`Socket`/`ServerSocket` 生成·連接·accept·양방향 InputStream/OutputStream·close·EOF·時間值 제한과 UTF-8 `String.getBytes`를 추가했다. JVM 0.4에서는 外部值 數字值 IPv4 TCP도 lwIP/SLIP에 연결했다. 연결형 結束分 16개, Java 루프백 버퍼 1024바이트, 外部值 TCP 버퍼 4096바이트다. DNS·TLS는 없다.

`JFrame`, `JPanel`, `JLabel`, `JButton`, `JTextField`, `ActionListener`, `ActionEvent`, `SwingUtilities.invokeLater`의 문서화한 부분집합을 네이티브 GUI에 연결했다. `setLayout(null)`과 명시적 좌표를 사용한다. 전체 OpenJDK Swing 또는 Java SE 호환 구현은 아니다. 交互式 이벤트 대기는 執行命令 기한을 갱신하고 終端 切換模式 시 프로세스 상태를 存儲值·복원한다. 이벤트 콜백 자체는 기존 字節碼/CPU 기한을 따른다.

中文 `窗口`, `小組件`, `連接狀態傳輸` 클래스를 分發值 JAR와 內建 JVM 내장 자원에 추가했다. 상세 方法值·限制值·原始碼樹·업로드 방법: [韓文文本 開發 매뉴얼](開發指南.md).

## 中文 객체의 직접 執行命令

`窗口`, `標籤`, `文本字段`, `按鈕`, `事件排隊`, `動作通知`, `後臺任務`은
표준 GUI/Thread 객체를 보관하는 래퍼가 아니다. 內建 JVM의 物件值 生成,
格式值 檢查項, 屏幕 調用, 事件 큐, 執行緒值 스케줄러에 中文 계약을 직접 구현했다.
표준 `javax.swing`·`Thread` 코드의 執行命令 경로도 유지한다.
中文 단추와 표준 JButton은 서로 다른 형식이며, 해당 instanceof 검사도 검증한다.

內建 실행기의 中文 진입점은 `public static void 運行()`이다.
표준 `main(String[])`도 지원하며 二值 第三操作數 있으면 中文 진입점을 우선한다.
명령행 인수는 `運行參數.項目個數()`와 `運行參數.文本(序數索引)`으로 읽는다.
`example/java`의 다섯 예제는 이 규약을 사용한다. 靜態值 檔案 예제는 게스트
javac로도 컴파일하며, GUI/執行緒值 소스는 宿主 `javac --release 8`을 사용한다.
직접 GUI/執行緒值 API는 內建 JVM 전용이다. 기존 OpenJDK 비교 시험과 별도로
中文 가닥의 執行命令·等待狀態值·중복 運行 拒絕值, GUI 事件 原點值·編號·콜백을 검사한다.
전체 JDK 번역이나 모든 API의 jaot 지원을 뜻하지 않는다.

方法值 이름은 바이트코드에서도 유지된다. 이름과 참조를 같이 수정하면
中文 클래스도 실행되지만, 字符串 리터럴·표준 庫 재정의·native
連接·진입점은 각각 컴파일러와 실행기의 계약을 맞춰야 한다.
[상세 계약과 範例](中文Java/指南.md)를 참고한다.

## 終端 子部分值 刷新

移動值·大小 변경은 새 窗口 영역과 上一個項目 자리에서 드러난 띠만 합성한다.
1920×32 像素(240 KiB)의 臨時值 그림에서 배경·겹친 窗口·字元值·GUI를 먼저
완성하고, 當前項目 顯示值 메모리와 비교하여 달라진 화소만 기록한다.
32줄보다 큰 영역은 여러 띠로 처리하므로 전체 프레임을 원자적으로
교체하거나 수직 동기에 맞추는 방식은 아니다. 전체 배경을 먼저 지우는
중간 화면은 표시하지 않는다. 좌표가 같으면 重試值 그리지 않는다.

`make test-redraw`는 實際資料 C 畫圖屏幕 코드를 호스트의 記憶體資料 화면에 연결해
移動值 80회·大小 更改值 40회·겹친 窗口 4개를 전체 합성 결과와 像素 단위로 대조한다.
區域值 밖 使用者 繪圖, 동일 像素 무기록, 指針 밑그림, 實際資料 屏幕 行 간격을
검사한다. 이 시험의 시간은 宿主 CPU 측정이며 Pi 4/QEMU 속도로 해석하지 않는다.
`make test-resize`는 QEMU/VNC의 640×480 및 1920×1080에서 左側 角值 拖動值,
韓文文本 輸入值·vi 미저장 內容值·독립 窗口 크기를 검사한다.
