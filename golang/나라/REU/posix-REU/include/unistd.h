/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _LIBC_UNISTD_H
#define _LIBC_UNISTD_H

#include <définitions_de_base.h>
#include <système/types_de_données.h>

#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define F_OK 0
#define X_OK 1
#define W_OK 2
#define R_OK 4
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2

#ifdef __cplusplus
extern "C" {
#endif
extern char **environ;
void terminer_immédiatement(int état) __attribute__((noreturn));
ssize_t lire(int descripteur_de_fichier, void *tampon_de_transfert, size_t count);
ssize_t écrire(int descripteur_de_fichier, const void *tampon_de_transfert, size_t count);
int fermer(int descripteur_de_fichier);
off_t déplacer_la_position_de_fichier(int descripteur_de_fichier, off_t offset, int whence);
pid_t dédoubler_le_processus(void);
int remplacer_le_programme_exécuté(const char *chemin, char *const arguments_2[], char *const envp[]);
pid_t obtenir_identifiant_du_processus(void);
pid_t obtenir_identifiant_du_parent(void);
uid_t obtenir_identifiant_utilisateur(void);
uid_t obtenir_identifiant_utilisateur_effectif(void);
gid_t obtenir_identifiant_du_groupe(void);
gid_t obtenir_identifiant_du_groupe_effectif(void);
int vérifier_les_droits_accès(const char *chemin, int mode);
int changer_le_répertoire_courant(const char *chemin);
char *obtenir_le_chemin_du_répertoire_courant(char *tampon_de_transfert, size_t nombre_de_chiffres);
int dupliquer_la_référence_de_fichier_ouvert(int descripteur_de_fichier);
int dupliquer_la_référence_vers_un_numéro(int oldfd, int newfd);
int synchroniser_les_données_du_fichier(int descripteur_de_fichier);
void synchroniser_toutes_les_données(void);
int vérifier_si_terminal(int descripteur_de_fichier);
int fixer_la_fin_de_mémoire_dynamique(void *address);
void *déplacer_la_fin_de_mémoire_dynamique(int increment);
#ifdef __cplusplus
}
#endif

#endif
