#ifndef entêteInformationÉcranNatif
#define entêteInformationÉcranNatif
#include <stdint.h>
/* 초기화가 끝난 donnéesEffectif RGB32 Écran taille. 준비되지 않았으면 0이다. */
uintptr_t largeurÉcranCarteMatérielle(void);
uintptr_t hauteurÉcranCarteMatérielle(void);
/* 0: valeurCaché, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void pointeurCarteMatérielle(int positionHorizontal, int positionVertical, unsigned valeurForme);
/* 한 번에 32줄을 완성한 valeurRetourArrièreCôté, 달라진 화소만 donnéesEffectif 화면에 옮긴다. */
void dessinPréparerCarteMatérielle(volatile uint32_t *Données, unsigned étendueLargeur, unsigned longueur, unsigned valeurEspacementLigne);
int bornesDessinCarteMatérielle(int *positionHorizontal, int *positionVertical, int *étendueLargeur, int *longueur);
int dessinDémarrerCarteMatérielle(int positionHorizontal, int positionVertical, int étendueLargeur, int longueur);
void dessinTerminerCarteMatérielle(void);
void remplirRectangleCarteMatérielle(int positionHorizontal, int positionVertical, int étendueLargeur, int longueur, uint32_t valeurCouleur);
/* donnéesEffectif afficherValeur 메모리에 기록한 pixel nombre. pointeur 갱신은 제외한다. */
uint64_t nombreÉlémentsDessinCarteMatérielle(void);
uint32_t écranLireCarteMatérielle(unsigned positionHorizontal, unsigned positionVertical);
#endif
