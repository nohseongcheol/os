// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Bala 전용 phethagatša_taelo 묶음의 ELF32 kgonthiša_5fb2b747, 인수 romela_pele_boleng, 한 번에 한 mošomiši tiragalo_boleng phethagatša_taelo. */
public final class 실행관리 {
    static final int Thomišo_mošomiši_tirišo = 0x04000000;
    static final int mošomiši_fetša = 0x04400000;
    static final int seswantšho_fetša_atrese = 0x04200000;
    static final int akumente_Thomišo = 0x04300000;
    static int 인수수 = 0;
    static int[] akumente_atrese = new int[16];

    static boolean setsopolwa(int atrese, int botelele_boleng) {
        return atrese >= Thomišo_mošomiši_tirišo && atrese < mošomiši_fetša && botelele_boleng >= 0 && botelele_boleng <= mošomiši_fetša - atrese;
    }

    static int 수(int atrese) { return 기억공간.ripaganya_palotlalo(atrese); }
    static int 짧은수(int atrese) { return sedirišwa_boleng.기억읽기(atrese) | sedirišwa_boleng.기억읽기(atrese + 1) << 8; }
    static void 수쓰기(int atrese, int boleng) {
        for (int lokela = 0; lokela < 4; lokela++) sedirišwa_boleng.ngwala_memori(atrese + lokela, boleng >>> (lokela * 8));
    }

    static int 묶음개수() {
        int atrese = sedirišwa_boleng.실행묶음();
        int Bogolo = sedirišwa_boleng.실행묶음크기();
        if (Bogolo < 8 || 수(atrese) != 0x50414b4a) return 0;
        int 개수 = 수(atrese + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (Bogolo - 8) / 24 ? 개수 : 0;
    }

    static void go_tsenya_tshedimošo_Lenaneo() {
        for (int lokela = 0; lokela < 묶음개수(); lokela++) {
            int go_tsenya_tshedimošo_boleng = sedirišwa_boleng.실행묶음() + 8 + lokela * 24;
            for (int tlhaka_boleng = 0; tlhaka_boleng < 16 && sedirišwa_boleng.기억읽기(go_tsenya_tshedimošo_boleng + tlhaka_boleng) != 0; tlhaka_boleng++)
                문자단말.문자(sedirišwa_boleng.기억읽기(go_tsenya_tshedimošo_boleng + tlhaka_boleng));
            문자단말.Ngwala("\n");
        }
    }

    static int hwetša_go_tsenya_tshedimošo(int[] 입력, int Diriša, int botelele_boleng) {
        if (botelele_boleng <= 0 || botelele_boleng >= 16) return 0;
        for (int lokela = 0; lokela < 묶음개수(); lokela++) {
            int go_tsenya_tshedimošo_boleng = sedirišwa_boleng.실행묶음() + 8 + lokela * 24;
            boolean 같음 = sedirišwa_boleng.기억읽기(go_tsenya_tshedimošo_boleng + botelele_boleng) == 0;
            for (int tlhaka_boleng = 0; tlhaka_boleng < botelele_boleng; tlhaka_boleng++)
                if (입력[Diriša + tlhaka_boleng] != sedirišwa_boleng.기억읽기(go_tsenya_tshedimošo_boleng + tlhaka_boleng)) 같음 = false;
            if (같음) return go_tsenya_tshedimošo_boleng;
        }
        return 0;
    }

    static int kgonthiša_5fb2b747(int Faele, int botelele_boleng) {
        if (botelele_boleng < 52 || 수(Faele) != 0x464c457f || sedirišwa_boleng.기억읽기(Faele + 4) != 1
            || sedirišwa_boleng.기억읽기(Faele + 5) != 1 || sedirišwa_boleng.기억읽기(Faele + 6) != 1
            || 짧은수(Faele + 16) != 2 || 짧은수(Faele + 18) != 3 || 수(Faele + 20) != 1
            || 짧은수(Faele + 40) != 52 || 짧은수(Faele + 42) != 32) return -8;
        int go_tsenya_tshedimošo_ntlha_boleng = 수(Faele + 24);
        int 표위치 = 수(Faele + 28);
        int 개수 = 짧은수(Faele + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > botelele_boleng - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int lokela = 0; lokela < 개수; lokela++) {
            int 표 = Faele + 표위치 + lokela * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Ikgokaganye/해석기 미지원
            if (종류 != 1) continue;
            int 위치 = 수(표 + 4), atrese = 수(표 + 8), faele_bogolo = 수(표 + 16), memori_bogolo = 수(표 + 20);
            int tsepanya_boleng = 수(표 + 28);
            if (atrese < Thomišo_mošomiši_tirišo || atrese >= seswantšho_fetša_atrese || memori_bogolo < 0 || memori_bogolo > seswantšho_fetša_atrese - atrese
                || faele_bogolo < 0 || faele_bogolo > memori_bogolo || 위치 < 0 || (faele_bogolo > 0 && 위치 > botelele_boleng - faele_bogolo)
                || (tsepanya_boleng != 0 && (tsepanya_boleng < 0 || (tsepanya_boleng & (tsepanya_boleng - 1)) != 0
                    || ((atrese - 위치) & (tsepanya_boleng - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < lokela; 앞++) {
                int 이전 = Faele + 표위치 + 앞 * 32;
                if (수(이전) == 1 && memori_bogolo > 0 && 수(이전 + 20) > 0
                    && atrese < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < atrese + memori_bogolo) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && go_tsenya_tshedimošo_ntlha_boleng >= atrese && go_tsenya_tshedimošo_ntlha_boleng - atrese < faele_bogolo) 실행가능 = true;
        }
        return 실행가능 ? go_tsenya_tshedimošo_ntlha_boleng : -8;
    }

    static int phethagatša_taelo(int[] 입력, int Diriša, int botelele_boleng) {
        while (Diriša < botelele_boleng && 입력[Diriša] == ' ') Diriša++;
        int 끝 = Diriša;
        while (끝 < botelele_boleng && 입력[끝] != ' ') 끝++;
        int go_tsenya_tshedimošo_boleng = hwetša_go_tsenya_tshedimošo(입력, Diriša, 끝 - Diriša);
        if (go_tsenya_tshedimošo_boleng == 0) return -2;
        int 위치 = 수(go_tsenya_tshedimošo_boleng + 16), Bogolo = 수(go_tsenya_tshedimošo_boleng + 20);
        if (위치 < 8 + 묶음개수() * 24 || Bogolo < 52 || 위치 > sedirišwa_boleng.실행묶음크기() - Bogolo) return -8;
        int Faele = sedirišwa_boleng.실행묶음() + 위치;
        int go_tsenya_tshedimošo_ntlha_boleng = kgonthiša_5fb2b747(Faele, Bogolo);
        if (go_tsenya_tshedimošo_ntlha_boleng < 0) return go_tsenya_tshedimošo_ntlha_boleng;
        sedirišwa_boleng.mošomiši_tloša_TOC();
        int 표위치 = 수(Faele + 28), 개수 = 짧은수(Faele + 44);
        for (int lokela = 0; lokela < 개수; lokela++) {
            int 표 = Faele + 표위치 + lokela * 32;
            if (수(표) != 1) continue;
            int 원본 = Faele + 수(표 + 4), boyo_boleng = 수(표 + 8), faele_bogolo = 수(표 + 16);
            for (int paete_boleng = 0; paete_boleng < faele_bogolo; paete_boleng++) sedirišwa_boleng.ngwala_memori(boyo_boleng + paete_boleng, sedirišwa_boleng.기억읽기(원본 + paete_boleng));
        }
        인수수 = 0;
        int lota_boleng = akumente_Thomišo;
        while (끝 < botelele_boleng) {
            while (끝 < botelele_boleng && 입력[끝] == ' ') 끝++;
            if (끝 == botelele_boleng) break;
            if (인수수 == akumente_atrese.length) return -22;
            Diriša = 끝;
            while (끝 < botelele_boleng && 입력[끝] != ' ') 끝++;
            akumente_atrese[인수수++] = lota_boleng;
            수쓰기(lota_boleng, 끝 - Diriša);
            for (int tlhaka_boleng = Diriša; tlhaka_boleng < 끝; tlhaka_boleng++) 수쓰기(lota_boleng + 4 + (tlhaka_boleng - Diriša) * 4, 입력[tlhaka_boleng]);
            lota_boleng += 4 + (끝 - Diriša) * 4;
        }
        Netweke_kgoboko.과정정리();
        파일서술자관리.Thomišo_tiragalo();
        int 결과 = sedirišwa_boleng.sepetša_mošomiši_tirišo(go_tsenya_tshedimošo_ntlha_boleng, mošomiši_fetša - 16);
        파일서술자관리.과정정리();
        Netweke_kgoboko.과정정리();
        return 결과;
    }
}
