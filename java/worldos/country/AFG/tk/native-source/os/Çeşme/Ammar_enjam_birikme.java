// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 bölüm_baha_366e0bfa. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Ammar_enjam_birikme {
    static boolean 사용가능 = false;
    static int[] bölüm_maglumat = new int[512];
    static void 잠깐기다리기() {
        for (int indeks = 0; indeks < 4; indeks++) enjam_baha.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Bitir = enjam_baha.밀리초();
        while (enjam_baha.밀리초() - Bitir < 500) {
            int ýagdaý_baha = enjam_baha.입출력바이트읽기(0x1f7);
            if (ýagdaý_baha == 0 || ýagdaý_baha == 255) return -19;
            if ((ýagdaý_baha & 128) == 0) {
                if ((ýagdaý_baha & 33) != 0) return -5;
                if (!자료필요 || (ýagdaý_baha & 8) != 0) return 0;
            }
            enjam_baha.잠시양보();
        }
        return -110;
    }
    static int 요청(int bölüm_baha_366e0bfa, int buýruk) {
        if (bölüm_baha_366e0bfa < 0 || bölüm_baha_366e0bfa >= 2048) return -22;
        enjam_baha.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        enjam_baha.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int 결과 = 준비기다리기(false);
        if (결과 < 0) return 결과;
        enjam_baha.입출력바이트쓰기(0x1f2, 1);
        enjam_baha.입출력바이트쓰기(0x1f3, bölüm_baha_366e0bfa & 255);
        enjam_baha.입출력바이트쓰기(0x1f4, (bölüm_baha_366e0bfa >>> 8) & 255);
        enjam_baha.입출력바이트쓰기(0x1f5, 0);
        enjam_baha.입출력바이트쓰기(0x1f7, buýruk); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Oka(int bölüm_baha_366e0bfa) {
        int 결과 = 요청(bölüm_baha_366e0bfa, 0x20);
        if (결과 < 0) return 결과;
        for (int indeks = 0; indeks < 256; indeks++) {
            int baha = enjam_baha.입출력짧은수읽기(0x1f0);
            bölüm_maglumat[indeks * 2] = baha & 255; bölüm_maglumat[indeks * 2 + 1] = baha >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Ýaz(int bölüm_baha_366e0bfa) {
        if (!사용가능 || bölüm_baha_366e0bfa < 1 || bölüm_baha_366e0bfa > 518) return -19;
        int 결과 = 요청(bölüm_baha_366e0bfa, 0x30);
        if (결과 < 0) return 결과;
        for (int indeks = 0; indeks < 256; indeks++)
            enjam_baha.입출력짧은수쓰기(0x1f0, bölüm_maglumat[indeks * 2] | bölüm_maglumat[indeks * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        enjam_baha.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int seljer_bitin(int 위치) {
        return bölüm_maglumat[위치] | bölüm_maglumat[위치 + 1] << 8 | bölüm_maglumat[위치 + 2] << 16 | bölüm_maglumat[위치 + 3] << 24;
    }
    static void ýaz_bitin_baha(int 위치, int baha) {
        for (int indeks = 0; indeks < 4; indeks++) bölüm_maglumat[위치 + indeks] = (baha >>> (indeks * 8)) & 255;
    }
}
