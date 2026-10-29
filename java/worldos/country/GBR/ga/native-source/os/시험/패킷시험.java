// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** iarbhír_sonraí Java cás_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void fíoraigh(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int suim_seiceála(int[] VALUE, int Rith_2, int fad_VALUE, int 초기) {
        int SUM_VALUE = 초기;
        for (int INDEX = 0; INDEX < fad_VALUE; INDEX++) SUM_VALUE += VALUE[Rith_2 + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Ullmhaigh(int fad_VALUE) {
        Líonra_Cruach.CLEAN_Próiseas();
        fíoraigh(Líonra_Cruach.Oscail(5000) == 3);
        int[] fráma_INDEX = Líonra_Cruach.입력틀;
        Arrays.fill(fráma_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) fráma_INDEX[INDEX] = Líonra_tiománaí.gléas_ADDRESS[INDEX];
        Líonra_Cruach.넣기16(fráma_INDEX, 12, 0x0800);
        fráma_INDEX[14] = 0x45; fráma_INDEX[22] = 64; fráma_INDEX[23] = 17;
        Líonra_Cruach.넣기16(fráma_INDEX, 16, 28 + fad_VALUE);
        Líonra_Cruach.넣기32(fráma_INDEX, 26, 0x0a000202); Líonra_Cruach.넣기32(fráma_INDEX, 30, Líonra_Cruach.내주소);
        Líonra_Cruach.넣기16(fráma_INDEX, 34, 4321); Líonra_Cruach.넣기16(fráma_INDEX, 36, 5000); Líonra_Cruach.넣기16(fráma_INDEX, 38, fad_VALUE + 8);
        for (int INDEX = 0; INDEX < fad_VALUE; INDEX++) fráma_INDEX[42 + INDEX] = INDEX & 255;
        tacar_suim_seiceála(fad_VALUE);
    }
    static void tacar_suim_seiceála(int fad_VALUE) {
        int[] fráma_INDEX = Líonra_Cruach.입력틀;
        Líonra_Cruach.넣기16(fráma_INDEX, 24, 0); Líonra_Cruach.넣기16(fráma_INDEX, 40, 0);
        Líonra_Cruach.넣기16(fráma_INDEX, 24, suim_seiceála(fráma_INDEX, 14, 20, 0));
        int 초기 = Líonra_Cruach.가상머리합(Líonra_Cruach.slánuimhir_32(fráma_INDEX, 26), Líonra_Cruach.내주소, fad_VALUE + 8);
        int SUM_VALUE = suim_seiceála(fráma_INDEX, 34, fad_VALUE + 8, 초기);
        Líonra_Cruach.넣기16(fráma_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void diúltaigh_VALUE(int fad_VALUE) { Líonra_Cruach.Próiseas_fráma(fad_VALUE); fíoraigh(Líonra_Cruach.RECEIVED_fad[0] == -1); }
    public static void main(String[] Argóintí) {
        for (int fad_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Ullmhaigh(fad_VALUE); Líonra_Cruach.Próiseas_fráma(fad_VALUE + 42);
            fíoraigh(Líonra_Cruach.RECEIVED_fad[0] == fad_VALUE);
            fíoraigh(Líonra_Cruach.RECEIVED_ADDRESS[0] == 0x0a000202 && Líonra_Cruach.RECEIVED_uimhir_phoirt[0] == 4321);
            for (int INDEX = 0; INDEX < fad_VALUE; INDEX++) fíoraigh(Líonra_Cruach.RECEIVED_sonraí[INDEX] == (INDEX & 255));
        }
        for (int fad_VALUE = 0; fad_VALUE < 42; fad_VALUE++) { Ullmhaigh(0); diúltaigh_VALUE(fad_VALUE); }
        Ullmhaigh(1025); diúltaigh_VALUE(1067);
        Ullmhaigh(2); Líonra_Cruach.입력틀[24] ^= 1; diúltaigh_VALUE(44);
        Ullmhaigh(2); Líonra_Cruach.입력틀[42] ^= 1; diúltaigh_VALUE(44);
        Ullmhaigh(2); Líonra_Cruach.넣기16(Líonra_Cruach.입력틀, 38, 7); diúltaigh_VALUE(44);
        Ullmhaigh(2); Líonra_Cruach.넣기16(Líonra_Cruach.입력틀, 38, 65535); diúltaigh_VALUE(44);
        Ullmhaigh(2); Líonra_Cruach.입력틀[14] = 0x4f; diúltaigh_VALUE(44);
        Ullmhaigh(2); Líonra_Cruach.입력틀[14] = 0x44; diúltaigh_VALUE(44);
        Ullmhaigh(2); Líonra_Cruach.입력틀[20] = 0x20; tacar_suim_seiceála(2); diúltaigh_VALUE(44);
        Ullmhaigh(2); Líonra_Cruach.입력틀[21] = 1; tacar_suim_seiceála(2); diúltaigh_VALUE(44);
        Ullmhaigh(2); Líonra_Cruach.입력틀[33] = 99; tacar_suim_seiceála(2); diúltaigh_VALUE(44);
        Ullmhaigh(2); Líonra_Cruach.입력틀[0] ^= 1; diúltaigh_VALUE(44);
        Ullmhaigh(2); Líonra_Cruach.입력틀[23] = 6; tacar_suim_seiceála(2); diúltaigh_VALUE(44);
        Ullmhaigh(2); Líonra_Cruach.넣기16(Líonra_Cruach.입력틀, 40, 0); Líonra_Cruach.Próiseas_fráma(44); fíoraigh(Líonra_Cruach.RECEIVED_fad[0] == 2);
        int[] tomhas = new int[4];
        fíoraigh(Líonra_Cruach.받기(3, tomhas, 1, 0) == -90);
        fíoraigh(Líonra_Cruach.받기(3, tomhas, 4, 0) == -11);
        Ullmhaigh(2); Líonra_Cruach.Próiseas_fráma(44); int cuileáil_VALUE = Líonra_Cruach.폐기수;
        Líonra_Cruach.Próiseas_fráma(44); fíoraigh(Líonra_Cruach.폐기수 == cuileáil_VALUE + 1);
        Líonra_Cruach.CLEAN_Próiseas(); fíoraigh(Líonra_Cruach.Oscail(5000) == 3);
        fíoraigh(Líonra_Cruach.Oscail(5000) == -98); fíoraigh(Líonra_Cruach.Oscail(0) == 4);
        fíoraigh(Líonra_Cruach.Oscail(0) == 5); fíoraigh(Líonra_Cruach.Oscail(0) == 6); fíoraigh(Líonra_Cruach.Oscail(0) == -24);
        fíoraigh(Líonra_Cruach.Dún(4) == 0); fíoraigh(Líonra_Cruach.Dún(4) == -9);
        Líonra_Cruach.찾은주소 = Líonra_Cruach.geata_VALUE;
        fíoraigh(Líonra_Cruach.seol(3, Líonra_Cruach.geata_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Líonra_tiománaí.le_déanaí_VALUE;
        fíoraigh(suim_seiceála(보냄, 14, 20, 0) == 0);
        fíoraigh(suim_seiceála(보냄, 34, 11, Líonra_Cruach.가상머리합(Líonra_Cruach.내주소, Líonra_Cruach.geata_VALUE, 11)) == 0);
        fíoraigh(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
