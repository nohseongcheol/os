// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** aktual_të_dhëna Java punë_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void verifikoj(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int kontrolli_i_shumës(int[] VALUE, int Ekzekuto, int gjatësi_VALUE, int 초기) {
        int SUM_VALUE = 초기;
        for (int INDEX = 0; INDEX < gjatësi_VALUE; INDEX++) SUM_VALUE += VALUE[Ekzekuto + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Përgatit(int gjatësi_VALUE) {
        rrjet_Stivë.CLEAN_Proces();
        verifikoj(rrjet_Stivë.Hap(5000) == 3);
        int[] kuadër_INDEX = rrjet_Stivë.입력틀;
        Arrays.fill(kuadër_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) kuadër_INDEX[INDEX] = rrjet_drejtues.pajisje_email[INDEX];
        rrjet_Stivë.넣기16(kuadër_INDEX, 12, 0x0800);
        kuadër_INDEX[14] = 0x45; kuadër_INDEX[22] = 64; kuadër_INDEX[23] = 17;
        rrjet_Stivë.넣기16(kuadër_INDEX, 16, 28 + gjatësi_VALUE);
        rrjet_Stivë.넣기32(kuadër_INDEX, 26, 0x0a000202); rrjet_Stivë.넣기32(kuadër_INDEX, 30, rrjet_Stivë.내주소);
        rrjet_Stivë.넣기16(kuadër_INDEX, 34, 4321); rrjet_Stivë.넣기16(kuadër_INDEX, 36, 5000); rrjet_Stivë.넣기16(kuadër_INDEX, 38, gjatësi_VALUE + 8);
        for (int INDEX = 0; INDEX < gjatësi_VALUE; INDEX++) kuadër_INDEX[42 + INDEX] = INDEX & 255;
        bashkësi_kontrolli_i_shumës(gjatësi_VALUE);
    }
    static void bashkësi_kontrolli_i_shumës(int gjatësi_VALUE) {
        int[] kuadër_INDEX = rrjet_Stivë.입력틀;
        rrjet_Stivë.넣기16(kuadër_INDEX, 24, 0); rrjet_Stivë.넣기16(kuadër_INDEX, 40, 0);
        rrjet_Stivë.넣기16(kuadër_INDEX, 24, kontrolli_i_shumës(kuadër_INDEX, 14, 20, 0));
        int 초기 = rrjet_Stivë.가상머리합(rrjet_Stivë.numër_i_plotë_32(kuadër_INDEX, 26), rrjet_Stivë.내주소, gjatësi_VALUE + 8);
        int SUM_VALUE = kontrolli_i_shumës(kuadër_INDEX, 34, gjatësi_VALUE + 8, 초기);
        rrjet_Stivë.넣기16(kuadër_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void refuzo_VALUE(int gjatësi_VALUE) { rrjet_Stivë.Proces_kuadër(gjatësi_VALUE); verifikoj(rrjet_Stivë.RECEIVED_gjatësi[0] == -1); }
    public static void main(String[] Argumente) {
        for (int gjatësi_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Përgatit(gjatësi_VALUE); rrjet_Stivë.Proces_kuadër(gjatësi_VALUE + 42);
            verifikoj(rrjet_Stivë.RECEIVED_gjatësi[0] == gjatësi_VALUE);
            verifikoj(rrjet_Stivë.RECEIVED_email[0] == 0x0a000202 && rrjet_Stivë.RECEIVED_numri_i_portës[0] == 4321);
            for (int INDEX = 0; INDEX < gjatësi_VALUE; INDEX++) verifikoj(rrjet_Stivë.RECEIVED_të_dhëna[INDEX] == (INDEX & 255));
        }
        for (int gjatësi_VALUE = 0; gjatësi_VALUE < 42; gjatësi_VALUE++) { Përgatit(0); refuzo_VALUE(gjatësi_VALUE); }
        Përgatit(1025); refuzo_VALUE(1067);
        Përgatit(2); rrjet_Stivë.입력틀[24] ^= 1; refuzo_VALUE(44);
        Përgatit(2); rrjet_Stivë.입력틀[42] ^= 1; refuzo_VALUE(44);
        Përgatit(2); rrjet_Stivë.넣기16(rrjet_Stivë.입력틀, 38, 7); refuzo_VALUE(44);
        Përgatit(2); rrjet_Stivë.넣기16(rrjet_Stivë.입력틀, 38, 65535); refuzo_VALUE(44);
        Përgatit(2); rrjet_Stivë.입력틀[14] = 0x4f; refuzo_VALUE(44);
        Përgatit(2); rrjet_Stivë.입력틀[14] = 0x44; refuzo_VALUE(44);
        Përgatit(2); rrjet_Stivë.입력틀[20] = 0x20; bashkësi_kontrolli_i_shumës(2); refuzo_VALUE(44);
        Përgatit(2); rrjet_Stivë.입력틀[21] = 1; bashkësi_kontrolli_i_shumës(2); refuzo_VALUE(44);
        Përgatit(2); rrjet_Stivë.입력틀[33] = 99; bashkësi_kontrolli_i_shumës(2); refuzo_VALUE(44);
        Përgatit(2); rrjet_Stivë.입력틀[0] ^= 1; refuzo_VALUE(44);
        Përgatit(2); rrjet_Stivë.입력틀[23] = 6; bashkësi_kontrolli_i_shumës(2); refuzo_VALUE(44);
        Përgatit(2); rrjet_Stivë.넣기16(rrjet_Stivë.입력틀, 40, 0); rrjet_Stivë.Proces_kuadër(44); verifikoj(rrjet_Stivë.RECEIVED_gjatësi[0] == 2);
        int[] llogaritje = new int[4];
        verifikoj(rrjet_Stivë.받기(3, llogaritje, 1, 0) == -90);
        verifikoj(rrjet_Stivë.받기(3, llogaritje, 4, 0) == -11);
        Përgatit(2); rrjet_Stivë.Proces_kuadër(44); int heq_VALUE = rrjet_Stivë.폐기수;
        rrjet_Stivë.Proces_kuadër(44); verifikoj(rrjet_Stivë.폐기수 == heq_VALUE + 1);
        rrjet_Stivë.CLEAN_Proces(); verifikoj(rrjet_Stivë.Hap(5000) == 3);
        verifikoj(rrjet_Stivë.Hap(5000) == -98); verifikoj(rrjet_Stivë.Hap(0) == 4);
        verifikoj(rrjet_Stivë.Hap(0) == 5); verifikoj(rrjet_Stivë.Hap(0) == 6); verifikoj(rrjet_Stivë.Hap(0) == -24);
        verifikoj(rrjet_Stivë.Mbyll(4) == 0); verifikoj(rrjet_Stivë.Mbyll(4) == -9);
        rrjet_Stivë.찾은주소 = rrjet_Stivë.portëkalimi_VALUE;
        verifikoj(rrjet_Stivë.dërgoj(3, rrjet_Stivë.portëkalimi_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = rrjet_drejtues.së_fundi_VALUE;
        verifikoj(kontrolli_i_shumës(보냄, 14, 20, 0) == 0);
        verifikoj(kontrolli_i_shumës(보냄, 34, 11, rrjet_Stivë.가상머리합(rrjet_Stivë.내주소, rrjet_Stivë.portëkalimi_VALUE, 11)) == 0);
        verifikoj(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
