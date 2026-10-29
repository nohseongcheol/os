// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** dearbh_dàta Java cùis_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void dearbh(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] VALUE, int ruith, int faid_VALUE, int 초기) {
        int SUM_VALUE = 초기;
        for (int INDEX = 0; INDEX < faid_VALUE; INDEX++) SUM_VALUE += VALUE[ruith + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Ullaich(int faid_VALUE) {
        lìonra_stac.CLEAN_Pròiseas();
        dearbh(lìonra_stac.fosgail(5000) == 3);
        int[] frèam_INDEX = lìonra_stac.입력틀;
        Arrays.fill(frèam_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) frèam_INDEX[INDEX] = lìonra_dràibhear.uidheam_ADDRESS[INDEX];
        lìonra_stac.넣기16(frèam_INDEX, 12, 0x0800);
        frèam_INDEX[14] = 0x45; frèam_INDEX[22] = 64; frèam_INDEX[23] = 17;
        lìonra_stac.넣기16(frèam_INDEX, 16, 28 + faid_VALUE);
        lìonra_stac.넣기32(frèam_INDEX, 26, 0x0a000202); lìonra_stac.넣기32(frèam_INDEX, 30, lìonra_stac.내주소);
        lìonra_stac.넣기16(frèam_INDEX, 34, 4321); lìonra_stac.넣기16(frèam_INDEX, 36, 5000); lìonra_stac.넣기16(frèam_INDEX, 38, faid_VALUE + 8);
        for (int INDEX = 0; INDEX < faid_VALUE; INDEX++) frèam_INDEX[42 + INDEX] = INDEX & 255;
        검사합넣기(faid_VALUE);
    }
    static void 검사합넣기(int faid_VALUE) {
        int[] frèam_INDEX = lìonra_stac.입력틀;
        lìonra_stac.넣기16(frèam_INDEX, 24, 0); lìonra_stac.넣기16(frèam_INDEX, 40, 0);
        lìonra_stac.넣기16(frèam_INDEX, 24, 검사합(frèam_INDEX, 14, 20, 0));
        int 초기 = lìonra_stac.가상머리합(lìonra_stac.àireamh_shlàn_32(frèam_INDEX, 26), lìonra_stac.내주소, faid_VALUE + 8);
        int SUM_VALUE = 검사합(frèam_INDEX, 34, faid_VALUE + 8, 초기);
        lìonra_stac.넣기16(frèam_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void 거부(int faid_VALUE) { lìonra_stac.Pròiseas_frèam(faid_VALUE); dearbh(lìonra_stac.RECEIVED_faid[0] == -1); }
    public static void main(String[] 인수) {
        for (int faid_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Ullaich(faid_VALUE); lìonra_stac.Pròiseas_frèam(faid_VALUE + 42);
            dearbh(lìonra_stac.RECEIVED_faid[0] == faid_VALUE);
            dearbh(lìonra_stac.RECEIVED_ADDRESS[0] == 0x0a000202 && lìonra_stac.받은접속번호[0] == 4321);
            for (int INDEX = 0; INDEX < faid_VALUE; INDEX++) dearbh(lìonra_stac.RECEIVED_dàta[INDEX] == (INDEX & 255));
        }
        for (int faid_VALUE = 0; faid_VALUE < 42; faid_VALUE++) { Ullaich(0); 거부(faid_VALUE); }
        Ullaich(1025); 거부(1067);
        Ullaich(2); lìonra_stac.입력틀[24] ^= 1; 거부(44);
        Ullaich(2); lìonra_stac.입력틀[42] ^= 1; 거부(44);
        Ullaich(2); lìonra_stac.넣기16(lìonra_stac.입력틀, 38, 7); 거부(44);
        Ullaich(2); lìonra_stac.넣기16(lìonra_stac.입력틀, 38, 65535); 거부(44);
        Ullaich(2); lìonra_stac.입력틀[14] = 0x4f; 거부(44);
        Ullaich(2); lìonra_stac.입력틀[14] = 0x44; 거부(44);
        Ullaich(2); lìonra_stac.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        Ullaich(2); lìonra_stac.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        Ullaich(2); lìonra_stac.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        Ullaich(2); lìonra_stac.입력틀[0] ^= 1; 거부(44);
        Ullaich(2); lìonra_stac.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        Ullaich(2); lìonra_stac.넣기16(lìonra_stac.입력틀, 40, 0); lìonra_stac.Pròiseas_frèam(44); dearbh(lìonra_stac.RECEIVED_faid[0] == 2);
        int[] tomhas = new int[4];
        dearbh(lìonra_stac.받기(3, tomhas, 1, 0) == -90);
        dearbh(lìonra_stac.받기(3, tomhas, 4, 0) == -11);
        Ullaich(2); lìonra_stac.Pròiseas_frèam(44); int tilg_air_falbh_VALUE = lìonra_stac.폐기수;
        lìonra_stac.Pròiseas_frèam(44); dearbh(lìonra_stac.폐기수 == tilg_air_falbh_VALUE + 1);
        lìonra_stac.CLEAN_Pròiseas(); dearbh(lìonra_stac.fosgail(5000) == 3);
        dearbh(lìonra_stac.fosgail(5000) == -98); dearbh(lìonra_stac.fosgail(0) == 4);
        dearbh(lìonra_stac.fosgail(0) == 5); dearbh(lìonra_stac.fosgail(0) == 6); dearbh(lìonra_stac.fosgail(0) == -24);
        dearbh(lìonra_stac.dùin(4) == 0); dearbh(lìonra_stac.dùin(4) == -9);
        lìonra_stac.찾은주소 = lìonra_stac.관문;
        dearbh(lìonra_stac.cuir(3, lìonra_stac.관문, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = lìonra_dràibhear.o_chionn_ghoirid_VALUE;
        dearbh(검사합(보냄, 14, 20, 0) == 0);
        dearbh(검사합(보냄, 34, 11, lìonra_stac.가상머리합(lìonra_stac.내주소, lìonra_stac.관문, 11)) == 0);
        dearbh(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
