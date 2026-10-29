// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int цифра_VALUE(String Текст) {
        if (Текст == null || Текст.length() == 0) return -1;
        int мерка = 0;
        for (int INDEX = 0; INDEX < Текст.length(); INDEX++) {
            int VALUE = Текст.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || мерка > 6553) return -1;
            мерка = мерка * 10 + VALUE;
            if (мерка > 65535) return -1;
        }
        return мерка;
    }
    static int адреса(String Текст) {
        if (Текст == null) return 0;
        int VALUE = 0, мерка = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Текст.length(); INDEX++) {
            int 문자 = INDEX == Текст.length() ? '.' : Текст.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                мерка = (мерка << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? мерка : 0;
    }
    public static int Изврши_2() {
        if (корисник.인수개수() != 3) { корисник.Запиши("Usage: run udp IP PORT TEXT\n"); return 2; }
        int адреса = адреса(корисник.Аргументи(0)), порта_VALUE = цифра_VALUE(корисник.Аргументи(1));
        String Содржина_VALUE = корисник.Аргументи(2);
        if (адреса == 0 || порта_VALUE < 1 || Содржина_VALUE.length() > 1024) { корисник.Запиши("Bad destination\n"); return 2; }
        int рачка_VALUE = корисник.отвори_Мрежа(0);
        if (рачка_VALUE < 0) { корисник.Запиши("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] податоци = new int[1024];
        for (int INDEX = 0; INDEX < Содржина_VALUE.length(); INDEX++) податоци[INDEX] = Содржина_VALUE.charAt(INDEX);
        if (корисник.испрати_податоци(рачка_VALUE, адреса, порта_VALUE, податоци, Содржина_VALUE.length()) < 0) {
            корисник.Запиши("UDP SEND FAILED\n"); корисник.затвори_Мрежа(рачка_VALUE); return 4;
        }
        корисник.Запиши("UDP SENT\n");
        int RECEIVED_должина = корисник.자료받기(рачка_VALUE, податоци, 1500);
        boolean 같음 = RECEIVED_должина == Содржина_VALUE.length() && корисник.보낸주소(рачка_VALUE) == адреса && корисник.보낸창구(рачка_VALUE) == порта_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_должина; INDEX++) if (податоци[INDEX] != Содржина_VALUE.charAt(INDEX)) 같음 = false;
        корисник.затвори_Мрежа(рачка_VALUE);
        if (RECEIVED_должина < 0) { корисник.Запиши("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        корисник.Запиши(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
