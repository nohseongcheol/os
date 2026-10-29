// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 abala_iye. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Ibi_ìpamọ́_ohun_èlò_Ìsomọ́ {
    static boolean 사용가능 = false;
    static int[] abala_détà = new int[512];
    static void 잠깐기다리기() {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 4; wá_atọ̀ka_àkóónú++) ohun_èlò_iye.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Rọ́ọ̀nù = ohun_èlò_iye.밀리초();
        while (ohun_èlò_iye.밀리초() - Rọ́ọ̀nù < 500) {
            int ipò_iye = ohun_èlò_iye.입출력바이트읽기(0x1f7);
            if (ipò_iye == 0 || ipò_iye == 255) return -19;
            if ((ipò_iye & 128) == 0) {
                if ((ipò_iye & 33) != 0) return -5;
                if (!자료필요 || (ipò_iye & 8) != 0) return 0;
            }
            ohun_èlò_iye.잠시양보();
        }
        return -110;
    }
    static int 요청(int abala_iye, int Àṣẹ) {
        if (abala_iye < 0 || abala_iye >= 2048) return -22;
        ohun_èlò_iye.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        ohun_èlò_iye.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int 결과 = 준비기다리기(false);
        if (결과 < 0) return 결과;
        ohun_èlò_iye.입출력바이트쓰기(0x1f2, 1);
        ohun_èlò_iye.입출력바이트쓰기(0x1f3, abala_iye & 255);
        ohun_èlò_iye.입출력바이트쓰기(0x1f4, (abala_iye >>> 8) & 255);
        ohun_èlò_iye.입출력바이트쓰기(0x1f5, 0);
        ohun_èlò_iye.입출력바이트쓰기(0x1f7, Àṣẹ); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Kàá(int abala_iye) {
        int 결과 = 요청(abala_iye, 0x20);
        if (결과 < 0) return 결과;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 256; wá_atọ̀ka_àkóónú++) {
            int iye = ohun_èlò_iye.입출력짧은수읽기(0x1f0);
            abala_détà[wá_atọ̀ka_àkóónú * 2] = iye & 255; abala_détà[wá_atọ̀ka_àkóónú * 2 + 1] = iye >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Kọ(int abala_iye) {
        if (!사용가능 || abala_iye < 1 || abala_iye > 518) return -19;
        int 결과 = 요청(abala_iye, 0x30);
        if (결과 < 0) return 결과;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 256; wá_atọ̀ka_àkóónú++)
            ohun_èlò_iye.입출력짧은수쓰기(0x1f0, abala_détà[wá_atọ̀ka_àkóónú * 2] | abala_détà[wá_atọ̀ka_àkóónú * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        ohun_èlò_iye.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(int 위치) {
        return abala_détà[위치] | abala_détà[위치 + 1] << 8 | abala_détà[위치 + 2] << 16 | abala_détà[위치 + 3] << 24;
    }
    static void kọ_nọ́ńbà_odindi_iye(int 위치, int iye) {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 4; wá_atọ̀ka_àkóónú++) abala_détà[위치 + wá_atọ̀ka_àkóónú] = (iye >>> (wá_atọ̀ka_àkóónú * 8)) & 255;
    }
}
