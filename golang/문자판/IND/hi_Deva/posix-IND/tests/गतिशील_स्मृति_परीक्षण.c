/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <प्रणाली/संतान_प्रतीक्षा.h>
#include <unistd.h>

static void say(const char *text, unsigned int अंकों_की_संख्या)
{
    (void)लिखना(STDOUT_FILENO, text, अंकों_की_संख्या);
}

int main(void)
{
    volatile unsigned char *start = (volatile unsigned char *)गतिशील_स्मृति_अंत_बदलना(0);
    volatile unsigned char *memory;
    pid_t child;
    int स्थिति;

    say("\nPOSIX-HEAP:START\n", 18);
    memory = (volatile unsigned char *)गतिशील_स्मृति_अंत_बदलना(32);
    if (start == (void *)-1 || memory != start || गतिशील_स्मृति_अंत_बदलना(0) != (void *)(start + 32)) {
        say("PTEST:FAIL:sbrk-grow\n", 22);
        तुरंत_समाप्त_करना(1);
    }
    say("PTEST:PASS:sbrk-grow\n", 22);
    memory[0] = 0x5a;
    memory[31] = 0xa5;
    if (memory[0] != 0x5a || memory[31] != 0xa5) {
        say("PTEST:FAIL:sbrk-memory\n", 24);
        तुरंत_समाप्त_करना(1);
    }
    say("PTEST:PASS:sbrk-memory\n", 24);
    if (गतिशील_स्मृति_अंत_निर्धारित_करना((void *)start) != 0 || गतिशील_स्मृति_अंत_बदलना(0) != (void *)start) {
        say("PTEST:FAIL:brk-restore\n", 24);
        तुरंत_समाप्त_करना(1);
    }
    say("PTEST:PASS:brk-restore\n", 24);

    child = संतान_प्रक्रिया_बनाना();
    if (child == 0) {
        if (गतिशील_स्मृति_अंत_बदलना(64) != (void *)start)
            तुरंत_समाप्त_करना(2);
        तुरंत_समाप्त_करना(0);
    }
    if (child < 0 || नियत_संतान_की_प्रतीक्षा_करना(child, &स्थिति, 0) != child ||
        !WIFEXITED(स्थिति) || WEXITSTATUS(स्थिति) != 0 ||
        गतिशील_स्मृति_अंत_बदलना(0) != (void *)start) {
        say("PTEST:FAIL:brk-process-isolation\n", 33);
        तुरंत_समाप्त_करना(1);
    }
    say("PTEST:PASS:brk-process-isolation\n", 33);
    say("POSIX-HEAP:PASS\n", 16);
    तुरंत_समाप्त_करना(0);
}
