// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 секција_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Склад_уред_врска {
    static boolean информатичка_технологија_Активен_9e72441a = false;
    static int[] секција_податоци = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) уред_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Изврши_2 = уред_VALUE.밀리초();
        while (уред_VALUE.밀리초() - Изврши_2 < 500) {
            int статус_VALUE = уред_VALUE.입출력바이트읽기(0x1f7);
            if (статус_VALUE == 0 || статус_VALUE == 255) return -19;
            if ((статус_VALUE & 128) == 0) {
                if ((статус_VALUE & 33) != 0) return -5;
                if (!자료필요 || (статус_VALUE & 8) != 0) return 0;
            }
            уред_VALUE.잠시양보();
        }
        return -110;
    }
    static int Барање_на_HTTP(int секција_VALUE, int Команда) {
        if (секција_VALUE < 0 || секција_VALUE >= 2048) return -22;
        уред_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        уред_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int мерка = 준비기다리기(false);
        if (мерка < 0) return мерка;
        уред_VALUE.입출력바이트쓰기(0x1f2, 1);
        уред_VALUE.입출력바이트쓰기(0x1f3, секција_VALUE & 255);
        уред_VALUE.입출력바이트쓰기(0x1f4, (секција_VALUE >>> 8) & 255);
        уред_VALUE.입출력바이트쓰기(0x1f5, 0);
        уред_VALUE.입출력바이트쓰기(0x1f7, Команда); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Читај(int секција_VALUE) {
        int мерка = Барање_на_HTTP(секција_VALUE, 0x20);
        if (мерка < 0) return мерка;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = уред_VALUE.입출력짧은수읽기(0x1f0);
            секција_податоци[INDEX * 2] = VALUE & 255; секција_податоци[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Запиши(int секција_VALUE) {
        if (!информатичка_технологија_Активен_9e72441a || секција_VALUE < 1 || секција_VALUE > 518) return -19;
        int мерка = Барање_на_HTTP(секција_VALUE, 0x30);
        if (мерка < 0) return мерка;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            уред_VALUE.입출력짧은수쓰기(0x1f0, секција_податоци[INDEX * 2] | секција_податоци[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!информатичка_технологија_Активен_9e72441a) return -19;
        уред_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int разложи_цел_број(int Позиција) {
        return секција_податоци[Позиција] | секција_податоци[Позиција + 1] << 8 | секција_податоци[Позиција + 2] << 16 | секција_податоци[Позиција + 3] << 24;
    }
    static void запиши_цел_број_VALUE(int Позиција, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) секција_податоци[Позиција + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
