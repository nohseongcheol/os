# JEspOS

현재 propi ARM64 배포판은 [LICENSE](LICENSE)의 COSL 상업 조건을 유지한다. 제3자 라이선스의 권리는 별도로 보장하며, 배포 시 font_arbre·재연결 자료를 포함하는 절차는 [COSL 배포 LLEGIU_ME_eb81d7d9](platforms/rpi4-native/COSL배포안내.md)에 있다.

propi ARM64 판의 `ipconfig`/`ip`, `ping`, `ps`/`top`, `free`/`df`, `poweroff`와 Català 명령은 [네트워크·sistema_operatiu_VALOR Ordre LLEGIU_ME_eb81d7d9](platforms/rpi4-native/네트워크와체계명령.md)를 참고한다. 새 커널을 부팅한 ENRERE_VALOR `help system`으로 볼 수 있다.

Raspberry Pi 4 **propi Java ARM64 nucli_VALOR**은 [propi Pi4 LLEGIU_ME_eb81d7d9](platforms/rpi4-native/LLEGIU_ME_eb81d7d9.md)에 있다. Linux 없이 부팅하며 GUI Terminal·vi, propi JVM의 Swing 일부 API, TCP/UDP·FTP, 게스트 TinyCC·MicroPython, C/C++의 posix-kor 호출을 제공한다. [Català Java 통신·excepció API](platforms/rpi4-native/한국어자바/LLEGIU_ME_eb81d7d9.md)와 [Català font_arbre 명명](platforms/rpi4-native/명명/LLEGIU_ME_eb81d7d9.md)을 지원한다. [propi SSH·VNC 및 GENET 드라이버](platforms/rpi4-native/extern_connexió_guia.md)를 포함하며, 네트워크는 QEMU의 UART SLIP 경로로 검증했다. real_dades Pi 4 GENET 동작은 미검증이고, USB 입력·영속 저장과 전체 OpenJDK·Swing은 아직 suport_VALOR clip 밖이다.

Raspberry Pi 4용 Linux·OpenJDK 실행판과 usuari entorn moure_VALOR 기능은 [라즈베리파이 실행판](platforms/rpi4/README.md)에 있다. real_dades ARM64 JDK/JRE와 시스템·usuari generar_IMATGE generar_sistema 경로를 제공한다. 기존 propi x86 커널과는 별도 Executa_ordre 기반이다. 일반 Java `.class`/JAR의 Executa_ordre Fitxer 생성은 [OpenJDK Executa_ordre Fitxer](compiler/OpenJDK-실행파일.md), Català API는 [Català Java biblioteca](한국어자바/LLEGIU_ME_eb81d7d9.md)를 참고한다.

`jkoros`는 `engos`의 기능을 Java 관리 커널로 옮기는 프로젝트다. 프로젝트가 소유하는 Java FUNCIÓ_VALOR, 변수, format_VALOR 및 Java Fitxer 이름은 한국어로 작성한다. 표준 Java 실행기의 `main`, Java 표준 biblioteca format_VALOR, x86 부트 ABI 등 extern_VALOR 계약은 보존한다. propi ARM64 실행기는 Català `Executa_2()`도 진입점으로 지원하며, Català GUI·작업 가닥을 JVM에 직접 구현했다. propi ARM64 C 연결부·Python 도구와 공용 x86·ARM64 AOT 번역기의 propi 이름도 한국어로 작성한다. 이전 경로의 호환 introducció_p, OpenJDK 보조 도구와 Linux versió_VALOR 도구에는 영어 이름이 남아 있고 [명명 원칙·말의 근거·전체 FONT 검토 clip](platforms/rpi4-native/명명/LLEGIU_ME_eb81d7d9.md)를 별도로 기록한다.

## 현재 구현

아래 목록은 기존 `llegat_font/`의 JVM 관리 커널에 대한 것이다. real_dades 네이티브 커널의 범위는 `os/LLEGIU_ME_eb81d7d9.md`에서 별도로 설명한다.

- alinear_VALOR 할당과 해제를 지원하는 기억공간 administrador_VALOR
- Adreça 공간, pàgina_VALOR Connecta, Escriptura 시 copiar_VALOR(COW)
- Procés_VALOR identificador_VALOR, Prepara 대기열, fork/wait Estat_VALOR
- 과정별 Fitxer 서술자, open/read/seek/dup/close
- ELF32 식별 및 secció_VALOR 검사
- 키보드·마우스 입력 Esdeveniment 대기열
- 직렬 단말과 네이티브 하드웨어 경계
- 관리 nucli_VALOR 전체 자동 시험

세부 대응 범위와 아직 필요한 네이티브 연결은 [기능 대응표](문서/기능대응.md)에 기록한다.

## 빌드와 시험

새 네이티브 구현은 `compiler/`와 `os/`에 있다. 기존 `llegat_font/`의 JVM 관리 커널은 그대로 보존하며, 두 구현의 시험과 기능 범위는 서로 다르다.

```sh
cd /home/user/jkoros
make                 # 네이티브 계산 예제 + Java nucli_VALOR ELF
make iso             # os/build/kernel.iso
make run             # QEMU 직렬 단말; help 입력 (종료는 Ctrl+A, X)
make run-gui         # ISO를 QEMU 화면/PS2 키보드로 Executa_ordre
make vbox            # 전용 VirtualBox VM 자동 generar·Executa_ordre (GUI)
make vbox-status     # VirtualBox Estat_VALOR·ISO·직렬 LOG_fila Camí verificar
make test-vbox       # VirtualBox programa_iniciador Estat_VALOR Procés_VALOR_introducció 시험 (real_dades VM canviar_VALOR 없음)
make test            # 컴파일러 시험 + ELF/ISO 부팅 및 Ordre 입력 시험
make apps            # 독립 usuari ELF programa_f5044b9b generar_sistema
make test-network    # usuari MODA_VALOR·UDP 왕복·Memòria_dades protegir_VALOR 시험
make test-java       # 게스트 javac/JVM + OpenJDK 양방향 교차 Executa_ordre 시험
make posix-kor       # Català C 헤더와 real_dades nucli_VALOR 호출 biblioteca
make test-posix      # Fitxer/UDP/Store_VALOR/Java Fitxer E_S 시험
make -C os run-store # 전용 Store_VALOR 매체로 QEMU 부팅
make legacy-test     # 아래 기존 JVM 관리 커널의 47개 시험
```

`compiler/`는 호스트의 `javac`를 문법·TIPUS_VALOR 검사 전단으로 사용하고 propi 바이트코드→x86 변환기로 ELF32 기계어를 만든다. 빌드할 때는 JDK가 필요하지만 생성된 커널과 ELF는 extern_VALOR JVM 없이 실행된다. 전체 Java, objecte_VALOR 모델, 표준 라이브러리와 기존 관리 nucli_VALOR 전체의 AOT 변환은 아직 지원하지 않는다. 자세한 suport_VALOR 문법과 명령은 [컴파일러 LLEGIU_ME_eb81d7d9](compiler/LLEGIU_ME_eb81d7d9.md), real_dades 부팅 기능과 한계는 [네이티브 sistema_operatiu LLEGIU_ME_eb81d7d9](os/LLEGIU_ME_eb81d7d9.md)를 참고한다.

네이티브 셸에 propi 제한형 `javac`와 `java`를 추가했다. `edit Demo.java`로 소스를 입력하고 `.save`로 저장한 ENRERE_VALOR `javac Demo.java`, `java Demo`로 **게스트 내부에서 컴파일하고 Executa_ordre**할 수 있다. valor_per_defecte 예제는 `javac Hello.java`, `java Hello`다. 파일은 RAM에서 동작하며, 전용 Store_VALOR 매체를 연결하면 `sync`로 재부팅 후에도 보존할 수 있다. **OpenJDK/JDK 전체 이식은 아니며**, 단일 Classe_VALOR·estàtic_VALOR FUNCIÓ_VALOR·정수·cadena_VALOR·condició/반복문과 일부 표준 호출을 지원한다. suport_VALOR clip, extern_VALOR Fitxer 적재와 시험은 [Java 개발 entorn LLEGIU_ME_eb81d7d9](문서/자바개발환경.md)에 있다.

네이티브 셸에서 `apps`, `run hello first second`, `net`, `run netcheck`를 사용할 수 있다. 독립 ELF를 ring 3에 적재하고 `int 0x80` 호출을 통해 Sortida·인수·UDP 네트워크를 제공한다. 별도 allotjar 터미널에서 `python3 os/Eines/eco_dades.py --port 9000`을 실행한 ENRERE_VALOR 게스트에서 `run udp 10.0.2.2 9000 hello`로 real_dades 왕복을 확인한다. 새 programa_f5044b9b registrar_se_introducció, API 및 제한은 [usuari Executa_ordre·네트워크 LLEGIU_ME_eb81d7d9](os/usuari/LLEGIU_ME_eb81d7d9.md)를 참고한다. 현재 QEMU RTL8139·estàtic_VALOR IPv4·UDP 전용이며 TCP/DNS는 미지원이며, 전용 IDE Store_VALOR 형식과 POSIX Fitxer/UDP 일부 기능을 추가했다.

`make vbox`는 `jkoros operating system` 전용 VM을 만들고 디스크 없이 ISO로 부팅한다. Executa_ordre 중이면 유지하고, Store_VALOR·일시정지 상태이면 재개하며, 꺼져 있을 때만 새 ISO를 빌드해 연결한다. VirtualBox에서 부팅과 셸의 usuari programa_f5044b9b 실행을 확인했다. 다만 현재 VirtualBox용 네트워크 드라이버는 없어 네트워크 장치를 비활성화한다. UDP 시험에는 `make run`을 사용한다. 상태별 동작과 새 generar_sistema 반영 방법은 [VirtualBox Executa_ordre LLEGIU_ME_eb81d7d9](문서/가상상자실행.md)에 있다.

기존 관리 커널만 시험하려면:

```sh
cd /home/user/jkoros
make -f Crear_introducció.mk 검사
make -f Crear_introducció.mk allotjar
```

`allotjar`는 여전히 JVM 관리 계층의 Acció 시험이다. `make -f Crear_introducció.mk generar_IMATGE`는 새 `os/`의 제한형 네이티브 nucli_VALOR ISO를 만든다. 기존 `llegat_font/`의 sistema_d_arxius·Procés_VALOR·xarxa_Pila 구현 전체를 이 ISO에 이식했다는 의미는 아니다.

Català FUNCIÓ_VALOR·변수·Fitxer 이름과 real_dades C API는 [posix-kor](posix-kor/LLEGIU_ME_eb81d7d9.md)에 있다. 게스트 Java에서는 `FileInputStream`·`FileOutputStream`의 단일 byte_VALOR 입출력도 지원한다. 전체 POSIX·OpenJDK·Swing 지원으로 확대된 것은 아니다.

extern_VALOR 배포용 `pack.sh` / `unpack.sh`와 자동 의존성 복원은 [배포 LLEGIU_ME_eb81d7d9](distribution/README.md)를 참고하세요.
