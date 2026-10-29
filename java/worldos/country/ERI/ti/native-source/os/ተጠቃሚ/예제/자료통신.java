// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int ኣሃዝ_ዋጋ(String ጽሑፍ) {
        if (ጽሑፍ == null || ጽሑፍ.length() == 0) return -1;
        int 결과 = 0;
        for (int መሐበሪ = 0; መሐበሪ < ጽሑፍ.length(); መሐበሪ++) {
            int ዋጋ = ጽሑፍ.charAt(መሐበሪ) - '0';
            if (ዋጋ < 0 || ዋጋ > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + ዋጋ;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int ኣድራሻ(String ጽሑፍ) {
        if (ጽሑፍ == null) return 0;
        int ዋጋ = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int መሐበሪ = 0; መሐበሪ <= ጽሑፍ.length(); መሐበሪ++) {
            int 문자 = መሐበሪ == ጽሑፍ.length() ? '.' : ጽሑፍ.charAt(መሐበሪ);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | ዋጋ; 부분++; ዋጋ = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                ዋጋ = ዋጋ * 10 + 문자 - '0';
                if (++자릿수 > 3 || ዋጋ > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int ኣኺድ() {
        if (ተጠቃሚ.인수개수() != 3) { ተጠቃሚ.ጸሓፍ("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ኣድራሻ = ኣድራሻ(ተጠቃሚ.인수(0)), ወደብ_ዋጋ = ኣሃዝ_ዋጋ(ተጠቃሚ.인수(1));
        String ትሕዝቶ_ዋጋ = ተጠቃሚ.인수(2);
        if (ኣድራሻ == 0 || ወደብ_ዋጋ < 1 || ትሕዝቶ_ዋጋ.length() > 1024) { ተጠቃሚ.ጸሓፍ("Bad destination\n"); return 2; }
        int መትሓዚ_ዋጋ = ተጠቃሚ.ክፈት_ማሕበራዊ_ኔትወርክ(0);
        if (መትሓዚ_ዋጋ < 0) { ተጠቃሚ.ጸሓፍ("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] ሓበሬታ = new int[1024];
        for (int መሐበሪ = 0; መሐበሪ < ትሕዝቶ_ዋጋ.length(); መሐበሪ++) ሓበሬታ[መሐበሪ] = ትሕዝቶ_ዋጋ.charAt(መሐበሪ);
        if (ተጠቃሚ.ለኣኽ_ሓበሬታ(መትሓዚ_ዋጋ, ኣድራሻ, ወደብ_ዋጋ, ሓበሬታ, ትሕዝቶ_ዋጋ.length()) < 0) {
            ተጠቃሚ.ጸሓፍ("UDP SEND FAILED\n"); ተጠቃሚ.ዕጸው_ማሕበራዊ_ኔትወርክ(መትሓዚ_ዋጋ); return 4;
        }
        ተጠቃሚ.ጸሓፍ("UDP SENT\n");
        int 받은길이 = ተጠቃሚ.자료받기(መትሓዚ_ዋጋ, ሓበሬታ, 1500);
        boolean 같음 = 받은길이 == ትሕዝቶ_ዋጋ.length() && ተጠቃሚ.보낸주소(መትሓዚ_ዋጋ) == ኣድራሻ && ተጠቃሚ.보낸창구(መትሓዚ_ዋጋ) == ወደብ_ዋጋ;
        if (같음) for (int መሐበሪ = 0; መሐበሪ < 받은길이; መሐበሪ++) if (ሓበሬታ[መሐበሪ] != ትሕዝቶ_ዋጋ.charAt(መሐበሪ)) 같음 = false;
        ተጠቃሚ.ዕጸው_ማሕበራዊ_ኔትወርክ(መትሓዚ_ዋጋ);
        if (받은길이 < 0) { ተጠቃሚ.ጸሓፍ("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        ተጠቃሚ.ጸሓፍ(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
