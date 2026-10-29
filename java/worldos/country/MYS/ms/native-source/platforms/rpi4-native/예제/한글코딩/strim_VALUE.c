#include "통신규약.h"

int Mula_pengguna_aplikasi(int 인수) {
    (void)인수;
    struct 인터넷통신주소 e_mel = {0};
    e_mel.e_mel_Keluarga = awan_Keluarga;
    e_mel.nombor_port = 망차례짧은수(9260);
    e_mel.alamat_Internet.e_mel_VALUE = rangkaian_integer(되돌림주소);
    int pelayan_VALUE = cipta_peserta(awan_Keluarga, strim_rangkaian, strim_protokol_pengangkutan);
    if (pelayan_VALUE < 0 || ikat_e_mel(pelayan_VALUE, (struct 통신주소 *)&e_mel, sizeof(e_mel)) < 0 ||
        통신연결기다리기(pelayan_VALUE, 4) < 0) return 1;
    if (terima_sambungan_rangkaian(pelayan_VALUE, 0, 0) != -1 || 오류번호 != 11) return 2;
    int tetamu_VALUE = cipta_peserta(awan_Keluarga, strim_rangkaian, strim_protokol_pengangkutan);
    if (tetamu_VALUE < 0 || CONNECT_rangkaian(tetamu_VALUE, (struct 통신주소 *)&e_mel, sizeof(e_mel)) < 0) return 3;
    int Sambung = terima_sambungan_rangkaian(pelayan_VALUE, 0, 0);
    if (Sambung < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_item[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int kepanjangan_VALUE = tulis_fail_data(tetamu_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (kepanjangan_VALUE <= 0) return 5;
        보낸수 += kepanjangan_VALUE;
    }
    if (tulis_fail_data(tetamu_VALUE, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 BACK_VALUE EOF가 된다. */
    Tutup_fail(tetamu_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int kepanjangan_VALUE = 파일자료읽기(Sambung, RECEIVED_item + RECEIVED_COUNT, sizeof(RECEIVED_item) - RECEIVED_COUNT);
        if (kepanjangan_VALUE <= 0) return 7;
        RECEIVED_COUNT += kepanjangan_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_item[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Sambung, RECEIVED_item, 1) != 0) return 9;
    if (tulis_fail_data(Sambung, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    Tutup_fail(Sambung); Tutup_fail(pelayan_VALUE);
    const char ukuran[] = "C posix-kor 연결형 통신 PASS\n";
    tulis_fail_data(1, ukuran, sizeof(ukuran) - 1);
    return 0;
}
