#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char স্থানান্তরের_অস্থায়ী_ভান্ডার_2[16];
        int দৈর্ঘ্য = 0;
        লেখা(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { স্থানান্তরের_অস্থায়ী_ভান্ডার_2[দৈর্ঘ্য++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (দৈর্ঘ্য) লেখা(1, &স্থানান্তরের_অস্থায়ী_ভান্ডার_2[--দৈর্ঘ্য], 1);
        লেখা(1, "\n", 1);
        return 1;
    }
    return লেখা(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
