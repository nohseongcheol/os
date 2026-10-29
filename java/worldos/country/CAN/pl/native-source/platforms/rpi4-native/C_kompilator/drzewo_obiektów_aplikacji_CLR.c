#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "Plik_ABI.h"
typedef unsigned long maszyna_Word;
static maszyna_Word pamięć_dynamiczna[8192];static unsigned 사용량;
void 자바실패(void){const char tekst[]="AOT runtime error\n";zapis_Plik_dane(2,tekst,sizeof(tekst)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(maszyna_Word *pamięć_stosu,int *깊이,maszyna_Word WARTOŚĆ){if(*깊이<0||*깊이>=128)자바실패();pamięć_stosu[(*깊이)++]=WARTOŚĆ;}
maszyna_Word 자바꺼내기(maszyna_Word *pamięć_stosu,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return pamięć_stosu[--*깊이];}
maszyna_Word 자바배열(int towar_ILE_LICZB){if(towar_ILE_LICZB<0||(unsigned)towar_ILE_LICZB+1>8192-사용량)자바실패();maszyna_Word*dane_stanowisko=pamięć_dynamiczna+사용량;사용량+=towar_ILE_LICZB+1;dane_stanowisko[0]=towar_ILE_LICZB;return (maszyna_Word)dane_stanowisko;}
maszyna_Word *자바색인(maszyna_Word obiekt_odwołanie,int towar_ILE_LICZB){maszyna_Word*dane_stanowisko=(maszyna_Word*)obiekt_odwołanie;if(!dane_stanowisko||towar_ILE_LICZB<0||(maszyna_Word)towar_ILE_LICZB>=dane_stanowisko[0])자바실패();return dane_stanowisko+towar_ILE_LICZB+1;}
int 자바길이(maszyna_Word obiekt_odwołanie){if(!obiekt_odwołanie)자바실패();return *(maszyna_Word*)obiekt_odwołanie;}
int 자바나누기(int współrzędna_X,int Y_współrzędna,int 나머지){if(!Y_współrzędna)자바실패();if(współrzędna_X==(-2147483647-1)&&Y_współrzędna==-1)return 나머지?0:współrzędna_X;return 나머지?współrzędna_X%Y_współrzędna:współrzędna_X/Y_współrzędna;}
static unsigned długość_WARTOŚĆ(const char*ciąg_dane){unsigned towar_ILE_LICZB=0;if(!ciąg_dane)자바실패();while(ciąg_dane[towar_ILE_LICZB])towar_ILE_LICZB++;return towar_ILE_LICZB;}
void 자바출력(maszyna_Word dane_stanowisko,int 수치,int 줄바꿈){
    if(수치){char SEKUNDA_WARTOŚĆ[16];unsigned towar_ILE_LICZB=0;int WARTOŚĆ=(int)dane_stanowisko;unsigned 부호없는값=WARTOŚĆ<0?0-(unsigned)WARTOŚĆ:WARTOŚĆ;do{SEKUNDA_WARTOŚĆ[towar_ILE_LICZB++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(WARTOŚĆ<0)SEKUNDA_WARTOŚĆ[towar_ILE_LICZB++]='-';while(towar_ILE_LICZB)zapis_Plik_dane(1,SEKUNDA_WARTOŚĆ+--towar_ILE_LICZB,1);}
    else{const char*ciąg_dane=dane_stanowisko?(const char*)dane_stanowisko:"null";zapis_Plik_dane(1,ciąg_dane,długość_WARTOŚĆ(ciąg_dane));}if(줄바꿈)zapis_Plik_dane(1,"\n",1);
}
maszyna_Word 자바파일쓰기(maszyna_Word ścieżka_2,maszyna_Word WARTOŚĆ){const char*ciąg_dane=(const char*)WARTOŚĆ;unsigned towar_ILE_LICZB=długość_WARTOŚĆ(ciąg_dane);int dojście_do_pliku=otwarty_Plik((const char*)ścieżka_2,tylko_do_zapisu_WARTOŚĆ|없으면만들기|obcinać_Spis_treści,0600);if(dojście_do_pliku<0)자바실패();int 반환값=zapis_Plik_dane(dojście_do_pliku,ciąg_dane,towar_ILE_LICZB);Zamknij_Plik(dojście_do_pliku);if(반환값!=(int)towar_ILE_LICZB)자바실패();return 0;}
maszyna_Word 자바파일읽기(maszyna_Word ścieżka_2){int dojście_do_pliku=otwarty_Plik((const char*)ścieżka_2,tylko_do_odczytu_WARTOŚĆ,0);if(dojście_do_pliku<0)자바실패();int towar_ILE_LICZB=rozmiar_pliku(dojście_do_pliku);if(towar_ILE_LICZB<0||towar_ILE_LICZB>16384||(unsigned)(towar_ILE_LICZB+8)/8>8192-사용량)자바실패();char*dane_stanowisko=(char*)(pamięć_dynamiczna+사용량);사용량+=(towar_ILE_LICZB+8)/8;int 반환값=파일자료읽기(dojście_do_pliku,dane_stanowisko,towar_ILE_LICZB);Zamknij_Plik(dojście_do_pliku);if(반환값!=towar_ILE_LICZB)자바실패();dane_stanowisko[towar_ILE_LICZB]=0;return (maszyna_Word)dane_stanowisko;}
