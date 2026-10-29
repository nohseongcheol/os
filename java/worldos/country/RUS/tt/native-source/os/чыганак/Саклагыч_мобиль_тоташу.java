// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 өлеш_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Саклагыч_мобиль_тоташу {
    static boolean 사용가능 = false;
    static int[] өлеш_мәгълүмат = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) мобиль_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int эшләтү = мобиль_VALUE.밀리초();
        while (мобиль_VALUE.밀리초() - эшләтү < 500) {
            int халәт_VALUE = мобиль_VALUE.입출력바이트읽기(0x1f7);
            if (халәт_VALUE == 0 || халәт_VALUE == 255) return -19;
            if ((халәт_VALUE & 128) == 0) {
                if ((халәт_VALUE & 33) != 0) return -5;
                if (!자료필요 || (халәт_VALUE & 8) != 0) return 0;
            }
            мобиль_VALUE.잠시양보();
        }
        return -110;
    }
    static int 요청(int өлеш_VALUE, int команда) {
        if (өлеш_VALUE < 0 || өлеш_VALUE >= 2048) return -22;
        мобиль_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        мобиль_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int үлчәм = 준비기다리기(false);
        if (үлчәм < 0) return үлчәм;
        мобиль_VALUE.입출력바이트쓰기(0x1f2, 1);
        мобиль_VALUE.입출력바이트쓰기(0x1f3, өлеш_VALUE & 255);
        мобиль_VALUE.입출력바이트쓰기(0x1f4, (өлеш_VALUE >>> 8) & 255);
        мобиль_VALUE.입출력바이트쓰기(0x1f5, 0);
        мобиль_VALUE.입출력바이트쓰기(0x1f7, команда); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int 읽기(int өлеш_VALUE) {
        int үлчәм = 요청(өлеш_VALUE, 0x20);
        if (үлчәм < 0) return үлчәм;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = мобиль_VALUE.입출력짧은수읽기(0x1f0);
            өлеш_мәгълүмат[INDEX * 2] = VALUE & 255; өлеш_мәгълүмат[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int язу(int өлеш_VALUE) {
        if (!사용가능 || өлеш_VALUE < 1 || өлеш_VALUE > 518) return -19;
        int үлчәм = 요청(өлеш_VALUE, 0x30);
        if (үлчәм < 0) return үлчәм;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            мобиль_VALUE.입출력짧은수쓰기(0x1f0, өлеш_мәгълүмат[INDEX * 2] | өлеш_мәгълүмат[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        мобиль_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int бүлү_бөтен_сан(int урнаштыру) {
        return өлеш_мәгълүмат[урнаштыру] | өлеш_мәгълүмат[урнаштыру + 1] << 8 | өлеш_мәгълүмат[урнаштыру + 2] << 16 | өлеш_мәгълүмат[урнаштыру + 3] << 24;
    }
    static void язу_бөтен_сан_VALUE(int урнаштыру, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) өлеш_мәгълүмат[урнаштыру + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
