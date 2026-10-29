#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long mašina_Word;
static mašina_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Tekstas[]="AOT runtime error\n";rašymas_Failas_duomenys(2,Tekstas,sizeof(Tekstas)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(mašina_Word *eilė_Saugykla,int *깊이,mašina_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();eilė_Saugykla[(*깊이)++]=VALUE;}
mašina_Word 자바꺼내기(mašina_Word *eilė_Saugykla,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return eilė_Saugykla[--*깊이];}
mašina_Word 자바배열(int prekė_COUNT){if(prekė_COUNT<0||(unsigned)prekė_COUNT+1>8192-사용량)자바실패();mašina_Word*duomenys_padėtis=동적기억공간+사용량;사용량+=prekė_COUNT+1;duomenys_padėtis[0]=prekė_COUNT;return (mašina_Word)duomenys_padėtis;}
mašina_Word *자바색인(mašina_Word objektas_nuoroda,int prekė_COUNT){mašina_Word*duomenys_padėtis=(mašina_Word*)objektas_nuoroda;if(!duomenys_padėtis||prekė_COUNT<0||(mašina_Word)prekė_COUNT>=duomenys_padėtis[0])자바실패();return duomenys_padėtis+prekė_COUNT+1;}
int 자바길이(mašina_Word objektas_nuoroda){if(!objektas_nuoroda)자바실패();return *(mašina_Word*)objektas_nuoroda;}
int 자바나누기(int x_koordinatė,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(x_koordinatė==(-2147483647-1)&&세로좌표==-1)return 나머지?0:x_koordinatė;return 나머지?x_koordinatė%세로좌표:x_koordinatė/세로좌표;}
static unsigned 길이(const char*eilutė_duomenys){unsigned prekė_COUNT=0;if(!eilutė_duomenys)자바실패();while(eilutė_duomenys[prekė_COUNT])prekė_COUNT++;return prekė_COUNT;}
void 자바출력(mašina_Word duomenys_padėtis,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned prekė_COUNT=0;int VALUE=(int)duomenys_padėtis;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[prekė_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[prekė_COUNT++]='-';while(prekė_COUNT)rašymas_Failas_duomenys(1,SECOND_VALUE+--prekė_COUNT,1);}
    else{const char*eilutė_duomenys=duomenys_padėtis?(const char*)duomenys_padėtis:"null";rašymas_Failas_duomenys(1,eilutė_duomenys,길이(eilutė_duomenys));}if(줄바꿈)rašymas_Failas_duomenys(1,"\n",1);
}
mašina_Word 자바파일쓰기(mašina_Word KELIAS,mašina_Word VALUE){const char*eilutė_duomenys=(const char*)VALUE;unsigned prekė_COUNT=길이(eilutė_duomenys);int Failas_rodyklė=kurti_Failas((const char*)KELIAS,쓰기전용|없으면만들기|trumpinti_Turinys,0600);if(Failas_rodyklė<0)자바실패();int 반환값=rašymas_Failas_duomenys(Failas_rodyklė,eilutė_duomenys,prekė_COUNT);Uždaryti_Failas(Failas_rodyklė);if(반환값!=(int)prekė_COUNT)자바실패();return 0;}
mašina_Word 자바파일읽기(mašina_Word KELIAS){int Failas_rodyklė=kurti_Failas((const char*)KELIAS,tik_skaitomas_VALUE,0);if(Failas_rodyklė<0)자바실패();int prekė_COUNT=failo_dydis(Failas_rodyklė);if(prekė_COUNT<0||prekė_COUNT>16384||(unsigned)(prekė_COUNT+8)/8>8192-사용량)자바실패();char*duomenys_padėtis=(char*)(동적기억공간+사용량);사용량+=(prekė_COUNT+8)/8;int 반환값=파일자료읽기(Failas_rodyklė,duomenys_padėtis,prekė_COUNT);Uždaryti_Failas(Failas_rodyklė);if(반환값!=prekė_COUNT)자바실패();duomenys_padėtis[prekė_COUNT]=0;return (mašina_Word)duomenys_padėtis;}
