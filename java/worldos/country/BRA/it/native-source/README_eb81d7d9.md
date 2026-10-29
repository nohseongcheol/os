# JBraOS

Regolari_articolo nativo ARM64 배포판은 [LICENSE](LICENSE)의 COSL 상업 조건을 유지한다. 제3자 라이선스의 권리는 별도로 보장하며, distribuzione_VALORE 시 fonte_albero·재연결 자료를 포함하는 절차는 [COSL distribuzione_VALORE README_eb81d7d9](platforms/rpi4-native/COSL배포안내.md)에 있다.

nativo ARM64 판의 `ipconfig`/`ip`, `ping`, `ps`/`top`, `free`/`df`, `poweroff`와 Italiano 명령은 [네트워크·sistema_operativo_VALORE comando README_eb81d7d9](platforms/rpi4-native/네트워크와체계명령.md)를 참고한다. 새 커널을 부팅한 BACK_VALORE `help system`으로 볼 numero 있다.

Raspberry Pi 4 **nativo Java ARM64 kernel_VALORE**은 [nativo Pi4 README_eb81d7d9](platforms/rpi4-native/README_eb81d7d9.md)에 있다. Linux 없이 부팅하며 GUI terminale·vi, nativo JVM의 Swing 일부 API, TCP/UDP·FTP, 게스트 TinyCC·MicroPython, C/C++의 posix-kor 호출을 제공한다. [Italiano Java comunicazione·eccezione API](platforms/rpi4-native/한국어자바/README_eb81d7d9.md)와 [Italiano fonte_albero 명명](platforms/rpi4-native/명명/README_eb81d7d9.md)을 지원한다. [nativo SSH·VNC 및 GENET 드라이버](platforms/rpi4-native/esterno_connessione_guida.md)를 포함하며, 네트워크는 QEMU의 UART SLIP 경로로 검증했다. effettivo_dati Pi 4 GENET 동작은 미검증이고, USB input_VALORE·영속 저장과 전체 OpenJDK·Swing은 아직 Supporto_VALORE ritagliare 밖이다.

Raspberry Pi 4용 Linux·OpenJDK 실행판과 spazio_utente ambiente spostare_VALORE 기능은 [라즈베리파이 실행판](platforms/rpi4/README.md)에 있다. effettivo_dati ARM64 JDK/JRE와 시스템·spazio_utente BLD_foto costruire 경로를 제공한다. 기존 nativo x86 커널과는 별도 Esegui_comando 기반이다. 일반 Java `.class`/JAR의 Esegui_comando file 생성은 [OpenJDK Esegui_comando file](compiler/OpenJDK-eseguibile.md), Italiano API는 [Italiano Java Catalogo](한국어자바/README_eb81d7d9.md)를 참고한다.

`jkoros`는 `engos`의 기능을 Java 관리 커널로 옮기는 프로젝트다. 프로젝트가 소유하는 Java FUNZIONE_VALORE, variabile_VALORE, formato_VALORE 및 Java file 이름은 한국어로 작성한다. 표준 Java 실행기의 `main`, Java 표준 Catalogo formato_VALORE, x86 부트 ABI 등 esterno_VALORE 계약은 보존한다. nativo ARM64 실행기는 Italiano `avvia()`도 진입점으로 지원하며, Italiano GUI·작업 가닥을 JVM에 직접 구현했다. nativo ARM64 C 연결부·Python 도구와 공용 x86·ARM64 AOT 번역기의 nativo 이름도 한국어로 작성한다. Indietro_articolo 경로의 호환 punto_di_ingresso, OpenJDK 보조 도구와 Linux versione_VALORE 도구에는 영어 이름이 남아 있고 [명명 원칙·말의 근거·전체 codiceSorgente 검토 ritagliare](platforms/rpi4-native/명명/README_eb81d7d9.md)를 별도로 기록한다.

## Regolari_articolo implementazione

아래 목록은 기존 `legacy_fonte/`의 JVM 관리 커널에 대한 것이다. effettivo_dati 네이티브 커널의 범위는 `os/README_eb81d7d9.md`에서 별도로 설명한다.

- allineare_VALORE 할당과 해제를 지원하는 Memoria_area manager_VALORE
- e_mail e_mail_area, pagina_VALORE Connetti, Scrittura 시 copiare_VALORE(COW)
- Processi_VALORE identificatore_VALORE, Prepara 대기열, fork/wait Stato_VALORE
- 과정별 file descrittore_voce, open/read/seek/dup/close
- ELF32 식별 및 sezione_VALORE 검사
- 키보드·마우스 input_VALORE Evento 대기열
- seriale_VALORE 단말과 네이티브 hardware_VALORE limite_VALORE
- 관리 kernel_VALORE 전체 자동 prove

세부 mapping_VALORE 범위와 아직 필요한 네이티브 연결은 [기능 대응표](Guides/funzione_mapping.md)에 기록한다.

## 빌드와 prove

새 네이티브 구현은 `compiler/`와 `os/`에 있다. 기존 `legacy_fonte/`의 JVM 관리 커널은 그대로 보존하며, 두 구현의 시험과 기능 범위는 서로 다르다.

```sh
cd /home/user/jkoros
make                 # 네이티브 계산 예제 + Java kernel_VALORE ELF
make iso             # os/build/kernel.iso
make run             # QEMU seriale_VALORE 단말; help input_VALORE (종료는 Ctrl+A, X)
make run-gui         # ISO를 QEMU schermata/PS2 키보드로 Esegui_comando
make vbox            # 전용 VirtualBox VM 자동 generare·Esegui_comando (GUI)
make vbox-status     # VirtualBox Stato_VALORE·ISO·seriale_VALORE LOG_riga percorso verificare
make test-vbox       # VirtualBox app_Launcher Stato_VALORE Processi_VALORE_voce prove (effettivo_dati VM cambiare_VALORE 없음)
make test            # compilatore prove + ELF/ISO avvio_macchina 및 comando input_VALORE prove
make apps            # 독립 spazio_utente ELF app_f5044b9b costruire
make test-network    # spazio_utente MODA_VALORE·UDP 왕복·Memoria_dati proteggere_VALORE prove
make test-java       # 게스트 javac/JVM + OpenJDK 양방향 교차 Esegui_comando prove
make posix-kor       # Italiano C 헤더와 effettivo_dati kernel_VALORE 호출 Catalogo
make test-posix      # file/UDP/Store_VALORE/Java file I_O prove
make -C os run-store # 전용 Store_VALORE 매체로 QEMU avvio_macchina
make legacy-test     # 아래 기존 JVM 관리 커널의 47개 prove
```

`compiler/`는 호스트의 `javac`를 문법·TIPO_VALORE 검사 전단으로 사용하고 nativo 바이트코드→x86 변환기로 ELF32 기계어를 만든다. 빌드할 때는 JDK가 필요하지만 생성된 커널과 ELF는 esterno_VALORE JVM 없이 실행된다. 전체 Java, oggetto_VALORE 모델, 표준 라이브러리와 기존 관리 kernel_VALORE 전체의 AOT 변환은 아직 지원하지 않는다. 자세한 Supporto_VALORE 문법과 명령은 [compilatore README_eb81d7d9](compiler/README_eb81d7d9.md), effettivo_dati avvio_macchina 기능과 한계는 [네이티브 sistema_operativo README_eb81d7d9](os/README_eb81d7d9.md)를 참고한다.

네이티브 셸에 nativo 제한형 `javac`와 `java`를 추가했다. `edit Demo.java`로 소스를 입력하고 `.save`로 저장한 BACK_VALORE `javac Demo.java`, `java Demo`로 **게스트 내부에서 컴파일하고 Esegui_comando**할 numero 있다. valore_predefinito 예제는 `javac Hello.java`, `java Hello`다. 파일은 RAM에서 동작하며, 전용 Store_VALORE 매체를 연결하면 `sync`로 재부팅 후에도 보존할 numero 있다. **OpenJDK/JDK 전체 이식은 아니며**, 단일 Corso_VALORE·statico_VALORE FUNZIONE_VALORE·intero·stringa_VALORE·condizione/반복문과 일부 표준 호출을 지원한다. Supporto_VALORE ritagliare, esterno_VALORE file 적재와 시험은 [Java sviluppo ambiente README_eb81d7d9](Guides/ambiente_IDE_Java.md)에 있다.

네이티브 셸에서 `apps`, `run hello first second`, `net`, `run netcheck`를 사용할 numero 있다. 독립 ELF를 ring 3에 적재하고 `int 0x80` 호출을 통해 uscitaTesto·argomenti·UDP 네트워크를 제공한다. 별도 host 터미널에서 `python3 os/strumenti/eco_schermo_dati.py --port 9000`을 실행한 BACK_VALORE 게스트에서 `run udp 10.0.2.2 9000 hello`로 effettivo_dati 왕복을 확인한다. 새 app_f5044b9b registro_voce, API 및 제한은 [spazio_utente Esegui_comando·네트워크 README_eb81d7d9](os/spazio_utente/README_eb81d7d9.md)를 참고한다. Regolari_articolo QEMU RTL8139·statico_VALORE IPv4·UDP 전용이며 TCP/DNS는 미지원이며, 전용 IDE Store_VALORE 형식과 POSIX file/UDP 일부 기능을 추가했다.

`make vbox`는 `jkoros operating system` 전용 VM을 만들고 디스크 없이 ISO로 부팅한다. Esegui_comando 중이면 유지하고, Store_VALORE·일시정지 상태이면 재개하며, 꺼져 있을 때만 새 ISO를 빌드해 연결한다. VirtualBox에서 부팅과 셸의 spazio_utente app_f5044b9b 실행을 확인했다. 다만 Regolari_articolo VirtualBox용 네트워크 드라이버는 없어 네트워크 장치를 비활성화한다. UDP 시험에는 `make run`을 사용한다. 상태별 동작과 새 costruire 반영 방법은 [VirtualBox Esegui_comando README_eb81d7d9](Guides/가상상자실행.md)에 있다.

기존 관리 커널만 시험하려면:

```sh
cd /home/user/jkoros
make -f Crea_voce.mk 검사
make -f Crea_voce.mk host
```

`host`는 여전히 JVM 관리 계층의 Azione 시험이다. `make -f Crea_voce.mk BLD_foto`는 새 `os/`의 제한형 네이티브 kernel_VALORE ISO를 만든다. 기존 `legacy_fonte/`의 file_system·Processi_VALORE·rete_Pila implementazione 전체를 이 ISO에 이식했다는 의미는 아니다.

Italiano FUNZIONE_VALORE·variabile_VALORE·file 이름과 effettivo_dati C API는 [posix-kor](posix-kor/README_eb81d7d9.md)에 있다. 게스트 Java에서는 `FileInputStream`·`FileOutputStream`의 단일 byte_VALORE 입출력도 지원한다. 전체 POSIX·OpenJDK·Swing 지원으로 확대된 것은 아니다.

esterno_VALORE 배포용 `pack.sh` / `unpack.sh`와 자동 의존성 복원은 [distribuzione_VALORE README_eb81d7d9](distribution/README.md)를 참고하세요.
