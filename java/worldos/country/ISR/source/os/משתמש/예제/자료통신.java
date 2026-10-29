// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int ספרה_ערך(String טקסט) {
        if (טקסט == null || טקסט.length() == 0) return -1;
        int תוצאה = 0;
        for (int מדד = 0; מדד < טקסט.length(); מדד++) {
            int ערך = טקסט.charAt(מדד) - '0';
            if (ערך < 0 || ערך > 9 || תוצאה > 6553) return -1;
            תוצאה = תוצאה * 10 + ערך;
            if (תוצאה > 65535) return -1;
        }
        return תוצאה;
    }
    static int למען(String טקסט) {
        if (טקסט == null) return 0;
        int ערך = 0, תוצאה = 0, 부분 = 0, 자릿수 = 0;
        for (int מדד = 0; מדד <= טקסט.length(); מדד++) {
            int 문자 = מדד == טקסט.length() ? '.' : טקסט.charAt(מדד);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                תוצאה = (תוצאה << 8) | ערך; 부분++; ערך = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                ערך = ערך * 10 + 문자 - '0';
                if (++자릿수 > 3 || ערך > 255) return 0;
            }
        }
        return 부분 == 4 ? תוצאה : 0;
    }
    public static int הפעלה() {
        if (משתמש.인수개수() != 3) { משתמש.כתוב("Usage: run udp IP PORT TEXT\n"); return 2; }
        int למען = למען(משתמש.ארגומנטים(0)), הסב_ערך = ספרה_ערך(משתמש.ארגומנטים(1));
        String תוכן_ערך = משתמש.ארגומנטים(2);
        if (למען == 0 || הסב_ערך < 1 || תוכן_ערך.length() > 1024) { משתמש.כתוב("Bad destination\n"); return 2; }
        int נקודת_אחיזה_ערך = משתמש.פתח_רשת(0);
        if (נקודת_אחיזה_ערך < 0) { משתמש.כתוב("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] נתונים = new int[1024];
        for (int מדד = 0; מדד < תוכן_ערך.length(); מדד++) נתונים[מדד] = תוכן_ערך.charAt(מדד);
        if (משתמש.שלח_נתונים(נקודת_אחיזה_ערך, למען, הסב_ערך, נתונים, תוכן_ערך.length()) < 0) {
            משתמש.כתוב("UDP SEND FAILED\n"); משתמש.סגור_רשת(נקודת_אחיזה_ערך); return 4;
        }
        משתמש.כתוב("UDP SENT\n");
        int 받은길이 = משתמש.לקבל_נתונים(נקודת_אחיזה_ערך, נתונים, 1500);
        boolean 같음 = 받은길이 == תוכן_ערך.length() && משתמש.보낸주소(נקודת_אחיזה_ערך) == למען && משתמש.보낸창구(נקודת_אחיזה_ערך) == הסב_ערך;
        if (같음) for (int מדד = 0; מדד < 받은길이; מדד++) if (נתונים[מדד] != תוכן_ערך.charAt(מדד)) 같음 = false;
        משתמש.סגור_רשת(נקודת_אחיזה_ערך);
        if (받은길이 < 0) { משתמש.כתוב("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        משתמש.כתוב(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
