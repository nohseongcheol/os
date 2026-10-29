# spazio_utente 호출 limite_VALORE

대상은 jkoros i386 ELF32다. Linux i386의 호출 번호와 바이너리 호환이 아니다. C의 cdecl 인수를 `computer/sistema_operativo_Chiamate.s`에서 EAX(INDICE), EBX·ECX·EDX·ESI·EDI(첫째~다섯째 argomenti)로 변환한다. EBX·ESI·EDI·EBP를 보존하며 결과는 EAX다. kernel_VALORE 실패는 negativo_VALORE errore INDICE, C Catalogo 실패는 -1과 양수 errno다.

커널은 0x04000000 이상, 0x04400000 미만의 spazio_utente area_VALORE 안에 자료의 전체 길이가 들어가는지 확인한다. 단순 널 검사가 아니다. C dati 주소는 byte_VALORE 주소이며, 기존 Java AOT `int[]` 포인터와 혼용하지 않는다. Java file 흐름의 어셈블리 경계가 별도 byte_VALORE 버퍼를 마련하여 같은 호출을 사용한다.

| INDICE | Azione | argomenti |
|---|---|---|
| 30 | aperto_File | NUL 끝 Nome e_mail, Impostazioni, concessione_privilegio |
| 31 | 파일자료읽기 | descrittore_voce, dati e_mail, byte_VALORE numero |
| 32 | scrivere_File_dati | descrittore_voce, dati e_mail, byte_VALORE numero |
| 33 | Chiudi_File | descrittore_voce |
| 34 | cercare_File | descrittore_voce, Codifica_VALORE 있는 SCARTO_VALORE, azione_radice |
| 35 | Duplica_File_descrittore | descrittore_voce |
| 36 | 파일서술자지정복제 | descrittore_voce, 새 descrittore_voce |
| 37 | 파일상태읽기 | descrittore_voce, 48바이트 Stato_VALORE e_mail |
| 38 | rimuovere_File_voce_nome | NUL 끝 Nome e_mail |
| 39 | set_File_durata | descrittore_voce, 새 durata_VALORE |
| 40 | controllo_File_descrittore | descrittore_voce, comando, VALORE |
| 41 | Crea_endpoint | e_mail sistema_operativo_VALORE, Kind_VALORE, valore_di_contratto INDICE |
| 42 | BIND_e_mail | descrittore_voce, sockaddr_in e_mail, durata_VALORE |
| 43 | inviare_datagramma_dati | descrittore_voce, dati e_mail, durata_VALORE, Impostazioni, richiesta e_mail |
| 44 | ricevere_datagramma_dati | descrittore_voce, dati e_mail, durata_VALORE, Impostazioni, richiesta e_mail |
| 45 | 통신주소읽기 | descrittore_voce, sockaddr e_mail, socklen_t e_mail |
| 46 | set_ricevere_TIMEOUT | descrittore_voce, 0~2000 밀리초 |
| 47 | commit_File | descrittore_voce |

43번 요청은 32비트 주소와 32비트 길이의 두 칸이다. 44번 요청은 32비트 주소와 길이를 담은 32비트 값의 e_mail 두 칸이다. ricevere_VALORE 주소가 NULL이면 peer_VALORE e_mail 기록을 생략한다. sockaddr_in은 16바이트이며 e_mail 체계는 cellulare_VALORE byte_VALORE SEQUENZA_VALORE, 접속번호와 IP 주소는 네트워크 byte_VALORE 차례다. 축소된 e_mail 버퍼에도 들어가는 앞부분을 쓰고 전체 e_mail Dimensione 16을 반환한다.

0~22번의 기존 Java AOT 호출은 유지한다. 0은 Esci_app, 2·3은 기존 argomenti 조회다. Regolari_articolo 커널의 argomenti 목록이 Esegui_comando 이름을 제외하므로 C 진입기는 argv[0]에 고정 stringa_VALORE `jkoros-app`을 넣고 이후 인수를 전달한다. argv 끝에는 NULL이 있다. 이 제한도 일반 UNIX Processi_VALORE ABI와 다른 점이다.

표준 헤더의 intero Dimensione, 플래그 VALORE, stat valore_del_campo 순서는 `codiceSorgente/dichiarazioni/`에 정의한다. 동적 Connetti·다중 Processi_VALORE·스레드가 추가되면 errore INDICE 저장과 risorsa_VALORE 수명, 호출 경계도 함께 검토해야 한다.
