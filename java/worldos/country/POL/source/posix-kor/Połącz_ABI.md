# przestrzeń_użytkownika 호출 granica_WARTOŚĆ

대상은 jkoros i386 ELF32다. Linux i386의 호출 번호와 바이너리 호환이 아니다. C의 cdecl 인수를 `maszyna/system_operacyjny_Połączenia.s`에서 EAX(INDEKS), EBX·ECX·EDX·ESI·EDI(첫째~다섯째 argumenty)로 변환한다. EBX·ESI·EDI·EBP를 보존하며 결과는 EAX다. jądro_WARTOŚĆ 실패는 negatywny_WARTOŚĆ błąd INDEKS, C biblioteka 실패는 -1과 양수 errno다.

커널은 0x04000000 이상, 0x04400000 미만의 przestrzeń_użytkownika region_WARTOŚĆ 안에 자료의 전체 길이가 들어가는지 확인한다. 단순 널 검사가 아니다. C dane 주소는 bajt_WARTOŚĆ 주소이며, 기존 Java AOT `int[]` 포인터와 혼용하지 않는다. Java nazwa_pliku 흐름의 어셈블리 경계가 별도 bajt_WARTOŚĆ 버퍼를 마련하여 같은 호출을 사용한다.

| INDEKS | Akcja | argumenty |
|---|---|---|
| 30 | otwarty_Plik | NUL 끝 Nazwa Adres, Ustawienia, udzielenie_pozwolenie |
| 31 | 파일자료읽기 | deskryptor_wpis, dane Adres, bajt_WARTOŚĆ identyfikator |
| 32 | zapis_Plik_dane | deskryptor_wpis, dane Adres, bajt_WARTOŚĆ identyfikator |
| 33 | Zamknij_Plik | deskryptor_wpis |
| 34 | szukać_Plik | deskryptor_wpis, Encoding_WARTOŚĆ 있는 przesunąć_WARTOŚĆ_450fc799, Project_korzeń |
| 35 | Duplikuj_Plik_deskryptor | deskryptor_wpis |
| 36 | 파일서술자지정복제 | deskryptor_wpis, 새 deskryptor_wpis |
| 37 | 파일상태읽기 | deskryptor_wpis, 48바이트 Stan_WARTOŚĆ Adres |
| 38 | usuń_Plik_wpis_nazwa | NUL 끝 Nazwa Adres |
| 39 | set_Plik_długość | deskryptor_wpis, 새 długość_WARTOŚĆ |
| 40 | kontrola_Plik_deskryptor | deskryptor_wpis, polecenie, WARTOŚĆ |
| 41 | Twórca_uczestnik | Adres system_operacyjny_WARTOŚĆ, Rodzaj_WARTOŚĆ, wartość_kontraktu INDEKS |
| 42 | BIND_ADRES | deskryptor_wpis, sockaddr_in Adres, długość_WARTOŚĆ |
| 43 | wysłać_datagram_dane | deskryptor_wpis, dane Adres, długość_WARTOŚĆ, Ustawienia, żądanie Adres |
| 44 | odbierać_datagram_dane | deskryptor_wpis, dane Adres, długość_WARTOŚĆ, Ustawienia, żądanie Adres |
| 45 | 통신주소읽기 | deskryptor_wpis, sockaddr Adres, socklen_t Adres |
| 46 | set_odbierać_TIMEOUT | deskryptor_wpis, 0~2000 밀리초 |
| 47 | przekazywać_Files | deskryptor_wpis |

43번 요청은 32비트 주소와 32비트 길이의 두 칸이다. 44번 요청은 32비트 주소와 길이를 담은 32비트 값의 Adres 두 칸이다. odbierać_WARTOŚĆ 주소가 NULL이면 węzeł_równorzędny_WARTOŚĆ Adres 기록을 생략한다. sockaddr_in은 16바이트이며 Adres 체계는 urządzenie_WARTOŚĆ bajt_WARTOŚĆ SEKWENCJA_WARTOŚĆ, 접속번호와 IP 주소는 네트워크 bajt_WARTOŚĆ 차례다. 축소된 Adres 버퍼에도 들어가는 앞부분을 쓰고 전체 Adres Rozmiar 16을 반환한다.

0~22번의 기존 Java AOT 호출은 유지한다. 0은 wyjść_program, 2·3은 기존 argumenty 조회다. bieżący_towar 커널의 argumenty 목록이 Wykonaj_polecenie 이름을 제외하므로 C 진입기는 argv[0]에 고정 ciąg_WARTOŚĆ `jkoros-app`을 넣고 이후 인수를 전달한다. argv 끝에는 NULL이 있다. 이 제한도 일반 UNIX Proces_WARTOŚĆ ABI와 다른 점이다.

표준 헤더의 liczba_całkowita Rozmiar, 플래그 WARTOŚĆ, stat wartość_pola 순서는 `plik_źródłowy/deklaracje/`에 정의한다. 동적 Połącz·다중 Proces_WARTOŚĆ·스레드가 추가되면 błąd INDEKS 저장과 zasób_WARTOŚĆ 수명, 호출 경계도 함께 검토해야 한다.
