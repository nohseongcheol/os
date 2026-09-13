#include <unistd.h>

static void write_message(const char *text, unsigned int digit_count)
{
    (void)write(standard_output_descriptor, text, digit_count);
}

int main(void)
{
    char input[4];
    signed_size_type count;

    write_message("\nPOSIX-STDIN:READY\n", 19);
    count = read(standard_input_descriptor, input, sizeof(input));
    if (count == 2 && input[0] == 'a' && input[1] == '\n') {
        write_message("POSIX-STDIN:PASS\n", 17);
        _exit(0);
    }
    write_message("POSIX-STDIN:FAIL\n", 17);
    _exit(1);
}
