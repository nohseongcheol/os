#ifndef εγγενής_κρυπτογράφηση_κεφαλίδα
#define εγγενής_κρυπτογράφηση_κεφαλίδα
#include <stddef.h>
#include <stdint.h>
void *εκχωρώ_απομακρυσμένος(size_t);
void έκδοση_απομακρυσμένος(void *);
void *원격재할당(void *, size_t);
int απομακρυσμένος_τυχαίος(unsigned char *, unsigned);
void απομακρυσμένος_σύνοψη(const void *, size_t, unsigned char [32]);
#endif
