#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void ਤਿਆਰ_ਕਰੋ_ਨੈਟਵਰਕ(void);
void 통신망살피기(void);
int 통신끝점만들기(int ਟਾਈਪ_ਕਰੋ_ਸ਼੍ਰੇਣੀ);
int 망주소묶기(int ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ, uint32_t ਪਤਾ, unsigned 접속번호);
int 연결기다리기(int ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ);
void 통신주소재사용(int ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ);
int 망연결하기(int ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ, uint32_t ਪਤਾ, unsigned 접속번호);
int 망연결받기(int ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ);
int 통신읽기(int ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ, void *ਸਮੱਗਰੀ, unsigned 개수);
int 통신쓰기(int ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ, const void *ਸਮੱਗਰੀ, unsigned 개수);
int 전문보내기(int ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ, const void *ਸਮੱਗਰੀ, unsigned 개수, uint32_t ਪਤਾ, unsigned 접속번호);
int 전문받기(int ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ, void *ਸਮੱਗਰੀ, unsigned 개수);
unsigned 통신접속번호(int ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ);
unsigned 상대접속번호(int ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ);
uint32_t 상대통신주소(int ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ);
void ਬੰਦ_ਕਰੋ_ਨੈਟਵਰਕ(int ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ);
int ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਨਿਯੰਤਰਣ(int ਐਕਸ਼ਨ);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ਦਾਖਲਾ_ਕੀਮਤ, unsigned ਅਨੁਕ੍ਰਮਣਿਕਾ);
int ਰੂਪ_ਦਿਉ_ਨੈਟਵਰਕ(unsigned ਐਕਸ਼ਨ, uint32_t ਪਤਾ, uint32_t ਮਾਸਕ_ਕੀਮਤ, uint32_t ਗੇਟਵੇ_ਕੀਮਤ);
int 응답시험시작(uint32_t ਪਤਾ, unsigned ਕ੍ਰਮ_ਕੀਮਤ);
int 응답시험읽기(unsigned ਦਾਖਲਾ_ਕੀਮਤ);
#endif
