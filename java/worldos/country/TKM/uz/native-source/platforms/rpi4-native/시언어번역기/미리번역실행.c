#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long 기계낱말;
static 기계낱말 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Matn[]="AOT runtime error\n";yozmoq_fayl_ma_lumotlar(2,Matn,sizeof(Matn)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(기계낱말 *Stack_Xotira,int *깊이,기계낱말 VALUE){if(*깊이<0||*깊이>=128)자바실패();Stack_Xotira[(*깊이)++]=VALUE;}
기계낱말 자바꺼내기(기계낱말 *Stack_Xotira,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Stack_Xotira[--*깊이];}
기계낱말 자바배열(int element_COUNT){if(element_COUNT<0||(unsigned)element_COUNT+1>8192-사용량)자바실패();기계낱말*ma_lumotlar_holat=동적기억공간+사용량;사용량+=element_COUNT+1;ma_lumotlar_holat[0]=element_COUNT;return (기계낱말)ma_lumotlar_holat;}
기계낱말 *자바색인(기계낱말 obyekt_Ma_lumotnomalar,int element_COUNT){기계낱말*ma_lumotlar_holat=(기계낱말*)obyekt_Ma_lumotnomalar;if(!ma_lumotlar_holat||element_COUNT<0||(기계낱말)element_COUNT>=ma_lumotlar_holat[0])자바실패();return ma_lumotlar_holat+element_COUNT+1;}
int 자바길이(기계낱말 obyekt_Ma_lumotnomalar){if(!obyekt_Ma_lumotnomalar)자바실패();return *(기계낱말*)obyekt_Ma_lumotnomalar;}
int 자바나누기(int x_koordinata,int Y_tugmasi_koordinat,int 나머지){if(!Y_tugmasi_koordinat)자바실패();if(x_koordinata==(-2147483647-1)&&Y_tugmasi_koordinat==-1)return 나머지?0:x_koordinata;return 나머지?x_koordinata%Y_tugmasi_koordinat:x_koordinata/Y_tugmasi_koordinat;}
static unsigned uzunlik_VALUE(const char*satr_ma_lumotlar){unsigned element_COUNT=0;if(!satr_ma_lumotlar)자바실패();while(satr_ma_lumotlar[element_COUNT])element_COUNT++;return element_COUNT;}
void 자바출력(기계낱말 ma_lumotlar_holat,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned element_COUNT=0;int VALUE=(int)ma_lumotlar_holat;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[element_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[element_COUNT++]='-';while(element_COUNT)yozmoq_fayl_ma_lumotlar(1,SECOND_VALUE+--element_COUNT,1);}
    else{const char*satr_ma_lumotlar=ma_lumotlar_holat?(const char*)ma_lumotlar_holat:"null";yozmoq_fayl_ma_lumotlar(1,satr_ma_lumotlar,uzunlik_VALUE(satr_ma_lumotlar));}if(줄바꿈)yozmoq_fayl_ma_lumotlar(1,"\n",1);
}
기계낱말 자바파일쓰기(기계낱말 yo_l,기계낱말 VALUE){const char*satr_ma_lumotlar=(const char*)VALUE;unsigned element_COUNT=uzunlik_VALUE(satr_ma_lumotlar);int fayl_deskriptor=ochmoq_fayl((const char*)yo_l,쓰기전용|없으면만들기|내용비우기,0600);if(fayl_deskriptor<0)자바실패();int 반환값=yozmoq_fayl_ma_lumotlar(fayl_deskriptor,satr_ma_lumotlar,element_COUNT);yopmoq_fayl(fayl_deskriptor);if(반환값!=(int)element_COUNT)자바실패();return 0;}
기계낱말 자바파일읽기(기계낱말 yo_l){int fayl_deskriptor=ochmoq_fayl((const char*)yo_l,faqat_o_qish_uchun_VALUE,0);if(fayl_deskriptor<0)자바실패();int element_COUNT=fayl_o_lcham(fayl_deskriptor);if(element_COUNT<0||element_COUNT>16384||(unsigned)(element_COUNT+8)/8>8192-사용량)자바실패();char*ma_lumotlar_holat=(char*)(동적기억공간+사용량);사용량+=(element_COUNT+8)/8;int 반환값=파일자료읽기(fayl_deskriptor,ma_lumotlar_holat,element_COUNT);yopmoq_fayl(fayl_deskriptor);if(반환값!=element_COUNT)자바실패();ma_lumotlar_holat[element_COUNT]=0;return (기계낱말)ma_lumotlar_holat;}
