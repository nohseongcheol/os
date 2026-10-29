// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Baca 전용 Jalankan_perintah 묶음의 ELF32 validasi, argumen Maju_VALUE, 한 번에 한 ruang_pengguna Proses_VALUE Jalankan_perintah. */
public final class 실행관리 {
    static final int Mulai_pengguna_apl = 0x04000000;
    static final int pengguna_mengakhiri = 0x04400000;
    static final int foto_mengakhiri_surel = 0x04200000;
    static final int argumen_Mulai = 0x04300000;
    static int argumen_COUNT = 0;
    static int[] argumen_surel = new int[16];

    static boolean klip(int surel, int panjang_VALUE) {
        return surel >= Mulai_pengguna_apl && surel < pengguna_mengakhiri && panjang_VALUE >= 0 && panjang_VALUE <= pengguna_mengakhiri - surel;
    }

    static int 수(int surel) { return Memori_wilayah.urai_bilangan_bulat(surel); }
    static int 짧은수(int surel) { return Ponsel_VALUE.기억읽기(surel) | Ponsel_VALUE.기억읽기(surel + 1) << 8; }
    static void 수쓰기(int surel, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) Ponsel_VALUE.tulis_Memori(surel + INDEX, VALUE >>> (INDEX * 8));
    }

    static int grup_COUNT() {
        int surel = Ponsel_VALUE.실행묶음();
        int Ukuran = Ponsel_VALUE.실행묶음크기();
        if (Ukuran < 8 || 수(surel) != 0x50414b4a) return 0;
        int item_COUNT = 수(surel + 4);
        return item_COUNT >= 0 && item_COUNT <= 32 && item_COUNT <= (Ukuran - 8) / 24 ? item_COUNT : 0;
    }

    static void entri_Daftar() {
        for (int INDEX = 0; INDEX < grup_COUNT(); INDEX++) {
            int entri_VALUE = Ponsel_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int karakter_VALUE = 0; karakter_VALUE < 16 && Ponsel_VALUE.기억읽기(entri_VALUE + karakter_VALUE) != 0; karakter_VALUE++)
                SMS_Terminal.문자(Ponsel_VALUE.기억읽기(entri_VALUE + karakter_VALUE));
            SMS_Terminal.Tulis("\n");
        }
    }

    static int FIND_entri(int[] 입력, int jalankan, int panjang_VALUE) {
        if (panjang_VALUE <= 0 || panjang_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < grup_COUNT(); INDEX++) {
            int entri_VALUE = Ponsel_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = Ponsel_VALUE.기억읽기(entri_VALUE + panjang_VALUE) == 0;
            for (int karakter_VALUE = 0; karakter_VALUE < panjang_VALUE; karakter_VALUE++)
                if (입력[jalankan + karakter_VALUE] != Ponsel_VALUE.기억읽기(entri_VALUE + karakter_VALUE)) 같음 = false;
            if (같음) return entri_VALUE;
        }
        return 0;
    }

    static int validasi(int berkas, int panjang_VALUE) {
        if (panjang_VALUE < 52 || 수(berkas) != 0x464c457f || Ponsel_VALUE.기억읽기(berkas + 4) != 1
            || Ponsel_VALUE.기억읽기(berkas + 5) != 1 || Ponsel_VALUE.기억읽기(berkas + 6) != 1
            || 짧은수(berkas + 16) != 2 || 짧은수(berkas + 18) != 3 || 수(berkas + 20) != 1
            || 짧은수(berkas + 40) != 52 || 짧은수(berkas + 42) != 32) return -8;
        int entri_p_VALUE = 수(berkas + 24);
        int tabel_posisi = 수(berkas + 28);
        int item_COUNT = 짧은수(berkas + 44);
        if (item_COUNT == 0 || item_COUNT > 16 || tabel_posisi < 52 || tabel_posisi > panjang_VALUE - item_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < item_COUNT; INDEX++) {
            int LOOKUP_tabel = berkas + tabel_posisi + INDEX * 32;
            int 종류 = 수(LOOKUP_tabel);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Sambung/parser_48ee4b1b 미지원
            if (종류 != 1) continue;
            int posisi = 수(LOOKUP_tabel + 4), surel = 수(LOOKUP_tabel + 8), ukuran_file = 수(LOOKUP_tabel + 16), Memori_ukuran = 수(LOOKUP_tabel + 20);
            int ratakan_VALUE = 수(LOOKUP_tabel + 28);
            if (surel < Mulai_pengguna_apl || surel >= foto_mengakhiri_surel || Memori_ukuran < 0 || Memori_ukuran > foto_mengakhiri_surel - surel
                || ukuran_file < 0 || ukuran_file > Memori_ukuran || posisi < 0 || (ukuran_file > 0 && posisi > panjang_VALUE - ukuran_file)
                || (ratakan_VALUE != 0 && (ratakan_VALUE < 0 || (ratakan_VALUE & (ratakan_VALUE - 1)) != 0
                    || ((surel - posisi) & (ratakan_VALUE - 1)) != 0))) return -8;
            for (int depan_VALUE = 0; depan_VALUE < INDEX; depan_VALUE++) {
                int 이전 = berkas + tabel_posisi + depan_VALUE * 32;
                if (수(이전) == 1 && Memori_ukuran > 0 && 수(이전 + 20) > 0
                    && surel < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < surel + Memori_ukuran) return -8;
            }
            if ((수(LOOKUP_tabel + 24) & 1) != 0 && entri_p_VALUE >= surel && entri_p_VALUE - surel < ukuran_file) 실행가능 = true;
        }
        return 실행가능 ? entri_p_VALUE : -8;
    }

    static int Jalankan_perintah(int[] 입력, int jalankan, int panjang_VALUE) {
        while (jalankan < panjang_VALUE && 입력[jalankan] == ' ') jalankan++;
        int 끝 = jalankan;
        while (끝 < panjang_VALUE && 입력[끝] != ' ') 끝++;
        int entri_VALUE = FIND_entri(입력, jalankan, 끝 - jalankan);
        if (entri_VALUE == 0) return -2;
        int posisi = 수(entri_VALUE + 16), Ukuran = 수(entri_VALUE + 20);
        if (posisi < 8 + grup_COUNT() * 24 || Ukuran < 52 || posisi > Ponsel_VALUE.실행묶음크기() - Ukuran) return -8;
        int berkas = Ponsel_VALUE.실행묶음() + posisi;
        int entri_p_VALUE = validasi(berkas, Ukuran);
        if (entri_p_VALUE < 0) return entri_p_VALUE;
        Ponsel_VALUE.pengguna_bersihkan_Isi();
        int tabel_posisi = 수(berkas + 28), item_COUNT = 짧은수(berkas + 44);
        for (int INDEX = 0; INDEX < item_COUNT; INDEX++) {
            int LOOKUP_tabel = berkas + tabel_posisi + INDEX * 32;
            if (수(LOOKUP_tabel) != 1) continue;
            int 원본 = berkas + 수(LOOKUP_tabel + 4), tujuan_VALUE = 수(LOOKUP_tabel + 8), ukuran_file = 수(LOOKUP_tabel + 16);
            for (int byte_VALUE = 0; byte_VALUE < ukuran_file; byte_VALUE++) Ponsel_VALUE.tulis_Memori(tujuan_VALUE + byte_VALUE, Ponsel_VALUE.기억읽기(원본 + byte_VALUE));
        }
        argumen_COUNT = 0;
        int Store_VALUE = argumen_Mulai;
        while (끝 < panjang_VALUE) {
            while (끝 < panjang_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == panjang_VALUE) break;
            if (argumen_COUNT == argumen_surel.length) return -22;
            jalankan = 끝;
            while (끝 < panjang_VALUE && 입력[끝] != ' ') 끝++;
            argumen_surel[argumen_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - jalankan);
            for (int karakter_VALUE = jalankan; karakter_VALUE < 끝; karakter_VALUE++) 수쓰기(Store_VALUE + 4 + (karakter_VALUE - jalankan) * 4, 입력[karakter_VALUE]);
            Store_VALUE += 4 + (끝 - jalankan) * 4;
        }
        jaringan_tumpuk.CLEAN_Proses();
        파일서술자관리.Mulai_Proses();
        int hasil = Ponsel_VALUE.eksekusi_pengguna_apl(entri_p_VALUE, pengguna_mengakhiri - 16);
        파일서술자관리.CLEAN_Proses();
        jaringan_tumpuk.CLEAN_Proses();
        return hasil;
    }
}
