#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long kone_Word;
static kone_Word dynaaminen_muisti[8192];static unsigned 사용량;
void 자바실패(void){const char teksti[]="AOT runtime error\n";kirjoitus_Tiedosto_data(2,teksti,sizeof(teksti)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(kone_Word *pinomuisti,int *깊이,kone_Word ARVO){if(*깊이<0||*깊이>=128)자바실패();pinomuisti[(*깊이)++]=ARVO;}
kone_Word 자바꺼내기(kone_Word *pinomuisti,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return pinomuisti[--*깊이];}
kone_Word 자바배열(int kohde_LASKE){if(kohde_LASKE<0||(unsigned)kohde_LASKE+1>8192-사용량)자바실패();kone_Word*data_toimi=dynaaminen_muisti+사용량;사용량+=kohde_LASKE+1;data_toimi[0]=kohde_LASKE;return (kone_Word)data_toimi;}
kone_Word *자바색인(kone_Word objekti_viite,int kohde_LASKE){kone_Word*data_toimi=(kone_Word*)objekti_viite;if(!data_toimi||kohde_LASKE<0||(kone_Word)kohde_LASKE>=data_toimi[0])자바실패();return data_toimi+kohde_LASKE+1;}
int 자바길이(kone_Word objekti_viite){if(!objekti_viite)자바실패();return *(kone_Word*)objekti_viite;}
int 자바나누기(int x_koordinaatti,int Y_koordinaatti,int 나머지){if(!Y_koordinaatti)자바실패();if(x_koordinaatti==(-2147483647-1)&&Y_koordinaatti==-1)return 나머지?0:x_koordinaatti;return 나머지?x_koordinaatti%Y_koordinaatti:x_koordinaatti/Y_koordinaatti;}
static unsigned kesto_ARVO(const char*merkkijono_data){unsigned kohde_LASKE=0;if(!merkkijono_data)자바실패();while(merkkijono_data[kohde_LASKE])kohde_LASKE++;return kohde_LASKE;}
void 자바출력(kone_Word data_toimi,int 수치,int 줄바꿈){
    if(수치){char SEKUNNIT_ARVO[16];unsigned kohde_LASKE=0;int ARVO=(int)data_toimi;unsigned 부호없는값=ARVO<0?0-(unsigned)ARVO:ARVO;do{SEKUNNIT_ARVO[kohde_LASKE++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(ARVO<0)SEKUNNIT_ARVO[kohde_LASKE++]='-';while(kohde_LASKE)kirjoitus_Tiedosto_data(1,SEKUNNIT_ARVO+--kohde_LASKE,1);}
    else{const char*merkkijono_data=data_toimi?(const char*)data_toimi:"null";kirjoitus_Tiedosto_data(1,merkkijono_data,kesto_ARVO(merkkijono_data));}if(줄바꿈)kirjoitus_Tiedosto_data(1,"\n",1);
}
kone_Word 자바파일쓰기(kone_Word polku_2,kone_Word ARVO){const char*merkkijono_data=(const char*)ARVO;unsigned kohde_LASKE=kesto_ARVO(merkkijono_data);int Tiedosto_kahva=avata_Tiedosto((const char*)polku_2,쓰기전용|없으면만들기|내용비우기,0600);if(Tiedosto_kahva<0)자바실패();int 반환값=kirjoitus_Tiedosto_data(Tiedosto_kahva,merkkijono_data,kohde_LASKE);Sulje_Tiedosto(Tiedosto_kahva);if(반환값!=(int)kohde_LASKE)자바실패();return 0;}
kone_Word 자바파일읽기(kone_Word polku_2){int Tiedosto_kahva=avata_Tiedosto((const char*)polku_2,vain_luku_ARVO,0);if(Tiedosto_kahva<0)자바실패();int kohde_LASKE=tiedostokoko(Tiedosto_kahva);if(kohde_LASKE<0||kohde_LASKE>16384||(unsigned)(kohde_LASKE+8)/8>8192-사용량)자바실패();char*data_toimi=(char*)(dynaaminen_muisti+사용량);사용량+=(kohde_LASKE+8)/8;int 반환값=lukea_Tiedosto_data(Tiedosto_kahva,data_toimi,kohde_LASKE);Sulje_Tiedosto(Tiedosto_kahva);if(반환값!=kohde_LASKE)자바실패();data_toimi[kohde_LASKE]=0;return (kone_Word)data_toimi;}
