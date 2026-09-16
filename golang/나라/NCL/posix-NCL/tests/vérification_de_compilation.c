/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <système/stat.h>
#include <système/identité_du_système.h>
#include <système/attente_des_enfants.h>
#include <unistd.h>

int posix_compile_test(void)
{
    char cwd[8];
    struct état_du_fichier st;
    struct utsname identité_du_système;
    int descripteur_de_fichier = ouvrir("/USER1", O_RDONLY);
    int copy = descripteur_de_fichier >= 0 ? dupliquer_la_référence_de_fichier_ouvert(descripteur_de_fichier) : -1;
    if (copy >= 0) fermer(copy);
    if (descripteur_de_fichier >= 0) {
        obtenir_état_du_fichier_ouvert(descripteur_de_fichier, &st);
        déplacer_la_position_de_fichier(descripteur_de_fichier, 0, SEEK_SET);
        fermer(descripteur_de_fichier);
    }
    état_du_fichier("/", &st);
    obtenir_informations_du_système(&identité_du_système);
    obtenir_le_chemin_du_répertoire_courant(cwd, sizeof(cwd));
    return errno + obtenir_identifiant_du_processus() + obtenir_identifiant_du_parent();
}
