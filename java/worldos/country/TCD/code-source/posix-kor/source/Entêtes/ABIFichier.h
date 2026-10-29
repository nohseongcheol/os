#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define ouvrirFichier open
#define créerFichier creat
#define lireDonnéesFichier read
#define écrireDonnéesFichier write
#define fermerFichier close
#define positionnerFichier lseek
#define descripteurFichierDuplicata dup
#define àPositionDescripteurFichierDuplicata dup2
#define supprimerNomEntréeÉlémentFichier unlink
#define définirLongueurFichier ftruncate
#define stockageFichierConfirmer fsync
#define lireÉtatFichier fstat
#define descripteurFichierContrôle fcntl
#define lireValeurSeulement O_RDONLY
#define écrireValeurSeulement O_WRONLY
#define ÉcrireLire O_RDWR
#define ManquantSiCréer O_CREAT
#define créerFichierNouveau (O_CREAT | O_EXCL)
#define ContenuTronquer O_TRUNC
#define ajouterFinFinÀPosition O_APPEND
#define attendrePasFaire O_NONBLOCK
#define DébutDepuis SEEK_SET
#define racineActuel SEEK_CUR
#define origineFin SEEK_END
#define étatFichier stat
typedef size_t typeNombreÉlémentsOctet;
typedef ssize_t typeRésultatEntréeSortie;
typedef off_t typeDécalageFichier;
#endif
