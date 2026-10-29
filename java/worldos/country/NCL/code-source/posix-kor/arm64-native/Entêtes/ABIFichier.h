#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t typeRésultatEntréeSortie;
typedef size_t typeNombreÉlémentsOctet;
typedef int64_t typeDécalageFichier;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
typeRésultatEntréeSortie pk_read(int fd, void *buffer, size_t count);
typeRésultatEntréeSortie pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
typeDécalageFichier pk_lseek(int fd, typeDécalageFichier offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, typeDécalageFichier size);
int pk_fsync(int fd);
int pk_size(int fd);
int ouvrirFichier(const char *chemin, int modeMéthode, ...);
typeRésultatEntréeSortie lireDonnéesFichier(int Fichier, void *Données, size_t nombreÉlémentsÉlémentListe);
typeRésultatEntréeSortie écrireDonnéesFichier(int Fichier, const void *Données, size_t nombreÉlémentsÉlémentListe);
int fermerFichier(int Fichier);
typeDécalageFichier positionnerFichier(int Fichier, typeDécalageFichier valeurDistance, int racineProjet);
int supprimerNomEntréeÉlémentFichier(const char *chemin);
int définirLongueurFichier(int Fichier, typeDécalageFichier taille);
int stockageFichierConfirmer(int Fichier);
int tailleFichier(int Fichier);
#ifdef __cplusplus
}
#endif
#define numéroErreur (*pk_errno_location())
#define lireValeurSeulement 0
#define écrireValeurSeulement 1
#define ÉcrireLire 2
#define ManquantSiCréer 0x40
#define créerFichierNouveau 0xc0
#define ContenuTronquer 0x200
#define ajouterFinFinÀPosition 0x400
#define DébutDepuis 0
#define racineActuel 1
#define origineFin 2
#endif
