#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ kirjasto 없는 freestanding C++11 ohjelma_f5044b9b. 커널에 staattinen_ARVO 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Sisältö_ARVO[] = "C++ → Java ydin_ARVO · 한글 😀";
    unsigned char lukea_ARVO[sizeof(Sisältö_ARVO)] = {};
    int tiedoston_nimi = avata_Tiedosto("testit.txt", luku_ja_kirjoitus | 없으면만들기 | 내용비우기, 0600);
    if (tiedoston_nimi < 0) return 1;
    if (kirjoitus_Tiedosto_data(tiedoston_nimi, Sisältö_ARVO, sizeof(Sisältö_ARVO)) != sizeof(Sisältö_ARVO)) return 2;
    if (hae_Tiedosto(tiedoston_nimi, 0, 처음기준) != 0) return 3;
    if (lukea_Tiedosto_data(tiedoston_nimi, lukea_ARVO, sizeof(lukea_ARVO)) != sizeof(lukea_ARVO)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Sisältö_ARVO); 순번++) if (lukea_ARVO[순번] != (unsigned char)Sisältö_ARVO[순번]) return 5;
    if (lukea_Tiedosto_data(tiedoston_nimi, lukea_ARVO, 1) != 0) return 6;
    if (vahvistaa_muutokset_Files(tiedoston_nimi) != -1 || virhenumero != 38) return 7;
    if (Sulje_Tiedosto(tiedoston_nimi) || Sulje_Tiedosto(tiedoston_nimi) != -1 || virhenumero != 9) return 8;
    tiedoston_nimi = avata_Tiedosto("testit.txt", vain_luku_ARVO);
    if (tiedoston_nimi < 0 || kirjoitus_Tiedosto_data(tiedoston_nimi, Sisältö_ARVO, 1) != -1 || virhenumero != 9) return 9;
    if (Sulje_Tiedosto(tiedoston_nimi)) return 10;
    tiedoston_nimi = avata_Tiedosto("testit.txt", luku_ja_kirjoitus | 끝에이어쓰기);
    if (tiedoston_nimi < 0 || hae_Tiedosto(tiedoston_nimi, 0, 처음기준) != 0 || kirjoitus_Tiedosto_data(tiedoston_nimi, "!", 1) != 1 || tiedostokoko(tiedoston_nimi) != sizeof(Sisältö_ARVO) + 1) return 11;
    if (ryhmä_Tiedosto_kesto(tiedoston_nimi, 2) || hae_Tiedosto(tiedoston_nimi, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (kirjoitus_Tiedosto_data(tiedoston_nimi, "x", 1) != 1 || tiedostokoko(tiedoston_nimi) != 3 || Sulje_Tiedosto(tiedoston_nimi)) return 13;
    tiedoston_nimi = avata_Tiedosto("구멍.bin", luku_ja_kirjoitus | 없으면만들기 | 내용비우기, 0600);
    if (tiedoston_nimi < 0 || hae_Tiedosto(tiedoston_nimi, 3, 처음기준) != 3 || kirjoitus_Tiedosto_data(tiedoston_nimi, "z", 1) != 1) return 14;
    if (hae_Tiedosto(tiedoston_nimi, 0, 처음기준) != 0 || lukea_Tiedosto_data(tiedoston_nimi, lukea_ARVO, 4) != 4 || lukea_ARVO[0] || lukea_ARVO[1] || lukea_ARVO[2] || lukea_ARVO[3] != 'z') return 15;
    if (poistaa_Tiedosto_merkintä_nimi("구멍.bin") || tiedostokoko(tiedoston_nimi) != 4 || Sulje_Tiedosto(tiedoston_nimi)) return 16;
    if (avata_Tiedosto("구멍.bin", vain_luku_ARVO) != -1 || virhenumero != 2) return 17;
    if (avata_Tiedosto("testit.txt", luku_ja_kirjoitus | 새파일만들기, 0600) != -1 || virhenumero != 17) return 18;
    if (avata_Tiedosto("../금지", vain_luku_ARVO) != -1) return 19;
    return 0;
}
