# OpenJDK မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ 빌드와 ကိုယ်ပိုင် Java အူတိုင်တန်ဖိုး 이식

**소스에서 OpenJDK를 만드는 일과, 그 결과를 ကိုယ်ပိုင် 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 ကိုယ်ပိုင် Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## မူရင်းကုဒ်ဘာသာပြန် 경로의 ပိုင်းခြားအမှတ်

| ဦးတည်ချက်တန်ဖိုး | 입력과 ရလဒ် | စက်မောင်း အခြေအနေစည်းကမ်း |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → ကိုယ်ပိုင် x86 AOT → ELF32 | 해당 CPU·ကိုယ်ပိုင် ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | ကိုယ်ပိုင် ARM64 အူတိုင်တန်ဖိုး/သုံးစွဲသူ ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ → 공식 configure/make → JDK စက်ပုံရိပ်တည်ဆောက် | **တည်ဆောက် ဦးတည်ချက်တန်ဖိုး OS/CPU의 စက်မောင်း သဘောတူစည်းမျဉ်းတန်ဖိုး** |

OpenJDK는 Java ဖိုင် 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI ချိတ်ဆက်,
အတန်းတန်ဖိုး 라이브러리의 C/C++ အကောင်အထည်ဖော်မှု, ပရိုဂရမ်စက်နှိုးကိရိယာ, မော်ဂျူးတန်ဖိုး စက်ပုံရိပ်တည်ဆောက် 및 ထုတ်လုပ် 도구를 함께 빌드한다.
따라서 ကိုယ်ပိုင် AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK တည်ဆောက် စာတမ်း](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ တည်ဆောက် အမိန့်

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ ဘာသာပြန်စက်·Autoconf·Make와
ဖွံ့ဖြိုးရေး 헤더를 준비한다. Swing/AWT의 Linux စာကြည့်တိုက် 빌드에는 X11·စာလုံးပုံစံတန်ဖိုး 등의
ဖွံ့ဖြိုးရေး 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/ဘာသာပြန်စက်.py --target openjdk-build \
  --java-home /လမ်း/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /လမ်း/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ 트리 밖의 전용 တည်ဆောက် 디렉터리다.
မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ·တည်ဆောက်·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 တည်ဆောက် 디렉터리는 재실행할 ကိန်းတန်ဖိုး 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI စာကြည့်တိုက်
- `jkoros-openjdk-build.json`: အဆင့်ကာလတန်ဖိုး·အမိန့်·မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ 식별 ဖိုင်ဟက်ရှ်တွက်·အောင်မြင်မှုတန်ဖိုး/မအောင်မြင်မှု·ABI စစ်ဆေးချက်
- `driver-configure.log`, `images.log`: 단계별 မှတ်တမ်းတန်ဖိုး

실패하면 ထွက်ပရိုဂရမ် 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 တည်ဆောက် 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ 빌드만으로 ကိုယ်ပိုင် အူတိုင်တန်ဖိုး စက်မောင်း 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 최신 교차 컴파일러와 **ဦးတည်ချက်တန်ဖိုး libc/헤더/စာကြည့်တိုက်**ပထမတွက်ချက်ခံ 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/ဘာသာပြန်စက်.py --target openjdk-build \
  --java-home /လမ်း/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /လမ်း/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /လမ်း/OpenJDK소스
```

부트 JDK는 တည်ဆောက် 호스트에서 실행된다. 교차 တည်ဆောက် 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## လက်ရှိအချက်အလက်တစ်ခု အလုပ် 공간의 မှန်ကန်ကြောင်းစစ် ဒေတာ

တန်ဖိုးခွဲခြမ်းစိတ်ဖြာ စီမံကိန်းအမြစ် 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ 출처와 다운로드 ဖိုင်ဟက်ရှ်တွက်](build/openjdk-port/source.json)를 보관한다.
တည်ဆောက် 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 တည်ဆောက် 호스트용이며 ကိုယ်ပိုင် အူတိုင်တန်ဖိုး 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac စက်မောင်း 시험을 통과했다. 기존 ဘာသာပြန်စက် 회귀 시험과 새 တည်ဆောက် လမ်း 시험도
총 **25개 အောင်တန်ဖိုး**했다. 공식 ဖြန့်ချိမှုတန်ဖိုး 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 မှန်ကန်ကြောင်းစစ် မှတ်တမ်းမှတ်တမ်းတစ်ခု](build/openjdk-port/verification.json)은 တည်ဆောက် 산출물과 စက်မောင်း 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[တည်ဆောက် မှတ်တမ်းမှတ်တမ်းတစ်ခု](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[စက်မောင်း စမ်းသပ်မှု](build/openjdk-port/smoke/report.json)을 각각 확인한다.
စက်မောင်း 시험은 새로 빌드한 java/javac로 ဟန်ဂုစာသား မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ, long/double, UTF-8 ဖိုင်,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 တကယ့်ဒေတာ JFrame မျက်နှာပြင် 시험을 뜻하지 않는다.
Linux에서 한 시험이 ကိုယ်ပိုင် အူတိုင်တန်ဖိုး 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

လက်ရှိအချက်အလက်တစ်ခု 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 ကိန်းတန်ဖိုး 없으며, 준비한 musl ဝန်းကျင် 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 အလုပ် 공간에서는 နောက်တစ်ခုအချက်အလက်တစ်ခု 단축 명령으로 같은 musl 환경을 사용한다.
သုံးစွဲသူ·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 ကိန်းတန်ဖိုး 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 လက်ရှိအချက်အလက်တစ်ခု 디렉터리를 유지하므로, ဟန်ဂုစာသား 소스도 တစ်ဖက်တန်ဖိုး 경로로
컴파일하고 실행할 ကိန်းတန်ဖိုး 있다. 예를 들어 앞의 시험에서 생성한 소스를 ပြန်ကြိုးစား 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/ကိုယ်ပိုင်တည်ဆောက်စမ်းသပ်.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke ကိုယ်ပိုင်တည်ဆောက်စမ်းသပ်
```

## 기존 ARM64 OpenJDK를 ကိုယ်ပိုင် 커널에 복사할 ကိန်းတန်ဖိုး ရှိသလား

현재는 실행할 ကိန်းတန်ဖိုး 없다. 저장되어 있는 ARM64 OpenJDK 25의 တည်ငြိမ်တန်ဖိုး စစ်ဆေးချက် 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
စစ်ဆေးချက် 도구는 စက်မောင်း 파일을 **실행하지 않고** ELF와 동적 သင်္ကေတ·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

ကိုယ်ပိုင် 커널에 직접 적재할 ကိန်းတန်ဖိုး 없으면 စစ်ဆေးချက် 결과를 저장한 နောက်တန်ဖိုး **ထွက်ပရိုဂရမ် ကုဒ်တန်ဖိုး 3**을 반환한다.
ELF 호환성 검사는 တကယ့်ဒေတာ အူတိုင်တန်ဖိုး 로더의 모든 검증을 대체하지 않는다.

| 확인한 အခြေအနေစည်းကမ်း | ARM64 OpenJDK | လက်ရှိအချက်အလက်တစ်ခု ကိုယ်ပိုင် အူတိုင်တန်ဖိုး |
|---|---|---|
| ELF | PIE/공유 စာကြည့်တိုက်, 동적 재배치 | 고정 လိပ်စာ ET_EXEC, ကိုယ်ပိုင် ABI note |
| ပရိုဂရမ်စက်နှိုးကိရိယာ | `/lib/ld-musl-aarch64.so.1` 필요 | PT_INTERP/PT_DYNAMIC/PT_TLS တန်ဖိုးငြင်းပယ် |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 ခေါ်လုပ် | 일부 ဖိုင်·루프백·GUI SVC와 협력식 세션 |
| မှတ်ဉာဏ်ဒေတာ | VM·GC·အတန်းတန်ဖိုး·ကုဒ်တန်ဖိုး 캐시의 동적 လိပ်စာ သတ်မှတ်လိပ်စာနယ် | သုံးစွဲသူ နယ်ပယ်တန်ဖိုး 16 MiB, စက်ပုံရိပ်တည်ဆောက် နယ်ပယ်တန်ဖိုး 12 MiB |
| ဖိုင် | 큰 `lib/modules`, 공유 စာကြည့်တိုက် 및 ဒေတာ | RAM ဖိုင် 하나당 16 KiB, 영속 သိုလှောင်တန်ဖိုး 없음 |
| Java အတန်းတန်ဖိုး | OpenJDK 25 class 버전 69 | ကိုယ်ပိုင် JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·စာလုံးပုံစံတန်ဖိုး·ဝင်း 시스템 | 별도로 구현한 Swing API 부분집합 |

တကယ့်ဒေတာ ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 လက်ရှိအချက်အလက်တစ်ခု 제한은
[ELF 로더](../platforms/rpi4-native/စက်/သုံးစွဲသူ.c),
[လိပ်စာ သတ်မှတ်လိပ်စာနယ် 정의](../platforms/rpi4-native/စက်/သုံးစွဲသူ.h),
[RAM ဖိုင် အကောင်အထည်ဖော်မှု](../platforms/rpi4-native/မူရင်းကုဒ်/မှတ်ဉာဏ်ဖိုင်.java),
[သုံးစွဲသူ ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 ကိန်းတန်ဖိုး 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM ဖိုင် 업로드 제한을 피하지만,
OpenJDK에 필요한 လိပ်စာ သတ်မှတ်လိပ်စာနယ်·스레드·동적 ချိတ်ဆက် 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 စက်စနစ် ခေါ်လုပ်·မှတ်ဉာဏ်ဒေတာ·동적 ချိတ်ဆက် 규약까지 맞지는 않는다.
ဖိုင် အရွယ် 제한이나 ELF ပုံစံတန်ဖိုး 검사만 풀어도 해결되는 문제가 아니다.

## ကိုယ်ပိုင် 커널을 유지하면서 이식하는 အဆင့်ကာလတန်ဖိုး

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 စက်စနစ် ABI를 갖춘 သုံးစွဲသူ 프로그램으로 실행할 ကိန်းတန်ဖိုး 있다.

기술적으로는 새 운영체제용 OpenJDK စက်ပစ္စည်းဆက်သွယ်ပေါက် 또는 충분한 Linux သုံးစွဲသူ ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 လက်ရှိအချက်အလက်တစ်ခု 코드와 တကယ့်ဒေတာ 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **စက်စနစ် ABI와 libc 기반**: 큰 ဖိုင်·လိပ်စာ သတ်မှတ်လိပ်စာနယ်, 페이지 예약/확정/해제와 တန်ဖိုးကာကွယ် တန်ဖိုးပြောင်း,
   표준 ဖိုင်/နာရီ 인터페이스, အမှား နံပါတ်·C 런타임·ဦးတည်ချက်တန်ဖိုး sysroot를 구현한다.
2. **တကယ့်ဒေတာ 네이티브 스레드와 တစ်ပြေးညီလုပ်**: pthread에 대응하는 스케줄링·TLS·뮤텍스·အခြေအနေစည်းကမ်း ကိန်းရှင်တန်ဖိုး,
   원자 တွက်ချက်လုပ်ဆောင်မှု·မှတ်ဉာဏ်ဒေတာ အစဉ်တန်ဖိုး·중단/깨우기, 신호/ခြွင်းချက် 문맥과 가드 페이지를 제공한다.
   လက်ရှိအချက်အလက်တစ်ခု vi/Swing의 ဝင်ဒေတာ 대기에서 문맥을 보관하는 기능만으로 대체할 ကိန်းတန်ဖိုး 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 စာကြည့်တိုက်·TLS 또는 이식에 맞는 တည်ငြိမ်တန်ဖိုး ချိတ်ဆက်,
   JVM 네이티브 သင်္ကေတ 해결, 영속 ဖိုင် 시스템, 일반 프로그램의 2초 ကန့်သတ်ချက်တန်ဖိုး 재설계를 수행한다.
4. **HotSpot OS စက်ပစ္စည်းဆက်သွယ်ပေါက်**: တည်ဆောက် 시스템과 `src/hotspot/os`, `os_cpu`에 ကိုယ်ပိုင် OS/AArch64 경계를
   구현한다. 기존 AArch64 အမိန့် 생성기는 재사용할 ကိန်းတန်ဖိုး 있지만 OS 종속부를 구현해야 한다.
   ပထမအချက်အလက်တစ်ခု စက်မောင်း 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **အတန်းတန်ဖိုး စာကြည့်တိုက်·javac**: java.base의 JNI/ဖိုင်/ကွန်ရက်ဆက်/프로세스 연결과 မော်ဂျူးတန်ဖိုး 적재를
   구현한 နောက်တန်ဖိုး ကိုယ်ပိုင် အူတိုင်တန်ဖိုး 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 ပြင်ပတန်ဖိုး ကွန်ရက်ဆက်**: AWT/Java2D의 ဝင်း·ဝင်ဒေတာ·စာလုံးပုံစံတန်ဖိုး 백엔드와 တကယ့်ဒေတာ NIC/TCP/IP를
   이식한다. လက်ရှိအချက်အလက်တစ်ခု ကိုယ်ပိုင် Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **မှန်ကန်ကြောင်းစစ်**: 단계별 OS ABI စမ်းသပ်မှု, OpenJDK jtreg စမ်းသပ်မှု, GUI/ဟန်ဂုစာသား/ကွန်ရက်ဆက် 부하 စမ်းသပ်မှု,
   တကယ့်ဒေတာ Pi4 검증을 수행한다. 일부 စမ်းသပ်မှု 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK ကုဒ်တန်ဖိုး:
[POSIX မှတ်ဉာဏ်ဒေတာ·OS အကောင်အထည်ဖော်မှု](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS နယ်နိမိတ်တန်ဖိုး](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·မှတ်ဉာဏ်ဒေတာ လုပ်ငန်းစဉ်တန်ဖိုးအချက်](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

ကိုယ်ပိုင် Java AOT 자체를 OpenJDK의 Java ကုဒ်တန်ဖိုး 전체를 처리하도록 확장하는 경로도 별도 개발이다.
အရာဝတ္ထုတန်ဖိုး 모델·가상/인터페이스 ခေါ်လုပ်·ခြွင်းချက်·GC·long/float/double·모든 အခင်းအကျင်းတန်ဖိုး·တစ်ပြေးညီလုပ်·동적 ခေါ်လုပ်·
အတန်းတန်ဖိုး အစပြင်ဆင်/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
