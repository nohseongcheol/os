// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** attwali_data Java każ_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void vverifika(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] VALUE, int serje, int tul_VALUE, int 초기) {
        int SUM_VALUE = 초기;
        for (int INDEX = 0; INDEX < tul_VALUE; INDEX++) SUM_VALUE += VALUE[serje + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Ħejji(int tul_VALUE) {
        netwerk_Munzell.CLEAN_Proċess();
        vverifika(netwerk_Munzell.fetaħ(5000) == 3);
        int[] frejm_INDEX = netwerk_Munzell.입력틀;
        Arrays.fill(frejm_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) frejm_INDEX[INDEX] = netwerk_drajver.mowbajl_ADDRESS[INDEX];
        netwerk_Munzell.넣기16(frejm_INDEX, 12, 0x0800);
        frejm_INDEX[14] = 0x45; frejm_INDEX[22] = 64; frejm_INDEX[23] = 17;
        netwerk_Munzell.넣기16(frejm_INDEX, 16, 28 + tul_VALUE);
        netwerk_Munzell.넣기32(frejm_INDEX, 26, 0x0a000202); netwerk_Munzell.넣기32(frejm_INDEX, 30, netwerk_Munzell.내주소);
        netwerk_Munzell.넣기16(frejm_INDEX, 34, 4321); netwerk_Munzell.넣기16(frejm_INDEX, 36, 5000); netwerk_Munzell.넣기16(frejm_INDEX, 38, tul_VALUE + 8);
        for (int INDEX = 0; INDEX < tul_VALUE; INDEX++) frejm_INDEX[42 + INDEX] = INDEX & 255;
        검사합넣기(tul_VALUE);
    }
    static void 검사합넣기(int tul_VALUE) {
        int[] frejm_INDEX = netwerk_Munzell.입력틀;
        netwerk_Munzell.넣기16(frejm_INDEX, 24, 0); netwerk_Munzell.넣기16(frejm_INDEX, 40, 0);
        netwerk_Munzell.넣기16(frejm_INDEX, 24, 검사합(frejm_INDEX, 14, 20, 0));
        int 초기 = netwerk_Munzell.가상머리합(netwerk_Munzell.numru_sħiħ_32(frejm_INDEX, 26), netwerk_Munzell.내주소, tul_VALUE + 8);
        int SUM_VALUE = 검사합(frejm_INDEX, 34, tul_VALUE + 8, 초기);
        netwerk_Munzell.넣기16(frejm_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void 거부(int tul_VALUE) { netwerk_Munzell.Proċess_frejm(tul_VALUE); vverifika(netwerk_Munzell.RECEIVED_tul[0] == -1); }
    public static void main(String[] 인수) {
        for (int tul_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Ħejji(tul_VALUE); netwerk_Munzell.Proċess_frejm(tul_VALUE + 42);
            vverifika(netwerk_Munzell.RECEIVED_tul[0] == tul_VALUE);
            vverifika(netwerk_Munzell.RECEIVED_ADDRESS[0] == 0x0a000202 && netwerk_Munzell.받은접속번호[0] == 4321);
            for (int INDEX = 0; INDEX < tul_VALUE; INDEX++) vverifika(netwerk_Munzell.RECEIVED_data[INDEX] == (INDEX & 255));
        }
        for (int tul_VALUE = 0; tul_VALUE < 42; tul_VALUE++) { Ħejji(0); 거부(tul_VALUE); }
        Ħejji(1025); 거부(1067);
        Ħejji(2); netwerk_Munzell.입력틀[24] ^= 1; 거부(44);
        Ħejji(2); netwerk_Munzell.입력틀[42] ^= 1; 거부(44);
        Ħejji(2); netwerk_Munzell.넣기16(netwerk_Munzell.입력틀, 38, 7); 거부(44);
        Ħejji(2); netwerk_Munzell.넣기16(netwerk_Munzell.입력틀, 38, 65535); 거부(44);
        Ħejji(2); netwerk_Munzell.입력틀[14] = 0x4f; 거부(44);
        Ħejji(2); netwerk_Munzell.입력틀[14] = 0x44; 거부(44);
        Ħejji(2); netwerk_Munzell.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        Ħejji(2); netwerk_Munzell.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        Ħejji(2); netwerk_Munzell.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        Ħejji(2); netwerk_Munzell.입력틀[0] ^= 1; 거부(44);
        Ħejji(2); netwerk_Munzell.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        Ħejji(2); netwerk_Munzell.넣기16(netwerk_Munzell.입력틀, 40, 0); netwerk_Munzell.Proċess_frejm(44); vverifika(netwerk_Munzell.RECEIVED_tul[0] == 2);
        int[] miżura = new int[4];
        vverifika(netwerk_Munzell.받기(3, miżura, 1, 0) == -90);
        vverifika(netwerk_Munzell.받기(3, miżura, 4, 0) == -11);
        Ħejji(2); netwerk_Munzell.Proċess_frejm(44); int warrab_VALUE = netwerk_Munzell.폐기수;
        netwerk_Munzell.Proċess_frejm(44); vverifika(netwerk_Munzell.폐기수 == warrab_VALUE + 1);
        netwerk_Munzell.CLEAN_Proċess(); vverifika(netwerk_Munzell.fetaħ(5000) == 3);
        vverifika(netwerk_Munzell.fetaħ(5000) == -98); vverifika(netwerk_Munzell.fetaħ(0) == 4);
        vverifika(netwerk_Munzell.fetaħ(0) == 5); vverifika(netwerk_Munzell.fetaħ(0) == 6); vverifika(netwerk_Munzell.fetaħ(0) == -24);
        vverifika(netwerk_Munzell.agħlaq(4) == 0); vverifika(netwerk_Munzell.agħlaq(4) == -9);
        netwerk_Munzell.찾은주소 = netwerk_Munzell.gateway_VALUE;
        vverifika(netwerk_Munzell.bagħat(3, netwerk_Munzell.gateway_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = netwerk_drajver.reċenti_VALUE;
        vverifika(검사합(보냄, 14, 20, 0) == 0);
        vverifika(검사합(보냄, 34, 11, netwerk_Munzell.가상머리합(netwerk_Munzell.내주소, netwerk_Munzell.gateway_VALUE, 11)) == 0);
        vverifika(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
