#ifndef מקורי_קריפטוגרפיה_כותרת
#define מקורי_קריפטוגרפיה_כותרת
#include <stddef.h>
#include <stdint.h>
void *הקצה_מרוחק(size_t);
void לשחרר_מרוחק(void *);
void *원격재할당(void *, size_t);
int 원격난수(unsigned char *, unsigned);
void מרוחק_סיכום(const void *, size_t, unsigned char [32]);
#endif
