# 일반 Java 클래스의 ṣiṣẹ́_àṣẹ Fáìlì Ṣẹ̀dá_ìgbéwọlé

OpenJDK 자체를 소스에서 만드는 기능은 [OpenJDK orísun_ètò_afigijúwe 빌드와 자체 kánẹ́ẹ̀lì_iye 이식](OpenJDK-소스빌드와-자체커널-이식.md)의 `openjdk-build` 대상이다. 아래 `openjdk` 대상은 Java 응용프로그램 포장 기능이다.

`--target openjdk`는 OpenJDK로 실행하는 네이티브 ELF 실행기와 `.app` détà 폴더를 만든다. Java 바이트코드를 모두 기계어로 미리 변환하는 AOT는 아니다. nǹkan_iye·상속·인터페이스·예외·스레드·리플렉션·람다·표준 라이브러리는 설치된 OpenJDK가 실행하며, 필요한 코드는 JVM의 JIT가 기계어로 컴파일한다.

```sh
python3 compiler/컴파일러.py --target openjdk --entry 예제.Main \
  -o build/àtòjọ_ètò_f5044b9b build/classes
./build/àtòjọ_ètò_f5044b9b "tari_sí_iye 인수"
```

Pi 실행판에서는 같은 도구가 `jclassc` 명령으로 설치된다.

```sh
jclassc --target openjdk --entry Main -o àtòjọ_ètò_f5044b9b Main.java
jclassc --target openjdk --entry Main -o àtòjọ_ètò_f5044b9b Main.class
jclassc --target openjdk --entry Main --classpath helper.jar -o àtòjọ_ètò_f5044b9b app.jar
jclassc --target openjdk --entry Main --bundle-runtime /usr/lib/jvm/java-25-jre \
  -o àtòjọ_ètò_f5044b9b classes
```

입력은 `.java`, `.class`, `.jar`/`.zip`, 또는 컴파일된 클래스와 리소스가 있는 디렉터리다. 추가 의존성은 `--classpath`를 반복해서 지정한다. 개별 `.class` 입력은 Fáìlì 내부의 ọ̀wọ́_iye 이름을 읽어 올바른 패키지 경로에 배치한다. 내부 ọ̀wọ́_iye·다른 ọ̀wọ́_iye·리소스까지 포함하려면 ọ̀wọ́_iye 디렉터리를 전달한다. orísun 입력은 `javac`로 컴파일한 후 포함한다.

ṣiṣẹ́_àṣẹ Fáìlì `àtòjọ_ètò_f5044b9b`과 `àtòjọ_ètò_f5044b9b.app`를 **함께** 이동한다. 현재 작업 폴더와 관계없이 자신의 경로를 기준으로 자료를 찾는다. OS·CPU는 빌드한 실행기와 일치해야 한다. `--cc`로 C 컴파일러를 지정할 수 있으며, Pi에서는 àdáwọ̀ GCC가 ARM64 실행기를 만든다. 번들 런타임을 지정하지 않으면 `JAVA_HOME/bin/java` 또는 PATH의 `java`를 사용한다.

ṣiṣẹ́_àṣẹ 가능한 응용프로그램은 `public static void main(String[])` ìgbéwọlé_kókó_iye 클래스가 필요하다. ibi_ìpamọ́·인터페이스·`module-info.class` 하나만으로 ṣiṣẹ́_àṣẹ 프로그램이 되지는 않는다. ọ̀wọ́_iye 버전을 지원하는 JDK, 외부 JAR, JNI 네이티브 ibi_ìpamọ́, 사용 장치와 권한은 해당 프로그램의 요구사항에 맞춰 제공해야 한다. 모듈 ọ̀nà·추가 JVM 설정이 필요한 응용프로그램은 별도 ṣiṣẹ́_àṣẹ 설정이 필요하다. `JDK_JAVA_OPTIONS`로 JVM 옵션을 전달할 수 있다. 모든 외부 Java 응용프로그램을 개별 검증했다는 뜻은 아니다.

기존 `linux`, `kernel`, `user` 대상은 제한형 x86 ELF32 AOT로 유지된다. 이 경로에도 `.class` 직접 입력을 추가했지만 지원하지 않는 nǹkan_iye·표준 라이브러리를 자동으로 네이티브 변환하지는 않는다. ARM64 Linux에서 사용할 때는 `openjdk` 대상을 선택한다.
