#ifndef oprindelig_netværk_Header
#define oprindelig_netværk_Header
#include <stdint.h>
#include <stddef.h>
void Tilrettelæg_netværk(void);
void 통신망살피기(void);
int åbne_socket_slutpunkt(int Type_område);
int NET_BIND(int fil_handle, uint32_t mail, unsigned portnummer);
int NET_lytte(int fil_handle);
void 통신주소재사용(int fil_handle);
int NET_Forbind(int fil_handle, uint32_t mail, unsigned portnummer);
int NET_acceptere(int fil_handle);
int 통신읽기(int fil_handle, void *data, unsigned vare_TÆL);
int NET_skrive(int fil_handle, const void *data, unsigned vare_TÆL);
int maile_datagram(int fil_handle, const void *data, unsigned vare_TÆL, uint32_t mail, unsigned portnummer);
int modtage_datagram(int fil_handle, void *data, unsigned vare_TÆL);
unsigned netværk_portnummer(int fil_handle);
unsigned peer_portnummer(int fil_handle);
uint32_t NET_peer_mail(int fil_handle);
void Luk_netværk(int fil_handle);
int filoverførsel_kontrol(int Handling);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned post_VÆRDI_962f286b, unsigned INDEKS);
int konfigurere_netværk(unsigned Handling, uint32_t mail, uint32_t maske_VÆRDI, uint32_t gateway_VÆRDI);
int START_svar_test(uint32_t mail, unsigned ordre_VÆRDI);
int 응답시험읽기(unsigned post_VÆRDI_962f286b);
#endif
