#include <système/attente_des_enfants.h>
#include <fcntl.h>
#include <unistd.h>

static void say(const char *text, unsigned int nombre_de_chiffres)
{
    (void)écrire(STDOUT_FILENO, text, nombre_de_chiffres);
}

int main(void)
{
    int état;
    pid_t parent = obtenir_identifiant_du_processus();
    pid_t child;
    pid_t waited;
    volatile int private_value = 10;
    int descripteur_de_fichier;
    char byte;
    int iteration;

    say("\nPOSIX-FORK:START\n", 18);
    child = dédoubler_le_processus();
    if (child == 0) {
        private_value = 20;
        if (obtenir_identifiant_du_parent() != parent || private_value != 20)
            terminer_immédiatement(90);
        terminer_immédiatement(23);
    }
    if (child < 0) {
        say("PTEST:FAIL:fork-return\n", 23);
        terminer_immédiatement(1);
    }
    say("PTEST:PASS:fork-return\n", 23);
    waited = attendre_un_enfant_désigné(child, &état, 0);
    if (waited == child && WIFEXITED(état) && WEXITSTATUS(état) == 23 &&
        private_value == 10) {
        say("PTEST:PASS:fork-wait-exit\n", 26);
    } else {
        say("PTEST:FAIL:fork-wait-exit\n", 26);
        terminer_immédiatement(1);
    }

    child = dédoubler_le_processus();
    if (child == 0)
        terminer_immédiatement(29);
    waited = attendre_un_enfant(&état);
    if (waited == child && WIFEXITED(état) && WEXITSTATUS(état) == 29)
        say("PTEST:PASS:blocking-wait\n", 25);
    else {
        say("PTEST:FAIL:blocking-wait\n", 25);
        terminer_immédiatement(1);
    }

    descripteur_de_fichier = ouvrir("/USER2", O_RDONLY);
    child = dédoubler_le_processus();
    if (child == 0) {
        (void)fermer(descripteur_de_fichier);
        terminer_immédiatement(0);
    }
    waited = attendre_un_enfant_désigné(child, &état, 0);
    if (descripteur_de_fichier >= 0 && waited == child && lire(descripteur_de_fichier, &byte, 1) == 1 &&
        (unsigned char)byte == 0x7f)
        say("PTEST:PASS:fork-fd-isolation\n", 29);
    else {
        say("PTEST:FAIL:fork-fd-isolation\n", 29);
        terminer_immédiatement(1);
    }
    (void)fermer(descripteur_de_fichier);

    for (iteration = 0; iteration < 2; iteration++) {
        child = dédoubler_le_processus();
        if (child == 0)
            terminer_immédiatement(iteration);
        if (child < 0 || attendre_un_enfant_désigné(child, &état, 0) != child ||
            !WIFEXITED(état) || WEXITSTATUS(état) != iteration) {
            say("PTEST:FAIL:fork-stress\n", 23);
            terminer_immédiatement(1);
        }
    }
    say("PTEST:PASS:fork-stress\n", 23);
    say("POSIX-FORK:PASS\n", 16);
    terminer_immédiatement(0);
}
