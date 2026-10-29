// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 seksiyon_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Storage_device_koneksyon {
    static boolean information_technology_Aktibo_9e72441a = false;
    static int[] seksiyon_data = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) device_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int run = device_VALUE.밀리초();
        while (device_VALUE.밀리초() - run < 500) {
            int katayuan_VALUE = device_VALUE.입출력바이트읽기(0x1f7);
            if (katayuan_VALUE == 0 || katayuan_VALUE == 255) return -19;
            if ((katayuan_VALUE & 128) == 0) {
                if ((katayuan_VALUE & 33) != 0) return -5;
                if (!자료필요 || (katayuan_VALUE & 8) != 0) return 0;
            }
            device_VALUE.잠시양보();
        }
        return -110;
    }
    static int 요청(int seksiyon_VALUE, int utos) {
        if (seksiyon_VALUE < 0 || seksiyon_VALUE >= 2048) return -22;
        device_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        device_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int sukat = 준비기다리기(false);
        if (sukat < 0) return sukat;
        device_VALUE.입출력바이트쓰기(0x1f2, 1);
        device_VALUE.입출력바이트쓰기(0x1f3, seksiyon_VALUE & 255);
        device_VALUE.입출력바이트쓰기(0x1f4, (seksiyon_VALUE >>> 8) & 255);
        device_VALUE.입출력바이트쓰기(0x1f5, 0);
        device_VALUE.입출력바이트쓰기(0x1f7, utos); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int 읽기(int seksiyon_VALUE) {
        int sukat = 요청(seksiyon_VALUE, 0x20);
        if (sukat < 0) return sukat;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = device_VALUE.입출력짧은수읽기(0x1f0);
            seksiyon_data[INDEX * 2] = VALUE & 255; seksiyon_data[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int sumulat(int seksiyon_VALUE) {
        if (!information_technology_Aktibo_9e72441a || seksiyon_VALUE < 1 || seksiyon_VALUE > 518) return -19;
        int sukat = 요청(seksiyon_VALUE, 0x30);
        if (sukat < 0) return sukat;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            device_VALUE.입출력짧은수쓰기(0x1f0, seksiyon_data[INDEX * 2] | seksiyon_data[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!information_technology_Aktibo_9e72441a) return -19;
        device_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int mag_parse_integer_buong_numero(int posisyon) {
        return seksiyon_data[posisyon] | seksiyon_data[posisyon + 1] << 8 | seksiyon_data[posisyon + 2] << 16 | seksiyon_data[posisyon + 3] << 24;
    }
    static void sumulat_integer_buong_numero_VALUE(int posisyon, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) seksiyon_data[posisyon + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
