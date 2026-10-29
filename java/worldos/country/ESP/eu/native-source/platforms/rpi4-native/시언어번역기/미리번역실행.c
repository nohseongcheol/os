#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long gailu_Word;
static gailu_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Testua[]="AOT runtime error\n";idatzi_fitxategi_datuak(2,Testua,sizeof(Testua)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(gailu_Word *pila_biltegi,int *깊이,gailu_Word balio){if(*깊이<0||*깊이>=128)자바실패();pila_biltegi[(*깊이)++]=balio;}
gailu_Word 자바꺼내기(gailu_Word *pila_biltegi,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return pila_biltegi[--*깊이];}
gailu_Word 자바배열(int elementu_ZENBATU){if(elementu_ZENBATU<0||(unsigned)elementu_ZENBATU+1>8192-사용량)자바실패();gailu_Word*datuak_kargu=동적기억공간+사용량;사용량+=elementu_ZENBATU+1;datuak_kargu[0]=elementu_ZENBATU;return (gailu_Word)datuak_kargu;}
gailu_Word *자바색인(gailu_Word objektu_Erreferentzia_materiala,int elementu_ZENBATU){gailu_Word*datuak_kargu=(gailu_Word*)objektu_Erreferentzia_materiala;if(!datuak_kargu||elementu_ZENBATU<0||(gailu_Word)elementu_ZENBATU>=datuak_kargu[0])자바실패();return datuak_kargu+elementu_ZENBATU+1;}
int 자바길이(gailu_Word objektu_Erreferentzia_materiala){if(!objektu_Erreferentzia_materiala)자바실패();return *(gailu_Word*)objektu_Erreferentzia_materiala;}
int 자바나누기(int X_koordenatu,int Y_koordenatu,int 나머지){if(!Y_koordenatu)자바실패();if(X_koordenatu==(-2147483647-1)&&Y_koordenatu==-1)return 나머지?0:X_koordenatu;return 나머지?X_koordenatu%Y_koordenatu:X_koordenatu/Y_koordenatu;}
static unsigned luzera_balio(const char*kate_datuak){unsigned elementu_ZENBATU=0;if(!kate_datuak)자바실패();while(kate_datuak[elementu_ZENBATU])elementu_ZENBATU++;return elementu_ZENBATU;}
void 자바출력(gailu_Word datuak_kargu,int 수치,int 줄바꿈){
    if(수치){char SEGUNDOA_balio[16];unsigned elementu_ZENBATU=0;int balio=(int)datuak_kargu;unsigned 부호없는값=balio<0?0-(unsigned)balio:balio;do{SEGUNDOA_balio[elementu_ZENBATU++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(balio<0)SEGUNDOA_balio[elementu_ZENBATU++]='-';while(elementu_ZENBATU)idatzi_fitxategi_datuak(1,SEGUNDOA_balio+--elementu_ZENBATU,1);}
    else{const char*kate_datuak=datuak_kargu?(const char*)datuak_kargu:"null";idatzi_fitxategi_datuak(1,kate_datuak,luzera_balio(kate_datuak));}if(줄바꿈)idatzi_fitxategi_datuak(1,"\n",1);
}
gailu_Word 자바파일쓰기(gailu_Word Bide_izena,gailu_Word balio){const char*kate_datuak=(const char*)balio;unsigned elementu_ZENBATU=luzera_balio(kate_datuak);int fitxategi_helduleku=ireki_fitxategi((const char*)Bide_izena,쓰기전용|없으면만들기|내용비우기,0600);if(fitxategi_helduleku<0)자바실패();int 반환값=idatzi_fitxategi_datuak(fitxategi_helduleku,kate_datuak,elementu_ZENBATU);itxi_fitxategi(fitxategi_helduleku);if(반환값!=(int)elementu_ZENBATU)자바실패();return 0;}
gailu_Word 자바파일읽기(gailu_Word Bide_izena){int fitxategi_helduleku=ireki_fitxategi((const char*)Bide_izena,irakurtzeko_soilik_balio,0);if(fitxategi_helduleku<0)자바실패();int elementu_ZENBATU=파일크기(fitxategi_helduleku);if(elementu_ZENBATU<0||elementu_ZENBATU>16384||(unsigned)(elementu_ZENBATU+8)/8>8192-사용량)자바실패();char*datuak_kargu=(char*)(동적기억공간+사용량);사용량+=(elementu_ZENBATU+8)/8;int 반환값=파일자료읽기(fitxategi_helduleku,datuak_kargu,elementu_ZENBATU);itxi_fitxategi(fitxategi_helduleku);if(반환값!=elementu_ZENBATU)자바실패();datuak_kargu[elementu_ZENBATU]=0;return (gailu_Word)datuak_kargu;}
