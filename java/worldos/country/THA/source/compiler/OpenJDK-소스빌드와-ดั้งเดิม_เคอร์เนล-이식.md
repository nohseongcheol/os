# OpenJDK แหล่ง_ทรี 빌드와 เอง Java เคอร์เนล_ค่า 이식

**소스에서 OpenJDK를 만드는 일과, 그 결과를 เอง 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 เอง Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## คอมไพล์_แหล่ง 경로의 ตัวคั่น_ค่า

| เป้าหมาย | 입력과 ผลลัพธ์ | ดําเนินการ_คําสั่ง โรค |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → เอง x86 AOT → ELF32 | 해당 CPU·เอง ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | เอง ARM64 เคอร์เนล_ค่า/ผู้ใช้ ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 แหล่ง_ทรี → 공식 configure/make → JDK รุ่น_รูป | **สร้าง เป้าหมาย OS/CPU의 ดําเนินการ_คําสั่ง มูลค่าตามสัญญา** |

OpenJDK는 Java แฟ้ม 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI เชื่อมต่อ,
คลาส_ค่า 라이브러리의 C/C++ 구현, แอป_ลิ้นชักแอป, มอดูล_ค่า รุ่น_รูป 및 สร้าง_167eff27 도구를 함께 빌드한다.
따라서 เอง AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK สร้าง 문서](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## แหล่ง_ทรี สร้าง คําสั่ง

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ คอมไพเลอร์·Autoconf·Make와
개발 헤더를 준비한다. Swing/AWT의 Linux ไลบรารี 빌드에는 X11·ฟอนต์_ค่า 등의
개발 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/คอมไพเลอร์.py --target openjdk-build \
  --java-home /เส้นทาง/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /เส้นทาง/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 แหล่ง_ทรี 트리 밖의 전용 สร้าง 디렉터리다.
แหล่ง_ทรี·สร้าง·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 สร้าง 디렉터리는 재실행할 หมายเลข 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI ไลบรารี
- `jkoros-openjdk-build.json`: สเตจ_ค่า·คําสั่ง·แหล่ง_ทรี 식별 แฮช_แฟ้ม·성공/ความล้มเหลว_ค่า·ABI 검사
- `driver-configure.log`, `images.log`: 단계별 บันทึก_ค่า

실패하면 ออก_แอป 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 สร้าง 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
แหล่ง_ทรี 빌드만으로 เอง เคอร์เนล_ค่า ดําเนินการ_คําสั่ง 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 최신 교차 컴파일러와 **เป้าหมาย libc/헤더/ไลบรารี**가 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/คอมไพเลอร์.py --target openjdk-build \
  --java-home /เส้นทาง/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /เส้นทาง/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /เส้นทาง/OpenJDK소스
```

부트 JDK는 สร้าง 호스트에서 실행된다. 교차 สร้าง 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## ปัจจุบัน_รายการ 작업 공간의 ตรวจสอบความถูกต้อง ข้อมูล

วิเคราะห์_ค่า แสดง_ราก 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[แหล่ง_ทรี 출처와 다운로드 แฮช_แฟ้ม](build/openjdk-port/source.json)를 보관한다.
สร้าง 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 สร้าง 호스트용이며 เอง เคอร์เนล_ค่า 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac ดําเนินการ_คําสั่ง 시험을 통과했다. 기존 คอมไพเลอร์ 회귀 시험과 새 สร้าง เส้นทาง 시험도
총 **25개 ส่งต่อ_ค่า**했다. 공식 การกระจาย_ค่า 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 ตรวจสอบความถูกต้อง บันทึก_สถิติ](build/openjdk-port/verification.json)은 สร้าง 산출물과 ดําเนินการ_คําสั่ง 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[สร้าง บันทึก_สถิติ](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[ดําเนินการ_คําสั่ง 시험](build/openjdk-port/smoke/report.json)을 각각 확인한다.
ดําเนินการ_คําสั่ง 시험은 새로 빌드한 java/javac로 한글 แหล่ง_ทรี, long/double, UTF-8 แฟ้ม,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 ค่าจริง_ข้อมูล JFrame 화면 시험을 뜻하지 않는다.
Linux에서 한 시험이 เอง เคอร์เนล_ค่า 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

ปัจจุบัน_รายการ 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 หมายเลข 없으며, 준비한 musl สภาพแวดล้อม 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 작업 공간에서는 ถัดไป_รายการ 단축 명령으로 같은 musl 환경을 사용한다.
ผู้ใช้·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 แหล่ง_ทรี/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 หมายเลข 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 ปัจจุบัน_รายการ 디렉터리를 유지하므로, 한글 소스도 ชั้น_ค่า 경로로
컴파일하고 실행할 หมายเลข 있다. 예를 들어 앞의 시험에서 생성한 소스를 ลองอีกครั้ง_ค่า 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/ดั้งเดิม_รุ่น_การทดสอบ.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke ดั้งเดิม_รุ่น_การทดสอบ
```

## 기존 ARM64 OpenJDK를 เอง 커널에 복사할 หมายเลข 있는가

현재는 실행할 หมายเลข 없다. 저장되어 있는 ARM64 OpenJDK 25의 คงที่_ค่า 검사 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
검사 도구는 ดําเนินการ_คําสั่ง 파일을 **실행하지 않고** ELF와 동적 สัญลักษณ์·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

เอง 커널에 직접 적재할 หมายเลข 없으면 검사 결과를 저장한 ย้อนกลับ_ค่า **ออก_แอป รหัส_ค่า 3**을 반환한다.
ELF 호환성 검사는 ค่าจริง_ข้อมูล เคอร์เนล_ค่า 로더의 모든 검증을 대체하지 않는다.

| 확인한 โรค | ARM64 OpenJDK | ปัจจุบัน_รายการ เอง เคอร์เนล_ค่า |
|---|---|---|
| ELF | PIE/공유 ไลบรารี, 동적 재배치 | 고정 อีเมล ET_EXEC, เอง ABI note |
| แอป_ลิ้นชักแอป | `/lib/ld-musl-aarch64.so.1` 필요 | PT_INTERP/PT_DYNAMIC/PT_TLS ปฏิเสธ_ค่า |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 호출 | 일부 แฟ้ม·루프백·GUI SVC와 협력식 세션 |
| ความจํา_ข้อมูล | VM·GC·คลาส_ค่า·รหัส_ค่า 캐시의 동적 อีเมล อีเมล_ขอบเขต | ผู้ใช้ ขอบเขต_ค่า 16 MiB, รุ่น_รูป ขอบเขต_ค่า 12 MiB |
| แฟ้ม | 큰 `lib/modules`, 공유 ไลบรารี 및 ข้อมูล | RAM แฟ้ม 하나당 16 KiB, 영속 เก็บ_ค่า 없음 |
| Java คลาส_ค่า | OpenJDK 25 class 버전 69 | เอง JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·ฟอนต์_ค่า·หน้าต่าง 시스템 | 별도로 구현한 Swing API 부분집합 |

ค่าจริง_ข้อมูล ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 ปัจจุบัน_รายการ 제한은
[ELF 로더](../platforms/rpi4-native/เครื่อง/ผู้ใช้.c),
[อีเมล อีเมล_ขอบเขต คําจํากัดความ_ค่า](../platforms/rpi4-native/เครื่อง/ผู้ใช้.h),
[RAM แฟ้ม 구현](../platforms/rpi4-native/รหัสต้นฉบับ/แฟ้มในหน่วยความจํา.java),
[ผู้ใช้ ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 หมายเลข 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM แฟ้ม 업로드 제한을 피하지만,
OpenJDK에 필요한 อีเมล อีเมล_ขอบเขต·스레드·동적 เชื่อมต่อ 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 ระบบปฏิบัติการ 호출·ความจํา_ข้อมูล·동적 เชื่อมต่อ 규약까지 맞지는 않는다.
แฟ้ม ขนาด 제한이나 ELF รูปแบบ_ค่า_d1a42ea5 검사만 풀어도 해결되는 문제가 아니다.

## เอง 커널을 유지하면서 이식하는 สเตจ_ค่า

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 ระบบปฏิบัติการ ABI를 갖춘 ผู้ใช้ 프로그램으로 실행할 หมายเลข 있다.

기술적으로는 새 운영체제용 OpenJDK ฮาร์ดแวร์_แปลง 또는 충분한 Linux ผู้ใช้ ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 ปัจจุบัน_รายการ 코드와 ค่าจริง_ข้อมูล 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **ระบบปฏิบัติการ ABI와 libc 기반**: 큰 แฟ้ม·อีเมล อีเมล_ขอบเขต, 페이지 예약/확정/해제와 ป้องกัน_ค่า เปลี่ยนแปลง_ค่า,
   표준 แฟ้ม/นาฬิกา 인터페이스, ข้อผิดพลาด ดัชนี·C 런타임·เป้าหมาย sysroot를 구현한다.
2. **ค่าจริง_ข้อมูล 네이티브 스레드와 ซิงค์**: pthread에 대응하는 스케줄링·TLS·뮤텍스·โรค ตัวแปร_ค่า_541034c4,
   원자 ศัลยกรรม_ค่า·ความจํา_ข้อมูล ลําดับ_ค่า·중단/깨우기, 신호/ข้อยกเว้น 문맥과 가드 페이지를 제공한다.
   ปัจจุบัน_รายการ vi/Swing의 입력 대기에서 문맥을 보관하는 기능만으로 대체할 หมายเลข 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 ไลบรารี·TLS 또는 이식에 맞는 คงที่_ค่า เชื่อมต่อ,
   JVM 네이티브 สัญลักษณ์ 해결, 영속 แฟ้ม 시스템, 일반 프로그램의 2초 제한 재설계를 수행한다.
4. **HotSpot OS ฮาร์ดแวร์_แปลง**: สร้าง 시스템과 `src/hotspot/os`, `os_cpu`에 เอง OS/AArch64 경계를
   구현한다. 기존 AArch64 คําสั่ง 생성기는 재사용할 หมายเลข 있지만 OS 종속부를 구현해야 한다.
   첫 ดําเนินการ_คําสั่ง 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **คลาส_ค่า ไลบรารี·javac**: java.base의 JNI/แฟ้ม/네트워크/프로세스 연결과 มอดูล_ค่า 적재를
   구현한 ย้อนกลับ_ค่า เอง เคอร์เนล_ค่า 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 ภายนอก_ค่า 네트워크**: AWT/Java2D의 หน้าต่าง·입력·ฟอนต์_ค่า 백엔드와 ค่าจริง_ข้อมูล NIC/TCP/IP를
   이식한다. ปัจจุบัน_รายการ เอง Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **ตรวจสอบความถูกต้อง**: 단계별 OS ABI 시험, OpenJDK jtreg 시험, GUI/한글/네트워크 부하 시험,
   ค่าจริง_ข้อมูล Pi4 검증을 수행한다. 일부 시험 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK รหัส_ค่า:
[POSIX ความจํา_ข้อมูล·OS 구현](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS 경계](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·ความจํา_ข้อมูล กระบวนการ_ค่า_รายการ](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

เอง Java AOT 자체를 OpenJDK의 Java รหัส_ค่า 전체를 처리하도록 확장하는 경로도 별도 개발이다.
วัตถุ_ค่า 모델·가상/인터페이스 호출·ข้อยกเว้น·GC·long/float/double·모든 อาร์เรย์_ค่า·ซิงค์·동적 호출·
คลาส_ค่า เริ่มต้น/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
