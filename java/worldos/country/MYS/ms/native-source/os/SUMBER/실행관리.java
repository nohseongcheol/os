// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Baca 전용 laksanakan_perintah 묶음의 ELF32 sahkan, 인수 Mara_VALUE, 한 번에 한 ruang_pengguna Proses_VALUE laksanakan_perintah. */
public final class 실행관리 {
    static final int Mula_pengguna_aplikasi = 0x04000000;
    static final int pengguna_tamat = 0x04400000;
    static final int imej_tamat_e_mel = 0x04200000;
    static final int argumen_Mula = 0x04300000;
    static int argumen_COUNT = 0;
    static int[] argumen_e_mel = new int[16];

    static boolean klip(int e_mel, int kepanjangan_VALUE) {
        return e_mel >= Mula_pengguna_aplikasi && e_mel < pengguna_tamat && kepanjangan_VALUE >= 0 && kepanjangan_VALUE <= pengguna_tamat - e_mel;
    }

    static int 수(int e_mel) { return Memori_rantau.hurai_integer(e_mel); }
    static int 짧은수(int e_mel) { return peranti_VALUE.기억읽기(e_mel) | peranti_VALUE.기억읽기(e_mel + 1) << 8; }
    static void 수쓰기(int e_mel, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) peranti_VALUE.tulis_Memori(e_mel + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Kumpulan_COUNT() {
        int e_mel = peranti_VALUE.fail_boleh_laku_pakej();
        int Saiz = peranti_VALUE.fail_boleh_laku_pakej_saiz();
        if (Saiz < 8 || 수(e_mel) != 0x50414b4a) return 0;
        int item_COUNT = 수(e_mel + 4);
        return item_COUNT >= 0 && item_COUNT <= 32 && item_COUNT <= (Saiz - 8) / 24 ? item_COUNT : 0;
    }

    static void pemasukan_Senarai() {
        for (int INDEX = 0; INDEX < Kumpulan_COUNT(); INDEX++) {
            int pemasukan_VALUE = peranti_VALUE.fail_boleh_laku_pakej() + 8 + INDEX * 24;
            for (int aksara_VALUE = 0; aksara_VALUE < 16 && peranti_VALUE.기억읽기(pemasukan_VALUE + aksara_VALUE) != 0; aksara_VALUE++)
                SMS_Terminal.문자(peranti_VALUE.기억읽기(pemasukan_VALUE + aksara_VALUE));
            SMS_Terminal.Tulis("\n");
        }
    }

    static int Cari_pemasukan(int[] 입력, int Jalan, int kepanjangan_VALUE) {
        if (kepanjangan_VALUE <= 0 || kepanjangan_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < Kumpulan_COUNT(); INDEX++) {
            int pemasukan_VALUE = peranti_VALUE.fail_boleh_laku_pakej() + 8 + INDEX * 24;
            boolean 같음 = peranti_VALUE.기억읽기(pemasukan_VALUE + kepanjangan_VALUE) == 0;
            for (int aksara_VALUE = 0; aksara_VALUE < kepanjangan_VALUE; aksara_VALUE++)
                if (입력[Jalan + aksara_VALUE] != peranti_VALUE.기억읽기(pemasukan_VALUE + aksara_VALUE)) 같음 = false;
            if (같음) return pemasukan_VALUE;
        }
        return 0;
    }

    static int sahkan(int Fail, int kepanjangan_VALUE) {
        if (kepanjangan_VALUE < 52 || 수(Fail) != 0x464c457f || peranti_VALUE.기억읽기(Fail + 4) != 1
            || peranti_VALUE.기억읽기(Fail + 5) != 1 || peranti_VALUE.기억읽기(Fail + 6) != 1
            || 짧은수(Fail + 16) != 2 || 짧은수(Fail + 18) != 3 || 수(Fail + 20) != 1
            || 짧은수(Fail + 40) != 52 || 짧은수(Fail + 42) != 32) return -8;
        int titik_permulaan_VALUE = 수(Fail + 24);
        int jadual_jawatan = 수(Fail + 28);
        int item_COUNT = 짧은수(Fail + 44);
        if (item_COUNT == 0 || item_COUNT > 16 || jadual_jawatan < 52 || jadual_jawatan > kepanjangan_VALUE - item_COUNT * 32) return -8;
        boolean teknologi_maklumat_fail_boleh_laku = false;
        for (int INDEX = 0; INDEX < item_COUNT; INDEX++) {
            int Carian_jadual = Fail + jadual_jawatan + INDEX * 32;
            int 종류 = 수(Carian_jadual);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Sambung/penghurai_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Kedudukan = 수(Carian_jadual + 4), e_mel = 수(Carian_jadual + 8), saiz_fail = 수(Carian_jadual + 16), Memori_saiz = 수(Carian_jadual + 20);
            int jajar_VALUE = 수(Carian_jadual + 28);
            if (e_mel < Mula_pengguna_aplikasi || e_mel >= imej_tamat_e_mel || Memori_saiz < 0 || Memori_saiz > imej_tamat_e_mel - e_mel
                || saiz_fail < 0 || saiz_fail > Memori_saiz || Kedudukan < 0 || (saiz_fail > 0 && Kedudukan > kepanjangan_VALUE - saiz_fail)
                || (jajar_VALUE != 0 && (jajar_VALUE < 0 || (jajar_VALUE & (jajar_VALUE - 1)) != 0
                    || ((e_mel - Kedudukan) & (jajar_VALUE - 1)) != 0))) return -8;
            for (int hadapan_VALUE = 0; hadapan_VALUE < INDEX; hadapan_VALUE++) {
                int 이전 = Fail + jadual_jawatan + hadapan_VALUE * 32;
                if (수(이전) == 1 && Memori_saiz > 0 && 수(이전 + 20) > 0
                    && e_mel < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < e_mel + Memori_saiz) return -8;
            }
            if ((수(Carian_jadual + 24) & 1) != 0 && titik_permulaan_VALUE >= e_mel && titik_permulaan_VALUE - e_mel < saiz_fail) teknologi_maklumat_fail_boleh_laku = true;
        }
        return teknologi_maklumat_fail_boleh_laku ? titik_permulaan_VALUE : -8;
    }

    static int laksanakan_perintah(int[] 입력, int Jalan, int kepanjangan_VALUE) {
        while (Jalan < kepanjangan_VALUE && 입력[Jalan] == ' ') Jalan++;
        int 끝 = Jalan;
        while (끝 < kepanjangan_VALUE && 입력[끝] != ' ') 끝++;
        int pemasukan_VALUE = Cari_pemasukan(입력, Jalan, 끝 - Jalan);
        if (pemasukan_VALUE == 0) return -2;
        int Kedudukan = 수(pemasukan_VALUE + 16), Saiz = 수(pemasukan_VALUE + 20);
        if (Kedudukan < 8 + Kumpulan_COUNT() * 24 || Saiz < 52 || Kedudukan > peranti_VALUE.fail_boleh_laku_pakej_saiz() - Saiz) return -8;
        int Fail = peranti_VALUE.fail_boleh_laku_pakej() + Kedudukan;
        int titik_permulaan_VALUE = sahkan(Fail, Saiz);
        if (titik_permulaan_VALUE < 0) return titik_permulaan_VALUE;
        peranti_VALUE.pengguna_buang_TOC();
        int jadual_jawatan = 수(Fail + 28), item_COUNT = 짧은수(Fail + 44);
        for (int INDEX = 0; INDEX < item_COUNT; INDEX++) {
            int Carian_jadual = Fail + jadual_jawatan + INDEX * 32;
            if (수(Carian_jadual) != 1) continue;
            int 원본 = Fail + 수(Carian_jadual + 4), destinasi_VALUE = 수(Carian_jadual + 8), saiz_fail = 수(Carian_jadual + 16);
            for (int bait_VALUE = 0; bait_VALUE < saiz_fail; bait_VALUE++) peranti_VALUE.tulis_Memori(destinasi_VALUE + bait_VALUE, peranti_VALUE.기억읽기(원본 + bait_VALUE));
        }
        argumen_COUNT = 0;
        int stor_VALUE = argumen_Mula;
        while (끝 < kepanjangan_VALUE) {
            while (끝 < kepanjangan_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == kepanjangan_VALUE) break;
            if (argumen_COUNT == argumen_e_mel.length) return -22;
            Jalan = 끝;
            while (끝 < kepanjangan_VALUE && 입력[끝] != ' ') 끝++;
            argumen_e_mel[argumen_COUNT++] = stor_VALUE;
            수쓰기(stor_VALUE, 끝 - Jalan);
            for (int aksara_VALUE = Jalan; aksara_VALUE < 끝; aksara_VALUE++) 수쓰기(stor_VALUE + 4 + (aksara_VALUE - Jalan) * 4, 입력[aksara_VALUE]);
            stor_VALUE += 4 + (끝 - Jalan) * 4;
        }
        rangkaian_tindan.CLEAN_Proses();
        파일서술자관리.Mula_Proses();
        int ukuran = peranti_VALUE.jalankan_pengguna_aplikasi(titik_permulaan_VALUE, pengguna_tamat - 16);
        파일서술자관리.CLEAN_Proses();
        rangkaian_tindan.CLEAN_Proses();
        return ukuran;
    }
}
