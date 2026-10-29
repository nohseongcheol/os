# OpenJDK quelltextBaum 빌드와 eigen Java betriebskernWert Portierung

**소스에서 OpenJDK를 만드는 일과, 그 결과를 eigen 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 eigen Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## quelltextÜbersetzen 경로의 trennzeichenWert

| zielobjektWert | 입력과 ergebnis | befehlAusführen bedingung |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → eigen x86 AOT → ELF32 | 해당 CPU·eigen ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | eigen ARM64 betriebskernWert/Benutzer ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 quelltextBaum → 공식 configure/make → JDK abbildErzeugenAbbild | **systemErzeugenAbbild zielobjektWert OS/CPU의 befehlAusführen vertragWert** |

OpenJDK는 Java Datei 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI verbinden,
klasseWert 라이브러리의 C/C++ umsetzung, ProgrammStarter, modulWert abbildErzeugenAbbild 및 generieren 도구를 함께 빌드한다.
따라서 eigen AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK systemErzeugenAbbild Dokumentation](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## quelltextBaum systemErzeugenAbbild befehl

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ Übersetzer·Autoconf·Make와
entwicklung 헤더를 준비한다. Swing/AWT의 Linux bibliothek 빌드에는 X11·schriftartWert 등의
entwicklung 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/Übersetzer.py --target openjdk-build \
  --java-home /pfad/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /pfad/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 quelltextBaum 트리 밖의 전용 systemErzeugenAbbild 디렉터리다.
quelltextBaum·systemErzeugenAbbild·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 systemErzeugenAbbild 디렉터리는 재실행할 Zahl 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI bibliothek
- `jkoros-openjdk-build.json`: stufeWert·befehl·quelltextBaum wertIdentifizieren prüfsummeDatei·erfolgWert/fehlschlagWert·ABI Prüfpunkte
- `driver-configure.log`, `images.log`: 단계별 protokolldateiWert

실패하면 verlassenProzessProgramm 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 systemErzeugenAbbild 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
quelltextBaum 빌드만으로 eigen betriebskernWert befehlAusführen 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 neuesterWert 교차 컴파일러와 **zielobjektWert libc/헤더/bibliothek**ersterOperand 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/Übersetzer.py --target openjdk-build \
  --java-home /pfad/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /pfad/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /pfad/OpenJDK소스
```

부트 JDK는 systemErzeugenAbbild 호스트에서 실행된다. 교차 systemErzeugenAbbild 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## aktuellElementeintrag Aufgabe 공간의 validieren Daten

wertUntersuchenWert projektWurzel 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[quelltextBaum 출처와 다운로드 prüfsummeDatei](build/openjdk-port/source.json)를 보관한다.
systemErzeugenAbbild 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 systemErzeugenAbbild 호스트용이며 eigen betriebskernWert 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac befehlAusführen 시험을 통과했다. 기존 Übersetzer 회귀 시험과 새 systemErzeugenAbbild pfad 시험도
총 **25개 durchgangWert**했다. 공식 verteilungWert 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 validieren protokolldateiAufzeichnung](build/openjdk-port/verification.json)은 systemErzeugenAbbild 산출물과 befehlAusführen 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[systemErzeugenAbbild protokolldateiAufzeichnung](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[befehlAusführen Prüfungen](build/openjdk-port/smoke/report.json)을 각각 확인한다.
befehlAusführen 시험은 새로 빌드한 java/javac로 HangulText quelltextBaum, long/double, UTF-8 Datei,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 tatsächlichDaten JFrame Bildschirm 시험을 뜻하지 않는다.
Linux에서 한 시험이 eigen betriebskernWert 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

aktuellElementeintrag 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 Zahl 없으며, 준비한 musl umgebung 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 Aufgabe 공간에서는 nächsterElementeintrag 단축 명령으로 같은 musl 환경을 사용한다.
Benutzer·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 quelltextBaum/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 Zahl 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 aktuellElementeintrag 디렉터리를 유지하므로, HangulText 소스도 gegenstelleWert 경로로
컴파일하고 실행할 Zahl 있다. 예를 들어 앞의 시험에서 생성한 소스를 erneutVersuchenWert 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/SystemnahErzeugenAbbildPrüfung.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke SystemnahErzeugenAbbildPrüfung
```

## 기존 ARM64 OpenJDK를 eigen 커널에 복사할 Zahl führtAusVorhanden

현재는 실행할 Zahl 없다. 저장되어 있는 ARM64 OpenJDK 25의 statischWert Prüfpunkte 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
Prüfpunkte 도구는 befehlAusführen 파일을 **실행하지 않고** ELF와 동적 symbol·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

eigen 커널에 직접 적재할 Zahl 없으면 Prüfpunkte 결과를 저장한 rückseiteWert **verlassenProzessProgramm kodeWert 3**을 반환한다.
ELF 호환성 검사는 tatsächlichDaten betriebskernWert 로더의 모든 검증을 대체하지 않는다.

| 확인한 bedingung | ARM64 OpenJDK | aktuellElementeintrag eigen betriebskernWert |
|---|---|---|
| ELF | PIE/공유 bibliothek, 동적 재배치 | 고정 adresse ET_EXEC, eigen ABI note |
| ProgrammStarter | `/lib/ld-musl-aarch64.so.1` benötigtWert | PT_INTERP/PT_DYNAMIC/PT_TLS wertZurückweisen |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 aufrufen | 일부 Datei·루프백·GUI SVC와 협력식 세션 |
| speicherDaten | VM·GC·klasseWert·kodeWert 캐시의 동적 adresse adresseGebiet | Benutzer gebietWert 16 MiB, abbildErzeugenAbbild gebietWert 12 MiB |
| Datei | 큰 `lib/modules`, 공유 bibliothek 및 Daten | RAM Datei 하나당 16 KiB, 영속 ablegenDatenWert fehlendMethode |
| Java klasseWert | OpenJDK 25 class 버전 69 | eigen JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·schriftartWert·fenster 시스템 | 별도로 구현한 Swing API 부분집합 |

tatsächlichDaten ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 aktuellElementeintrag 제한은
[ELF 로더](../platforms/rpi4-native/maschine/Benutzer.c),
[adresse adresseGebiet definitionWert](../platforms/rpi4-native/maschine/Benutzer.h),
[RAM Datei umsetzung](../platforms/rpi4-native/Quelltext/SpeicherDateien.java),
[Benutzer ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 Zahl 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM Datei 업로드 제한을 피하지만,
OpenJDK에 필요한 adresse adresseGebiet·스레드·동적 verbinden 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 Betriebssystem aufrufen·speicherDaten·동적 verbinden 규약까지 맞지는 않는다.
Datei größe 제한이나 ELF formatWert 검사만 풀어도 해결되는 문제가 아니다.

## eigen 커널을 유지하면서 이식하는 stufeWert

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 Betriebssystem ABI를 갖춘 Benutzer 프로그램으로 실행할 Zahl 있다.

기술적으로는 새 운영체제용 OpenJDK hardwarePort 또는 충분한 Linux Benutzer ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 aktuellElementeintrag 코드와 tatsächlichDaten 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **Betriebssystem ABI와 libc grundlage**: 큰 Datei·adresse adresseGebiet, 페이지 예약/bestätigenWert/해제와 wertSchützen wertÄndern,
   표준 Datei/Uhr 인터페이스, fehler Nummer·C 런타임·zielobjektWert sysroot를 구현한다.
2. **tatsächlichDaten 네이티브 스레드와 synchronisieren**: pthread에 대응하는 스케줄링·TLS·뮤텍스·bedingung variableWert,
   원자 vorgangWert·speicherDaten reihenfolgeWert·중단/깨우기, 신호/ausnahme 문맥과 가드 페이지를 제공한다.
   aktuellElementeintrag vi/Swing의 Eingabewert 대기에서 문맥을 보관하는 기능만으로 대체할 Zahl 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 bibliothek·TLS 또는 이식에 맞는 statischWert verbinden,
   JVM 네이티브 symbol 해결, 영속 Datei 시스템, 일반 프로그램의 2초 grenzwertWert 재설계를 수행한다.
4. **HotSpot OS hardwarePort**: systemErzeugenAbbild 시스템과 `src/hotspot/os`, `os_cpu`에 eigen OS/AArch64 경계를
   구현한다. 기존 AArch64 befehl 생성기는 재사용할 Zahl 있지만 OS 종속부를 구현해야 한다.
   ersterElementeintrag befehlAusführen 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **klasseWert bibliothek·javac**: java.base의 JNI/Datei/네트워크/프로세스 연결과 modulWert 적재를
   구현한 rückseiteWert eigen betriebskernWert 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 externWert 네트워크**: AWT/Java2D의 fenster·Eingabewert·schriftartWert 백엔드와 tatsächlichDaten NIC/TCP/IP를
   이식한다. aktuellElementeintrag eigen Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **validieren**: 단계별 OS ABI Prüfungen, OpenJDK jtreg Prüfungen, GUI/HangulText/네트워크 부하 Prüfungen,
   tatsächlichDaten Pi4 검증을 수행한다. 일부 Prüfungen 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK kodeWert:
[POSIX speicherDaten·OS umsetzung](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS grenzstelleWert](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·speicherDaten prozessWertEintrag](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

eigen Java AOT 자체를 OpenJDK의 Java kodeWert 전체를 처리하도록 확장하는 경로도 별도 개발이다.
objektWert 모델·가상/인터페이스 aufrufen·ausnahme·GC·long/float/double·모든 datenfeldWert·synchronisieren·동적 aufrufen·
klasseWert initialisieren/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
