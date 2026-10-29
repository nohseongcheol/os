#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long vél_Word;
static vél_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Texti[]="AOT runtime error\n";skrifa_skrá_gögn(2,Texti,sizeof(Texti)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(vél_Word *bunki_geymsla,int *깊이,vél_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();bunki_geymsla[(*깊이)++]=VALUE;}
vél_Word 자바꺼내기(vél_Word *bunki_geymsla,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return bunki_geymsla[--*깊이];}
vél_Word 자바배열(int vara_COUNT){if(vara_COUNT<0||(unsigned)vara_COUNT+1>8192-사용량)자바실패();vél_Word*gögn_staða=동적기억공간+사용량;사용량+=vara_COUNT+1;gögn_staða[0]=vara_COUNT;return (vél_Word)gögn_staða;}
vél_Word *자바색인(vél_Word hlutur_tilvísun,int vara_COUNT){vél_Word*gögn_staða=(vél_Word*)hlutur_tilvísun;if(!gögn_staða||vara_COUNT<0||(vél_Word)vara_COUNT>=gögn_staða[0])자바실패();return gögn_staða+vara_COUNT+1;}
int 자바길이(vél_Word hlutur_tilvísun){if(!hlutur_tilvísun)자바실패();return *(vél_Word*)hlutur_tilvísun;}
int 자바나누기(int x_hnit,int Y_hnit,int 나머지){if(!Y_hnit)자바실패();if(x_hnit==(-2147483647-1)&&Y_hnit==-1)return 나머지?0:x_hnit;return 나머지?x_hnit%Y_hnit:x_hnit/Y_hnit;}
static unsigned lengd_VALUE(const char*strengur_gögn){unsigned vara_COUNT=0;if(!strengur_gögn)자바실패();while(strengur_gögn[vara_COUNT])vara_COUNT++;return vara_COUNT;}
void 자바출력(vél_Word gögn_staða,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned vara_COUNT=0;int VALUE=(int)gögn_staða;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[vara_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[vara_COUNT++]='-';while(vara_COUNT)skrifa_skrá_gögn(1,SECOND_VALUE+--vara_COUNT,1);}
    else{const char*strengur_gögn=gögn_staða?(const char*)gögn_staða:"null";skrifa_skrá_gögn(1,strengur_gögn,lengd_VALUE(strengur_gögn));}if(줄바꿈)skrifa_skrá_gögn(1,"\n",1);
}
vél_Word 자바파일쓰기(vél_Word SLÓÐ,vél_Word VALUE){const char*strengur_gögn=(const char*)VALUE;unsigned vara_COUNT=lengd_VALUE(strengur_gögn);int skrá_hald=opið_skrá((const char*)SLÓÐ,쓰기전용|없으면만들기|내용비우기,0600);if(skrá_hald<0)자바실패();int 반환값=skrifa_skrá_gögn(skrá_hald,strengur_gögn,vara_COUNT);loka_skrá(skrá_hald);if(반환값!=(int)vara_COUNT)자바실패();return 0;}
vél_Word 자바파일읽기(vél_Word SLÓÐ){int skrá_hald=opið_skrá((const char*)SLÓÐ,skrifvarið_VALUE,0);if(skrá_hald<0)자바실패();int vara_COUNT=skrá_breyta_stærð(skrá_hald);if(vara_COUNT<0||vara_COUNT>16384||(unsigned)(vara_COUNT+8)/8>8192-사용량)자바실패();char*gögn_staða=(char*)(동적기억공간+사용량);사용량+=(vara_COUNT+8)/8;int 반환값=파일자료읽기(skrá_hald,gögn_staða,vara_COUNT);loka_skrá(skrá_hald);if(반환값!=vara_COUNT)자바실패();gögn_staða[vara_COUNT]=0;return (vél_Word)gögn_staða;}
