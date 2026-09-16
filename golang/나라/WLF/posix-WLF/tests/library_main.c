/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char tampon_de_transfert_2[16];
        int longueur = 0;
        écrire(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { tampon_de_transfert_2[longueur++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (longueur) écrire(1, &tampon_de_transfert_2[--longueur], 1);
        écrire(1, "\n", 1);
        return 1;
    }
    return écrire(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
