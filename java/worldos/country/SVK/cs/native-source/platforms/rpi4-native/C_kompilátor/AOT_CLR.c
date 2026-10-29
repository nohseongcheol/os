#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "Soubor_ABI.h"
typedef unsigned long počítač_Word;
static počítač_Word dynamická_paměť[8192];static unsigned 사용량;
void 자바실패(void){const char text[]="AOT runtime error\n";zápis_Soubor_data(2,text,sizeof(text)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(počítač_Word *paměť_zásobníku,int *깊이,počítač_Word HODNOTA){if(*깊이<0||*깊이>=128)자바실패();paměť_zásobníku[(*깊이)++]=HODNOTA;}
počítač_Word 자바꺼내기(počítač_Word *paměť_zásobníku,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return paměť_zásobníku[--*깊이];}
počítač_Word 자바배열(int zboží_POČET){if(zboží_POČET<0||(unsigned)zboží_POČET+1>8192-사용량)자바실패();počítač_Word*data_pozice=dynamická_paměť+사용량;사용량+=zboží_POČET+1;data_pozice[0]=zboží_POČET;return (počítač_Word)data_pozice;}
počítač_Word *자바색인(počítač_Word objekt_odkaz,int zboží_POČET){počítač_Word*data_pozice=(počítač_Word*)objekt_odkaz;if(!data_pozice||zboží_POČET<0||(počítač_Word)zboží_POČET>=data_pozice[0])자바실패();return data_pozice+zboží_POČET+1;}
int 자바길이(počítač_Word objekt_odkaz){if(!objekt_odkaz)자바실패();return *(počítač_Word*)objekt_odkaz;}
int 자바나누기(int souřadnice_x,int Y_souřadnice,int 나머지){if(!Y_souřadnice)자바실패();if(souřadnice_x==(-2147483647-1)&&Y_souřadnice==-1)return 나머지?0:souřadnice_x;return 나머지?souřadnice_x%Y_souřadnice:souřadnice_x/Y_souřadnice;}
static unsigned délka_HODNOTA(const char*řetězec_data){unsigned zboží_POČET=0;if(!řetězec_data)자바실패();while(řetězec_data[zboží_POČET])zboží_POČET++;return zboží_POČET;}
void 자바출력(počítač_Word data_pozice,int 수치,int 줄바꿈){
    if(수치){char SEKUNDA_HODNOTA[16];unsigned zboží_POČET=0;int HODNOTA=(int)data_pozice;unsigned 부호없는값=HODNOTA<0?0-(unsigned)HODNOTA:HODNOTA;do{SEKUNDA_HODNOTA[zboží_POČET++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(HODNOTA<0)SEKUNDA_HODNOTA[zboží_POČET++]='-';while(zboží_POČET)zápis_Soubor_data(1,SEKUNDA_HODNOTA+--zboží_POČET,1);}
    else{const char*řetězec_data=data_pozice?(const char*)data_pozice:"null";zápis_Soubor_data(1,řetězec_data,délka_HODNOTA(řetězec_data));}if(줄바꿈)zápis_Soubor_data(1,"\n",1);
}
počítač_Word 자바파일쓰기(počítač_Word cesta_2,počítač_Word HODNOTA){const char*řetězec_data=(const char*)HODNOTA;unsigned zboží_POČET=délka_HODNOTA(řetězec_data);int popisovač_souboru=otevřít_Soubor((const char*)cesta_2,쓰기전용|없으면만들기|stříhat_Obsah,0600);if(popisovač_souboru<0)자바실패();int 반환값=zápis_Soubor_data(popisovač_souboru,řetězec_data,zboží_POČET);Zavřít_Soubor(popisovač_souboru);if(반환값!=(int)zboží_POČET)자바실패();return 0;}
počítač_Word 자바파일읽기(počítač_Word cesta_2){int popisovač_souboru=otevřít_Soubor((const char*)cesta_2,jen_pro_čtení_HODNOTA,0);if(popisovač_souboru<0)자바실패();int zboží_POČET=velikost_souboru(popisovač_souboru);if(zboží_POČET<0||zboží_POČET>16384||(unsigned)(zboží_POČET+8)/8>8192-사용량)자바실패();char*data_pozice=(char*)(dynamická_paměť+사용량);사용량+=(zboží_POČET+8)/8;int 반환값=파일자료읽기(popisovač_souboru,data_pozice,zboží_POČET);Zavřít_Soubor(popisovač_souboru);if(반환값!=zboží_POČET)자바실패();data_pozice[zboží_POČET]=0;return (počítač_Word)data_pozice;}
