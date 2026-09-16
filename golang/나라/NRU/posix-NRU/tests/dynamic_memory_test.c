/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <system/child_wait.h>
#include <unistd.h>

static void write_message(const char *text, unsigned int digit_count)
{
    (void)write(standard_output_descriptor, text, digit_count);
}

int main(void)
{
    volatile unsigned char *starting_position = (volatile unsigned char *)sbrk(0);
    volatile unsigned char *memory_region;
    process_identifier_type child;
    int status;

    write_message("\nPOSIX-HEAP:START\n", 18);
    memory_region = (volatile unsigned char *)sbrk(32);
    if (starting_position == (void *)-1 || memory_region != starting_position || sbrk(0) != (void *)(starting_position + 32)) {
        write_message("PTEST:FAIL:sbrk-grow\n", 22);
        _exit(1);
    }
    write_message("PTEST:PASS:sbrk-grow\n", 22);
    memory_region[0] = 0x5a;
    memory_region[31] = 0xa5;
    if (memory_region[0] != 0x5a || memory_region[31] != 0xa5) {
        write_message("PTEST:FAIL:sbrk-memory\n", 24);
        _exit(1);
    }
    write_message("PTEST:PASS:sbrk-memory\n", 24);
    if (brk((void *)starting_position) != 0 || sbrk(0) != (void *)starting_position) {
        write_message("PTEST:FAIL:brk-restore\n", 24);
        _exit(1);
    }
    write_message("PTEST:PASS:brk-restore\n", 24);

    child = fork();
    if (child == 0) {
        if (sbrk(64) != (void *)starting_position)
            _exit(2);
        _exit(0);
    }
    if (child < 0 || waitpid(child, &status, 0) != child ||
        !exited_normally(status) || extract_exit_status(status) != 0 ||
        sbrk(0) != (void *)starting_position) {
        write_message("PTEST:FAIL:brk-process-isolation\n", 33);
        _exit(1);
    }
    write_message("PTEST:PASS:brk-process-isolation\n", 33);
    write_message("POSIX-HEAP:PASS\n", 16);
    _exit(0);
}
