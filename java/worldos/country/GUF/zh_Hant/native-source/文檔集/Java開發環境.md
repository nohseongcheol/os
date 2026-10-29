# jkoros 안에서 Java 編譯原始碼·執行命令

이 문서의 啓動·命令殼·存儲值 명령은 **x86 版本值** 기준이다. 공유 Java 編譯器/JVM은 [內建 ARM64 Pi4 版本值](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART 輸入值·韓文文本 檔案名稱文本, `edit`의 단독 `.` 存儲值, 16개 RAM 檔案, 약 2초 執行命令 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 實際資料 JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. 宿主 編譯原始碼 서버나 Linux 게스트는 사용하지 않는다.

**當前項目 구현은 內建 제한형 編譯器·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java 程式 실행은 아직 지원하지 않는다.

## 바로 執行命令

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

ISO는 `os/build/kernel.iso`第三操作數. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. 執行命令 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 啓動 절차는 [VirtualBox 執行命令 指南](VirtualBox運行.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 檔案 전체를 새 내용으로 작성한다. 기존 내용의 行 編輯值 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

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

- `ls`: 파일과 位元組值 數 顯示值.
- `cat FILE`: 檔案 內容值 顯示值. 텍스트 소스에 사용한다.
- `rm FILE`: 記憶體資料 檔案 삭제.
- `edit FILE`: 전체 내용을 새로 輸入值. 빈 파일도 저장할 數 있다.
- 구문·類型值 檢查項 失敗值 시 기존 `.class`는 유지된다. 소스를 고친 後端值 컴파일이 실패했다면 上一個項目 執行命令 파일이 남아 있으므로 編譯原始碼 成功值 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 存儲值 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 原始碼樹·類別值·資料 파일을 보존할 數 있다. 最大值 8개, 파일마다 16KiB, 檔案 이름은 ASCII 1~63자다. 原始碼樹 이름은 `.class` 확장자 地址區域 때문에 最大值 62자다. 編輯值 입력은 ASCII이고 한 行 最大值 128자다. 行 또는 檔案 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. 內核值/編譯器/JVM 구현의 Java 식별자는 한국어이며, 當前項目 게스트 輸入值 限制值 때문에 使用者 範例 이름은 ASCII로 작성한다.

## 外部值 檔案 적재

호스트에서 만든 소스나 支持值 裁剪 안의 `.class`를 啓動 이미지에 포함할 數 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 實際資料 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# 宿主 JDK로 컴파일한 클래스도 사용할 數 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 啓動 之後狀態 `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 下一項目 빌드에서는 追加條目 파일을 포함하지 않는다. 檔案 內容值 변경과 條目列表 제거도 下一項目 빌드에 반영된다. 原始 宿主 파일에는 쓰지 않는다. 默認值 `Hello.java`直到 합해 8개이며, 같은 이름을 명시하면 默認值 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 類別值 檔案 버전을 맞추는 옵션이다. 사용하는 문법·字節碼·라이브러리도 底端值 支持值 裁剪 안에 있어야 한다.

## 支持值 裁剪

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| 類別值 | 패키지 없는 단일 類別值, 靜態值 函數, 재귀, 實參/發回結果 | 실행마다 단일 類別值 적재, public static main(String[]) |
| 默認值 值 | int, boolean, char, String, main의 String[] 實參 | 整數·引用 操作數棧, String, int[], String[], 내부 StringBuilder |
| 語句值 | 初始值 있는 局部作用域 聲明, 賦值狀態值, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 整數·引用 바이트코드와 條件 分支 |
| 表達式值 | 십진 整數, UTF-8 소스의 字符串/字元, + - * / %, 비교, ==/!=, !/&&/\|\|, 字符串 合併值列 | 整數 操作值·位元值 操作值·類型值 轉換值, 단락 평가, 陣列值 存取條目 |
| 檔案 | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | 實際資料 內核值 파일서술자와 連接, 生成·清空內容·追加繼續狀態·EOF |
| 輸出 | System.out.print/println: int/boolean/char/String, println() | 동일 |
| 字符串/實參 | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), 字符串 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, 初始值 없는 局部作用域 聲明, 오버로드, 임의 類型值 轉換值, 陣列值 生成 原始碼, 8/16진 리터럴, Unicode 原始碼樹 이스케이프 등은 미지원이다. `char`는 字元 리터럴로 초기화하며 일반 JDK의 모든 常量值 축소 변환을 구현하지 않는다. 外部值 `.class`의 `int[]` 生成/讀取/쓰기는 지원하므로 宿主 `javac --release 8`로 만든 陣列值 예제는 실행할 數 있다.

物件值 字段值·일반 物件值 生成·상속·인터페이스·여러 類別值 連接, long/float/double, 異常 程序值條目, 스레드·모니터, 리플렉션, JNI, JIT, GC, 頂端值 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java 異常 객체를 던지지 않고 診斷值 之後狀態 當前項目 프로그램을 종료한다. 객체와 字符串 存儲值 공간은 執行命令 退出程式 시 使用者 區域值 전체와 함께 회수한다. 지속 執行命令 중 GC는 없다.

## 執行命令 한도와 錯誤

| 資源值 | 容量限制 |
| --- | --- |
| 原始碼樹/類別值 檔案 | 각각 16KiB |
| 編譯器 | 詞元值 2,047개, 生成 程式碼值 4KiB, 常量值 풀 4KiB |
| 函數/實參 | 클래스당 32함수, 함수당 16인수 |
| JVM 常量值 | 511개 |
| JVM 函數 程式碼值 | 함수당 8KiB |
| JVM 調用/操作數棧/局部作用域 變量值 | 32프레임, 프레임당 操作數棧 128칸·局部作用域 128칸 |
| JVM 物件值 存儲值 地址區域 | 8,192개 32비트 槽條目, 헤더 頭文件 약 32KiB |
| 執行命令 | 最大值 500,000 命令, 기존 커널의 약 3초 CPU 執行命令 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 支持值 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM 字典 검증기를 구현한 것은 아니다. 檔案/屬性值 長度, 常量值 引用, 命令·分支 경계를 검사하고, 執行命令 중 操作數棧 格式值·局部作用域 初始化·陣列值 下標值·物件值 참조를 검사한다. 使用者 코드의 페이지·硬件埠 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, 編譯原始碼·JVM 오류는 `Exit: 1`, 命令 實參 오류는 `Exit: 2`第三操作數. CPU 時間值 상한은 기존 `Exit: 124`이며, 使用者 ELF 자체의 CPU/런타임 오류는 기존 退出程式 코드를 따른다. 失敗值 之後狀態 셸에서 다른 프로그램을 繼續處理 실행할 數 있다.

## 實現 위치와 測試

- `os/使用者/Java/Java編譯器.java`: 게스트 어휘·구문·類型值 檢查項, 常量值 풀 및 字節碼 生成.
- `os/使用者/Java/Java虛擬機器.java`: 類別值 적재, 操作數棧·프레임·物件值 存儲值, 命令 해석과 제한된 표준 調用.
- `os/原始碼/主記憶體檔案系統.java`: 記憶體資料 檔案系統, 編輯值, 啓動 檔案 적재.
- `os/原始碼/系統呼叫.java`, `compiler/開始用戶程式.s`: 檔案/字元 輸出 API와 使用者 指針 檢查項.
- `os/工具集/Java檔案打包.py`: 宿主 輸入值 檔案 有效性校驗·啓動 組值 生成.

```sh
make test-java
make test
```

`os/測試/Java測試.py`는 ELF/ISO 啓動, 게스트 編譯原始碼·執行命令, 使用者 輸入值, 재귀·반복문·整數 극값·字符串 合併值列·단락 평가, 재실행, 原始碼樹 錯誤 之後狀態 기존 類別值 보존, 陣列值/數 해독 錯誤, 무한 迭代值 限制值, 編輯值 넘침과 檔案 부족을 검사한다. 게스트 生成 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 宿主 OpenJDK의 類別值, 整數 배열과 韓文文本 상수를 게스트에 적재하며, 손상된 檔案 標記值·버전·常量值 數·分支·스택을 거부하는지도 검사한다. 기록은 `os/build/Java測試.json`에 남는다. 디스크 없는 별도 測試 VM만 생성하고 종료한다.

實現 형식의 참고 資料: Oracle [JVM 類別值 檔案 規格](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM 命令 規格](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java 檔案 輸入輸出

[FileDemo.java](../posix-kor/Java範例/FileDemo.java)는 일반 Java 표준 類別值 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 啓動 이미지에 넣은 後端值 `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`第三操作數. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. 默認值 輸出 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. 異常 物件值·try/catch·try-with-resources는 지원하지 않으며 檔案 오류를 진단하고 프로그램을 종료한다. 陣列值 輸入輸出, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 檔案 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 命令殼 `sync`首位操作數 필요하다. 예제의 檔案 이름은 當前項目 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/測試/Java檔案測試.py`는 實際資料 게스트 編譯原始碼 결과를 OpenJDK `-Xverify:all`로 重試值 실행해 檔案 바이트와 출력을 대조한다. 범위와 存儲值 介質值 사용법은 [posix-kor 指南](../posix-kor/指南.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
