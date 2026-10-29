// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** faktisk_data Java sak_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void stadfeste(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int kontrollsum(int[] VALUE, int Køyr_2, int lengd_VALUE, int 초기) {
        int SUM_VALUE = 초기;
        for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) SUM_VALUE += VALUE[Køyr_2 + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Klargjer(int lengd_VALUE) {
        Nettverk_Stabel.CLEAN_Prosess();
        stadfeste(Nettverk_Stabel.Opna(5000) == 3);
        int[] rute_INDEX = Nettverk_Stabel.입력틀;
        Arrays.fill(rute_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) rute_INDEX[INDEX] = Nettverk_drivar.mobil_ADDRESS[INDEX];
        Nettverk_Stabel.넣기16(rute_INDEX, 12, 0x0800);
        rute_INDEX[14] = 0x45; rute_INDEX[22] = 64; rute_INDEX[23] = 17;
        Nettverk_Stabel.넣기16(rute_INDEX, 16, 28 + lengd_VALUE);
        Nettverk_Stabel.넣기32(rute_INDEX, 26, 0x0a000202); Nettverk_Stabel.넣기32(rute_INDEX, 30, Nettverk_Stabel.내주소);
        Nettverk_Stabel.넣기16(rute_INDEX, 34, 4321); Nettverk_Stabel.넣기16(rute_INDEX, 36, 5000); Nettverk_Stabel.넣기16(rute_INDEX, 38, lengd_VALUE + 8);
        for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) rute_INDEX[42 + INDEX] = INDEX & 255;
        sett_kontrollsum(lengd_VALUE);
    }
    static void sett_kontrollsum(int lengd_VALUE) {
        int[] rute_INDEX = Nettverk_Stabel.입력틀;
        Nettverk_Stabel.넣기16(rute_INDEX, 24, 0); Nettverk_Stabel.넣기16(rute_INDEX, 40, 0);
        Nettverk_Stabel.넣기16(rute_INDEX, 24, kontrollsum(rute_INDEX, 14, 20, 0));
        int 초기 = Nettverk_Stabel.가상머리합(Nettverk_Stabel.heiltal_32(rute_INDEX, 26), Nettverk_Stabel.내주소, lengd_VALUE + 8);
        int SUM_VALUE = kontrollsum(rute_INDEX, 34, lengd_VALUE + 8, 초기);
        Nettverk_Stabel.넣기16(rute_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void avvise_VALUE(int lengd_VALUE) { Nettverk_Stabel.Prosess_rute(lengd_VALUE); stadfeste(Nettverk_Stabel.RECEIVED_lengd[0] == -1); }
    public static void main(String[] Argument) {
        for (int lengd_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Klargjer(lengd_VALUE); Nettverk_Stabel.Prosess_rute(lengd_VALUE + 42);
            stadfeste(Nettverk_Stabel.RECEIVED_lengd[0] == lengd_VALUE);
            stadfeste(Nettverk_Stabel.RECEIVED_ADDRESS[0] == 0x0a000202 && Nettverk_Stabel.RECEIVED_portnummer[0] == 4321);
            for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) stadfeste(Nettverk_Stabel.RECEIVED_data[INDEX] == (INDEX & 255));
        }
        for (int lengd_VALUE = 0; lengd_VALUE < 42; lengd_VALUE++) { Klargjer(0); avvise_VALUE(lengd_VALUE); }
        Klargjer(1025); avvise_VALUE(1067);
        Klargjer(2); Nettverk_Stabel.입력틀[24] ^= 1; avvise_VALUE(44);
        Klargjer(2); Nettverk_Stabel.입력틀[42] ^= 1; avvise_VALUE(44);
        Klargjer(2); Nettverk_Stabel.넣기16(Nettverk_Stabel.입력틀, 38, 7); avvise_VALUE(44);
        Klargjer(2); Nettverk_Stabel.넣기16(Nettverk_Stabel.입력틀, 38, 65535); avvise_VALUE(44);
        Klargjer(2); Nettverk_Stabel.입력틀[14] = 0x4f; avvise_VALUE(44);
        Klargjer(2); Nettverk_Stabel.입력틀[14] = 0x44; avvise_VALUE(44);
        Klargjer(2); Nettverk_Stabel.입력틀[20] = 0x20; sett_kontrollsum(2); avvise_VALUE(44);
        Klargjer(2); Nettverk_Stabel.입력틀[21] = 1; sett_kontrollsum(2); avvise_VALUE(44);
        Klargjer(2); Nettverk_Stabel.입력틀[33] = 99; sett_kontrollsum(2); avvise_VALUE(44);
        Klargjer(2); Nettverk_Stabel.입력틀[0] ^= 1; avvise_VALUE(44);
        Klargjer(2); Nettverk_Stabel.입력틀[23] = 6; sett_kontrollsum(2); avvise_VALUE(44);
        Klargjer(2); Nettverk_Stabel.넣기16(Nettverk_Stabel.입력틀, 40, 0); Nettverk_Stabel.Prosess_rute(44); stadfeste(Nettverk_Stabel.RECEIVED_lengd[0] == 2);
        int[] forretningsmål = new int[4];
        stadfeste(Nettverk_Stabel.받기(3, forretningsmål, 1, 0) == -90);
        stadfeste(Nettverk_Stabel.받기(3, forretningsmål, 4, 0) == -11);
        Klargjer(2); Nettverk_Stabel.Prosess_rute(44); int forkaste_VALUE = Nettverk_Stabel.폐기수;
        Nettverk_Stabel.Prosess_rute(44); stadfeste(Nettverk_Stabel.폐기수 == forkaste_VALUE + 1);
        Nettverk_Stabel.CLEAN_Prosess(); stadfeste(Nettverk_Stabel.Opna(5000) == 3);
        stadfeste(Nettverk_Stabel.Opna(5000) == -98); stadfeste(Nettverk_Stabel.Opna(0) == 4);
        stadfeste(Nettverk_Stabel.Opna(0) == 5); stadfeste(Nettverk_Stabel.Opna(0) == 6); stadfeste(Nettverk_Stabel.Opna(0) == -24);
        stadfeste(Nettverk_Stabel.Lukk(4) == 0); stadfeste(Nettverk_Stabel.Lukk(4) == -9);
        Nettverk_Stabel.찾은주소 = Nettverk_Stabel.gateway_VALUE;
        stadfeste(Nettverk_Stabel.sende(3, Nettverk_Stabel.gateway_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Nettverk_drivar.nyaste_VALUE;
        stadfeste(kontrollsum(보냄, 14, 20, 0) == 0);
        stadfeste(kontrollsum(보냄, 34, 11, Nettverk_Stabel.가상머리합(Nettverk_Stabel.내주소, Nettverk_Stabel.gateway_VALUE, 11)) == 0);
        stadfeste(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
