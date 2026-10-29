// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 읽기 전용 ausféieren_Befeel 묶음의 ELF32 validéieren, 인수 Virun_VALUE, 한 번에 한 Benotzer Prozess_VALUE ausféieren_Befeel. */
public final class 실행관리 {
    static final int Start_Benotzer_App = 0x04000000;
    static final int Benotzer_bëennegen = 0x04400000;
    static final int Bild_bëennegen_Adress = 0x04200000;
    static final int Argument_Start = 0x04300000;
    static int Argument_COUNT = 0;
    static int[] Argument_Adress = new int[16];

    static boolean Clip(int Adress, int Längt_VALUE) {
        return Adress >= Start_Benotzer_App && Adress < Benotzer_bëennegen && Längt_VALUE >= 0 && Längt_VALUE <= Benotzer_bëennegen - Adress;
    }

    static int 수(int Adress) { return 기억공간.analyséieren_Ganzzuel(Adress); }
    static int 짧은수(int Adress) { return Mobil_VALUE.기억읽기(Adress) | Mobil_VALUE.기억읽기(Adress + 1) << 8; }
    static void 수쓰기(int Adress, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) Mobil_VALUE.schreiwen_Späicher(Adress + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Grupp_COUNT() {
        int Adress = Mobil_VALUE.실행묶음();
        int d_Gréisst_veränneren = Mobil_VALUE.실행묶음크기();
        if (d_Gréisst_veränneren < 8 || 수(Adress) != 0x50414b4a) return 0;
        int Element_COUNT = 수(Adress + 4);
        return Element_COUNT >= 0 && Element_COUNT <= 32 && Element_COUNT <= (d_Gréisst_veränneren - 8) / 24 ? Element_COUNT : 0;
    }

    static void Agab_Lëscht() {
        for (int INDEX = 0; INDEX < Grupp_COUNT(); INDEX++) {
            int Agab_VALUE = Mobil_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int Zeechen_VALUE = 0; Zeechen_VALUE < 16 && Mobil_VALUE.기억읽기(Agab_VALUE + Zeechen_VALUE) != 0; Zeechen_VALUE++)
                SMS_Terminal.문자(Mobil_VALUE.기억읽기(Agab_VALUE + Zeechen_VALUE));
            SMS_Terminal.schreiwen("\n");
        }
    }

    static int FIND_Agab(int[] 입력, int Laf, int Längt_VALUE) {
        if (Längt_VALUE <= 0 || Längt_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < Grupp_COUNT(); INDEX++) {
            int Agab_VALUE = Mobil_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = Mobil_VALUE.기억읽기(Agab_VALUE + Längt_VALUE) == 0;
            for (int Zeechen_VALUE = 0; Zeechen_VALUE < Längt_VALUE; Zeechen_VALUE++)
                if (입력[Laf + Zeechen_VALUE] != Mobil_VALUE.기억읽기(Agab_VALUE + Zeechen_VALUE)) 같음 = false;
            if (같음) return Agab_VALUE;
        }
        return 0;
    }

    static int validéieren(int Fichier, int Längt_VALUE) {
        if (Längt_VALUE < 52 || 수(Fichier) != 0x464c457f || Mobil_VALUE.기억읽기(Fichier + 4) != 1
            || Mobil_VALUE.기억읽기(Fichier + 5) != 1 || Mobil_VALUE.기억읽기(Fichier + 6) != 1
            || 짧은수(Fichier + 16) != 2 || 짧은수(Fichier + 18) != 3 || 수(Fichier + 20) != 1
            || 짧은수(Fichier + 40) != 52 || 짧은수(Fichier + 42) != 32) return -8;
        int Agab_Punkt_VALUE = 수(Fichier + 24);
        int Tabell_positionéieren = 수(Fichier + 28);
        int Element_COUNT = 짧은수(Fichier + 44);
        if (Element_COUNT == 0 || Element_COUNT > 16 || Tabell_positionéieren < 52 || Tabell_positionéieren > Längt_VALUE - Element_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < Element_COUNT; INDEX++) {
            int LOOKUP_Tabell = Fichier + Tabell_positionéieren + INDEX * 32;
            int 종류 = 수(LOOKUP_Tabell);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Verbannen/해석기 미지원
            if (종류 != 1) continue;
            int positionéieren = 수(LOOKUP_Tabell + 4), Adress = 수(LOOKUP_Tabell + 8), Fichier_d_Gréisst_veränneren = 수(LOOKUP_Tabell + 16), Späicher_d_Gréisst_veränneren = 수(LOOKUP_Tabell + 20);
            int alignéieren_VALUE = 수(LOOKUP_Tabell + 28);
            if (Adress < Start_Benotzer_App || Adress >= Bild_bëennegen_Adress || Späicher_d_Gréisst_veränneren < 0 || Späicher_d_Gréisst_veränneren > Bild_bëennegen_Adress - Adress
                || Fichier_d_Gréisst_veränneren < 0 || Fichier_d_Gréisst_veränneren > Späicher_d_Gréisst_veränneren || positionéieren < 0 || (Fichier_d_Gréisst_veränneren > 0 && positionéieren > Längt_VALUE - Fichier_d_Gréisst_veränneren)
                || (alignéieren_VALUE != 0 && (alignéieren_VALUE < 0 || (alignéieren_VALUE & (alignéieren_VALUE - 1)) != 0
                    || ((Adress - positionéieren) & (alignéieren_VALUE - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < INDEX; 앞++) {
                int 이전 = Fichier + Tabell_positionéieren + 앞 * 32;
                if (수(이전) == 1 && Späicher_d_Gréisst_veränneren > 0 && 수(이전 + 20) > 0
                    && Adress < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < Adress + Späicher_d_Gréisst_veränneren) return -8;
            }
            if ((수(LOOKUP_Tabell + 24) & 1) != 0 && Agab_Punkt_VALUE >= Adress && Agab_Punkt_VALUE - Adress < Fichier_d_Gréisst_veränneren) 실행가능 = true;
        }
        return 실행가능 ? Agab_Punkt_VALUE : -8;
    }

    static int ausféieren_Befeel(int[] 입력, int Laf, int Längt_VALUE) {
        while (Laf < Längt_VALUE && 입력[Laf] == ' ') Laf++;
        int 끝 = Laf;
        while (끝 < Längt_VALUE && 입력[끝] != ' ') 끝++;
        int Agab_VALUE = FIND_Agab(입력, Laf, 끝 - Laf);
        if (Agab_VALUE == 0) return -2;
        int positionéieren = 수(Agab_VALUE + 16), d_Gréisst_veränneren = 수(Agab_VALUE + 20);
        if (positionéieren < 8 + Grupp_COUNT() * 24 || d_Gréisst_veränneren < 52 || positionéieren > Mobil_VALUE.실행묶음크기() - d_Gréisst_veränneren) return -8;
        int Fichier = Mobil_VALUE.실행묶음() + positionéieren;
        int Agab_Punkt_VALUE = validéieren(Fichier, d_Gréisst_veränneren);
        if (Agab_Punkt_VALUE < 0) return Agab_Punkt_VALUE;
        Mobil_VALUE.Benotzer_läschen_Inhalt();
        int Tabell_positionéieren = 수(Fichier + 28), Element_COUNT = 짧은수(Fichier + 44);
        for (int INDEX = 0; INDEX < Element_COUNT; INDEX++) {
            int LOOKUP_Tabell = Fichier + Tabell_positionéieren + INDEX * 32;
            if (수(LOOKUP_Tabell) != 1) continue;
            int 원본 = Fichier + 수(LOOKUP_Tabell + 4), Zil_VALUE = 수(LOOKUP_Tabell + 8), Fichier_d_Gréisst_veränneren = 수(LOOKUP_Tabell + 16);
            for (int Byte_VALUE = 0; Byte_VALUE < Fichier_d_Gréisst_veränneren; Byte_VALUE++) Mobil_VALUE.schreiwen_Späicher(Zil_VALUE + Byte_VALUE, Mobil_VALUE.기억읽기(원본 + Byte_VALUE));
        }
        Argument_COUNT = 0;
        int Store_VALUE = Argument_Start;
        while (끝 < Längt_VALUE) {
            while (끝 < Längt_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == Längt_VALUE) break;
            if (Argument_COUNT == Argument_Adress.length) return -22;
            Laf = 끝;
            while (끝 < Längt_VALUE && 입력[끝] != ' ') 끝++;
            Argument_Adress[Argument_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - Laf);
            for (int Zeechen_VALUE = Laf; Zeechen_VALUE < 끝; Zeechen_VALUE++) 수쓰기(Store_VALUE + 4 + (Zeechen_VALUE - Laf) * 4, 입력[Zeechen_VALUE]);
            Store_VALUE += 4 + (끝 - Laf) * 4;
        }
        Reseau_Stapel.CLEAN_Prozess();
        파일서술자관리.Start_Prozess();
        int Mooss = Mobil_VALUE.Laf_Benotzer_App(Agab_Punkt_VALUE, Benotzer_bëennegen - 16);
        파일서술자관리.CLEAN_Prozess();
        Reseau_Stapel.CLEAN_Prozess();
        return Mooss;
    }
}
