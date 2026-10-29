#ifndef εγγενής_απομακρυσμένη_σύνδεση_κεφαλίδα
#define εγγενής_απομακρυσμένη_σύνδεση_κεφαλίδα
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Προετοίμασε_απομακρυσμένος(void);
void 원격살피기(void);
void 원격출력(unsigned char);
int απομακρυσμένος_είσοδος(void);
int τροφοδοσία_απομακρυσμένος_είσοδος(const unsigned char *,unsigned);
uintptr_t Πίνακας_απομακρυσμένος_έλεγχος(uintptr_t,uintptr_t);
uintptr_t Πίνακας_Τελική_οντότητα_απομακρυσμένος_εντολή(uintptr_t);
uintptr_t Πίνακας_απομακρυσμένος_περίμενε(uintptr_t);
void 원격화면살피기(void);
int έλεγχος_απομακρυσμένος_οθόνη(unsigned);
#endif
