/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char memória_intermédia_de_transferência_2[16];
        int comprimento = 0;
        escrever(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { memória_intermédia_de_transferência_2[comprimento++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (comprimento) escrever(1, &memória_intermédia_de_transferência_2[--comprimento], 1);
        escrever(1, "\n", 1);
        return 1;
    }
    return escrever(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
