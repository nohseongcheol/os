#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ 라이브러리 없는 freestanding C++11 프로그램. 커널에 정적 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char 내용[] = "C++ → Java 커널 · 한글 😀";
    unsigned char 읽은값[sizeof(내용)] = {};
    int FICHIÉR = 파일열기("시험.txt", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600);
    if (FICHIÉR < 0) return 1;
    if (파일자료쓰기(FICHIÉR, 내용, sizeof(내용)) != sizeof(내용)) return 2;
    if (파일위치옮기기(FICHIÉR, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(FICHIÉR, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(내용); 순번++) if (읽은값[순번] != (unsigned char)내용[순번]) return 5;
    if (파일자료읽기(FICHIÉR, 읽은값, 1) != 0) return 6;
    if (파일저장확정(FICHIÉR) != -1 || 오류번호 != 38) return 7;
    if (파일닫기(FICHIÉR) || 파일닫기(FICHIÉR) != -1 || 오류번호 != 9) return 8;
    FICHIÉR = 파일열기("시험.txt", 읽기전용);
    if (FICHIÉR < 0 || 파일자료쓰기(FICHIÉR, 내용, 1) != -1 || 오류번호 != 9) return 9;
    if (파일닫기(FICHIÉR)) return 10;
    FICHIÉR = 파일열기("시험.txt", 읽고쓰기 | 끝에이어쓰기);
    if (FICHIÉR < 0 || 파일위치옮기기(FICHIÉR, 0, 처음기준) != 0 || 파일자료쓰기(FICHIÉR, "!", 1) != 1 || 파일크기(FICHIÉR) != sizeof(내용) + 1) return 11;
    if (파일길이정하기(FICHIÉR, 2) || 파일위치옮기기(FICHIÉR, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (파일자료쓰기(FICHIÉR, "x", 1) != 1 || 파일크기(FICHIÉR) != 3 || 파일닫기(FICHIÉR)) return 13;
    FICHIÉR = 파일열기("구멍.bin", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600);
    if (FICHIÉR < 0 || 파일위치옮기기(FICHIÉR, 3, 처음기준) != 3 || 파일자료쓰기(FICHIÉR, "z", 1) != 1) return 14;
    if (파일위치옮기기(FICHIÉR, 0, 처음기준) != 0 || 파일자료읽기(FICHIÉR, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (파일이름지우기("구멍.bin") || 파일크기(FICHIÉR) != 4 || 파일닫기(FICHIÉR)) return 16;
    if (파일열기("구멍.bin", 읽기전용) != -1 || 오류번호 != 2) return 17;
    if (파일열기("시험.txt", 읽고쓰기 | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (파일열기("../금지", 읽기전용) != -1) return 19;
    return 0;
}
