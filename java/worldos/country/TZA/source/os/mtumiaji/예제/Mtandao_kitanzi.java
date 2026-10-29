// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 panga_ukubwa/홀수 urefu_thamani 데이터그램으로 halisi_data RTL8139 수신 kitanzi_thamani 순환을 시험한다. */
public final class Mtandao_kitanzi {
    public static int endesha() {
        if (mtumiaji.인수개수() != 1) { mtumiaji.andika("Usage: run stress PORT\n"); return 2; }
        String SMS = mtumiaji.인수(0);
        int kituo_thamani = 0;
        for (int kielezo = 0; kielezo < SMS.length(); kielezo++) {
            if (SMS.charAt(kielezo) < '0' || SMS.charAt(kielezo) > '9' || kituo_thamani > 6553) return 2;
            kituo_thamani = kituo_thamani * 10 + SMS.charAt(kielezo) - '0';
        }
        if (kituo_thamani < 1 || kituo_thamani > 65535) return 2;
        int kishiko_thamani = mtumiaji.unda_Mtandao(0);
        if (kishiko_thamani < 0) return 3;
        int[] data = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int urefu_thamani = 1024 - (회차 & 1);
            for (int kielezo = 0; kielezo < urefu_thamani; kielezo++) data[kielezo] = (kielezo + 회차) & 255;
            if (mtumiaji.tuma_data(kishiko_thamani, 0x0a000202, kituo_thamani, data, urefu_thamani) != urefu_thamani) return 4;
            if (mtumiaji.자료받기(kishiko_thamani, data, 300) != urefu_thamani) return 5;
            for (int kielezo = 0; kielezo < urefu_thamani; kielezo++) if (data[kielezo] != ((kielezo + 회차) & 255)) return 6;
        }
        mtumiaji.funga_Mtandao(kishiko_thamani);
        mtumiaji.andika("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
