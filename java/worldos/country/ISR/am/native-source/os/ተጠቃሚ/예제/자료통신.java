// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int 숫자(String ጽሁፍ) {
        if (ጽሁፍ == null || ጽሁፍ.length() == 0) return -1;
        int ልኬት = 0;
        for (int መረጃ_ጠቆመ = 0; መረጃ_ጠቆመ < ጽሁፍ.length(); መረጃ_ጠቆመ++) {
            int እሴት = ጽሁፍ.charAt(መረጃ_ጠቆመ) - '0';
            if (እሴት < 0 || እሴት > 9 || ልኬት > 6553) return -1;
            ልኬት = ልኬት * 10 + እሴት;
            if (ልኬት > 65535) return -1;
        }
        return ልኬት;
    }
    static int አድራሻ(String ጽሁፍ) {
        if (ጽሁፍ == null) return 0;
        int እሴት = 0, ልኬት = 0, 부분 = 0, 자릿수 = 0;
        for (int መረጃ_ጠቆመ = 0; መረጃ_ጠቆመ <= ጽሁፍ.length(); መረጃ_ጠቆመ++) {
            int 문자 = መረጃ_ጠቆመ == ጽሁፍ.length() ? '.' : ጽሁፍ.charAt(መረጃ_ጠቆመ);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                ልኬት = (ልኬት << 8) | እሴት; 부분++; እሴት = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                እሴት = እሴት * 10 + 문자 - '0';
                if (++자릿수 > 3 || እሴት > 255) return 0;
            }
        }
        return 부분 == 4 ? ልኬት : 0;
    }
    public static int ማስኬጃ() {
        if (ተጠቃሚ.인수개수() != 3) { ተጠቃሚ.መጻፊያ("Usage: run udp IP PORT TEXT\n"); return 2; }
        int አድራሻ = አድራሻ(ተጠቃሚ.인수(0)), ወደብ_እሴት = 숫자(ተጠቃሚ.인수(1));
        String ይዘት_እሴት = ተጠቃሚ.인수(2);
        if (አድራሻ == 0 || ወደብ_እሴት < 1 || ይዘት_እሴት.length() > 1024) { ተጠቃሚ.መጻፊያ("Bad destination\n"); return 2; }
        int እጀታ_እሴት = ተጠቃሚ.ክፈት_መረብ(0);
        if (እጀታ_እሴት < 0) { ተጠቃሚ.መጻፊያ("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] ውሂብ = new int[1024];
        for (int መረጃ_ጠቆመ = 0; መረጃ_ጠቆመ < ይዘት_እሴት.length(); መረጃ_ጠቆመ++) ውሂብ[መረጃ_ጠቆመ] = ይዘት_እሴት.charAt(መረጃ_ጠቆመ);
        if (ተጠቃሚ.ላክ_ውሂብ(እጀታ_እሴት, አድራሻ, ወደብ_እሴት, ውሂብ, ይዘት_እሴት.length()) < 0) {
            ተጠቃሚ.መጻፊያ("UDP SEND FAILED\n"); ተጠቃሚ.ዝጋ_መረብ(እጀታ_እሴት); return 4;
        }
        ተጠቃሚ.መጻፊያ("UDP SENT\n");
        int 받은길이 = ተጠቃሚ.자료받기(እጀታ_እሴት, ውሂብ, 1500);
        boolean 같음 = 받은길이 == ይዘት_እሴት.length() && ተጠቃሚ.보낸주소(እጀታ_እሴት) == አድራሻ && ተጠቃሚ.보낸창구(እጀታ_እሴት) == ወደብ_እሴት;
        if (같음) for (int መረጃ_ጠቆመ = 0; መረጃ_ጠቆመ < 받은길이; መረጃ_ጠቆመ++) if (ውሂብ[መረጃ_ጠቆመ] != ይዘት_እሴት.charAt(መረጃ_ጠቆመ)) 같음 = false;
        ተጠቃሚ.ዝጋ_መረብ(እጀታ_እሴት);
        if (받은길이 < 0) { ተጠቃሚ.መጻፊያ("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        ተጠቃሚ.መጻፊያ(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
