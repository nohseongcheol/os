#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *ষ্ট্ৰিং_মান) { size_t দৈর্ঘ্য_মান = 0; while (ষ্ট্ৰিং_মান[দৈর্ঘ্য_মান]) দৈর্ঘ্য_মান++; return দৈর্ঘ্য_মান; }
int strcmp(const char *앞, const char *পাছলৈ_মান) {
    while (*앞 && *앞 == *পাছলৈ_মান) { 앞++; পাছলৈ_মান++; }
    return (unsigned char)*앞 - (unsigned char)*পাছলৈ_মান;
}
int memcmp(const void *앞, const void *পাছলৈ_মান, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = পাছলৈ_মান;
    for (size_t শ্লট_প্রবিষ্ট = 0; শ্লট_প্রবিষ্ট < 바이트수; শ্লট_প্রবিষ্ট++) if (가[শ্লট_প্রবিষ্ট] != 나[শ্লট_প্রবিষ্ট]) return 가[শ্লট_প্রবিষ্ট] - 나[শ্লট_প্রবিষ্ট];
    return 0;
}
void *memcpy(void *গন্তব্য_স্থান_মান, const void *원본, size_t 바이트수) {
    unsigned char *가 = গন্তব্য_স্থান_মান; const unsigned char *나 = 원본;
    for (size_t শ্লট_প্রবিষ্ট = 0; শ্লট_প্রবিষ্ট < 바이트수; শ্লট_প্রবিষ্ট++) 가[শ্লট_প্রবিষ্ট] = 나[শ্লট_প্রবিষ্ট];
    return গন্তব্য_স্থান_মান;
}
void *memset(void *গন্তব্য_স্থান_মান, int মান, size_t 바이트수) {
    unsigned char *ডাটা = গন্তব্য_স্থান_মান;
    for (size_t শ্লট_প্রবিষ্ট = 0; শ্লট_প্রবিষ্ট < 바이트수; শ্লট_প্রবিষ্ট++) ডাটা[শ্লট_প্রবিষ্ট] = মান;
    return গন্তব্য_স্থান_মান;
}
int putchar(int 문자) { unsigned char মান = 문자; return write(1, &মান, 1) == 1 ? মান : EOF; }
int puts(const char *ষ্ট্ৰিং_মান) {
    size_t দৈর্ঘ্য_মান = strlen(ষ্ট্ৰিং_মান), অৱস্থান = 0;
    while (অৱস্থান < দৈর্ঘ্য_মান) { ssize_t পৰিমাপ = write(1, ষ্ট্ৰিং_মান + অৱস্থান, দৈর্ঘ্য_মান - অৱস্থান); if (পৰিমাপ <= 0) return EOF; অৱস্থান += পৰিমাপ; }
    return putchar('\n') == EOF ? EOF : 0;
}
