// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int rəqəm_VALUE(String Mətn) {
        if (Mətn == null || Mətn.length() == 0) return -1;
        int ölçü = 0;
        for (int INDEX = 0; INDEX < Mətn.length(); INDEX++) {
            int VALUE = Mətn.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || ölçü > 6553) return -1;
            ölçü = ölçü * 10 + VALUE;
            if (ölçü > 65535) return -1;
        }
        return ölçü;
    }
    static int ünvan(String Mətn) {
        if (Mətn == null) return 0;
        int VALUE = 0, ölçü = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Mətn.length(); INDEX++) {
            int 문자 = INDEX == Mətn.length() ? '.' : Mətn.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                ölçü = (ölçü << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? ölçü : 0;
    }
    public static int İcra_Et() {
        if (istifadəçi.인수개수() != 3) { istifadəçi.Yazma("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ünvan = ünvan(istifadəçi.인수(0)), port_VALUE = rəqəm_VALUE(istifadəçi.인수(1));
        String Məzmun_VALUE = istifadəçi.인수(2);
        if (ünvan == 0 || port_VALUE < 1 || Məzmun_VALUE.length() > 1024) { istifadəçi.Yazma("Bad destination\n"); return 2; }
        int tutacaq_VALUE = istifadəçi.açmaq_Şəbəkə(0);
        if (tutacaq_VALUE < 0) { istifadəçi.Yazma("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] verilənlər = new int[1024];
        for (int INDEX = 0; INDEX < Məzmun_VALUE.length(); INDEX++) verilənlər[INDEX] = Məzmun_VALUE.charAt(INDEX);
        if (istifadəçi.göndərmək_verilənlər(tutacaq_VALUE, ünvan, port_VALUE, verilənlər, Məzmun_VALUE.length()) < 0) {
            istifadəçi.Yazma("UDP SEND FAILED\n"); istifadəçi.bağlamaq_Şəbəkə(tutacaq_VALUE); return 4;
        }
        istifadəçi.Yazma("UDP SENT\n");
        int RECEIVED_uzunluq = istifadəçi.자료받기(tutacaq_VALUE, verilənlər, 1500);
        boolean 같음 = RECEIVED_uzunluq == Məzmun_VALUE.length() && istifadəçi.보낸주소(tutacaq_VALUE) == ünvan && istifadəçi.보낸창구(tutacaq_VALUE) == port_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_uzunluq; INDEX++) if (verilənlər[INDEX] != Məzmun_VALUE.charAt(INDEX)) 같음 = false;
        istifadəçi.bağlamaq_Şəbəkə(tutacaq_VALUE);
        if (RECEIVED_uzunluq < 0) { istifadəçi.Yazma("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        istifadəçi.Yazma(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
