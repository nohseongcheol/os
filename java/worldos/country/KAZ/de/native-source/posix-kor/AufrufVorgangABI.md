# Benutzer aufrufen grenzstelleWert

대상은 jkoros i386 ELF32다. Linux i386의 aufrufen 번호와 바이너리 호환이 아니다. C의 cdecl 인수를 `maschine/BetriebSystemAufrufliste.s`에서 EAX(Nummer), EBX·ECX·EDX·ESI·EDI(ersterOrdnungszahl~fünfterOrdnungszahl argumente)로 변환한다. EBX·ESI·EDI·EBP를 보존하며 결과는 EAX다. betriebskernWert 실패는 negativWert fehler Nummer, C bibliothek 실패는 -1과 양수 errno다.

커널은 0x04000000 이상, 0x04400000 미만의 Benutzer gebietWert 안에 자료의 전체 길이가 들어가는지 확인한다. 단순 널 검사가 아니다. C Daten 주소는 byteWert 주소이며, 기존 Java AOT `int[]` 포인터와 혼용하지 않는다. Java Datei 흐름의 어셈블리 경계가 별도 byteWert 버퍼를 마련하여 같은 호출을 사용한다.

| Nummer | aktion | argumente |
|---|---|---|
| 30 | dateiÖffnen | NUL endung Name adresse, einstellungen, erlaubnisGewähren |
| 31 | dateiDatenLesen | deskriptorEintrag, Daten adresse, byteWert Zahl |
| 32 | dateiDatenSchreiben | deskriptorEintrag, Daten adresse, byteWert Zahl |
| 33 | dateiSchließen | deskriptorEintrag |
| 34 | dateiPositionieren | deskriptorEintrag, kodierungWert 있는 versatzwertWert, projektWurzel |
| 35 | duplikatDateiDeskriptor | deskriptorEintrag |
| 36 | duplikatDateiDeskriptorAnStelle | deskriptorEintrag, 새 deskriptorEintrag |
| 37 | dateiZustandLesen | deskriptorEintrag, 48바이트 statuswertWert adresse |
| 38 | dateiEintragNameEntfernen | NUL endung Name adresse |
| 39 | dateiLängeSetzen | deskriptorEintrag, 새 Länge |
| 40 | steuerungDateiDeskriptor | deskriptorEintrag, befehl, Wert |
| 41 | endpunktErstellen | adresse betriebSystemWert, artWert, vertragWert Nummer |
| 42 | adresseZuordnen | deskriptorEintrag, sockaddr_in adresse, Länge |
| 43 | datagrammDatenSenden | deskriptorEintrag, Daten adresse, Länge, einstellungen, anfrage adresse |
| 44 | datagrammDatenEmpfangen | deskriptorEintrag, Daten adresse, Länge, einstellungen, anfrage adresse |
| 45 | netzbuchseAdresseLesen | deskriptorEintrag, sockaddr adresse, socklen_t adresse |
| 46 | empfangenZeitüberschreitungSetzen | deskriptorEintrag, 0~2000 millisekunden |
| 47 | bestätigenDateiSpeichergerät | deskriptorEintrag |

43번 요청은 32비트 주소와 32비트 길이의 두 칸이다. 44번 요청은 32비트 주소와 길이를 담은 32비트 값의 adresse 두 칸이다. wertEmpfangen 주소가 NULL이면 gegenstelleWert adresse 기록을 생략한다. sockaddr_in은 16바이트이며 adresse 체계는 Gerät byteWert folgeWert, 접속번호와 IP 주소는 네트워크 byteWert 차례다. 축소된 adresse 버퍼에도 들어가는 앞부분을 쓰고 전체 adresse größe 16을 반환한다.

0~22번의 기존 Java AOT 호출은 유지한다. 0은 verlassenProzessProgramm, 2·3은 기존 argumente 조회다. aktuellElementeintrag 커널의 argumente 목록이 befehlAusführen 이름을 제외하므로 C 진입기는 argv[0]에 고정 Zeichenkette `jkoros-app`을 넣고 danachWert 인수를 전달한다. argv 끝에는 NULL이 있다. 이 제한도 일반 UNIX prozessWert ABI와 다른 점이다.

표준 헤더의 Ganzzahl größe, merkmalbitsWert Wert, stat feldWert 순서는 `Quelltext/Kopfdateien/`에 정의한다. 동적 verbinden·다중 prozessWert·스레드가 추가되면 fehler Nummer 저장과 betriebsmittelEintragWert 수명, aufrufen 경계도 함께 검토해야 한다.
