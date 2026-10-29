#include "통신규약.h"

int Mulai_pengguna_apl(int argumen) {
    (void)argumen;
    struct 인터넷통신주소 surel = {0};
    surel.surel_famili = cloud_famili;
    surel.nomor_port = 망차례짧은수(9260);
    surel.Alamat_internet.surel_VALUE = jaringan_bilangan_bulat(alamat_loopback);
    int server_VALUE = Buat_peserta(cloud_famili, Stream_jaringan, Stream_protokol_transportasi);
    if (server_VALUE < 0 || ikat_surel(server_VALUE, (struct 통신주소 *)&surel, sizeof(surel)) < 0 ||
        통신연결기다리기(server_VALUE, 4) < 0) return 1;
    if (terima_koneksi_jaringan(server_VALUE, 0, 0) != -1 || nomor_kesalahan != 11) return 2;
    int tamu_VALUE = Buat_peserta(cloud_famili, Stream_jaringan, Stream_protokol_transportasi);
    if (tamu_VALUE < 0 || CONNECT_jaringan(tamu_VALUE, (struct 통신주소 *)&surel, sizeof(surel)) < 0) return 3;
    int Sambung = terima_koneksi_jaringan(server_VALUE, 0, 0);
    if (Sambung < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_item[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int panjang_VALUE = tulis_file_data(tamu_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (panjang_VALUE <= 0) return 5;
        보낸수 += panjang_VALUE;
    }
    if (tulis_file_data(tamu_VALUE, 보낼것, 1) != -1 || nomor_kesalahan != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 BACK_VALUE EOF가 된다. */
    Tutup_file(tamu_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int panjang_VALUE = 파일자료읽기(Sambung, RECEIVED_item + RECEIVED_COUNT, sizeof(RECEIVED_item) - RECEIVED_COUNT);
        if (panjang_VALUE <= 0) return 7;
        RECEIVED_COUNT += panjang_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_item[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Sambung, RECEIVED_item, 1) != 0) return 9;
    if (tulis_file_data(Sambung, 보낼것, 1) != -1 || nomor_kesalahan != 32) return 10;
    Tutup_file(Sambung); Tutup_file(server_VALUE);
    const char hasil[] = "C posix-kor 연결형 komunikasi PASS\n";
    tulis_file_data(1, hasil, sizeof(hasil) - 1);
    return 0;
}
