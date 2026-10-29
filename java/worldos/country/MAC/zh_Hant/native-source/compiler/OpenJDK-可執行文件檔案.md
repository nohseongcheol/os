# 일반 Java 클래스의 執行命令 檔案 創建條目

OpenJDK 자체를 소스에서 만드는 기능은 [OpenJDK 原始碼樹 빌드와 內建 內核值 移植](OpenJDK原始碼建置與核心移植.md)의 `openjdk-build` 대상이다. 底端值 `openjdk` 대상은 Java 응용프로그램 포장 기능이다.

`--target openjdk`는 OpenJDK로 실행하는 네이티브 ELF 실행기와 `.app` 資料 폴더를 만든다. Java 바이트코드를 構建全部 기계어로 미리 변환하는 AOT는 아니다. 物件值·상속·인터페이스·異常·스레드·리플렉션·람다·표준 라이브러리는 설치된 OpenJDK가 실행하며, 필요한 코드는 JVM의 JIT가 기계어로 컴파일한다.

```sh
python3 compiler/編譯器.py --target openjdk --entry 範例.Main \
  -o build/程式 build/classes
./build/程式 "前向值 實參"
```

Pi 실행판에서는 같은 도구가 `jclassc` 명령으로 설치된다.

```sh
jclassc --target openjdk --entry Main -o 程式 Main.java
jclassc --target openjdk --entry Main -o 程式 Main.class
jclassc --target openjdk --entry Main --classpath helper.jar -o 程式 app.jar
jclassc --target openjdk --entry Main --bundle-runtime /usr/lib/jvm/java-25-jre \
  -o 程式 classes
```

입력은 `.java`, `.class`, `.jar`/`.zip`, 또는 컴파일된 클래스와 리소스가 있는 디렉터리다. 追加條目 의존성은 `--classpath`를 반복해서 지정한다. 개별 `.class` 입력은 檔案 내부의 類別值 이름을 읽어 올바른 패키지 경로에 배치한다. 내부 類別值·다른 類別值·리소스까지 포함하려면 類別值 디렉터리를 전달한다. 原始碼 입력은 `javac`로 컴파일한 之後狀態 포함한다.

執行命令 檔案 `程式`과 `程式.app`를 **함께** 이동한다. 當前項目 任務 폴더와 관계없이 자신의 경로를 기준으로 자료를 찾는다. 操作系統·CPU는 빌드한 실행기와 일치해야 한다. `--cc`로 C 컴파일러를 지정할 數 있으며, Pi에서는 默認值 GCC가 ARM64 실행기를 만든다. 번들 런타임을 지정하지 않으면 `JAVA_HOME/bin/java` 또는 PATH의 `java`를 사용한다.

執行命令 가능한 응용프로그램은 `public static void main(String[])` 條目分值 클래스가 필요하다. 庫·인터페이스·`module-info.class` 하나만으로 執行命令 프로그램이 되지는 않는다. 類別值 버전을 지원하는 JDK, 外部值 JAR, JNI 네이티브 庫, 使用值 장치와 권한은 해당 프로그램의 요구사항에 맞춰 제공해야 한다. 模塊值 路徑·追加條目 JVM 설정이 필요한 응용프로그램은 별도 執行命令 설정이 필요하다. `JDK_JAVA_OPTIONS`로 JVM 옵션을 전달할 數 있다. 모든 外部值 Java 응용프로그램을 개별 검증했다는 뜻은 아니다.

기존 `linux`, `kernel`, `user` 대상은 제한형 x86 ELF32 AOT로 유지된다. 이 경로에도 `.class` 직접 입력을 추가했지만 지원하지 않는 物件值·표준 라이브러리를 자동으로 네이티브 변환하지는 않는다. ARM64 Linux에서 사용할 때는 `openjdk` 대상을 선택한다.
