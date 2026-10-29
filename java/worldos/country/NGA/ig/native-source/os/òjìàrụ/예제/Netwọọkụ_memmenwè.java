// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Ụhara/홀수 ogologo_valuu 데이터그램으로 ǹdịnezie_datà RTL8139 수신 memmenwè_valuu 순환을 시험한다. */
public final class Netwọọkụ_memmenwè {
    public static int Bido() {
        if (òjìàrụ.인수개수() != 1) { òjìàrụ.Chekwaa_ozi("Usage: run stress PORT\n"); return 2; }
        String SMS = òjìàrụ.인수(0);
        int pọọt_valuu = 0;
        for (int indèks = 0; indèks < SMS.length(); indèks++) {
            if (SMS.charAt(indèks) < '0' || SMS.charAt(indèks) > '9' || pọọt_valuu > 6553) return 2;
            pọọt_valuu = pọọt_valuu * 10 + SMS.charAt(indèks) - '0';
        }
        if (pọọt_valuu < 1 || pọọt_valuu > 65535) return 2;
        int ebenjìaka_valuu = òjìàrụ.mepee_Netwọọkụ(0);
        if (ebenjìaka_valuu < 0) return 3;
        int[] datà = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int ogologo_valuu = 1024 - (회차 & 1);
            for (int indèks = 0; indèks < ogologo_valuu; indèks++) datà[indèks] = (indèks + 회차) & 255;
            if (òjìàrụ.zìga_datà(ebenjìaka_valuu, 0x0a000202, pọọt_valuu, datà, ogologo_valuu) != ogologo_valuu) return 4;
            if (òjìàrụ.자료받기(ebenjìaka_valuu, datà, 300) != ogologo_valuu) return 5;
            for (int indèks = 0; indèks < ogologo_valuu; indèks++) if (datà[indèks] != ((indèks + 회차) & 255)) return 6;
        }
        òjìàrụ.mmechi_Netwọọkụ(ebenjìaka_valuu);
        òjìàrụ.Chekwaa_ozi("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
