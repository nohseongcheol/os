# 일반 Java 클래스의 thựcThiLệnh Tệp tạoMục

OpenJDK 자체를 소스에서 만드는 기능은 [OpenJDK câyNguồn 빌드와 tựThân giáTrịNhân ChuyểnNền](OpenJDK-VàXâyDựngNguồn-NhânBảnĐịa-ChuyểnNền.md)의 `openjdk-build` 대상이다. giáTrịĐáy `openjdk` 대상은 Java 응용프로그램 포장 기능이다.

`--target openjdk`는 OpenJDK로 실행하는 네이티브 ELF 실행기와 `.app` DữLiệu 폴더를 만든다. Java 바이트코드를 xâyDựngTấtCả 기계어로 미리 변환하는 AOT는 아니다. giáTrịĐốiTượng·상속·인터페이스·ngoạiLệ·스레드·리플렉션·람다·표준 라이브러리는 설치된 OpenJDK가 실행하며, 필요한 코드는 JVM의 JIT가 기계어로 컴파일한다.

```sh
python3 compiler/TrìnhBiênDịch.py --target openjdk --entry VíDụ.Main \
  -o build/ChươngTrình build/classes
./build/ChươngTrình "giáTrịTiến cácĐốiSố"
```

Pi 실행판에서는 같은 도구가 `jclassc` 명령으로 설치된다.

```sh
jclassc --target openjdk --entry Main -o ChươngTrình Main.java
jclassc --target openjdk --entry Main -o ChươngTrình Main.class
jclassc --target openjdk --entry Main --classpath helper.jar -o ChươngTrình app.jar
jclassc --target openjdk --entry Main --bundle-runtime /usr/lib/jvm/java-25-jre \
  -o ChươngTrình classes
```

입력은 `.java`, `.class`, `.jar`/`.zip`, 또는 컴파일된 클래스와 리소스가 있는 디렉터리다. thêmCuốiMục 의존성은 `--classpath`를 반복해서 지정한다. 개별 `.class` 입력은 Tệp 내부의 giáTrịLớp 이름을 읽어 올바른 패키지 경로에 배치한다. 내부 giáTrịLớp·다른 giáTrịLớp·리소스까지 포함하려면 giáTrịLớp 디렉터리를 전달한다. mãNguồn 입력은 `javac`로 컴파일한 trạngTháiSau 포함한다.

thựcThiLệnh Tệp `ChươngTrình`과 `ChươngTrình.app`를 **함께** 이동한다. phầnMụcHiệnTại TácVụ 폴더와 관계없이 자신의 경로를 기준으로 자료를 찾는다. HệĐiềuHành·CPU는 빌드한 실행기와 일치해야 한다. `--cc`로 C 컴파일러를 지정할 trịSố 있으며, Pi에서는 giáTrịMặcĐịnh GCC가 ARM64 실행기를 만든다. 번들 런타임을 지정하지 않으면 `JAVA_HOME/bin/java` 또는 PATH의 `java`를 사용한다.

thựcThiLệnh 가능한 응용프로그램은 `public static void main(String[])` giáTrịĐiểmMục 클래스가 필요하다. thưViện·인터페이스·`module-info.class` 하나만으로 thựcThiLệnh 프로그램이 되지는 않는다. giáTrịLớp 버전을 지원하는 JDK, giáTrịBênNgoài JAR, JNI 네이티브 thưViện, giáTrịDùng 장치와 권한은 해당 프로그램의 요구사항에 맞춰 제공해야 한다. giáTrịMôĐun đườngDẫn·thêmCuốiMục JVM 설정이 필요한 응용프로그램은 별도 thựcThiLệnh 설정이 필요하다. `JDK_JAVA_OPTIONS`로 JVM 옵션을 전달할 trịSố 있다. 모든 giáTrịBênNgoài Java 응용프로그램을 개별 검증했다는 뜻은 아니다.

기존 `linux`, `kernel`, `user` 대상은 제한형 x86 ELF32 AOT로 유지된다. 이 경로에도 `.class` 직접 입력을 추가했지만 지원하지 않는 giáTrịĐốiTượng·표준 라이브러리를 자동으로 네이티브 변환하지는 않는다. ARM64 Linux에서 사용할 때는 `openjdk` 대상을 선택한다.
