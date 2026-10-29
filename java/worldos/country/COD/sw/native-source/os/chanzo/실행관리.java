// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 읽기 전용 tekeleza_amri 묶음의 ELF32 hakikisha, 인수 tuma_mbele_thamani, 한 번에 한 mtumiaji Mchakato_thamani tekeleza_amri. */
public final class 실행관리 {
    static final int Anza_mtumiaji_programu = 0x04000000;
    static final int mtumiaji_tamatia = 0x04400000;
    static final int picha_tamatia_anwani = 0x04200000;
    static final int hoja_Anza = 0x04300000;
    static int 인수수 = 0;
    static int[] hoja_anwani = new int[16];

    static boolean dondoo(int anwani, int urefu_thamani) {
        return anwani >= Anza_mtumiaji_programu && anwani < mtumiaji_tamatia && urefu_thamani >= 0 && urefu_thamani <= mtumiaji_tamatia - anwani;
    }

    static int 수(int anwani) { return 기억공간.changanua_namba_kamili(anwani); }
    static int 짧은수(int anwani) { return kifaa_thamani.기억읽기(anwani) | kifaa_thamani.기억읽기(anwani + 1) << 8; }
    static void 수쓰기(int anwani, int thamani) {
        for (int kielezo = 0; kielezo < 4; kielezo++) kifaa_thamani.andika_kumbukumbu(anwani + kielezo, thamani >>> (kielezo * 8));
    }

    static int 묶음개수() {
        int anwani = kifaa_thamani.실행묶음();
        int panga_ukubwa = kifaa_thamani.실행묶음크기();
        if (panga_ukubwa < 8 || 수(anwani) != 0x50414b4a) return 0;
        int 개수 = 수(anwani + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (panga_ukubwa - 8) / 24 ? 개수 : 0;
    }

    static void ingizo_Orodha() {
        for (int kielezo = 0; kielezo < 묶음개수(); kielezo++) {
            int ingizo_thamani = kifaa_thamani.실행묶음() + 8 + kielezo * 24;
            for (int kibambo_thamani = 0; kibambo_thamani < 16 && kifaa_thamani.기억읽기(ingizo_thamani + kibambo_thamani) != 0; kibambo_thamani++)
                문자단말.문자(kifaa_thamani.기억읽기(ingizo_thamani + kibambo_thamani));
            문자단말.andika("\n");
        }
    }

    static int gundua_ingizo(int[] 입력, int endesha, int urefu_thamani) {
        if (urefu_thamani <= 0 || urefu_thamani >= 16) return 0;
        for (int kielezo = 0; kielezo < 묶음개수(); kielezo++) {
            int ingizo_thamani = kifaa_thamani.실행묶음() + 8 + kielezo * 24;
            boolean 같음 = kifaa_thamani.기억읽기(ingizo_thamani + urefu_thamani) == 0;
            for (int kibambo_thamani = 0; kibambo_thamani < urefu_thamani; kibambo_thamani++)
                if (입력[endesha + kibambo_thamani] != kifaa_thamani.기억읽기(ingizo_thamani + kibambo_thamani)) 같음 = false;
            if (같음) return ingizo_thamani;
        }
        return 0;
    }

    static int hakikisha(int faili, int urefu_thamani) {
        if (urefu_thamani < 52 || 수(faili) != 0x464c457f || kifaa_thamani.기억읽기(faili + 4) != 1
            || kifaa_thamani.기억읽기(faili + 5) != 1 || kifaa_thamani.기억읽기(faili + 6) != 1
            || 짧은수(faili + 16) != 2 || 짧은수(faili + 18) != 3 || 수(faili + 20) != 1
            || 짧은수(faili + 40) != 52 || 짧은수(faili + 42) != 32) return -8;
        int ingizo_pointi_thamani = 수(faili + 24);
        int 표위치 = 수(faili + 28);
        int 개수 = 짧은수(faili + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > urefu_thamani - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int kielezo = 0; kielezo < 개수; kielezo++) {
            int 표 = faili + 표위치 + kielezo * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 UNGANISHA/kichanganuzi_48ee4b1b 미지원
            if (종류 != 1) continue;
            int 위치 = 수(표 + 4), anwani = 수(표 + 8), faili_panga_ukubwa = 수(표 + 16), kumbukumbu_panga_ukubwa = 수(표 + 20);
            int pangilia_thamani = 수(표 + 28);
            if (anwani < Anza_mtumiaji_programu || anwani >= picha_tamatia_anwani || kumbukumbu_panga_ukubwa < 0 || kumbukumbu_panga_ukubwa > picha_tamatia_anwani - anwani
                || faili_panga_ukubwa < 0 || faili_panga_ukubwa > kumbukumbu_panga_ukubwa || 위치 < 0 || (faili_panga_ukubwa > 0 && 위치 > urefu_thamani - faili_panga_ukubwa)
                || (pangilia_thamani != 0 && (pangilia_thamani < 0 || (pangilia_thamani & (pangilia_thamani - 1)) != 0
                    || ((anwani - 위치) & (pangilia_thamani - 1)) != 0))) return -8;
            for (int mbele_thamani = 0; mbele_thamani < kielezo; mbele_thamani++) {
                int 이전 = faili + 표위치 + mbele_thamani * 32;
                if (수(이전) == 1 && kumbukumbu_panga_ukubwa > 0 && 수(이전 + 20) > 0
                    && anwani < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < anwani + kumbukumbu_panga_ukubwa) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && ingizo_pointi_thamani >= anwani && ingizo_pointi_thamani - anwani < faili_panga_ukubwa) 실행가능 = true;
        }
        return 실행가능 ? ingizo_pointi_thamani : -8;
    }

    static int tekeleza_amri(int[] 입력, int endesha, int urefu_thamani) {
        while (endesha < urefu_thamani && 입력[endesha] == ' ') endesha++;
        int 끝 = endesha;
        while (끝 < urefu_thamani && 입력[끝] != ' ') 끝++;
        int ingizo_thamani = gundua_ingizo(입력, endesha, 끝 - endesha);
        if (ingizo_thamani == 0) return -2;
        int 위치 = 수(ingizo_thamani + 16), panga_ukubwa = 수(ingizo_thamani + 20);
        if (위치 < 8 + 묶음개수() * 24 || panga_ukubwa < 52 || 위치 > kifaa_thamani.실행묶음크기() - panga_ukubwa) return -8;
        int faili = kifaa_thamani.실행묶음() + 위치;
        int ingizo_pointi_thamani = hakikisha(faili, panga_ukubwa);
        if (ingizo_pointi_thamani < 0) return ingizo_pointi_thamani;
        kifaa_thamani.mtumiaji_ondoa_YAL();
        int 표위치 = 수(faili + 28), 개수 = 짧은수(faili + 44);
        for (int kielezo = 0; kielezo < 개수; kielezo++) {
            int 표 = faili + 표위치 + kielezo * 32;
            if (수(표) != 1) continue;
            int 원본 = faili + 수(표 + 4), fikio_thamani = 수(표 + 8), faili_panga_ukubwa = 수(표 + 16);
            for (int baiti_thamani = 0; baiti_thamani < faili_panga_ukubwa; baiti_thamani++) kifaa_thamani.andika_kumbukumbu(fikio_thamani + baiti_thamani, kifaa_thamani.기억읽기(원본 + baiti_thamani));
        }
        인수수 = 0;
        int Store_thamani = hoja_Anza;
        while (끝 < urefu_thamani) {
            while (끝 < urefu_thamani && 입력[끝] == ' ') 끝++;
            if (끝 == urefu_thamani) break;
            if (인수수 == hoja_anwani.length) return -22;
            endesha = 끝;
            while (끝 < urefu_thamani && 입력[끝] != ' ') 끝++;
            hoja_anwani[인수수++] = Store_thamani;
            수쓰기(Store_thamani, 끝 - endesha);
            for (int kibambo_thamani = endesha; kibambo_thamani < 끝; kibambo_thamani++) 수쓰기(Store_thamani + 4 + (kibambo_thamani - endesha) * 4, 입력[kibambo_thamani]);
            Store_thamani += 4 + (끝 - endesha) * 4;
        }
        Mtandao_Mpororo.Safi_Mchakato();
        파일서술자관리.Anza_Mchakato();
        int 결과 = kifaa_thamani.endesha_mtumiaji_programu(ingizo_pointi_thamani, mtumiaji_tamatia - 16);
        파일서술자관리.Safi_Mchakato();
        Mtandao_Mpororo.Safi_Mchakato();
        return 결과;
    }
}
