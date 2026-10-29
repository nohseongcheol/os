#ifndef ursprunglig_nätverk_huvud
#define ursprunglig_nätverk_huvud
#include <stdint.h>
#include <stddef.h>
void Förbereda_nätverk(void);
void 통신망살피기(void);
int Skapa_socket_deltagare(int Typ_område);
int NET_BIND(int filreferens, uint32_t Adress, unsigned portnummer);
int NET_lyssna(int filreferens);
void 통신주소재사용(int filreferens);
int NET_ANSLUT(int filreferens, uint32_t Adress, unsigned portnummer);
int NET_acceptera(int filreferens);
int NET_läsa(int filreferens, void *data, unsigned objekt_ANTAL);
int NET_skriva(int filreferens, const void *data, unsigned objekt_ANTAL);
int skicka_datagram(int filreferens, const void *data, unsigned objekt_ANTAL, uint32_t Adress, unsigned portnummer);
int få_datagram(int filreferens, void *data, unsigned objekt_ANTAL);
unsigned nätverk_portnummer(int filreferens);
unsigned peer_portnummer(int filreferens);
uint32_t NET_peer_ADRESS(int filreferens);
void Stäng_nätverk(int filreferens);
int filöverföring_kontroll(int Åtgärd);
void 파일전송살피기(void);
uint32_t läsa_nätverk_status(unsigned post_värde, unsigned INDEX);
int konfigurera_nätverk(unsigned Åtgärd, uint32_t Adress, uint32_t mask_värde, uint32_t gateway_värde);
int START_svar_test(uint32_t Adress, unsigned order_värde);
int läsa_svar_test(unsigned post_värde);
#endif
