# OpenJDK fonte_árvore 빌드와 nativo Java kernel_VALOR 이식

**소스에서 OpenJDK를 만드는 일과, 그 결과를 nativo 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 nativo Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## compilar_fonte 경로의 delimitador_VALOR

| meta | 입력과 resultado | Executar_comando doença |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → nativo x86 AOT → ELF32 | 해당 CPU·nativo ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | nativo ARM64 kernel_VALOR/espaço_do_utilizador ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 fonte_árvore → 공식 configure/make → JDK BLD_foto | **construir meta OS/CPU의 Executar_comando valor_do_contrato** |

OpenJDK는 Java ficheiro 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI Ligar,
aula_VALOR 라이브러리의 C/C++ implementação, app_Launcher, módulo_VALOR BLD_foto 및 gerar 도구를 함께 빌드한다.
따라서 nativo AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK construir 문서](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## fonte_árvore construir comando

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ compilador·Autoconf·Make와
개발 헤더를 준비한다. Swing/AWT의 Linux biblioteca 빌드에는 X11·fonte_VALOR 등의
개발 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/compilador.py --target openjdk-build \
  --java-home /caminho/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /caminho/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 fonte_árvore 트리 밖의 전용 construir 디렉터리다.
fonte_árvore·construir·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 construir 디렉터리는 재실행할 número 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI biblioteca
- `jkoros-openjdk-build.json`: fase_VALOR·comando·fonte_árvore 식별 hash_Arquivo·성공/falha_VALOR·ABI 검사
- `driver-configure.log`, `images.log`: 단계별 LOG_VALOR

실패하면 sair_app 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 construir 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
fonte_árvore 빌드만으로 nativo kernel_VALOR Executar_comando 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 최신 교차 컴파일러와 **meta libc/헤더/biblioteca**가 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/compilador.py --target openjdk-build \
  --java-home /caminho/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /caminho/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /caminho/OpenJDK소스
```

부트 JDK는 construir 호스트에서 실행된다. 교차 construir 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## em_dia_item 작업 공간의 validar dados

Analisar_VALOR ação_raiz 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[fonte_árvore 출처와 다운로드 hash_Arquivo](build/openjdk-port/source.json)를 보관한다.
construir 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 construir 호스트용이며 nativo kernel_VALOR 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac Executar_comando 시험을 통과했다. 기존 compilador 회귀 시험과 새 construir caminho 시험도
총 **25개 통과**했다. 공식 distribuição_VALOR 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 validar LOG_linha](build/openjdk-port/verification.json)은 construir 산출물과 Executar_comando 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[construir LOG_linha](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[Executar_comando testes](build/openjdk-port/smoke/report.json)을 각각 확인한다.
Executar_comando 시험은 새로 빌드한 java/javac로 한글 fonte_árvore, long/double, UTF-8 ficheiro,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 real_dados JFrame tela 시험을 뜻하지 않는다.
Linux에서 한 시험이 nativo kernel_VALOR 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

em_dia_item 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 número 없으며, 준비한 musl ambiente 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 작업 공간에서는 Avançar_item 단축 명령으로 같은 musl 환경을 사용한다.
espaço_do_utilizador·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 fonte_árvore/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 número 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 em_dia_item 디렉터리를 유지하므로, 한글 소스도 par_VALOR 경로로
컴파일하고 실행할 número 있다. 예를 들어 앞의 시험에서 생성한 소스를 repetir_VALOR 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/nativo_BLD_teste.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke nativo_BLD_teste
```

## 기존 ARM64 OpenJDK를 nativo 커널에 복사할 número 있는가

현재는 실행할 número 없다. 저장되어 있는 ARM64 OpenJDK 25의 estático_VALOR 검사 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
검사 도구는 Executar_comando 파일을 **실행하지 않고** ELF와 동적 símbolo·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

nativo 커널에 직접 적재할 número 없으면 검사 결과를 저장한 BACK_VALOR **sair_app valor_do_código 3**을 반환한다.
ELF 호환성 검사는 real_dados kernel_VALOR 로더의 모든 검증을 대체하지 않는다.

| 확인한 doença | ARM64 OpenJDK | em_dia_item nativo kernel_VALOR |
|---|---|---|
| ELF | PIE/공유 biblioteca, 동적 재배치 | 고정 Endereço ET_EXEC, nativo ABI note |
| app_Launcher | `/lib/ld-musl-aarch64.so.1` 필요 | PT_INTERP/PT_DYNAMIC/PT_TLS rejeitar_VALOR |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 호출 | 일부 ficheiro·루프백·GUI SVC와 협력식 세션 |
| Memória_dados | VM·GC·aula_VALOR·valor_do_código 캐시의 동적 Endereço email_região | espaço_do_utilizador região_VALOR 16 MiB, BLD_foto região_VALOR 12 MiB |
| ficheiro | 큰 `lib/modules`, 공유 biblioteca 및 dados | RAM ficheiro 하나당 16 KiB, 영속 Store_VALOR 없음 |
| Java aula_VALOR | OpenJDK 25 class 버전 69 | nativo JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·fonte_VALOR·Janela 시스템 | 별도로 구현한 Swing API 부분집합 |

real_dados ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 em_dia_item 제한은
[ELF 로더](../platforms/rpi4-native/computador/espaço_do_utilizador.c),
[Endereço email_região Definição_VALOR](../platforms/rpi4-native/computador/espaço_do_utilizador.h),
[RAM ficheiro implementação](../platforms/rpi4-native/códigoFonte/FicheirosMemória.java),
[espaço_do_utilizador ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 número 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM ficheiro 업로드 제한을 피하지만,
OpenJDK에 필요한 Endereço email_região·스레드·동적 Ligar 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 SO 호출·Memória_dados·동적 Ligar 규약까지 맞지는 않는다.
ficheiro Tamanho 제한이나 ELF formato_VALOR 검사만 풀어도 해결되는 문제가 아니다.

## nativo 커널을 유지하면서 이식하는 fase_VALOR

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 SO ABI를 갖춘 espaço_do_utilizador 프로그램으로 실행할 número 있다.

기술적으로는 새 운영체제용 OpenJDK hardware_porta 또는 충분한 Linux espaço_do_utilizador ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 em_dia_item 코드와 real_dados 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **SO ABI와 libc 기반**: 큰 ficheiro·Endereço email_região, 페이지 예약/commit_VALOR/해제와 proteger_VALOR alterar_VALOR,
   표준 ficheiro/Relógio 인터페이스, erro ÍNDICE·C 런타임·meta sysroot를 구현한다.
2. **real_dados 네이티브 스레드와 sincronizar**: pthread에 대응하는 스케줄링·TLS·뮤텍스·doença variável_VALOR,
   원자 cirurgia_VALOR·Memória_dados ordem_VALOR·중단/깨우기, 신호/exceção 문맥과 가드 페이지를 제공한다.
   em_dia_item vi/Swing의 entrada_VALOR 대기에서 문맥을 보관하는 기능만으로 대체할 número 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 biblioteca·TLS 또는 이식에 맞는 estático_VALOR Ligar,
   JVM 네이티브 símbolo 해결, 영속 ficheiro 시스템, 일반 프로그램의 2초 제한 재설계를 수행한다.
4. **HotSpot OS hardware_porta**: construir 시스템과 `src/hotspot/os`, `os_cpu`에 nativo OS/AArch64 경계를
   구현한다. 기존 AArch64 comando 생성기는 재사용할 número 있지만 OS 종속부를 구현해야 한다.
   첫 Executar_comando 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **aula_VALOR biblioteca·javac**: java.base의 JNI/ficheiro/네트워크/프로세스 연결과 módulo_VALOR 적재를
   구현한 BACK_VALOR nativo kernel_VALOR 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 externo_VALOR 네트워크**: AWT/Java2D의 Janela·entrada_VALOR·fonte_VALOR 백엔드와 real_dados NIC/TCP/IP를
   이식한다. em_dia_item nativo Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **validar**: 단계별 OS ABI testes, OpenJDK jtreg testes, GUI/한글/네트워크 부하 testes,
   real_dados Pi4 검증을 수행한다. 일부 testes 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK valor_do_código:
[POSIX Memória_dados·OS implementação](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS limite_VALOR](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·Memória_dados Processo_VALOR_entrada](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

nativo Java AOT 자체를 OpenJDK의 Java valor_do_código 전체를 처리하도록 확장하는 경로도 별도 개발이다.
objeto_VALOR 모델·가상/인터페이스 호출·exceção·GC·long/float/double·모든 MATRIZ_VALOR·sincronizar·동적 호출·
aula_VALOR inicializar/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
