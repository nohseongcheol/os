// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 읽기 전용 실행 묶음의 ELF32 검증, 인수 전달, 한 번에 한 ka_yataayakalü 과정 실행. */
public final class 실행관리 {
    static final int achuwalaa_ka_yataayakalü_akumajiaa = 0x04000000;
    static final int ka_yataayakalü_ajattiraa = 0x04400000;
    static final int ayaakuaa_ajattiraa_ejepüsee = 0x04200000;
    static final int ajutuu_achuwalaa = 0x04300000;
    static int 인수수 = 0;
    static int[] ajutuu_ejepüsee = new int[16];

    static boolean külipü_ayaakuaapijana(int ejepüsee, int akaliaa_ajutuu) {
        return ejepüsee >= achuwalaa_ka_yataayakalü_akumajiaa && ejepüsee < ka_yataayakalü_ajattiraa && akaliaa_ajutuu >= 0 && akaliaa_ajutuu <= ka_yataayakalü_ajattiraa - ejepüsee;
    }

    static int 수(int ejepüsee) { return 기억공간.akatajaa_waneepiasü(ejepüsee); }
    static int 짧은수(int ejepüsee) { return serulaalü_ajutuu.기억읽기(ejepüsee) | serulaalü_ajutuu.기억읽기(ejepüsee + 1) << 8; }
    static void 수쓰기(int ejepüsee, int ajutuu) {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 4; ee_iyatialujuna++) serulaalü_ajutuu.기억쓰기(ejepüsee + ee_iyatialujuna, ajutuu >>> (ee_iyatialujuna * 8));
    }

    static int 묶음개수() {
        int ejepüsee = serulaalü_ajutuu.실행묶음();
        int 크기 = serulaalü_ajutuu.실행묶음크기();
        if (크기 < 8 || 수(ejepüsee) != 0x50414b4a) return 0;
        int 개수 = 수(ejepüsee + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (크기 - 8) / 24 ? 개수 : 0;
    }

    static void 목록() {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 묶음개수(); ee_iyatialujuna++) {
            int ekeroliaa_ajutuu = serulaalü_ajutuu.실행묶음() + 8 + ee_iyatialujuna * 24;
            for (int jeerü_ajutuu = 0; jeerü_ajutuu < 16 && serulaalü_ajutuu.기억읽기(ekeroliaa_ajutuu + jeerü_ajutuu) != 0; jeerü_ajutuu++)
                문자단말.문자(serulaalü_ajutuu.기억읽기(ekeroliaa_ajutuu + jeerü_ajutuu));
            문자단말.ashajaa("\n");
        }
    }

    static int 찾기(int[] 입력, int 시작, int akaliaa_ajutuu) {
        if (akaliaa_ajutuu <= 0 || akaliaa_ajutuu >= 16) return 0;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 묶음개수(); ee_iyatialujuna++) {
            int ekeroliaa_ajutuu = serulaalü_ajutuu.실행묶음() + 8 + ee_iyatialujuna * 24;
            boolean 같음 = serulaalü_ajutuu.기억읽기(ekeroliaa_ajutuu + akaliaa_ajutuu) == 0;
            for (int jeerü_ajutuu = 0; jeerü_ajutuu < akaliaa_ajutuu; jeerü_ajutuu++)
                if (입력[시작 + jeerü_ajutuu] != serulaalü_ajutuu.기억읽기(ekeroliaa_ajutuu + jeerü_ajutuu)) 같음 = false;
            if (같음) return ekeroliaa_ajutuu;
        }
        return 0;
    }

    static int 검증(int anaajaalaa, int akaliaa_ajutuu) {
        if (akaliaa_ajutuu < 52 || 수(anaajaalaa) != 0x464c457f || serulaalü_ajutuu.기억읽기(anaajaalaa + 4) != 1
            || serulaalü_ajutuu.기억읽기(anaajaalaa + 5) != 1 || serulaalü_ajutuu.기억읽기(anaajaalaa + 6) != 1
            || 짧은수(anaajaalaa + 16) != 2 || 짧은수(anaajaalaa + 18) != 3 || 수(anaajaalaa + 20) != 1
            || 짧은수(anaajaalaa + 40) != 52 || 짧은수(anaajaalaa + 42) != 32) return -8;
        int ekeroliaa_o_uchikanain_ajutuu = 수(anaajaalaa + 24);
        int 표위치 = 수(anaajaalaa + 28);
        int 개수 = 짧은수(anaajaalaa + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > akaliaa_ajutuu - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 개수; ee_iyatialujuna++) {
            int 표 = anaajaalaa + 표위치 + ee_iyatialujuna * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 a_ataa/해석기 미지원
            if (종류 != 1) continue;
            int 위치 = 수(표 + 4), ejepüsee = 수(표 + 8), 파일크기 = 수(표 + 16), 기억크기 = 수(표 + 20);
            int aliniaajaa_ajutuu = 수(표 + 28);
            if (ejepüsee < achuwalaa_ka_yataayakalü_akumajiaa || ejepüsee >= ayaakuaa_ajattiraa_ejepüsee || 기억크기 < 0 || 기억크기 > ayaakuaa_ajattiraa_ejepüsee - ejepüsee
                || 파일크기 < 0 || 파일크기 > 기억크기 || 위치 < 0 || (파일크기 > 0 && 위치 > akaliaa_ajutuu - 파일크기)
                || (aliniaajaa_ajutuu != 0 && (aliniaajaa_ajutuu < 0 || (aliniaajaa_ajutuu & (aliniaajaa_ajutuu - 1)) != 0
                    || ((ejepüsee - 위치) & (aliniaajaa_ajutuu - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < ee_iyatialujuna; 앞++) {
                int 이전 = anaajaalaa + 표위치 + 앞 * 32;
                if (수(이전) == 1 && 기억크기 > 0 && 수(이전 + 20) > 0
                    && ejepüsee < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < ejepüsee + 기억크기) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && ekeroliaa_o_uchikanain_ajutuu >= ejepüsee && ekeroliaa_o_uchikanain_ajutuu - ejepüsee < 파일크기) 실행가능 = true;
        }
        return 실행가능 ? ekeroliaa_o_uchikanain_ajutuu : -8;
    }

    static int 실행(int[] 입력, int 시작, int akaliaa_ajutuu) {
        while (시작 < akaliaa_ajutuu && 입력[시작] == ' ') 시작++;
        int 끝 = 시작;
        while (끝 < akaliaa_ajutuu && 입력[끝] != ' ') 끝++;
        int ekeroliaa_ajutuu = 찾기(입력, 시작, 끝 - 시작);
        if (ekeroliaa_ajutuu == 0) return -2;
        int 위치 = 수(ekeroliaa_ajutuu + 16), 크기 = 수(ekeroliaa_ajutuu + 20);
        if (위치 < 8 + 묶음개수() * 24 || 크기 < 52 || 위치 > serulaalü_ajutuu.실행묶음크기() - 크기) return -8;
        int anaajaalaa = serulaalü_ajutuu.실행묶음() + 위치;
        int ekeroliaa_o_uchikanain_ajutuu = 검증(anaajaalaa, 크기);
        if (ekeroliaa_o_uchikanain_ajutuu < 0) return ekeroliaa_o_uchikanain_ajutuu;
        serulaalü_ajutuu.ka_yataayakalü_ama_inrüinjiraa_TA();
        int 표위치 = 수(anaajaalaa + 28), 개수 = 짧은수(anaajaalaa + 44);
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 개수; ee_iyatialujuna++) {
            int 표 = anaajaalaa + 표위치 + ee_iyatialujuna * 32;
            if (수(표) != 1) continue;
            int 원본 = anaajaalaa + 수(표 + 4), jalamüinjatü_ajutuu = 수(표 + 8), 파일크기 = 수(표 + 16);
            for (int waai_ajutuu = 0; waai_ajutuu < 파일크기; waai_ajutuu++) serulaalü_ajutuu.기억쓰기(jalamüinjatü_ajutuu + waai_ajutuu, serulaalü_ajutuu.기억읽기(원본 + waai_ajutuu));
        }
        인수수 = 0;
        int 저장 = ajutuu_achuwalaa;
        while (끝 < akaliaa_ajutuu) {
            while (끝 < akaliaa_ajutuu && 입력[끝] == ' ') 끝++;
            if (끝 == akaliaa_ajutuu) break;
            if (인수수 == ajutuu_ejepüsee.length) return -22;
            시작 = 끝;
            while (끝 < akaliaa_ajutuu && 입력[끝] != ' ') 끝++;
            ajutuu_ejepüsee[인수수++] = 저장;
            수쓰기(저장, 끝 - 시작);
            for (int jeerü_ajutuu = 시작; jeerü_ajutuu < 끝; jeerü_ajutuu++) 수쓰기(저장 + 4 + (jeerü_ajutuu - 시작) * 4, 입력[jeerü_ajutuu]);
            저장 += 4 + (끝 - 시작) * 4;
        }
        통신망.과정정리();
        파일서술자관리.과정시작();
        int 결과 = serulaalü_ajutuu.사용자실행(ekeroliaa_o_uchikanain_ajutuu, ka_yataayakalü_ajattiraa - 16);
        파일서술자관리.과정정리();
        통신망.과정정리();
        return 결과;
    }
}
