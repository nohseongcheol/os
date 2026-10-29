#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long machine_Word;
static machine_Word dynamisch_geheugen[8192];static unsigned 사용량;
void 자바실패(void){const char tekst[]="AOT runtime error\n";schrijven_Bestand_gegevens(2,tekst,sizeof(tekst)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(machine_Word *stapelgeheugen,int *깊이,machine_Word WAARDE){if(*깊이<0||*깊이>=128)자바실패();stapelgeheugen[(*깊이)++]=WAARDE;}
machine_Word 자바꺼내기(machine_Word *stapelgeheugen,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return stapelgeheugen[--*깊이];}
machine_Word 자바배열(int item_AANTAL){if(item_AANTAL<0||(unsigned)item_AANTAL+1>8192-사용량)자바실패();machine_Word*gegevens_functie=dynamisch_geheugen+사용량;사용량+=item_AANTAL+1;gegevens_functie[0]=item_AANTAL;return (machine_Word)gegevens_functie;}
machine_Word *자바색인(machine_Word object_verwijzen,int item_AANTAL){machine_Word*gegevens_functie=(machine_Word*)object_verwijzen;if(!gegevens_functie||item_AANTAL<0||(machine_Word)item_AANTAL>=gegevens_functie[0])자바실패();return gegevens_functie+item_AANTAL+1;}
int 자바길이(machine_Word object_verwijzen){if(!object_verwijzen)자바실패();return *(machine_Word*)object_verwijzen;}
int 자바나누기(int x_coördinaat,int Y_coördinaat,int 나머지){if(!Y_coördinaat)자바실패();if(x_coördinaat==(-2147483647-1)&&Y_coördinaat==-1)return 나머지?0:x_coördinaat;return 나머지?x_coördinaat%Y_coördinaat:x_coördinaat/Y_coördinaat;}
static unsigned tijdsduur_WAARDE(const char*tekenreeks_gegevens){unsigned item_AANTAL=0;if(!tekenreeks_gegevens)자바실패();while(tekenreeks_gegevens[item_AANTAL])item_AANTAL++;return item_AANTAL;}
void 자바출력(machine_Word gegevens_functie,int 수치,int 줄바꿈){
    if(수치){char SECONDE_WAARDE[16];unsigned item_AANTAL=0;int WAARDE=(int)gegevens_functie;unsigned 부호없는값=WAARDE<0?0-(unsigned)WAARDE:WAARDE;do{SECONDE_WAARDE[item_AANTAL++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(WAARDE<0)SECONDE_WAARDE[item_AANTAL++]='-';while(item_AANTAL)schrijven_Bestand_gegevens(1,SECONDE_WAARDE+--item_AANTAL,1);}
    else{const char*tekenreeks_gegevens=gegevens_functie?(const char*)gegevens_functie:"null";schrijven_Bestand_gegevens(1,tekenreeks_gegevens,tijdsduur_WAARDE(tekenreeks_gegevens));}if(줄바꿈)schrijven_Bestand_gegevens(1,"\n",1);
}
machine_Word 자바파일쓰기(machine_Word pad,machine_Word WAARDE){const char*tekenreeks_gegevens=(const char*)WAARDE;unsigned item_AANTAL=tijdsduur_WAARDE(tekenreeks_gegevens);int bestandsingang=open_Bestand((const char*)pad,쓰기전용|없으면만들기|afkappen_Inhoud,0600);if(bestandsingang<0)자바실패();int 반환값=schrijven_Bestand_gegevens(bestandsingang,tekenreeks_gegevens,item_AANTAL);Sluiten_Bestand(bestandsingang);if(반환값!=(int)item_AANTAL)자바실패();return 0;}
machine_Word 자바파일읽기(machine_Word pad){int bestandsingang=open_Bestand((const char*)pad,alleen_lezen_WAARDE,0);if(bestandsingang<0)자바실패();int item_AANTAL=bestandsgrootte(bestandsingang);if(item_AANTAL<0||item_AANTAL>16384||(unsigned)(item_AANTAL+8)/8>8192-사용량)자바실패();char*gegevens_functie=(char*)(dynamisch_geheugen+사용량);사용량+=(item_AANTAL+8)/8;int 반환값=파일자료읽기(bestandsingang,gegevens_functie,item_AANTAL);Sluiten_Bestand(bestandsingang);if(반환값!=item_AANTAL)자바실패();gegevens_functie[item_AANTAL]=0;return (machine_Word)gegevens_functie;}
