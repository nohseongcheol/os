#include "../명명/기계연결이름.h"
#include "Dosya_ABI.h"
// 표준 C++ kitaplık 없는 freestanding C++11 program_f5044b9b. 커널에 statik_değer 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char içerik_değer[] = "C++ → Java çekirdek_değer · 한글 😀";
    unsigned char 읽은값[sizeof(içerik_değer)] = {};
    int dosya = açık_Dosya("sınamalar.txt", R_W | 없으면만들기 | kesmek_içindekiler, 0600);
    if (dosya < 0) return 1;
    if (yazma_Dosya_veri(dosya, içerik_değer, sizeof(içerik_değer)) != sizeof(içerik_değer)) return 2;
    if (arama_Dosya(dosya, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(dosya, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(içerik_değer); 순번++) if (읽은값[순번] != (unsigned char)içerik_değer[순번]) return 5;
    if (파일자료읽기(dosya, 읽은값, 1) != 0) return 6;
    if (commit_Dosyalar(dosya) != -1 || hata_numarası != 38) return 7;
    if (Kapat_Dosya(dosya) || Kapat_Dosya(dosya) != -1 || hata_numarası != 9) return 8;
    dosya = açık_Dosya("sınamalar.txt", salt_okunur_değer);
    if (dosya < 0 || yazma_Dosya_veri(dosya, içerik_değer, 1) != -1 || hata_numarası != 9) return 9;
    if (Kapat_Dosya(dosya)) return 10;
    dosya = açık_Dosya("sınamalar.txt", R_W | 끝에이어쓰기);
    if (dosya < 0 || arama_Dosya(dosya, 0, 처음기준) != 0 || yazma_Dosya_veri(dosya, "!", 1) != 1 || dosya_boyutu(dosya) != sizeof(içerik_değer) + 1) return 11;
    if (küme_Dosya_süre(dosya, 2) || arama_Dosya(dosya, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (yazma_Dosya_veri(dosya, "x", 1) != 1 || dosya_boyutu(dosya) != 3 || Kapat_Dosya(dosya)) return 13;
    dosya = açık_Dosya("구멍.bin", R_W | 없으면만들기 | kesmek_içindekiler, 0600);
    if (dosya < 0 || arama_Dosya(dosya, 3, 처음기준) != 3 || yazma_Dosya_veri(dosya, "z", 1) != 1) return 14;
    if (arama_Dosya(dosya, 0, 처음기준) != 0 || 파일자료읽기(dosya, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (kaldırmak_Dosya_girdi_ad("구멍.bin") || dosya_boyutu(dosya) != 4 || Kapat_Dosya(dosya)) return 16;
    if (açık_Dosya("구멍.bin", salt_okunur_değer) != -1 || hata_numarası != 2) return 17;
    if (açık_Dosya("sınamalar.txt", R_W | 새파일만들기, 0600) != -1 || hata_numarası != 17) return 18;
    if (açık_Dosya("../금지", salt_okunur_değer) != -1) return 19;
    return 0;
}
