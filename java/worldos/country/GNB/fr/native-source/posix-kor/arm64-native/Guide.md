# interne ARM64 Java 커널의 C/C++ Fichier·루프백 connecter

이 디렉터리는 `platforms/rpi4-native` interne valeurNoyau 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`Entêtes/ABIFichier.h`는 français 함수명과 `extern "C"` ABI를 제공한다. `connecter.c`는 valeurNoyau 안에서 AOT Java Fichier 메서드에 직접 연결하고, `pontUtilisateur.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. donnéesEffectif Fichier 처리는 `FichiersMémoire.java`, 루프백 datagramme 처리는 `RéseauBoucleRetour.java`, 연결형 흐름은 `RéseauFlux.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 valeurNoyau 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`opérandeTroisième. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·valeurPointFlottant valeurOpération·Fichier·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

valeurPriseEnCharge: `ouvrirFichier`, `lireDonnéesFichier`, `écrireDonnéesFichier`, `fermerFichier`, `positionnerFichier`, `supprimerNomEntréeÉlémentFichier`, `définirLongueurFichier`, valeurAuxiliaire Fonction `tailleFichier`. erreur 시 -1과 작업별 `numéroErreur`를 반환한다. `stockageFichierConfirmer`은 RAM 파일이므로 ENOSYS를 반환한다. Fichier 16개, 각 16384바이트, nom 63바이트, entréeÉlémentDescripteur 16개이며 RAM 디렉터리·valeurPairRéseau/절대 경로를 제공한다. valeurPermission/영속 저장은 없다.

사용자용 `Entêtes/ABIRéseau.h`는 donnéesEffectif français 함수와 독립 구조체를 선언한다.
`créerExtrémité`, `associerAdresse`, `envoyerDonnéesDatagramme/recevoir`, `connecterRéseau/attendreFin/recevoir`는
`pontUtilisateur.c`에서 SVC를 호출하며 valeurMacro 별칭이 아니다. `struct AdressePriseRéseauInternet`의
`familleAdresse`, `numéroPort`, `AdresseInternet.valeurAdresse`을 사용한다. 상수는 enum의
`FamilleInternet`, `PriseRéseauDatagramme`, `ProtocoleDatagramme`, `RéseauFlux`, `protocoleTransportFlux`이다.
français·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. valeurExtérieur 통신은 interne 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. donnéesEffectif Pi 4 GENET 드라이버는 미지원이다.
소켓도 donnéesEffectif Fonction `fermerFichier`로 닫는다.

[사용법·Architecture·limiteFrontière](../../platforms/rpi4-native/README.md), [Utilisateur ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ Fichier Exemples](../../platforms/rpi4-native/Utilisateur/ExempleFichier.cpp), [UDP 루프백 Exemples](../../platforms/rpi4-native/Utilisateur/ExempleCommunication.cpp), [기존 valeurNoyau 내부 invoquer Tests](../../platforms/rpi4-native/Tests/AppelsFichier.cpp)을 참고한다.

C11/C++11의 texteHangul valeurIdentificateur·헤더 valeurUtiliser, SDK construireSystème, ELF 업로드·exécuterCommande, erreur/valeurSousPartie sortieEntrée 처리는 [texteHangul développement 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 Communication Exemples](../../platforms/rpi4-native/Exemples/CodageHangul/valeurFlux.c)도 제공한다.
