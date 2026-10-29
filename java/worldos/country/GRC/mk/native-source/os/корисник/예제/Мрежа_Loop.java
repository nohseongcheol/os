// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Големина/홀수 должина_VALUE 데이터그램으로 реален_податоци RTL8139 수신 Loop_VALUE 순환을 시험한다. */
public final class Мрежа_Loop {
    public static int Изврши_2() {
        if (корисник.인수개수() != 1) { корисник.Запиши("Usage: run stress PORT\n"); return 2; }
        String Текст = корисник.Аргументи(0);
        int порта_VALUE = 0;
        for (int INDEX = 0; INDEX < Текст.length(); INDEX++) {
            if (Текст.charAt(INDEX) < '0' || Текст.charAt(INDEX) > '9' || порта_VALUE > 6553) return 2;
            порта_VALUE = порта_VALUE * 10 + Текст.charAt(INDEX) - '0';
        }
        if (порта_VALUE < 1 || порта_VALUE > 65535) return 2;
        int рачка_VALUE = корисник.отвори_Мрежа(0);
        if (рачка_VALUE < 0) return 3;
        int[] податоци = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int должина_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < должина_VALUE; INDEX++) податоци[INDEX] = (INDEX + 회차) & 255;
            if (корисник.испрати_податоци(рачка_VALUE, 0x0a000202, порта_VALUE, податоци, должина_VALUE) != должина_VALUE) return 4;
            if (корисник.자료받기(рачка_VALUE, податоци, 300) != должина_VALUE) return 5;
            for (int INDEX = 0; INDEX < должина_VALUE; INDEX++) if (податоци[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        корисник.затвори_Мрежа(рачка_VALUE);
        корисник.Запиши("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
