#ifndef systeemeigen_net_header
#define systeemeigen_net_header
#include <stdint.h>
#include <stddef.h>
void Bereid_voor_net(void);
void 통신망살피기(void);
int maken_socket_eindpunt(int TYPE_gebied);
int NET_BIND(int bestandsingang, uint32_t ADRES, unsigned poortnummer);
int 연결기다리기(int bestandsingang);
void 통신주소재사용(int bestandsingang);
int NET_VERBINDEN(int bestandsingang, uint32_t ADRES, unsigned poortnummer);
int NET_accepteren(int bestandsingang);
int 통신읽기(int bestandsingang, void *gegevens, unsigned item_AANTAL);
int NET_schrijven(int bestandsingang, const void *gegevens, unsigned item_AANTAL);
int e_mailen_datagram(int bestandsingang, const void *gegevens, unsigned item_AANTAL, uint32_t ADRES, unsigned poortnummer);
int ontvangen_datagram(int bestandsingang, void *gegevens, unsigned item_AANTAL);
unsigned net_poortnummer(int bestandsingang);
unsigned peer_poortnummer(int bestandsingang);
uint32_t NET_peer_ADRES(int bestandsingang);
void Sluiten_net(int bestandsingang);
int bestandsoverdracht_controle(int Actie);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned invoer_WAARDE_962f286b, unsigned INDEX);
int configureren_net(unsigned Actie, uint32_t ADRES, uint32_t masker_WAARDE, uint32_t gateway_WAARDE);
int START_reactie_test(uint32_t ADRES, unsigned order_WAARDE);
int 응답시험읽기(unsigned invoer_WAARDE_962f286b);
#endif
