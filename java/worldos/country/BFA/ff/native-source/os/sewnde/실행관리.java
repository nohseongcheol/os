// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 읽기 전용 실행 묶음의 ELF32 검증, 인수 yawtinde_njaru, 한 번에 한 kuutoro Yuɓɓo_golle_njaru 실행. */
public final class 실행관리 {
    static final int huɓɓude_kuutoro_tafirde = 0x04000000;
    static final int kuutoro_taƴde = 0x04400000;
    static final int natal_taƴde_ñiiɓirde = 0x04200000;
    static final int hujja_huɓɓude = 0x04300000;
    static int 인수수 = 0;
    static int[] hujja_ñiiɓirde = new int[16];

    static boolean kilip(int ñiiɓirde, int njuuteendi_njaru) {
        return ñiiɓirde >= huɓɓude_kuutoro_tafirde && ñiiɓirde < kuutoro_taƴde && njuuteendi_njaru >= 0 && njuuteendi_njaru <= kuutoro_taƴde - ñiiɓirde;
    }

    static int 수(int ñiiɓirde) { return 기억공간.정수읽기(ñiiɓirde); }
    static int 짧은수(int ñiiɓirde) { return kaɓirgal_njaru.기억읽기(ñiiɓirde) | kaɓirgal_njaru.기억읽기(ñiiɓirde + 1) << 8; }
    static void 수쓰기(int ñiiɓirde, int njaru) {
        for (int joopirdu = 0; joopirdu < 4; joopirdu++) kaɓirgal_njaru.winndude_teskordu(ñiiɓirde + joopirdu, njaru >>> (joopirdu * 8));
    }

    static int 묶음개수() {
        int ñiiɓirde = kaɓirgal_njaru.실행묶음();
        int waylude_etannde = kaɓirgal_njaru.실행묶음크기();
        if (waylude_etannde < 8 || 수(ñiiɓirde) != 0x50414b4a) return 0;
        int 개수 = 수(ñiiɓirde + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (waylude_etannde - 8) / 24 ? 개수 : 0;
    }

    static void naatnugol_Doggol() {
        for (int joopirdu = 0; joopirdu < 묶음개수(); joopirdu++) {
            int naatnugol_njaru = kaɓirgal_njaru.실행묶음() + 8 + joopirdu * 24;
            for (int alkulal_njaru = 0; alkulal_njaru < 16 && kaɓirgal_njaru.기억읽기(naatnugol_njaru + alkulal_njaru) != 0; alkulal_njaru++)
                문자단말.문자(kaɓirgal_njaru.기억읽기(naatnugol_njaru + alkulal_njaru));
            문자단말.winndude("\n");
        }
    }

    static int yiylaade_naatnugol(int[] 입력, int huutoraade, int njuuteendi_njaru) {
        if (njuuteendi_njaru <= 0 || njuuteendi_njaru >= 16) return 0;
        for (int joopirdu = 0; joopirdu < 묶음개수(); joopirdu++) {
            int naatnugol_njaru = kaɓirgal_njaru.실행묶음() + 8 + joopirdu * 24;
            boolean 같음 = kaɓirgal_njaru.기억읽기(naatnugol_njaru + njuuteendi_njaru) == 0;
            for (int alkulal_njaru = 0; alkulal_njaru < njuuteendi_njaru; alkulal_njaru++)
                if (입력[huutoraade + alkulal_njaru] != kaɓirgal_njaru.기억읽기(naatnugol_njaru + alkulal_njaru)) 같음 = false;
            if (같음) return naatnugol_njaru;
        }
        return 0;
    }

    static int 검증(int fiilde, int njuuteendi_njaru) {
        if (njuuteendi_njaru < 52 || 수(fiilde) != 0x464c457f || kaɓirgal_njaru.기억읽기(fiilde + 4) != 1
            || kaɓirgal_njaru.기억읽기(fiilde + 5) != 1 || kaɓirgal_njaru.기억읽기(fiilde + 6) != 1
            || 짧은수(fiilde + 16) != 2 || 짧은수(fiilde + 18) != 3 || 수(fiilde + 20) != 1
            || 짧은수(fiilde + 40) != 52 || 짧은수(fiilde + 42) != 32) return -8;
        int naatnugol_toɓɓere_njaru = 수(fiilde + 24);
        int 표위치 = 수(fiilde + 28);
        int 개수 = 짧은수(fiilde + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > njuuteendi_njaru - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int joopirdu = 0; joopirdu < 개수; joopirdu++) {
            int 표 = fiilde + 표위치 + joopirdu * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 seŋaade/해석기 미지원
            if (종류 != 1) continue;
            int 위치 = 수(표 + 4), ñiiɓirde = 수(표 + 8), fiilde_waylude_etannde = 수(표 + 16), teskordu_waylude_etannde = 수(표 + 20);
            int fonndude_njaru = 수(표 + 28);
            if (ñiiɓirde < huɓɓude_kuutoro_tafirde || ñiiɓirde >= natal_taƴde_ñiiɓirde || teskordu_waylude_etannde < 0 || teskordu_waylude_etannde > natal_taƴde_ñiiɓirde - ñiiɓirde
                || fiilde_waylude_etannde < 0 || fiilde_waylude_etannde > teskordu_waylude_etannde || 위치 < 0 || (fiilde_waylude_etannde > 0 && 위치 > njuuteendi_njaru - fiilde_waylude_etannde)
                || (fonndude_njaru != 0 && (fonndude_njaru < 0 || (fonndude_njaru & (fonndude_njaru - 1)) != 0
                    || ((ñiiɓirde - 위치) & (fonndude_njaru - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < joopirdu; 앞++) {
                int 이전 = fiilde + 표위치 + 앞 * 32;
                if (수(이전) == 1 && teskordu_waylude_etannde > 0 && 수(이전 + 20) > 0
                    && ñiiɓirde < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < ñiiɓirde + teskordu_waylude_etannde) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && naatnugol_toɓɓere_njaru >= ñiiɓirde && naatnugol_toɓɓere_njaru - ñiiɓirde < fiilde_waylude_etannde) 실행가능 = true;
        }
        return 실행가능 ? naatnugol_toɓɓere_njaru : -8;
    }

    static int 실행(int[] 입력, int huutoraade, int njuuteendi_njaru) {
        while (huutoraade < njuuteendi_njaru && 입력[huutoraade] == ' ') huutoraade++;
        int 끝 = huutoraade;
        while (끝 < njuuteendi_njaru && 입력[끝] != ' ') 끝++;
        int naatnugol_njaru = yiylaade_naatnugol(입력, huutoraade, 끝 - huutoraade);
        if (naatnugol_njaru == 0) return -2;
        int 위치 = 수(naatnugol_njaru + 16), waylude_etannde = 수(naatnugol_njaru + 20);
        if (위치 < 8 + 묶음개수() * 24 || waylude_etannde < 52 || 위치 > kaɓirgal_njaru.실행묶음크기() - waylude_etannde) return -8;
        int fiilde = kaɓirgal_njaru.실행묶음() + 위치;
        int naatnugol_toɓɓere_njaru = 검증(fiilde, waylude_etannde);
        if (naatnugol_toɓɓere_njaru < 0) return naatnugol_toɓɓere_njaru;
        kaɓirgal_njaru.kuutoro_festude_Haatumeere_loowdi();
        int 표위치 = 수(fiilde + 28), 개수 = 짧은수(fiilde + 44);
        for (int joopirdu = 0; joopirdu < 개수; joopirdu++) {
            int 표 = fiilde + 표위치 + joopirdu * 32;
            if (수(표) != 1) continue;
            int 원본 = fiilde + 수(표 + 4), tiindaare_njaru = 수(표 + 8), fiilde_waylude_etannde = 수(표 + 16);
            for (int oktee_njaru = 0; oktee_njaru < fiilde_waylude_etannde; oktee_njaru++) kaɓirgal_njaru.winndude_teskordu(tiindaare_njaru + oktee_njaru, kaɓirgal_njaru.기억읽기(원본 + oktee_njaru));
        }
        인수수 = 0;
        int resde_njaru = hujja_huɓɓude;
        while (끝 < njuuteendi_njaru) {
            while (끝 < njuuteendi_njaru && 입력[끝] == ' ') 끝++;
            if (끝 == njuuteendi_njaru) break;
            if (인수수 == hujja_ñiiɓirde.length) return -22;
            huutoraade = 끝;
            while (끝 < njuuteendi_njaru && 입력[끝] != ' ') 끝++;
            hujja_ñiiɓirde[인수수++] = resde_njaru;
            수쓰기(resde_njaru, 끝 - huutoraade);
            for (int alkulal_njaru = huutoraade; alkulal_njaru < 끝; alkulal_njaru++) 수쓰기(resde_njaru + 4 + (alkulal_njaru - huutoraade) * 4, 입력[alkulal_njaru]);
            resde_njaru += 4 + (끝 - huutoraade) * 4;
        }
        통신망.과정정리();
        파일서술자관리.huɓɓude_Yuɓɓo_golle();
        int 결과 = kaɓirgal_njaru.huutoraade_kuutoro_tafirde(naatnugol_toɓɓere_njaru, kuutoro_taƴde - 16);
        파일서술자관리.과정정리();
        통신망.과정정리();
        return 결과;
    }
}
