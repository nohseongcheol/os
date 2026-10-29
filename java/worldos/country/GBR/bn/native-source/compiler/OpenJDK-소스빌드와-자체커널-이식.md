# OpenJDK উত্স_ট্রী 빌드와 নিজ Java কারনেল_মান 이식

**소스에서 OpenJDK를 만드는 일과, 그 결과를 নিজ 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 নিজ Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## গঠন_উত্স 경로의 সীমানির্ধারক_মান

| লক্ষ্য | 입력과 পরিমাপ | কার্যকর_করুন_আদেশ শর্ত |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → নিজ x86 AOT → ELF32 | 해당 CPU·নিজ ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | নিজ ARM64 কারনেল_মান/ব্যবহারকারী ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 উত্স_ট্রী → 공식 configure/make → JDK গঠন_ছবি | **গঠন_সিস্টেম লক্ষ্য OS/CPU의 কার্যকর_করুন_আদেশ কাজ_মান** |

OpenJDK는 Java নথির_নাম 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI সংযোগ_স্থাপনা,
শ্রেণী_মান 라이브러리의 C/C++ 구현, অ্যাপ_অ্যাপ_লঞ্চার, মডিউল_মান গঠন_ছবি 및 সৃষ্টি_করুন 도구를 함께 빌드한다.
따라서 নিজ AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK গঠন_সিস্টেম 문서](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## উত্স_ট্রী গঠন_সিস্টেম আদেশ

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ 컴파일러·Autoconf·Make와
개발 헤더를 준비한다. Swing/AWT의 Linux লাইব্রেরি 빌드에는 X11·হরফ_মান 등의
개발 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target openjdk-build \
  --java-home /পথ_2/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /পথ_2/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 উত্স_ট্রী 트리 밖의 전용 গঠন_সিস্টেম 디렉터리다.
উত্স_ট্রী·গঠন_সিস্টেম·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 গঠন_সিস্টেম 디렉터리는 재실행할 수 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI লাইব্রেরি
- `jkoros-openjdk-build.json`: স্টেজ_মান·আদেশ·উত্স_ট্রী 식별 হ্যাশ_ফাইল·성공/বিফলতা_মান·ABI 검사
- `driver-configure.log`, `images.log`: 단계별 লগ_মান

실패하면 প্রস্থান_অ্যাপ 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 গঠন_সিস্টেম 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
উত্স_ট্রী 빌드만으로 নিজ কারনেল_মান কার্যকর_করুন_আদেশ 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 최신 교차 컴파일러와 **লক্ষ্য libc/헤더/লাইব্রেরি**가 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/컴파일러.py --target openjdk-build \
  --java-home /পথ_2/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /পথ_2/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /পথ_2/OpenJDK소스
```

부트 JDK는 গঠন_সিস্টেম 호스트에서 실행된다. 교차 গঠন_সিস্টেম 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## 현재 작업 공간의 বৈধ_করুন ডাটা

분석 প্রকল্প_মূল 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[উত্স_ট্রী 출처와 다운로드 হ্যাশ_ফাইল](build/openjdk-port/source.json)를 보관한다.
গঠন_সিস্টেম 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 গঠন_সিস্টেম 호스트용이며 নিজ কারনেল_মান 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac কার্যকর_করুন_আদেশ 시험을 통과했다. 기존 컴파일러 회귀 시험과 새 গঠন_সিস্টেম পথ_2 시험도
총 **25개 পাস_মান**했다. 공식 배포 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 বৈধ_করুন লগ_সারি](build/openjdk-port/verification.json)은 গঠন_সিস্টেম 산출물과 কার্যকর_করুন_আদেশ 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[গঠন_সিস্টেম লগ_সারি](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[কার্যকর_করুন_আদেশ 시험](build/openjdk-port/smoke/report.json)을 각각 확인한다.
কার্যকর_করুন_আদেশ 시험은 새로 빌드한 java/javac로 한글 উত্স_ট্রী, long/double, UTF-8 নথির_নাম,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 প্রকৃত_ডাটা JFrame 화면 시험을 뜻하지 않는다.
Linux에서 한 시험이 নিজ কারনেল_মান 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

현재 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 수 없으며, 준비한 musl 환경 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 작업 공간에서는 পরবর্তী_দফা 단축 명령으로 같은 musl 환경을 사용한다.
ব্যবহারকারী·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 উত্স_ট্রী/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 수 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 현재 디렉터리를 유지하므로, 한글 소스도 পিয়ার_মান 경로로
컴파일하고 실행할 수 있다. 예를 들어 앞의 시험에서 생성한 소스를 다시 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/자체빌드시험.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke 자체빌드시험
```

## 기존 ARM64 OpenJDK를 নিজ 커널에 복사할 수 있는가

현재는 실행할 수 없다. 저장되어 있는 ARM64 OpenJDK 25의 স্থির_মান 검사 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
검사 도구는 কার্যকর_করুন_আদেশ 파일을 **실행하지 않고** ELF와 동적 প্রতীক·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

নিজ 커널에 직접 적재할 수 없으면 검사 결과를 저장한 ফিরে_যান_মান **প্রস্থান_অ্যাপ কোড_মান 3**을 반환한다.
ELF 호환성 검사는 প্রকৃত_ডাটা কারনেল_মান 로더의 모든 검증을 대체하지 않는다.

| 확인한 শর্ত | ARM64 OpenJDK | 현재 নিজ কারনেল_মান |
|---|---|---|
| ELF | PIE/공유 লাইব্রেরি, 동적 재배치 | 고정 ইমেইল ET_EXEC, নিজ ABI note |
| অ্যাপ_অ্যাপ_লঞ্চার | `/lib/ld-musl-aarch64.so.1` 필요 | PT_INTERP/PT_DYNAMIC/PT_TLS প্রত্যাখ্যান_মান |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 호출 | 일부 নথির_নাম·루프백·GUI SVC와 협력식 세션 |
| মেমরি_ডাটা | VM·GC·শ্রেণী_মান·কোড_মান 캐시의 동적 ইমেইল 공간 | ব্যবহারকারী 영역 16 MiB, গঠন_ছবি 영역 12 MiB |
| নথির_নাম | 큰 `lib/modules`, 공유 লাইব্রেরি 및 ডাটা | RAM নথির_নাম 하나당 16 KiB, 영속 ভাণ্ডার_মান 없음 |
| Java শ্রেণী_মান | OpenJDK 25 class 버전 69 | নিজ JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·হরফ_মান·উইন্ডো 시스템 | 별도로 구현한 Swing API 부분집합 |

প্রকৃত_ডাটা ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 현재 제한은
[ELF 로더](../platforms/rpi4-native/মেশিন/ব্যবহারকারী.c),
[ইমেইল 공간 সংজ্ঞা_মান](../platforms/rpi4-native/মেশিন/ব্যবহারকারী.h),
[RAM নথির_নাম 구현](../platforms/rpi4-native/উৎস_নথি/মেমরি_ফাইলগুলি.java),
[ব্যবহারকারী ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 수 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM নথির_নাম 업로드 제한을 피하지만,
OpenJDK에 필요한 ইমেইল 공간·스레드·동적 সংযোগ_স্থাপনা 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 অপারেটিং_সিস্টেম 호출·মেমরি_ডাটা·동적 সংযোগ_স্থাপনা 규약까지 맞지는 않는다.
নথির_নাম আকার 제한이나 ELF বিন্যাস_মান 검사만 풀어도 해결되는 문제가 아니다.

## নিজ 커널을 유지하면서 이식하는 স্টেজ_মান

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 অপারেটিং_সিস্টেম ABI를 갖춘 ব্যবহারকারী 프로그램으로 실행할 수 있다.

기술적으로는 새 운영체제용 OpenJDK হার্ডওয়্যার_পোর্ট 또는 충분한 Linux ব্যবহারকারী ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 현재 코드와 প্রকৃত_ডাটা 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **অপারেটিং_সিস্টেম ABI와 libc 기반**: 큰 নথির_নাম·ইমেইল 공간, 페이지 예약/확정/해제와 রক্ষা_করুন_মান পরিবর্তন_করা_মান,
   표준 নথির_নাম/ঘড়ি 인터페이스, ত্রুটি সূচি·C 런타임·লক্ষ্য sysroot를 구현한다.
2. **প্রকৃত_ডাটা 네이티브 스레드와 সমলয়_করা**: pthread에 대응하는 스케줄링·TLS·뮤텍스·শর্ত 변수,
   원자 অপারেশন_মান·মেমরি_ডাটা ক্রম_মান·중단/깨우기, 신호/ব্যতিক্রম 문맥과 가드 페이지를 제공한다.
   현재 vi/Swing의 입력 대기에서 문맥을 보관하는 기능만으로 대체할 수 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 লাইব্রেরি·TLS 또는 이식에 맞는 স্থির_মান সংযোগ_স্থাপনা,
   JVM 네이티브 প্রতীক 해결, 영속 নথির_নাম 시스템, 일반 프로그램의 2초 제한 재설계를 수행한다.
4. **HotSpot OS হার্ডওয়্যার_পোর্ট**: গঠন_সিস্টেম 시스템과 `src/hotspot/os`, `os_cpu`에 নিজ OS/AArch64 경계를
   구현한다. 기존 AArch64 আদেশ 생성기는 재사용할 수 있지만 OS 종속부를 구현해야 한다.
   첫 কার্যকর_করুন_আদেশ 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **শ্রেণী_মান লাইব্রেরি·javac**: java.base의 JNI/নথির_নাম/네트워크/프로세스 연결과 মডিউল_মান 적재를
   구현한 ফিরে_যান_মান নিজ কারনেল_মান 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 외부 네트워크**: AWT/Java2D의 উইন্ডো·입력·হরফ_মান 백엔드와 প্রকৃত_ডাটা NIC/TCP/IP를
   이식한다. 현재 নিজ Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **বৈধ_করুন**: 단계별 OS ABI 시험, OpenJDK jtreg 시험, GUI/한글/네트워크 부하 시험,
   প্রকৃত_ডাটা Pi4 검증을 수행한다. 일부 시험 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK কোড_মান:
[POSIX মেমরি_ডাটা·OS 구현](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS 경계](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·মেমরি_ডাটা প্রসেসর_মান_ভুক্তি](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

নিজ Java AOT 자체를 OpenJDK의 Java কোড_মান 전체를 처리하도록 확장하는 경로도 별도 개발이다.
বস্তু_মান 모델·가상/인터페이스 호출·ব্যতিক্রম·GC·long/float/double·모든 অ্যারে_মান·সমলয়_করা·동적 호출·
শ্রেণী_মান শুরু_করা/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
