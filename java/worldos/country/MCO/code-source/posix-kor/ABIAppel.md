# Utilisateur invoquer valeurFrontière

대상은 jkoros i386 ELF32다. Linux i386의 invoquer 번호와 바이너리 호환이 아니다. C의 cdecl 인수를 `machine/AppelsSystèmeExploitation.s`에서 EAX(numéro), EBX·ECX·EDX·ESI·EDI(ordinalPremier~ordinalCinquième arguments)로 변환한다. EBX·ESI·EDI·EBP를 보존하며 결과는 EAX다. valeurNoyau 실패는 valeurNégatif erreur numéro, C bibliothèque 실패는 -1과 양수 errno다.

커널은 0x04000000 이상, 0x04400000 미만의 Utilisateur valeurRégion 안에 자료의 전체 길이가 들어가는지 확인한다. 단순 널 검사가 아니다. C Données 주소는 valeurOctet 주소이며, 기존 Java AOT `int[]` 포인터와 혼용하지 않는다. Java Fichier 흐름의 어셈블리 경계가 별도 valeurOctet 버퍼를 마련하여 같은 호출을 사용한다.

| numéro | action | arguments |
|---|---|---|
| 30 | ouvrirFichier | NUL terminaison nom adresse, réglages, accorderPermission |
| 31 | lireDonnéesFichier | entréeÉlémentDescripteur, Données adresse, valeurOctet nombre |
| 32 | écrireDonnéesFichier | entréeÉlémentDescripteur, Données adresse, valeurOctet nombre |
| 33 | fermerFichier | entréeÉlémentDescripteur |
| 34 | positionnerFichier | entréeÉlémentDescripteur, valeurEncodage 있는 valeurDécalage, racineProjet |
| 35 | descripteurFichierDuplicata | entréeÉlémentDescripteur |
| 36 | àPositionDescripteurFichierDuplicata | entréeÉlémentDescripteur, 새 entréeÉlémentDescripteur |
| 37 | lireÉtatFichier | entréeÉlémentDescripteur, 48바이트 valeurÉtatValeur adresse |
| 38 | supprimerNomEntréeÉlémentFichier | NUL terminaison nom adresse |
| 39 | définirLongueurFichier | entréeÉlémentDescripteur, 새 longueur |
| 40 | descripteurFichierContrôle | entréeÉlémentDescripteur, commande, valeur |
| 41 | créerExtrémité | adresse valeurSystèmeExploitation, valeurGenre, valeurContrat numéro |
| 42 | associerAdresse | entréeÉlémentDescripteur, sockaddr_in adresse, longueur |
| 43 | envoyerDonnéesDatagramme | entréeÉlémentDescripteur, Données adresse, longueur, réglages, requête adresse |
| 44 | recevoirDonnéesDatagramme | entréeÉlémentDescripteur, Données adresse, longueur, réglages, requête adresse |
| 45 | lireAdressePriseRéseau | entréeÉlémentDescripteur, sockaddr adresse, socklen_t adresse |
| 46 | définirDélaiExpirationRecevoir | entréeÉlémentDescripteur, 0~2000 millisecondes |
| 47 | stockageFichierConfirmer | entréeÉlémentDescripteur |

43번 요청은 32비트 주소와 32비트 길이의 두 칸이다. 44번 요청은 32비트 주소와 길이를 담은 32비트 값의 adresse 두 칸이다. recevoirValeur 주소가 NULL이면 valeurPairRéseau adresse 기록을 생략한다. sockaddr_in은 16바이트이며 adresse 체계는 Périphérique valeurOctet valeurSéquence, 접속번호와 IP 주소는 네트워크 valeurOctet 차례다. 축소된 adresse 버퍼에도 들어가는 앞부분을 쓰고 전체 adresse taille 16을 반환한다.

0~22번의 기존 Java AOT 호출은 유지한다. 0은 programmeQuitter, 2·3은 기존 arguments 조회다. élémentListeActuel 커널의 arguments 목록이 exécuterCommande 이름을 제외하므로 C 진입기는 argv[0]에 고정 Chaîne `jkoros-app`을 넣고 valeurAprès 인수를 전달한다. argv 끝에는 NULL이 있다. 이 제한도 일반 UNIX valeurProcessus ABI와 다른 점이다.

표준 헤더의 Entier taille, valeurDrapeaux valeur, stat valeurChamp 순서는 `source/Entêtes/`에 정의한다. 동적 connecter·다중 valeurProcessus·스레드가 추가되면 erreur numéro 저장과 valeurRessource 수명, invoquer 경계도 함께 검토해야 한다.
