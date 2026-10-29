# 内置 ARM64 JVM 0.4와 中文 库

中文 通信·异常 사용법은 [中文 Java API](中文Java/指南.md), 函数·变量值·文件 이름의 변경과 어원 근거는 [命名 指南](命名/指南.md)를 참고한다.

JAR 执行命令, 外部值 IPv4 TCP/UDP, 별도 静态值 부분집합 `jaot`와 게스트 C 컴파일은 [FTP·C·JAR·AOT 매뉴얼](文件传送与编译过程.md)에 설명한다. 底端值 对象值·Thread·Swing은 JVM 경로의 기능이며 AOT 支持值 범위와 같지 않다.

이 구현은 **Linux 없이 부팅한 Java AOT 커널의 EL0에서 执行命令**한다. JDK/JRE의 거의 모든 기능을 제공하는 단계는 아직 아니다. HotSpot·OpenJDK 类值 库 전체를 이식하거나 Java SE 인증/TCK를 통과한 구현도 아니다. 이번 확장은 단일 类值·静态值 方法值 중심이던 실행기를 对象值·库 执行命令 기반으로 넓힌 것이다.

## 실행과 编译源代码

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
# 内置 内核值 안에서 源代码树 编译源代码 → class 执行命令, 中文 API 调用
python3 工具集/执行文件.py 测试/Java/韩文字母源代码.java

# 对象值·异常 등은 宿主 JDK로 Java 8 class를 만든 之后状态 内置 커널에서 执行命令
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java 测试/Java/测试韩文字母.java
python3 工具集/执行文件.py build/my-java/测试韩文字母.class

# 의존 class 파일은 --include로 함께 传送值
javac --release 8 -encoding UTF-8 -d build/my-java 测试/Java/测试对象集.java
python3 工具集/执行文件.py build/my-java/测试对象集.class \
  --include build/my-java/背景值.class --include build/my-java/分支值.class \
  --include build/my-java/能够计算.class

make test-jvm
```

`--include DIR`는 그 디렉터리의 class 파일을 재귀적으로 읽어 `패키지.类值.class`라는 RAM 文件 이름으로 전송한다. 주 클래스도 패키지가 있다면 `--class-name 패키지.类值`를 지정한다. 셸에서는 해당 이름으로 업로드하고 `java 패키지.类值`로 실행한다. JVM 0.4는 Main-Class가 있는 16 KiB 이하 JAR도 `java -jar 文件.jar`로 실행한다. JAR 모드에서는 JAR 내부 클래스와 내장 中文 클래스만 찾는다. 分发值 中文 库 JAR는 宿主 javac의 classpath로 사용하며, 같은 클래스가 用户 JVM ELF에도 读取 전용 자료로 포함된다. 일반 class 모드에서는 사용자가 같은 이름으로 올린 RAM class를 먼저 읽는다.

게스트 `javac`는 여전히 静态值 方法值, int/boolean/char/String, 条件·迭代值, 字符串 合并值列, 일부 文件 스트림 등의 **内置 부분집합 编译器**第三操作数. 对象值 声明·상속·try/catch·Thread 使用值 소스를 게스트 javac가 构建全部 컴파일하는 것은 아니다. 顶端值 기능은 `javac --release 8`로 만든 class를 内置 JVM에서 실행한다. 中文 API 중 输出·字符 스칼라 函数·文件 读取/쓰기는 게스트 컴파일러에도 연결했다. 다음처럼 전체 이름으로 호출한다.

```java
public class 问候例 {
    public static void main(String[] 实参) throws Exception {
        中文.内置.输出.写入行("안녕하세요😀");
        中文.内置.输出.写入编号(中文.内置.字符.代码分个数("韩文文本😀"));
        中文.内置.文件.写入("问候例.txt", "韩文文本 文件😀");
        中文.内置.输出.写入行(中文.内置.文件.读取("问候例.txt"));
    }
}
```

## 内置 JVM에서 구현한 裁剪

| 区域值 | 제공 裁剪 |
|---|---|
| 类值 | class 버전 45…52, 여러 类值 로딩, 인스턴스/静态值 字段值, 생성자, 상속, 가상 调用, 인터페이스 调用, 静态值 初始化 |
| 值·命令 | 32비트 int 계열, boolean/byte/char/short, 引用, 1차원 数组值, 分支·switch·wide, instanceof/checkcast, category-1 操作数栈 命令 |
| 异常 | 지원하는 표준 异常 生成·throw·catch·finally, 方法值 경계를 넘는 前向值, getMessage; 底端值 限制值 引用 |
| 内存数据 | 비이동 mark/sweep GC, 빈 区域值 병합, 操作数栈·静态值 字段值·컬렉션·线程值·모니터·字符串 상수의 引用 保持值 |
| 字符串 | UTF-16, length/charAt/equals/isEmpty/substring/concat/hashCode/toString, String.valueOf(int), StringBuilder의 默认值 生成·append(int/boolean/char/String)·toString |
| 数 | Integer.parseInt/valueOf/intValue/toString, 작은 Integer 캐시, Math.abs/min/max(int) |
| 표준 输出 | System.out/err, PrintStream.print/println의 int/boolean/char/String 및 빈 println |
| 数组值 | int/byte/boolean/char/short/引用 数组值, 长度·裁剪 检查项, 引用 数组值 项目元素 类型值 检查项, System.arraycopy의 重叠区列/裁剪/项目元素 类型值 检查项 |
| 文件 | FileInputStream(String), FileOutputStream(String[,boolean]); read()/read(byte[][,offset,len]), write(int)/write(byte[][,offset,len]), close, 输出 flush. EOF는 -1 |
| 컬렉션 | ArrayList/List: add(E), get, set, remove(int), size, isEmpty, clear. HashMap/Map: put/get/remove/containsKey/size/isEmpty/clear |
| 线程值 | Thread(), Thread(Runnable), Thread 상속, start/join/isAlive/currentThread/yield; synchronized 方法值·블록의 재진입·경합·异常 시 释放存储装置 |
| UDP | DatagramSocket의 默认值/硬件端口 생성자, send/receive/close/getLocalPort/setSoTimeout; DatagramPacket의 byte[]/长度 生成 및 地址·硬件端口 头文件 生成, getData/getLength/getAddress/getPort/setLength |
| 地址 | InetAddress.getByName은 localhost/数字值 IPv4 (DNS 是否不支持), getLoopbackAddress/getHostAddress |
| 绘图 | 中文 屏幕 API가 EL0 SVC를 통해 프레임버퍼에 사각형을 绘图; 裁剪 检查项 |

컬렉션은 지정한 메서드만 제공하며 iterator/stream/对齐值·用户 定义值 equals/hashCode 콜백은 없다. 사전의 열쇠는 String/Integer/null 사용을 시험했다. UTF-16 代码值 단위와 Unicode 代码值 포인트 수는 구분한다. 韩文文本 输入值 组合·正规化值·아랍어 조판·GUI 다국어 글꼴은 이 字符串 지원과 별개다.

예외는 Throwable/Exception/RuntimeException, ArithmeticException, NullPointerException, IndexOutOfBoundsException/ArrayIndexOutOfBoundsException/StringIndexOutOfBoundsException, IllegalArgumentException/NumberFormatException/IllegalThreadStateException, IOException/FileNotFoundException, IllegalStateException, ClassCastException, NegativeArraySizeException, ArrayStoreException, UnknownHostException, SocketTimeoutException의 제한된 生成·分类值·처리를 제공한다. 用户 定义值 Throwable 상속, stack trace/cause/suppressed 异常, try-with-resources의 addSuppressed, 완전한 初始化 错误 포장은 아직 없다. 잡히지 않은 예외는 当前项目 전체 Java 실행을 실패로 끝낸다.

## 中文 API

독립 패키지 **`中文.内置`**를 사용한다. Linux판 `中文.Java`首位操作数 요구하는 NIO/Swing/HTTP API를 内置 커널에서 실행할 数 있다고 혼동하지 않도록 패키지를 나눴다. 이 라이브러리는 类值 名称·方法值·实参·字段值·文件 이름에 한국어를 사용한다. 표준 Java 类值 이름은 호환성을 위해 보존한다.

| 类值 | 공개 기능 | 이름의 의미 |
|---|---|---|
| 输出 | 写入, 写入行, 写入编号 | 输出(出力): 내용을 바깥으로 已导出值 |
| 字符 | 长度, 相等文本, 粘贴文本, 剪切值, 解析整数/写入整数值, 代码分个数, 编码/解密数据 | 字符(文字), 编码状态值(符號): 글의 단위와 그 값을 바이트로 나타내는 规则值 |
| 文件 | 读取/写入(String 名称), 读取字节值/写入字节值 | 널리 쓰는 用户 용어를 보존; RAM 자료의 名称 |
| 条目列表 | 添加值列, 读取, 替换值, 擦除条目, 大小, 是否空值, 清空内容 | 条目列表(目錄): 순서가 있는 条目值 모음 |
| 字典 | 放入值, 查找条目, 是否执行存在, 擦除条目, 大小, 清空内容 | 字典(辭典): 찾는 말인 열쇠에 값을 映射值 |
| 任务 | 运行(可运行任务任务), 等待(后台任务), 挂起任务, 是否存活 | 任务 线程值: 한 程序 안의 执行命令 流值 |
| 通信 | 打开, 发送, 接收, 超时, 关闭 | 通信(通信), 数据报(電文), 端口值: 数据 교환·메시지·포트의 역할 |
| 屏幕 | 矩形, 擦除条目 | 屏幕(畫面): 实际数据 그림을 표시하는 면 |
| 内核值 | 毫秒, 矩形 | 内置 JVM의 고정 native 连接; 일반 JNI는 아님 |

이 명명은 当前项目 기능을 설명하는 용어 선택이다. 기존 한국어에 없던 역사적 어원을 만들어 주장하지 않는다. 文件名称文本·식별자는 UTF-8 소스로 보관한다. `字符.解密数据`는 잘못된 UTF-8에 IllegalArgumentException을 던지며, `编码`는 짝이 없는 서로게이트를 `?`로 바꾼다. `文件.读取`는 엄격한 UTF-8 복호화를 적용한다. 屏幕 색은 `빨강 | (초록 << 8) | (파랑 << 16)` 형식이다.

## 执行命令 제한과 남은 任务

- 동시에 적재하는 class 最大值 16개(中文 类值 头文件), class당 16 KiB·常量值 풀 511항목, 전체 方法值/字段值 각각 512개. 方法值 代码值 8 KiB, 局部作用域 变量值·피연산자 操作数栈 각각 128슬롯, 实参 最大值 16개(this 头文件).
- VM 가닥은 main 头文件 **실행당 最大值 4개**, 가닥당 调用 深度值 32. 100개 명령마다 执行命令 대상을 바꾼다. 네이티브 调用 도중에는 전환하지 않는다. pthread/SMP/OS 스레드가 아니며 Thread.sleep/interrupt/daemon/우선순위, Object.wait/notify, java.util.concurrent는 없다.
- 对象值 힙은 32768개의 32비트 슬롯이다. 런타임의 AOT 배열은 实际数据 메모리에서 64비트 슬롯을 사용한다. GC가 있어도 대형 文件·대형 字符串·객체가 이 제한을 넘을 数 있다.
- 실행은 50만 字节码 命令 및 커널의 약 2초 EL0 기한으로 제한된다. Swing의 输入值 대기는 기한을 갱신하고 窗口 切换模式 시 중단·재개한다. 일반 服务器值·계산의 무제한 실행은 아직 없다. 是否不支持 命令·资源值 부족은 명시적인 오류로 종료한다.
- RAM 文件 最大值 64개, 파일당 16384바이트, 路径 UTF-8 63바이트. RAM 디렉터리와 对端值/절대 경로를 제공하며 영속 저장은 아직 없다. 내장 中文 class는 RAM 文件 슬롯을 소비하지 않는다. 셸의 `cd`로 정한 当前项目 경로에서 源代码树·类值·数据 파일을 읽는다.
- UDP는 Java 루프백 및 lwIP/SLIP를 통한 外部值 IPv4를 제공한다. 实际数据 GENET/Wi-Fi/DNS/TLS/HTTP 전체는 없다. 数据报 512바이트, 套接字值 8개, 소켓당 큐 4개. receive는 VM 가닥을 양보하며 대기하고 setSoTimeout을 적용하지만 전체 执行命令 기한은 여전히 적용된다.
- long/float/double, invokedynamic/람다, enum/annotation, 다차원 数组值, 완전한 数组值 공변성·인터페이스 层值 检查项, Reflection/JNI/JIT, NIO/ZIP API/Charset 전체, 보안/加密数据/국제화 전체, 전체 AWT/Swing/JavaFX는 미지원이다. Swing의 별도 支持值 부분집합은 底端值 및 开发 매뉴얼을 참고한다. 类值 文件 전체 검증기·存取条目 权限值/보호된 멤버 검사는 아직 완전하지 않다. 손상된 입력은 EL0 保护值 边界位置值 내에서 종료되도록 한다.

전체 OpenJDK를 목표로 하려면 다음은 별도의 주요 实现 단계다: 완전한 JVM 值/有效性校验/类值 로더와 异常 모델 → 영속 VFS·mmap·时钟·원자 操作值·实际数据 스레드/同步化 ABI → OpenJDK java.base 및 native 库 移植 → 设备 네트워크·TCP/IP → 窗口 시스템/字体值/입력기·java.desktop → Java SE 호환성 测试. 当前项目 内置 JVM의 일부 메서드를 더하는 것으로 이 작업이 완료되지는 않는다.

## 有效性校验

`工具集/测试JVM.py`는 같은 Java 8 class 파일의 출력을 宿主 OpenJDK `-Xverify:all`과 QEMU raspi4b 内置 커널에서 비교한다. 对象值/상속/인터페이스·switch·数组值, 异常/finally, 컬렉션/GC, Thread/锁值, 中文 UTF-8/文件/컬렉션, 实际数据 UDP 루프백/时间值 초과, 게스트 韩文文本 源代码树 编译源代码, 数组值 类型值/复制值/文件 边界位置值·韩文文本 패키지의 9개 비교 시험과 잘못된 class 버전/已裁剪值 文件 拒绝值 시험을 실행한다. UDP 项目根 실행에는 宿主 루프백 套接字值 권한이 필요하다.

`工具集/启动测试.py`는 内核值 保护值/회귀 시험과 별도로 中文 Java 屏幕 API가 实际数据 픽셀을 그렸는지도 QMP 屏幕 캡처로 검사한다. 보고서는 `build/verification/jvm/report.json`, `build/verification/report.json`이며 시험한 kernel8.img의 SHA-256을 기록한다. 实际数据 Pi4 硬件值 启动 시험과 전체 JDK 호환성 测试 결과는 아니다.


## JVM 0.3: 네트워크와 GUI 扩展名值

`Socket`/`ServerSocket` 生成·连接·accept·양방향 InputStream/OutputStream·close·EOF·时间值 제한과 UTF-8 `String.getBytes`를 추가했다. JVM 0.4에서는 外部值 数字值 IPv4 TCP도 lwIP/SLIP에 연결했다. 연결형 结束分 16개, Java 루프백 버퍼 1024바이트, 外部值 TCP 버퍼 4096바이트다. DNS·TLS는 없다.

`JFrame`, `JPanel`, `JLabel`, `JButton`, `JTextField`, `ActionListener`, `ActionEvent`, `SwingUtilities.invokeLater`의 문서화한 부분집합을 네이티브 GUI에 연결했다. `setLayout(null)`과 명시적 좌표를 사용한다. 전체 OpenJDK Swing 또는 Java SE 호환 구현은 아니다. 交互式 이벤트 대기는 执行命令 기한을 갱신하고 终端 切换模式 시 프로세스 상태를 存储值·복원한다. 이벤트 콜백 자체는 기존 字节码/CPU 기한을 따른다.

中文 `窗口`, `小组件`, `连接状态传输` 클래스를 分发值 JAR와 内置 JVM 내장 자원에 추가했다. 상세 方法值·限制值·源代码树·업로드 방법: [韩文文本 开发 매뉴얼](开发指南.md).

## 中文 객체의 직접 执行命令

`窗口`, `标签`, `文本字段`, `按钮`, `事件排队`, `动作通知`, `后台任务`은
표준 GUI/Thread 객체를 보관하는 래퍼가 아니다. 内置 JVM의 对象值 生成,
格式值 检查项, 屏幕 调用, 事件 큐, 线程值 스케줄러에 中文 계약을 직접 구현했다.
표준 `javax.swing`·`Thread` 코드의 执行命令 경로도 유지한다.
中文 단추와 표준 JButton은 서로 다른 형식이며, 해당 instanceof 검사도 검증한다.

内置 실행기의 中文 진입점은 `public static void 运行()`이다.
표준 `main(String[])`도 지원하며 二值 第三操作数 있으면 中文 진입점을 우선한다.
명령행 인수는 `运行参数.项目个数()`와 `运行参数.文本(序数索引)`으로 읽는다.
`example/java`의 다섯 예제는 이 규약을 사용한다. 静态值 文件 예제는 게스트
javac로도 컴파일하며, GUI/线程值 소스는 宿主 `javac --release 8`을 사용한다.
직접 GUI/线程值 API는 内置 JVM 전용이다. 기존 OpenJDK 비교 시험과 별도로
中文 가닥의 执行命令·等待状态值·중복 运行 拒绝值, GUI 事件 原点值·编号·콜백을 검사한다.
전체 JDK 번역이나 모든 API의 jaot 지원을 뜻하지 않는다.

方法值 이름은 바이트코드에서도 유지된다. 이름과 참조를 같이 수정하면
中文 클래스도 실행되지만, 字符串 리터럴·표준 库 재정의·native
连接·진입점은 각각 컴파일러와 실행기의 계약을 맞춰야 한다.
[상세 계약과 用例](中文Java/指南.md)를 참고한다.

## 终端 子部分值 刷新

移动值·大小 변경은 새 窗口 영역과 上一个项目 자리에서 드러난 띠만 합성한다.
1920×32 像素(240 KiB)의 临时值 그림에서 배경·겹친 窗口·字符值·GUI를 먼저
완성하고, 当前项目 显示值 메모리와 비교하여 달라진 화소만 기록한다.
32줄보다 큰 영역은 여러 띠로 처리하므로 전체 프레임을 원자적으로
교체하거나 수직 동기에 맞추는 방식은 아니다. 전체 배경을 먼저 지우는
중간 화면은 표시하지 않는다. 좌표가 같으면 重试值 그리지 않는다.

`make test-redraw`는 实际数据 C 画图屏幕 코드를 호스트의 内存数据 화면에 연결해
移动值 80회·大小 更改值 40회·겹친 窗口 4개를 전체 합성 결과와 像素 단위로 대조한다.
区域值 밖 用户 绘图, 동일 像素 무기록, 指针 밑그림, 实际数据 屏幕 行 간격을
검사한다. 이 시험의 시간은 宿主 CPU 측정이며 Pi 4/QEMU 속도로 해석하지 않는다.
`make test-resize`는 QEMU/VNC의 640×480 및 1920×1080에서 左侧 角值 拖动值,
韩文文本 输入值·vi 미저장 内容值·독립 窗口 크기를 검사한다.
