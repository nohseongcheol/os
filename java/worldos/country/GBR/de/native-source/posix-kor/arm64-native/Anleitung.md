# eigen ARM64 Java 커널의 C/C++ Datei·루프백 verbinden

이 디렉터리는 `platforms/rpi4-native` eigen betriebskernWert 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`Kopfdateien/DateiABI.h`는 Deutsch 함수명과 `extern "C"` ABI를 제공한다. `verbinden.c`는 betriebskernWert 안에서 AOT Java Datei 메서드에 직접 연결하고, `benutzerBrücke.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. tatsächlichDaten Datei 처리는 `SpeicherDateien.java`, 루프백 datagramm 처리는 `RückschleifeNetzwerk.java`, 연결형 흐름은 `DatenstromNetzwerk.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 betriebskernWert 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`dritterOperand. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·fließendPunktWert vorgangWert·Datei·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

unterstützungWert: `dateiÖffnen`, `dateiDatenLesen`, `dateiDatenSchreiben`, `dateiSchließen`, `dateiPositionieren`, `dateiEintragNameEntfernen`, `dateiLängeSetzen`, hilfsWert Funktion `dateiGröße`. fehler 시 -1과 작업별 `fehlerNummer`를 반환한다. `bestätigenDateiSpeichergerät`은 RAM 파일이므로 ENOSYS를 반환한다. Datei 16개, 각 16384바이트, Name 63바이트, deskriptorEintrag 16개이며 RAM 디렉터리·gegenstelleWert/절대 경로를 제공한다. erlaubnisWert/영속 저장은 없다.

사용자용 `Kopfdateien/NetzwerkABI.h`는 tatsächlichDaten Deutsch 함수와 독립 구조체를 선언한다.
`endpunktErstellen`, `adresseZuordnen`, `datagrammDatenSenden/empfangen`, `netzwerkVerbinden/abwarten/empfangen`는
`benutzerBrücke.c`에서 SVC를 호출하며 makroWert 별칭이 아니다. `struct InternetNetzbuchseAdresse`의
`adresseFamilie`, `portNummer`, `InternetAdresse.adresseWert`을 사용한다. 상수는 enum의
`InternetFamilie`, `DatagrammNetzbuchse`, `DatagrammProtokoll`, `DatenstromNetzwerk`, `datenstromBeförderungProtokoll`이다.
Deutsch·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. externWert 통신은 eigen 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. tatsächlichDaten Pi 4 GENET 드라이버는 미지원이다.
소켓도 tatsächlichDaten Funktion `dateiSchließen`로 닫는다.

[사용법·Aufbau·grenzstelleGrenzwert](../../platforms/rpi4-native/README.md), [Benutzer ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ Datei Beispiele](../../platforms/rpi4-native/Benutzer/Dateibeispiel.cpp), [UDP 루프백 Beispiele](../../platforms/rpi4-native/Benutzer/KommunikationBeispiel.cpp), [기존 betriebskernWert 내부 aufrufen Prüfungen](../../platforms/rpi4-native/Prüfungen/DateiAufrufliste.cpp)을 참고한다.

C11/C++11의 HangulText bezeichnerWert·헤더 benutzenWert, SDK systemErzeugenAbbild, ELF 업로드·befehlAusführen, fehler/unterteilWert eingabeAusgabe 처리는 [HangulText entwicklung 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 Kommunikation Beispiele](../../platforms/rpi4-native/Beispiele/HangulKodierweise/datenstromWert.c)도 제공한다.
