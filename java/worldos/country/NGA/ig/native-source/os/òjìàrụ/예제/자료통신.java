// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int ọbula_valuu(String SMS) {
        if (SMS == null || SMS.length() == 0) return -1;
        int 결과 = 0;
        for (int indèks = 0; indèks < SMS.length(); indèks++) {
            int valuu = SMS.charAt(indèks) - '0';
            if (valuu < 0 || valuu > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + valuu;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int àdreèsì(String SMS) {
        if (SMS == null) return 0;
        int valuu = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int indèks = 0; indèks <= SMS.length(); indèks++) {
            int 문자 = indèks == SMS.length() ? '.' : SMS.charAt(indèks);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | valuu; 부분++; valuu = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                valuu = valuu * 10 + 문자 - '0';
                if (++자릿수 > 3 || valuu > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int Bido() {
        if (òjìàrụ.인수개수() != 3) { òjìàrụ.Chekwaa_ozi("Usage: run udp IP PORT TEXT\n"); return 2; }
        int àdreèsì = àdreèsì(òjìàrụ.인수(0)), pọọt_valuu = ọbula_valuu(òjìàrụ.인수(1));
        String ndịnà_valuu = òjìàrụ.인수(2);
        if (àdreèsì == 0 || pọọt_valuu < 1 || ndịnà_valuu.length() > 1024) { òjìàrụ.Chekwaa_ozi("Bad destination\n"); return 2; }
        int ebenjìaka_valuu = òjìàrụ.mepee_Netwọọkụ(0);
        if (ebenjìaka_valuu < 0) { òjìàrụ.Chekwaa_ozi("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] datà = new int[1024];
        for (int indèks = 0; indèks < ndịnà_valuu.length(); indèks++) datà[indèks] = ndịnà_valuu.charAt(indèks);
        if (òjìàrụ.zìga_datà(ebenjìaka_valuu, àdreèsì, pọọt_valuu, datà, ndịnà_valuu.length()) < 0) {
            òjìàrụ.Chekwaa_ozi("UDP SEND FAILED\n"); òjìàrụ.mmechi_Netwọọkụ(ebenjìaka_valuu); return 4;
        }
        òjìàrụ.Chekwaa_ozi("UDP SENT\n");
        int 받은길이 = òjìàrụ.자료받기(ebenjìaka_valuu, datà, 1500);
        boolean 같음 = 받은길이 == ndịnà_valuu.length() && òjìàrụ.보낸주소(ebenjìaka_valuu) == àdreèsì && òjìàrụ.보낸창구(ebenjìaka_valuu) == pọọt_valuu;
        if (같음) for (int indèks = 0; indèks < 받은길이; indèks++) if (datà[indèks] != ndịnà_valuu.charAt(indèks)) 같음 = false;
        òjìàrụ.mmechi_Netwọọkụ(ebenjìaka_valuu);
        if (받은길이 < 0) { òjìàrụ.Chekwaa_ozi("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        òjìàrụ.Chekwaa_ozi(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
