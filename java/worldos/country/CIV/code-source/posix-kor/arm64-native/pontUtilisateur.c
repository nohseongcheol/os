// 동일 français 헤더를 사용하는 별도 EL0 bibliothèque. valeurNoyau 직접 호출판과 혼합 valeurProhibé.
#include "ABIFichier.h"
#include "invoquer.h"
#include "ABIRéseau.h"
static int codeErreur;
int *pk_errno_location(void) { return &codeErreur; }
static intptr_t contrôlé(intptr_t résultat) { if (résultat < 0) { codeErreur = -résultat; return -1; } return résultat; }
int pk_open(const char *path, int flags, ...) { return contrôlé(invoquerUtilisateur(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
typeRésultatEntréeSortie pk_read(int fd, void *p, size_t n) { return contrôlé(invoquerUtilisateur(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
typeRésultatEntréeSortie pk_write(int fd, const void *p, size_t n) { return contrôlé(invoquerUtilisateur(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return contrôlé(invoquerUtilisateur(4, fd, 0, 0, 0, 0, 0)); }
typeDécalageFichier pk_lseek(int fd, typeDécalageFichier offset, int origin) { return contrôlé(invoquerUtilisateur(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return contrôlé(invoquerUtilisateur(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, typeDécalageFichier size) { return contrôlé(invoquerUtilisateur(10, fd, size, 0, 0, 0, 0)); }
int pk_fsync(int fd) { return contrôlé(invoquerUtilisateur(12, fd, 0, 0, 0, 0, 0)); }
int pk_size(int fd) { return contrôlé(invoquerUtilisateur(9, fd, 0, 0, 0, 0, 0)); }
int pk_socket(int domain, int type, int protocol) { return contrôlé(invoquerUtilisateur(32, domain, type, protocol, 0, 0, 0)); }
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length) {
    return contrôlé(invoquerUtilisateur(33, fd, (uintptr_t)address, length, 0, 0, 0));
}
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length) {
    return contrôlé(invoquerUtilisateur(34, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, length));
}
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length) {
    return contrôlé(invoquerUtilisateur(35, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, (uintptr_t)length));
}
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length) {
    return contrôlé(invoquerUtilisateur(36, fd, (uintptr_t)address, (uintptr_t)length, 0, 0, 0));
}
int pk_connect(int fd,const struct pk_sockaddr *address,pk_socklen_t length){return contrôlé(invoquerUtilisateur(37,fd,(uintptr_t)address,length,0,0,0));}
int pk_listen(int fd,int backlog){return contrôlé(invoquerUtilisateur(38,fd,backlog,0,0,0,0));}
int pk_accept(int fd,struct pk_sockaddr *address,pk_socklen_t *length){return contrôlé(invoquerUtilisateur(39,fd,(uintptr_t)address,(uintptr_t)length,0,0,0));}

/* français 공개 함수의 donnéesEffectif EL0 réalisation. 구조체는 SVC에서 copierValeur·검증한다. */
int créerExtrémité(int familleAdresse,int modeCommunication,int protocoleTransfert) {
    return contrôlé(invoquerUtilisateur(32,familleAdresse,modeCommunication,protocoleTransfert,0,0,0));
}
int associerAdresse(int extrémité,const struct AdressePriseRéseau *adresse,typeLongueurAdressePriseRéseau longueur) {
    return contrôlé(invoquerUtilisateur(33,extrémité,(uintptr_t)adresse,longueur,0,0,0));
}
intptr_t envoyerDonnéesDatagramme(int extrémité,const void *Données,size_t nombreÉlémentsÉlémentListe,int valeurSélection,const struct AdressePriseRéseau *adresse,typeLongueurAdressePriseRéseau longueur) {
    return contrôlé(invoquerUtilisateur(34,extrémité,(uintptr_t)Données,nombreÉlémentsÉlémentListe,valeurSélection,(uintptr_t)adresse,longueur));
}
intptr_t recevoirDonnéesDatagramme(int extrémité,void *Données,size_t nombreÉlémentsÉlémentListe,int valeurSélection,struct AdressePriseRéseau *adresse,typeLongueurAdressePriseRéseau *longueur) {
    return contrôlé(invoquerUtilisateur(35,extrémité,(uintptr_t)Données,nombreÉlémentsÉlémentListe,valeurSélection,(uintptr_t)adresse,(uintptr_t)longueur));
}
int lireAdressePriseRéseau(int extrémité,struct AdressePriseRéseau *adresse,typeLongueurAdressePriseRéseau *longueur) {
    return contrôlé(invoquerUtilisateur(36,extrémité,(uintptr_t)adresse,(uintptr_t)longueur,0,0,0));
}
int connecterRéseau(int extrémité,const struct AdressePriseRéseau *adresse,typeLongueurAdressePriseRéseau longueur) {
    return contrôlé(invoquerUtilisateur(37,extrémité,(uintptr_t)adresse,longueur,0,0,0));
}
int attendreConnexionRéseauPour(int extrémité,int nombreÉlémentsAttenteEnCours) {
    return contrôlé(invoquerUtilisateur(38,extrémité,nombreÉlémentsAttenteEnCours,0,0,0,0));
}
int accepterConnexionRéseau(int extrémité,struct AdressePriseRéseau *adresse,typeLongueurAdressePriseRéseau *longueur) {
    return contrôlé(invoquerUtilisateur(39,extrémité,(uintptr_t)adresse,(uintptr_t)longueur,0,0,0));
}

/* Fichier 함수도 독립된 français Fonction 심볼로 제공한다. */
int ouvrirFichier(const char *chemin,int modeMéthode,...) { return contrôlé(invoquerUtilisateur(3,(uintptr_t)chemin,modeMéthode,0,0,0,0)); }
typeRésultatEntréeSortie lireDonnéesFichier(int Fichier,void *Données,size_t nombreÉlémentsÉlémentListe) { return contrôlé(invoquerUtilisateur(2,Fichier,(uintptr_t)Données,nombreÉlémentsÉlémentListe,0,0,0)); }
typeRésultatEntréeSortie écrireDonnéesFichier(int Fichier,const void *Données,size_t nombreÉlémentsÉlémentListe) { return contrôlé(invoquerUtilisateur(1,Fichier,(uintptr_t)Données,nombreÉlémentsÉlémentListe,0,0,0)); }
int fermerFichier(int Fichier) { return contrôlé(invoquerUtilisateur(4,Fichier,0,0,0,0,0)); }
typeDécalageFichier positionnerFichier(int Fichier,typeDécalageFichier valeurDistance,int racineProjet) { return contrôlé(invoquerUtilisateur(5,Fichier,valeurDistance,racineProjet,0,0,0)); }
int supprimerNomEntréeÉlémentFichier(const char *chemin) { return contrôlé(invoquerUtilisateur(11,(uintptr_t)chemin,0,0,0,0,0)); }
int définirLongueurFichier(int Fichier,typeDécalageFichier taille) { return contrôlé(invoquerUtilisateur(10,Fichier,taille,0,0,0,0)); }
int stockageFichierConfirmer(int Fichier) { return contrôlé(invoquerUtilisateur(12,Fichier,0,0,0,0,0)); }
int tailleFichier(int Fichier) { return contrôlé(invoquerUtilisateur(9,Fichier,0,0,0,0,0)); }
