# OpenJDK джерело_дерево 빌드와 своє Java ядро_значення 이식

**소스에서 OpenJDK를 만드는 일과, 그 결과를 своє 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 своє Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## компілювати_джерело 경로의 роздільник_значення

| мета | 입력과 результат | Виконати_команда умова |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → своє x86 AOT → ELF32 | 해당 CPU·своє ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | своє ARM64 ядро_значення/простір_користувача ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 джерело_дерево → 공식 configure/make → JDK збірка_фото | **збирання мета OS/CPU의 Виконати_команда контракт_значення** |

OpenJDK는 Java файл 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI З_єднання,
Клас_значення 라이브러리의 C/C++ реалізація, програма_запускач, модуль_значення збірка_фото 및 генерувати 도구를 함께 빌드한다.
따라서 своє AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK збирання 문서](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## джерело_дерево збирання команда

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ компілятор·Autoconf·Make와
개발 헤더를 준비한다. Swing/AWT의 Linux бібліотека 빌드에는 X11·шрифт_значення 등의
개발 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/компілятор.py --target openjdk-build \
  --java-home /шлях/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /шлях/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 джерело_дерево 트리 밖의 전용 збирання 디렉터리다.
джерело_дерево·збирання·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 збирання 디렉터리는 재실행할 수 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI бібліотека
- `jkoros-openjdk-build.json`: етап_значення·команда·джерело_дерево 식별 геш_код_Файл·성공/неполадка_значення·ABI 검사
- `driver-configure.log`, `images.log`: 단계별 журнал_значення

실패하면 Вийти_програма 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 збирання 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
джерело_дерево 빌드만으로 своє ядро_значення Виконати_команда 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 최신 교차 컴파일러와 **мета libc/헤더/бібліотека**가 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/компілятор.py --target openjdk-build \
  --java-home /шлях/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /шлях/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /шлях/OpenJDK소스
```

부트 JDK는 збирання 호스트에서 실행된다. 교차 збирання 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## чинний_елемент 작업 공간의 затвердити дані

Аналіз_значення Дії_корінь 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[джерело_дерево 출처와 다운로드 геш_код_Файл](build/openjdk-port/source.json)를 보관한다.
збирання 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 збирання 호스트용이며 своє ядро_значення 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac Виконати_команда 시험을 통과했다. 기존 компілятор 회귀 시험과 새 збирання шлях 시험도
총 **25개 передавати_значення**했다. 공식 배포 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 затвердити журнал_запис](build/openjdk-port/verification.json)은 збирання 산출물과 Виконати_команда 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[збирання журнал_запис](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[Виконати_команда випробування](build/openjdk-port/smoke/report.json)을 각각 확인한다.
Виконати_команда 시험은 새로 빌드한 java/javac로 한글 джерело_дерево, long/double, UTF-8 файл,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 фактично_дані JFrame 화면 시험을 뜻하지 않는다.
Linux에서 한 시험이 своє ядро_значення 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

чинний_елемент 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 수 없으며, 준비한 musl середовище 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 작업 공간에서는 Далі_елемент 단축 명령으로 같은 musl 환경을 사용한다.
простір_користувача·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 джерело_дерево/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 수 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 чинний_елемент 디렉터리를 유지하므로, 한글 소스도 точка_значення 경로로
컴파일하고 실행할 수 있다. 예를 들어 앞의 시험에서 생성한 소스를 пробувати_знову_значення 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/자체빌드시험.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke 자체빌드시험
```

## 기존 ARM64 OpenJDK를 своє 커널에 복사할 수 있는가

현재는 실행할 수 없다. 저장되어 있는 ARM64 OpenJDK 25의 정적 검사 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
검사 도구는 Виконати_команда 파일을 **실행하지 않고** ELF와 동적 символ·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

своє 커널에 직접 적재할 수 없으면 검사 결과를 저장한 НАЗАД_значення **Вийти_програма код_значення 3**을 반환한다.
ELF 호환성 검사는 фактично_дані ядро_значення 로더의 모든 검증을 대체하지 않는다.

| 확인한 умова | ARM64 OpenJDK | чинний_елемент своє ядро_значення |
|---|---|---|
| ELF | PIE/공유 бібліотека, 동적 재배치 | 고정 Адреса ET_EXEC, своє ABI note |
| програма_запускач | `/lib/ld-musl-aarch64.so.1` 필요 | PT_INTERP/PT_DYNAMIC/PT_TLS відхилити_значення |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 호출 | 일부 файл·루프백·GUI SVC와 협력식 세션 |
| Пам_ять_дані | VM·GC·Клас_значення·код_значення 캐시의 동적 Адреса адреса_область | простір_користувача область_значення_0e9a97ab 16 MiB, збірка_фото область_значення_0e9a97ab 12 MiB |
| файл | 큰 `lib/modules`, 공유 бібліотека 및 дані | RAM файл 하나당 16 KiB, 영속 сховище_значення 없음 |
| Java Клас_значення | OpenJDK 25 class 버전 69 | своє JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·шрифт_значення·Вікно 시스템 | 별도로 구현한 Swing API 부분집합 |

фактично_дані ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 чинний_елемент 제한은
[ELF 로더](../platforms/rpi4-native/комп_ютер/простір_користувача.c),
[Адреса адреса_область Визначення_значення](../platforms/rpi4-native/комп_ютер/простір_користувача.h),
[RAM файл реалізація](../platforms/rpi4-native/вихіднийКод/ФайлиПамʼяті.java),
[простір_користувача ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 수 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM файл 업로드 제한을 피하지만,
OpenJDK에 필요한 Адреса адреса_область·스레드·동적 З_єднання 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 операційна_система_ОС 호출·Пам_ять_дані·동적 З_єднання 규약까지 맞지는 않는다.
файл Розмір 제한이나 ELF формат_значення 검사만 풀어도 해결되는 문제가 아니다.

## своє 커널을 유지하면서 이식하는 етап_значення

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 операційна_система_ОС ABI를 갖춘 простір_користувача 프로그램으로 실행할 수 있다.

기술적으로는 새 운영체제용 OpenJDK обладнання_порт 또는 충분한 Linux простір_користувача ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 чинний_елемент 코드와 фактично_дані 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **операційна_система_ОС ABI와 libc 기반**: 큰 файл·Адреса адреса_область, 페이지 예약/затвердження_значення/해제와 захищати_значення змінювати_значення,
   표준 файл/Годинник 인터페이스, ПОМИЛКА індекс·C 런타임·мета sysroot를 구현한다.
2. **фактично_дані 네이티브 스레드와 синхронізувати**: pthread에 대응하는 스케줄링·TLS·뮤텍스·умова змінна_значення,
   원자 операція_значення·Пам_ять_дані порядок_значення·중단/깨우기, 신호/виняток 문맥과 가드 페이지를 제공한다.
   чинний_елемент vi/Swing의 입력 대기에서 문맥을 보관하는 기능만으로 대체할 수 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 бібліотека·TLS 또는 이식에 맞는 정적 З_єднання,
   JVM 네이티브 символ 해결, 영속 файл 시스템, 일반 프로그램의 2초 제한 재설계를 수행한다.
4. **HotSpot OS обладнання_порт**: збирання 시스템과 `src/hotspot/os`, `os_cpu`에 своє OS/AArch64 경계를
   구현한다. 기존 AArch64 команда 생성기는 재사용할 수 있지만 OS 종속부를 구현해야 한다.
   첫 Виконати_команда 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **Клас_значення бібліотека·javac**: java.base의 JNI/файл/네트워크/프로세스 연결과 модуль_значення 적재를
   구현한 НАЗАД_значення своє ядро_значення 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 зовнішній_значення 네트워크**: AWT/Java2D의 Вікно·입력·шрифт_значення 백엔드와 фактично_дані NIC/TCP/IP를
   이식한다. чинний_елемент своє Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **затвердити**: 단계별 OS ABI випробування, OpenJDK jtreg випробування, GUI/한글/네트워크 부하 випробування,
   фактично_дані Pi4 검증을 수행한다. 일부 випробування 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK код_значення:
[POSIX Пам_ять_дані·OS реалізація](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS 경계](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·Пам_ять_дані процес_значення_запис](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

своє Java AOT 자체를 OpenJDK의 Java код_значення 전체를 처리하도록 확장하는 경로도 별도 개발이다.
об_єкт_значення 모델·가상/인터페이스 호출·виняток·GC·long/float/double·모든 масив_значення·синхронізувати·동적 호출·
Клас_значення ініціалізувати/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
