#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long makinë_Word;
static makinë_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Teksti[]="AOT runtime error\n";shkruaj_skedar_të_dhëna(2,Teksti,sizeof(Teksti)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(makinë_Word *Stivë_hapësira_ruajtëse,int *깊이,makinë_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();Stivë_hapësira_ruajtëse[(*깊이)++]=VALUE;}
makinë_Word 자바꺼내기(makinë_Word *Stivë_hapësira_ruajtëse,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Stivë_hapësira_ruajtëse[--*깊이];}
makinë_Word 자바배열(int njësi_COUNT){if(njësi_COUNT<0||(unsigned)njësi_COUNT+1>8192-사용량)자바실패();makinë_Word*të_dhëna_pozicioni=동적기억공간+사용량;사용량+=njësi_COUNT+1;të_dhëna_pozicioni[0]=njësi_COUNT;return (makinë_Word)të_dhëna_pozicioni;}
makinë_Word *자바색인(makinë_Word objekt_Referencë,int njësi_COUNT){makinë_Word*të_dhëna_pozicioni=(makinë_Word*)objekt_Referencë;if(!të_dhëna_pozicioni||njësi_COUNT<0||(makinë_Word)njësi_COUNT>=të_dhëna_pozicioni[0])자바실패();return të_dhëna_pozicioni+njësi_COUNT+1;}
int 자바길이(makinë_Word objekt_Referencë){if(!objekt_Referencë)자바실패();return *(makinë_Word*)objekt_Referencë;}
int 자바나누기(int koordinata_x,int Y_koordinatë,int 나머지){if(!Y_koordinatë)자바실패();if(koordinata_x==(-2147483647-1)&&Y_koordinatë==-1)return 나머지?0:koordinata_x;return 나머지?koordinata_x%Y_koordinatë:koordinata_x/Y_koordinatë;}
static unsigned gjatësi_VALUE(const char*varg_të_dhëna){unsigned njësi_COUNT=0;if(!varg_të_dhëna)자바실패();while(varg_të_dhëna[njësi_COUNT])njësi_COUNT++;return njësi_COUNT;}
void 자바출력(makinë_Word të_dhëna_pozicioni,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned njësi_COUNT=0;int VALUE=(int)të_dhëna_pozicioni;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[njësi_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[njësi_COUNT++]='-';while(njësi_COUNT)shkruaj_skedar_të_dhëna(1,SECOND_VALUE+--njësi_COUNT,1);}
    else{const char*varg_të_dhëna=të_dhëna_pozicioni?(const char*)të_dhëna_pozicioni:"null";shkruaj_skedar_të_dhëna(1,varg_të_dhëna,gjatësi_VALUE(varg_të_dhëna));}if(줄바꿈)shkruaj_skedar_të_dhëna(1,"\n",1);
}
makinë_Word 자바파일쓰기(makinë_Word POZICIONI,makinë_Word VALUE){const char*varg_të_dhëna=(const char*)VALUE;unsigned njësi_COUNT=gjatësi_VALUE(varg_të_dhëna);int skedar_dorezë=hap_skedar((const char*)POZICIONI,쓰기전용|없으면만들기|내용비우기,0600);if(skedar_dorezë<0)자바실패();int 반환값=shkruaj_skedar_të_dhëna(skedar_dorezë,varg_të_dhëna,njësi_COUNT);mbyll_skedar(skedar_dorezë);if(반환값!=(int)njësi_COUNT)자바실패();return 0;}
makinë_Word 자바파일읽기(makinë_Word POZICIONI){int skedar_dorezë=hap_skedar((const char*)POZICIONI,vetëm_për_lexim_VALUE,0);if(skedar_dorezë<0)자바실패();int njësi_COUNT=skedar_ndryshoj_përmasat(skedar_dorezë);if(njësi_COUNT<0||njësi_COUNT>16384||(unsigned)(njësi_COUNT+8)/8>8192-사용량)자바실패();char*të_dhëna_pozicioni=(char*)(동적기억공간+사용량);사용량+=(njësi_COUNT+8)/8;int 반환값=파일자료읽기(skedar_dorezë,të_dhëna_pozicioni,njësi_COUNT);mbyll_skedar(skedar_dorezë);if(반환값!=njësi_COUNT)자바실패();të_dhëna_pozicioni[njësi_COUNT]=0;return (makinë_Word)të_dhëna_pozicioni;}
