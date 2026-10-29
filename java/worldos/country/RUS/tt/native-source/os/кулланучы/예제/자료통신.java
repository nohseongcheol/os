// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int сан_VALUE(String Mäten) {
        if (Mäten == null || Mäten.length() == 0) return -1;
        int үлчәм = 0;
        for (int INDEX = 0; INDEX < Mäten.length(); INDEX++) {
            int VALUE = Mäten.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || үлчәм > 6553) return -1;
            үлчәм = үлчәм * 10 + VALUE;
            if (үлчәм > 65535) return -1;
        }
        return үлчәм;
    }
    static int адрес(String Mäten) {
        if (Mäten == null) return 0;
        int VALUE = 0, үлчәм = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Mäten.length(); INDEX++) {
            int 문자 = INDEX == Mäten.length() ? '.' : Mäten.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                үлчәм = (үлчәм << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? үлчәм : 0;
    }
    public static int эшләтү() {
        if (кулланучы.인수개수() != 3) { кулланучы.язу("Usage: run udp IP PORT TEXT\n"); return 2; }
        int адрес = адрес(кулланучы.인수(0)), порт_VALUE = сан_VALUE(кулланучы.인수(1));
        String Эчтәлек_VALUE = кулланучы.인수(2);
        if (адрес == 0 || порт_VALUE < 1 || Эчтәлек_VALUE.length() > 1024) { кулланучы.язу("Bad destination\n"); return 2; }
        int дескриптор_VALUE = кулланучы.ачу_Челтәр(0);
        if (дескриптор_VALUE < 0) { кулланучы.язу("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] мәгълүмат = new int[1024];
        for (int INDEX = 0; INDEX < Эчтәлек_VALUE.length(); INDEX++) мәгълүмат[INDEX] = Эчтәлек_VALUE.charAt(INDEX);
        if (кулланучы.җибәрү_мәгълүмат(дескриптор_VALUE, адрес, порт_VALUE, мәгълүмат, Эчтәлек_VALUE.length()) < 0) {
            кулланучы.язу("UDP SEND FAILED\n"); кулланучы.чик_Челтәр(дескриптор_VALUE); return 4;
        }
        кулланучы.язу("UDP SENT\n");
        int RECEIVED_озынлык = кулланучы.자료받기(дескриптор_VALUE, мәгълүмат, 1500);
        boolean 같음 = RECEIVED_озынлык == Эчтәлек_VALUE.length() && кулланучы.보낸주소(дескриптор_VALUE) == адрес && кулланучы.보낸창구(дескриптор_VALUE) == порт_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_озынлык; INDEX++) if (мәгълүмат[INDEX] != Эчтәлек_VALUE.charAt(INDEX)) 같음 = false;
        кулланучы.чик_Челтәр(дескриптор_VALUE);
        if (RECEIVED_озынлык < 0) { кулланучы.язу("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        кулланучы.язу(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
