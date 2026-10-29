// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int 숫자(String Sengwalwa) {
        if (Sengwalwa == null || Sengwalwa.length() == 0) return -1;
        int 결과 = 0;
        for (int lokela = 0; lokela < Sengwalwa.length(); lokela++) {
            int boleng = Sengwalwa.charAt(lokela) - '0';
            if (boleng < 0 || boleng > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + boleng;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int atrese(String Sengwalwa) {
        if (Sengwalwa == null) return 0;
        int boleng = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int lokela = 0; lokela <= Sengwalwa.length(); lokela++) {
            int 문자 = lokela == Sengwalwa.length() ? '.' : Sengwalwa.charAt(lokela);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | boleng; 부분++; boleng = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                boleng = boleng * 10 + 문자 - '0';
                if (++자릿수 > 3 || boleng > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int Diriša() {
        if (mošomiši.인수개수() != 3) { mošomiši.Ngwala("Usage: run udp IP PORT TEXT\n"); return 2; }
        int atrese = atrese(mošomiši.인수(0)), phote_boleng = 숫자(mošomiši.인수(1));
        String Diteng_boleng = mošomiši.인수(2);
        if (atrese == 0 || phote_boleng < 1 || Diteng_boleng.length() > 1024) { mošomiši.Ngwala("Bad destination\n"); return 2; }
        int tshwaro_boleng = mošomiši.bula_Netweke(0);
        if (tshwaro_boleng < 0) { mošomiši.Ngwala("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] data = new int[1024];
        for (int lokela = 0; lokela < Diteng_boleng.length(); lokela++) data[lokela] = Diteng_boleng.charAt(lokela);
        if (mošomiši.Romela_data(tshwaro_boleng, atrese, phote_boleng, data, Diteng_boleng.length()) < 0) {
            mošomiši.Ngwala("UDP SEND FAILED\n"); mošomiši.tswalela_Netweke(tshwaro_boleng); return 4;
        }
        mošomiši.Ngwala("UDP SENT\n");
        int 받은길이 = mošomiši.자료받기(tshwaro_boleng, data, 1500);
        boolean 같음 = 받은길이 == Diteng_boleng.length() && mošomiši.보낸주소(tshwaro_boleng) == atrese && mošomiši.보낸창구(tshwaro_boleng) == phote_boleng;
        if (같음) for (int lokela = 0; lokela < 받은길이; lokela++) if (data[lokela] != Diteng_boleng.charAt(lokela)) 같음 = false;
        mošomiši.tswalela_Netweke(tshwaro_boleng);
        if (받은길이 < 0) { mošomiši.Ngwala("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        mošomiši.Ngwala(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
