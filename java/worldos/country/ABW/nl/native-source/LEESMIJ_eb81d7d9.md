# JAbwOS

actueel_item Eigen ARM64 배포판은 [LICENSE](LICENSE)의 COSL 상업 조건을 유지한다. 제3자 라이선스의 권리는 별도로 보장하며, distributie_WAARDE 시 bron_structuur·재연결 자료를 포함하는 절차는 [COSL distributie_WAARDE LEESMIJ_eb81d7d9](platforms/rpi4-native/COSL배포안내.md)에 있다.

Eigen ARM64 판의 `ipconfig`/`ip`, `ping`, `ps`/`top`, `free`/`df`, `poweroff`와 Nederlands 명령은 [네트워크·besturingssysteem_WAARDE opdracht LEESMIJ_eb81d7d9](platforms/rpi4-native/네트워크와체계명령.md)를 참고한다. 새 커널을 부팅한 BACK_WAARDE `help system`으로 볼 nummer 있다.

Raspberry Pi 4 **Eigen Java ARM64 kernel_WAARDE**은 [Eigen Pi4 LEESMIJ_eb81d7d9](platforms/rpi4-native/LEESMIJ_eb81d7d9.md)에 있다. Linux 없이 부팅하며 GUI terminal·vi, Eigen JVM의 Swing 일부 API, TCP/UDP·FTP, 게스트 TinyCC·MicroPython, C/C++의 posix-kor 호출을 제공한다. [Nederlands Java communicatie·uitzondering API](platforms/rpi4-native/한국어자바/LEESMIJ_eb81d7d9.md)와 [Nederlands bron_structuur 명명](platforms/rpi4-native/명명/LEESMIJ_eb81d7d9.md)을 지원한다. [Eigen SSH·VNC 및 GENET 드라이버](platforms/rpi4-native/extern_verbinding_guide.md)를 포함하며, 네트워크는 QEMU의 UART SLIP 경로로 검증했다. werkelijk_gegevens Pi 4 GENET 동작은 미검증이고, USB invoer_WAARDE·영속 저장과 전체 OpenJDK·Swing은 아직 steun_WAARDE clip 밖이다.

Raspberry Pi 4용 Linux·OpenJDK 실행판과 gebruikersruimte omgeving verplaatsen_WAARDE_83b651b8 기능은 [라즈베리파이 실행판](platforms/rpi4/README.md)에 있다. werkelijk_gegevens ARM64 JDK/JRE와 시스템·gebruikersruimte build_kopie bouwen 경로를 제공한다. 기존 Eigen x86 커널과는 별도 Uitvoeren_opdracht 기반이다. 일반 Java `.class`/JAR의 Uitvoeren_opdracht bestand 생성은 [OpenJDK Uitvoeren_opdracht bestand](compiler/OpenJDK-uitvoerbaar_bestand.md), Nederlands API는 [Nederlands Java bibliotheek](한국어자바/LEESMIJ_eb81d7d9.md)를 참고한다.

`jkoros`는 `engos`의 기능을 Java 관리 커널로 옮기는 프로젝트다. 프로젝트가 소유하는 Java FUNCTIE_WAARDE, variabele_WAARDE, opmaak_WAARDE 및 Java bestand 이름은 한국어로 작성한다. 표준 Java 실행기의 `main`, Java 표준 bibliotheek opmaak_WAARDE, x86 부트 ABI 등 extern_WAARDE 계약은 보존한다. Eigen ARM64 실행기는 Nederlands `starten()`도 진입점으로 지원하며, Nederlands GUI·작업 가닥을 JVM에 직접 구현했다. Eigen ARM64 C 연결부·Python 도구와 공용 x86·ARM64 AOT 번역기의 Eigen 이름도 한국어로 작성한다. Vorige_item 경로의 호환 beginpunt, OpenJDK 보조 도구와 Linux versie_WAARDE 도구에는 영어 이름이 남아 있고 [명명 원칙·말의 근거·전체 broncode 검토 clip](platforms/rpi4-native/명명/LEESMIJ_eb81d7d9.md)를 별도로 기록한다.

## actueel_item implementatie

아래 목록은 기존 `verouderd_bron/`의 JVM 관리 커널에 대한 것이다. werkelijk_gegevens 네이티브 커널의 범위는 `os/LEESMIJ_eb81d7d9.md`에서 별도로 설명한다.

- uitlijnen_WAARDE 할당과 해제를 지원하는 Geheugen_regio Manager_WAARDE
- ADRES ADRES_regio, page_WAARDE Verbinden, Schrijven 시 kopiëren_WAARDE(COW)
- Proces_WAARDE id_WAARDE, Bereid_voor 대기열, fork/wait Status_WAARDE
- 과정별 bestand 서술자, open/read/seek/dup/close
- ELF32 식별 및 sectie_WAARDE 검사
- 키보드·마우스 invoer_WAARDE Gebeurtenis 대기열
- 직렬 단말과 네이티브 hardware_WAARDE grens_WAARDE
- 관리 kernel_WAARDE 전체 자동 tests

세부 toewijzing_WAARDE 범위와 아직 필요한 네이티브 연결은 [기능 대응표](Guides/functie_toewijzing.md)에 기록한다.

## 빌드와 tests

새 네이티브 구현은 `compiler/`와 `os/`에 있다. 기존 `verouderd_bron/`의 JVM 관리 커널은 그대로 보존하며, 두 구현의 시험과 기능 범위는 서로 다르다.

```sh
cd /home/user/jkoros
make                 # 네이티브 계산 예제 + Java kernel_WAARDE ELF
make iso             # os/build/kernel.iso
make run             # QEMU 직렬 단말; help invoer_WAARDE (종료는 Ctrl+A, X)
make run-gui         # ISO를 QEMU scherm/PS2 키보드로 Uitvoeren_opdracht
make vbox            # 전용 VirtualBox VM 자동 genereren·Uitvoeren_opdracht (GUI)
make vbox-status     # VirtualBox Status_WAARDE·ISO·직렬 LOG_RECORD pad bevestigen
make test-vbox       # VirtualBox app_app_lade Status_WAARDE Proces_WAARDE_invoer tests (werkelijk_gegevens VM wijzigen_WAARDE 없음)
make test            # compiler tests + ELF/ISO machineopstart 및 opdracht invoer_WAARDE tests
make apps            # 독립 gebruikersruimte ELF app_f5044b9b bouwen
make test-network    # gebruikersruimte MODUS_WAARDE·UDP 왕복·Geheugen_gegevens beschermen_WAARDE tests
make test-java       # 게스트 javac/JVM + OpenJDK 양방향 교차 Uitvoeren_opdracht tests
make posix-kor       # Nederlands C 헤더와 werkelijk_gegevens kernel_WAARDE 호출 bibliotheek
make test-posix      # bestand/UDP/Store_WAARDE/Java bestand I_O tests
make -C os run-store # 전용 Store_WAARDE 매체로 QEMU machineopstart
make legacy-test     # 아래 기존 JVM 관리 커널의 47개 tests
```

`compiler/`는 호스트의 `javac`를 문법·TYPE_WAARDE 검사 전단으로 사용하고 Eigen 바이트코드→x86 변환기로 ELF32 기계어를 만든다. 빌드할 때는 JDK가 필요하지만 생성된 커널과 ELF는 extern_WAARDE JVM 없이 실행된다. 전체 Java, object_WAARDE 모델, 표준 라이브러리와 기존 관리 kernel_WAARDE 전체의 AOT 변환은 아직 지원하지 않는다. 자세한 steun_WAARDE 문법과 명령은 [compiler LEESMIJ_eb81d7d9](compiler/LEESMIJ_eb81d7d9.md), werkelijk_gegevens machineopstart 기능과 한계는 [네이티브 besturingssysteem LEESMIJ_eb81d7d9](os/LEESMIJ_eb81d7d9.md)를 참고한다.

네이티브 셸에 Eigen 제한형 `javac`와 `java`를 추가했다. `edit Demo.java`로 소스를 입력하고 `.save`로 저장한 BACK_WAARDE `javac Demo.java`, `java Demo`로 **게스트 내부에서 컴파일하고 Uitvoeren_opdracht**할 nummer 있다. standaardwaarde 예제는 `javac Hello.java`, `java Hello`다. 파일은 RAM에서 동작하며, 전용 Store_WAARDE 매체를 연결하면 `sync`로 재부팅 후에도 보존할 nummer 있다. **OpenJDK/JDK 전체 이식은 아니며**, 단일 les_WAARDE·statisch_WAARDE FUNCTIE_WAARDE·geheel_getal·tekenreeks_WAARDE·toestand/반복문과 일부 표준 호출을 지원한다. steun_WAARDE clip, extern_WAARDE bestand 적재와 시험은 [Java ontwikkeling omgeving LEESMIJ_eb81d7d9](Guides/Java_IDE.md)에 있다.

네이티브 셸에서 `apps`, `run hello first second`, `net`, `run netcheck`를 사용할 nummer 있다. 독립 ELF를 ring 3에 적재하고 `int 0x80` 호출을 통해 tekstuitvoer·argumenten·UDP 네트워크를 제공한다. 별도 host 터미널에서 `python3 os/hulpmiddelen/echo_gegevens.py --port 9000`을 실행한 BACK_WAARDE 게스트에서 `run udp 10.0.2.2 9000 hello`로 werkelijk_gegevens 왕복을 확인한다. 새 app_f5044b9b register_invoer, API 및 제한은 [gebruikersruimte Uitvoeren_opdracht·네트워크 LEESMIJ_eb81d7d9](os/gebruikersruimte/LEESMIJ_eb81d7d9.md)를 참고한다. actueel_item QEMU RTL8139·statisch_WAARDE IPv4·UDP 전용이며 TCP/DNS는 미지원이며, 전용 IDE Store_WAARDE 형식과 POSIX bestand/UDP 일부 기능을 추가했다.

`make vbox`는 `jkoros operating system` 전용 VM을 만들고 디스크 없이 ISO로 부팅한다. Uitvoeren_opdracht 중이면 유지하고, Store_WAARDE·일시정지 상태이면 재개하며, 꺼져 있을 때만 새 ISO를 빌드해 연결한다. VirtualBox에서 부팅과 셸의 gebruikersruimte app_f5044b9b 실행을 확인했다. 다만 actueel_item VirtualBox용 네트워크 드라이버는 없어 네트워크 장치를 비활성화한다. UDP 시험에는 `make run`을 사용한다. 상태별 동작과 새 bouwen 반영 방법은 [VirtualBox Uitvoeren_opdracht LEESMIJ_eb81d7d9](Guides/가상상자실행.md)에 있다.

기존 관리 커널만 시험하려면:

```sh
cd /home/user/jkoros
make -f maken_invoer.mk 검사
make -f maken_invoer.mk host
```

`host`는 여전히 JVM 관리 계층의 Actie 시험이다. `make -f maken_invoer.mk build_kopie`는 새 `os/`의 제한형 네이티브 kernel_WAARDE ISO를 만든다. 기존 `verouderd_bron/`의 bestandssysteem·Proces_WAARDE·net_stack implementatie 전체를 이 ISO에 이식했다는 의미는 아니다.

Nederlands FUNCTIE_WAARDE·variabele_WAARDE·bestand 이름과 werkelijk_gegevens C API는 [posix-kor](posix-kor/LEESMIJ_eb81d7d9.md)에 있다. 게스트 Java에서는 `FileInputStream`·`FileOutputStream`의 단일 byte_WAARDE 입출력도 지원한다. 전체 POSIX·OpenJDK·Swing 지원으로 확대된 것은 아니다.

extern_WAARDE 배포용 `pack.sh` / `unpack.sh`와 자동 의존성 복원은 [distributie_WAARDE LEESMIJ_eb81d7d9](distribution/README.md)를 참고하세요.
