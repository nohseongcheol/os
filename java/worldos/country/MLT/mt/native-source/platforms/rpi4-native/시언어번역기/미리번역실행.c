#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long kompjuter_Word;
static kompjuter_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char SMS[]="AOT runtime error\n";kiteb_fajl_data(2,SMS,sizeof(SMS)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(kompjuter_Word *Munzell_Ħażna,int *깊이,kompjuter_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();Munzell_Ħażna[(*깊이)++]=VALUE;}
kompjuter_Word 자바꺼내기(kompjuter_Word *Munzell_Ħażna,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Munzell_Ħażna[--*깊이];}
kompjuter_Word 자바배열(int element_COUNT){if(element_COUNT<0||(unsigned)element_COUNT+1>8192-사용량)자바실패();kompjuter_Word*data_pożizzjoni=동적기억공간+사용량;사용량+=element_COUNT+1;data_pożizzjoni[0]=element_COUNT;return (kompjuter_Word)data_pożizzjoni;}
kompjuter_Word *자바색인(kompjuter_Word oġġett_Referenza,int element_COUNT){kompjuter_Word*data_pożizzjoni=(kompjuter_Word*)oġġett_Referenza;if(!data_pożizzjoni||element_COUNT<0||(kompjuter_Word)element_COUNT>=data_pożizzjoni[0])자바실패();return data_pożizzjoni+element_COUNT+1;}
int 자바길이(kompjuter_Word oġġett_Referenza){if(!oġġett_Referenza)자바실패();return *(kompjuter_Word*)oġġett_Referenza;}
int 자바나누기(int koordinat_x,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(koordinat_x==(-2147483647-1)&&세로좌표==-1)return 나머지?0:koordinat_x;return 나머지?koordinat_x%세로좌표:koordinat_x/세로좌표;}
static unsigned tul_VALUE(const char*string_data){unsigned element_COUNT=0;if(!string_data)자바실패();while(string_data[element_COUNT])element_COUNT++;return element_COUNT;}
void 자바출력(kompjuter_Word data_pożizzjoni,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned element_COUNT=0;int VALUE=(int)data_pożizzjoni;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[element_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[element_COUNT++]='-';while(element_COUNT)kiteb_fajl_data(1,SECOND_VALUE+--element_COUNT,1);}
    else{const char*string_data=data_pożizzjoni?(const char*)data_pożizzjoni:"null";kiteb_fajl_data(1,string_data,tul_VALUE(string_data));}if(줄바꿈)kiteb_fajl_data(1,"\n",1);
}
kompjuter_Word 자바파일쓰기(kompjuter_Word mogħdija,kompjuter_Word VALUE){const char*string_data=(const char*)VALUE;unsigned element_COUNT=tul_VALUE(string_data);int fajl_handle=fetaħ_fajl((const char*)mogħdija,쓰기전용|없으면만들기|내용비우기,0600);if(fajl_handle<0)자바실패();int 반환값=kiteb_fajl_data(fajl_handle,string_data,element_COUNT);agħlaq_fajl(fajl_handle);if(반환값!=(int)element_COUNT)자바실패();return 0;}
kompjuter_Word 자바파일읽기(kompjuter_Word mogħdija){int fajl_handle=fetaħ_fajl((const char*)mogħdija,qari_biss_VALUE,0);if(fajl_handle<0)자바실패();int element_COUNT=fajl_daqqas(fajl_handle);if(element_COUNT<0||element_COUNT>16384||(unsigned)(element_COUNT+8)/8>8192-사용량)자바실패();char*data_pożizzjoni=(char*)(동적기억공간+사용량);사용량+=(element_COUNT+8)/8;int 반환값=파일자료읽기(fajl_handle,data_pożizzjoni,element_COUNT);agħlaq_fajl(fajl_handle);if(반환값!=element_COUNT)자바실패();data_pożizzjoni[element_COUNT]=0;return (kompjuter_Word)data_pożizzjoni;}
