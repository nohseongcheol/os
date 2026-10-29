// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** tegelik_andmed Java lepingu_väärtus 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void kinnitama(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int kontrollsumma(int[] VALUE, int Käivita_2, int 길이, int lähteolek) {
        int SUM_VALUE = lähteolek;
        for (int INDEX = 0; INDEX < 길이; INDEX++) SUM_VALUE += VALUE[Käivita_2 + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Ettevalmistamine(int 길이) {
        võrk_Virn.CLEAN_Joonis();
        kinnitama(võrk_Virn.Ava(5000) == 3);
        int[] raam_INDEX = võrk_Virn.입력틀;
        Arrays.fill(raam_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) raam_INDEX[INDEX] = võrk_draiver.seade_ADDRESS[INDEX];
        võrk_Virn.넣기16(raam_INDEX, 12, 0x0800);
        raam_INDEX[14] = 0x45; raam_INDEX[22] = 64; raam_INDEX[23] = 17;
        võrk_Virn.넣기16(raam_INDEX, 16, 28 + 길이);
        võrk_Virn.넣기32(raam_INDEX, 26, 0x0a000202); võrk_Virn.넣기32(raam_INDEX, 30, võrk_Virn.내주소);
        võrk_Virn.넣기16(raam_INDEX, 34, 4321); võrk_Virn.넣기16(raam_INDEX, 36, 5000); võrk_Virn.넣기16(raam_INDEX, 38, 길이 + 8);
        for (int INDEX = 0; INDEX < 길이; INDEX++) raam_INDEX[42 + INDEX] = INDEX & 255;
        hulk_kontrollsumma(길이);
    }
    static void hulk_kontrollsumma(int 길이) {
        int[] raam_INDEX = võrk_Virn.입력틀;
        võrk_Virn.넣기16(raam_INDEX, 24, 0); võrk_Virn.넣기16(raam_INDEX, 40, 0);
        võrk_Virn.넣기16(raam_INDEX, 24, kontrollsumma(raam_INDEX, 14, 20, 0));
        int lähteolek = võrk_Virn.가상머리합(võrk_Virn.täisarv_32(raam_INDEX, 26), võrk_Virn.내주소, 길이 + 8);
        int SUM_VALUE = kontrollsumma(raam_INDEX, 34, 길이 + 8, lähteolek);
        võrk_Virn.넣기16(raam_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void keelduma_VALUE(int 길이) { võrk_Virn.Joonis_raam(길이); kinnitama(võrk_Virn.받은길이[0] == -1); }
    public static void main(String[] Argumendid) {
        for (int 길이 : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Ettevalmistamine(길이); võrk_Virn.Joonis_raam(길이 + 42);
            kinnitama(võrk_Virn.받은길이[0] == 길이);
            kinnitama(võrk_Virn.RECEIVED_ADDRESS[0] == 0x0a000202 && võrk_Virn.RECEIVED_pordinumber[0] == 4321);
            for (int INDEX = 0; INDEX < 길이; INDEX++) kinnitama(võrk_Virn.RECEIVED_andmed[INDEX] == (INDEX & 255));
        }
        for (int 길이 = 0; 길이 < 42; 길이++) { Ettevalmistamine(0); keelduma_VALUE(길이); }
        Ettevalmistamine(1025); keelduma_VALUE(1067);
        Ettevalmistamine(2); võrk_Virn.입력틀[24] ^= 1; keelduma_VALUE(44);
        Ettevalmistamine(2); võrk_Virn.입력틀[42] ^= 1; keelduma_VALUE(44);
        Ettevalmistamine(2); võrk_Virn.넣기16(võrk_Virn.입력틀, 38, 7); keelduma_VALUE(44);
        Ettevalmistamine(2); võrk_Virn.넣기16(võrk_Virn.입력틀, 38, 65535); keelduma_VALUE(44);
        Ettevalmistamine(2); võrk_Virn.입력틀[14] = 0x4f; keelduma_VALUE(44);
        Ettevalmistamine(2); võrk_Virn.입력틀[14] = 0x44; keelduma_VALUE(44);
        Ettevalmistamine(2); võrk_Virn.입력틀[20] = 0x20; hulk_kontrollsumma(2); keelduma_VALUE(44);
        Ettevalmistamine(2); võrk_Virn.입력틀[21] = 1; hulk_kontrollsumma(2); keelduma_VALUE(44);
        Ettevalmistamine(2); võrk_Virn.입력틀[33] = 99; hulk_kontrollsumma(2); keelduma_VALUE(44);
        Ettevalmistamine(2); võrk_Virn.입력틀[0] ^= 1; keelduma_VALUE(44);
        Ettevalmistamine(2); võrk_Virn.입력틀[23] = 6; hulk_kontrollsumma(2); keelduma_VALUE(44);
        Ettevalmistamine(2); võrk_Virn.넣기16(võrk_Virn.입력틀, 40, 0); võrk_Virn.Joonis_raam(44); kinnitama(võrk_Virn.받은길이[0] == 2);
        int[] TULEMUS = new int[4];
        kinnitama(võrk_Virn.saama(3, TULEMUS, 1, 0) == -90);
        kinnitama(võrk_Virn.saama(3, TULEMUS, 4, 0) == -11);
        Ettevalmistamine(2); võrk_Virn.Joonis_raam(44); int hülgama_VALUE = võrk_Virn.폐기수;
        võrk_Virn.Joonis_raam(44); kinnitama(võrk_Virn.폐기수 == hülgama_VALUE + 1);
        võrk_Virn.CLEAN_Joonis(); kinnitama(võrk_Virn.Ava(5000) == 3);
        kinnitama(võrk_Virn.Ava(5000) == -98); kinnitama(võrk_Virn.Ava(0) == 4);
        kinnitama(võrk_Virn.Ava(0) == 5); kinnitama(võrk_Virn.Ava(0) == 6); kinnitama(võrk_Virn.Ava(0) == -24);
        kinnitama(võrk_Virn.Suletud(4) == 0); kinnitama(võrk_Virn.Suletud(4) == -9);
        võrk_Virn.찾은주소 = võrk_Virn.lüüs_VALUE;
        kinnitama(võrk_Virn.saatma(3, võrk_Virn.lüüs_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = võrk_draiver.hiljutised_VALUE;
        kinnitama(kontrollsumma(보냄, 14, 20, 0) == 0);
        kinnitama(kontrollsumma(보냄, 34, 11, võrk_Virn.가상머리합(võrk_Virn.내주소, võrk_Virn.lüüs_VALUE, 11)) == 0);
        kinnitama(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
