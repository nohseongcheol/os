/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <système/stat.h>
int __posix_library_test(void);

int main(void)
{
    char tampon_de_transfert_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int descripteur_de_fichier = ouvrir("/USER2", O_RDONLY);
    struct état_du_fichier st;
    if (descripteur_de_fichier < 0 || obtenir_état_du_fichier_ouvert(descripteur_de_fichier, &st) < 0 || lire(descripteur_de_fichier, tampon_de_transfert_2, 4) != 4 ||
        (unsigned char)tampon_de_transfert_2[0] != 0x7f || tampon_de_transfert_2[1] != 'E' || tampon_de_transfert_2[2] != 'L' || tampon_de_transfert_2[3] != 'F' ||
        déplacer_la_position_de_fichier(descripteur_de_fichier, 0, SEEK_SET) != 0 || fermer(descripteur_de_fichier) < 0 || obtenir_identifiant_du_processus() <= 0)
        goto failure;
    errno = 0;
    if (lire(-1, tampon_de_transfert_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (écrire(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    écrire(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
