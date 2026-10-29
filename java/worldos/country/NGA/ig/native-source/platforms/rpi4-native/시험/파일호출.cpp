#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ ọbaakwụkwọ 없는 freestanding C++11 app_f5044b9b. 커널에 adịmgbanwò_valuu 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char ndịnà_valuu[] = "C++ → Java mkpụrụobī_kọmpùta_valuu · 한글 😀";
    unsigned char 읽은값[sizeof(ndịnà_valuu)] = {};
    int Faịlụ = mepee_ọbọakwụkwọ("시험.txt", gụọ_dèe | 없으면만들기 | 내용비우기, 0600);
    if (Faịlụ < 0) return 1;
    if (dee_ọbọakwụkwọ_datà(Faịlụ, ndịnà_valuu, sizeof(ndịnà_valuu)) != sizeof(ndịnà_valuu)) return 2;
    if (ọchịchọ_ọbọakwụkwọ(Faịlụ, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Faịlụ, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(ndịnà_valuu); 순번++) if (읽은값[순번] != (unsigned char)ndịnà_valuu[순번]) return 5;
    if (파일자료읽기(Faịlụ, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Faịlụ) != -1 || 오류번호 != 38) return 7;
    if (mmechi_ọbọakwụkwọ(Faịlụ) || mmechi_ọbọakwụkwọ(Faịlụ) != -1 || 오류번호 != 9) return 8;
    Faịlụ = mepee_ọbọakwụkwọ("시험.txt", ọgụgụ_naanị_valuu);
    if (Faịlụ < 0 || dee_ọbọakwụkwọ_datà(Faịlụ, ndịnà_valuu, 1) != -1 || 오류번호 != 9) return 9;
    if (mmechi_ọbọakwụkwọ(Faịlụ)) return 10;
    Faịlụ = mepee_ọbọakwụkwọ("시험.txt", gụọ_dèe | 끝에이어쓰기);
    if (Faịlụ < 0 || ọchịchọ_ọbọakwụkwọ(Faịlụ, 0, 처음기준) != 0 || dee_ọbọakwụkwọ_datà(Faịlụ, "!", 1) != 1 || ọbọakwụkwọ_ụha(Faịlụ) != sizeof(ndịnà_valuu) + 1) return 11;
    if (Seti_ọbọakwụkwọ_ogologo(Faịlụ, 2) || ọchịchọ_ọbọakwụkwọ(Faịlụ, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (dee_ọbọakwụkwọ_datà(Faịlụ, "x", 1) != 1 || ọbọakwụkwọ_ụha(Faịlụ) != 3 || mmechi_ọbọakwụkwọ(Faịlụ)) return 13;
    Faịlụ = mepee_ọbọakwụkwọ("구멍.bin", gụọ_dèe | 없으면만들기 | 내용비우기, 0600);
    if (Faịlụ < 0 || ọchịchọ_ọbọakwụkwọ(Faịlụ, 3, 처음기준) != 3 || dee_ọbọakwụkwọ_datà(Faịlụ, "z", 1) != 1) return 14;
    if (ọchịchọ_ọbọakwụkwọ(Faịlụ, 0, 처음기준) != 0 || 파일자료읽기(Faịlụ, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (wepụ_ọbọakwụkwọ_ndebà_akara_ahà("구멍.bin") || ọbọakwụkwọ_ụha(Faịlụ) != 4 || mmechi_ọbọakwụkwọ(Faịlụ)) return 16;
    if (mepee_ọbọakwụkwọ("구멍.bin", ọgụgụ_naanị_valuu) != -1 || 오류번호 != 2) return 17;
    if (mepee_ọbọakwụkwọ("시험.txt", gụọ_dèe | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (mepee_ọbọakwụkwọ("../금지", ọgụgụ_naanị_valuu) != -1) return 19;
    return 0;
}
