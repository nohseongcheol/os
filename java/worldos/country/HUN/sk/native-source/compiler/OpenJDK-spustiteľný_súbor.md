# 일반 Java 클래스의 Vykonať_príkaz Súbor Create_položka

OpenJDK 자체를 소스에서 만드는 기능은 [OpenJDK zdroj_strom 빌드와 vlastné jadro_VALUE 이식](OpenJDK-zdroj_zostava_AND-자체커널-이식.md)의 `openjdk-build` 대상이다. 아래 `openjdk` 대상은 Java 응용프로그램 포장 기능이다.

`--target openjdk`는 OpenJDK로 실행하는 네이티브 ELF 실행기와 `.app` údaje 폴더를 만든다. Java 바이트코드를 모두 기계어로 미리 변환하는 AOT는 아니다. objekt_VALUE·상속·인터페이스·výnimka·스레드·리플렉션·람다·표준 라이브러리는 설치된 OpenJDK가 실행하며, 필요한 코드는 JVM의 JIT가 기계어로 컴파일한다.

```sh
python3 compiler/kompilátor.py --target openjdk --entry 예제.Main \
  -o build/program_f5044b9b build/classes
./build/program_f5044b9b "Dopredu_VALUE Argumenty"
```

Pi 실행판에서는 같은 도구가 `jclassc` 명령으로 설치된다.

```sh
jclassc --target openjdk --entry Main -o program_f5044b9b Main.java
jclassc --target openjdk --entry Main -o program_f5044b9b Main.class
jclassc --target openjdk --entry Main --classpath helper.jar -o program_f5044b9b app.jar
jclassc --target openjdk --entry Main --bundle-runtime /usr/lib/jvm/java-25-jre \
  -o program_f5044b9b classes
```

입력은 `.java`, `.class`, `.jar`/`.zip`, 또는 컴파일된 클래스와 리소스가 있는 디렉터리다. Pripojiť_položka 의존성은 `--classpath`를 반복해서 지정한다. 개별 `.class` 입력은 Súbor 내부의 lekcia_VALUE 이름을 읽어 올바른 패키지 경로에 배치한다. 내부 lekcia_VALUE·다른 lekcia_VALUE·리소스까지 포함하려면 lekcia_VALUE 디렉터리를 전달한다. ZDROJ 입력은 `javac`로 컴파일한 후 포함한다.

Vykonať_príkaz Súbor `program_f5044b9b`과 `program_f5044b9b.app`를 **함께** 이동한다. v_termíne_splatnosti_položka 작업 폴더와 관계없이 자신의 경로를 기준으로 자료를 찾는다. operačný_systém·CPU는 빌드한 실행기와 일치해야 한다. `--cc`로 C 컴파일러를 지정할 수 있으며, Pi에서는 predvolená_hodnota GCC가 ARM64 실행기를 만든다. 번들 런타임을 지정하지 않으면 `JAVA_HOME/bin/java` 또는 PATH의 `java`를 사용한다.

Vykonať_príkaz 가능한 응용프로그램은 `public static void main(String[])` položka_bod_VALUE 클래스가 필요하다. knižnica·인터페이스·`module-info.class` 하나만으로 Vykonať_príkaz 프로그램이 되지는 않는다. lekcia_VALUE 버전을 지원하는 JDK, externý_VALUE JAR, JNI 네이티브 knižnica, používať_VALUE 장치와 권한은 해당 프로그램의 요구사항에 맞춰 제공해야 한다. modul_VALUE Cesta·Pripojiť_položka JVM 설정이 필요한 응용프로그램은 별도 Vykonať_príkaz 설정이 필요하다. `JDK_JAVA_OPTIONS`로 JVM 옵션을 전달할 수 있다. 모든 externý_VALUE Java 응용프로그램을 개별 검증했다는 뜻은 아니다.

기존 `linux`, `kernel`, `user` 대상은 제한형 x86 ELF32 AOT로 유지된다. 이 경로에도 `.class` 직접 입력을 추가했지만 지원하지 않는 objekt_VALUE·표준 라이브러리를 자동으로 네이티브 변환하지는 않는다. ARM64 Linux에서 사용할 때는 `openjdk` 대상을 선택한다.
