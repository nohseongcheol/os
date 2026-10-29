#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ bibliotekë 없는 freestanding C++11 program_f5044b9b. 커널에 statik_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Përmbajtje_VALUE[] = "C++ → Java bërthamë_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Përmbajtje_VALUE)] = {};
    int Kartelë = hap_skedar("시험.txt", lexoj_shkruaj | 없으면만들기 | 내용비우기, 0600);
    if (Kartelë < 0) return 1;
    if (shkruaj_skedar_të_dhëna(Kartelë, Përmbajtje_VALUE, sizeof(Përmbajtje_VALUE)) != sizeof(Përmbajtje_VALUE)) return 2;
    if (kërko_skedar(Kartelë, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Kartelë, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Përmbajtje_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Përmbajtje_VALUE[순번]) return 5;
    if (파일자료읽기(Kartelë, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Kartelë) != -1 || 오류번호 != 38) return 7;
    if (mbyll_skedar(Kartelë) || mbyll_skedar(Kartelë) != -1 || 오류번호 != 9) return 8;
    Kartelë = hap_skedar("시험.txt", vetëm_për_lexim_VALUE);
    if (Kartelë < 0 || shkruaj_skedar_të_dhëna(Kartelë, Përmbajtje_VALUE, 1) != -1 || 오류번호 != 9) return 9;
    if (mbyll_skedar(Kartelë)) return 10;
    Kartelë = hap_skedar("시험.txt", lexoj_shkruaj | 끝에이어쓰기);
    if (Kartelë < 0 || kërko_skedar(Kartelë, 0, 처음기준) != 0 || shkruaj_skedar_të_dhëna(Kartelë, "!", 1) != 1 || skedar_ndryshoj_përmasat(Kartelë) != sizeof(Përmbajtje_VALUE) + 1) return 11;
    if (bashkësi_skedar_gjatësi(Kartelë, 2) || kërko_skedar(Kartelë, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (shkruaj_skedar_të_dhëna(Kartelë, "x", 1) != 1 || skedar_ndryshoj_përmasat(Kartelë) != 3 || mbyll_skedar(Kartelë)) return 13;
    Kartelë = hap_skedar("구멍.bin", lexoj_shkruaj | 없으면만들기 | 내용비우기, 0600);
    if (Kartelë < 0 || kërko_skedar(Kartelë, 3, 처음기준) != 3 || shkruaj_skedar_të_dhëna(Kartelë, "z", 1) != 1) return 14;
    if (kërko_skedar(Kartelë, 0, 처음기준) != 0 || 파일자료읽기(Kartelë, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (heq_skedar_futje_emër("구멍.bin") || skedar_ndryshoj_përmasat(Kartelë) != 4 || mbyll_skedar(Kartelë)) return 16;
    if (hap_skedar("구멍.bin", vetëm_për_lexim_VALUE) != -1 || 오류번호 != 2) return 17;
    if (hap_skedar("시험.txt", lexoj_shkruaj | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (hap_skedar("../금지", vetëm_për_lexim_VALUE) != -1) return 19;
    return 0;
}
