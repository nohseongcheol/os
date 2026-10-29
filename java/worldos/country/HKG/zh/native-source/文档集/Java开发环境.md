# jkoros 안에서 Java 编译源代码·执行命令

이 문서의 启动·命令壳·存储值 명령은 **x86 版本值** 기준이다. 공유 Java 编译器/JVM은 [内置 ARM64 Pi4 版本值](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART 输入值·韩文文本 文件名称文本, `edit`의 단독 `.` 存储值, 16개 RAM 文件, 약 2초 执行命令 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 实际数据 JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. 宿主 编译源代码 서버나 Linux 게스트는 사용하지 않는다.

**当前项目 구현은 内置 제한형 编译器·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java 程序 실행은 아직 지원하지 않는다.

## 바로 执行命令

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

ISO는 `os/build/kernel.iso`第三操作数. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. 执行命令 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 启动 절차는 [VirtualBox 执行命令 指南](VirtualBox运行.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 文件 전체를 새 내용으로 작성한다. 기존 내용의 行 编辑值 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

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

- `ls`: 파일과 字节值 数 显示值.
- `cat FILE`: 文件 内容值 显示值. 텍스트 소스에 사용한다.
- `rm FILE`: 内存数据 文件 삭제.
- `edit FILE`: 전체 내용을 새로 输入值. 빈 파일도 저장할 数 있다.
- 구문·类型值 检查项 失败值 시 기존 `.class`는 유지된다. 소스를 고친 后端值 컴파일이 실패했다면 上一个项目 执行命令 파일이 남아 있으므로 编译源代码 成功值 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 存储值 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 源代码树·类值·数据 파일을 보존할 数 있다. 最大值 8개, 파일마다 16KiB, 文件 이름은 ASCII 1~63자다. 源代码树 이름은 `.class` 확장자 地址区域 때문에 最大值 62자다. 编辑值 입력은 ASCII이고 한 行 最大值 128자다. 行 또는 文件 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. 内核值/编译器/JVM 구현의 Java 식별자는 한국어이며, 当前项目 게스트 输入值 限制值 때문에 用户 用例 이름은 ASCII로 작성한다.

## 外部值 文件 적재

호스트에서 만든 소스나 支持值 裁剪 안의 `.class`를 启动 이미지에 포함할 数 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 实际数据 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# 宿主 JDK로 컴파일한 클래스도 사용할 数 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 启动 之后状态 `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 下一项目 빌드에서는 追加条目 파일을 포함하지 않는다. 文件 内容值 변경과 条目列表 제거도 下一项目 빌드에 반영된다. 原始 宿主 파일에는 쓰지 않는다. 默认值 `Hello.java`直到 합해 8개이며, 같은 이름을 명시하면 默认值 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 类值 文件 버전을 맞추는 옵션이다. 사용하는 문법·字节码·라이브러리도 底端值 支持值 裁剪 안에 있어야 한다.

## 支持值 裁剪

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| 类值 | 패키지 없는 단일 类值, 静态值 函数, 재귀, 实参/发回结果 | 실행마다 단일 类值 적재, public static main(String[]) |
| 默认值 值 | int, boolean, char, String, main의 String[] 实参 | 整数·引用 操作数栈, String, int[], String[], 내부 StringBuilder |
| 语句值 | 初始值 있는 局部作用域 声明, 赋值状态值, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 整数·引用 바이트코드와 条件 分支 |
| 表达式值 | 십진 整数, UTF-8 소스의 字符串/字符, + - * / %, 비교, ==/!=, !/&&/\|\|, 字符串 合并值列 | 整数 操作值·位值 操作值·类型值 转换值, 단락 평가, 数组值 存取条目 |
| 文件 | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | 实际数据 内核值 파일서술자와 连接, 生成·清空内容·追加继续状态·EOF |
| 输出 | System.out.print/println: int/boolean/char/String, println() | 동일 |
| 字符串/实参 | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), 字符串 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, 初始值 없는 局部作用域 声明, 오버로드, 임의 类型值 转换值, 数组值 生成 源代码, 8/16진 리터럴, Unicode 源代码树 이스케이프 등은 미지원이다. `char`는 字符 리터럴로 초기화하며 일반 JDK의 모든 常量值 축소 변환을 구현하지 않는다. 外部值 `.class`의 `int[]` 生成/读取/쓰기는 지원하므로 宿主 `javac --release 8`로 만든 数组值 예제는 실행할 数 있다.

对象值 字段值·일반 对象值 生成·상속·인터페이스·여러 类值 连接, long/float/double, 异常 进程值条目, 스레드·모니터, 리플렉션, JNI, JIT, GC, 顶端值 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java 异常 객체를 던지지 않고 诊断值 之后状态 当前项目 프로그램을 종료한다. 객체와 字符串 存储值 공간은 执行命令 退出程序 시 用户 区域值 전체와 함께 회수한다. 지속 执行命令 중 GC는 없다.

## 执行命令 한도와 错误

| 资源值 | 容量限制 |
| --- | --- |
| 源代码树/类值 文件 | 각각 16KiB |
| 编译器 | 词元值 2,047개, 生成 代码值 4KiB, 常量值 풀 4KiB |
| 函数/实参 | 클래스당 32함수, 함수당 16인수 |
| JVM 常量值 | 511개 |
| JVM 函数 代码值 | 함수당 8KiB |
| JVM 调用/操作数栈/局部作用域 变量值 | 32프레임, 프레임당 操作数栈 128칸·局部作用域 128칸 |
| JVM 对象值 存储值 地址区域 | 8,192개 32비트 槽条目, 헤더 头文件 약 32KiB |
| 执行命令 | 最大值 500,000 命令, 기존 커널의 약 3초 CPU 执行命令 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 支持值 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM 字典 검증기를 구현한 것은 아니다. 文件/属性值 长度, 常量值 引用, 命令·分支 경계를 검사하고, 执行命令 중 操作数栈 格式值·局部作用域 初始化·数组值 下标值·对象值 참조를 검사한다. 用户 코드의 페이지·硬件端口 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, 编译源代码·JVM 오류는 `Exit: 1`, 命令 实参 오류는 `Exit: 2`第三操作数. CPU 时间值 상한은 기존 `Exit: 124`이며, 用户 ELF 자체의 CPU/런타임 오류는 기존 退出程序 코드를 따른다. 失败值 之后状态 셸에서 다른 프로그램을 继续处理 실행할 数 있다.

## 实现 위치와 测试

- `os/用户/Java/Java编译器.java`: 게스트 어휘·구문·类型值 检查项, 常量值 풀 및 字节码 生成.
- `os/用户/Java/Java虚拟机.java`: 类值 적재, 操作数栈·프레임·对象值 存储值, 命令 해석과 제한된 표준 调用.
- `os/源代码/主存文件系统.java`: 内存数据 文件系统, 编辑值, 启动 文件 적재.
- `os/源代码/系统调用.java`, `compiler/开始用户程序.s`: 文件/字符 输出 API와 用户 指针 检查项.
- `os/工具集/Java文件打包.py`: 宿主 输入值 文件 有效性校验·启动 组值 生成.

```sh
make test-java
make test
```

`os/测试/Java测试.py`는 ELF/ISO 启动, 게스트 编译源代码·执行命令, 用户 输入值, 재귀·반복문·整数 극값·字符串 合并值列·단락 평가, 재실행, 源代码树 错误 之后状态 기존 类值 보존, 数组值/数 해독 错误, 무한 迭代值 限制值, 编辑值 넘침과 文件 부족을 검사한다. 게스트 生成 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 宿主 OpenJDK의 类值, 整数 배열과 韩文文本 상수를 게스트에 적재하며, 손상된 文件 标记值·버전·常量值 数·分支·스택을 거부하는지도 검사한다. 기록은 `os/build/Java测试.json`에 남는다. 디스크 없는 별도 测试 VM만 생성하고 종료한다.

实现 형식의 참고 数据: Oracle [JVM 类值 文件 规格](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM 命令 规格](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java 文件 输入输出

[FileDemo.java](../posix-kor/Java示例/FileDemo.java)는 일반 Java 표준 类值 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 启动 이미지에 넣은 后端值 `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`第三操作数. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. 默认值 输出 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. 异常 对象值·try/catch·try-with-resources는 지원하지 않으며 文件 오류를 진단하고 프로그램을 종료한다. 数组值 输入输出, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 文件 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 命令壳 `sync`首位操作数 필요하다. 예제의 文件 이름은 当前项目 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/测试/Java文件测试.py`는 实际数据 게스트 编译源代码 결과를 OpenJDK `-Xverify:all`로 重试值 실행해 文件 바이트와 출력을 대조한다. 범위와 存储值 介质值 사용법은 [posix-kor 指南](../posix-kor/指南.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
