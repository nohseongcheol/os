// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 sehemu_thamani. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Hifadhi_kifaa_muunganisho {
    static boolean teknolojia_ya_maelezo_Amilifu_9e72441a = false;
    static int[] sehemu_data = new int[512];
    static void 잠깐기다리기() {
        for (int kielezo = 0; kielezo < 4; kielezo++) kifaa_thamani.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int endesha = kifaa_thamani.밀리초();
        while (kifaa_thamani.밀리초() - endesha < 500) {
            int hali_thamani = kifaa_thamani.입출력바이트읽기(0x1f7);
            if (hali_thamani == 0 || hali_thamani == 255) return -19;
            if ((hali_thamani & 128) == 0) {
                if ((hali_thamani & 33) != 0) return -5;
                if (!자료필요 || (hali_thamani & 8) != 0) return 0;
            }
            kifaa_thamani.잠시양보();
        }
        return -110;
    }
    static int 요청(int sehemu_thamani, int amri) {
        if (sehemu_thamani < 0 || sehemu_thamani >= 2048) return -22;
        kifaa_thamani.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        kifaa_thamani.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int 결과 = 준비기다리기(false);
        if (결과 < 0) return 결과;
        kifaa_thamani.입출력바이트쓰기(0x1f2, 1);
        kifaa_thamani.입출력바이트쓰기(0x1f3, sehemu_thamani & 255);
        kifaa_thamani.입출력바이트쓰기(0x1f4, (sehemu_thamani >>> 8) & 255);
        kifaa_thamani.입출력바이트쓰기(0x1f5, 0);
        kifaa_thamani.입출력바이트쓰기(0x1f7, amri); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int 읽기(int sehemu_thamani) {
        int 결과 = 요청(sehemu_thamani, 0x20);
        if (결과 < 0) return 결과;
        for (int kielezo = 0; kielezo < 256; kielezo++) {
            int thamani = kifaa_thamani.입출력짧은수읽기(0x1f0);
            sehemu_data[kielezo * 2] = thamani & 255; sehemu_data[kielezo * 2 + 1] = thamani >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int andika(int sehemu_thamani) {
        if (!teknolojia_ya_maelezo_Amilifu_9e72441a || sehemu_thamani < 1 || sehemu_thamani > 518) return -19;
        int 결과 = 요청(sehemu_thamani, 0x30);
        if (결과 < 0) return 결과;
        for (int kielezo = 0; kielezo < 256; kielezo++)
            kifaa_thamani.입출력짧은수쓰기(0x1f0, sehemu_data[kielezo * 2] | sehemu_data[kielezo * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!teknolojia_ya_maelezo_Amilifu_9e72441a) return -19;
        kifaa_thamani.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int changanua_namba_kamili(int 위치) {
        return sehemu_data[위치] | sehemu_data[위치 + 1] << 8 | sehemu_data[위치 + 2] << 16 | sehemu_data[위치 + 3] << 24;
    }
    static void andika_namba_kamili_thamani(int 위치, int thamani) {
        for (int kielezo = 0; kielezo < 4; kielezo++) sehemu_data[위치 + kielezo] = (thamani >>> (kielezo * 8)) & 255;
    }
}
