# VirtualBox exécuterCommande

```sh
cd ~/jkoros
make vbox
```

별도로 VM을 만들거나 ISO를 연결할 필요가 없다. élémentListeInitialValeur 실행하면 `os/build/kernel.iso`를 빌드하고 `jkoros operating system`이라는 전용 VM을 만들어 VirtualBox 창으로 부팅한다. `jkoros/os` 안에서도 `make vbox`를 사용할 nombre 있다.

게스트의 `jkoros>` 프롬프트에서 élémentListeSuivant 명령을 입력한다.

```text
help
apps
run hello vbox
```

élémentListeDernier 명령은 별도 Java ELF를 실행한다. `USER MODE ring 3`, `arg: vbox`, `Exit: 0` Sortie étatValeurAprès 셸로 돌아오면 정상이다. VGA 화면은 élémentListeActuel ASCII 글꼴만 지원하므로 한글은 `?`로 보이며, texteHangul 원문은 valeurSériel 기록에서 확인할 nombre 있다.

## valeurÉtatValeur 확인과 valeurRéessayer exécuterCommande

```sh
make vbox-status
```

이 명령은 VM valeurÉtatValeur, ISO와 valeurSériel 기록의 절대 경로를 JSON으로 출력한다.

| élémentListeActuel valeurÉtatValeur | `make vbox` action |
| --- | --- |
| 아직 생성하지 않음 | ISO construireSystème → 전용 VM générer → Amorçage |
| possèdeQuitté (`poweroff`, `aborted`) | ISO construireSystème → 광학 valeurSupports actualiser → 새로 Amorçage |
| exécuterCommande 중 (`running`) | 재빌드·재부팅 없이 élémentListeActuel VM retenirValeur |
| 일시정지 (`paused`) | 기존 VM exécutionReprendre |
| 저장됨 (`saved`) | élémentListePrécédentÉlément valeurSériel 기록을 복사해 보관하고 valeurStocker valeurÉtatValeur exécutionReprendre |
| valeurStocker·lancer 등 modeCommuter 중 | 변경하지 않고 Tâche estTerminé étatValeurAprès 재실행하도록 Guide |

arbreSource 변경을 반영하려면 VM을 종료한 élémentListeSuivant valeurRéessayer `make vbox`를 실행한다. **valeurStocker 상태를 재개하면 élémentListePrécédentÉlément 커널이 traitementContinuer 실행되므로 새 빌드를 반영하지 않는다.** 실행기는 강제 종료하거나 valeurStocker 상태를 폐기하지 않는다. VirtualBox 창을 닫을 때 사용자가 전원 끄기를 선택하면 donnéesMémoire 상태가 사라지므로 보존할 작업이 없는지 먼저 확인한다. 게스트의 `halt`는 CPU만 멈추며 VirtualBox의 전원을 끄는 명령은 아니다.

fenêtre 없는 실행이 필요하면 VM이 꺼져 있을 때 사용한다.

```sh
make vbox VBOX_TYPE=headless
```

exécuterCommande 중인 VM에 valeurRéessayer 명령을 내려도 GUI/headless 방식은 바뀌지 않는다. valeurDéfaut nom 대신 다른 이름이 필요하면 **최초 générer 시에만** `VBOX_NAME="원하는 nom"`을 지정하고 이후에도 같은 값을 사용한다.

## 설정과 Données 보존

- valeurDéfaut 설정은 BIOS, donnéesMémoire 64MiB, CPU 1개, VGA donnéesMémoire 16MiB, IDE 광학 부팅이다. 가상 하드디스크를 만들지 않는다.
- VM 설정은 `.vbox/machines/`, valeurContenuValeur 검사합별 ISO 사본은 `.vbox/media/`, valeurSériel 기록은 `.vbox/logs/`에 보관한다. `.vbox/state.json`은 전용 VM의 UUID와 valeurPropriétaire 표식을 저장한다.
- 꺼진 VM을 부팅할 때 새 valeurSériel 기록을 만든다. valeurStocker valeurÉtatValeur exécutionReprendre 전의 기록은 `before-resume-*.log`로 복사한다. valeurStocker valeurÉtatValeur 자체는 삭제하지 않고 VirtualBox가 그대로 재개한다.
- 같은 이름의 다른 VM을 인수하지 않는다. UUID·réglages chemin·valeurPropriétaire 표식을 검사하며, 사용자가 별도로 연결한 디스크나 광학 매체를 자동 교체하지 않는다.
- 기존 ISO 사본과 기록은 자동 삭제하지 않는다. `.vbox`는 Git valeurExclure 대상이다. 용량을 정리할 때도 exécuterCommande·valeurStocker 상태의 VM이 참조하는 파일과 관리 정보를 임의로 삭제하지 않는다.
- VirtualBox 또는 Hôte 드라이버가 없으면 오류를 안내한다. 자동 installerValeur, valeurGestionnaire valeurPermission exécuterCommande, Périphérique valeurPermission 변경은 하지 않는다.

## 네트워크 valeurLimite

élémentListeActuel 커널의 RTL8139 드라이버는 QEMU에서 사용한다. VirtualBox의 PCnet/E1000 드라이버는 아직 구현하지 않아 이 실행기는 네트워크 장치를 비활성화한다. 셸과 Utilisateur 프로그램은 실행되지만 UDP 열기는 `-19`로 실패한다. UDP 왕복은 `make run`과 [Utilisateur exécuterCommande·네트워크 Guide](../os/Utilisateur/Guide.md)의 절차로 시험한다.

## valider

`make test-vbox`는 가짜 VirtualBox 응답을 사용하여 새 VM générer, exécuterCommande·valeurStocker·일시정지·modeCommuter valeurÉtatValeur, nom 충돌, 소유권 불일치, Utilisateur valeurSupports protégerValeur, construireSystème valeurÉchec, 중단된 générer récupérerÉtatValeur, ISO changerValeur 감지, chemin protégerValeur 등을 검사한다. donnéesEffectif VM을 만들거나 변경하지 않는다.

2026-09-13에 LanceurProgramme valeurUnité Tests 16개가 통과했다. 별도로 donnéesEffectif VirtualBox 5.2.42에서 `make vbox`의 VM générer·GUI Amorçage, `JAVA SELFTEST PASS`, 셸의 `run hello vbox` 실행과 `Exit: 0`, exécuterCommande 중 재호출 시 재부팅하지 않는 action 및 `make vbox-status`를 확인했다. valeurStocker·일시정지 분기는 valeurUnité 시험으로 검증했다.
