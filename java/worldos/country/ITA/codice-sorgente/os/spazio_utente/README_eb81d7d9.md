# 셸에서 실행하는 spazio_utente 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java sviluppo ambiente README_eb81d7d9](../../Guides/ambiente_IDE_Java.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 Esegui_comando

host terminale 1:

```sh
cd /home/user/jkoros
python3 os/strumenti/eco_schermo_dati.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. esterno_VALORE 연결을 받도록 방화벽이나 hardware_porta 전달을 변경하지 않는다. Ctrl+C로 종료한다.

host terminale 2:

```sh
cd /home/user/jkoros
make run
```

게스트의 `jkoros>` 프롬프트에 input_VALORE:

```text
apps
run hello first second
net
run netcheck
run udp 10.0.2.2 9000 hello
run stress 9000
```

- `hello`: 독립 Java ELF 실행과 effettivo_dati CPU privilegio_VALORE `ring 3`, argomenti uscitaTesto.
- `netcheck`: porta_VALORE 중복, 잘못된 handle_VALORE/puntatore/durata_VALORE, 비차단 받기와 valore 초과 verificare.
- `udp`: IPv4 e_mail·meta_VALORE porta_VALORE·한 Word_VALORE 메시지를 받아 UDP로 보내고 같은 응답을 verificare. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: host `10.0.2.2`의 Assegna_VALORE 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. ricevere_VALORE Loop_VALORE 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. Regolari_articolo 주소는 게스트 `10.0.2.15/24`, gateway_VALORE `10.0.2.2`로 고정돼 있다. QEMU spazio_utente 네트워크의 host accesso_voce 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 app_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java app_f5044b9b Aggiunta_voce

`예제/내프로그램.java`를 Avanti_articolo 형식으로 만든다. 진입점은 argomenti 없는 `static int` 또는 `static void` 함수다. 인수는 spazio_utente API로 조회한다.

```java
public final class 내프로그램 {
    public static int avvia() {
        spazio_utente.Scrittura("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/spazio_utente/app_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := spazio_utente/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.avvia
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `spazio_utente/dichiarazione/spazio_utente.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 Esegui_comando 중인 VM에는 costruire 결과가 자동 반영되지 않는다. app_f5044b9b 이름은 Regolari_articolo 셸의 ASCII input_VALORE 제한에 맞춘 1~15자의 소문자 이름이며 Java Corso_VALORE·FUNZIONE_VALORE·변수에는 한국어를 쓴다. 최대 32개 app_f5044b9b, 한 Esegui_comando 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/compilatore.py --target user --entry messaggio_di_saluto_ae353e94.avvia \
    -o os/build/apps/hello.elf os/spazio_utente/dichiarazione/spazio_utente.java os/spazio_utente/예제/messaggio_di_saluto_ae353e94.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 host 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 Supporto_VALORE ritagliare 안에서 실행한다. `.jar`와 일반 Linux Esegui_comando 파일은 지원하지 않는다.

## spazio_utente 네트워크 API

선언은 `dichiarazione/spazio_utente.java`에 있다. `inviare_dati`/`ricevere_dati`의 `int[]` articolo_elemento 한 개는 byte_VALORE 하나(0~255)를 나타낸다. 한 데이터그램의 최대 dati 길이는 1,024바이트다.

```java
int handle_VALORE = spazio_utente.aperto_rete(0); // 0: 임시 locale_Scope UDP porta_VALORE 자동 selezione_VALORE
int[] dati = new int[32];
dati[0] = 'H'; dati[1] = 'i';
int 보낸길이 = spazio_utente.inviare_dati(handle_VALORE, 0x0a000202, 9000, dati, 2);
int RICEV_SCAD_durata = spazio_utente.ricevere_dati(handle_VALORE, dati, 1500);
spazio_utente.Chiudi_rete(handle_VALORE);
```

effettivo_dati 프로그램에서는 Apri·inviare·받기의 negativo_VALORE 반환값을 각각 검사한다. 완성된 예제는 `예제/dati_comunicazione.java`에 있다. `ricevere_dati`의 aspetta_VALORE 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 ricevere_VALORE 대기열은 한 개뿐이므로 Aggiunta_voce 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | handle_VALORE·Processi_VALORE_voce durata_VALORE·성공 등 해당 함수의 risultato |
| -5 | cellulare_VALORE inviare_VALORE errore_VALORE |
| -9 | 잘못되었거나 닫힌 comunicazione handle_VALORE |
| -11 | 비차단 받기에서 도착한 dati 없음 |
| -14 | spazio_utente puntatore/array_VALORE ritagliare errore |
| -19 | Supporto_VALORE NIC 없음 |
| -22 | porta_VALORE/aspetta_VALORE valore/argomenti VALORE errore |
| -24 | 열린 rete_porta 4개 한도 |
| -38 | 알 numero 없는 시스템 호출 |
| -90 | dati 또는 ricevere_VALORE array_VALORE Dimensione 문제 |
| -98 | locale_Scope porta_VALORE INDICE 중복 |
| -101 | 지원하지 않는 meta_VALORE e_mail |
| -110 | ARP·cellulare_VALORE·ricevere_VALORE valore 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 Codifica_VALORE 있는 Java `int`의 bit_VALORE 패턴을 사용하므로 상위 비트가 1인 reparto_IT_normale IP 주소가 음수로 보일 numero 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## Esegui_comando 경계와 시스템 호출

```text
Shell run → JKAP에서 ELF convalidare·적재 → ring 3 spazio_utente app_f5044b9b
                                 ↓ int 0x80
                      puntatore 검사 → Java kernel_VALORE API → RTL8139/UDP
                                 ↓ Esci_app·eccezione·valore 초과
                                Shell 복귀
```

시스템 호출 레지스터는 `EAX=INDICE`, `EBX,ECX,EDX,ESI,EDI=argomenti`, `EAX=risultato`다. Java 호출 operando_Pila ABI는 컴파일러가 spazio_utente 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| INDICE | 호출 |
| --- | --- |
| 0 | Esci_app(Stato_VALORE CODICE_VALORE) — avvia/errore 런타임에서 usare_VALORE |
| 1 | stringa_VALORE Scrittura |
| 2 / 3 | argomenti articolo_CONTA_NUMERI / argomenti stringa_VALORE e_mail |
| 10 | UDP Apri |
| 11 | UDP inviare(handle_VALORE, IP, meta_VALORE porta_VALORE, array_VALORE e_mail, durata_VALORE) |
| 12 | UDP ricevere(handle_VALORE, array_VALORE e_mail, 제한 밀리초) |
| 13 | UDP Chiudi |
| 14 | locale_Scope IP e_mail |
| 15 / 16 | 마지막 peer_VALORE IP / UDP porta_VALORE |
| 20 | RAM file Lettura(Nome int[] e_mail, uscitaTesto int[] e_mail) |
| 21 | RAM file Scrittura(Nome int[] e_mail, input_VALORE int[] e_mail, byte_VALORE durata_VALORE) |
| 22 | UTF-16 CODICE_VALORE unità_VALORE 문자 uscitaTesto(0~65535) |

file API는 `spazio_utente.파일읽기(int[] Nome, int[] dati)`와 `spazio_utente.scrivere_File(int[] Nome, int[] dati, int durata_VALORE)`다. 이름은 ASCII CODICE_VALORE array_VALORE(최대 64칸, 0 Esci_app 또는 array_VALORE 끝), dati articolo_elemento 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 file 없음 `-2`, puntatore errore `-14`, Nome/durata_VALORE errore `-22`, file slot_VALORE 부족 `-28`, Dimensione 초과 `-90`을 반환한다. 쓰기는 convalidare 후 file 전체를 대체한다. `spazio_utente.scrivere_carattere_VALORE(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`esecuzione_privilegio()`은 시스템 호출이 아니라 spazio_utente 모드에서 CS의 하위 비트를 직접 읽으므로 effettivo_dati Esegui_comando 권한을 확인한다. kernel_VALORE hardware_porta 접근용 `cellulare_VALORE` native 함수는 spazio_utente target 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 Esegui_comando, 파이프, 프로세스 간 통신은 없다. Esegui_comando 파일은 커널의 Lettura 전용 JKAP 묶음에서 적재한다. dati 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- spazio_utente 가상 e_mail `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. Esegui_comando 영상은 frontale_VALORE 2MiB, 인수는 `0x04300000`부터, 스택은 area_VALORE 끝에서 시작한다. kernel_VALORE identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB spazio_utente 영역을 비우고 file 구역을 복사해 BSS·array_VALORE 영역을 초기화한다. spazio_utente GC는 없지만 Esci_app 후 Avanti_articolo Esegui_comando 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 offerta/이스케이프 파싱은 없다.
- spazio_utente 페이지의 CODICE_VALORE/dati 분리 Lettura 전용 Impostazioni, NX, operando_Pila guard, ASLR은 아직 없다. 커널과 spazio_utente Memoria_dati·hardware_porta privilegio_VALORE 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 Esegui_comando 상한을 두며 valore 초과는 `Exit: 124`다. spazio_utente CPU 예외는 `128 + eccezione INDICE`(페이지 errore 142, 특권 위반 141), Java array_VALORE/계산 오류는 101~105다. kernel_VALORE 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, statico_VALORE IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP checksum 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- spazio_utente Esegui_comando·네트워크·proteggere_VALORE limite_VALORE 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 Esegui_comando·reparto_IT_normale 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## convalidare 근거

`make test`는 compilatore 14개 prove, Java 패킷 condizione 2,201개 검사, 기존 Shell ELF/ISO avvio_macchina prove, spazio_utente ELF/effettivo_dati UDP/proteggere_VALORE limite_VALORE 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 durata_VALORE·해시까지 `os/build/test_Usenet.json`에 기록한다. 시험용 손상된 ELF·특권 comando·무한 sprint_VALORE 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 dati: [Intel 시스템 프로그래밍 specifica](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 implementazione](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 README_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
