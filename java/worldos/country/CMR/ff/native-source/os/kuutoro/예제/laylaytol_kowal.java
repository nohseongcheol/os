// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 waylude_etannde/홀수 njuuteendi_njaru 데이터그램으로 laatii_keɓe RTL8139 수신 kowal_njaru 순환을 시험한다. */
public final class laylaytol_kowal {
    public static int huutoraade() {
        if (kuutoro.인수개수() != 1) { kuutoro.winndude("Usage: run stress PORT\n"); return 2; }
        String binndi = kuutoro.인수(0);
        int poor_njaru = 0;
        for (int joopirdu = 0; joopirdu < binndi.length(); joopirdu++) {
            if (binndi.charAt(joopirdu) < '0' || binndi.charAt(joopirdu) > '9' || poor_njaru > 6553) return 2;
            poor_njaru = poor_njaru * 10 + binndi.charAt(joopirdu) - '0';
        }
        if (poor_njaru < 1 || poor_njaru > 65535) return 2;
        int jaggoode_njaru = kuutoro.udditde_laylaytol(0);
        if (jaggoode_njaru < 0) return 3;
        int[] keɓe = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int njuuteendi_njaru = 1024 - (회차 & 1);
            for (int joopirdu = 0; joopirdu < njuuteendi_njaru; joopirdu++) keɓe[joopirdu] = (joopirdu + 회차) & 255;
            if (kuutoro.neldude_keɓe(jaggoode_njaru, 0x0a000202, poor_njaru, keɓe, njuuteendi_njaru) != njuuteendi_njaru) return 4;
            if (kuutoro.자료받기(jaggoode_njaru, keɓe, 300) != njuuteendi_njaru) return 5;
            for (int joopirdu = 0; joopirdu < njuuteendi_njaru; joopirdu++) if (keɓe[joopirdu] != ((joopirdu + 회차) & 255)) return 6;
        }
        kuutoro.uddude_laylaytol(jaggoode_njaru);
        kuutoro.winndude("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
