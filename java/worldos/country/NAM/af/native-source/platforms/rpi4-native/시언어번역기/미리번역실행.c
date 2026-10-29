#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long masjien_Word;
static masjien_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Teks[]="AOT runtime error\n";skryf_lêer_data(2,Teks,sizeof(Teks)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(masjien_Word *Stapel_Berging,int *깊이,masjien_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();Stapel_Berging[(*깊이)++]=VALUE;}
masjien_Word 자바꺼내기(masjien_Word *Stapel_Berging,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Stapel_Berging[--*깊이];}
masjien_Word 자바배열(int item_COUNT){if(item_COUNT<0||(unsigned)item_COUNT+1>8192-사용량)자바실패();masjien_Word*data_plaas=동적기억공간+사용량;사용량+=item_COUNT+1;data_plaas[0]=item_COUNT;return (masjien_Word)data_plaas;}
masjien_Word *자바색인(masjien_Word objek_Naslaan,int item_COUNT){masjien_Word*data_plaas=(masjien_Word*)objek_Naslaan;if(!data_plaas||item_COUNT<0||(masjien_Word)item_COUNT>=data_plaas[0])자바실패();return data_plaas+item_COUNT+1;}
int 자바길이(masjien_Word objek_Naslaan){if(!objek_Naslaan)자바실패();return *(masjien_Word*)objek_Naslaan;}
int 자바나누기(int x_koördinaat,int Y_koördinaat,int 나머지){if(!Y_koördinaat)자바실패();if(x_koördinaat==(-2147483647-1)&&Y_koördinaat==-1)return 나머지?0:x_koördinaat;return 나머지?x_koördinaat%Y_koördinaat:x_koördinaat/Y_koördinaat;}
static unsigned lengte_VALUE(const char*string_data){unsigned item_COUNT=0;if(!string_data)자바실패();while(string_data[item_COUNT])item_COUNT++;return item_COUNT;}
void 자바출력(masjien_Word data_plaas,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned item_COUNT=0;int VALUE=(int)data_plaas;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[item_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[item_COUNT++]='-';while(item_COUNT)skryf_lêer_data(1,SECOND_VALUE+--item_COUNT,1);}
    else{const char*string_data=data_plaas?(const char*)data_plaas:"null";skryf_lêer_data(1,string_data,lengte_VALUE(string_data));}if(줄바꿈)skryf_lêer_data(1,"\n",1);
}
masjien_Word 자바파일쓰기(masjien_Word Pad,masjien_Word VALUE){const char*string_data=(const char*)VALUE;unsigned item_COUNT=lengte_VALUE(string_data);int lêer_handvatsel=skep_lêer((const char*)Pad,쓰기전용|없으면만들기|내용비우기,0600);if(lêer_handvatsel<0)자바실패();int 반환값=skryf_lêer_data(lêer_handvatsel,string_data,item_COUNT);sluit_lêer(lêer_handvatsel);if(반환값!=(int)item_COUNT)자바실패();return 0;}
masjien_Word 자바파일읽기(masjien_Word Pad){int lêer_handvatsel=skep_lêer((const char*)Pad,leesalleen_VALUE,0);if(lêer_handvatsel<0)자바실패();int item_COUNT=lêer_verstel(lêer_handvatsel);if(item_COUNT<0||item_COUNT>16384||(unsigned)(item_COUNT+8)/8>8192-사용량)자바실패();char*data_plaas=(char*)(동적기억공간+사용량);사용량+=(item_COUNT+8)/8;int 반환값=파일자료읽기(lêer_handvatsel,data_plaas,item_COUNT);sluit_lêer(lêer_handvatsel);if(반환값!=item_COUNT)자바실패();data_plaas[item_COUNT]=0;return (masjien_Word)data_plaas;}
