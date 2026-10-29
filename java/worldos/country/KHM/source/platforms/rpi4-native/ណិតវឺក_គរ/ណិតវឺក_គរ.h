#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void រៀបចំ_ណិតវឺក_7c090b15(void);
void 통신망살피기(void);
int 통신끝점만들기(int វាយបញ្ចូល_ប្រភេទ);
int 망주소묶기(int ឯកសារ_ការកាន់កាប់, uint32_t អ៊ីម៉ែល, unsigned លេខរន្ធ);
int 연결기다리기(int ឯកសារ_ការកាន់កាប់);
void 통신주소재사용(int ឯកសារ_ការកាន់កាប់);
int 망연결하기(int ឯកសារ_ការកាន់កាប់, uint32_t អ៊ីម៉ែល, unsigned លេខរន្ធ);
int 망연결받기(int ឯកសារ_ការកាន់កាប់);
int 통신읽기(int ឯកសារ_ការកាន់កាប់, void *ទិន្នន័យ, unsigned 개수);
int 통신쓰기(int ឯកសារ_ការកាន់កាប់, const void *ទិន្នន័យ, unsigned 개수);
int 전문보내기(int ឯកសារ_ការកាន់កាប់, const void *ទិន្នន័យ, unsigned 개수, uint32_t អ៊ីម៉ែល, unsigned លេខរន្ធ);
int 전문받기(int ឯកសារ_ការកាន់កាប់, void *ទិន្នន័យ, unsigned 개수);
unsigned ណិតវឺក_លេខរន្ធ(int ឯកសារ_ការកាន់កាប់);
unsigned សិទ្ធស្មើ_លេខរន្ធ(int ឯកសារ_ការកាន់កាប់);
uint32_t 상대통신주소(int ឯកសារ_ការកាន់កាប់);
void បិទ_ណិតវឺក(int ឯកសារ_ការកាន់កាប់);
int ឯកសារ_ផ្ទេរ_អង្គបញ្ជា(int អំពើ);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ការបញ្ចូល_តំលៃ, unsigned សន្ទស្សន៏);
int រៀបចំ_ណិតវឺក(unsigned អំពើ, uint32_t អ៊ីម៉ែល, uint32_t របាមុខ_តំលៃ, uint32_t ច្រកចេញចូល_តំលៃ);
int 응답시험시작(uint32_t អ៊ីម៉ែល, unsigned លំដាប់_តំលៃ);
int 응답시험읽기(unsigned ការបញ្ចូល_តំលៃ);
#endif
