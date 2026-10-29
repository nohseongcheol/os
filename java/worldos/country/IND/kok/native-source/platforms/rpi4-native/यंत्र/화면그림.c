/* प्रत्यक्ष_डेटा 화면 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 स्त्रोत/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "화면정보.h"
static volatile uint32_t *화소들;
static unsigned 화면줄낱말수, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t उबें_स्थिती){
    return 화소들&&가로<화면너비&&उबें_स्थिती<화면높이?화소들[उबें_स्थिती*화면줄낱말수+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t उबें_स्थिती,uintptr_t 색){
    if(화소들&&가로<화면너비&&उबें_स्थिती<화면높이)화소들[उबें_स्थिती*화면줄낱말수+가로]=(uint32_t)색;
}
void बोर्ड_तयार_करचें_रेखाटन(volatile uint32_t *डेटा,unsigned 폭,unsigned लांबाय_मोल,unsigned प्रधान_मोल){
    화소들=डेटा;화면너비=폭;화면높이=लांबाय_मोल;화면줄낱말수=प्रधान_मोल/4;자바그림준비((int)폭,(int)लांबाय_मोल);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t बोर्ड_रेखाटन_COUNT(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned उबें_स्थिती){return (uint32_t)보드표시화소읽기(가로,उबें_स्थिती);}
int 보드그림범위(int *가로,int *उबें_स्थिती,int *폭,int *लांबाय_मोल){
    if(!자바그림범위(*가로,*उबें_स्थिती,*폭,*लांबाय_मोल))return 0;
    *가로=자바그림범위값(0);*उबें_स्थिती=자바그림범위값(1);*폭=자바그림범위값(2);*लांबाय_मोल=자바그림범위값(3);return 1;
}
int बोर्ड_Start_रेखाटन(int 가로,int उबें_स्थिती,int 폭,int लांबाय_मोल){return 자바그림시작(가로,उबें_स्थिती,폭,लांबाय_मोल);}
void बोर्ड_समाप्त_रेखाटन(void){자바그림마침();}
uintptr_t बोर्ड_पिक्सॅल(uintptr_t 가로,uintptr_t उबें_स्थिती,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)उबें_स्थिती,(int)색);}
void 보드사각그림(int 가로,int उबें_स्थिती,int 폭,int लांबाय_मोल,uint32_t 색){자바사각그림(가로,उबें_स्थिती,폭,लांबाय_मोल,(int)색);}
void बोर्ड_पॉयंटर(int 가로,int उबें_स्थिती,unsigned आकृती_मोल){자바포인터(가로,उबें_स्थिती,(int)आकृती_मोल);}
