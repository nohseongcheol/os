# JDeuOS

bieżący_towar własny ARM64 배포판은 [LICENSE](LICENSE)의 COSL 상업 조건을 유지한다. 제3자 라이선스의 권리는 별도로 보장하며, dystrybucja_WARTOŚĆ 시 źródło_drzewo·재연결 자료를 포함하는 절차는 [COSL dystrybucja_WARTOŚĆ plik_README_eb81d7d9](platforms/rpi4-native/COSL배포안내.md)에 있다.

własny ARM64 판의 `ipconfig`/`ip`, `ping`, `ps`/`top`, `free`/`df`, `poweroff`와 polski 명령은 [네트워크·system_operacyjny_WARTOŚĆ polecenie plik_README_eb81d7d9](platforms/rpi4-native/네트워크와체계명령.md)를 참고한다. 새 커널을 부팅한 BACK_WARTOŚĆ `help system`으로 볼 identyfikator 있다.

Raspberry Pi 4 **własny Java ARM64 jądro_WARTOŚĆ**은 [własny Pi4 plik_README_eb81d7d9](platforms/rpi4-native/plik_README_eb81d7d9.md)에 있다. Linux 없이 부팅하며 GUI interpretator_poleceń·vi, własny JVM의 Swing 일부 API, TCP/UDP·FTP, 게스트 TinyCC·MicroPython, C/C++의 posix-kor 호출을 제공한다. [polski Java komunikacja·wyjątek API](platforms/rpi4-native/한국어자바/plik_README_eb81d7d9.md)와 [polski źródło_drzewo 명명](platforms/rpi4-native/명명/plik_README_eb81d7d9.md)을 지원한다. [własny SSH·VNC 및 GENET 드라이버](platforms/rpi4-native/zewnętrzny_połączenie_prowadnica.md)를 포함하며, 네트워크는 QEMU의 UART SLIP 경로로 검증했다. rzeczywisty_dane Pi 4 GENET 동작은 미검증이고, USB wejście_WARTOŚĆ·영속 저장과 전체 OpenJDK·Swing은 아직 wsparcie_WARTOŚĆ obcinać 밖이다.

Raspberry Pi 4용 Linux·OpenJDK 실행판과 przestrzeń_użytkownika środowisko przenosić_WARTOŚĆ 기능은 [라즈베리파이 실행판](platforms/rpi4/README.md)에 있다. rzeczywisty_dane ARM64 JDK/JRE와 시스템·przestrzeń_użytkownika BLD_OBRAZ BLD_System 경로를 제공한다. 기존 własny x86 커널과는 별도 Wykonaj_polecenie 기반이다. 일반 Java `.class`/JAR의 Wykonaj_polecenie nazwa_pliku 생성은 [OpenJDK Wykonaj_polecenie nazwa_pliku](compiler/OpenJDK-plik_wykonywalny.md), polski API는 [polski Java biblioteka](한국어자바/plik_README_eb81d7d9.md)를 참고한다.

`jkoros`는 `engos`의 기능을 Java 관리 커널로 옮기는 프로젝트다. 프로젝트가 소유하는 Java FUNKCJA_WARTOŚĆ, zmienna_WARTOŚĆ, format_WARTOŚĆ 및 Java nazwa_pliku 이름은 한국어로 작성한다. 표준 Java 실행기의 `main`, Java 표준 biblioteka format_WARTOŚĆ, x86 부트 ABI 등 zewnętrzny_WARTOŚĆ 계약은 보존한다. własny ARM64 실행기는 polski `Uruchom_2()`도 진입점으로 지원하며, polski GUI·작업 가닥을 JVM에 직접 구현했다. własny ARM64 C 연결부·Python 도구와 공용 x86·ARM64 AOT 번역기의 własny 이름도 한국어로 작성한다. Wstecz_towar 경로의 호환 punkt_wejścia, OpenJDK 보조 도구와 Linux wersja_WARTOŚĆ 도구에는 영어 이름이 남아 있고 [명명 원칙·말의 근거·전체 plik_źródłowy 검토 obcinać](platforms/rpi4-native/명명/plik_README_eb81d7d9.md)를 별도로 기록한다.

## bieżący_towar implementacja

아래 목록은 기존 `starsze_źródło/`의 JVM 관리 커널에 대한 것이다. rzeczywisty_dane 네이티브 커널의 범위는 `os/plik_README_eb81d7d9.md`에서 별도로 설명한다.

- wyrównać_WARTOŚĆ 할당과 해제를 지원하는 Pamięć_region Menedżer_WARTOŚĆ
- Adres ADRES_region, strona_WARTOŚĆ Połącz, Zapis 시 kopiować_WARTOŚĆ(COW)
- Proces_WARTOŚĆ identyfikator_WARTOŚĆ, Przygotuj 대기열, fork/wait Stan_WARTOŚĆ
- 과정별 nazwa_pliku deskryptor_wpis, open/read/seek/dup/close
- ELF32 식별 및 obszar_WARTOŚĆ_366e0bfa 검사
- 키보드·마우스 wejście_WARTOŚĆ Wydarzenie 대기열
- 직렬 단말과 네이티브 sprzęt_WARTOŚĆ granica_WARTOŚĆ
- 관리 jądro_WARTOŚĆ 전체 자동 testy

세부 mapowanie_WARTOŚĆ 범위와 아직 필요한 네이티브 연결은 [기능 대응표](문서/cecha_mapowanie.md)에 기록한다.

## 빌드와 testy

새 네이티브 구현은 `compiler/`와 `os/`에 있다. 기존 `starsze_źródło/`의 JVM 관리 커널은 그대로 보존하며, 두 구현의 시험과 기능 범위는 서로 다르다.

```sh
cd /home/user/jkoros
make                 # 네이티브 계산 예제 + Java jądro_WARTOŚĆ ELF
make iso             # os/build/kernel.iso
make run             # QEMU 직렬 단말; help wejście_WARTOŚĆ (종료는 Ctrl+A, X)
make run-gui         # ISO를 QEMU 화면/PS2 키보드로 Wykonaj_polecenie
make vbox            # 전용 VirtualBox VM 자동 generować·Wykonaj_polecenie (GUI)
make vbox-status     # VirtualBox Stan_WARTOŚĆ·ISO·직렬 LOG_zapis ścieżka_2 확인
make test-vbox       # VirtualBox program_Launcher Stan_WARTOŚĆ Proces_WARTOŚĆ_wpis testy (rzeczywisty_dane VM zmienić_WARTOŚĆ 없음)
make test            # kompilator testy + ELF/ISO rozruch_maszyny 및 polecenie wejście_WARTOŚĆ testy
make apps            # 독립 przestrzeń_użytkownika ELF program_f5044b9b BLD_System
make test-network    # przestrzeń_użytkownika tryb_WARTOŚĆ·UDP 왕복·Pamięć_dane chronić_WARTOŚĆ testy
make test-java       # 게스트 javac/JVM + OpenJDK 양방향 교차 Wykonaj_polecenie testy
make posix-kor       # polski C 헤더와 rzeczywisty_dane jądro_WARTOŚĆ 호출 biblioteka
make test-posix      # nazwa_pliku/UDP/Store_WARTOŚĆ/Java nazwa_pliku We_Wy testy
make -C os run-store # 전용 Store_WARTOŚĆ 매체로 QEMU rozruch_maszyny
make legacy-test     # 아래 기존 JVM 관리 커널의 47개 testy
```

`compiler/`는 호스트의 `javac`를 문법·TYP_WARTOŚĆ 검사 전단으로 사용하고 własny 바이트코드→x86 변환기로 ELF32 기계어를 만든다. 빌드할 때는 JDK가 필요하지만 생성된 커널과 ELF는 zewnętrzny_WARTOŚĆ JVM 없이 실행된다. 전체 Java, obiekt_WARTOŚĆ 모델, 표준 라이브러리와 기존 관리 jądro_WARTOŚĆ 전체의 AOT 변환은 아직 지원하지 않는다. 자세한 wsparcie_WARTOŚĆ 문법과 명령은 [kompilator plik_README_eb81d7d9](compiler/plik_README_eb81d7d9.md), rzeczywisty_dane rozruch_maszyny 기능과 한계는 [네이티브 system_operacyjny plik_README_eb81d7d9](os/plik_README_eb81d7d9.md)를 참고한다.

네이티브 셸에 własny 제한형 `javac`와 `java`를 추가했다. `edit Demo.java`로 소스를 입력하고 `.save`로 저장한 BACK_WARTOŚĆ `javac Demo.java`, `java Demo`로 **게스트 내부에서 컴파일하고 Wykonaj_polecenie**할 identyfikator 있다. wartość_domyślna 예제는 `javac Hello.java`, `java Hello`다. 파일은 RAM에서 동작하며, 전용 Store_WARTOŚĆ 매체를 연결하면 `sync`로 재부팅 후에도 보존할 identyfikator 있다. **OpenJDK/JDK 전체 이식은 아니며**, 단일 Klasa_WARTOŚĆ·statyczny_WARTOŚĆ FUNKCJA_WARTOŚĆ·liczba_całkowita·ciąg_WARTOŚĆ·choroba/반복문과 일부 표준 호출을 지원한다. wsparcie_WARTOŚĆ obcinać, zewnętrzny_WARTOŚĆ nazwa_pliku 적재와 시험은 [Java materiał_pochodny środowisko plik_README_eb81d7d9](문서/IDE_Java.md)에 있다.

네이티브 셸에서 `apps`, `run hello first second`, `net`, `run netcheck`를 사용할 identyfikator 있다. 독립 ELF를 ring 3에 적재하고 `int 0x80` 호출을 통해 pozycja_wyjścia·argumenty·UDP 네트워크를 제공한다. 별도 host 터미널에서 `python3 os/narzędzia/echo_dane.py --port 9000`을 실행한 BACK_WARTOŚĆ 게스트에서 `run udp 10.0.2.2 9000 hello`로 rzeczywisty_dane 왕복을 확인한다. 새 program_f5044b9b rejestr_wpis, API 및 제한은 [przestrzeń_użytkownika Wykonaj_polecenie·네트워크 plik_README_eb81d7d9](os/przestrzeń_użytkownika/plik_README_eb81d7d9.md)를 참고한다. bieżący_towar QEMU RTL8139·statyczny_WARTOŚĆ IPv4·UDP 전용이며 TCP/DNS는 미지원이며, 전용 IDE Store_WARTOŚĆ 형식과 POSIX nazwa_pliku/UDP 일부 기능을 추가했다.

`make vbox`는 `jkoros operating system` 전용 VM을 만들고 디스크 없이 ISO로 부팅한다. Wykonaj_polecenie 중이면 유지하고, Store_WARTOŚĆ·일시정지 상태이면 재개하며, 꺼져 있을 때만 새 ISO를 빌드해 연결한다. VirtualBox에서 부팅과 셸의 przestrzeń_użytkownika program_f5044b9b 실행을 확인했다. 다만 bieżący_towar VirtualBox용 네트워크 드라이버는 없어 네트워크 장치를 비활성화한다. UDP 시험에는 `make run`을 사용한다. 상태별 동작과 새 BLD_System 반영 방법은 [VirtualBox Wykonaj_polecenie plik_README_eb81d7d9](문서/가상상자실행.md)에 있다.

기존 관리 커널만 시험하려면:

```sh
cd /home/user/jkoros
make -f Twórca_wpis.mk 검사
make -f Twórca_wpis.mk host
```

`host`는 여전히 JVM 관리 계층의 Akcja 시험이다. `make -f Twórca_wpis.mk BLD_OBRAZ`는 새 `os/`의 제한형 네이티브 jądro_WARTOŚĆ ISO를 만든다. 기존 `starsze_źródło/`의 system_plików·Proces_WARTOŚĆ·sieć_Stos implementacja 전체를 이 ISO에 이식했다는 의미는 아니다.

polski FUNKCJA_WARTOŚĆ·zmienna_WARTOŚĆ·nazwa_pliku 이름과 rzeczywisty_dane C API는 [posix-kor](posix-kor/plik_README_eb81d7d9.md)에 있다. 게스트 Java에서는 `FileInputStream`·`FileOutputStream`의 단일 bajt_WARTOŚĆ 입출력도 지원한다. 전체 POSIX·OpenJDK·Swing 지원으로 확대된 것은 아니다.

zewnętrzny_WARTOŚĆ 배포용 `pack.sh` / `unpack.sh`와 자동 의존성 복원은 [dystrybucja_WARTOŚĆ plik_README_eb81d7d9](distribution/README.md)를 참고하세요.
