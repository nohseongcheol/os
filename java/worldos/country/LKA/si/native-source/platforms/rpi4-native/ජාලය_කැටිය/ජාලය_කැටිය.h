#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void පිළියෙල_කරන්න_ජාලය(void);
void 통신망살피기(void);
int 통신끝점만들기(int ටයිප්_කරන්න_ප්_රවර්ගය);
int 망주소묶기(int ගොනුව_හසුරුව, uint32_t යොමුව, unsigned 접속번호);
int 연결기다리기(int ගොනුව_හසුරුව);
void 통신주소재사용(int ගොනුව_හසුරුව);
int 망연결하기(int ගොනුව_හසුරුව, uint32_t යොමුව, unsigned 접속번호);
int 망연결받기(int ගොනුව_හසුරුව);
int 통신읽기(int ගොනුව_හසුරුව, void *දත්ත, unsigned 개수);
int 통신쓰기(int ගොනුව_හසුරුව, const void *දත්ත, unsigned 개수);
int 전문보내기(int ගොනුව_හසුරුව, const void *දත්ත, unsigned 개수, uint32_t යොමුව, unsigned 접속번호);
int 전문받기(int ගොනුව_හසුරුව, void *දත්ත, unsigned 개수);
unsigned 통신접속번호(int ගොනුව_හසුරුව);
unsigned 상대접속번호(int ගොනුව_හසුරුව);
uint32_t 상대통신주소(int ගොනුව_හසුරුව);
void වසන්න_ජාලය(int ගොනුව_හසුරුව);
int ගොනුව_මාරුව_පාලකය(int ක්_රීයාව);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned පිවිසුම_අගය, unsigned සූචිය);
int වින්_යාස_කරන්න_ජාලය(unsigned ක්_රීයාව, uint32_t යොමුව, uint32_t වසනය_අගය, uint32_t වාහල_අගය);
int 응답시험시작(uint32_t යොමුව, unsigned අනුපිළිවෙළ_අගය);
int 응답시험읽기(unsigned පිවිසුම_අගය);
#endif
