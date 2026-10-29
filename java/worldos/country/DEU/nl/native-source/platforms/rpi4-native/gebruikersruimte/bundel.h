#ifndef systeemeigen_bundel_header
#define systeemeigen_bundel_header
#include <stddef.h>
int 꾸러미열기(const char *Bestand_invoer_naam);
int 꾸러미읽기(const char *Naam, unsigned char *HR_gegevens, unsigned buffer_capaciteit);
const char *꾸러미진입클래스(void);
#endif
