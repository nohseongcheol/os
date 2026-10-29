#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ library 없는 freestanding C++11 app_f5044b9b. 커널에 hindi_nababago_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Nilalaman_VALUE[] = "C++ → Java kernel_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Nilalaman_VALUE)] = {};
    int file = buksan_file("시험.txt", nababasa_nasusulatan | 없으면만들기 | 내용비우기, 0600);
    if (file < 0) return 1;
    if (sumulat_file_data(file, Nilalaman_VALUE, sizeof(Nilalaman_VALUE)) != sizeof(Nilalaman_VALUE)) return 2;
    if (i_seek_file(file, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(file, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Nilalaman_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Nilalaman_VALUE[순번]) return 5;
    if (파일자료읽기(file, 읽은값, 1) != 0) return 6;
    if (파일저장확정(file) != -1 || 오류번호 != 38) return 7;
    if (isara_file(file) || isara_file(file) != -1 || 오류번호 != 9) return 8;
    file = buksan_file("시험.txt", mababasa_lamang_VALUE);
    if (file < 0 || sumulat_file_data(file, Nilalaman_VALUE, 1) != -1 || 오류번호 != 9) return 9;
    if (isara_file(file)) return 10;
    file = buksan_file("시험.txt", nababasa_nasusulatan | 끝에이어쓰기);
    if (file < 0 || i_seek_file(file, 0, 처음기준) != 0 || sumulat_file_data(file, "!", 1) != 1 || file_sukat(file) != sizeof(Nilalaman_VALUE) + 1) return 11;
    if (set_file_haba(file, 2) || i_seek_file(file, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (sumulat_file_data(file, "x", 1) != 1 || file_sukat(file) != 3 || isara_file(file)) return 13;
    file = buksan_file("구멍.bin", nababasa_nasusulatan | 없으면만들기 | 내용비우기, 0600);
    if (file < 0 || i_seek_file(file, 3, 처음기준) != 3 || sumulat_file_data(file, "z", 1) != 1) return 14;
    if (i_seek_file(file, 0, 처음기준) != 0 || 파일자료읽기(file, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (tanggalin_file_pagpasok_pangalan("구멍.bin") || file_sukat(file) != 4 || isara_file(file)) return 16;
    if (buksan_file("구멍.bin", mababasa_lamang_VALUE) != -1 || 오류번호 != 2) return 17;
    if (buksan_file("시험.txt", nababasa_nasusulatan | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (buksan_file("../금지", mababasa_lamang_VALUE) != -1) return 19;
    return 0;
}
