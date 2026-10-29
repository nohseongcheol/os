#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long maskin_Word;
static maskin_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Tekst[]="AOT runtime error\n";skrive_fil_data(2,Tekst,sizeof(Tekst)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(maskin_Word *Stabel_Lagring,int *깊이,maskin_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();Stabel_Lagring[(*깊이)++]=VALUE;}
maskin_Word 자바꺼내기(maskin_Word *Stabel_Lagring,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Stabel_Lagring[--*깊이];}
maskin_Word 자바배열(int vare_COUNT){if(vare_COUNT<0||(unsigned)vare_COUNT+1>8192-사용량)자바실패();maskin_Word*data_plassere=동적기억공간+사용량;사용량+=vare_COUNT+1;data_plassere[0]=vare_COUNT;return (maskin_Word)data_plassere;}
maskin_Word *자바색인(maskin_Word objekt_Oppslagsverk,int vare_COUNT){maskin_Word*data_plassere=(maskin_Word*)objekt_Oppslagsverk;if(!data_plassere||vare_COUNT<0||(maskin_Word)vare_COUNT>=data_plassere[0])자바실패();return data_plassere+vare_COUNT+1;}
int 자바길이(maskin_Word objekt_Oppslagsverk){if(!objekt_Oppslagsverk)자바실패();return *(maskin_Word*)objekt_Oppslagsverk;}
int 자바나누기(int x_koordinat,int Y_koordinat,int 나머지){if(!Y_koordinat)자바실패();if(x_koordinat==(-2147483647-1)&&Y_koordinat==-1)return 나머지?0:x_koordinat;return 나머지?x_koordinat%Y_koordinat:x_koordinat/Y_koordinat;}
static unsigned lengd_VALUE(const char*streng_data){unsigned vare_COUNT=0;if(!streng_data)자바실패();while(streng_data[vare_COUNT])vare_COUNT++;return vare_COUNT;}
void 자바출력(maskin_Word data_plassere,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned vare_COUNT=0;int VALUE=(int)data_plassere;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[vare_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[vare_COUNT++]='-';while(vare_COUNT)skrive_fil_data(1,SECOND_VALUE+--vare_COUNT,1);}
    else{const char*streng_data=data_plassere?(const char*)data_plassere:"null";skrive_fil_data(1,streng_data,lengd_VALUE(streng_data));}if(줄바꿈)skrive_fil_data(1,"\n",1);
}
maskin_Word 자바파일쓰기(maskin_Word STIGE,maskin_Word VALUE){const char*streng_data=(const char*)VALUE;unsigned vare_COUNT=lengd_VALUE(streng_data);int fil_handtak=opne_fil((const char*)STIGE,쓰기전용|없으면만들기|내용비우기,0600);if(fil_handtak<0)자바실패();int 반환값=skrive_fil_data(fil_handtak,streng_data,vare_COUNT);Lukk_fil(fil_handtak);if(반환값!=(int)vare_COUNT)자바실패();return 0;}
maskin_Word 자바파일읽기(maskin_Word STIGE){int fil_handtak=opne_fil((const char*)STIGE,skriveverna_VALUE,0);if(fil_handtak<0)자바실패();int vare_COUNT=fil_endre_storleik(fil_handtak);if(vare_COUNT<0||vare_COUNT>16384||(unsigned)(vare_COUNT+8)/8>8192-사용량)자바실패();char*data_plassere=(char*)(동적기억공간+사용량);사용량+=(vare_COUNT+8)/8;int 반환값=파일자료읽기(fil_handtak,data_plassere,vare_COUNT);Lukk_fil(fil_handtak);if(반환값!=vare_COUNT)자바실패();data_plassere[vare_COUNT]=0;return (maskin_Word)data_plassere;}
