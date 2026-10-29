#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ puna 없는 freestanding C++11 kaupapa_f5044b9b. 커널에 pateko_uara 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Ihirangi_uara[] = "C++ → Java kākano_uara_0611a8a8 · 한글 😀";
    unsigned char 읽은값[sizeof(Ihirangi_uara)] = {};
    int Kōnae = tiwhikete_kōnae("시험.txt", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600);
    if (Kōnae < 0) return 1;
    if (tuhi_kōnae_raraunga(Kōnae, Ihirangi_uara, sizeof(Ihirangi_uara)) != sizeof(Ihirangi_uara)) return 2;
    if (kimi_kōnae(Kōnae, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Kōnae, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Ihirangi_uara); 순번++) if (읽은값[순번] != (unsigned char)Ihirangi_uara[순번]) return 5;
    if (파일자료읽기(Kōnae, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Kōnae) != -1 || 오류번호 != 38) return 7;
    if (kati_kōnae(Kōnae) || kati_kōnae(Kōnae) != -1 || 오류번호 != 9) return 8;
    Kōnae = tiwhikete_kōnae("시험.txt", pānui_anake_uara);
    if (Kōnae < 0 || tuhi_kōnae_raraunga(Kōnae, Ihirangi_uara, 1) != -1 || 오류번호 != 9) return 9;
    if (kati_kōnae(Kōnae)) return 10;
    Kōnae = tiwhikete_kōnae("시험.txt", 읽고쓰기 | 끝에이어쓰기);
    if (Kōnae < 0 || kimi_kōnae(Kōnae, 0, 처음기준) != 0 || tuhi_kōnae_raraunga(Kōnae, "!", 1) != 1 || kōnae_rahi(Kōnae) != sizeof(Ihirangi_uara) + 1) return 11;
    if (huinga_kōnae_roa(Kōnae, 2) || kimi_kōnae(Kōnae, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (tuhi_kōnae_raraunga(Kōnae, "x", 1) != 1 || kōnae_rahi(Kōnae) != 3 || kati_kōnae(Kōnae)) return 13;
    Kōnae = tiwhikete_kōnae("구멍.bin", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600);
    if (Kōnae < 0 || kimi_kōnae(Kōnae, 3, 처음기준) != 3 || tuhi_kōnae_raraunga(Kōnae, "z", 1) != 1) return 14;
    if (kimi_kōnae(Kōnae, 0, 처음기준) != 0 || 파일자료읽기(Kōnae, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (tango_kōnae_tāurunga_ingoa("구멍.bin") || kōnae_rahi(Kōnae) != 4 || kati_kōnae(Kōnae)) return 16;
    if (tiwhikete_kōnae("구멍.bin", pānui_anake_uara) != -1 || 오류번호 != 2) return 17;
    if (tiwhikete_kōnae("시험.txt", 읽고쓰기 | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (tiwhikete_kōnae("../금지", pānui_anake_uara) != -1) return 19;
    return 0;
}
