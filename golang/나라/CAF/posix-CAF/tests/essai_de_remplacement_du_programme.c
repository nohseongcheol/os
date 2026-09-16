/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <système/attente_des_enfants.h>
#include <unistd.h>

static void say(const char *text, unsigned int nombre_de_chiffres)
{
    (void)écrire(STDOUT_FILENO, text, nombre_de_chiffres);
}

int main(void)
{
    int état;
    int descripteur_de_fichier;
    char *arguments_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (attendre_un_enfant_désigné(-1, &état, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (attendre_un_enfant(&état) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    descripteur_de_fichier = ouvrir("/USER2", O_RDONLY);
    if (descripteur_de_fichier < 0 || dupliquer_la_référence_vers_un_numéro(descripteur_de_fichier, 10) != 10 || contrôler_le_fichier(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        terminer_immédiatement(98);
    }
    if (descripteur_de_fichier != 10)
        (void)fermer(descripteur_de_fichier);

    (void)remplacer_le_programme_exécuté("/PXEXEC", arguments_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    terminer_immédiatement(99);
}
