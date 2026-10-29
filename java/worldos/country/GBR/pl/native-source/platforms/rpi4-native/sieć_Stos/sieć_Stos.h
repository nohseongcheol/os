#ifndef natywny_sieć_Nagłówek
#define natywny_sieć_Nagłówek
#include <stdint.h>
#include <stddef.h>
void Przygotuj_sieć(void);
void 통신망살피기(void);
int Twórca_gniazdo_uczestnik(int TYP_obszar);
int NET_BIND(int dojście_do_pliku, uint32_t Adres, unsigned numer_portu);
int NET_nasłuchiwać(int dojście_do_pliku);
void 통신주소재사용(int dojście_do_pliku);
int NET_POŁĄCZ(int dojście_do_pliku, uint32_t Adres, unsigned numer_portu);
int NET_akceptować(int dojście_do_pliku);
int 통신읽기(int dojście_do_pliku, void *dane, unsigned towar_ILE_LICZB);
int NET_zapis(int dojście_do_pliku, const void *dane, unsigned towar_ILE_LICZB);
int wysłać_datagram(int dojście_do_pliku, const void *dane, unsigned towar_ILE_LICZB, uint32_t Adres, unsigned numer_portu);
int odbierać_datagram(int dojście_do_pliku, void *dane, unsigned towar_ILE_LICZB);
unsigned sieć_numer_portu(int dojście_do_pliku);
unsigned węzeł_równorzędny_numer_portu(int dojście_do_pliku);
uint32_t NET_węzeł_równorzędny_ADRES(int dojście_do_pliku);
void Zamknij_sieć(int dojście_do_pliku);
int transfer_plików_kontrola(int Akcja);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned wpis_WARTOŚĆ, unsigned INDEKS);
int konfigurować_sieć(unsigned Akcja, uint32_t Adres, uint32_t maska_WARTOŚĆ, uint32_t brama_WARTOŚĆ);
int START_odpowiedź_test(uint32_t Adres, unsigned zamówić_WARTOŚĆ);
int 응답시험읽기(unsigned wpis_WARTOŚĆ);
#endif
