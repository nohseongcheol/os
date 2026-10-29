// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** go_iawn_data Java tasg_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void dilysu(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int prawfswm(int[] VALUE, int Gweithredu_2, int hyd_VALUE, int 초기) {
        int SUM_VALUE = 초기;
        for (int INDEX = 0; INDEX < hyd_VALUE; INDEX++) SUM_VALUE += VALUE[Gweithredu_2 + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Paratoi(int hyd_VALUE) {
        Rhwydwaith_pentwr.Glân_Proses();
        dilysu(Rhwydwaith_pentwr.Agor(5000) == 3);
        int[] ffrâm_INDEX = Rhwydwaith_pentwr.입력틀;
        Arrays.fill(ffrâm_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) ffrâm_INDEX[INDEX] = Rhwydwaith_gyrrwr.dyfais_ADDRESS[INDEX];
        Rhwydwaith_pentwr.넣기16(ffrâm_INDEX, 12, 0x0800);
        ffrâm_INDEX[14] = 0x45; ffrâm_INDEX[22] = 64; ffrâm_INDEX[23] = 17;
        Rhwydwaith_pentwr.넣기16(ffrâm_INDEX, 16, 28 + hyd_VALUE);
        Rhwydwaith_pentwr.넣기32(ffrâm_INDEX, 26, 0x0a000202); Rhwydwaith_pentwr.넣기32(ffrâm_INDEX, 30, Rhwydwaith_pentwr.내주소);
        Rhwydwaith_pentwr.넣기16(ffrâm_INDEX, 34, 4321); Rhwydwaith_pentwr.넣기16(ffrâm_INDEX, 36, 5000); Rhwydwaith_pentwr.넣기16(ffrâm_INDEX, 38, hyd_VALUE + 8);
        for (int INDEX = 0; INDEX < hyd_VALUE; INDEX++) ffrâm_INDEX[42 + INDEX] = INDEX & 255;
        set_prawfswm(hyd_VALUE);
    }
    static void set_prawfswm(int hyd_VALUE) {
        int[] ffrâm_INDEX = Rhwydwaith_pentwr.입력틀;
        Rhwydwaith_pentwr.넣기16(ffrâm_INDEX, 24, 0); Rhwydwaith_pentwr.넣기16(ffrâm_INDEX, 40, 0);
        Rhwydwaith_pentwr.넣기16(ffrâm_INDEX, 24, prawfswm(ffrâm_INDEX, 14, 20, 0));
        int 초기 = Rhwydwaith_pentwr.가상머리합(Rhwydwaith_pentwr.cyfanrif_32(ffrâm_INDEX, 26), Rhwydwaith_pentwr.내주소, hyd_VALUE + 8);
        int SUM_VALUE = prawfswm(ffrâm_INDEX, 34, hyd_VALUE + 8, 초기);
        Rhwydwaith_pentwr.넣기16(ffrâm_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void gwrthod_VALUE(int hyd_VALUE) { Rhwydwaith_pentwr.Proses_ffrâm(hyd_VALUE); dilysu(Rhwydwaith_pentwr.RECEIVED_hyd[0] == -1); }
    public static void main(String[] 인수) {
        for (int hyd_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Paratoi(hyd_VALUE); Rhwydwaith_pentwr.Proses_ffrâm(hyd_VALUE + 42);
            dilysu(Rhwydwaith_pentwr.RECEIVED_hyd[0] == hyd_VALUE);
            dilysu(Rhwydwaith_pentwr.RECEIVED_ADDRESS[0] == 0x0a000202 && Rhwydwaith_pentwr.RECEIVED_rhif_porth[0] == 4321);
            for (int INDEX = 0; INDEX < hyd_VALUE; INDEX++) dilysu(Rhwydwaith_pentwr.RECEIVED_data[INDEX] == (INDEX & 255));
        }
        for (int hyd_VALUE = 0; hyd_VALUE < 42; hyd_VALUE++) { Paratoi(0); gwrthod_VALUE(hyd_VALUE); }
        Paratoi(1025); gwrthod_VALUE(1067);
        Paratoi(2); Rhwydwaith_pentwr.입력틀[24] ^= 1; gwrthod_VALUE(44);
        Paratoi(2); Rhwydwaith_pentwr.입력틀[42] ^= 1; gwrthod_VALUE(44);
        Paratoi(2); Rhwydwaith_pentwr.넣기16(Rhwydwaith_pentwr.입력틀, 38, 7); gwrthod_VALUE(44);
        Paratoi(2); Rhwydwaith_pentwr.넣기16(Rhwydwaith_pentwr.입력틀, 38, 65535); gwrthod_VALUE(44);
        Paratoi(2); Rhwydwaith_pentwr.입력틀[14] = 0x4f; gwrthod_VALUE(44);
        Paratoi(2); Rhwydwaith_pentwr.입력틀[14] = 0x44; gwrthod_VALUE(44);
        Paratoi(2); Rhwydwaith_pentwr.입력틀[20] = 0x20; set_prawfswm(2); gwrthod_VALUE(44);
        Paratoi(2); Rhwydwaith_pentwr.입력틀[21] = 1; set_prawfswm(2); gwrthod_VALUE(44);
        Paratoi(2); Rhwydwaith_pentwr.입력틀[33] = 99; set_prawfswm(2); gwrthod_VALUE(44);
        Paratoi(2); Rhwydwaith_pentwr.입력틀[0] ^= 1; gwrthod_VALUE(44);
        Paratoi(2); Rhwydwaith_pentwr.입력틀[23] = 6; set_prawfswm(2); gwrthod_VALUE(44);
        Paratoi(2); Rhwydwaith_pentwr.넣기16(Rhwydwaith_pentwr.입력틀, 40, 0); Rhwydwaith_pentwr.Proses_ffrâm(44); dilysu(Rhwydwaith_pentwr.RECEIVED_hyd[0] == 2);
        int[] mesur = new int[4];
        dilysu(Rhwydwaith_pentwr.받기(3, mesur, 1, 0) == -90);
        dilysu(Rhwydwaith_pentwr.받기(3, mesur, 4, 0) == -11);
        Paratoi(2); Rhwydwaith_pentwr.Proses_ffrâm(44); int gwaredu_VALUE = Rhwydwaith_pentwr.폐기수;
        Rhwydwaith_pentwr.Proses_ffrâm(44); dilysu(Rhwydwaith_pentwr.폐기수 == gwaredu_VALUE + 1);
        Rhwydwaith_pentwr.Glân_Proses(); dilysu(Rhwydwaith_pentwr.Agor(5000) == 3);
        dilysu(Rhwydwaith_pentwr.Agor(5000) == -98); dilysu(Rhwydwaith_pentwr.Agor(0) == 4);
        dilysu(Rhwydwaith_pentwr.Agor(0) == 5); dilysu(Rhwydwaith_pentwr.Agor(0) == 6); dilysu(Rhwydwaith_pentwr.Agor(0) == -24);
        dilysu(Rhwydwaith_pentwr.Cau(4) == 0); dilysu(Rhwydwaith_pentwr.Cau(4) == -9);
        Rhwydwaith_pentwr.찾은주소 = Rhwydwaith_pentwr.adwy_VALUE;
        dilysu(Rhwydwaith_pentwr.anfon(3, Rhwydwaith_pentwr.adwy_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Rhwydwaith_gyrrwr.yn_ddiweddar_VALUE;
        dilysu(prawfswm(보냄, 14, 20, 0) == 0);
        dilysu(prawfswm(보냄, 34, 11, Rhwydwaith_pentwr.가상머리합(Rhwydwaith_pentwr.내주소, Rhwydwaith_pentwr.adwy_VALUE, 11)) == 0);
        dilysu(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
