#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long stroj_Word;
static stroj_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Tekst[]="AOT runtime error\n";zapisivanje_Datoteka_podaci(2,Tekst,sizeof(Tekst)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(stroj_Word *hrpa_Pohrana,int *깊이,stroj_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();hrpa_Pohrana[(*깊이)++]=VALUE;}
stroj_Word 자바꺼내기(stroj_Word *hrpa_Pohrana,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return hrpa_Pohrana[--*깊이];}
stroj_Word 자바배열(int artikl_COUNT){if(artikl_COUNT<0||(unsigned)artikl_COUNT+1>8192-사용량)자바실패();stroj_Word*podaci_položaj=동적기억공간+사용량;사용량+=artikl_COUNT+1;podaci_položaj[0]=artikl_COUNT;return (stroj_Word)podaci_položaj;}
stroj_Word *자바색인(stroj_Word objekt_Reference,int artikl_COUNT){stroj_Word*podaci_položaj=(stroj_Word*)objekt_Reference;if(!podaci_položaj||artikl_COUNT<0||(stroj_Word)artikl_COUNT>=podaci_položaj[0])자바실패();return podaci_položaj+artikl_COUNT+1;}
int 자바길이(stroj_Word objekt_Reference){if(!objekt_Reference)자바실패();return *(stroj_Word*)objekt_Reference;}
int 자바나누기(int koordinata_x,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(koordinata_x==(-2147483647-1)&&세로좌표==-1)return 나머지?0:koordinata_x;return 나머지?koordinata_x%세로좌표:koordinata_x/세로좌표;}
static unsigned 길이(const char*niz_podaci){unsigned artikl_COUNT=0;if(!niz_podaci)자바실패();while(niz_podaci[artikl_COUNT])artikl_COUNT++;return artikl_COUNT;}
void 자바출력(stroj_Word podaci_položaj,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned artikl_COUNT=0;int VALUE=(int)podaci_položaj;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[artikl_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[artikl_COUNT++]='-';while(artikl_COUNT)zapisivanje_Datoteka_podaci(1,SECOND_VALUE+--artikl_COUNT,1);}
    else{const char*niz_podaci=podaci_položaj?(const char*)podaci_položaj:"null";zapisivanje_Datoteka_podaci(1,niz_podaci,길이(niz_podaci));}if(줄바꿈)zapisivanje_Datoteka_podaci(1,"\n",1);
}
stroj_Word 자바파일쓰기(stroj_Word PUTANJA,stroj_Word VALUE){const char*niz_podaci=(const char*)VALUE;unsigned artikl_COUNT=길이(niz_podaci);int Datoteka_ustroj=otvoreno_Datoteka((const char*)PUTANJA,쓰기전용|없으면만들기|skratiti_Sadržaj,0600);if(Datoteka_ustroj<0)자바실패();int 반환값=zapisivanje_Datoteka_podaci(Datoteka_ustroj,niz_podaci,artikl_COUNT);Zatvori_Datoteka(Datoteka_ustroj);if(반환값!=(int)artikl_COUNT)자바실패();return 0;}
stroj_Word 자바파일읽기(stroj_Word PUTANJA){int Datoteka_ustroj=otvoreno_Datoteka((const char*)PUTANJA,samo_za_čitanje_VALUE,0);if(Datoteka_ustroj<0)자바실패();int artikl_COUNT=veličina_datoteke(Datoteka_ustroj);if(artikl_COUNT<0||artikl_COUNT>16384||(unsigned)(artikl_COUNT+8)/8>8192-사용량)자바실패();char*podaci_položaj=(char*)(동적기억공간+사용량);사용량+=(artikl_COUNT+8)/8;int 반환값=파일자료읽기(Datoteka_ustroj,podaci_položaj,artikl_COUNT);Zatvori_Datoteka(Datoteka_ustroj);if(반환값!=artikl_COUNT)자바실패();podaci_položaj[artikl_COUNT]=0;return (stroj_Word)podaci_položaj;}
