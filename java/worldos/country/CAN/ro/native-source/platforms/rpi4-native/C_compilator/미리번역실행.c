#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long mașină_Word;
static mașină_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char SMS[]="AOT runtime error\n";scriere_Fișier_date(2,SMS,sizeof(SMS)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(mașină_Word *Teanc_Stocare,int *깊이,mașină_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();Teanc_Stocare[(*깊이)++]=VALUE;}
mașină_Word 자바꺼내기(mașină_Word *Teanc_Stocare,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Teanc_Stocare[--*깊이];}
mașină_Word 자바배열(int element_COUNT){if(element_COUNT<0||(unsigned)element_COUNT+1>8192-사용량)자바실패();mașină_Word*date_poziție=동적기억공간+사용량;사용량+=element_COUNT+1;date_poziție[0]=element_COUNT;return (mașină_Word)date_poziție;}
mașină_Word *자바색인(mașină_Word obiect_referință,int element_COUNT){mașină_Word*date_poziție=(mașină_Word*)obiect_referință;if(!date_poziție||element_COUNT<0||(mașină_Word)element_COUNT>=date_poziție[0])자바실패();return date_poziție+element_COUNT+1;}
int 자바길이(mașină_Word obiect_referință){if(!obiect_referință)자바실패();return *(mașină_Word*)obiect_referință;}
int 자바나누기(int coordonata_X,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(coordonata_X==(-2147483647-1)&&세로좌표==-1)return 나머지?0:coordonata_X;return 나머지?coordonata_X%세로좌표:coordonata_X/세로좌표;}
static unsigned lungime_VALUE(const char*șir_date){unsigned element_COUNT=0;if(!șir_date)자바실패();while(șir_date[element_COUNT])element_COUNT++;return element_COUNT;}
void 자바출력(mașină_Word date_poziție,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned element_COUNT=0;int VALUE=(int)date_poziție;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[element_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[element_COUNT++]='-';while(element_COUNT)scriere_Fișier_date(1,SECOND_VALUE+--element_COUNT,1);}
    else{const char*șir_date=date_poziție?(const char*)date_poziție:"null";scriere_Fișier_date(1,șir_date,lungime_VALUE(șir_date));}if(줄바꿈)scriere_Fișier_date(1,"\n",1);
}
mașină_Word 자바파일쓰기(mașină_Word Cale,mașină_Word VALUE){const char*șir_date=(const char*)VALUE;unsigned element_COUNT=lungime_VALUE(șir_date);int Fișier_handle=crea_Fișier((const char*)Cale,쓰기전용|없으면만들기|trunchia_TOC,0600);if(Fișier_handle<0)자바실패();int 반환값=scriere_Fișier_date(Fișier_handle,șir_date,element_COUNT);închide_Fișier(Fișier_handle);if(반환값!=(int)element_COUNT)자바실패();return 0;}
mașină_Word 자바파일읽기(mașină_Word Cale){int Fișier_handle=crea_Fișier((const char*)Cale,doar_în_citire_VALUE,0);if(Fișier_handle<0)자바실패();int element_COUNT=dimensiune_fișier(Fișier_handle);if(element_COUNT<0||element_COUNT>16384||(unsigned)(element_COUNT+8)/8>8192-사용량)자바실패();char*date_poziție=(char*)(동적기억공간+사용량);사용량+=(element_COUNT+8)/8;int 반환값=파일자료읽기(Fișier_handle,date_poziție,element_COUNT);închide_Fișier(Fișier_handle);if(반환값!=element_COUNT)자바실패();date_poziție[element_COUNT]=0;return (mașină_Word)date_poziție;}
