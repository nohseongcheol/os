/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char स्थानांतरण_का_अस्थायी_भंडार_2[16];
        int लंबाई = 0;
        लिखना(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { स्थानांतरण_का_अस्थायी_भंडार_2[लंबाई++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (लंबाई) लिखना(1, &स्थानांतरण_का_अस्थायी_भंडार_2[--लंबाई], 1);
        लिखना(1, "\n", 1);
        return 1;
    }
    return लिखना(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
