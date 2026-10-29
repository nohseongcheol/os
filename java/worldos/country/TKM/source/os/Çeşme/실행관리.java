// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Oka 전용 ýerine_ýetir_buýruk 묶음의 ELF32 tassykla, 인수 ugrukdyr_baha, 한 번에 한 ulanyjy Proses_baha ýerine_ýetir_buýruk. */
public final class 실행관리 {
    static final int başlat_ulanyjy_programma = 0x04000000;
    static final int ulanyjy_tamamla = 0x04400000;
    static final int surat_tamamla_salgy = 0x04200000;
    static final int argument_başlat = 0x04300000;
    static int 인수수 = 0;
    static int[] argument_salgy = new int[16];

    static boolean klip(int salgy, int dowamlylyk_baha) {
        return salgy >= başlat_ulanyjy_programma && salgy < ulanyjy_tamamla && dowamlylyk_baha >= 0 && dowamlylyk_baha <= ulanyjy_tamamla - salgy;
    }

    static int 수(int salgy) { return 기억공간.seljer_bitin(salgy); }
    static int 짧은수(int salgy) { return enjam_baha.기억읽기(salgy) | enjam_baha.기억읽기(salgy + 1) << 8; }
    static void 수쓰기(int salgy, int baha) {
        for (int indeks = 0; indeks < 4; indeks++) enjam_baha.ýaz_ýat(salgy + indeks, baha >>> (indeks * 8));
    }

    static int 묶음개수() {
        int salgy = enjam_baha.실행묶음();
        int Ululyk = enjam_baha.실행묶음크기();
        if (Ululyk < 8 || 수(salgy) != 0x50414b4a) return 0;
        int 개수 = 수(salgy + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (Ululyk - 8) / 24 ? 개수 : 0;
    }

    static void girizmeklik_Sanaw() {
        for (int indeks = 0; indeks < 묶음개수(); indeks++) {
            int girizmeklik_baha = enjam_baha.실행묶음() + 8 + indeks * 24;
            for (int nyşan_baha_068c2631 = 0; nyşan_baha_068c2631 < 16 && enjam_baha.기억읽기(girizmeklik_baha + nyşan_baha_068c2631) != 0; nyşan_baha_068c2631++)
                문자단말.문자(enjam_baha.기억읽기(girizmeklik_baha + nyşan_baha_068c2631));
            문자단말.Ýaz("\n");
        }
    }

    static int tap_girizmeklik(int[] 입력, int Bitir, int dowamlylyk_baha) {
        if (dowamlylyk_baha <= 0 || dowamlylyk_baha >= 16) return 0;
        for (int indeks = 0; indeks < 묶음개수(); indeks++) {
            int girizmeklik_baha = enjam_baha.실행묶음() + 8 + indeks * 24;
            boolean 같음 = enjam_baha.기억읽기(girizmeklik_baha + dowamlylyk_baha) == 0;
            for (int nyşan_baha_068c2631 = 0; nyşan_baha_068c2631 < dowamlylyk_baha; nyşan_baha_068c2631++)
                if (입력[Bitir + nyşan_baha_068c2631] != enjam_baha.기억읽기(girizmeklik_baha + nyşan_baha_068c2631)) 같음 = false;
            if (같음) return girizmeklik_baha;
        }
        return 0;
    }

    static int tassykla(int Faýl, int dowamlylyk_baha) {
        if (dowamlylyk_baha < 52 || 수(Faýl) != 0x464c457f || enjam_baha.기억읽기(Faýl + 4) != 1
            || enjam_baha.기억읽기(Faýl + 5) != 1 || enjam_baha.기억읽기(Faýl + 6) != 1
            || 짧은수(Faýl + 16) != 2 || 짧은수(Faýl + 18) != 3 || 수(Faýl + 20) != 1
            || 짧은수(Faýl + 40) != 52 || 짧은수(Faýl + 42) != 32) return -8;
        int girizmeklik_utuk_baha = 수(Faýl + 24);
        int 표위치 = 수(Faýl + 28);
        int 개수 = 짧은수(Faýl + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > dowamlylyk_baha - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int indeks = 0; indeks < 개수; indeks++) {
            int 표 = Faýl + 표위치 + indeks * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Birikme/해석기 미지원
            if (종류 != 1) continue;
            int 위치 = 수(표 + 4), salgy = 수(표 + 8), faýl_ölçegi_üýtget = 수(표 + 16), ýat_ölçegi_üýtget = 수(표 + 20);
            int deňle_baha = 수(표 + 28);
            if (salgy < başlat_ulanyjy_programma || salgy >= surat_tamamla_salgy || ýat_ölçegi_üýtget < 0 || ýat_ölçegi_üýtget > surat_tamamla_salgy - salgy
                || faýl_ölçegi_üýtget < 0 || faýl_ölçegi_üýtget > ýat_ölçegi_üýtget || 위치 < 0 || (faýl_ölçegi_üýtget > 0 && 위치 > dowamlylyk_baha - faýl_ölçegi_üýtget)
                || (deňle_baha != 0 && (deňle_baha < 0 || (deňle_baha & (deňle_baha - 1)) != 0
                    || ((salgy - 위치) & (deňle_baha - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < indeks; 앞++) {
                int 이전 = Faýl + 표위치 + 앞 * 32;
                if (수(이전) == 1 && ýat_ölçegi_üýtget > 0 && 수(이전 + 20) > 0
                    && salgy < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < salgy + ýat_ölçegi_üýtget) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && girizmeklik_utuk_baha >= salgy && girizmeklik_utuk_baha - salgy < faýl_ölçegi_üýtget) 실행가능 = true;
        }
        return 실행가능 ? girizmeklik_utuk_baha : -8;
    }

    static int ýerine_ýetir_buýruk(int[] 입력, int Bitir, int dowamlylyk_baha) {
        while (Bitir < dowamlylyk_baha && 입력[Bitir] == ' ') Bitir++;
        int 끝 = Bitir;
        while (끝 < dowamlylyk_baha && 입력[끝] != ' ') 끝++;
        int girizmeklik_baha = tap_girizmeklik(입력, Bitir, 끝 - Bitir);
        if (girizmeklik_baha == 0) return -2;
        int 위치 = 수(girizmeklik_baha + 16), Ululyk = 수(girizmeklik_baha + 20);
        if (위치 < 8 + 묶음개수() * 24 || Ululyk < 52 || 위치 > enjam_baha.실행묶음크기() - Ululyk) return -8;
        int Faýl = enjam_baha.실행묶음() + 위치;
        int girizmeklik_utuk_baha = tassykla(Faýl, Ululyk);
        if (girizmeklik_utuk_baha < 0) return girizmeklik_utuk_baha;
        enjam_baha.ulanyjy_arassala_TOC();
        int 표위치 = 수(Faýl + 28), 개수 = 짧은수(Faýl + 44);
        for (int indeks = 0; indeks < 개수; indeks++) {
            int 표 = Faýl + 표위치 + indeks * 32;
            if (수(표) != 1) continue;
            int 원본 = Faýl + 수(표 + 4), barylmaly_ýer_baha = 수(표 + 8), faýl_ölçegi_üýtget = 수(표 + 16);
            for (int baýt_baha = 0; baýt_baha < faýl_ölçegi_üýtget; baýt_baha++) enjam_baha.ýaz_ýat(barylmaly_ýer_baha + baýt_baha, enjam_baha.기억읽기(원본 + baýt_baha));
        }
        인수수 = 0;
        int Store_baha = argument_başlat;
        while (끝 < dowamlylyk_baha) {
            while (끝 < dowamlylyk_baha && 입력[끝] == ' ') 끝++;
            if (끝 == dowamlylyk_baha) break;
            if (인수수 == argument_salgy.length) return -22;
            Bitir = 끝;
            while (끝 < dowamlylyk_baha && 입력[끝] != ' ') 끝++;
            argument_salgy[인수수++] = Store_baha;
            수쓰기(Store_baha, 끝 - Bitir);
            for (int nyşan_baha_068c2631 = Bitir; nyşan_baha_068c2631 < 끝; nyşan_baha_068c2631++) 수쓰기(Store_baha + 4 + (nyşan_baha_068c2631 - Bitir) * 4, 입력[nyşan_baha_068c2631]);
            Store_baha += 4 + (끝 - Bitir) * 4;
        }
        Tor_Desse.Päkize_Proses();
        파일서술자관리.başlat_Proses();
        int 결과 = enjam_baha.işe_goýber_ulanyjy_programma(girizmeklik_utuk_baha, ulanyjy_tamamla - 16);
        파일서술자관리.Päkize_Proses();
        Tor_Desse.Päkize_Proses();
        return 결과;
    }
}
