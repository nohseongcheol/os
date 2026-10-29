#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long gép_szó;
static gép_szó halommemória_tár[8192];static unsigned 사용량;
void 자바실패(void){const char Szöveg[]="AOT runtime error\n";ír_Fájl_adat(2,Szöveg,sizeof(Szöveg)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(gép_szó *Sor_tár,int *깊이,gép_szó ÉRTÉK){if(*깊이<0||*깊이>=128)자바실패();Sor_tár[(*깊이)++]=ÉRTÉK;}
gép_szó 자바꺼내기(gép_szó *Sor_tár,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Sor_tár[--*깊이];}
gép_szó 자바배열(int cikk_DARAB){if(cikk_DARAB<0||(unsigned)cikk_DARAB+1>8192-사용량)자바실패();gép_szó*adat_pozíció=halommemória_tár+사용량;사용량+=cikk_DARAB+1;adat_pozíció[0]=cikk_DARAB;return (gép_szó)adat_pozíció;}
gép_szó *자바색인(gép_szó objektum_hivatkozik,int cikk_DARAB){gép_szó*adat_pozíció=(gép_szó*)objektum_hivatkozik;if(!adat_pozíció||cikk_DARAB<0||(gép_szó)cikk_DARAB>=adat_pozíció[0])자바실패();return adat_pozíció+cikk_DARAB+1;}
int 자바길이(gép_szó objektum_hivatkozik){if(!objektum_hivatkozik)자바실패();return *(gép_szó*)objektum_hivatkozik;}
int 자바나누기(int x_koordináta,int Y_koordináta,int 나머지){if(!Y_koordináta)자바실패();if(x_koordináta==(-2147483647-1)&&Y_koordináta==-1)return 나머지?0:x_koordináta;return 나머지?x_koordináta%Y_koordináta:x_koordináta/Y_koordináta;}
static unsigned hossz_ÉRTÉK(const char*sztring_adat){unsigned cikk_DARAB=0;if(!sztring_adat)자바실패();while(sztring_adat[cikk_DARAB])cikk_DARAB++;return cikk_DARAB;}
void 자바출력(gép_szó adat_pozíció,int 수치,int 줄바꿈){
    if(수치){char MPERC_ÉRTÉK[16];unsigned cikk_DARAB=0;int ÉRTÉK=(int)adat_pozíció;unsigned 부호없는값=ÉRTÉK<0?0-(unsigned)ÉRTÉK:ÉRTÉK;do{MPERC_ÉRTÉK[cikk_DARAB++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(ÉRTÉK<0)MPERC_ÉRTÉK[cikk_DARAB++]='-';while(cikk_DARAB)ír_Fájl_adat(1,MPERC_ÉRTÉK+--cikk_DARAB,1);}
    else{const char*sztring_adat=adat_pozíció?(const char*)adat_pozíció:"null";ír_Fájl_adat(1,sztring_adat,hossz_ÉRTÉK(sztring_adat));}if(줄바꿈)ír_Fájl_adat(1,"\n",1);
}
gép_szó 자바파일쓰기(gép_szó ÚTVONAL,gép_szó ÉRTÉK){const char*sztring_adat=(const char*)ÉRTÉK;unsigned cikk_DARAB=hossz_ÉRTÉK(sztring_adat);int fájlleíró=készít_Fájl((const char*)ÚTVONAL,쓰기전용|없으면만들기|vág_Tartalom,0600);if(fájlleíró<0)자바실패();int 반환값=ír_Fájl_adat(fájlleíró,sztring_adat,cikk_DARAB);bezár_Fájl(fájlleíró);if(반환값!=(int)cikk_DARAB)자바실패();return 0;}
gép_szó 자바파일읽기(gép_szó ÚTVONAL){int fájlleíró=készít_Fájl((const char*)ÚTVONAL,írásvédett_ÉRTÉK,0);if(fájlleíró<0)자바실패();int cikk_DARAB=fájlméret(fájlleíró);if(cikk_DARAB<0||cikk_DARAB>16384||(unsigned)(cikk_DARAB+8)/8>8192-사용량)자바실패();char*adat_pozíció=(char*)(halommemória_tár+사용량);사용량+=(cikk_DARAB+8)/8;int 반환값=파일자료읽기(fájlleíró,adat_pozíció,cikk_DARAB);bezár_Fájl(fájlleíró);if(반환값!=cikk_DARAB)자바실패();adat_pozíció[cikk_DARAB]=0;return (gép_szó)adat_pozíció;}
