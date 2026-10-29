#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void ಸಿದ್ಧಪಡಿಸು_ನೆಟ್_ವರ್ಕ್(void);
void 통신망살피기(void);
int 통신끝점만들기(int ಪ್ರಕಾರ_ವರ್ಗ);
int 망주소묶기(int ಫೈಲ್_ಹ್ಯಾಂಡಲ್, uint32_t ಇಮೇಲ್, unsigned ಪೋರ್ಟ್_ಸಂಖ್ಯೆ);
int 연결기다리기(int ಫೈಲ್_ಹ್ಯಾಂಡಲ್);
void 통신주소재사용(int ಫೈಲ್_ಹ್ಯಾಂಡಲ್);
int 망연결하기(int ಫೈಲ್_ಹ್ಯಾಂಡಲ್, uint32_t ಇಮೇಲ್, unsigned ಪೋರ್ಟ್_ಸಂಖ್ಯೆ);
int 망연결받기(int ಫೈಲ್_ಹ್ಯಾಂಡಲ್);
int 통신읽기(int ಫೈಲ್_ಹ್ಯಾಂಡಲ್, void *ಡೇಟಾ, unsigned 개수);
int 통신쓰기(int ಫೈಲ್_ಹ್ಯಾಂಡಲ್, const void *ಡೇಟಾ, unsigned 개수);
int 전문보내기(int ಫೈಲ್_ಹ್ಯಾಂಡಲ್, const void *ಡೇಟಾ, unsigned 개수, uint32_t ಇಮೇಲ್, unsigned ಪೋರ್ಟ್_ಸಂಖ್ಯೆ);
int 전문받기(int ಫೈಲ್_ಹ್ಯಾಂಡಲ್, void *ಡೇಟಾ, unsigned 개수);
unsigned ನೆಟ್_ವರ್ಕ್_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ(int ಫೈಲ್_ಹ್ಯಾಂಡಲ್);
unsigned ಪೀರ್_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ(int ಫೈಲ್_ಹ್ಯಾಂಡಲ್);
uint32_t 상대통신주소(int ಫೈಲ್_ಹ್ಯಾಂಡಲ್);
void ಮುಚ್ಚು_ನೆಟ್_ವರ್ಕ್(int ಫೈಲ್_ಹ್ಯಾಂಡಲ್);
int ಫೈಲ್_ವರ್ಗಾವಣೆ_ನಿಯಂತ್ರಣ(int ಹಕ್ರಿಯೆ);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ನಮೂದು_ಮೌಲ್ಯ, unsigned ಪದಸೂಚಿ);
int ಕಾನ್ಫಿಗರ್_ಮಾಡಿ_ನೆಟ್_ವರ್ಕ್(unsigned ಹಕ್ರಿಯೆ, uint32_t ಇಮೇಲ್, uint32_t ಮುಖವಾಡ_ಮೌಲ್ಯ, uint32_t ಗೇಟ್_ವೇ_ಮೌಲ್ಯ);
int 응답시험시작(uint32_t ಇಮೇಲ್, unsigned ಕ್ರಮ_ಮೌಲ್ಯ);
int 응답시험읽기(unsigned ನಮೂದು_ಮೌಲ್ಯ);
#endif
