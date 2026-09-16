/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <System/Kindwartung.h>
#include <fcntl.h>
#include <unistd.h>

static void say(const char *text, unsigned int Ziffernanzahl)
{
    (void)schreiben(STDOUT_FILENO, text, Ziffernanzahl);
}

int main(void)
{
    int Status;
    pid_t parent = Prozesskennung_ermitteln();
    pid_t child;
    pid_t waited;
    volatile int private_value = 10;
    int Dateideskriptor;
    char byte;
    int iteration;

    say("\nPOSIX-FORK:START\n", 18);
    child = Prozess_verzweigen();
    if (child == 0) {
        private_value = 20;
        if (Elternprozesskennung_ermitteln() != parent || private_value != 20)
            sofort_beenden(90);
        sofort_beenden(23);
    }
    if (child < 0) {
        say("PTEST:FAIL:fork-return\n", 23);
        sofort_beenden(1);
    }
    say("PTEST:PASS:fork-return\n", 23);
    waited = bestimmtes_Kind_abwarten(child, &Status, 0);
    if (waited == child && WIFEXITED(Status) && WEXITSTATUS(Status) == 23 &&
        private_value == 10) {
        say("PTEST:PASS:fork-wait-exit\n", 26);
    } else {
        say("PTEST:FAIL:fork-wait-exit\n", 26);
        sofort_beenden(1);
    }

    child = Prozess_verzweigen();
    if (child == 0)
        sofort_beenden(29);
    waited = Kind_abwarten(&Status);
    if (waited == child && WIFEXITED(Status) && WEXITSTATUS(Status) == 29)
        say("PTEST:PASS:blocking-wait\n", 25);
    else {
        say("PTEST:FAIL:blocking-wait\n", 25);
        sofort_beenden(1);
    }

    Dateideskriptor = öffnen("/USER2", O_RDONLY);
    child = Prozess_verzweigen();
    if (child == 0) {
        (void)schließen(Dateideskriptor);
        sofort_beenden(0);
    }
    waited = bestimmtes_Kind_abwarten(child, &Status, 0);
    if (Dateideskriptor >= 0 && waited == child && lesen(Dateideskriptor, &byte, 1) == 1 &&
        (unsigned char)byte == 0x7f)
        say("PTEST:PASS:fork-fd-isolation\n", 29);
    else {
        say("PTEST:FAIL:fork-fd-isolation\n", 29);
        sofort_beenden(1);
    }
    (void)schließen(Dateideskriptor);

    for (iteration = 0; iteration < 2; iteration++) {
        child = Prozess_verzweigen();
        if (child == 0)
            sofort_beenden(iteration);
        if (child < 0 || bestimmtes_Kind_abwarten(child, &Status, 0) != child ||
            !WIFEXITED(Status) || WEXITSTATUS(Status) != iteration) {
            say("PTEST:FAIL:fork-stress\n", 23);
            sofort_beenden(1);
        }
    }
    say("PTEST:PASS:fork-stress\n", 23);
    say("POSIX-FORK:PASS\n", 16);
    sofort_beenden(0);
}
