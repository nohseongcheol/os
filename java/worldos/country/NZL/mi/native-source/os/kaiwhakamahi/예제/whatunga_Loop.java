// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 rahi/홀수 roa_uara 데이터그램으로 tūturu_raraunga RTL8139 수신 Loop_uara 순환을 시험한다. */
public final class whatunga_Loop {
    public static int whakahaere() {
        if (kaiwhakamahi.인수개수() != 1) { kaiwhakamahi.Tuhia("Usage: run stress PORT\n"); return 2; }
        String Ngā_kupu = kaiwhakamahi.인수(0);
        int kawe_uara = 0;
        for (int INDEX = 0; INDEX < Ngā_kupu.length(); INDEX++) {
            if (Ngā_kupu.charAt(INDEX) < '0' || Ngā_kupu.charAt(INDEX) > '9' || kawe_uara > 6553) return 2;
            kawe_uara = kawe_uara * 10 + Ngā_kupu.charAt(INDEX) - '0';
        }
        if (kawe_uara < 1 || kawe_uara > 65535) return 2;
        int raweke_uara = kaiwhakamahi.tiwhikete_whatunga(0);
        if (raweke_uara < 0) return 3;
        int[] raraunga = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int roa_uara = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < roa_uara; INDEX++) raraunga[INDEX] = (INDEX + 회차) & 255;
            if (kaiwhakamahi.tuku_raraunga(raweke_uara, 0x0a000202, kawe_uara, raraunga, roa_uara) != roa_uara) return 4;
            if (kaiwhakamahi.자료받기(raweke_uara, raraunga, 300) != roa_uara) return 5;
            for (int INDEX = 0; INDEX < roa_uara; INDEX++) if (raraunga[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        kaiwhakamahi.kati_whatunga(raweke_uara);
        kaiwhakamahi.Tuhia("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
