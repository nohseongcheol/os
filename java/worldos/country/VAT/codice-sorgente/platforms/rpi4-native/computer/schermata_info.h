#ifndef nativo_schermata_info_Intestazione
#define nativo_schermata_info_Intestazione
#include <stdint.h>
/* 초기화가 끝난 effettivo_dati RGB32 schermata Dimensione. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t scheda_schermata_altezza(void);
/* 0: Nascosta_VALORE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void scheda_puntatore(int 가로, int Verticale_funzione, unsigned forma_VALORE);
/* 한 번에 32줄을 완성한 BACK_VALORE, 달라진 화소만 effettivo_dati 화면에 옮긴다. */
void scheda_Prepara_disegno(volatile uint32_t *dati, unsigned 폭, unsigned durata_VALORE, unsigned interlinea_VALORE);
int 보드그림범위(int *가로, int *Verticale_funzione, int *폭, int *durata_VALORE);
int scheda_START_disegno(int 가로, int Verticale_funzione, int 폭, int durata_VALORE);
void scheda_Fine_disegno(void);
void scheda_rettangolo_Riempi(int 가로, int Verticale_funzione, int 폭, int durata_VALORE, uint32_t 색);
/* effettivo_dati mostrare_VALORE 메모리에 기록한 pixel numero. puntatore 갱신은 제외한다. */
uint64_t scheda_disegno_CONTA_NUMERI(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Verticale_funzione);
#endif
