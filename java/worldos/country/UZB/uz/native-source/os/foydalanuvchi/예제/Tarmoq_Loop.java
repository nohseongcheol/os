// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Hajmi/홀수 uzunlik_VALUE 데이터그램으로 real_ma_lumotlar RTL8139 수신 Loop_VALUE 순환을 시험한다. */
public final class Tarmoq_Loop {
    public static int Bajarish() {
        if (foydalanuvchi.인수개수() != 1) { foydalanuvchi.Yozish("Usage: run stress PORT\n"); return 2; }
        String Matn = foydalanuvchi.인수(0);
        int port_VALUE = 0;
        for (int INDEX = 0; INDEX < Matn.length(); INDEX++) {
            if (Matn.charAt(INDEX) < '0' || Matn.charAt(INDEX) > '9' || port_VALUE > 6553) return 2;
            port_VALUE = port_VALUE * 10 + Matn.charAt(INDEX) - '0';
        }
        if (port_VALUE < 1 || port_VALUE > 65535) return 2;
        int deskriptor_VALUE = foydalanuvchi.ochmoq_Tarmoq(0);
        if (deskriptor_VALUE < 0) return 3;
        int[] ma_lumotlar = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int uzunlik_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < uzunlik_VALUE; INDEX++) ma_lumotlar[INDEX] = (INDEX + 회차) & 255;
            if (foydalanuvchi.yuborish_ma_lumotlar(deskriptor_VALUE, 0x0a000202, port_VALUE, ma_lumotlar, uzunlik_VALUE) != uzunlik_VALUE) return 4;
            if (foydalanuvchi.자료받기(deskriptor_VALUE, ma_lumotlar, 300) != uzunlik_VALUE) return 5;
            for (int INDEX = 0; INDEX < uzunlik_VALUE; INDEX++) if (ma_lumotlar[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        foydalanuvchi.yopmoq_Tarmoq(deskriptor_VALUE);
        foydalanuvchi.Yozish("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
