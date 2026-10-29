# VirtualBox befehlAusführen

```sh
cd ~/jkoros
make vbox
```

별도로 VM을 만들거나 ISO를 연결할 필요가 없다. anfänglichElementeintrag 실행하면 `os/build/kernel.iso`를 빌드하고 `jkoros operating system`이라는 전용 VM을 만들어 VirtualBox 창으로 부팅한다. `jkoros/os` 안에서도 `make vbox`를 사용할 Zahl 있다.

게스트의 `jkoros>` 프롬프트에서 nächsterElementeintrag 명령을 입력한다.

```text
help
apps
run hello vbox
```

letzterElementeintrag 명령은 별도 Java ELF를 실행한다. `USER MODE ring 3`, `arg: vbox`, `Exit: 0` Ausgabe danachStatuswert 셸로 돌아오면 정상이다. VGA 화면은 aktuellElementeintrag ASCII 글꼴만 지원하므로 한글은 `?`로 보이며, HangulText 원문은 seriellWert 기록에서 확인할 Zahl 있다.

## statuswertWert 확인과 erneutVersuchenWert befehlAusführen

```sh
make vbox-status
```

이 명령은 VM statuswertWert, ISO와 seriellWert 기록의 절대 경로를 JSON으로 출력한다.

| aktuellElementeintrag statuswertWert | `make vbox` aktion |
| --- | --- |
| 아직 생성하지 않음 | ISO systemErzeugenAbbild → 전용 VM generieren → Startvorgang |
| hatVerlassen (`poweroff`, `aborted`) | ISO systemErzeugenAbbild → 광학 medienWert auffrischen → 새로 Startvorgang |
| befehlAusführen 중 (`running`) | 재빌드·재부팅 없이 aktuellElementeintrag VM wertBeibehalten |
| 일시정지 (`paused`) | 기존 VM fortführenAusführung |
| 저장됨 (`saved`) | vorherigElementeintrag seriellWert 기록을 복사해 보관하고 ablegenDatenWert statuswertWert fortführenAusführung |
| ablegenDatenWert·ausführenVorgang 등 umschaltenBetriebsart 중 | 변경하지 않고 Aufgabe istFertig danachStatuswert 재실행하도록 Anleitung |

quelltextBaum 변경을 반영하려면 VM을 종료한 nächsterElementeintrag erneutVersuchenWert `make vbox`를 실행한다. **ablegenDatenWert 상태를 재개하면 vorherigElementeintrag 커널이 fortsetzenVerarbeitung 실행되므로 새 빌드를 반영하지 않는다.** 실행기는 강제 종료하거나 ablegenDatenWert 상태를 폐기하지 않는다. VirtualBox 창을 닫을 때 사용자가 전원 끄기를 선택하면 speicherDaten 상태가 사라지므로 보존할 작업이 없는지 먼저 확인한다. 게스트의 `halt`는 CPU만 멈추며 VirtualBox의 전원을 끄는 명령은 아니다.

fenster 없는 실행이 필요하면 VM이 꺼져 있을 때 사용한다.

```sh
make vbox VBOX_TYPE=headless
```

befehlAusführen 중인 VM에 erneutVersuchenWert 명령을 내려도 GUI/headless 방식은 바뀌지 않는다. standardwertWert Name 대신 다른 이름이 필요하면 **최초 generieren 시에만** `VBOX_NAME="원하는 Name"`을 지정하고 이후에도 같은 값을 사용한다.

## 설정과 Daten 보존

- standardwertWert 설정은 BIOS, speicherDaten 64MiB, CPU 1개, VGA speicherDaten 16MiB, IDE 광학 부팅이다. 가상 하드디스크를 만들지 않는다.
- VM 설정은 `.vbox/machines/`, inhaltswertWert 검사합별 ISO 사본은 `.vbox/media/`, seriellWert 기록은 `.vbox/logs/`에 보관한다. `.vbox/state.json`은 전용 VM의 UUID와 eigentümerWert 표식을 저장한다.
- 꺼진 VM을 부팅할 때 새 seriellWert 기록을 만든다. ablegenDatenWert statuswertWert fortführenAusführung 전의 기록은 `before-resume-*.log`로 복사한다. ablegenDatenWert statuswertWert 자체는 삭제하지 않고 VirtualBox가 그대로 재개한다.
- 같은 이름의 다른 VM을 인수하지 않는다. UUID·einstellungen pfad·eigentümerWert 표식을 검사하며, 사용자가 별도로 연결한 디스크나 광학 매체를 자동 교체하지 않는다.
- 기존 ISO 사본과 기록은 자동 삭제하지 않는다. `.vbox`는 Git ausschließenWert 대상이다. 용량을 정리할 때도 befehlAusführen·ablegenDatenWert 상태의 VM이 참조하는 파일과 관리 정보를 임의로 삭제하지 않는다.
- VirtualBox 또는 Wirtssystem 드라이버가 없으면 오류를 안내한다. 자동 wertEinrichten, verwalterWert erlaubnisWert befehlAusführen, Gerät erlaubnisWert 변경은 하지 않는다.

## 네트워크 grenzwertWert

aktuellElementeintrag 커널의 RTL8139 드라이버는 QEMU에서 사용한다. VirtualBox의 PCnet/E1000 드라이버는 아직 구현하지 않아 이 실행기는 네트워크 장치를 비활성화한다. 셸과 Benutzer 프로그램은 실행되지만 UDP 열기는 `-19`로 실패한다. UDP 왕복은 `make run`과 [Benutzer befehlAusführen·네트워크 Anleitung](../os/Benutzer/Anleitung.md)의 절차로 시험한다.

## validieren

`make test-vbox`는 가짜 VirtualBox 응답을 사용하여 새 VM generieren, befehlAusführen·ablegenDatenWert·일시정지·umschaltenBetriebsart statuswertWert, Name 충돌, 소유권 불일치, Benutzer medienWert wertSchützen, systemErzeugenAbbild fehlschlagWert, 중단된 generieren statuswertWiederherstellen, ISO wertÄndern 감지, pfad wertSchützen 등을 검사한다. tatsächlichDaten VM을 만들거나 변경하지 않는다.

2026-09-13에 ProgrammStarter einheitWert Prüfungen 16개가 통과했다. 별도로 tatsächlichDaten VirtualBox 5.2.42에서 `make vbox`의 VM generieren·GUI Startvorgang, `JAVA SELFTEST PASS`, 셸의 `run hello vbox` 실행과 `Exit: 0`, befehlAusführen 중 재호출 시 재부팅하지 않는 aktion 및 `make vbox-status`를 확인했다. ablegenDatenWert·일시정지 분기는 einheitWert 시험으로 검증했다.
