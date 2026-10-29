#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long računalnik_Word;
static računalnik_Word kopica_Senzor_prostora[8192];static unsigned 사용량;
void 자바실패(void){const char Besedilo[]="AOT runtime error\n";pisati_Datoteka_podatki(2,Besedilo,sizeof(Besedilo)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(računalnik_Word *Sklad_Senzor_prostora,int *깊이,računalnik_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();Sklad_Senzor_prostora[(*깊이)++]=VALUE;}
računalnik_Word 자바꺼내기(računalnik_Word *Sklad_Senzor_prostora,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Sklad_Senzor_prostora[--*깊이];}
računalnik_Word 자바배열(int element_COUNT){if(element_COUNT<0||(unsigned)element_COUNT+1>8192-사용량)자바실패();računalnik_Word*podatki_položaj=kopica_Senzor_prostora+사용량;사용량+=element_COUNT+1;podatki_položaj[0]=element_COUNT;return (računalnik_Word)podatki_položaj;}
računalnik_Word *자바색인(računalnik_Word predmet_Gradiva,int element_COUNT){računalnik_Word*podatki_položaj=(računalnik_Word*)predmet_Gradiva;if(!podatki_položaj||element_COUNT<0||(računalnik_Word)element_COUNT>=podatki_položaj[0])자바실패();return podatki_položaj+element_COUNT+1;}
int 자바길이(računalnik_Word predmet_Gradiva){if(!predmet_Gradiva)자바실패();return *(računalnik_Word*)predmet_Gradiva;}
int 자바나누기(int koordinata_x,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(koordinata_x==(-2147483647-1)&&세로좌표==-1)return 나머지?0:koordinata_x;return 나머지?koordinata_x%세로좌표:koordinata_x/세로좌표;}
static unsigned 길이(const char*niz_podatki){unsigned element_COUNT=0;if(!niz_podatki)자바실패();while(niz_podatki[element_COUNT])element_COUNT++;return element_COUNT;}
void 자바출력(računalnik_Word podatki_položaj,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned element_COUNT=0;int VALUE=(int)podatki_položaj;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[element_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[element_COUNT++]='-';while(element_COUNT)pisati_Datoteka_podatki(1,SECOND_VALUE+--element_COUNT,1);}
    else{const char*niz_podatki=podatki_položaj?(const char*)podatki_položaj:"null";pisati_Datoteka_podatki(1,niz_podatki,길이(niz_podatki));}if(줄바꿈)pisati_Datoteka_podatki(1,"\n",1);
}
računalnik_Word 자바파일쓰기(računalnik_Word POT,računalnik_Word VALUE){const char*niz_podatki=(const char*)VALUE;unsigned element_COUNT=길이(niz_podatki);int Datoteka_ročica=odprto_Datoteka((const char*)POT,쓰기전용|없으면만들기|내용비우기,0600);if(Datoteka_ročica<0)자바실패();int 반환값=pisati_Datoteka_podatki(Datoteka_ročica,niz_podatki,element_COUNT);Zapri_Datoteka(Datoteka_ročica);if(반환값!=(int)element_COUNT)자바실패();return 0;}
računalnik_Word 자바파일읽기(računalnik_Word POT){int Datoteka_ročica=odprto_Datoteka((const char*)POT,samo_za_branje_VALUE,0);if(Datoteka_ročica<0)자바실패();int element_COUNT=velikost_datoteke(Datoteka_ročica);if(element_COUNT<0||element_COUNT>16384||(unsigned)(element_COUNT+8)/8>8192-사용량)자바실패();char*podatki_položaj=(char*)(kopica_Senzor_prostora+사용량);사용량+=(element_COUNT+8)/8;int 반환값=파일자료읽기(Datoteka_ročica,podatki_položaj,element_COUNT);Zapri_Datoteka(Datoteka_ročica);if(반환값!=element_COUNT)자바실패();podatki_položaj[element_COUNT]=0;return (računalnik_Word)podatki_položaj;}
