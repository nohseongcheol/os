// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int Ziffer_VALUE(String SMS) {
        if (SMS == null || SMS.length() == 0) return -1;
        int Mooss = 0;
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            int VALUE = SMS.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || Mooss > 6553) return -1;
            Mooss = Mooss * 10 + VALUE;
            if (Mooss > 65535) return -1;
        }
        return Mooss;
    }
    static int Adress(String SMS) {
        if (SMS == null) return 0;
        int VALUE = 0, Mooss = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= SMS.length(); INDEX++) {
            int 문자 = INDEX == SMS.length() ? '.' : SMS.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                Mooss = (Mooss << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? Mooss : 0;
    }
    public static int Laf() {
        if (Benotzer.인수개수() != 3) { Benotzer.schreiwen("Usage: run udp IP PORT TEXT\n"); return 2; }
        int Adress = Adress(Benotzer.인수(0)), Port_VALUE = Ziffer_VALUE(Benotzer.인수(1));
        String Inhalt_VALUE = Benotzer.인수(2);
        if (Adress == 0 || Port_VALUE < 1 || Inhalt_VALUE.length() > 1024) { Benotzer.schreiwen("Bad destination\n"); return 2; }
        int Handle_VALUE = Benotzer.ariichten_Reseau(0);
        if (Handle_VALUE < 0) { Benotzer.schreiwen("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] Daten = new int[1024];
        for (int INDEX = 0; INDEX < Inhalt_VALUE.length(); INDEX++) Daten[INDEX] = Inhalt_VALUE.charAt(INDEX);
        if (Benotzer.mailen_Daten(Handle_VALUE, Adress, Port_VALUE, Daten, Inhalt_VALUE.length()) < 0) {
            Benotzer.schreiwen("UDP SEND FAILED\n"); Benotzer.Clôture_Reseau(Handle_VALUE); return 4;
        }
        Benotzer.schreiwen("UDP SENT\n");
        int RECEIVED_Längt = Benotzer.자료받기(Handle_VALUE, Daten, 1500);
        boolean 같음 = RECEIVED_Längt == Inhalt_VALUE.length() && Benotzer.보낸주소(Handle_VALUE) == Adress && Benotzer.보낸창구(Handle_VALUE) == Port_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_Längt; INDEX++) if (Daten[INDEX] != Inhalt_VALUE.charAt(INDEX)) 같음 = false;
        Benotzer.Clôture_Reseau(Handle_VALUE);
        if (RECEIVED_Längt < 0) { Benotzer.schreiwen("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        Benotzer.schreiwen(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
