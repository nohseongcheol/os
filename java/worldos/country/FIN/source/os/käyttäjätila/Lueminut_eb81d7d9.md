# 셸에서 실행하는 käyttäjätila 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java kehitystuote ympäristö Lueminut_eb81d7d9](../../문서/Java_kehitysympäristö.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 Suorita_komento

isäntä komentotulkki 1:

```sh
cd /home/user/jkoros
python3 os/työkalut/päivitys_data.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. ulkoinen_ARVO 연결을 받도록 방화벽이나 laitteisto_portti 전달을 변경하지 않는다. Ctrl+C로 종료한다.

isäntä komentotulkki 2:

```sh
cd /home/user/jkoros
make run
```

게스트의 `jkoros>` 프롬프트에 syöte_ARVO:

```text
apps
run hello first second
net
run netcheck
run udp 10.0.2.2 9000 hello
run stress 9000
```

- `hello`: 독립 Java ELF 실행과 todellinen_data CPU lupa_ARVO `ring 3`, argumentit tulostuspaikka.
- `netcheck`: portti_ARVO 중복, 잘못된 kahva_ARVO/osoitin/kesto_ARVO, 비차단 받기와 AIKA_ARVO 초과 tarkistaa.
- `udp`: IPv4 OSOITE·kohde_ARVO portti_ARVO·한 Word_ARVO 메시지를 받아 UDP로 보내고 같은 응답을 tarkistaa. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: isäntä `10.0.2.2`의 Määritä_ARVO 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. saada_ARVO Loop_ARVO 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. nykyinen_kohde 주소는 게스트 `10.0.2.15/24`, yhdyskäytävä_ARVO `10.0.2.2`로 고정돼 있다. QEMU käyttäjätila 네트워크의 isäntä pääsy_merkintä_68aed533 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 ohjelma_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java ohjelma_f5044b9b liitä_merkintä

`예제/내프로그램.java`를 Seuraava_kohde 형식으로 만든다. 진입점은 argumentit 없는 `static int` 또는 `static void` 함수다. 인수는 käyttäjätila API로 조회한다.

```java
public final class 내프로그램 {
    public static int Suorita_2() {
        käyttäjätila.Kirjoitus("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/käyttäjätila/ohjelma_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := käyttäjätila/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.Suorita_2
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `käyttäjätila/esittely/käyttäjätila.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 Suorita_komento 중인 VM에는 kääntää_Järjestelmä 결과가 자동 반영되지 않는다. ohjelma_f5044b9b 이름은 nykyinen_kohde 셸의 ASCII syöte_ARVO 제한에 맞춘 1~15자의 소문자 이름이며 Java Luokka_ARVO·funktio_ARVO·변수에는 한국어를 쓴다. 최대 32개 ohjelma_f5044b9b, 한 Suorita_komento 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/kääntäjä.py --target user --entry 인사.Suorita_2 \
    -o os/build/apps/hello.elf os/käyttäjätila/esittely/käyttäjätila.java os/käyttäjätila/예제/인사.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 isäntä 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 Tuki_ARVO leikata 안에서 실행한다. `.jar`와 일반 Linux Suorita_komento 파일은 지원하지 않는다.

## käyttäjätila 네트워크 API

선언은 `esittely/käyttäjätila.java`에 있다. `lähettää_data_5b5410b2`/`saada_data`의 `int[]` kohde_elementti 한 개는 tavu_ARVO 하나(0~255)를 나타낸다. 한 데이터그램의 최대 data 길이는 1,024바이트다.

```java
int kahva_ARVO = käyttäjätila.avata_verkko(0); // 0: 임시 paikallinen_laajuus UDP portti_ARVO 자동 valinta_ARVO
int[] data = new int[32];
data[0] = 'H'; data[1] = 'i';
int 보낸길이 = käyttäjätila.lähettää_data_5b5410b2(kahva_ARVO, 0x0a000202, 9000, data, 2);
int SAATU_HINTA_kesto = käyttäjätila.saada_data(kahva_ARVO, data, 1500);
käyttäjätila.Sulje_verkko(kahva_ARVO);
```

todellinen_data 프로그램에서는 Avaa·lähettää·받기의 음수 반환값을 각각 검사한다. 완성된 예제는 `예제/자료통신.java`에 있다. `saada_data`의 odottaa_ARVO 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 saada_ARVO 대기열은 한 개뿐이므로 liitä_merkintä 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | kahva_ARVO·prosessi_ARVO_merkintä kesto_ARVO·성공 등 해당 함수의 TULOS |
| -5 | laite_ARVO lähettää_ARVO virhe_ARVO |
| -9 | 잘못되었거나 닫힌 통신 kahva_ARVO |
| -11 | 비차단 받기에서 도착한 data 없음 |
| -14 | käyttäjätila osoitin/MATRIISI_ARVO leikata VIRHE |
| -19 | Tuki_ARVO NIC 없음 |
| -22 | portti_ARVO/odottaa_ARVO AIKA_ARVO/argumentit ARVO VIRHE |
| -24 | 열린 verkko_portti 4개 한도 |
| -38 | 알 numero 없는 시스템 호출 |
| -90 | data 또는 saada_ARVO MATRIISI_ARVO Koko 문제 |
| -98 | paikallinen_laajuus portti_ARVO INDEKSI 중복 |
| -101 | 지원하지 않는 kohde_ARVO OSOITE |
| -110 | ARP·laite_ARVO·saada_ARVO AIKA_ARVO 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 koodaus_ARVO 있는 Java `int`의 bitti_ARVO 패턴을 사용하므로 상위 비트가 1인 tietojärjestelmät_normaali IP 주소가 음수로 보일 numero 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## Suorita_komento 경계와 시스템 호출

```text
liittymä run → JKAP에서 ELF vahvista·적재 → ring 3 käyttäjätila ohjelma_f5044b9b
                                 ↓ int 0x80
                      osoitin 검사 → Java ydin_ARVO API → RTL8139/UDP
                                 ↓ Lopeta_ohjelma·poikkeus·AIKA_ARVO 초과
                                liittymä 복귀
```

시스템 호출 레지스터는 `EAX=INDEKSI`, `EBX,ECX,EDX,ESI,EDI=argumentit`, `EAX=TULOS`다. Java 호출 operandi_Pino ABI는 컴파일러가 käyttäjätila 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| INDEKSI | 호출 |
| --- | --- |
| 0 | Lopeta_ohjelma(Tila_ARVO KOODI_ARVO) — Suorita_2/VIRHE 런타임에서 käyttö_ARVO |
| 1 | merkkijono_ARVO Kirjoitus |
| 2 / 3 | argumentit kohde_LASKE / argumentit merkkijono_ARVO OSOITE |
| 10 | UDP Avaa |
| 11 | UDP lähettää(kahva_ARVO, IP, kohde_ARVO portti_ARVO, MATRIISI_ARVO OSOITE, kesto_ARVO) |
| 12 | UDP saada(kahva_ARVO, MATRIISI_ARVO OSOITE, 제한 밀리초) |
| 13 | UDP Sulje |
| 14 | paikallinen_laajuus IP OSOITE |
| 15 / 16 | 마지막 vertaissolmu_ARVO IP / UDP portti_ARVO |
| 20 | RAM tiedoston_nimi Luku(Nimi int[] OSOITE, tulostuspaikka int[] OSOITE) |
| 21 | RAM tiedoston_nimi Kirjoitus(Nimi int[] OSOITE, syöte_ARVO int[] OSOITE, tavu_ARVO kesto_ARVO) |
| 22 | UTF-16 KOODI_ARVO osio_ARVO_7c611f50 문자 tulostuspaikka(0~65535) |

tiedoston_nimi API는 `käyttäjätila.lukea_Tiedosto(int[] Nimi, int[] data)`와 `käyttäjätila.kirjoitus_Tiedosto(int[] Nimi, int[] data, int kesto_ARVO)`다. 이름은 ASCII KOODI_ARVO MATRIISI_ARVO(최대 64칸, 0 Lopeta_ohjelma 또는 MATRIISI_ARVO 끝), data kohde_elementti 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 tiedoston_nimi 없음 `-2`, osoitin VIRHE `-14`, Nimi/kesto_ARVO VIRHE `-22`, tiedoston_nimi paikka_ARVO 부족 `-28`, Koko 초과 `-90`을 반환한다. 쓰기는 vahvista 후 tiedoston_nimi 전체를 대체한다. `käyttäjätila.kirjoitus_merkki_ARVO(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`suoritus_lupa()`은 시스템 호출이 아니라 käyttäjätila 모드에서 CS의 하위 비트를 직접 읽으므로 todellinen_data Suorita_komento 권한을 확인한다. ydin_ARVO laitteisto_portti 접근용 `laite_ARVO` native 함수는 käyttäjätila tavoite 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 Suorita_komento, 파이프, 프로세스 간 통신은 없다. Suorita_komento 파일은 커널의 Luku 전용 JKAP 묶음에서 적재한다. data 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- käyttäjätila 가상 OSOITE `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. Suorita_komento 영상은 etukamera_ARVO 2MiB, 인수는 `0x04300000`부터, 스택은 alue_ARVO_0e9a97ab 끝에서 시작한다. ydin_ARVO identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB käyttäjätila 영역을 비우고 tiedoston_nimi 구역을 복사해 BSS·MATRIISI_ARVO 영역을 초기화한다. käyttäjätila GC는 없지만 Lopeta_ohjelma 후 Seuraava_kohde Suorita_komento 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 Lainaus/이스케이프 파싱은 없다.
- käyttäjätila 페이지의 KOODI_ARVO/data 분리 Luku 전용 Asetukset, NX, operandi_Pino guard, ASLR은 아직 없다. 커널과 käyttäjätila Muisti_data·laitteisto_portti lupa_ARVO 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 Suorita_komento 상한을 두며 AIKA_ARVO 초과는 `Exit: 124`다. käyttäjätila CPU 예외는 `128 + poikkeus INDEKSI`(페이지 VIRHE 142, 특권 위반 141), Java MATRIISI_ARVO/계산 오류는 101~105다. ydin_ARVO 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, staattinen_ARVO IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP tarkistussumma 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- käyttäjätila Suorita_komento·네트워크·suojata_ARVO rajattu_alue_ARVO 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 Suorita_komento·tietojärjestelmät_normaali 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## vahvista 근거

`make test`는 kääntäjä 14개 testit, Java 패킷 ehto 2,201개 검사, 기존 liittymä ELF/ISO koneen_käynnistys testit, käyttäjätila ELF/todellinen_data UDP/suojata_ARVO rajattu_alue_ARVO 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 kesto_ARVO·해시까지 `os/build/testi_käyttäjä_verkko.json`에 기록한다. 시험용 손상된 ELF·특권 komento·무한 sprintti_ARVO 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 data: [Intel 시스템 프로그래밍 määritys](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 toteutus](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 Lueminut_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
