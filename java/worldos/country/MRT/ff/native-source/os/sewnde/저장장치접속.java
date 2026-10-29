// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 taƴre_njaru. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class 저장장치접속 {
    static boolean 사용가능 = false;
    static int[] taƴre_keɓe = new int[512];
    static void 잠깐기다리기() {
        for (int joopirdu = 0; joopirdu < 4; joopirdu++) kaɓirgal_njaru.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int huutoraade = kaɓirgal_njaru.밀리초();
        while (kaɓirgal_njaru.밀리초() - huutoraade < 500) {
            int ngonka_njaru = kaɓirgal_njaru.입출력바이트읽기(0x1f7);
            if (ngonka_njaru == 0 || ngonka_njaru == 255) return -19;
            if ((ngonka_njaru & 128) == 0) {
                if ((ngonka_njaru & 33) != 0) return -5;
                if (!자료필요 || (ngonka_njaru & 8) != 0) return 0;
            }
            kaɓirgal_njaru.잠시양보();
        }
        return -110;
    }
    static int 요청(int taƴre_njaru, int ginol) {
        if (taƴre_njaru < 0 || taƴre_njaru >= 2048) return -22;
        kaɓirgal_njaru.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        kaɓirgal_njaru.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int 결과 = 준비기다리기(false);
        if (결과 < 0) return 결과;
        kaɓirgal_njaru.입출력바이트쓰기(0x1f2, 1);
        kaɓirgal_njaru.입출력바이트쓰기(0x1f3, taƴre_njaru & 255);
        kaɓirgal_njaru.입출력바이트쓰기(0x1f4, (taƴre_njaru >>> 8) & 255);
        kaɓirgal_njaru.입출력바이트쓰기(0x1f5, 0);
        kaɓirgal_njaru.입출력바이트쓰기(0x1f7, ginol); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int 읽기(int taƴre_njaru) {
        int 결과 = 요청(taƴre_njaru, 0x20);
        if (결과 < 0) return 결과;
        for (int joopirdu = 0; joopirdu < 256; joopirdu++) {
            int njaru = kaɓirgal_njaru.입출력짧은수읽기(0x1f0);
            taƴre_keɓe[joopirdu * 2] = njaru & 255; taƴre_keɓe[joopirdu * 2 + 1] = njaru >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int winndude(int taƴre_njaru) {
        if (!사용가능 || taƴre_njaru < 1 || taƴre_njaru > 518) return -19;
        int 결과 = 요청(taƴre_njaru, 0x30);
        if (결과 < 0) return 결과;
        for (int joopirdu = 0; joopirdu < 256; joopirdu++)
            kaɓirgal_njaru.입출력짧은수쓰기(0x1f0, taƴre_keɓe[joopirdu * 2] | taƴre_keɓe[joopirdu * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        kaɓirgal_njaru.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int 정수읽기(int 위치) {
        return taƴre_keɓe[위치] | taƴre_keɓe[위치 + 1] << 8 | taƴre_keɓe[위치 + 2] << 16 | taƴre_keɓe[위치 + 3] << 24;
    }
    static void 정수쓰기(int 위치, int njaru) {
        for (int joopirdu = 0; joopirdu < 4; joopirdu++) taƴre_keɓe[위치 + joopirdu] = (njaru >>> (joopirdu * 8)) & 255;
    }
}
