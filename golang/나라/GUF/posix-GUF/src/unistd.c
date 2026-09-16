/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <système/stat.h>
#include <système/attente_des_enfants.h>
#include <unistd.h>
#include <système/syscall.h>

enum {
    SYS_terminer_immédiatement = 1,
    SYS_dédoubler_le_processus = 2,
    SYS_lire = 3,
    SYS_écrire = 4,
    SYS_fermer = 6,
    SYS_remplacer_le_programme_exécuté = 11,
    SYS_changer_le_répertoire_courant = 12,
    SYS_déplacer_la_position_de_fichier = 19,
    SYS_obtenir_identifiant_du_processus = 20,
    SYS_obtenir_identifiant_utilisateur = 24,
    SYS_vérifier_les_droits_accès = 33,
    SYS_synchroniser_toutes_les_données = 36,
    SYS_dupliquer_la_référence_de_fichier_ouvert = 41,
    SYS_fixer_la_fin_de_mémoire_dynamique = 45,
    SYS_obtenir_identifiant_du_groupe = 47,
    SYS_obtenir_identifiant_utilisateur_effectif = 49,
    SYS_obtenir_identifiant_du_groupe_effectif = 50,
    SYS_dupliquer_la_référence_vers_un_numéro = 63,
    SYS_obtenir_identifiant_du_parent = 64,
    SYS_synchroniser_les_données_du_fichier = 118,
    SYS_obtenir_le_chemin_du_répertoire_courant = 183
};

#define SC0(n) __syscall6((n), 0, 0, 0, 0, 0, 0)
#define SC1(n,a) __syscall6((n), (long)(a), 0, 0, 0, 0, 0)
#define SC2(n,a,b) __syscall6((n), (long)(a), (long)(b), 0, 0, 0, 0)
#define SC3(n,a,b,c) __syscall6((n), (long)(a), (long)(b), (long)(c), 0, 0, 0)

void terminer_immédiatement(int état)
{
    SC1(SYS_terminer_immédiatement, état);
    for (;;) {
        __asm__ __volatile__("hlt");
    }
}

ssize_t lire(int descripteur_de_fichier, void *tampon_de_transfert, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_lire, descripteur_de_fichier, tampon_de_transfert, count));
}

ssize_t écrire(int descripteur_de_fichier, const void *tampon_de_transfert, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_écrire, descripteur_de_fichier, tampon_de_transfert, count));
}

int fermer(int descripteur_de_fichier)
{
    return (int)__syscall_result(SC1(SYS_fermer, descripteur_de_fichier));
}

off_t déplacer_la_position_de_fichier(int descripteur_de_fichier, off_t offset, int whence)
{
    return (off_t)__syscall_result(SC3(SYS_déplacer_la_position_de_fichier, descripteur_de_fichier, offset, whence));
}

pid_t dédoubler_le_processus(void)
{
    return (pid_t)__syscall_result(SC0(SYS_dédoubler_le_processus));
}

int remplacer_le_programme_exécuté(const char *chemin, char *const arguments_2[], char *const envp[])
{
    return (int)__syscall_result(SC3(SYS_remplacer_le_programme_exécuté, chemin, arguments_2, envp));
}

pid_t obtenir_identifiant_du_processus(void) { return (pid_t)SC0(SYS_obtenir_identifiant_du_processus); }
pid_t obtenir_identifiant_du_parent(void) { return (pid_t)SC0(SYS_obtenir_identifiant_du_parent); }
uid_t obtenir_identifiant_utilisateur(void) { return (uid_t)SC0(SYS_obtenir_identifiant_utilisateur); }
uid_t obtenir_identifiant_utilisateur_effectif(void) { return (uid_t)SC0(SYS_obtenir_identifiant_utilisateur_effectif); }
gid_t obtenir_identifiant_du_groupe(void) { return (gid_t)SC0(SYS_obtenir_identifiant_du_groupe); }
gid_t obtenir_identifiant_du_groupe_effectif(void) { return (gid_t)SC0(SYS_obtenir_identifiant_du_groupe_effectif); }

int vérifier_les_droits_accès(const char *chemin, int mode)
{
    return (int)__syscall_result(SC2(SYS_vérifier_les_droits_accès, chemin, mode));
}

int changer_le_répertoire_courant(const char *chemin)
{
    return (int)__syscall_result(SC1(SYS_changer_le_répertoire_courant, chemin));
}

char *obtenir_le_chemin_du_répertoire_courant(char *tampon_de_transfert, size_t nombre_de_chiffres)
{
    long result = __syscall_result(SC2(SYS_obtenir_le_chemin_du_répertoire_courant, tampon_de_transfert, nombre_de_chiffres));
    return result < 0 ? (char *)0 : tampon_de_transfert;
}

int dupliquer_la_référence_de_fichier_ouvert(int descripteur_de_fichier)
{
    return (int)__syscall_result(SC1(SYS_dupliquer_la_référence_de_fichier_ouvert, descripteur_de_fichier));
}

int dupliquer_la_référence_vers_un_numéro(int oldfd, int newfd)
{
    return (int)__syscall_result(SC2(SYS_dupliquer_la_référence_vers_un_numéro, oldfd, newfd));
}

int synchroniser_les_données_du_fichier(int descripteur_de_fichier)
{
    return (int)__syscall_result(SC1(SYS_synchroniser_les_données_du_fichier, descripteur_de_fichier));
}

void synchroniser_toutes_les_données(void)
{
    SC0(SYS_synchroniser_toutes_les_données);
}

int vérifier_si_terminal(int descripteur_de_fichier)
{
    struct état_du_fichier st;
    if (obtenir_état_du_fichier_ouvert(descripteur_de_fichier, &st) < 0)
        return 0;
    if (!S_ISCHR(st.st_mode)) {
        errno = ENOTTY;
        return 0;
    }
    return 1;
}

int fixer_la_fin_de_mémoire_dynamique(void *address)
{
    long result = SC1(SYS_fixer_la_fin_de_mémoire_dynamique, address);
    if (result != (long)address) {
        errno = ENOMEM;
        return -1;
    }
    return 0;
}

void *déplacer_la_fin_de_mémoire_dynamique(int increment)
{
    long current = SC1(SYS_fixer_la_fin_de_mémoire_dynamique, 0);
    long requested = current + increment;
    if (increment != 0 && fixer_la_fin_de_mémoire_dynamique((void *)requested) < 0)
        return (void *)-1;
    return (void *)current;
}

pid_t attendre_un_enfant_désigné(pid_t pid, int *état, int options)
{
    long result;
    do {
        result = SC3(7, pid, état, options);
    } while (result == -EAGAIN && (options & WNOHANG) == 0);
    return (pid_t)__syscall_result(result);
}

pid_t attendre_un_enfant(int *état)
{
    return attendre_un_enfant_désigné(-1, état, 0);
}
