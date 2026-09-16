/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <système/stat.h>
#include <système/identité_du_système.h>
#include <système/syscall.h>

enum { SYS_état_du_fichier = 106, SYS_obtenir_état_du_lien_même = 107, SYS_obtenir_état_du_fichier_ouvert = 108, SYS_obtenir_informations_du_système = 122 };

int état_du_fichier(const char *chemin, struct état_du_fichier *tampon_de_transfert)
{
    return (int)__syscall_result(
        __syscall6(SYS_état_du_fichier, (long)chemin, (long)tampon_de_transfert, 0, 0, 0, 0));
}

int obtenir_état_du_lien_même(const char *chemin, struct état_du_fichier *tampon_de_transfert)
{
    return (int)__syscall_result(
        __syscall6(SYS_obtenir_état_du_lien_même, (long)chemin, (long)tampon_de_transfert, 0, 0, 0, 0));
}

int obtenir_état_du_fichier_ouvert(int descripteur_de_fichier, struct état_du_fichier *tampon_de_transfert)
{
    return (int)__syscall_result(
        __syscall6(SYS_obtenir_état_du_fichier_ouvert, descripteur_de_fichier, (long)tampon_de_transfert, 0, 0, 0, 0));
}

int obtenir_informations_du_système(struct utsname *identité_du_système)
{
    return (int)__syscall_result(
        __syscall6(SYS_obtenir_informations_du_système, (long)identité_du_système, 0, 0, 0, 0, 0));
}
