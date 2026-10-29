#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long maskin_ord;
static maskin_ord heap_lager[8192];static unsigned 사용량;
void 자바실패(void){const char Tekst[]="AOT runtime error\n";skrive_Fil_data(2,Tekst,sizeof(Tekst)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(maskin_ord *stakk_lager,int *깊이,maskin_ord VERDI){if(*깊이<0||*깊이>=128)자바실패();stakk_lager[(*깊이)++]=VERDI;}
maskin_ord 자바꺼내기(maskin_ord *stakk_lager,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return stakk_lager[--*깊이];}
maskin_ord 자바배열(int vare_ANTALL){if(vare_ANTALL<0||(unsigned)vare_ANTALL+1>8192-사용량)자바실패();maskin_ord*data_plassere=heap_lager+사용량;사용량+=vare_ANTALL+1;data_plassere[0]=vare_ANTALL;return (maskin_ord)data_plassere;}
maskin_ord *자바색인(maskin_ord objekt_referere,int vare_ANTALL){maskin_ord*data_plassere=(maskin_ord*)objekt_referere;if(!data_plassere||vare_ANTALL<0||(maskin_ord)vare_ANTALL>=data_plassere[0])자바실패();return data_plassere+vare_ANTALL+1;}
int 자바길이(maskin_ord objekt_referere){if(!objekt_referere)자바실패();return *(maskin_ord*)objekt_referere;}
int 자바나누기(int x_koordinat,int Y_koordinat,int 나머지){if(!Y_koordinat)자바실패();if(x_koordinat==(-2147483647-1)&&Y_koordinat==-1)return 나머지?0:x_koordinat;return 나머지?x_koordinat%Y_koordinat:x_koordinat/Y_koordinat;}
static unsigned lengde_VERDI(const char*streng_data){unsigned vare_ANTALL=0;if(!streng_data)자바실패();while(streng_data[vare_ANTALL])vare_ANTALL++;return vare_ANTALL;}
void 자바출력(maskin_ord data_plassere,int 수치,int 줄바꿈){
    if(수치){char SEKUND_VERDI[16];unsigned vare_ANTALL=0;int VERDI=(int)data_plassere;unsigned 부호없는값=VERDI<0?0-(unsigned)VERDI:VERDI;do{SEKUND_VERDI[vare_ANTALL++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VERDI<0)SEKUND_VERDI[vare_ANTALL++]='-';while(vare_ANTALL)skrive_Fil_data(1,SEKUND_VERDI+--vare_ANTALL,1);}
    else{const char*streng_data=data_plassere?(const char*)data_plassere:"null";skrive_Fil_data(1,streng_data,lengde_VERDI(streng_data));}if(줄바꿈)skrive_Fil_data(1,"\n",1);
}
maskin_ord 자바파일쓰기(maskin_ord Sti,maskin_ord VERDI){const char*streng_data=(const char*)VERDI;unsigned vare_ANTALL=lengde_VERDI(streng_data);int Fil_håndtak=åpen_Fil((const char*)Sti,쓰기전용|없으면만들기|avkorte_Innhold,0600);if(Fil_håndtak<0)자바실패();int 반환값=skrive_Fil_data(Fil_håndtak,streng_data,vare_ANTALL);Lukk_Fil(Fil_håndtak);if(반환값!=(int)vare_ANTALL)자바실패();return 0;}
maskin_ord 자바파일읽기(maskin_ord Sti){int Fil_håndtak=åpen_Fil((const char*)Sti,skrivebeskyttet_VERDI,0);if(Fil_håndtak<0)자바실패();int vare_ANTALL=filstørrelse(Fil_håndtak);if(vare_ANTALL<0||vare_ANTALL>16384||(unsigned)(vare_ANTALL+8)/8>8192-사용량)자바실패();char*data_plassere=(char*)(heap_lager+사용량);사용량+=(vare_ANTALL+8)/8;int 반환값=파일자료읽기(Fil_håndtak,data_plassere,vare_ANTALL);Lukk_Fil(Fil_håndtak);if(반환값!=vare_ANTALL)자바실패();data_plassere[vare_ANTALL]=0;return (maskin_ord)data_plassere;}
