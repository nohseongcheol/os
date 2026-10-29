#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long यंत्र_Word;
static यंत्र_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char SMS[]="AOT runtime error\n";बरोवचें_फायल_डेटा(2,SMS,sizeof(SMS)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(यंत्र_Word *स्टॅक_सांठवण,int *깊이,यंत्र_Word मोल){if(*깊이<0||*깊이>=128)자바실패();स्टॅक_सांठवण[(*깊이)++]=मोल;}
यंत्र_Word 자바꺼내기(यंत्र_Word *स्टॅक_सांठवण,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return स्टॅक_सांठवण[--*깊이];}
यंत्र_Word 자바배열(int आयटम_COUNT){if(आयटम_COUNT<0||(unsigned)आयटम_COUNT+1>8192-사용량)자바실패();यंत्र_Word*डेटा_स्थिती=동적기억공간+사용량;사용량+=आयटम_COUNT+1;डेटा_स्थिती[0]=आयटम_COUNT;return (यंत्र_Word)डेटा_स्थिती;}
यंत्र_Word *자바색인(यंत्र_Word ऑब्जॅक्ट_संदर्भ,int आयटम_COUNT){यंत्र_Word*डेटा_स्थिती=(यंत्र_Word*)ऑब्जॅक्ट_संदर्भ;if(!डेटा_स्थिती||आयटम_COUNT<0||(यंत्र_Word)आयटम_COUNT>=डेटा_स्थिती[0])자바실패();return डेटा_स्थिती+आयटम_COUNT+1;}
int 자바길이(यंत्र_Word ऑब्जॅक्ट_संदर्भ){if(!ऑब्जॅक्ट_संदर्भ)자바실패();return *(यंत्र_Word*)ऑब्जॅक्ट_संदर्भ;}
int 자바나누기(int x_coordinate,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(x_coordinate==(-2147483647-1)&&세로좌표==-1)return 나머지?0:x_coordinate;return 나머지?x_coordinate%세로좌표:x_coordinate/세로좌표;}
static unsigned लांबाय_मोल(const char*स्ट्रिंग_डेटा){unsigned आयटम_COUNT=0;if(!स्ट्रिंग_डेटा)자바실패();while(स्ट्रिंग_डेटा[आयटम_COUNT])आयटम_COUNT++;return आयटम_COUNT;}
void 자바출력(यंत्र_Word डेटा_स्थिती,int 수치,int 줄바꿈){
    if(수치){char SECOND_मोल[16];unsigned आयटम_COUNT=0;int मोल=(int)डेटा_स्थिती;unsigned 부호없는값=मोल<0?0-(unsigned)मोल:मोल;do{SECOND_मोल[आयटम_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(मोल<0)SECOND_मोल[आयटम_COUNT++]='-';while(आयटम_COUNT)बरोवचें_फायल_डेटा(1,SECOND_मोल+--आयटम_COUNT,1);}
    else{const char*स्ट्रिंग_डेटा=डेटा_स्थिती?(const char*)डेटा_स्थिती:"null";बरोवचें_फायल_डेटा(1,स्ट्रिंग_डेटा,लांबाय_मोल(स्ट्रिंग_डेटा));}if(줄바꿈)बरोवचें_फायल_डेटा(1,"\n",1);
}
यंत्र_Word 자바파일쓰기(यंत्र_Word पाथ,यंत्र_Word मोल){const char*स्ट्रिंग_डेटा=(const char*)मोल;unsigned आयटम_COUNT=लांबाय_मोल(स्ट्रिंग_डेटा);int फायल_हँडल=उगडचें_फायल((const char*)पाथ,쓰기전용|없으면만들기|내용비우기,0600);if(फायल_हँडल<0)자바실패();int 반환값=बरोवचें_फायल_डेटा(फायल_हँडल,स्ट्रिंग_डेटा,आयटम_COUNT);शेवट_फायल(फायल_हँडल);if(반환값!=(int)आयटम_COUNT)자바실패();return 0;}
यंत्र_Word 자바파일읽기(यंत्र_Word पाथ){int फायल_हँडल=उगडचें_फायल((const char*)पाथ,फकत_वाचचें_मोल,0);if(फायल_हँडल<0)자바실패();int आयटम_COUNT=फायल_आवाठ(फायल_हँडल);if(आयटम_COUNT<0||आयटम_COUNT>16384||(unsigned)(आयटम_COUNT+8)/8>8192-사용량)자바실패();char*डेटा_स्थिती=(char*)(동적기억공간+사용량);사용량+=(आयटम_COUNT+8)/8;int 반환값=파일자료읽기(फायल_हँडल,डेटा_स्थिती,आयटम_COUNT);शेवट_फायल(फायल_हँडल);if(반환값!=आयटम_COUNT)자바실패();डेटा_स्थिती[आयटम_COUNT]=0;return (यंत्र_Word)डेटा_स्थिती;}
