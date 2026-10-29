// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 icandelo_ixabiso. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Ugcino_isixhobo_uqhagamshelo {
    static boolean 사용가능 = false;
    static int[] icandelo_iingcombolo = new int[512];
    static void 잠깐기다리기() {
        for (int indeksa = 0; indeksa < 4; indeksa++) isixhobo_ixabiso.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Phumeza = isixhobo_ixabiso.밀리초();
        while (isixhobo_ixabiso.밀리초() - Phumeza < 500) {
            int imo_ixabiso = isixhobo_ixabiso.입출력바이트읽기(0x1f7);
            if (imo_ixabiso == 0 || imo_ixabiso == 255) return -19;
            if ((imo_ixabiso & 128) == 0) {
                if ((imo_ixabiso & 33) != 0) return -5;
                if (!자료필요 || (imo_ixabiso & 8) != 0) return 0;
            }
            isixhobo_ixabiso.잠시양보();
        }
        return -110;
    }
    static int 요청(int icandelo_ixabiso, int Umyalelo) {
        if (icandelo_ixabiso < 0 || icandelo_ixabiso >= 2048) return -22;
        isixhobo_ixabiso.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        isixhobo_ixabiso.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int 결과 = 준비기다리기(false);
        if (결과 < 0) return 결과;
        isixhobo_ixabiso.입출력바이트쓰기(0x1f2, 1);
        isixhobo_ixabiso.입출력바이트쓰기(0x1f3, icandelo_ixabiso & 255);
        isixhobo_ixabiso.입출력바이트쓰기(0x1f4, (icandelo_ixabiso >>> 8) & 255);
        isixhobo_ixabiso.입출력바이트쓰기(0x1f5, 0);
        isixhobo_ixabiso.입출력바이트쓰기(0x1f7, Umyalelo); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Funda(int icandelo_ixabiso) {
        int 결과 = 요청(icandelo_ixabiso, 0x20);
        if (결과 < 0) return 결과;
        for (int indeksa = 0; indeksa < 256; indeksa++) {
            int ixabiso = isixhobo_ixabiso.입출력짧은수읽기(0x1f0);
            icandelo_iingcombolo[indeksa * 2] = ixabiso & 255; icandelo_iingcombolo[indeksa * 2 + 1] = ixabiso >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Bhala(int icandelo_ixabiso) {
        if (!사용가능 || icandelo_ixabiso < 1 || icandelo_ixabiso > 518) return -19;
        int 결과 = 요청(icandelo_ixabiso, 0x30);
        if (결과 < 0) return 결과;
        for (int indeksa = 0; indeksa < 256; indeksa++)
            isixhobo_ixabiso.입출력짧은수쓰기(0x1f0, icandelo_iingcombolo[indeksa * 2] | icandelo_iingcombolo[indeksa * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        isixhobo_ixabiso.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int ingcaciso_yegama_inani_elipheleleyo(int 위치) {
        return icandelo_iingcombolo[위치] | icandelo_iingcombolo[위치 + 1] << 8 | icandelo_iingcombolo[위치 + 2] << 16 | icandelo_iingcombolo[위치 + 3] << 24;
    }
    static void bhala_inani_elipheleleyo_ixabiso(int 위치, int ixabiso) {
        for (int indeksa = 0; indeksa < 4; indeksa++) icandelo_iingcombolo[위치 + indeksa] = (ixabiso >>> (indeksa * 8)) & 255;
    }
}
