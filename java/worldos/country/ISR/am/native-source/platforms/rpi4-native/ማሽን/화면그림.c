/* ትክክለኛ_ውሂብ 화면 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 ምንጭ/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "화면정보.h"
static volatile uint32_t *화소들;
static unsigned 화면줄낱말수, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t ቋሚ_በቦታ_አስቀመጠ){
    return 화소들&&가로<화면너비&&ቋሚ_በቦታ_አስቀመጠ<화면높이?화소들[ቋሚ_በቦታ_አስቀመጠ*화면줄낱말수+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t ቋሚ_በቦታ_አስቀመጠ,uintptr_t 색){
    if(화소들&&가로<화면너비&&ቋሚ_በቦታ_አስቀመጠ<화면높이)화소들[ቋሚ_በቦታ_አስቀመጠ*화면줄낱말수+가로]=(uint32_t)색;
}
void ቦርድ_አዘጋጅ_ስዕል(volatile uint32_t *ውሂብ,unsigned 폭,unsigned ርዝመት_እሴት,unsigned መሪ_እሴት){
    화소들=ውሂብ;화면너비=폭;화면높이=ርዝመት_እሴት;화면줄낱말수=መሪ_እሴት/4;자바그림준비((int)폭,(int)ርዝመት_እሴት);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t 보드그림기록수(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned ቋሚ_በቦታ_አስቀመጠ){return (uint32_t)보드표시화소읽기(가로,ቋሚ_በቦታ_አስቀመጠ);}
int 보드그림범위(int *가로,int *ቋሚ_በቦታ_አስቀመጠ,int *폭,int *ርዝመት_እሴት){
    if(!자바그림범위(*가로,*ቋሚ_በቦታ_አስቀመጠ,*폭,*ርዝመት_እሴት))return 0;
    *가로=자바그림범위값(0);*ቋሚ_በቦታ_አስቀመጠ=자바그림범위값(1);*폭=자바그림범위값(2);*ርዝመት_እሴት=자바그림범위값(3);return 1;
}
int ቦርድ_ጀምር_ስዕል(int 가로,int ቋሚ_በቦታ_አስቀመጠ,int 폭,int ርዝመት_እሴት){return 자바그림시작(가로,ቋሚ_በቦታ_አስቀመጠ,폭,ርዝመት_እሴት);}
void ቦርድ_ጨርስ_ስዕል(void){자바그림마침();}
uintptr_t ቦርድ_ፒክስል(uintptr_t 가로,uintptr_t ቋሚ_በቦታ_አስቀመጠ,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)ቋሚ_በቦታ_አስቀመጠ,(int)색);}
void 보드사각그림(int 가로,int ቋሚ_በቦታ_አስቀመጠ,int 폭,int ርዝመት_እሴት,uint32_t 색){자바사각그림(가로,ቋሚ_በቦታ_አስቀመጠ,폭,ርዝመት_እሴት,(int)색);}
void ቦርድ_ጠቋሚ(int 가로,int ቋሚ_በቦታ_አስቀመጠ,unsigned ቅርጽ_እሴት){자바포인터(가로,ቋሚ_በቦታ_አስቀመጠ,(int)ቅርጽ_እሴት);}
