#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Sagatavot_tīkls(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_joma);
int NET_BIND(int Fails_turis, uint32_t adrese, unsigned porta_numurs);
int NET_klausīties(int Fails_turis);
void 통신주소재사용(int Fails_turis);
int NET_saziņa(int Fails_turis, uint32_t adrese, unsigned porta_numurs);
int NET_akceptēt(int Fails_turis);
int 통신읽기(int Fails_turis, void *dati, unsigned krājums_COUNT);
int NET_rakstīšana(int Fails_turis, const void *dati, unsigned krājums_COUNT);
int sūtīt_datogramma(int Fails_turis, const void *dati, unsigned krājums_COUNT, uint32_t adrese, unsigned porta_numurs);
int saņemt_datogramma(int Fails_turis, void *dati, unsigned krājums_COUNT);
unsigned tīkls_porta_numurs(int Fails_turis);
unsigned vienranga_porta_numurs(int Fails_turis);
uint32_t NET_vienranga_adrese(int Fails_turis);
void Aizvērt_tīkls(int Fails_turis);
int faila_pārsūtīšana_vadība(int Darbība);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ievade_VALUE, unsigned INDEX);
int konfigurēt_tīkls(unsigned Darbība, uint32_t adrese, uint32_t maska_VALUE, uint32_t vārteja_VALUE);
int 응답시험시작(uint32_t adrese, unsigned secība_VALUE);
int 응답시험읽기(unsigned ievade_VALUE);
#endif
