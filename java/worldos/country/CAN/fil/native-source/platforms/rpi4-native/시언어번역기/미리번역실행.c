#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long machine_Word;
static machine_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char SMS[]="AOT runtime error\n";sumulat_file_data(2,SMS,sizeof(SMS)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(machine_Word *Stack_Storage,int *깊이,machine_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();Stack_Storage[(*깊이)++]=VALUE;}
machine_Word 자바꺼내기(machine_Word *Stack_Storage,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Stack_Storage[--*깊이];}
machine_Word 자바배열(int item_COUNT){if(item_COUNT<0||(unsigned)item_COUNT+1>8192-사용량)자바실패();machine_Word*data_posisyon=동적기억공간+사용량;사용량+=item_COUNT+1;data_posisyon[0]=item_COUNT;return (machine_Word)data_posisyon;}
machine_Word *자바색인(machine_Word bagay_Sanggunian,int item_COUNT){machine_Word*data_posisyon=(machine_Word*)bagay_Sanggunian;if(!data_posisyon||item_COUNT<0||(machine_Word)item_COUNT>=data_posisyon[0])자바실패();return data_posisyon+item_COUNT+1;}
int 자바길이(machine_Word bagay_Sanggunian){if(!bagay_Sanggunian)자바실패();return *(machine_Word*)bagay_Sanggunian;}
int 자바나누기(int x_coordinate,int Y_button_coordinate,int 나머지){if(!Y_button_coordinate)자바실패();if(x_coordinate==(-2147483647-1)&&Y_button_coordinate==-1)return 나머지?0:x_coordinate;return 나머지?x_coordinate%Y_button_coordinate:x_coordinate/Y_button_coordinate;}
static unsigned haba_VALUE(const char*string_data){unsigned item_COUNT=0;if(!string_data)자바실패();while(string_data[item_COUNT])item_COUNT++;return item_COUNT;}
void 자바출력(machine_Word data_posisyon,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned item_COUNT=0;int VALUE=(int)data_posisyon;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[item_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[item_COUNT++]='-';while(item_COUNT)sumulat_file_data(1,SECOND_VALUE+--item_COUNT,1);}
    else{const char*string_data=data_posisyon?(const char*)data_posisyon:"null";sumulat_file_data(1,string_data,haba_VALUE(string_data));}if(줄바꿈)sumulat_file_data(1,"\n",1);
}
machine_Word 자바파일쓰기(machine_Word path,machine_Word VALUE){const char*string_data=(const char*)VALUE;unsigned item_COUNT=haba_VALUE(string_data);int file_hawakán=buksan_file((const char*)path,쓰기전용|없으면만들기|내용비우기,0600);if(file_hawakán<0)자바실패();int 반환값=sumulat_file_data(file_hawakán,string_data,item_COUNT);isara_file(file_hawakán);if(반환값!=(int)item_COUNT)자바실패();return 0;}
machine_Word 자바파일읽기(machine_Word path){int file_hawakán=buksan_file((const char*)path,mababasa_lamang_VALUE,0);if(file_hawakán<0)자바실패();int item_COUNT=file_sukat(file_hawakán);if(item_COUNT<0||item_COUNT>16384||(unsigned)(item_COUNT+8)/8>8192-사용량)자바실패();char*data_posisyon=(char*)(동적기억공간+사용량);사용량+=(item_COUNT+8)/8;int 반환값=파일자료읽기(file_hawakán,data_posisyon,item_COUNT);isara_file(file_hawakán);if(반환값!=item_COUNT)자바실패();data_posisyon[item_COUNT]=0;return (machine_Word)data_posisyon;}
