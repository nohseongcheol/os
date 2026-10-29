#ifndef nativo_rete_Intestazione
#define nativo_rete_Intestazione
#include <stdint.h>
#include <stddef.h>
void Prepara_rete(void);
void 통신망살피기(void);
int Crea_socket_endpoint(int TIPO_area);
int NET_BIND(int handle_di_file, uint32_t e_mail, unsigned numero_di_porta);
int NET_essere_in_ascolto(int handle_di_file);
void 통신주소재사용(int handle_di_file);
int NET_CONNETTI(int handle_di_file, uint32_t e_mail, unsigned numero_di_porta);
int NET_accettare(int handle_di_file);
int 통신읽기(int handle_di_file, void *dati, unsigned articolo_CONTA_NUMERI);
int NET_scrivere(int handle_di_file, const void *dati, unsigned articolo_CONTA_NUMERI);
int inviare_datagramma(int handle_di_file, const void *dati, unsigned articolo_CONTA_NUMERI, uint32_t e_mail, unsigned numero_di_porta);
int ricevere_datagramma(int handle_di_file, void *dati, unsigned articolo_CONTA_NUMERI);
unsigned rete_numero_di_porta(int handle_di_file);
unsigned peer_numero_di_porta(int handle_di_file);
uint32_t NET_peer_e_mail(int handle_di_file);
void Chiudi_rete(int handle_di_file);
int trasferimento_di_file_controllo(int Azione);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned voce_VALORE, unsigned INDICE);
int configurare_rete(unsigned Azione, uint32_t e_mail, uint32_t maschera_VALORE, uint32_t gateway_VALORE);
int START_risposta_test(uint32_t e_mail, unsigned ordine_VALORE);
int 응답시험읽기(unsigned voce_VALORE);
#endif
