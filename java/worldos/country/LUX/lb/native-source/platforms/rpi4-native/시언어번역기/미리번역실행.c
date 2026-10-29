#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long Computer_Word;
static Computer_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char SMS[]="AOT runtime error\n";schreiwen_Fichier_Daten(2,SMS,sizeof(SMS)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(Computer_Word *Stapel_Späicher,int *깊이,Computer_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();Stapel_Späicher[(*깊이)++]=VALUE;}
Computer_Word 자바꺼내기(Computer_Word *Stapel_Späicher,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Stapel_Späicher[--*깊이];}
Computer_Word 자바배열(int Element_COUNT){if(Element_COUNT<0||(unsigned)Element_COUNT+1>8192-사용량)자바실패();Computer_Word*Daten_positionéieren=동적기억공간+사용량;사용량+=Element_COUNT+1;Daten_positionéieren[0]=Element_COUNT;return (Computer_Word)Daten_positionéieren;}
Computer_Word *자바색인(Computer_Word Objet_Referenzen,int Element_COUNT){Computer_Word*Daten_positionéieren=(Computer_Word*)Objet_Referenzen;if(!Daten_positionéieren||Element_COUNT<0||(Computer_Word)Element_COUNT>=Daten_positionéieren[0])자바실패();return Daten_positionéieren+Element_COUNT+1;}
int 자바길이(Computer_Word Objet_Referenzen){if(!Objet_Referenzen)자바실패();return *(Computer_Word*)Objet_Referenzen;}
int 자바나누기(int X_Koordinat,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(X_Koordinat==(-2147483647-1)&&세로좌표==-1)return 나머지?0:X_Koordinat;return 나머지?X_Koordinat%세로좌표:X_Koordinat/세로좌표;}
static unsigned Längt_VALUE(const char*Zeechefolleg_Daten){unsigned Element_COUNT=0;if(!Zeechefolleg_Daten)자바실패();while(Zeechefolleg_Daten[Element_COUNT])Element_COUNT++;return Element_COUNT;}
void 자바출력(Computer_Word Daten_positionéieren,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned Element_COUNT=0;int VALUE=(int)Daten_positionéieren;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[Element_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[Element_COUNT++]='-';while(Element_COUNT)schreiwen_Fichier_Daten(1,SECOND_VALUE+--Element_COUNT,1);}
    else{const char*Zeechefolleg_Daten=Daten_positionéieren?(const char*)Daten_positionéieren:"null";schreiwen_Fichier_Daten(1,Zeechefolleg_Daten,Längt_VALUE(Zeechefolleg_Daten));}if(줄바꿈)schreiwen_Fichier_Daten(1,"\n",1);
}
Computer_Word 자바파일쓰기(Computer_Word Wee,Computer_Word VALUE){const char*Zeechefolleg_Daten=(const char*)VALUE;unsigned Element_COUNT=Längt_VALUE(Zeechefolleg_Daten);int Fichier_Handle=ariichten_Fichier((const char*)Wee,쓰기전용|없으면만들기|내용비우기,0600);if(Fichier_Handle<0)자바실패();int 반환값=schreiwen_Fichier_Daten(Fichier_Handle,Zeechefolleg_Daten,Element_COUNT);Clôture_Fichier(Fichier_Handle);if(반환값!=(int)Element_COUNT)자바실패();return 0;}
Computer_Word 자바파일읽기(Computer_Word Wee){int Fichier_Handle=ariichten_Fichier((const char*)Wee,schreifgeschützt_VALUE,0);if(Fichier_Handle<0)자바실패();int Element_COUNT=Fichier_d_Gréisst_veränneren(Fichier_Handle);if(Element_COUNT<0||Element_COUNT>16384||(unsigned)(Element_COUNT+8)/8>8192-사용량)자바실패();char*Daten_positionéieren=(char*)(동적기억공간+사용량);사용량+=(Element_COUNT+8)/8;int 반환값=파일자료읽기(Fichier_Handle,Daten_positionéieren,Element_COUNT);Clôture_Fichier(Fichier_Handle);if(반환값!=Element_COUNT)자바실패();Daten_positionéieren[Element_COUNT]=0;return (Computer_Word)Daten_positionéieren;}
