#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long mesin_Kata;
static mesin_Kata memori_dinamis[8192];static unsigned 사용량;
void 자바실패(void){const char teks[]="AOT runtime error\n";tulis_file_data(2,teks,sizeof(teks)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(mesin_Kata *memori_tumpukan,int *깊이,mesin_Kata VALUE){if(*깊이<0||*깊이>=128)자바실패();memori_tumpukan[(*깊이)++]=VALUE;}
mesin_Kata 자바꺼내기(mesin_Kata *memori_tumpukan,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return memori_tumpukan[--*깊이];}
mesin_Kata 자바배열(int item_COUNT){if(item_COUNT<0||(unsigned)item_COUNT+1>8192-사용량)자바실패();mesin_Kata*data_posisi=memori_dinamis+사용량;사용량+=item_COUNT+1;data_posisi[0]=item_COUNT;return (mesin_Kata)data_posisi;}
mesin_Kata *자바색인(mesin_Kata objek_Referensi,int item_COUNT){mesin_Kata*data_posisi=(mesin_Kata*)objek_Referensi;if(!data_posisi||item_COUNT<0||(mesin_Kata)item_COUNT>=data_posisi[0])자바실패();return data_posisi+item_COUNT+1;}
int 자바길이(mesin_Kata objek_Referensi){if(!objek_Referensi)자바실패();return *(mesin_Kata*)objek_Referensi;}
int 자바나누기(int koordinat_x,int Y_koordinat,int 나머지){if(!Y_koordinat)자바실패();if(koordinat_x==(-2147483647-1)&&Y_koordinat==-1)return 나머지?0:koordinat_x;return 나머지?koordinat_x%Y_koordinat:koordinat_x/Y_koordinat;}
static unsigned panjang_VALUE(const char*string_data){unsigned item_COUNT=0;if(!string_data)자바실패();while(string_data[item_COUNT])item_COUNT++;return item_COUNT;}
void 자바출력(mesin_Kata data_posisi,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned item_COUNT=0;int VALUE=(int)data_posisi;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[item_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[item_COUNT++]='-';while(item_COUNT)tulis_file_data(1,SECOND_VALUE+--item_COUNT,1);}
    else{const char*string_data=data_posisi?(const char*)data_posisi:"null";tulis_file_data(1,string_data,panjang_VALUE(string_data));}if(줄바꿈)tulis_file_data(1,"\n",1);
}
mesin_Kata 자바파일쓰기(mesin_Kata jalur,mesin_Kata VALUE){const char*string_data=(const char*)VALUE;unsigned item_COUNT=panjang_VALUE(string_data);int file_handel=buat_file((const char*)jalur,쓰기전용|없으면만들기|내용비우기,0600);if(file_handel<0)자바실패();int 반환값=tulis_file_data(file_handel,string_data,item_COUNT);Tutup_file(file_handel);if(반환값!=(int)item_COUNT)자바실패();return 0;}
mesin_Kata 자바파일읽기(mesin_Kata jalur){int file_handel=buat_file((const char*)jalur,baca_saja_VALUE,0);if(file_handel<0)자바실패();int item_COUNT=ukuran_file(file_handel);if(item_COUNT<0||item_COUNT>16384||(unsigned)(item_COUNT+8)/8>8192-사용량)자바실패();char*data_posisi=(char*)(memori_dinamis+사용량);사용량+=(item_COUNT+8)/8;int 반환값=파일자료읽기(file_handel,data_posisi,item_COUNT);Tutup_file(file_handel);if(반환값!=item_COUNT)자바실패();data_posisi[item_COUNT]=0;return (mesin_Kata)data_posisi;}
