#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long računar_Word;
static računar_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char SMS[]="AOT runtime error\n";파일자료쓰기(2,SMS,sizeof(SMS)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(računar_Word *stek_Skladište,int *깊이,računar_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();stek_Skladište[(*깊이)++]=VALUE;}
računar_Word 자바꺼내기(računar_Word *stek_Skladište,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return stek_Skladište[--*깊이];}
računar_Word 자바배열(int stavka_COUNT){if(stavka_COUNT<0||(unsigned)stavka_COUNT+1>8192-사용량)자바실패();računar_Word*podaci_pozicija=동적기억공간+사용량;사용량+=stavka_COUNT+1;podaci_pozicija[0]=stavka_COUNT;return (računar_Word)podaci_pozicija;}
računar_Word *자바색인(računar_Word objekat_referenca,int stavka_COUNT){računar_Word*podaci_pozicija=(računar_Word*)objekat_referenca;if(!podaci_pozicija||stavka_COUNT<0||(računar_Word)stavka_COUNT>=podaci_pozicija[0])자바실패();return podaci_pozicija+stavka_COUNT+1;}
int 자바길이(računar_Word objekat_referenca){if(!objekat_referenca)자바실패();return *(računar_Word*)objekat_referenca;}
int 자바나누기(int x_koordinata,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(x_koordinata==(-2147483647-1)&&세로좌표==-1)return 나머지?0:x_koordinata;return 나머지?x_koordinata%세로좌표:x_koordinata/세로좌표;}
static unsigned 길이(const char*niska_podaci){unsigned stavka_COUNT=0;if(!niska_podaci)자바실패();while(niska_podaci[stavka_COUNT])stavka_COUNT++;return stavka_COUNT;}
void 자바출력(računar_Word podaci_pozicija,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned stavka_COUNT=0;int VALUE=(int)podaci_pozicija;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[stavka_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[stavka_COUNT++]='-';while(stavka_COUNT)파일자료쓰기(1,SECOND_VALUE+--stavka_COUNT,1);}
    else{const char*niska_podaci=podaci_pozicija?(const char*)podaci_pozicija:"null";파일자료쓰기(1,niska_podaci,길이(niska_podaci));}if(줄바꿈)파일자료쓰기(1,"\n",1);
}
računar_Word 자바파일쓰기(računar_Word putanja,računar_Word VALUE){const char*niska_podaci=(const char*)VALUE;unsigned stavka_COUNT=길이(niska_podaci);int Datoteka_pokazivač=otvoren_Datoteka((const char*)putanja,쓰기전용|없으면만들기|내용비우기,0600);if(Datoteka_pokazivač<0)자바실패();int 반환값=파일자료쓰기(Datoteka_pokazivač,niska_podaci,stavka_COUNT);Zatvori_Datoteka(Datoteka_pokazivač);if(반환값!=(int)stavka_COUNT)자바실패();return 0;}
računar_Word 자바파일읽기(računar_Word putanja){int Datoteka_pokazivač=otvoren_Datoteka((const char*)putanja,samo_za_čitanje_VALUE,0);if(Datoteka_pokazivač<0)자바실패();int stavka_COUNT=veličina_datoteke(Datoteka_pokazivač);if(stavka_COUNT<0||stavka_COUNT>16384||(unsigned)(stavka_COUNT+8)/8>8192-사용량)자바실패();char*podaci_pozicija=(char*)(동적기억공간+사용량);사용량+=(stavka_COUNT+8)/8;int 반환값=파일자료읽기(Datoteka_pokazivač,podaci_pozicija,stavka_COUNT);Zatvori_Datoteka(Datoteka_pokazivač);if(반환값!=stavka_COUNT)자바실패();podaci_pozicija[stavka_COUNT]=0;return (računar_Word)podaci_pozicija;}
