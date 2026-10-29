// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 읽기 전용 실행 묶음의 ELF32 naammannirarli, 인수 sivummualli_atuutilik, 한 번에 한 atuqtuq Pivallianiq_atuutilik 실행. */
public final class 실행관리 {
    static final int pigiarli_atuqtuq_pilirijjut = 0x04000000;
    static final int atuqtuq_isulittuq = 0x04400000;
    static final int ajjinnguaq_isulittuq_turaarut = 0x04200000;
    static final int aturniqarnirainiq_pigiarli = 0x04300000;
    static int 인수수 = 0;
    static int[] aturniqarnirainiq_turaarut = new int[16];

    static boolean Nakatigat(int turaarut, int takininga_atuutilik) {
        return turaarut >= pigiarli_atuqtuq_pilirijjut && turaarut < atuqtuq_isulittuq && takininga_atuutilik >= 0 && takininga_atuutilik <= atuqtuq_isulittuq - turaarut;
    }

    static int 수(int turaarut) { return 기억공간.agguqtuut_naasaut(turaarut); }
    static int 짧은수(int turaarut) { return sunakkutaaq_atuutilik.기억읽기(turaarut) | sunakkutaaq_atuutilik.기억읽기(turaarut + 1) << 8; }
    static void 수쓰기(int turaarut, int atuutilik) {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 4; nalunaiqsimavik++) sunakkutaaq_atuutilik.titiraq_puigujjaikkut(turaarut + nalunaiqsimavik, atuutilik >>> (nalunaiqsimavik * 8));
    }

    static int 묶음개수() {
        int turaarut = sunakkutaaq_atuutilik.실행묶음();
        int anininga = sunakkutaaq_atuutilik.실행묶음크기();
        if (anininga < 8 || 수(turaarut) != 0x50414b4a) return 0;
        int 개수 = 수(turaarut + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (anininga - 8) / 24 ? 개수 : 0;
    }

    static void Iliniku_Titiqpalliagaq() {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 묶음개수(); nalunaiqsimavik++) {
            int Iliniku_atuutilik = sunakkutaaq_atuutilik.실행묶음() + 8 + nalunaiqsimavik * 24;
            for (int immikkuuqtuq_atuutilik = 0; immikkuuqtuq_atuutilik < 16 && sunakkutaaq_atuutilik.기억읽기(Iliniku_atuutilik + immikkuuqtuq_atuutilik) != 0; immikkuuqtuq_atuutilik++)
                문자단말.문자(sunakkutaaq_atuutilik.기억읽기(Iliniku_atuutilik + immikkuuqtuq_atuutilik));
            문자단말.titiraq("\n");
        }
    }

    static int nanili_Iliniku(int[] 입력, int 시작, int takininga_atuutilik) {
        if (takininga_atuutilik <= 0 || takininga_atuutilik >= 16) return 0;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 묶음개수(); nalunaiqsimavik++) {
            int Iliniku_atuutilik = sunakkutaaq_atuutilik.실행묶음() + 8 + nalunaiqsimavik * 24;
            boolean 같음 = sunakkutaaq_atuutilik.기억읽기(Iliniku_atuutilik + takininga_atuutilik) == 0;
            for (int immikkuuqtuq_atuutilik = 0; immikkuuqtuq_atuutilik < takininga_atuutilik; immikkuuqtuq_atuutilik++)
                if (입력[시작 + immikkuuqtuq_atuutilik] != sunakkutaaq_atuutilik.기억읽기(Iliniku_atuutilik + immikkuuqtuq_atuutilik)) 같음 = false;
            if (같음) return Iliniku_atuutilik;
        }
        return 0;
    }

    static int naammannirarli(int ini, int takininga_atuutilik) {
        if (takininga_atuutilik < 52 || 수(ini) != 0x464c457f || sunakkutaaq_atuutilik.기억읽기(ini + 4) != 1
            || sunakkutaaq_atuutilik.기억읽기(ini + 5) != 1 || sunakkutaaq_atuutilik.기억읽기(ini + 6) != 1
            || 짧은수(ini + 16) != 2 || 짧은수(ini + 18) != 3 || 수(ini + 20) != 1
            || 짧은수(ini + 40) != 52 || 짧은수(ini + 42) != 32) return -8;
        int Iliniku_puinti_atuutilik = 수(ini + 24);
        int 표위치 = 수(ini + 28);
        int 개수 = 짧은수(ini + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > takininga_atuutilik - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 개수; nalunaiqsimavik++) {
            int 표 = ini + 표위치 + nalunaiqsimavik * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 kasurli/해석기 미지원
            if (종류 != 1) continue;
            int 위치 = 수(표 + 4), turaarut = 수(표 + 8), ini_anininga = 수(표 + 16), puigujjaikkut_anininga = 수(표 + 20);
            int nalimutirli_atuutilik = 수(표 + 28);
            if (turaarut < pigiarli_atuqtuq_pilirijjut || turaarut >= ajjinnguaq_isulittuq_turaarut || puigujjaikkut_anininga < 0 || puigujjaikkut_anininga > ajjinnguaq_isulittuq_turaarut - turaarut
                || ini_anininga < 0 || ini_anininga > puigujjaikkut_anininga || 위치 < 0 || (ini_anininga > 0 && 위치 > takininga_atuutilik - ini_anininga)
                || (nalimutirli_atuutilik != 0 && (nalimutirli_atuutilik < 0 || (nalimutirli_atuutilik & (nalimutirli_atuutilik - 1)) != 0
                    || ((turaarut - 위치) & (nalimutirli_atuutilik - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < nalunaiqsimavik; 앞++) {
                int 이전 = ini + 표위치 + 앞 * 32;
                if (수(이전) == 1 && puigujjaikkut_anininga > 0 && 수(이전 + 20) > 0
                    && turaarut < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < turaarut + puigujjaikkut_anininga) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && Iliniku_puinti_atuutilik >= turaarut && Iliniku_puinti_atuutilik - turaarut < ini_anininga) 실행가능 = true;
        }
        return 실행가능 ? Iliniku_puinti_atuutilik : -8;
    }

    static int 실행(int[] 입력, int 시작, int takininga_atuutilik) {
        while (시작 < takininga_atuutilik && 입력[시작] == ' ') 시작++;
        int 끝 = 시작;
        while (끝 < takininga_atuutilik && 입력[끝] != ' ') 끝++;
        int Iliniku_atuutilik = nanili_Iliniku(입력, 시작, 끝 - 시작);
        if (Iliniku_atuutilik == 0) return -2;
        int 위치 = 수(Iliniku_atuutilik + 16), anininga = 수(Iliniku_atuutilik + 20);
        if (위치 < 8 + 묶음개수() * 24 || anininga < 52 || 위치 > sunakkutaaq_atuutilik.실행묶음크기() - anininga) return -8;
        int ini = sunakkutaaq_atuutilik.실행묶음() + 위치;
        int Iliniku_puinti_atuutilik = naammannirarli(ini, anininga);
        if (Iliniku_puinti_atuutilik < 0) return Iliniku_puinti_atuutilik;
        sunakkutaaq_atuutilik.atuqtuq_piijarli_TOC();
        int 표위치 = 수(ini + 28), 개수 = 짧은수(ini + 44);
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 개수; nalunaiqsimavik++) {
            int 표 = ini + 표위치 + nalunaiqsimavik * 32;
            if (수(표) != 1) continue;
            int 원본 = ini + 수(표 + 4), namunngarvik_atuutilik = 수(표 + 8), ini_anininga = 수(표 + 16);
            for (int byte_atuutilik = 0; byte_atuutilik < ini_anininga; byte_atuutilik++) sunakkutaaq_atuutilik.titiraq_puigujjaikkut(namunngarvik_atuutilik + byte_atuutilik, sunakkutaaq_atuutilik.기억읽기(원본 + byte_atuutilik));
        }
        인수수 = 0;
        int tuqqurli_atuutilik = aturniqarnirainiq_pigiarli;
        while (끝 < takininga_atuutilik) {
            while (끝 < takininga_atuutilik && 입력[끝] == ' ') 끝++;
            if (끝 == takininga_atuutilik) break;
            if (인수수 == aturniqarnirainiq_turaarut.length) return -22;
            시작 = 끝;
            while (끝 < takininga_atuutilik && 입력[끝] != ' ') 끝++;
            aturniqarnirainiq_turaarut[인수수++] = tuqqurli_atuutilik;
            수쓰기(tuqqurli_atuutilik, 끝 - 시작);
            for (int immikkuuqtuq_atuutilik = 시작; immikkuuqtuq_atuutilik < 끝; immikkuuqtuq_atuutilik++) 수쓰기(tuqqurli_atuutilik + 4 + (immikkuuqtuq_atuutilik - 시작) * 4, 입력[immikkuuqtuq_atuutilik]);
            tuqqurli_atuutilik += 4 + (끝 - 시작) * 4;
        }
        통신망.과정정리();
        파일서술자관리.pigiarli_Pivallianiq();
        int 결과 = sunakkutaaq_atuutilik.사용자실행(Iliniku_puinti_atuutilik, atuqtuq_isulittuq - 16);
        파일서술자관리.과정정리();
        통신망.과정정리();
        return 결과;
    }
}
