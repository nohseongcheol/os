#include <errno.h>
#include <fcntl.h>
#include <System/Kindwartung.h>
#include <unistd.h>

static void say(const char *text, unsigned int Ziffernanzahl)
{
    (void)schreiben(STDOUT_FILENO, text, Ziffernanzahl);
}

int main(void)
{
    int Status;
    int Dateideskriptor;
    char *Argumente_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (bestimmtes_Kind_abwarten(-1, &Status, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (Kind_abwarten(&Status) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    Dateideskriptor = öffnen("/USER2", O_RDONLY);
    if (Dateideskriptor < 0 || Dateiverweis_auf_Kennung_duplizieren(Dateideskriptor, 10) != 10 || Dateizugriff_steuern(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        sofort_beenden(98);
    }
    if (Dateideskriptor != 10)
        (void)schließen(Dateideskriptor);

    (void)Programmbild_ersetzen("/PXEXEC", Argumente_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    sofort_beenden(99);
}
