// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int अंक_मोल(String SMS) {
        if (SMS == null || SMS.length() == 0) return -1;
        int मेजप = 0;
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            int मोल = SMS.charAt(INDEX) - '0';
            if (मोल < 0 || मोल > 9 || मेजप > 6553) return -1;
            मेजप = मेजप * 10 + मोल;
            if (मेजप > 65535) return -1;
        }
        return मेजप;
    }
    static int नामो(String SMS) {
        if (SMS == null) return 0;
        int मोल = 0, मेजप = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= SMS.length(); INDEX++) {
            int 문자 = INDEX == SMS.length() ? '.' : SMS.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                मेजप = (मेजप << 8) | मोल; 부분++; मोल = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                मोल = मोल * 10 + 문자 - '0';
                if (++자릿수 > 3 || मोल > 255) return 0;
            }
        }
        return 부분 == 4 ? मेजप : 0;
    }
    public static int चलोवप() {
        if (उपेगकर्तो.인수개수() != 3) { उपेगकर्तो.बरोवचें("Usage: run udp IP PORT TEXT\n"); return 2; }
        int नामो = नामो(उपेगकर्तो.인수(0)), पोर्ट_मोल = अंक_मोल(उपेगकर्तो.인수(1));
        String अनुक्रमणिका_मोल = उपेगकर्तो.인수(2);
        if (नामो == 0 || पोर्ट_मोल < 1 || अनुक्रमणिका_मोल.length() > 1024) { उपेगकर्तो.बरोवचें("Bad destination\n"); return 2; }
        int हँडल_मोल = उपेगकर्तो.उगडचें_नॅटवर्क(0);
        if (हँडल_मोल < 0) { उपेगकर्तो.बरोवचें("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] डेटा = new int[1024];
        for (int INDEX = 0; INDEX < अनुक्रमणिका_मोल.length(); INDEX++) डेटा[INDEX] = अनुक्रमणिका_मोल.charAt(INDEX);
        if (उपेगकर्तो.धाडचें_डेटा(हँडल_मोल, नामो, पोर्ट_मोल, डेटा, अनुक्रमणिका_मोल.length()) < 0) {
            उपेगकर्तो.बरोवचें("UDP SEND FAILED\n"); उपेगकर्तो.शेवट_नॅटवर्क(हँडल_मोल); return 4;
        }
        उपेगकर्तो.बरोवचें("UDP SENT\n");
        int RECEIVED_लांबाय = उपेगकर्तो.자료받기(हँडल_मोल, डेटा, 1500);
        boolean 같음 = RECEIVED_लांबाय == अनुक्रमणिका_मोल.length() && उपेगकर्तो.보낸주소(हँडल_मोल) == नामो && उपेगकर्तो.보낸창구(हँडल_मोल) == पोर्ट_मोल;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_लांबाय; INDEX++) if (डेटा[INDEX] != अनुक्रमणिका_मोल.charAt(INDEX)) 같음 = false;
        उपेगकर्तो.शेवट_नॅटवर्क(हँडल_मोल);
        if (RECEIVED_लांबाय < 0) { उपेगकर्तो.बरोवचें("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        उपेगकर्तो.बरोवचें(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
