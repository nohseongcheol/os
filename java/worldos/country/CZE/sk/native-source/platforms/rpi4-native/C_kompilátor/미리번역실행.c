#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long počítač_Word;
static počítač_Word halda_Úložisko[8192];static unsigned 사용량;
void 자바실패(void){const char Spracovanie_textu[]="AOT runtime error\n";zapísať_Súbor_údaje(2,Spracovanie_textu,sizeof(Spracovanie_textu)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(počítač_Word *Vrstvy_Úložisko,int *깊이,počítač_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();Vrstvy_Úložisko[(*깊이)++]=VALUE;}
počítač_Word 자바꺼내기(počítač_Word *Vrstvy_Úložisko,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Vrstvy_Úložisko[--*깊이];}
počítač_Word 자바배열(int položka_COUNT){if(položka_COUNT<0||(unsigned)položka_COUNT+1>8192-사용량)자바실패();počítač_Word*údaje_pozícia=halda_Úložisko+사용량;사용량+=položka_COUNT+1;údaje_pozícia[0]=položka_COUNT;return (počítač_Word)údaje_pozícia;}
počítač_Word *자바색인(počítač_Word objekt_zdroj,int položka_COUNT){počítač_Word*údaje_pozícia=(počítač_Word*)objekt_zdroj;if(!údaje_pozícia||položka_COUNT<0||(počítač_Word)položka_COUNT>=údaje_pozícia[0])자바실패();return údaje_pozícia+položka_COUNT+1;}
int 자바길이(počítač_Word objekt_zdroj){if(!objekt_zdroj)자바실패();return *(počítač_Word*)objekt_zdroj;}
int 자바나누기(int X_súradnica,int Y_súradnica,int 나머지){if(!Y_súradnica)자바실패();if(X_súradnica==(-2147483647-1)&&Y_súradnica==-1)return 나머지?0:X_súradnica;return 나머지?X_súradnica%Y_súradnica:X_súradnica/Y_súradnica;}
static unsigned dĺžka_VALUE(const char*reťazec_údaje){unsigned položka_COUNT=0;if(!reťazec_údaje)자바실패();while(reťazec_údaje[položka_COUNT])položka_COUNT++;return položka_COUNT;}
void 자바출력(počítač_Word údaje_pozícia,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned položka_COUNT=0;int VALUE=(int)údaje_pozícia;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[položka_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[položka_COUNT++]='-';while(položka_COUNT)zapísať_Súbor_údaje(1,SECOND_VALUE+--položka_COUNT,1);}
    else{const char*reťazec_údaje=údaje_pozícia?(const char*)údaje_pozícia:"null";zapísať_Súbor_údaje(1,reťazec_údaje,dĺžka_VALUE(reťazec_údaje));}if(줄바꿈)zapísať_Súbor_údaje(1,"\n",1);
}
počítač_Word 자바파일쓰기(počítač_Word Cesta,počítač_Word VALUE){const char*reťazec_údaje=(const char*)VALUE;unsigned položka_COUNT=dĺžka_VALUE(reťazec_údaje);int Súbor_rukoväť=otvoriť_Súbor((const char*)Cesta,쓰기전용|없으면만들기|skrátiť_Obsah,0600);if(Súbor_rukoväť<0)자바실패();int 반환값=zapísať_Súbor_údaje(Súbor_rukoväť,reťazec_údaje,položka_COUNT);Zavrieť_Súbor(Súbor_rukoväť);if(반환값!=(int)položka_COUNT)자바실패();return 0;}
počítač_Word 자바파일읽기(počítač_Word Cesta){int Súbor_rukoväť=otvoriť_Súbor((const char*)Cesta,iba_na_čítanie_VALUE,0);if(Súbor_rukoväť<0)자바실패();int položka_COUNT=veľkosť_súboru(Súbor_rukoväť);if(položka_COUNT<0||položka_COUNT>16384||(unsigned)(položka_COUNT+8)/8>8192-사용량)자바실패();char*údaje_pozícia=(char*)(halda_Úložisko+사용량);사용량+=(položka_COUNT+8)/8;int 반환값=파일자료읽기(Súbor_rukoväť,údaje_pozícia,položka_COUNT);Zavrieť_Súbor(Súbor_rukoväť);if(반환값!=položka_COUNT)자바실패();údaje_pozícia[položka_COUNT]=0;return (počítač_Word)údaje_pozícia;}
