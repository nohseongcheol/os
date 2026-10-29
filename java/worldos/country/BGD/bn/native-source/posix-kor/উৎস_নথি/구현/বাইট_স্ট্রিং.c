#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *স্ট্রিং_মান) { size_t দৈর্ঘ্য_মান = 0; while (স্ট্রিং_মান[দৈর্ঘ্য_মান]) দৈর্ঘ্য_মান++; return দৈর্ঘ্য_মান; }
int strcmp(const char *সম্মুখ_মান, const char *ফিরে_যান_মান) {
    while (*সম্মুখ_মান && *সম্মুখ_মান == *ফিরে_যান_মান) { সম্মুখ_মান++; ফিরে_যান_মান++; }
    return (unsigned char)*সম্মুখ_মান - (unsigned char)*ফিরে_যান_মান;
}
int memcmp(const void *সম্মুখ_মান, const void *ফিরে_যান_মান, size_t 바이트수) {
    const unsigned char *가 = সম্মুখ_মান, *나 = ফিরে_যান_মান;
    for (size_t স্লট_ভুক্তি = 0; স্লট_ভুক্তি < 바이트수; স্লট_ভুক্তি++) if (가[স্লট_ভুক্তি] != 나[স্লট_ভুক্তি]) return 가[স্লট_ভুক্তি] - 나[স্লট_ভুক্তি];
    return 0;
}
void *memcpy(void *গন্তব্য_মান, const void *원본, size_t 바이트수) {
    unsigned char *가 = গন্তব্য_মান; const unsigned char *나 = 원본;
    for (size_t স্লট_ভুক্তি = 0; স্লট_ভুক্তি < 바이트수; স্লট_ভুক্তি++) 가[স্লট_ভুক্তি] = 나[স্লট_ভুক্তি];
    return গন্তব্য_মান;
}
void *memset(void *গন্তব্য_মান, int মান, size_t 바이트수) {
    unsigned char *ডাটা = গন্তব্য_মান;
    for (size_t স্লট_ভুক্তি = 0; স্লট_ভুক্তি < 바이트수; স্লট_ভুক্তি++) ডাটা[স্লট_ভুক্তি] = মান;
    return গন্তব্য_মান;
}
int putchar(int 문자) { unsigned char মান = 문자; return write(1, &মান, 1) == 1 ? মান : EOF; }
int puts(const char *স্ট্রিং_মান) {
    size_t দৈর্ঘ্য_মান = strlen(স্ট্রিং_মান), অবস্থান = 0;
    while (অবস্থান < দৈর্ঘ্য_মান) { ssize_t পরিমাপ = write(1, স্ট্রিং_মান + অবস্থান, দৈর্ঘ্য_মান - অবস্থান); if (পরিমাপ <= 0) return EOF; অবস্থান += পরিমাপ; }
    return putchar('\n') == EOF ? EOF : 0;
}
