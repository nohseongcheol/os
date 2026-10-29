/* প্রকৃত_ডাটা 화면 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 উৎস_নথি/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "화면정보.h"
static volatile uint32_t *화소들;
static unsigned 화면줄낱말수, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t উল্লম্ব_পদ){
    return 화소들&&가로<화면너비&&উল্লম্ব_পদ<화면높이?화소들[উল্লম্ব_পদ*화면줄낱말수+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t উল্লম্ব_পদ,uintptr_t 색){
    if(화소들&&가로<화면너비&&উল্লম্ব_পদ<화면높이)화소들[উল্লম্ব_পদ*화면줄낱말수+가로]=(uint32_t)색;
}
void বোর্ড_প্রস্তুত_করুন_অঙ্কন(volatile uint32_t *ডাটা,unsigned 폭,unsigned দৈর্ঘ্য_মান,unsigned অগ্র_মান){
    화소들=ডাটা;화면너비=폭;화면높이=দৈর্ঘ্য_মান;화면줄낱말수=অগ্র_মান/4;자바그림준비((int)폭,(int)দৈর্ঘ্য_মান);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t 보드그림기록수(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned উল্লম্ব_পদ){return (uint32_t)보드표시화소읽기(가로,উল্লম্ব_পদ);}
int 보드그림범위(int *가로,int *উল্লম্ব_পদ,int *폭,int *দৈর্ঘ্য_মান){
    if(!자바그림범위(*가로,*উল্লম্ব_পদ,*폭,*দৈর্ঘ্য_মান))return 0;
    *가로=자바그림범위값(0);*উল্লম্ব_পদ=자바그림범위값(1);*폭=자바그림범위값(2);*দৈর্ঘ্য_মান=자바그림범위값(3);return 1;
}
int বোর্ড_শুরু_অঙ্কন(int 가로,int উল্লম্ব_পদ,int 폭,int দৈর্ঘ্য_মান){return 자바그림시작(가로,উল্লম্ব_পদ,폭,দৈর্ঘ্য_মান);}
void বোর্ড_শেষ_অঙ্কন(void){자바그림마침();}
uintptr_t বোর্ড_পেল্(uintptr_t 가로,uintptr_t উল্লম্ব_পদ,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)উল্লম্ব_পদ,(int)색);}
void 보드사각그림(int 가로,int উল্লম্ব_পদ,int 폭,int দৈর্ঘ্য_মান,uint32_t 색){자바사각그림(가로,উল্লম্ব_পদ,폭,দৈর্ঘ্য_মান,(int)색);}
void বোর্ড_নির্দেশক(int 가로,int উল্লম্ব_পদ,unsigned আকৃতি_মান){자바포인터(가로,উল্লম্ব_পদ,(int)আকৃতি_মান);}
