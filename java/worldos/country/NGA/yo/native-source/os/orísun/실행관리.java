// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Kàá 전용 ṣiṣẹ́_àṣẹ 묶음의 ELF32 ìfọwọ́síìwé, 인수 tari_sí_iye, 한 번에 한 aṣàmúlò Ìlànà_iye ṣiṣẹ́_àṣẹ. */
public final class 실행관리 {
    static final int bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò = 0x04000000;
    static final int aṣàmúlò_parí = 0x04400000;
    static final int àwòrán_parí_àdírẹ́ẹ̀sì = 0x04200000;
    static final int ágúmẹ́ntì_bẹ̀rẹ̀ = 0x04300000;
    static int 인수수 = 0;
    static int[] ágúmẹ́ntì_àdírẹ́ẹ̀sì = new int[16];

    static boolean ní_ṣókí(int àdírẹ́ẹ̀sì, int gígùn_iye) {
        return àdírẹ́ẹ̀sì >= bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò && àdírẹ́ẹ̀sì < aṣàmúlò_parí && gígùn_iye >= 0 && gígùn_iye <= aṣàmúlò_parí - àdírẹ́ẹ̀sì;
    }

    static int 수(int àdírẹ́ẹ̀sì) { return 기억공간.ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(àdírẹ́ẹ̀sì); }
    static int 짧은수(int àdírẹ́ẹ̀sì) { return ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì) | ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì + 1) << 8; }
    static void 수쓰기(int àdírẹ́ẹ̀sì, int iye) {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 4; wá_atọ̀ka_àkóónú++) ohun_èlò_iye.kọ_ibi_ìpamọ́(àdírẹ́ẹ̀sì + wá_atọ̀ka_àkóónú, iye >>> (wá_atọ̀ka_àkóónú * 8));
    }

    static int 묶음개수() {
        int àdírẹ́ẹ̀sì = ohun_èlò_iye.실행묶음();
        int Ìwọ̀n = ohun_èlò_iye.실행묶음크기();
        if (Ìwọ̀n < 8 || 수(àdírẹ́ẹ̀sì) != 0x50414b4a) return 0;
        int 개수 = 수(àdírẹ́ẹ̀sì + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (Ìwọ̀n - 8) / 24 ? 개수 : 0;
    }

    static void ìgbéwọlé_Àtòkọ() {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 묶음개수(); wá_atọ̀ka_àkóónú++) {
            int ìgbéwọlé_iye = ohun_èlò_iye.실행묶음() + 8 + wá_atọ̀ka_àkóónú * 24;
            for (int ẹyọ_ọ̀rọ̀_iye = 0; ẹyọ_ọ̀rọ̀_iye < 16 && ohun_èlò_iye.기억읽기(ìgbéwọlé_iye + ẹyọ_ọ̀rọ̀_iye) != 0; ẹyọ_ọ̀rọ̀_iye++)
                문자단말.문자(ohun_èlò_iye.기억읽기(ìgbéwọlé_iye + ẹyọ_ọ̀rọ̀_iye));
            문자단말.Kọ("\n");
        }
    }

    static int wá_ìgbéwọlé(int[] 입력, int Rọ́ọ̀nù, int gígùn_iye) {
        if (gígùn_iye <= 0 || gígùn_iye >= 16) return 0;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 묶음개수(); wá_atọ̀ka_àkóónú++) {
            int ìgbéwọlé_iye = ohun_èlò_iye.실행묶음() + 8 + wá_atọ̀ka_àkóónú * 24;
            boolean 같음 = ohun_èlò_iye.기억읽기(ìgbéwọlé_iye + gígùn_iye) == 0;
            for (int ẹyọ_ọ̀rọ̀_iye = 0; ẹyọ_ọ̀rọ̀_iye < gígùn_iye; ẹyọ_ọ̀rọ̀_iye++)
                if (입력[Rọ́ọ̀nù + ẹyọ_ọ̀rọ̀_iye] != ohun_èlò_iye.기억읽기(ìgbéwọlé_iye + ẹyọ_ọ̀rọ̀_iye)) 같음 = false;
            if (같음) return ìgbéwọlé_iye;
        }
        return 0;
    }

    static int ìfọwọ́síìwé(int Fáìlì, int gígùn_iye) {
        if (gígùn_iye < 52 || 수(Fáìlì) != 0x464c457f || ohun_èlò_iye.기억읽기(Fáìlì + 4) != 1
            || ohun_èlò_iye.기억읽기(Fáìlì + 5) != 1 || ohun_èlò_iye.기억읽기(Fáìlì + 6) != 1
            || 짧은수(Fáìlì + 16) != 2 || 짧은수(Fáìlì + 18) != 3 || 수(Fáìlì + 20) != 1
            || 짧은수(Fáìlì + 40) != 52 || 짧은수(Fáìlì + 42) != 32) return -8;
        int ìgbéwọlé_kókó_iye = 수(Fáìlì + 24);
        int 표위치 = 수(Fáìlì + 28);
        int 개수 = 짧은수(Fáìlì + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > gígùn_iye - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 개수; wá_atọ̀ka_àkóónú++) {
            int 표 = Fáìlì + 표위치 + wá_atọ̀ka_àkóónú * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Darapọ̀/해석기 미지원
            if (종류 != 1) continue;
            int 위치 = 수(표 + 4), àdírẹ́ẹ̀sì = 수(표 + 8), fáìlì_ìwọn = 수(표 + 16), ibi_ìpamọ́_ìwọn = 수(표 + 20);
            int mu_dọ́gba_iye = 수(표 + 28);
            if (àdírẹ́ẹ̀sì < bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò || àdírẹ́ẹ̀sì >= àwòrán_parí_àdírẹ́ẹ̀sì || ibi_ìpamọ́_ìwọn < 0 || ibi_ìpamọ́_ìwọn > àwòrán_parí_àdírẹ́ẹ̀sì - àdírẹ́ẹ̀sì
                || fáìlì_ìwọn < 0 || fáìlì_ìwọn > ibi_ìpamọ́_ìwọn || 위치 < 0 || (fáìlì_ìwọn > 0 && 위치 > gígùn_iye - fáìlì_ìwọn)
                || (mu_dọ́gba_iye != 0 && (mu_dọ́gba_iye < 0 || (mu_dọ́gba_iye & (mu_dọ́gba_iye - 1)) != 0
                    || ((àdírẹ́ẹ̀sì - 위치) & (mu_dọ́gba_iye - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < wá_atọ̀ka_àkóónú; 앞++) {
                int 이전 = Fáìlì + 표위치 + 앞 * 32;
                if (수(이전) == 1 && ibi_ìpamọ́_ìwọn > 0 && 수(이전 + 20) > 0
                    && àdírẹ́ẹ̀sì < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < àdírẹ́ẹ̀sì + ibi_ìpamọ́_ìwọn) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && ìgbéwọlé_kókó_iye >= àdírẹ́ẹ̀sì && ìgbéwọlé_kókó_iye - àdírẹ́ẹ̀sì < fáìlì_ìwọn) 실행가능 = true;
        }
        return 실행가능 ? ìgbéwọlé_kókó_iye : -8;
    }

    static int ṣiṣẹ́_àṣẹ(int[] 입력, int Rọ́ọ̀nù, int gígùn_iye) {
        while (Rọ́ọ̀nù < gígùn_iye && 입력[Rọ́ọ̀nù] == ' ') Rọ́ọ̀nù++;
        int 끝 = Rọ́ọ̀nù;
        while (끝 < gígùn_iye && 입력[끝] != ' ') 끝++;
        int ìgbéwọlé_iye = wá_ìgbéwọlé(입력, Rọ́ọ̀nù, 끝 - Rọ́ọ̀nù);
        if (ìgbéwọlé_iye == 0) return -2;
        int 위치 = 수(ìgbéwọlé_iye + 16), Ìwọ̀n = 수(ìgbéwọlé_iye + 20);
        if (위치 < 8 + 묶음개수() * 24 || Ìwọ̀n < 52 || 위치 > ohun_èlò_iye.실행묶음크기() - Ìwọ̀n) return -8;
        int Fáìlì = ohun_èlò_iye.실행묶음() + 위치;
        int ìgbéwọlé_kókó_iye = ìfọwọ́síìwé(Fáìlì, Ìwọ̀n);
        if (ìgbéwọlé_kókó_iye < 0) return ìgbéwọlé_kókó_iye;
        ohun_èlò_iye.aṣàmúlò_mú_kúrò_TOC();
        int 표위치 = 수(Fáìlì + 28), 개수 = 짧은수(Fáìlì + 44);
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 개수; wá_atọ̀ka_àkóónú++) {
            int 표 = Fáìlì + 표위치 + wá_atọ̀ka_àkóónú * 32;
            if (수(표) != 1) continue;
            int 원본 = Fáìlì + 수(표 + 4), èbúté_iye = 수(표 + 8), fáìlì_ìwọn = 수(표 + 16);
            for (int báìtì_iye = 0; báìtì_iye < fáìlì_ìwọn; báìtì_iye++) ohun_èlò_iye.kọ_ibi_ìpamọ́(èbúté_iye + báìtì_iye, ohun_èlò_iye.기억읽기(원본 + báìtì_iye));
        }
        인수수 = 0;
        int Store_iye = ágúmẹ́ntì_bẹ̀rẹ̀;
        while (끝 < gígùn_iye) {
            while (끝 < gígùn_iye && 입력[끝] == ' ') 끝++;
            if (끝 == gígùn_iye) break;
            if (인수수 == ágúmẹ́ntì_àdírẹ́ẹ̀sì.length) return -22;
            Rọ́ọ̀nù = 끝;
            while (끝 < gígùn_iye && 입력[끝] != ' ') 끝++;
            ágúmẹ́ntì_àdírẹ́ẹ̀sì[인수수++] = Store_iye;
            수쓰기(Store_iye, 끝 - Rọ́ọ̀nù);
            for (int ẹyọ_ọ̀rọ̀_iye = Rọ́ọ̀nù; ẹyọ_ọ̀rọ̀_iye < 끝; ẹyọ_ọ̀rọ̀_iye++) 수쓰기(Store_iye + 4 + (ẹyọ_ọ̀rọ̀_iye - Rọ́ọ̀nù) * 4, 입력[ẹyọ_ọ̀rọ̀_iye]);
            Store_iye += 4 + (끝 - Rọ́ọ̀nù) * 4;
        }
        Alásopọ̀_kójọ.과정정리();
        파일서술자관리.bẹ̀rẹ̀_Ìlànà();
        int 결과 = ohun_èlò_iye.ṣiṣẹ́_aṣàmúlò_àtòjọ_ètò(ìgbéwọlé_kókó_iye, aṣàmúlò_parí - 16);
        파일서술자관리.과정정리();
        Alásopọ̀_kójọ.과정정리();
        return 결과;
    }
}
