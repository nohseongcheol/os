#include <ABIFichier.h>
#include "FrontièreAppel.h"

int numéroErreur;
int résultatInvocation(int résultat) {
    if (résultat < 0) { numéroErreur = -résultat; return -1; }
    return résultat;
}
int open(const char *nomEntréeÉlémentFichier, int ouvrirRéglages, ...) {
    mode_t accorderPermission = 0;
    if (ouvrirRéglages & O_CREAT) {
        __builtin_va_list arguments;
        __builtin_va_start(arguments, ouvrirRéglages);
        accorderPermission = __builtin_va_arg(arguments, mode_t);
        __builtin_va_end(arguments);
    }
    return résultatInvocation(jkoros_syscall(30, (int)nomEntréeÉlémentFichier, ouvrirRéglages, accorderPermission, 0, 0));
}
int creat(const char *nomEntréeÉlémentFichier, mode_t accorderPermission) { return open(nomEntréeÉlémentFichier, O_WRONLY | O_CREAT | O_TRUNC, accorderPermission); }
ssize_t read(int descripteurFichier, void *Données, size_t nombreÉlémentsOctet) {
    return résultatInvocation(jkoros_syscall(31, descripteurFichier, (int)Données, nombreÉlémentsOctet, 0, 0));
}
ssize_t write(int descripteurFichier, const void *Données, size_t nombreÉlémentsOctet) {
    return résultatInvocation(jkoros_syscall(32, descripteurFichier, (int)Données, nombreÉlémentsOctet, 0, 0));
}
int close(int descripteurFichier) { return résultatInvocation(jkoros_syscall(33, descripteurFichier, 0, 0, 0, 0)); }
off_t lseek(int descripteurFichier, off_t valeurDécalage, int racineProjet) {
    return résultatInvocation(jkoros_syscall(34, descripteurFichier, valeurDécalage, racineProjet, 0, 0));
}
int dup(int descripteurFichier) { return résultatInvocation(jkoros_syscall(35, descripteurFichier, 0, 0, 0, 0)); }
int dup2(int descripteurFichier, int descripteurNouveau) { return résultatInvocation(jkoros_syscall(36, descripteurFichier, descripteurNouveau, 0, 0, 0)); }
int fstat(int descripteurFichier, struct stat *valeurÉtatValeur) { return résultatInvocation(jkoros_syscall(37, descripteurFichier, (int)valeurÉtatValeur, 0, 0, 0)); }
int unlink(const char *nomEntréeÉlémentFichier) { return résultatInvocation(jkoros_syscall(38, (int)nomEntréeÉlémentFichier, 0, 0, 0, 0)); }
int ftruncate(int descripteurFichier, off_t nombreÉlémentsOctet) { return résultatInvocation(jkoros_syscall(39, descripteurFichier, nombreÉlémentsOctet, 0, 0, 0)); }
int fsync(int descripteurFichier) { return résultatInvocation(jkoros_syscall(47, descripteurFichier, 0, 0, 0, 0)); }
int fcntl(int descripteurFichier, int commande, ...) {
    int valeur = 0;
    if (commande == F_DUPFD || commande == F_DUPFD_CLOEXEC || commande == F_SETFD || commande == F_SETFL) {
        __builtin_va_list arguments;
        __builtin_va_start(arguments, commande); valeur = __builtin_va_arg(arguments, int); __builtin_va_end(arguments);
    }
    return résultatInvocation(jkoros_syscall(40, descripteurFichier, commande, valeur, 0, 0));
}
