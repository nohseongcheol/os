// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** raun_gögn Java samningsvirði 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void sannprófa(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int prófsumma(int[] VALUE, int Keyra_2, int lengd_VALUE, int 초기) {
        int SUM_VALUE = 초기;
        for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) SUM_VALUE += VALUE[Keyra_2 + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Undirbúa(int lengd_VALUE) {
        Net_bunki.CLEAN_Ferli();
        sannprófa(Net_bunki.Opna(5000) == 3);
        int[] ramma_INDEX = Net_bunki.입력틀;
        Arrays.fill(ramma_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) ramma_INDEX[INDEX] = Net_rekill.tæki_slóð[INDEX];
        Net_bunki.넣기16(ramma_INDEX, 12, 0x0800);
        ramma_INDEX[14] = 0x45; ramma_INDEX[22] = 64; ramma_INDEX[23] = 17;
        Net_bunki.넣기16(ramma_INDEX, 16, 28 + lengd_VALUE);
        Net_bunki.넣기32(ramma_INDEX, 26, 0x0a000202); Net_bunki.넣기32(ramma_INDEX, 30, Net_bunki.내주소);
        Net_bunki.넣기16(ramma_INDEX, 34, 4321); Net_bunki.넣기16(ramma_INDEX, 36, 5000); Net_bunki.넣기16(ramma_INDEX, 38, lengd_VALUE + 8);
        for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) ramma_INDEX[42 + INDEX] = INDEX & 255;
        sett_prófsumma(lengd_VALUE);
    }
    static void sett_prófsumma(int lengd_VALUE) {
        int[] ramma_INDEX = Net_bunki.입력틀;
        Net_bunki.넣기16(ramma_INDEX, 24, 0); Net_bunki.넣기16(ramma_INDEX, 40, 0);
        Net_bunki.넣기16(ramma_INDEX, 24, prófsumma(ramma_INDEX, 14, 20, 0));
        int 초기 = Net_bunki.가상머리합(Net_bunki.heiltala_32(ramma_INDEX, 26), Net_bunki.내주소, lengd_VALUE + 8);
        int SUM_VALUE = prófsumma(ramma_INDEX, 34, lengd_VALUE + 8, 초기);
        Net_bunki.넣기16(ramma_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void hafna_VALUE(int lengd_VALUE) { Net_bunki.Ferli_ramma(lengd_VALUE); sannprófa(Net_bunki.RECEIVED_lengd[0] == -1); }
    public static void main(String[] Viðföng) {
        for (int lengd_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Undirbúa(lengd_VALUE); Net_bunki.Ferli_ramma(lengd_VALUE + 42);
            sannprófa(Net_bunki.RECEIVED_lengd[0] == lengd_VALUE);
            sannprófa(Net_bunki.RECEIVED_slóð[0] == 0x0a000202 && Net_bunki.RECEIVED_tengisnúmer[0] == 4321);
            for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) sannprófa(Net_bunki.RECEIVED_gögn[INDEX] == (INDEX & 255));
        }
        for (int lengd_VALUE = 0; lengd_VALUE < 42; lengd_VALUE++) { Undirbúa(0); hafna_VALUE(lengd_VALUE); }
        Undirbúa(1025); hafna_VALUE(1067);
        Undirbúa(2); Net_bunki.입력틀[24] ^= 1; hafna_VALUE(44);
        Undirbúa(2); Net_bunki.입력틀[42] ^= 1; hafna_VALUE(44);
        Undirbúa(2); Net_bunki.넣기16(Net_bunki.입력틀, 38, 7); hafna_VALUE(44);
        Undirbúa(2); Net_bunki.넣기16(Net_bunki.입력틀, 38, 65535); hafna_VALUE(44);
        Undirbúa(2); Net_bunki.입력틀[14] = 0x4f; hafna_VALUE(44);
        Undirbúa(2); Net_bunki.입력틀[14] = 0x44; hafna_VALUE(44);
        Undirbúa(2); Net_bunki.입력틀[20] = 0x20; sett_prófsumma(2); hafna_VALUE(44);
        Undirbúa(2); Net_bunki.입력틀[21] = 1; sett_prófsumma(2); hafna_VALUE(44);
        Undirbúa(2); Net_bunki.입력틀[33] = 99; sett_prófsumma(2); hafna_VALUE(44);
        Undirbúa(2); Net_bunki.입력틀[0] ^= 1; hafna_VALUE(44);
        Undirbúa(2); Net_bunki.입력틀[23] = 6; sett_prófsumma(2); hafna_VALUE(44);
        Undirbúa(2); Net_bunki.넣기16(Net_bunki.입력틀, 40, 0); Net_bunki.Ferli_ramma(44); sannprófa(Net_bunki.RECEIVED_lengd[0] == 2);
        int[] NIÐURSTAÐA = new int[4];
        sannprófa(Net_bunki.받기(3, NIÐURSTAÐA, 1, 0) == -90);
        sannprófa(Net_bunki.받기(3, NIÐURSTAÐA, 4, 0) == -11);
        Undirbúa(2); Net_bunki.Ferli_ramma(44); int fleygja_VALUE = Net_bunki.폐기수;
        Net_bunki.Ferli_ramma(44); sannprófa(Net_bunki.폐기수 == fleygja_VALUE + 1);
        Net_bunki.CLEAN_Ferli(); sannprófa(Net_bunki.Opna(5000) == 3);
        sannprófa(Net_bunki.Opna(5000) == -98); sannprófa(Net_bunki.Opna(0) == 4);
        sannprófa(Net_bunki.Opna(0) == 5); sannprófa(Net_bunki.Opna(0) == 6); sannprófa(Net_bunki.Opna(0) == -24);
        sannprófa(Net_bunki.Loka(4) == 0); sannprófa(Net_bunki.Loka(4) == -9);
        Net_bunki.찾은주소 = Net_bunki.gátt_VALUE_cfee51e8;
        sannprófa(Net_bunki.senda(3, Net_bunki.gátt_VALUE_cfee51e8, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Net_rekill.nýlegt_VALUE;
        sannprófa(prófsumma(보냄, 14, 20, 0) == 0);
        sannprófa(prófsumma(보냄, 34, 11, Net_bunki.가상머리합(Net_bunki.내주소, Net_bunki.gátt_VALUE_cfee51e8, 11)) == 0);
        sannprófa(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
