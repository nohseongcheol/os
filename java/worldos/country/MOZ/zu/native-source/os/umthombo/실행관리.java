// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Funda 전용 yenza_umyalo 묶음의 ELF32 qinisekisa, 인수 dlulisela_phambili_inani, 한 번에 한 umsebenzisi Inqubo_inani yenza_umyalo. */
public final class 실행관리 {
    static final int qala_umsebenzisi_i_app = 0x04000000;
    static final int umsebenzisi_yekisa = 0x04400000;
    static final int isithombe_yekisa_ikheli = 0x04200000;
    static final int i_agumenti_qala = 0x04300000;
    static int 인수수 = 0;
    static int[] i_agumenti_ikheli = new int[16];

    static boolean isiqeshana(int ikheli, int ubude_inani) {
        return ikheli >= qala_umsebenzisi_i_app && ikheli < umsebenzisi_yekisa && ubude_inani >= 0 && ubude_inani <= umsebenzisi_yekisa - ikheli;
    }

    static int 수(int ikheli) { return 기억공간.zawula_inamba(ikheli); }
    static int 짧은수(int ikheli) { return idivayisi_inani.기억읽기(ikheli) | idivayisi_inani.기억읽기(ikheli + 1) << 8; }
    static void 수쓰기(int ikheli, int inani) {
        for (int thola_inkomba = 0; thola_inkomba < 4; thola_inkomba++) idivayisi_inani.bhala_inkumbulo(ikheli + thola_inkomba, inani >>> (thola_inkomba * 8));
    }

    static int 묶음개수() {
        int ikheli = idivayisi_inani.실행묶음();
        int Ubungako = idivayisi_inani.실행묶음크기();
        if (Ubungako < 8 || 수(ikheli) != 0x50414b4a) return 0;
        int 개수 = 수(ikheli + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (Ubungako - 8) / 24 ? 개수 : 0;
    }

    static void okufakwayo_Uhlu() {
        for (int thola_inkomba = 0; thola_inkomba < 묶음개수(); thola_inkomba++) {
            int okufakwayo_inani = idivayisi_inani.실행묶음() + 8 + thola_inkomba * 24;
            for (int uhlamvusimo_inani = 0; uhlamvusimo_inani < 16 && idivayisi_inani.기억읽기(okufakwayo_inani + uhlamvusimo_inani) != 0; uhlamvusimo_inani++)
                문자단말.문자(idivayisi_inani.기억읽기(okufakwayo_inani + uhlamvusimo_inani));
            문자단말.Bhala("\n");
        }
    }

    static int thola_okufakwayo(int[] 입력, int Sebenzisa, int ubude_inani) {
        if (ubude_inani <= 0 || ubude_inani >= 16) return 0;
        for (int thola_inkomba = 0; thola_inkomba < 묶음개수(); thola_inkomba++) {
            int okufakwayo_inani = idivayisi_inani.실행묶음() + 8 + thola_inkomba * 24;
            boolean 같음 = idivayisi_inani.기억읽기(okufakwayo_inani + ubude_inani) == 0;
            for (int uhlamvusimo_inani = 0; uhlamvusimo_inani < ubude_inani; uhlamvusimo_inani++)
                if (입력[Sebenzisa + uhlamvusimo_inani] != idivayisi_inani.기억읽기(okufakwayo_inani + uhlamvusimo_inani)) 같음 = false;
            if (같음) return okufakwayo_inani;
        }
        return 0;
    }

    static int qinisekisa(int Ihele, int ubude_inani) {
        if (ubude_inani < 52 || 수(Ihele) != 0x464c457f || idivayisi_inani.기억읽기(Ihele + 4) != 1
            || idivayisi_inani.기억읽기(Ihele + 5) != 1 || idivayisi_inani.기억읽기(Ihele + 6) != 1
            || 짧은수(Ihele + 16) != 2 || 짧은수(Ihele + 18) != 3 || 수(Ihele + 20) != 1
            || 짧은수(Ihele + 40) != 52 || 짧은수(Ihele + 42) != 32) return -8;
        int okufakwayo_iphoyinti_inani = 수(Ihele + 24);
        int 표위치 = 수(Ihele + 28);
        int 개수 = 짧은수(Ihele + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > ubude_inani - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int thola_inkomba = 0; thola_inkomba < 개수; thola_inkomba++) {
            int 표 = Ihele + 표위치 + thola_inkomba * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Xhumanisa/해석기 미지원
            if (종류 != 1) continue;
            int 위치 = 수(표 + 4), ikheli = 수(표 + 8), ifayela_linganisa = 수(표 + 16), inkumbulo_linganisa = 수(표 + 20);
            int qondisa_inani = 수(표 + 28);
            if (ikheli < qala_umsebenzisi_i_app || ikheli >= isithombe_yekisa_ikheli || inkumbulo_linganisa < 0 || inkumbulo_linganisa > isithombe_yekisa_ikheli - ikheli
                || ifayela_linganisa < 0 || ifayela_linganisa > inkumbulo_linganisa || 위치 < 0 || (ifayela_linganisa > 0 && 위치 > ubude_inani - ifayela_linganisa)
                || (qondisa_inani != 0 && (qondisa_inani < 0 || (qondisa_inani & (qondisa_inani - 1)) != 0
                    || ((ikheli - 위치) & (qondisa_inani - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < thola_inkomba; 앞++) {
                int 이전 = Ihele + 표위치 + 앞 * 32;
                if (수(이전) == 1 && inkumbulo_linganisa > 0 && 수(이전 + 20) > 0
                    && ikheli < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < ikheli + inkumbulo_linganisa) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && okufakwayo_iphoyinti_inani >= ikheli && okufakwayo_iphoyinti_inani - ikheli < ifayela_linganisa) 실행가능 = true;
        }
        return 실행가능 ? okufakwayo_iphoyinti_inani : -8;
    }

    static int yenza_umyalo(int[] 입력, int Sebenzisa, int ubude_inani) {
        while (Sebenzisa < ubude_inani && 입력[Sebenzisa] == ' ') Sebenzisa++;
        int 끝 = Sebenzisa;
        while (끝 < ubude_inani && 입력[끝] != ' ') 끝++;
        int okufakwayo_inani = thola_okufakwayo(입력, Sebenzisa, 끝 - Sebenzisa);
        if (okufakwayo_inani == 0) return -2;
        int 위치 = 수(okufakwayo_inani + 16), Ubungako = 수(okufakwayo_inani + 20);
        if (위치 < 8 + 묶음개수() * 24 || Ubungako < 52 || 위치 > idivayisi_inani.실행묶음크기() - Ubungako) return -8;
        int Ihele = idivayisi_inani.실행묶음() + 위치;
        int okufakwayo_iphoyinti_inani = qinisekisa(Ihele, Ubungako);
        if (okufakwayo_iphoyinti_inani < 0) return okufakwayo_iphoyinti_inani;
        idivayisi_inani.umsebenzisi_sula_i_TOC();
        int 표위치 = 수(Ihele + 28), 개수 = 짧은수(Ihele + 44);
        for (int thola_inkomba = 0; thola_inkomba < 개수; thola_inkomba++) {
            int 표 = Ihele + 표위치 + thola_inkomba * 32;
            if (수(표) != 1) continue;
            int 원본 = Ihele + 수(표 + 4), isikhumulo_inani = 수(표 + 8), ifayela_linganisa = 수(표 + 16);
            for (int ibhayithi_inani = 0; ibhayithi_inani < ifayela_linganisa; ibhayithi_inani++) idivayisi_inani.bhala_inkumbulo(isikhumulo_inani + ibhayithi_inani, idivayisi_inani.기억읽기(원본 + ibhayithi_inani));
        }
        인수수 = 0;
        int Store_inani = i_agumenti_qala;
        while (끝 < ubude_inani) {
            while (끝 < ubude_inani && 입력[끝] == ' ') 끝++;
            if (끝 == ubude_inani) break;
            if (인수수 == i_agumenti_ikheli.length) return -22;
            Sebenzisa = 끝;
            while (끝 < ubude_inani && 입력[끝] != ' ') 끝++;
            i_agumenti_ikheli[인수수++] = Store_inani;
            수쓰기(Store_inani, 끝 - Sebenzisa);
            for (int uhlamvusimo_inani = Sebenzisa; uhlamvusimo_inani < 끝; uhlamvusimo_inani++) 수쓰기(Store_inani + 4 + (uhlamvusimo_inani - Sebenzisa) * 4, 입력[uhlamvusimo_inani]);
            Store_inani += 4 + (끝 - Sebenzisa) * 4;
        }
        iNethiwekhi_Isitaki.과정정리();
        파일서술자관리.qala_Inqubo();
        int 결과 = idivayisi_inani.sebenzisa_umsebenzisi_i_app(okufakwayo_iphoyinti_inani, umsebenzisi_yekisa - 16);
        파일서술자관리.과정정리();
        iNethiwekhi_Isitaki.과정정리();
        return 결과;
    }
}
