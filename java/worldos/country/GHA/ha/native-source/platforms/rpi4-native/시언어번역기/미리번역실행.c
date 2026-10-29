#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long na_ura_mai_kwakwalwa_Microsoft_Word;
static na_ura_mai_kwakwalwa_Microsoft_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char SMS[]="AOT runtime error\n";Rubuta_Fayil_Tarin_bayani(2,SMS,sizeof(SMS)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(na_ura_mai_kwakwalwa_Microsoft_Word *tara_Wurin_adana,int *깊이,na_ura_mai_kwakwalwa_Microsoft_Word Daraja){if(*깊이<0||*깊이>=128)자바실패();tara_Wurin_adana[(*깊이)++]=Daraja;}
na_ura_mai_kwakwalwa_Microsoft_Word 자바꺼내기(na_ura_mai_kwakwalwa_Microsoft_Word *tara_Wurin_adana,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return tara_Wurin_adana[--*깊이];}
na_ura_mai_kwakwalwa_Microsoft_Word 자바배열(int 개수){if(개수<0||(unsigned)개수+1>8192-사용량)자바실패();na_ura_mai_kwakwalwa_Microsoft_Word*자료위치=동적기억공간+사용량;사용량+=개수+1;자료위치[0]=개수;return (na_ura_mai_kwakwalwa_Microsoft_Word)자료위치;}
na_ura_mai_kwakwalwa_Microsoft_Word *자바색인(na_ura_mai_kwakwalwa_Microsoft_Word abu_Manazarta,int 개수){na_ura_mai_kwakwalwa_Microsoft_Word*자료위치=(na_ura_mai_kwakwalwa_Microsoft_Word*)abu_Manazarta;if(!자료위치||개수<0||(na_ura_mai_kwakwalwa_Microsoft_Word)개수>=자료위치[0])자바실패();return 자료위치+개수+1;}
int 자바길이(na_ura_mai_kwakwalwa_Microsoft_Word abu_Manazarta){if(!abu_Manazarta)자바실패();return *(na_ura_mai_kwakwalwa_Microsoft_Word*)abu_Manazarta;}
int 자바나누기(int gamayyar_x,int Maɓallin_Y_Mai_tsarawa,int 나머지){if(!Maɓallin_Y_Mai_tsarawa)자바실패();if(gamayyar_x==(-2147483647-1)&&Maɓallin_Y_Mai_tsarawa==-1)return 나머지?0:gamayyar_x;return 나머지?gamayyar_x%Maɓallin_Y_Mai_tsarawa:gamayyar_x/Maɓallin_Y_Mai_tsarawa;}
static unsigned Tsawo_Daraja(const char*Zare_Tarin_bayani){unsigned 개수=0;if(!Zare_Tarin_bayani)자바실패();while(Zare_Tarin_bayani[개수])개수++;return 개수;}
void 자바출력(na_ura_mai_kwakwalwa_Microsoft_Word 자료위치,int 수치,int 줄바꿈){
    if(수치){char 둘째값[16];unsigned 개수=0;int Daraja=(int)자료위치;unsigned 부호없는값=Daraja<0?0-(unsigned)Daraja:Daraja;do{둘째값[개수++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(Daraja<0)둘째값[개수++]='-';while(개수)Rubuta_Fayil_Tarin_bayani(1,둘째값+--개수,1);}
    else{const char*Zare_Tarin_bayani=자료위치?(const char*)자료위치:"null";Rubuta_Fayil_Tarin_bayani(1,Zare_Tarin_bayani,Tsawo_Daraja(Zare_Tarin_bayani));}if(줄바꿈)Rubuta_Fayil_Tarin_bayani(1,"\n",1);
}
na_ura_mai_kwakwalwa_Microsoft_Word 자바파일쓰기(na_ura_mai_kwakwalwa_Microsoft_Word Hanyar_shiga,na_ura_mai_kwakwalwa_Microsoft_Word Daraja){const char*Zare_Tarin_bayani=(const char*)Daraja;unsigned 개수=Tsawo_Daraja(Zare_Tarin_bayani);int Fayil_Mariki=buɗe_Fayil((const char*)Hanyar_shiga,쓰기전용|없으면만들기|내용비우기,0600);if(Fayil_Mariki<0)자바실패();int 반환값=Rubuta_Fayil_Tarin_bayani(Fayil_Mariki,Zare_Tarin_bayani,개수);Rufe_Fayil(Fayil_Mariki);if(반환값!=(int)개수)자바실패();return 0;}
na_ura_mai_kwakwalwa_Microsoft_Word 자바파일읽기(na_ura_mai_kwakwalwa_Microsoft_Word Hanyar_shiga){int Fayil_Mariki=buɗe_Fayil((const char*)Hanyar_shiga,karanta_kawai_Daraja,0);if(Fayil_Mariki<0)자바실패();int 개수=Fayil_girma(Fayil_Mariki);if(개수<0||개수>16384||(unsigned)(개수+8)/8>8192-사용량)자바실패();char*자료위치=(char*)(동적기억공간+사용량);사용량+=(개수+8)/8;int 반환값=파일자료읽기(Fayil_Mariki,자료위치,개수);Rufe_Fayil(Fayil_Mariki);if(반환값!=개수)자바실패();자료위치[개수]=0;return (na_ura_mai_kwakwalwa_Microsoft_Word)자료위치;}
