# interne ARM64 커널의 Codex installerValeur 가능성 검토

검토일: 2026-10-05. 소스와 공식 문서를 대조한 설계 검토이며, 게스트에 Codex를 설치하거나
로그인·모델 호출을 실행한 결과는 아니다. interne ARM64 커널과 `../rpi4` Linux 실행판은 구분한다.

élémentListeActuel interne 커널에는 공식 Codex CLI를 그대로 installerValeur·실행할 nombre 없다.
기술적으로 필요한 exécuterCommande 환경을 추가하거나 Codex를 이식하는 경로는 있으나,
다운로드 commande 하나를 추가하는 작업으로 해결되지 않는다. JDK/JRE 기능 확장만으로도 해결되지 않는다.

## 확인한 근거

| valeurEntréeÉlément | élémentListeActuel 소스에서 확인한 valeurÉtatValeur | 직접 실행을 위한 Tâche |
|---|---|---|
| exécuterCommande Fichier | `machine/Utilisateur.c`: AArch64 ET_EXEC만, PT_INTERP/PT_DYNAMIC/PT_TLS rejeterValeur, 업로드 exécuterCommande 버퍼 16384바이트 | valeurCible 바이너리에 맞는 ELF 적재·재배치·exécuterCommande initialiser, donnéesMémoire/Fichier valeurLimite valeurExtension |
| Linux ABI | `machine/compatibilitéLinux.inc`: read/write/openat/brk 등 제한된 번호만 entréeÉlémentValeurProcessus, 나머지는 ENOSYS | libc/런타임에 필요한 시스템 호출을 추가하거나 interne ABI용 런타임 Portage |
| 프로세스·스레드 | 일반 fork/clone/execve, pthread/futex, 시그널, mmap, poll/epoll 계열이 미완성 | 비동기 I/O·스레드·valeurEnfant commande exécuterCommande·programmeQuitter/opérationAnnuler 기능 |
| Fichier | `source/FichiersMémoire.java`: RAM Fichier 64개, 파일당 16 KiB, 비영속 | 큰 exécuterCommande Fichier·프로젝트·réglages·세션을 위한 영속 VFS, Fichier valeurPermission·chemin·디렉터리 valeurExtension |
| 네트워크 | lwIP TCP/UDP는 있으나 `PileRéseau/lwipopts.h`의 LWIP_DNS=0, 일반 HTTPS 클라이언트 méthodeManquant | DNS, TLS 인증서 valider·신뢰 racineDépôt·정확한 valeurHorodatage, HTTPS/스트리밍 |
| terminal·Outils | interne 셸과 GUI 터미널은 있지만 표준 PTY·일반 프로세스 Tâche valeurContrôle méthodeManquant | interactif CLI용 terminal 기능, interpréteurCommandes/Fichier 검색/construireSystème Outils connecter |
| exécuterCommande valeurPermission | EL0 보호는 있으나 Codex의 Linux 샌드박스와 같은 정책 집행 environnement méthodeManquant | Fichier·네트워크·commande valeurPermission 정책과 승인 기능; interne 커널에 맞는 격리 réalisation |

여기서 ELF의 PT_TLS는 스레드별 valeurStocker 공간이다. HTTPS의 TLS valeurMotPasse 통신과 서로 다른 기능이다.
ELF Fichier 형식을 읽을 nombre 있다는 사실만으로 Linux exécuterCommande 환경을 제공하는 것은 아니다.
SSH/VNC를 위한 valeurMotPasse 라이브러리를 넣은 상태도 HTTPS réalisation 완료를 의미하지 않는다.

호스트의 `/home/user/.local/bin/codex`도 확인했다. 이것은 x86-64 ELF ET_DYN이며 약 209 MiB다.
해당 파일을 ARM64 게스트로 복사하여 실행할 nombre 없다. 이 크기를 ARM64 valeurDistribution 파일의 크기로
해석하지 않는다. 공식 ARM64 빌드의 donnéesEffectif taille·의존성은 설치할 버전으로 ajouterFinEntréeÉlément 검사해야 한다.

## 가능한 réalisation chemin

1. **interne 커널에 공식 CLI 직접 Portage**
   영속 valeurStocker/VFS와 Utilisateur donnéesMémoire, 프로세스·스레드·I/O, libc/런타임, DNS/HTTPS,
   terminal·valeurPermission 체계를 갖춘다. valeurAprès valeurCible 버전의 의존성을 조사하여 크로스 construireSystème·이식한다.
   Linux 커널을 반드시 탑재할 필요는 없지만, 공식 Linux 바이너리를 그대로 쓸 경우
   그 바이너리가 사용하는 Linux ABI까지 호환해야 한다. 큰 SystèmeExploitation développement 과제다.

2. **valeurExtérieur Hôte Codex와 interne valeurNoyau connecter — élémentListePremier 구현으로 권장**
   Linux PC에서 공식 CLI 또는 app-server를 실행하고 jkoros에는 전용 Utilisateur commande/화면을 만든다.
   호스트의 인증된 연결과 게스트 Fichier lire·modifierValeur·업로드·commande exécuterCommande 어댑터가 필요하다.
   기존 SSH/TCP 경로를 활용할 nombre 있으나, Fichier 동기화나 Codex 전용 어댑터는 élémentListeActuel 구현되어 있지 않다.
   호스트에서 수행한 빌드와 게스트에서 수행한 exécuterCommande 결과를 명확히 구분한다.
   이 구성은 interne 커널을 유지하지만, 공식 CLI 자체는 valeurExtérieur 호스트에서 실행된다.

3. **interne API 클라이언트 제작**
   interne ABI의 C 또는 지원되는 Java 부분집합으로 sessionInteractif UI와 Fichier/commande Outils invoquer 루프를 만든다.
   valeurExtérieur 중계기를 쓰지 않는다면 DNS/valider 가능한 TLS/HTTPS와 인증 Données 저장을 먼저 구현해야 한다.
   이는 OpenAI API를 이용하는 별도 에이전트이며 공식 Codex CLI 전체의 이식으로 표시하지 않는다.

4. **별도 ARM64 Linux 실행판에서 installerValeur**
   `../rpi4`는 Linux와 musl 기반이므로 일반 Linux installerValeur 경로를 검토할 nombre 있다.
   사용할 Codex 버전의 ARM64·musl 호환성, dépendances, 커널의 샌드박스 지원을 donnéesEffectif 검증해야 한다.
   이번 검토에서 installerValeur 성공을 확인하지 않았다. 이 결과를 interne Java 커널의 지원으로 표시하지 않는다.

## 단계별 estTerminé racineProjet

- 직접 Portage: `--version` lancer → 인증/HTTPS → Fichier lire·modifierValeur → valeurEnfant commande exécuterCommande →
  interactif valeurEntrée/스트리밍 → valeurPermission valeurLimite·opérationAnnuler → 재부팅 étatValeurAprès réglages/세션 보존을 각각 donnéesEffectif 게스트에서 확인한다.
- Hôte connecter: 게스트에서 requête valeurEntrée → Hôte Codex entréeÉlémentValeurProcessus → 게스트 Fichier changerValeur vérifier →
  게스트 javac/cc exécuterCommande → résultat 표시를 처음부터 끝까지 검증한다.
- COSL 상업 조건을 유지하려면 새로 도입하는 런타임/Communication 라이브러리의 라이선스와
  Codex valeurDistribution 버전의 제3자 고지를 검토한다. valeurExtérieur 구성요소를 일괄 COSL로 재라이선스하지 않는다.

## 공식 Documentation

- [Codex CLI installerValeur 및 action](https://learn.chatgpt.com/docs/codex/cli): 표준 Linux/macOS 독립 installerValeur 경로와 프로젝트 Fichier·commande Tâche.
- [인증](https://learn.chatgpt.com/docs/auth): ChatGPT/API 인증, 헤드리스 장치의 `codex login --device-auth`, HTTPS 인증서 réglages.
- [샌드박스](https://learn.chatgpt.com/docs/sandboxing): 운영체제별 집행 modeMéthode, Linux의 bubblewrap 및 Utilisateur 네임스페이스 valeurExigence 사항.
- [공개 구성요소](https://learn.chatgpt.com/docs/open-source): CLI/SDK/app-server의 공개 arbreSource 위치와 비공개 구성요소 valeurDélimiteur.

공식 문서에는 jkoros를 valeurPriseEnCharge 대상으로 명시한 내용이 없다. valeurSommet réalisation chemin·développement 순서는
élémentListeActuel 소스와 valeurExigence 기능을 대조한 기술적 판단이다.
