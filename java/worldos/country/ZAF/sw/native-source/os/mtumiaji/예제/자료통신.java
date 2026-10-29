// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int dijiti_thamani(String SMS) {
        if (SMS == null || SMS.length() == 0) return -1;
        int 결과 = 0;
        for (int kielezo = 0; kielezo < SMS.length(); kielezo++) {
            int thamani = SMS.charAt(kielezo) - '0';
            if (thamani < 0 || thamani > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + thamani;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int anwani(String SMS) {
        if (SMS == null) return 0;
        int thamani = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int kielezo = 0; kielezo <= SMS.length(); kielezo++) {
            int 문자 = kielezo == SMS.length() ? '.' : SMS.charAt(kielezo);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | thamani; 부분++; thamani = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                thamani = thamani * 10 + 문자 - '0';
                if (++자릿수 > 3 || thamani > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int endesha() {
        if (mtumiaji.인수개수() != 3) { mtumiaji.andika("Usage: run udp IP PORT TEXT\n"); return 2; }
        int anwani = anwani(mtumiaji.인수(0)), kituo_thamani = dijiti_thamani(mtumiaji.인수(1));
        String maudhui_thamani = mtumiaji.인수(2);
        if (anwani == 0 || kituo_thamani < 1 || maudhui_thamani.length() > 1024) { mtumiaji.andika("Bad destination\n"); return 2; }
        int kishiko_thamani = mtumiaji.unda_Mtandao(0);
        if (kishiko_thamani < 0) { mtumiaji.andika("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] data = new int[1024];
        for (int kielezo = 0; kielezo < maudhui_thamani.length(); kielezo++) data[kielezo] = maudhui_thamani.charAt(kielezo);
        if (mtumiaji.tuma_data(kishiko_thamani, anwani, kituo_thamani, data, maudhui_thamani.length()) < 0) {
            mtumiaji.andika("UDP SEND FAILED\n"); mtumiaji.funga_Mtandao(kishiko_thamani); return 4;
        }
        mtumiaji.andika("UDP SENT\n");
        int 받은길이 = mtumiaji.자료받기(kishiko_thamani, data, 1500);
        boolean 같음 = 받은길이 == maudhui_thamani.length() && mtumiaji.보낸주소(kishiko_thamani) == anwani && mtumiaji.보낸창구(kishiko_thamani) == kituo_thamani;
        if (같음) for (int kielezo = 0; kielezo < 받은길이; kielezo++) if (data[kielezo] != maudhui_thamani.charAt(kielezo)) 같음 = false;
        mtumiaji.funga_Mtandao(kishiko_thamani);
        if (받은길이 < 0) { mtumiaji.andika("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        mtumiaji.andika(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
