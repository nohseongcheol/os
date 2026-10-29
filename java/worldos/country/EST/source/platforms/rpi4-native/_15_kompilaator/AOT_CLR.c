#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long arvuti_Word;
static arvuti_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Tekst[]="AOT runtime error\n";kirjutamine_Fail_andmed(2,Tekst,sizeof(Tekst)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(arvuti_Word *Virn_salvesti,int *깊이,arvuti_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();Virn_salvesti[(*깊이)++]=VALUE;}
arvuti_Word 자바꺼내기(arvuti_Word *Virn_salvesti,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Virn_salvesti[--*깊이];}
arvuti_Word 자바배열(int kaup_COUNT){if(kaup_COUNT<0||(unsigned)kaup_COUNT+1>8192-사용량)자바실패();arvuti_Word*andmed_ametikoht=동적기억공간+사용량;사용량+=kaup_COUNT+1;andmed_ametikoht[0]=kaup_COUNT;return (arvuti_Word)andmed_ametikoht;}
arvuti_Word *자바색인(arvuti_Word objekt_viide,int kaup_COUNT){arvuti_Word*andmed_ametikoht=(arvuti_Word*)objekt_viide;if(!andmed_ametikoht||kaup_COUNT<0||(arvuti_Word)kaup_COUNT>=andmed_ametikoht[0])자바실패();return andmed_ametikoht+kaup_COUNT+1;}
int 자바길이(arvuti_Word objekt_viide){if(!objekt_viide)자바실패();return *(arvuti_Word*)objekt_viide;}
int 자바나누기(int 가로좌표,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(가로좌표==(-2147483647-1)&&세로좌표==-1)return 나머지?0:가로좌표;return 나머지?가로좌표%세로좌표:가로좌표/세로좌표;}
static unsigned 길이(const char*string_andmed){unsigned kaup_COUNT=0;if(!string_andmed)자바실패();while(string_andmed[kaup_COUNT])kaup_COUNT++;return kaup_COUNT;}
void 자바출력(arvuti_Word andmed_ametikoht,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned kaup_COUNT=0;int VALUE=(int)andmed_ametikoht;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[kaup_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[kaup_COUNT++]='-';while(kaup_COUNT)kirjutamine_Fail_andmed(1,SECOND_VALUE+--kaup_COUNT,1);}
    else{const char*string_andmed=andmed_ametikoht?(const char*)andmed_ametikoht:"null";kirjutamine_Fail_andmed(1,string_andmed,길이(string_andmed));}if(줄바꿈)kirjutamine_Fail_andmed(1,"\n",1);
}
arvuti_Word 자바파일쓰기(arvuti_Word RADA,arvuti_Word VALUE){const char*string_andmed=(const char*)VALUE;unsigned kaup_COUNT=길이(string_andmed);int Fail_pide=avama_Fail((const char*)RADA,쓰기전용|없으면만들기|lühendama_Sisu,0600);if(Fail_pide<0)자바실패();int 반환값=kirjutamine_Fail_andmed(Fail_pide,string_andmed,kaup_COUNT);Sule_Fail(Fail_pide);if(반환값!=(int)kaup_COUNT)자바실패();return 0;}
arvuti_Word 자바파일읽기(arvuti_Word RADA){int Fail_pide=avama_Fail((const char*)RADA,kirjutuskaitstud_VALUE,0);if(Fail_pide<0)자바실패();int kaup_COUNT=faili_maht(Fail_pide);if(kaup_COUNT<0||kaup_COUNT>16384||(unsigned)(kaup_COUNT+8)/8>8192-사용량)자바실패();char*andmed_ametikoht=(char*)(동적기억공간+사용량);사용량+=(kaup_COUNT+8)/8;int 반환값=파일자료읽기(Fail_pide,andmed_ametikoht,kaup_COUNT);Sule_Fail(Fail_pide);if(반환값!=kaup_COUNT)자바실패();andmed_ametikoht[kaup_COUNT]=0;return (arvuti_Word)andmed_ametikoht;}
