// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Yi_Karatu 전용 gudanar_Umarni 묶음의 ELF32 inganta, 인수 Ingiza_Daraja, 한 번에 한 Mai_anfani_da_kwamfuta haryar_aikin_na_ura_Daraja gudanar_Umarni. */
public final class 실행관리 {
    static final int Fara_Mai_anfani_da_kwamfuta_Shiri = 0x04000000;
    static final int Mai_anfani_da_kwamfuta_Ƙarshe = 0x04400000;
    static final int Hoto_Ƙarshe_imel = 0x04200000;
    static final int Tubalin_aiki_Fara = 0x04300000;
    static int 인수수 = 0;
    static int[] Tubalin_aiki_imel = new int[16];

    static boolean darfi(int imel, int Tsawo_Daraja) {
        return imel >= Fara_Mai_anfani_da_kwamfuta_Shiri && imel < Mai_anfani_da_kwamfuta_Ƙarshe && Tsawo_Daraja >= 0 && Tsawo_Daraja <= Mai_anfani_da_kwamfuta_Ƙarshe - imel;
    }

    static int 수(int imel) { return 기억공간.Daddatse_Lamba_mara(imel); }
    static int 짧은수(int imel) { return na_ura_Daraja.기억읽기(imel) | na_ura_Daraja.기억읽기(imel + 1) << 8; }
    static void 수쓰기(int imel, int Daraja) {
        for (int Indes = 0; Indes < 4; Indes++) na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(imel + Indes, Daraja >>> (Indes * 8));
    }

    static int 묶음개수() {
        int imel = na_ura_Daraja.실행묶음();
        int Girma = na_ura_Daraja.실행묶음크기();
        if (Girma < 8 || 수(imel) != 0x50414b4a) return 0;
        int 개수 = 수(imel + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (Girma - 8) / 24 ? 개수 : 0;
    }

    static void Mashigar_bayanai_Jeri() {
        for (int Indes = 0; Indes < 묶음개수(); Indes++) {
            int Mashigar_bayanai_Daraja = na_ura_Daraja.실행묶음() + 8 + Indes * 24;
            for (int Harafi_Daraja = 0; Harafi_Daraja < 16 && na_ura_Daraja.기억읽기(Mashigar_bayanai_Daraja + Harafi_Daraja) != 0; Harafi_Daraja++)
                문자단말.문자(na_ura_Daraja.기억읽기(Mashigar_bayanai_Daraja + Harafi_Daraja));
            문자단말.Yi_Rubutu("\n");
        }
    }

    static int nema_Mashigar_bayanai(int[] 입력, int Tafiyar_da, int Tsawo_Daraja) {
        if (Tsawo_Daraja <= 0 || Tsawo_Daraja >= 16) return 0;
        for (int Indes = 0; Indes < 묶음개수(); Indes++) {
            int Mashigar_bayanai_Daraja = na_ura_Daraja.실행묶음() + 8 + Indes * 24;
            boolean 같음 = na_ura_Daraja.기억읽기(Mashigar_bayanai_Daraja + Tsawo_Daraja) == 0;
            for (int Harafi_Daraja = 0; Harafi_Daraja < Tsawo_Daraja; Harafi_Daraja++)
                if (입력[Tafiyar_da + Harafi_Daraja] != na_ura_Daraja.기억읽기(Mashigar_bayanai_Daraja + Harafi_Daraja)) 같음 = false;
            if (같음) return Mashigar_bayanai_Daraja;
        }
        return 0;
    }

    static int inganta(int Fayil, int Tsawo_Daraja) {
        if (Tsawo_Daraja < 52 || 수(Fayil) != 0x464c457f || na_ura_Daraja.기억읽기(Fayil + 4) != 1
            || na_ura_Daraja.기억읽기(Fayil + 5) != 1 || na_ura_Daraja.기억읽기(Fayil + 6) != 1
            || 짧은수(Fayil + 16) != 2 || 짧은수(Fayil + 18) != 3 || 수(Fayil + 20) != 1
            || 짧은수(Fayil + 40) != 52 || 짧은수(Fayil + 42) != 32) return -8;
        int Mashigar_bayanai_maki_Daraja = 수(Fayil + 24);
        int 표위치 = 수(Fayil + 28);
        int 개수 = 짧은수(Fayil + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > Tsawo_Daraja - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int Indes = 0; Indes < 개수; Indes++) {
            int 표 = Fayil + 표위치 + Indes * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Haɗi/tatsar_manhaja_48ee4b1b 미지원
            if (종류 != 1) continue;
            int 위치 = 수(표 + 4), imel = 수(표 + 8), Fayil_girma = 수(표 + 16), Mahardatar_kwamfuta_girma = 수(표 + 20);
            int Daidaita_Daraja = 수(표 + 28);
            if (imel < Fara_Mai_anfani_da_kwamfuta_Shiri || imel >= Hoto_Ƙarshe_imel || Mahardatar_kwamfuta_girma < 0 || Mahardatar_kwamfuta_girma > Hoto_Ƙarshe_imel - imel
                || Fayil_girma < 0 || Fayil_girma > Mahardatar_kwamfuta_girma || 위치 < 0 || (Fayil_girma > 0 && 위치 > Tsawo_Daraja - Fayil_girma)
                || (Daidaita_Daraja != 0 && (Daidaita_Daraja < 0 || (Daidaita_Daraja & (Daidaita_Daraja - 1)) != 0
                    || ((imel - 위치) & (Daidaita_Daraja - 1)) != 0))) return -8;
            for (int kyamarar_gaba_Daraja = 0; kyamarar_gaba_Daraja < Indes; kyamarar_gaba_Daraja++) {
                int 이전 = Fayil + 표위치 + kyamarar_gaba_Daraja * 32;
                if (수(이전) == 1 && Mahardatar_kwamfuta_girma > 0 && 수(이전 + 20) > 0
                    && imel < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < imel + Mahardatar_kwamfuta_girma) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && Mashigar_bayanai_maki_Daraja >= imel && Mashigar_bayanai_maki_Daraja - imel < Fayil_girma) 실행가능 = true;
        }
        return 실행가능 ? Mashigar_bayanai_maki_Daraja : -8;
    }

    static int gudanar_Umarni(int[] 입력, int Tafiyar_da, int Tsawo_Daraja) {
        while (Tafiyar_da < Tsawo_Daraja && 입력[Tafiyar_da] == ' ') Tafiyar_da++;
        int 끝 = Tafiyar_da;
        while (끝 < Tsawo_Daraja && 입력[끝] != ' ') 끝++;
        int Mashigar_bayanai_Daraja = nema_Mashigar_bayanai(입력, Tafiyar_da, 끝 - Tafiyar_da);
        if (Mashigar_bayanai_Daraja == 0) return -2;
        int 위치 = 수(Mashigar_bayanai_Daraja + 16), Girma = 수(Mashigar_bayanai_Daraja + 20);
        if (위치 < 8 + 묶음개수() * 24 || Girma < 52 || 위치 > na_ura_Daraja.실행묶음크기() - Girma) return -8;
        int Fayil = na_ura_Daraja.실행묶음() + 위치;
        int Mashigar_bayanai_maki_Daraja = inganta(Fayil, Girma);
        if (Mashigar_bayanai_maki_Daraja < 0) return Mashigar_bayanai_maki_Daraja;
        na_ura_Daraja.Mai_anfani_da_kwamfuta_Share_TOC();
        int 표위치 = 수(Fayil + 28), 개수 = 짧은수(Fayil + 44);
        for (int Indes = 0; Indes < 개수; Indes++) {
            int 표 = Fayil + 표위치 + Indes * 32;
            if (수(표) != 1) continue;
            int 원본 = Fayil + 수(표 + 4), Zangon_ƙarshe_Daraja = 수(표 + 8), Fayil_girma = 수(표 + 16);
            for (int bayit_Daraja = 0; bayit_Daraja < Fayil_girma; bayit_Daraja++) na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(Zangon_ƙarshe_Daraja + bayit_Daraja, na_ura_Daraja.기억읽기(원본 + bayit_Daraja));
        }
        인수수 = 0;
        int Ajiye_Daraja = Tubalin_aiki_Fara;
        while (끝 < Tsawo_Daraja) {
            while (끝 < Tsawo_Daraja && 입력[끝] == ' ') 끝++;
            if (끝 == Tsawo_Daraja) break;
            if (인수수 == Tubalin_aiki_imel.length) return -22;
            Tafiyar_da = 끝;
            while (끝 < Tsawo_Daraja && 입력[끝] != ' ') 끝++;
            Tubalin_aiki_imel[인수수++] = Ajiye_Daraja;
            수쓰기(Ajiye_Daraja, 끝 - Tafiyar_da);
            for (int Harafi_Daraja = Tafiyar_da; Harafi_Daraja < 끝; Harafi_Daraja++) 수쓰기(Ajiye_Daraja + 4 + (Harafi_Daraja - Tafiyar_da) * 4, 입력[Harafi_Daraja]);
            Ajiye_Daraja += 4 + (끝 - Tafiyar_da) * 4;
        }
        Hanyar_sadarwa_tara.과정정리();
        파일서술자관리.Fara_haryar_aikin_na_ura();
        int 결과 = na_ura_Daraja.Gudanar_da_Mai_anfani_da_kwamfuta_Shiri(Mashigar_bayanai_maki_Daraja, Mai_anfani_da_kwamfuta_Ƙarshe - 16);
        파일서술자관리.과정정리();
        Hanyar_sadarwa_tara.과정정리();
        return 결과;
    }
}
