// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 읽기 전용 gukora_ibwiriza 묶음의 ELF32 kwemeza, 인수 koherereza_agaciro, 한 번에 한 ukoresha Inzira_agaciro gukora_ibwiriza. */
public final class 실행관리 {
    static final int Itangira_ukoresha_porogaramu = 0x04000000;
    static final int ukoresha_kurangiza = 0x04400000;
    static final int ishusho_kurangiza_aderesi = 0x04200000;
    static final int ingingo_Itangira = 0x04300000;
    static int 인수수 = 0;
    static int[] ingingo_aderesi = new int[16];

    static boolean kiripu(int aderesi, int uburebure_agaciro) {
        return aderesi >= Itangira_ukoresha_porogaramu && aderesi < ukoresha_kurangiza && uburebure_agaciro >= 0 && uburebure_agaciro <= ukoresha_kurangiza - aderesi;
    }

    static int 수(int aderesi) { return 기억공간.gusesengura_umubare_wuzuye(aderesi); }
    static int 짧은수(int aderesi) { return igendanwa_agaciro.기억읽기(aderesi) | igendanwa_agaciro.기억읽기(aderesi + 1) << 8; }
    static void 수쓰기(int aderesi, int agaciro) {
        for (int umugerekashakiro = 0; umugerekashakiro < 4; umugerekashakiro++) igendanwa_agaciro.kwandika_ububiko(aderesi + umugerekashakiro, agaciro >>> (umugerekashakiro * 8));
    }

    static int 묶음개수() {
        int aderesi = igendanwa_agaciro.실행묶음();
        int Ingano = igendanwa_agaciro.실행묶음크기();
        if (Ingano < 8 || 수(aderesi) != 0x50414b4a) return 0;
        int 개수 = 수(aderesi + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (Ingano - 8) / 24 ? 개수 : 0;
    }

    static void icyinjizwa_Urutonde() {
        for (int umugerekashakiro = 0; umugerekashakiro < 묶음개수(); umugerekashakiro++) {
            int icyinjizwa_agaciro = igendanwa_agaciro.실행묶음() + 8 + umugerekashakiro * 24;
            for (int inyuguti_agaciro = 0; inyuguti_agaciro < 16 && igendanwa_agaciro.기억읽기(icyinjizwa_agaciro + inyuguti_agaciro) != 0; inyuguti_agaciro++)
                문자단말.문자(igendanwa_agaciro.기억읽기(icyinjizwa_agaciro + inyuguti_agaciro));
            문자단말.kwandika("\n");
        }
    }

    static int gushaka_icyinjizwa(int[] 입력, int ihuriro, int uburebure_agaciro) {
        if (uburebure_agaciro <= 0 || uburebure_agaciro >= 16) return 0;
        for (int umugerekashakiro = 0; umugerekashakiro < 묶음개수(); umugerekashakiro++) {
            int icyinjizwa_agaciro = igendanwa_agaciro.실행묶음() + 8 + umugerekashakiro * 24;
            boolean 같음 = igendanwa_agaciro.기억읽기(icyinjizwa_agaciro + uburebure_agaciro) == 0;
            for (int inyuguti_agaciro = 0; inyuguti_agaciro < uburebure_agaciro; inyuguti_agaciro++)
                if (입력[ihuriro + inyuguti_agaciro] != igendanwa_agaciro.기억읽기(icyinjizwa_agaciro + inyuguti_agaciro)) 같음 = false;
            if (같음) return icyinjizwa_agaciro;
        }
        return 0;
    }

    static int kwemeza(int Idosiye, int uburebure_agaciro) {
        if (uburebure_agaciro < 52 || 수(Idosiye) != 0x464c457f || igendanwa_agaciro.기억읽기(Idosiye + 4) != 1
            || igendanwa_agaciro.기억읽기(Idosiye + 5) != 1 || igendanwa_agaciro.기억읽기(Idosiye + 6) != 1
            || 짧은수(Idosiye + 16) != 2 || 짧은수(Idosiye + 18) != 3 || 수(Idosiye + 20) != 1
            || 짧은수(Idosiye + 40) != 52 || 짧은수(Idosiye + 42) != 32) return -8;
        int icyinjizwa_inota_agaciro = 수(Idosiye + 24);
        int 표위치 = 수(Idosiye + 28);
        int 개수 = 짧은수(Idosiye + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > uburebure_agaciro - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int umugerekashakiro = 0; umugerekashakiro < 개수; umugerekashakiro++) {
            int 표 = Idosiye + 표위치 + umugerekashakiro * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Guhuza/해석기 미지원
            if (종류 != 1) continue;
            int 위치 = 수(표 + 4), aderesi = 수(표 + 8), dosiye_ingano = 수(표 + 16), ububiko_ingano = 수(표 + 20);
            int gutondeka_agaciro = 수(표 + 28);
            if (aderesi < Itangira_ukoresha_porogaramu || aderesi >= ishusho_kurangiza_aderesi || ububiko_ingano < 0 || ububiko_ingano > ishusho_kurangiza_aderesi - aderesi
                || dosiye_ingano < 0 || dosiye_ingano > ububiko_ingano || 위치 < 0 || (dosiye_ingano > 0 && 위치 > uburebure_agaciro - dosiye_ingano)
                || (gutondeka_agaciro != 0 && (gutondeka_agaciro < 0 || (gutondeka_agaciro & (gutondeka_agaciro - 1)) != 0
                    || ((aderesi - 위치) & (gutondeka_agaciro - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < umugerekashakiro; 앞++) {
                int 이전 = Idosiye + 표위치 + 앞 * 32;
                if (수(이전) == 1 && ububiko_ingano > 0 && 수(이전 + 20) > 0
                    && aderesi < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < aderesi + ububiko_ingano) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && icyinjizwa_inota_agaciro >= aderesi && icyinjizwa_inota_agaciro - aderesi < dosiye_ingano) 실행가능 = true;
        }
        return 실행가능 ? icyinjizwa_inota_agaciro : -8;
    }

    static int gukora_ibwiriza(int[] 입력, int ihuriro, int uburebure_agaciro) {
        while (ihuriro < uburebure_agaciro && 입력[ihuriro] == ' ') ihuriro++;
        int 끝 = ihuriro;
        while (끝 < uburebure_agaciro && 입력[끝] != ' ') 끝++;
        int icyinjizwa_agaciro = gushaka_icyinjizwa(입력, ihuriro, 끝 - ihuriro);
        if (icyinjizwa_agaciro == 0) return -2;
        int 위치 = 수(icyinjizwa_agaciro + 16), Ingano = 수(icyinjizwa_agaciro + 20);
        if (위치 < 8 + 묶음개수() * 24 || Ingano < 52 || 위치 > igendanwa_agaciro.실행묶음크기() - Ingano) return -8;
        int Idosiye = igendanwa_agaciro.실행묶음() + 위치;
        int icyinjizwa_inota_agaciro = kwemeza(Idosiye, Ingano);
        if (icyinjizwa_inota_agaciro < 0) return icyinjizwa_inota_agaciro;
        igendanwa_agaciro.ukoresha_gukuraho_TOC();
        int 표위치 = 수(Idosiye + 28), 개수 = 짧은수(Idosiye + 44);
        for (int umugerekashakiro = 0; umugerekashakiro < 개수; umugerekashakiro++) {
            int 표 = Idosiye + 표위치 + umugerekashakiro * 32;
            if (수(표) != 1) continue;
            int 원본 = Idosiye + 수(표 + 4), aho_ijya_agaciro = 수(표 + 8), dosiye_ingano = 수(표 + 16);
            for (int bayiti_agaciro = 0; bayiti_agaciro < dosiye_ingano; bayiti_agaciro++) igendanwa_agaciro.kwandika_ububiko(aho_ijya_agaciro + bayiti_agaciro, igendanwa_agaciro.기억읽기(원본 + bayiti_agaciro));
        }
        인수수 = 0;
        int Store_agaciro = ingingo_Itangira;
        while (끝 < uburebure_agaciro) {
            while (끝 < uburebure_agaciro && 입력[끝] == ' ') 끝++;
            if (끝 == uburebure_agaciro) break;
            if (인수수 == ingingo_aderesi.length) return -22;
            ihuriro = 끝;
            while (끝 < uburebure_agaciro && 입력[끝] != ' ') 끝++;
            ingingo_aderesi[인수수++] = Store_agaciro;
            수쓰기(Store_agaciro, 끝 - ihuriro);
            for (int inyuguti_agaciro = ihuriro; inyuguti_agaciro < 끝; inyuguti_agaciro++) 수쓰기(Store_agaciro + 4 + (inyuguti_agaciro - ihuriro) * 4, 입력[inyuguti_agaciro]);
            Store_agaciro += 4 + (끝 - ihuriro) * 4;
        }
        Urusobemiyoboro_Ikirundo.과정정리();
        파일서술자관리.Itangira_Inzira();
        int 결과 = igendanwa_agaciro.ihuriro_ukoresha_porogaramu(icyinjizwa_inota_agaciro, ukoresha_kurangiza - 16);
        파일서술자관리.과정정리();
        Urusobemiyoboro_Ikirundo.과정정리();
        return 결과;
    }
}
