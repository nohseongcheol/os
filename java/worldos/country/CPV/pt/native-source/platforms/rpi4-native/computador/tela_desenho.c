/* real_dados tela 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 códigoFonte/ComposiçãoEcrã.java. */
#include "../명명/기계연결이름.h"
#include "tela_informações.h"
static volatile uint32_t *화소들;
static unsigned tela_LIN_Contagem_de_Palavras, 화면너비, tela_altura;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t Vertical_cargo){
    return 화소들&&가로<화면너비&&Vertical_cargo<tela_altura?화소들[Vertical_cargo*tela_LIN_Contagem_de_Palavras+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t Vertical_cargo,uintptr_t 색){
    if(화소들&&가로<화면너비&&Vertical_cargo<tela_altura)화소들[Vertical_cargo*tela_LIN_Contagem_de_Palavras+가로]=(uint32_t)색;
}
void Quadro_Preparar_desenho(volatile uint32_t *dados,unsigned 폭,unsigned duração_VALOR,unsigned entrelinhamento_VALOR){
    화소들=dados;화면너비=폭;tela_altura=duração_VALOR;tela_LIN_Contagem_de_Palavras=entrelinhamento_VALOR/4;자바그림준비((int)폭,(int)duração_VALOR);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t Quadro_tela_altura(void){return (unsigned)자바그림높이();}
uint64_t Quadro_desenho_CONT_NÚM(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t Quadro_leitura_tela(unsigned 가로,unsigned Vertical_cargo){return (uint32_t)보드표시화소읽기(가로,Vertical_cargo);}
int 보드그림범위(int *가로,int *Vertical_cargo,int *폭,int *duração_VALOR){
    if(!자바그림범위(*가로,*Vertical_cargo,*폭,*duração_VALOR))return 0;
    *가로=자바그림범위값(0);*Vertical_cargo=자바그림범위값(1);*폭=자바그림범위값(2);*duração_VALOR=자바그림범위값(3);return 1;
}
int Quadro_START_desenho(int 가로,int Vertical_cargo,int 폭,int duração_VALOR){return 자바그림시작(가로,Vertical_cargo,폭,duração_VALOR);}
void Quadro_fim_desenho(void){자바그림마침();}
uintptr_t Quadro_pixel(uintptr_t 가로,uintptr_t Vertical_cargo,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)Vertical_cargo,(int)색);}
void Quadro_retângulo_preencher(int 가로,int Vertical_cargo,int 폭,int duração_VALOR,uint32_t 색){자바사각그림(가로,Vertical_cargo,폭,duração_VALOR,(int)색);}
void Quadro_ponteiro(int 가로,int Vertical_cargo,unsigned forma_VALOR){자바포인터(가로,Vertical_cargo,(int)forma_VALOR);}
