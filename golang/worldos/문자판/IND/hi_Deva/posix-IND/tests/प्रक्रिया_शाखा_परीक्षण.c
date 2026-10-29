#include <प्रणाली/संतान_प्रतीक्षा.h>
#include <fcntl.h>
#include <unistd.h>

static void say(const char *text, unsigned int अंकों_की_संख्या)
{
    (void)लिखना(STDOUT_FILENO, text, अंकों_की_संख्या);
}

int main(void)
{
    int स्थिति;
    pid_t parent = प्रक्रिया_पहचान_पाना();
    pid_t child;
    pid_t waited;
    volatile int private_value = 10;
    int संचिका_विवरणक;
    char byte;
    int iteration;

    say("\nPOSIX-FORK:START\n", 18);
    child = संतान_प्रक्रिया_बनाना();
    if (child == 0) {
        private_value = 20;
        if (जनक_प्रक्रिया_पहचान_पाना() != parent || private_value != 20)
            तुरंत_समाप्त_करना(90);
        तुरंत_समाप्त_करना(23);
    }
    if (child < 0) {
        say("PTEST:FAIL:fork-return\n", 23);
        तुरंत_समाप्त_करना(1);
    }
    say("PTEST:PASS:fork-return\n", 23);
    waited = नियत_संतान_की_प्रतीक्षा_करना(child, &स्थिति, 0);
    if (waited == child && WIFEXITED(स्थिति) && WEXITSTATUS(स्थिति) == 23 &&
        private_value == 10) {
        say("PTEST:PASS:fork-wait-exit\n", 26);
    } else {
        say("PTEST:FAIL:fork-wait-exit\n", 26);
        तुरंत_समाप्त_करना(1);
    }

    child = संतान_प्रक्रिया_बनाना();
    if (child == 0)
        तुरंत_समाप्त_करना(29);
    waited = संतान_की_प्रतीक्षा_करना(&स्थिति);
    if (waited == child && WIFEXITED(स्थिति) && WEXITSTATUS(स्थिति) == 29)
        say("PTEST:PASS:blocking-wait\n", 25);
    else {
        say("PTEST:FAIL:blocking-wait\n", 25);
        तुरंत_समाप्त_करना(1);
    }

    संचिका_विवरणक = खोलना("/USER2", O_RDONLY);
    child = संतान_प्रक्रिया_बनाना();
    if (child == 0) {
        (void)बंद_करना(संचिका_विवरणक);
        तुरंत_समाप्त_करना(0);
    }
    waited = नियत_संतान_की_प्रतीक्षा_करना(child, &स्थिति, 0);
    if (संचिका_विवरणक >= 0 && waited == child && पढ़ना(संचिका_विवरणक, &byte, 1) == 1 &&
        (unsigned char)byte == 0x7f)
        say("PTEST:PASS:fork-fd-isolation\n", 29);
    else {
        say("PTEST:FAIL:fork-fd-isolation\n", 29);
        तुरंत_समाप्त_करना(1);
    }
    (void)बंद_करना(संचिका_विवरणक);

    for (iteration = 0; iteration < 2; iteration++) {
        child = संतान_प्रक्रिया_बनाना();
        if (child == 0)
            तुरंत_समाप्त_करना(iteration);
        if (child < 0 || नियत_संतान_की_प्रतीक्षा_करना(child, &स्थिति, 0) != child ||
            !WIFEXITED(स्थिति) || WEXITSTATUS(स्थिति) != iteration) {
            say("PTEST:FAIL:fork-stress\n", 23);
            तुरंत_समाप्त_करना(1);
        }
    }
    say("PTEST:PASS:fork-stress\n", 23);
    say("POSIX-FORK:PASS\n", 16);
    तुरंत_समाप्त_करना(0);
}
