// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Izmērs/홀수 길이 데이터그램으로 faktisks_dati RTL8139 saņemt_VALUE Loop_VALUE 순환을 시험한다. */
public final class tīkls_Loop {
    public static int Palaist() {
        if (lietotājs.인수개수() != 1) { lietotājs.Rakstīt("Usage: run stress PORT\n"); return 2; }
        String Teksts = lietotājs.Parametri(0);
        int ports_VALUE = 0;
        for (int INDEX = 0; INDEX < Teksts.length(); INDEX++) {
            if (Teksts.charAt(INDEX) < '0' || Teksts.charAt(INDEX) > '9' || ports_VALUE > 6553) return 2;
            ports_VALUE = ports_VALUE * 10 + Teksts.charAt(INDEX) - '0';
        }
        if (ports_VALUE < 1 || ports_VALUE > 65535) return 2;
        int turis_VALUE = lietotājs.atvērt_tīkls(0);
        if (turis_VALUE < 0) return 3;
        int[] dati = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int 길이 = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < 길이; INDEX++) dati[INDEX] = (INDEX + 회차) & 255;
            if (lietotājs.sūtīt_dati(turis_VALUE, 0x0a000202, ports_VALUE, dati, 길이) != 길이) return 4;
            if (lietotājs.saņemt_dati(turis_VALUE, dati, 300) != 길이) return 5;
            for (int INDEX = 0; INDEX < 길이; INDEX++) if (dati[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        lietotājs.Aizvērt_tīkls(turis_VALUE);
        lietotājs.Rakstīt("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
