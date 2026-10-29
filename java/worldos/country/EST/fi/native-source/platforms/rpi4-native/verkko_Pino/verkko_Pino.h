#ifndef alkuperäinen_verkko_otsikko
#define alkuperäinen_verkko_otsikko
#include <stdint.h>
#include <stddef.h>
void Valmistele_verkko(void);
void 통신망살피기(void);
int Luo_vastake_päätepiste(int TYYPPI_alue);
int NET_BIND(int Tiedosto_kahva, uint32_t OSOITE, unsigned portin_numero);
int NET_kuunnella(int Tiedosto_kahva);
void 통신주소재사용(int Tiedosto_kahva);
int NET_YHDISTÄ(int Tiedosto_kahva, uint32_t OSOITE, unsigned portin_numero);
int NET_hyväksyä(int Tiedosto_kahva);
int NET_lukea(int Tiedosto_kahva, void *data, unsigned kohde_LASKE);
int NET_kirjoitus(int Tiedosto_kahva, const void *data, unsigned kohde_LASKE);
int lähettää_datagrammi(int Tiedosto_kahva, const void *data, unsigned kohde_LASKE, uint32_t OSOITE, unsigned portin_numero);
int saada_datagrammi(int Tiedosto_kahva, void *data, unsigned kohde_LASKE);
unsigned verkko_portin_numero(int Tiedosto_kahva);
unsigned vertaissolmu_portin_numero(int Tiedosto_kahva);
uint32_t NET_vertaissolmu_OSOITE(int Tiedosto_kahva);
void Sulje_verkko(int Tiedosto_kahva);
int tiedostonsiirto_ohjain(int Toiminto);
void 파일전송살피기(void);
uint32_t lukea_verkko_tila(unsigned merkintä_ARVO_962f286b, unsigned INDEKSI);
int määrittää_verkko(unsigned Toiminto, uint32_t OSOITE, uint32_t peite_ARVO, uint32_t yhdyskäytävä_ARVO);
int alku_vastaus_testi(uint32_t OSOITE, unsigned tilata_ARVO);
int lukea_vastaus_testi(unsigned merkintä_ARVO_962f286b);
#endif
