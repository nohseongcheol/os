#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ anaajaalee 없는 freestanding C++11 akumajiaa_f5044b9b. 커널에 jimatüsü_ajutuu 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char alu_ujatüü_ajutuu[] = "C++ → Java keetnerü_ajutuu · 한글 😀";
    unsigned char 읽은값[sizeof(alu_ujatüü_ajutuu)] = {};
    int anaajaalaa = 파일열기("시험.txt", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600);
    if (anaajaalaa < 0) return 1;
    if (ashajaa_anaajaalaa_atijaaya(anaajaalaa, alu_ujatüü_ajutuu, sizeof(alu_ujatüü_ajutuu)) != sizeof(alu_ujatüü_ajutuu)) return 2;
    if (파일위치옮기기(anaajaalaa, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(anaajaalaa, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(alu_ujatüü_ajutuu); 순번++) if (읽은값[순번] != (unsigned char)alu_ujatüü_ajutuu[순번]) return 5;
    if (파일자료읽기(anaajaalaa, 읽은값, 1) != 0) return 6;
    if (파일저장확정(anaajaalaa) != -1 || 오류번호 != 38) return 7;
    if (asürülaa_anaajaalaa(anaajaalaa) || asürülaa_anaajaalaa(anaajaalaa) != -1 || 오류번호 != 9) return 8;
    anaajaalaa = 파일열기("시험.txt", 읽기전용);
    if (anaajaalaa < 0 || ashajaa_anaajaalaa_atijaaya(anaajaalaa, alu_ujatüü_ajutuu, 1) != -1 || 오류번호 != 9) return 9;
    if (asürülaa_anaajaalaa(anaajaalaa)) return 10;
    anaajaalaa = 파일열기("시험.txt", 읽고쓰기 | 끝에이어쓰기);
    if (anaajaalaa < 0 || 파일위치옮기기(anaajaalaa, 0, 처음기준) != 0 || ashajaa_anaajaalaa_atijaaya(anaajaalaa, "!", 1) != 1 || 파일크기(anaajaalaa) != sizeof(alu_ujatüü_ajutuu) + 1) return 11;
    if (파일길이정하기(anaajaalaa, 2) || 파일위치옮기기(anaajaalaa, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (ashajaa_anaajaalaa_atijaaya(anaajaalaa, "x", 1) != 1 || 파일크기(anaajaalaa) != 3 || asürülaa_anaajaalaa(anaajaalaa)) return 13;
    anaajaalaa = 파일열기("구멍.bin", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600);
    if (anaajaalaa < 0 || 파일위치옮기기(anaajaalaa, 3, 처음기준) != 3 || ashajaa_anaajaalaa_atijaaya(anaajaalaa, "z", 1) != 1) return 14;
    if (파일위치옮기기(anaajaalaa, 0, 처음기준) != 0 || 파일자료읽기(anaajaalaa, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (파일이름지우기("구멍.bin") || 파일크기(anaajaalaa) != 4 || asürülaa_anaajaalaa(anaajaalaa)) return 16;
    if (파일열기("구멍.bin", 읽기전용) != -1 || 오류번호 != 2) return 17;
    if (파일열기("시험.txt", 읽고쓰기 | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (파일열기("../금지", 읽기전용) != -1) return 19;
    return 0;
}
