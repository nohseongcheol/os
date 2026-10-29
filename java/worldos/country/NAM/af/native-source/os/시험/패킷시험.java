// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** werklik_data Java saak_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void verifieer(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] VALUE, int Loop, int lengte_VALUE, int 초기) {
        int SUM_VALUE = 초기;
        for (int INDEX = 0; INDEX < lengte_VALUE; INDEX++) SUM_VALUE += VALUE[Loop + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Maak_gereed(int lengte_VALUE) {
        Netwerk_Stapel.CLEAN_Proses();
        verifieer(Netwerk_Stapel.skep(5000) == 3);
        int[] raam_INDEX = Netwerk_Stapel.입력틀;
        Arrays.fill(raam_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) raam_INDEX[INDEX] = Netwerk_drywer.mobiel_adres[INDEX];
        Netwerk_Stapel.넣기16(raam_INDEX, 12, 0x0800);
        raam_INDEX[14] = 0x45; raam_INDEX[22] = 64; raam_INDEX[23] = 17;
        Netwerk_Stapel.넣기16(raam_INDEX, 16, 28 + lengte_VALUE);
        Netwerk_Stapel.넣기32(raam_INDEX, 26, 0x0a000202); Netwerk_Stapel.넣기32(raam_INDEX, 30, Netwerk_Stapel.내주소);
        Netwerk_Stapel.넣기16(raam_INDEX, 34, 4321); Netwerk_Stapel.넣기16(raam_INDEX, 36, 5000); Netwerk_Stapel.넣기16(raam_INDEX, 38, lengte_VALUE + 8);
        for (int INDEX = 0; INDEX < lengte_VALUE; INDEX++) raam_INDEX[42 + INDEX] = INDEX & 255;
        검사합넣기(lengte_VALUE);
    }
    static void 검사합넣기(int lengte_VALUE) {
        int[] raam_INDEX = Netwerk_Stapel.입력틀;
        Netwerk_Stapel.넣기16(raam_INDEX, 24, 0); Netwerk_Stapel.넣기16(raam_INDEX, 40, 0);
        Netwerk_Stapel.넣기16(raam_INDEX, 24, 검사합(raam_INDEX, 14, 20, 0));
        int 초기 = Netwerk_Stapel.가상머리합(Netwerk_Stapel.heelgetal_32(raam_INDEX, 26), Netwerk_Stapel.내주소, lengte_VALUE + 8);
        int SUM_VALUE = 검사합(raam_INDEX, 34, lengte_VALUE + 8, 초기);
        Netwerk_Stapel.넣기16(raam_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void 거부(int lengte_VALUE) { Netwerk_Stapel.Proses_raam(lengte_VALUE); verifieer(Netwerk_Stapel.RECEIVED_lengte[0] == -1); }
    public static void main(String[] 인수) {
        for (int lengte_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Maak_gereed(lengte_VALUE); Netwerk_Stapel.Proses_raam(lengte_VALUE + 42);
            verifieer(Netwerk_Stapel.RECEIVED_lengte[0] == lengte_VALUE);
            verifieer(Netwerk_Stapel.RECEIVED_adres[0] == 0x0a000202 && Netwerk_Stapel.받은접속번호[0] == 4321);
            for (int INDEX = 0; INDEX < lengte_VALUE; INDEX++) verifieer(Netwerk_Stapel.RECEIVED_data[INDEX] == (INDEX & 255));
        }
        for (int lengte_VALUE = 0; lengte_VALUE < 42; lengte_VALUE++) { Maak_gereed(0); 거부(lengte_VALUE); }
        Maak_gereed(1025); 거부(1067);
        Maak_gereed(2); Netwerk_Stapel.입력틀[24] ^= 1; 거부(44);
        Maak_gereed(2); Netwerk_Stapel.입력틀[42] ^= 1; 거부(44);
        Maak_gereed(2); Netwerk_Stapel.넣기16(Netwerk_Stapel.입력틀, 38, 7); 거부(44);
        Maak_gereed(2); Netwerk_Stapel.넣기16(Netwerk_Stapel.입력틀, 38, 65535); 거부(44);
        Maak_gereed(2); Netwerk_Stapel.입력틀[14] = 0x4f; 거부(44);
        Maak_gereed(2); Netwerk_Stapel.입력틀[14] = 0x44; 거부(44);
        Maak_gereed(2); Netwerk_Stapel.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        Maak_gereed(2); Netwerk_Stapel.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        Maak_gereed(2); Netwerk_Stapel.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        Maak_gereed(2); Netwerk_Stapel.입력틀[0] ^= 1; 거부(44);
        Maak_gereed(2); Netwerk_Stapel.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        Maak_gereed(2); Netwerk_Stapel.넣기16(Netwerk_Stapel.입력틀, 40, 0); Netwerk_Stapel.Proses_raam(44); verifieer(Netwerk_Stapel.RECEIVED_lengte[0] == 2);
        int[] maatreël = new int[4];
        verifieer(Netwerk_Stapel.받기(3, maatreël, 1, 0) == -90);
        verifieer(Netwerk_Stapel.받기(3, maatreël, 4, 0) == -11);
        Maak_gereed(2); Netwerk_Stapel.Proses_raam(44); int wegdoen_met_VALUE = Netwerk_Stapel.폐기수;
        Netwerk_Stapel.Proses_raam(44); verifieer(Netwerk_Stapel.폐기수 == wegdoen_met_VALUE + 1);
        Netwerk_Stapel.CLEAN_Proses(); verifieer(Netwerk_Stapel.skep(5000) == 3);
        verifieer(Netwerk_Stapel.skep(5000) == -98); verifieer(Netwerk_Stapel.skep(0) == 4);
        verifieer(Netwerk_Stapel.skep(0) == 5); verifieer(Netwerk_Stapel.skep(0) == 6); verifieer(Netwerk_Stapel.skep(0) == -24);
        verifieer(Netwerk_Stapel.Sluit(4) == 0); verifieer(Netwerk_Stapel.Sluit(4) == -9);
        Netwerk_Stapel.찾은주소 = Netwerk_Stapel.deurgang_VALUE;
        verifieer(Netwerk_Stapel.e_pos(3, Netwerk_Stapel.deurgang_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Netwerk_drywer.onlangse_VALUE;
        verifieer(검사합(보냄, 14, 20, 0) == 0);
        verifieer(검사합(보냄, 34, 11, Netwerk_Stapel.가상머리합(Netwerk_Stapel.내주소, Netwerk_Stapel.deurgang_VALUE, 11)) == 0);
        verifieer(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
