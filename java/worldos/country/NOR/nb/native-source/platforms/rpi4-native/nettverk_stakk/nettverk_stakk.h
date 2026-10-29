#ifndef opprinnelig_nettverk_Topptekst
#define opprinnelig_nettverk_Topptekst
#include <stdint.h>
#include <stddef.h>
void Forbered_nettverk(void);
void 통신망살피기(void);
int åpne_socket_deltaker(int Type_område);
int netto_BIND(int Fil_håndtak, uint32_t e_post, unsigned portnummer);
int 연결기다리기(int Fil_håndtak);
void 통신주소재사용(int Fil_håndtak);
int netto_KOBLE_TIL(int Fil_håndtak, uint32_t e_post, unsigned portnummer);
int netto_godta(int Fil_håndtak);
int 통신읽기(int Fil_håndtak, void *data, unsigned vare_ANTALL);
int netto_skrive(int Fil_håndtak, const void *data, unsigned vare_ANTALL);
int sende_datagram(int Fil_håndtak, const void *data, unsigned vare_ANTALL, uint32_t e_post, unsigned portnummer);
int motta_datagram(int Fil_håndtak, void *data, unsigned vare_ANTALL);
unsigned nettverk_portnummer(int Fil_håndtak);
unsigned node_portnummer(int Fil_håndtak);
uint32_t netto_node_e_post(int Fil_håndtak);
void Lukk_nettverk(int Fil_håndtak);
int filoverføring_kontroll(int Handling);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned oppføring_VERDI, unsigned INDEKS);
int konfigurere_nettverk(unsigned Handling, uint32_t e_post, uint32_t maske_VERDI, uint32_t gateway_VERDI);
int START_svar_test(uint32_t e_post, unsigned ordre_VERDI);
int 응답시험읽기(unsigned oppføring_VERDI);
#endif
