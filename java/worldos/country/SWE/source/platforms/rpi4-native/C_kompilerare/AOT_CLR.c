#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long dator_Ord;
static dator_Ord dynamiskt_minne[8192];static unsigned 사용량;
void 자바실패(void){const char text[]="AOT runtime error\n";skriva_fil_data(2,text,sizeof(text)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(dator_Ord *stackminne,int *깊이,dator_Ord värde){if(*깊이<0||*깊이>=128)자바실패();stackminne[(*깊이)++]=värde;}
dator_Ord 자바꺼내기(dator_Ord *stackminne,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return stackminne[--*깊이];}
dator_Ord 자바배열(int objekt_ANTAL){if(objekt_ANTAL<0||(unsigned)objekt_ANTAL+1>8192-사용량)자바실패();dator_Ord*data_placera=dynamiskt_minne+사용량;사용량+=objekt_ANTAL+1;data_placera[0]=objekt_ANTAL;return (dator_Ord)data_placera;}
dator_Ord *자바색인(dator_Ord objekt_referens,int objekt_ANTAL){dator_Ord*data_placera=(dator_Ord*)objekt_referens;if(!data_placera||objekt_ANTAL<0||(dator_Ord)objekt_ANTAL>=data_placera[0])자바실패();return data_placera+objekt_ANTAL+1;}
int 자바길이(dator_Ord objekt_referens){if(!objekt_referens)자바실패();return *(dator_Ord*)objekt_referens;}
int 자바나누기(int x_koordinat,int Y_koordinat,int 나머지){if(!Y_koordinat)자바실패();if(x_koordinat==(-2147483647-1)&&Y_koordinat==-1)return 나머지?0:x_koordinat;return 나머지?x_koordinat%Y_koordinat:x_koordinat/Y_koordinat;}
static unsigned längd_värde(const char*sträng_data){unsigned objekt_ANTAL=0;if(!sträng_data)자바실패();while(sträng_data[objekt_ANTAL])objekt_ANTAL++;return objekt_ANTAL;}
void 자바출력(dator_Ord data_placera,int 수치,int 줄바꿈){
    if(수치){char SEKUND_värde[16];unsigned objekt_ANTAL=0;int värde=(int)data_placera;unsigned 부호없는값=värde<0?0-(unsigned)värde:värde;do{SEKUND_värde[objekt_ANTAL++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(värde<0)SEKUND_värde[objekt_ANTAL++]='-';while(objekt_ANTAL)skriva_fil_data(1,SEKUND_värde+--objekt_ANTAL,1);}
    else{const char*sträng_data=data_placera?(const char*)data_placera:"null";skriva_fil_data(1,sträng_data,längd_värde(sträng_data));}if(줄바꿈)skriva_fil_data(1,"\n",1);
}
dator_Ord 자바파일쓰기(dator_Ord sökväg_2,dator_Ord värde){const char*sträng_data=(const char*)värde;unsigned objekt_ANTAL=längd_värde(sträng_data);int filreferens=skapa_fil((const char*)sökväg_2,쓰기전용|없으면만들기|trimma_Innehåll,0600);if(filreferens<0)자바실패();int 반환값=skriva_fil_data(filreferens,sträng_data,objekt_ANTAL);Stäng_fil(filreferens);if(반환값!=(int)objekt_ANTAL)자바실패();return 0;}
dator_Ord 자바파일읽기(dator_Ord sökväg_2){int filreferens=skapa_fil((const char*)sökväg_2,skrivskyddad_värde,0);if(filreferens<0)자바실패();int objekt_ANTAL=filstorlek(filreferens);if(objekt_ANTAL<0||objekt_ANTAL>16384||(unsigned)(objekt_ANTAL+8)/8>8192-사용량)자바실패();char*data_placera=(char*)(dynamiskt_minne+사용량);사용량+=(objekt_ANTAL+8)/8;int 반환값=läsa_fil_data(filreferens,data_placera,objekt_ANTAL);Stäng_fil(filreferens);if(반환값!=objekt_ANTAL)자바실패();data_placera[objekt_ANTAL]=0;return (dator_Ord)data_placera;}
