#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long mesin_Word;
static mesin_Word ingatan_dinamik[8192];static unsigned 사용량;
void 자바실패(void){const char Teks[]="AOT runtime error\n";tulis_fail_data(2,Teks,sizeof(Teks)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(mesin_Word *ingatan_tindanan,int *깊이,mesin_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();ingatan_tindanan[(*깊이)++]=VALUE;}
mesin_Word 자바꺼내기(mesin_Word *ingatan_tindanan,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return ingatan_tindanan[--*깊이];}
mesin_Word 자바배열(int item_COUNT){if(item_COUNT<0||(unsigned)item_COUNT+1>8192-사용량)자바실패();mesin_Word*data_jawatan=ingatan_dinamik+사용량;사용량+=item_COUNT+1;data_jawatan[0]=item_COUNT;return (mesin_Word)data_jawatan;}
mesin_Word *자바색인(mesin_Word objek_Rujukan,int item_COUNT){mesin_Word*data_jawatan=(mesin_Word*)objek_Rujukan;if(!data_jawatan||item_COUNT<0||(mesin_Word)item_COUNT>=data_jawatan[0])자바실패();return data_jawatan+item_COUNT+1;}
int 자바길이(mesin_Word objek_Rujukan){if(!objek_Rujukan)자바실패();return *(mesin_Word*)objek_Rujukan;}
int 자바나누기(int koordinat_x,int Y_koordinat,int 나머지){if(!Y_koordinat)자바실패();if(koordinat_x==(-2147483647-1)&&Y_koordinat==-1)return 나머지?0:koordinat_x;return 나머지?koordinat_x%Y_koordinat:koordinat_x/Y_koordinat;}
static unsigned kepanjangan_VALUE(const char*rentetan_data){unsigned item_COUNT=0;if(!rentetan_data)자바실패();while(rentetan_data[item_COUNT])item_COUNT++;return item_COUNT;}
void 자바출력(mesin_Word data_jawatan,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned item_COUNT=0;int VALUE=(int)data_jawatan;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[item_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[item_COUNT++]='-';while(item_COUNT)tulis_fail_data(1,SECOND_VALUE+--item_COUNT,1);}
    else{const char*rentetan_data=data_jawatan?(const char*)data_jawatan:"null";tulis_fail_data(1,rentetan_data,kepanjangan_VALUE(rentetan_data));}if(줄바꿈)tulis_fail_data(1,"\n",1);
}
mesin_Word 자바파일쓰기(mesin_Word LALUAN,mesin_Word VALUE){const char*rentetan_data=(const char*)VALUE;unsigned item_COUNT=kepanjangan_VALUE(rentetan_data);int fail_pemegang=buka_fail((const char*)LALUAN,tulis_sahaja_VALUE|없으면만들기|potong_TOC,0600);if(fail_pemegang<0)자바실패();int 반환값=tulis_fail_data(fail_pemegang,rentetan_data,item_COUNT);Tutup_fail(fail_pemegang);if(반환값!=(int)item_COUNT)자바실패();return 0;}
mesin_Word 자바파일읽기(mesin_Word LALUAN){int fail_pemegang=buka_fail((const char*)LALUAN,baca_sahaja_VALUE,0);if(fail_pemegang<0)자바실패();int item_COUNT=saiz_fail(fail_pemegang);if(item_COUNT<0||item_COUNT>16384||(unsigned)(item_COUNT+8)/8>8192-사용량)자바실패();char*data_jawatan=(char*)(ingatan_dinamik+사용량);사용량+=(item_COUNT+8)/8;int 반환값=파일자료읽기(fail_pemegang,data_jawatan,item_COUNT);Tutup_fail(fail_pemegang);if(반환값!=item_COUNT)자바실패();data_jawatan[item_COUNT]=0;return (mesin_Word)data_jawatan;}
