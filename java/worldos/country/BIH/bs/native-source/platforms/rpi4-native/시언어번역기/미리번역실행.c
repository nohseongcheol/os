#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long mašina_Word;
static mašina_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Tekst[]="AOT runtime error\n";pisati_fajl_podaci(2,Tekst,sizeof(Tekst)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(mašina_Word *snop_Pohrana,int *깊이,mašina_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();snop_Pohrana[(*깊이)++]=VALUE;}
mašina_Word 자바꺼내기(mašina_Word *snop_Pohrana,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return snop_Pohrana[--*깊이];}
mašina_Word 자바배열(int stavka_COUNT){if(stavka_COUNT<0||(unsigned)stavka_COUNT+1>8192-사용량)자바실패();mašina_Word*podaci_položaj=동적기억공간+사용량;사용량+=stavka_COUNT+1;podaci_položaj[0]=stavka_COUNT;return (mašina_Word)podaci_položaj;}
mašina_Word *자바색인(mašina_Word objekt_Reference,int stavka_COUNT){mašina_Word*podaci_položaj=(mašina_Word*)objekt_Reference;if(!podaci_položaj||stavka_COUNT<0||(mašina_Word)stavka_COUNT>=podaci_položaj[0])자바실패();return podaci_položaj+stavka_COUNT+1;}
int 자바길이(mašina_Word objekt_Reference){if(!objekt_Reference)자바실패();return *(mašina_Word*)objekt_Reference;}
int 자바나누기(int koordinata_x,int Y_koordinata,int 나머지){if(!Y_koordinata)자바실패();if(koordinata_x==(-2147483647-1)&&Y_koordinata==-1)return 나머지?0:koordinata_x;return 나머지?koordinata_x%Y_koordinata:koordinata_x/Y_koordinata;}
static unsigned dužina_VALUE(const char*string_podaci){unsigned stavka_COUNT=0;if(!string_podaci)자바실패();while(string_podaci[stavka_COUNT])stavka_COUNT++;return stavka_COUNT;}
void 자바출력(mašina_Word podaci_položaj,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned stavka_COUNT=0;int VALUE=(int)podaci_položaj;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[stavka_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[stavka_COUNT++]='-';while(stavka_COUNT)pisati_fajl_podaci(1,SECOND_VALUE+--stavka_COUNT,1);}
    else{const char*string_podaci=podaci_položaj?(const char*)podaci_položaj:"null";pisati_fajl_podaci(1,string_podaci,dužina_VALUE(string_podaci));}if(줄바꿈)pisati_fajl_podaci(1,"\n",1);
}
mašina_Word 자바파일쓰기(mašina_Word Putanja,mašina_Word VALUE){const char*string_podaci=(const char*)VALUE;unsigned stavka_COUNT=dužina_VALUE(string_podaci);int fajl_hvatište=kreirati_fajl((const char*)Putanja,쓰기전용|없으면만들기|내용비우기,0600);if(fajl_hvatište<0)자바실패();int 반환값=pisati_fajl_podaci(fajl_hvatište,string_podaci,stavka_COUNT);zatvoriti_fajl(fajl_hvatište);if(반환값!=(int)stavka_COUNT)자바실패();return 0;}
mašina_Word 자바파일읽기(mašina_Word Putanja){int fajl_hvatište=kreirati_fajl((const char*)Putanja,samo_za_čitanje_VALUE,0);if(fajl_hvatište<0)자바실패();int stavka_COUNT=fajl_podesiti_veličinu(fajl_hvatište);if(stavka_COUNT<0||stavka_COUNT>16384||(unsigned)(stavka_COUNT+8)/8>8192-사용량)자바실패();char*podaci_položaj=(char*)(동적기억공간+사용량);사용량+=(stavka_COUNT+8)/8;int 반환값=파일자료읽기(fajl_hvatište,podaci_položaj,stavka_COUNT);zatvoriti_fajl(fajl_hvatište);if(반환값!=stavka_COUNT)자바실패();podaci_položaj[stavka_COUNT]=0;return (mašina_Word)podaci_položaj;}
