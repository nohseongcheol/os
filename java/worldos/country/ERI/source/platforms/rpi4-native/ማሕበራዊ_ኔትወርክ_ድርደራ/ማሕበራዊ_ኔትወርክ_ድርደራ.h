#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void ኣዳልው_ማሕበራዊ_ኔትወርክ(void);
void 통신망살피기(void);
int 통신끝점만들기(int ዓይነት_መደብ);
int 망주소묶기(int ፋይል_መትሓዚ, uint32_t ኣድራሻ, unsigned 접속번호);
int 연결기다리기(int ፋይል_መትሓዚ);
void 통신주소재사용(int ፋይል_መትሓዚ);
int 망연결하기(int ፋይል_መትሓዚ, uint32_t ኣድራሻ, unsigned 접속번호);
int 망연결받기(int ፋይል_መትሓዚ);
int 통신읽기(int ፋይል_መትሓዚ, void *ሓበሬታ, unsigned 개수);
int 통신쓰기(int ፋይል_መትሓዚ, const void *ሓበሬታ, unsigned 개수);
int 전문보내기(int ፋይል_መትሓዚ, const void *ሓበሬታ, unsigned 개수, uint32_t ኣድራሻ, unsigned 접속번호);
int 전문받기(int ፋይል_መትሓዚ, void *ሓበሬታ, unsigned 개수);
unsigned 통신접속번호(int ፋይል_መትሓዚ);
unsigned 상대접속번호(int ፋይል_መትሓዚ);
uint32_t 상대통신주소(int ፋይል_መትሓዚ);
void ዕጸው_ማሕበራዊ_ኔትወርክ(int ፋይል_መትሓዚ);
int ፋይል_ምስጋር_ቁጽጽር(int ስጉምቲ);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ምእታው_ዋጋ, unsigned መሐበሪ);
int ኣቃንይ_ማሕበራዊ_ኔትወርክ(unsigned ስጉምቲ, uint32_t ኣድራሻ, uint32_t 가림, uint32_t 관문);
int 응답시험시작(uint32_t ኣድራሻ, unsigned ተርታ_ዋጋ);
int 응답시험읽기(unsigned ምእታው_ዋጋ);
#endif
