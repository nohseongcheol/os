#ifndef yerel_şifreleme_Başlık
#define yerel_şifreleme_Başlık
#include <stddef.h>
#include <stdint.h>
void *ayırmak_uzak(size_t);
void sürüm_uzak(void *);
void *원격재할당(void *, size_t);
int uzak_rastgele(unsigned char *, unsigned);
void uzak_özet(const void *, size_t, unsigned char [32]);
#endif
