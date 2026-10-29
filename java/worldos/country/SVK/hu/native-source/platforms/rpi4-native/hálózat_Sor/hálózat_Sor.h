#ifndef natív_hálózat_fejléc
#define natív_hálózat_fejléc
#include <stdint.h>
#include <stddef.h>
void Előkészítés_hálózat(void);
void 통신망살피기(void);
int készít_szoftvercsatorna_végpont(int beír_terület);
int NET_BIND(int fájlleíró, uint32_t CÍM, unsigned portszám);
int NET_figyelés(int fájlleíró);
void 통신주소재사용(int fájlleíró);
int NET_KAPCSOLAT(int fájlleíró, uint32_t CÍM, unsigned portszám);
int NET_elfogad(int fájlleíró);
int 통신읽기(int fájlleíró, void *adat, unsigned cikk_DARAB);
int NET_ír(int fájlleíró, const void *adat, unsigned cikk_DARAB);
int küld_datagram(int fájlleíró, const void *adat, unsigned cikk_DARAB, uint32_t CÍM, unsigned portszám);
int fogad_datagram(int fájlleíró, void *adat, unsigned cikk_DARAB);
unsigned hálózat_portszám(int fájlleíró);
unsigned társ_portszám(int fájlleíró);
uint32_t NET_társ_CÍM(int fájlleíró);
void bezár_hálózat(int fájlleíró);
int fájlátvitel_vezérlő(int Művelet);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned bejegyzés_ÉRTÉK, unsigned INDEX);
int 망설정하기(unsigned Művelet, uint32_t CÍM, uint32_t maszk_ÉRTÉK, uint32_t átjáró_ÉRTÉK);
int START_válasz_teszt(uint32_t CÍM, unsigned rendel_ÉRTÉK);
int 응답시험읽기(unsigned bejegyzés_ÉRTÉK);
#endif
