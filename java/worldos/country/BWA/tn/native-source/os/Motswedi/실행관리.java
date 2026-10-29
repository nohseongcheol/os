// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 읽기 전용 diragatsa_Taelo 묶음의 ELF32 netefatsa_5fb2b747, 인수 fetisa_Boleng_24592b8a, 한 번에 한 modirisi Thulaganyo_Boleng diragatsa_Taelo. */
public final class 실행관리 {
    static final int simolola_modirisi_Tiriso = 0x04000000;
    static final int modirisi_kgaola = 0x04400000;
    static final int Setshwantsho_kgaola_aterese = 0x04200000;
    static final int Thulaganyo_simolola = 0x04300000;
    static int 인수수 = 0;
    static int[] Thulaganyo_aterese_841f6346 = new int[16];

    static boolean faelekhutshwe_ya_media(int aterese, int boleele_Boleng) {
        return aterese >= simolola_modirisi_Tiriso && aterese < modirisi_kgaola && boleele_Boleng >= 0 && boleele_Boleng <= modirisi_kgaola - aterese;
    }

    static int 수(int aterese) { return 기억공간.go_lokolola_Palotlalo(aterese); }
    static int 짧은수(int aterese) { return mobaele_Boleng.기억읽기(aterese) | mobaele_Boleng.기억읽기(aterese + 1) << 8; }
    static void 수쓰기(int aterese, int Boleng) {
        for (int tshupane = 0; tshupane < 4; tshupane++) mobaele_Boleng.kwala_memori(aterese + tshupane, Boleng >>> (tshupane * 8));
    }

    static int 묶음개수() {
        int aterese = mobaele_Boleng.실행묶음();
        int lekanya = mobaele_Boleng.실행묶음크기();
        if (lekanya < 8 || 수(aterese) != 0x50414b4a) return 0;
        int 개수 = 수(aterese + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (lekanya - 8) / 24 ? 개수 : 0;
    }

    static void tsenyo_lenaane() {
        for (int tshupane = 0; tshupane < 묶음개수(); tshupane++) {
            int tsenyo_Boleng = mobaele_Boleng.실행묶음() + 8 + tshupane * 24;
            for (int Letshwao_Boleng = 0; Letshwao_Boleng < 16 && mobaele_Boleng.기억읽기(tsenyo_Boleng + Letshwao_Boleng) != 0; Letshwao_Boleng++)
                문자단말.문자(mobaele_Boleng.기억읽기(tsenyo_Boleng + Letshwao_Boleng));
            문자단말.kwala("\n");
        }
    }

    static int batla_tsenyo(int[] 입력, int dirisa, int boleele_Boleng) {
        if (boleele_Boleng <= 0 || boleele_Boleng >= 16) return 0;
        for (int tshupane = 0; tshupane < 묶음개수(); tshupane++) {
            int tsenyo_Boleng = mobaele_Boleng.실행묶음() + 8 + tshupane * 24;
            boolean 같음 = mobaele_Boleng.기억읽기(tsenyo_Boleng + boleele_Boleng) == 0;
            for (int Letshwao_Boleng = 0; Letshwao_Boleng < boleele_Boleng; Letshwao_Boleng++)
                if (입력[dirisa + Letshwao_Boleng] != mobaele_Boleng.기억읽기(tsenyo_Boleng + Letshwao_Boleng)) 같음 = false;
            if (같음) return tsenyo_Boleng;
        }
        return 0;
    }

    static int netefatsa_5fb2b747(int faele, int boleele_Boleng) {
        if (boleele_Boleng < 52 || 수(faele) != 0x464c457f || mobaele_Boleng.기억읽기(faele + 4) != 1
            || mobaele_Boleng.기억읽기(faele + 5) != 1 || mobaele_Boleng.기억읽기(faele + 6) != 1
            || 짧은수(faele + 16) != 2 || 짧은수(faele + 18) != 3 || 수(faele + 20) != 1
            || 짧은수(faele + 40) != 52 || 짧은수(faele + 42) != 32) return -8;
        int tsenyo_ntlha_Boleng = 수(faele + 24);
        int 표위치 = 수(faele + 28);
        int 개수 = 짧은수(faele + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > boleele_Boleng - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int tshupane = 0; tshupane < 개수; tshupane++) {
            int 표 = faele + 표위치 + tshupane * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Golaganya/해석기 미지원
            if (종류 != 1) continue;
            int 위치 = 수(표 + 4), aterese = 수(표 + 8), faele_lekanya = 수(표 + 16), memori_lekanya = 수(표 + 20);
            int tlhamalatsa_Boleng = 수(표 + 28);
            if (aterese < simolola_modirisi_Tiriso || aterese >= Setshwantsho_kgaola_aterese || memori_lekanya < 0 || memori_lekanya > Setshwantsho_kgaola_aterese - aterese
                || faele_lekanya < 0 || faele_lekanya > memori_lekanya || 위치 < 0 || (faele_lekanya > 0 && 위치 > boleele_Boleng - faele_lekanya)
                || (tlhamalatsa_Boleng != 0 && (tlhamalatsa_Boleng < 0 || (tlhamalatsa_Boleng & (tlhamalatsa_Boleng - 1)) != 0
                    || ((aterese - 위치) & (tlhamalatsa_Boleng - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < tshupane; 앞++) {
                int 이전 = faele + 표위치 + 앞 * 32;
                if (수(이전) == 1 && memori_lekanya > 0 && 수(이전 + 20) > 0
                    && aterese < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < aterese + memori_lekanya) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && tsenyo_ntlha_Boleng >= aterese && tsenyo_ntlha_Boleng - aterese < faele_lekanya) 실행가능 = true;
        }
        return 실행가능 ? tsenyo_ntlha_Boleng : -8;
    }

    static int diragatsa_Taelo(int[] 입력, int dirisa, int boleele_Boleng) {
        while (dirisa < boleele_Boleng && 입력[dirisa] == ' ') dirisa++;
        int 끝 = dirisa;
        while (끝 < boleele_Boleng && 입력[끝] != ' ') 끝++;
        int tsenyo_Boleng = batla_tsenyo(입력, dirisa, 끝 - dirisa);
        if (tsenyo_Boleng == 0) return -2;
        int 위치 = 수(tsenyo_Boleng + 16), lekanya = 수(tsenyo_Boleng + 20);
        if (위치 < 8 + 묶음개수() * 24 || lekanya < 52 || 위치 > mobaele_Boleng.실행묶음크기() - lekanya) return -8;
        int faele = mobaele_Boleng.실행묶음() + 위치;
        int tsenyo_ntlha_Boleng = netefatsa_5fb2b747(faele, lekanya);
        if (tsenyo_ntlha_Boleng < 0) return tsenyo_ntlha_Boleng;
        mobaele_Boleng.modirisi_phimola_TOC();
        int 표위치 = 수(faele + 28), 개수 = 짧은수(faele + 44);
        for (int tshupane = 0; tshupane < 개수; tshupane++) {
            int 표 = faele + 표위치 + tshupane * 32;
            if (수(표) != 1) continue;
            int 원본 = faele + 수(표 + 4), bogorogelo_Boleng = 수(표 + 8), faele_lekanya = 수(표 + 16);
            for (int baete_Boleng = 0; baete_Boleng < faele_lekanya; baete_Boleng++) mobaele_Boleng.kwala_memori(bogorogelo_Boleng + baete_Boleng, mobaele_Boleng.기억읽기(원본 + baete_Boleng));
        }
        인수수 = 0;
        int Store_Boleng = Thulaganyo_simolola;
        while (끝 < boleele_Boleng) {
            while (끝 < boleele_Boleng && 입력[끝] == ' ') 끝++;
            if (끝 == boleele_Boleng) break;
            if (인수수 == Thulaganyo_aterese_841f6346.length) return -22;
            dirisa = 끝;
            while (끝 < boleele_Boleng && 입력[끝] != ' ') 끝++;
            Thulaganyo_aterese_841f6346[인수수++] = Store_Boleng;
            수쓰기(Store_Boleng, 끝 - dirisa);
            for (int Letshwao_Boleng = dirisa; Letshwao_Boleng < 끝; Letshwao_Boleng++) 수쓰기(Store_Boleng + 4 + (Letshwao_Boleng - dirisa) * 4, 입력[Letshwao_Boleng]);
            Store_Boleng += 4 + (끝 - dirisa) * 4;
        }
        Neteweke_kokoanyodinepe.과정정리();
        파일서술자관리.simolola_Thulaganyo();
        int 결과 = mobaele_Boleng.dirisa_modirisi_Tiriso(tsenyo_ntlha_Boleng, modirisi_kgaola - 16);
        파일서술자관리.과정정리();
        Neteweke_kokoanyodinepe.과정정리();
        return 결과;
    }
}
