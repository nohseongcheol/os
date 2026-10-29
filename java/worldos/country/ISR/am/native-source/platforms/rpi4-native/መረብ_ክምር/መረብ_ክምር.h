#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void አዘጋጅ_መረብ(void);
void 통신망살피기(void);
int 통신끝점만들기(int ተይብ_ምድብ);
int 망주소묶기(int ፋይል_እጀታ, uint32_t አድራሻ, unsigned የወደብ_ቁጥር);
int 연결기다리기(int ፋይል_እጀታ);
void 통신주소재사용(int ፋይል_እጀታ);
int 망연결하기(int ፋይል_እጀታ, uint32_t አድራሻ, unsigned የወደብ_ቁጥር);
int 망연결받기(int ፋይል_እጀታ);
int 통신읽기(int ፋይል_እጀታ, void *ውሂብ, unsigned 개수);
int 통신쓰기(int ፋይል_እጀታ, const void *ውሂብ, unsigned 개수);
int 전문보내기(int ፋይል_እጀታ, const void *ውሂብ, unsigned 개수, uint32_t አድራሻ, unsigned የወደብ_ቁጥር);
int 전문받기(int ፋይል_እጀታ, void *ውሂብ, unsigned 개수);
unsigned መረብ_የወደብ_ቁጥር(int ፋይል_እጀታ);
unsigned አቻ_የወደብ_ቁጥር(int ፋይል_እጀታ);
uint32_t 상대통신주소(int ፋይል_እጀታ);
void ዝጋ_መረብ(int ፋይል_እጀታ);
int ፋይል_ትልልፍ_ቁጥጥር(int ተግባር);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ምዝግብ_እሴት, unsigned መረጃ_ጠቆመ);
int አዋቅር_መረብ(unsigned ተግባር, uint32_t አድራሻ, uint32_t ጭንብል_እሴት, uint32_t አግባቢ_ፍኖት_እሴት);
int 응답시험시작(uint32_t አድራሻ, unsigned ቅደም_ተከተል_እሴት);
int 응답시험읽기(unsigned ምዝግብ_እሴት);
#endif
