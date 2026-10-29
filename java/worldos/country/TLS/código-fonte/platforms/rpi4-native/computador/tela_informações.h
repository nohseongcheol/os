#ifndef nativo_tela_informações_Cabeçalho
#define nativo_tela_informações_Cabeçalho
#include <stdint.h>
/* 초기화가 끝난 real_dados RGB32 tela Tamanho. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t Quadro_tela_altura(void);
/* 0: Oculta_VALOR, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Quadro_ponteiro(int 가로, int Vertical_cargo, unsigned forma_VALOR);
/* 한 번에 32줄을 완성한 BACK_VALOR, 달라진 화소만 real_dados 화면에 옮긴다. */
void Quadro_Preparar_desenho(volatile uint32_t *dados, unsigned 폭, unsigned duração_VALOR, unsigned entrelinhamento_VALOR);
int 보드그림범위(int *가로, int *Vertical_cargo, int *폭, int *duração_VALOR);
int Quadro_START_desenho(int 가로, int Vertical_cargo, int 폭, int duração_VALOR);
void Quadro_fim_desenho(void);
void Quadro_retângulo_preencher(int 가로, int Vertical_cargo, int 폭, int duração_VALOR, uint32_t 색);
/* real_dados mostrar_VALOR 메모리에 기록한 pixel número. ponteiro 갱신은 제외한다. */
uint64_t Quadro_desenho_CONT_NÚM(void);
uint32_t Quadro_leitura_tela(unsigned 가로, unsigned Vertical_cargo);
#endif
