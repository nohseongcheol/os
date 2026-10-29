# uživatelský_prostor 호출 mez_HODNOTA

대상은 jkoros i386 ELF32다. Linux i386의 호출 번호와 바이너리 호환이 아니다. C의 cdecl 인수를 `počítač/operační_systém_Hovory.s`에서 EAX(INDEX), EBX·ECX·EDX·ESI·EDI(첫째~다섯째 argumenty)로 변환한다. EBX·ESI·EDI·EBP를 보존하며 결과는 EAX다. jádro_HODNOTA 실패는 음수 chyba INDEX, C knihovna 실패는 -1과 양수 errno다.

커널은 0x04000000 이상, 0x04400000 미만의 uživatelský_prostor oblast_HODNOTA_0e9a97ab 안에 자료의 전체 길이가 들어가는지 확인한다. 단순 널 검사가 아니다. C data 주소는 bajt_HODNOTA 주소이며, 기존 Java AOT `int[]` 포인터와 혼용하지 않는다. Java název_souboru 흐름의 어셈블리 경계가 별도 bajt_HODNOTA 버퍼를 마련하여 같은 호출을 사용한다.

| INDEX | Akce | argumenty |
|---|---|---|
| 30 | otevřít_Soubor | NUL 끝 Název Adresa, Nastavení, oprávnění_oprávnění |
| 31 | 파일자료읽기 | popisovač_položka, data Adresa, bajt_HODNOTA číslo |
| 32 | zápis_Soubor_data | popisovač_položka, data Adresa, bajt_HODNOTA číslo |
| 33 | Zavřít_Soubor | popisovač_položka |
| 34 | hledat_Soubor | popisovač_položka, Encoding_HODNOTA 있는 POSUN_HODNOTA, akce_kořen |
| 35 | duplikát_Soubor_popisovač | popisovač_položka |
| 36 | 파일서술자지정복제 | popisovač_položka, 새 popisovač_položka |
| 37 | 파일상태읽기 | popisovač_položka, 48바이트 Stav_HODNOTA Adresa |
| 38 | odebrat_Soubor_položka_název | NUL 끝 Název Adresa |
| 39 | sada_Soubor_délka | popisovač_položka, 새 délka_HODNOTA |
| 40 | řízení_Soubor_popisovač | popisovač_položka, příkaz, HODNOTA |
| 41 | Create_účastník | Adresa operační_systém_HODNOTA, Druh_HODNOTA, hodnota_smlouvy INDEX |
| 42 | vázat_ODKAZ | popisovač_položka, sockaddr_in Adresa, délka_HODNOTA |
| 43 | poslat_datagram_data | popisovač_položka, data Adresa, délka_HODNOTA, Nastavení, žádost Adresa |
| 44 | dostat_datagram_data | popisovač_položka, data Adresa, délka_HODNOTA, Nastavení, žádost Adresa |
| 45 | 통신주소읽기 | popisovač_položka, sockaddr Adresa, socklen_t Adresa |
| 46 | sada_dostat_TIMEOUT | popisovač_položka, 0~2000 밀리초 |
| 47 | zápis_Files | popisovač_položka |

43번 요청은 32비트 주소와 32비트 길이의 두 칸이다. 44번 요청은 32비트 주소와 길이를 담은 32비트 값의 Adresa 두 칸이다. dostat_HODNOTA 주소가 NULL이면 partner_HODNOTA Adresa 기록을 생략한다. sockaddr_in은 16바이트이며 Adresa 체계는 mobilní_HODNOTA bajt_HODNOTA SEQUENCE_HODNOTA, 접속번호와 IP 주소는 네트워크 bajt_HODNOTA 차례다. 축소된 Adresa 버퍼에도 들어가는 앞부분을 쓰고 전체 Adresa Velikost 16을 반환한다.

0~22번의 기존 Java AOT 호출은 유지한다. 0은 Konec_program, 2·3은 기존 argumenty 조회다. dobrá_zboží 커널의 argumenty 목록이 Provést_příkaz 이름을 제외하므로 C 진입기는 argv[0]에 고정 řetězec_HODNOTA `jkoros-app`을 넣고 이후 인수를 전달한다. argv 끝에는 NULL이 있다. 이 제한도 일반 UNIX Proces_HODNOTA ABI와 다른 점이다.

표준 헤더의 integer Velikost, 플래그 HODNOTA, stat hodnota_pole 순서는 `zdrojový_soubor/deklarace/`에 정의한다. 동적 Připojit·다중 Proces_HODNOTA·스레드가 추가되면 chyba INDEX 저장과 zdroj_HODNOTA 수명, 호출 경계도 함께 검토해야 한다.
