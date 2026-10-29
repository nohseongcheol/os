#include <அமைப்பு/சேய்_காத்திருப்பு.h>
#include <fcntl.h>
#include <unistd.h>

static void say(const char *text, unsigned int இலக்கங்களின்_எண்ணிக்கை)
{
    (void)எழுது(STDOUT_FILENO, text, இலக்கங்களின்_எண்ணிக்கை);
}

int main(void)
{
    int நிலை;
    pid_t parent = செயல்முறை_அடையாளத்தைப்_பெறு();
    pid_t child;
    pid_t waited;
    volatile int private_value = 10;
    int கோப்பு_விவரிப்பி;
    char byte;
    int iteration;

    say("\nPOSIX-FORK:START\n", 18);
    child = சேய்_செயல்முறையை_உருவாக்கு();
    if (child == 0) {
        private_value = 20;
        if (தாய்_செயல்முறை_அடையாளத்தைப்_பெறு() != parent || private_value != 20)
            உடனே_முடி(90);
        உடனே_முடி(23);
    }
    if (child < 0) {
        say("PTEST:FAIL:fork-return\n", 23);
        உடனே_முடி(1);
    }
    say("PTEST:PASS:fork-return\n", 23);
    waited = குறித்த_சேய்க்குக்_காத்திரு(child, &நிலை, 0);
    if (waited == child && WIFEXITED(நிலை) && WEXITSTATUS(நிலை) == 23 &&
        private_value == 10) {
        say("PTEST:PASS:fork-wait-exit\n", 26);
    } else {
        say("PTEST:FAIL:fork-wait-exit\n", 26);
        உடனே_முடி(1);
    }

    child = சேய்_செயல்முறையை_உருவாக்கு();
    if (child == 0)
        உடனே_முடி(29);
    waited = சேய்க்குக்_காத்திரு(&நிலை);
    if (waited == child && WIFEXITED(நிலை) && WEXITSTATUS(நிலை) == 29)
        say("PTEST:PASS:blocking-wait\n", 25);
    else {
        say("PTEST:FAIL:blocking-wait\n", 25);
        உடனே_முடி(1);
    }

    கோப்பு_விவரிப்பி = திற("/USER2", O_RDONLY);
    child = சேய்_செயல்முறையை_உருவாக்கு();
    if (child == 0) {
        (void)மூடு(கோப்பு_விவரிப்பி);
        உடனே_முடி(0);
    }
    waited = குறித்த_சேய்க்குக்_காத்திரு(child, &நிலை, 0);
    if (கோப்பு_விவரிப்பி >= 0 && waited == child && படி(கோப்பு_விவரிப்பி, &byte, 1) == 1 &&
        (unsigned char)byte == 0x7f)
        say("PTEST:PASS:fork-fd-isolation\n", 29);
    else {
        say("PTEST:FAIL:fork-fd-isolation\n", 29);
        உடனே_முடி(1);
    }
    (void)மூடு(கோப்பு_விவரிப்பி);

    for (iteration = 0; iteration < 2; iteration++) {
        child = சேய்_செயல்முறையை_உருவாக்கு();
        if (child == 0)
            உடனே_முடி(iteration);
        if (child < 0 || குறித்த_சேய்க்குக்_காத்திரு(child, &நிலை, 0) != child ||
            !WIFEXITED(நிலை) || WEXITSTATUS(நிலை) != iteration) {
            say("PTEST:FAIL:fork-stress\n", 23);
            உடனே_முடி(1);
        }
    }
    say("PTEST:PASS:fork-stress\n", 23);
    say("POSIX-FORK:PASS\n", 16);
    உடனே_முடி(0);
}
