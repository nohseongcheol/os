// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** taannallarik_titiqqat Java pijatsaq_atuutilik 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void nalunairli_1aacb54c(boolean atuutilik) { if (!atuutilik) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] atuutilik, int 시작, int takininga_atuutilik, int 초기) {
        int 합 = 초기;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < takininga_atuutilik; nalunaiqsimavik++) 합 += atuutilik[시작 + nalunaiqsimavik] << ((nalunaiqsimavik & 1) == 0 ? 8 : 0);
        합 = (합 & 65535) + (합 >>> 16);
        합 = (합 & 65535) + (합 >>> 16);
        return ~합 & 65535;
    }
    static void Parnalli(int takininga_atuutilik) {
        통신망.과정정리();
        nalunairli_1aacb54c(통신망.matuirli(5000) == 3);
        int[] avalu_nalunaiqsimavik = 통신망.입력틀;
        Arrays.fill(avalu_nalunaiqsimavik, 0);
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 6; nalunaiqsimavik++) avalu_nalunaiqsimavik[nalunaiqsimavik] = Kasuqatigiitsimajut_qarasaujalirijjut.sunakkutaaq_turaarut[nalunaiqsimavik];
        통신망.넣기16(avalu_nalunaiqsimavik, 12, 0x0800);
        avalu_nalunaiqsimavik[14] = 0x45; avalu_nalunaiqsimavik[22] = 64; avalu_nalunaiqsimavik[23] = 17;
        통신망.넣기16(avalu_nalunaiqsimavik, 16, 28 + takininga_atuutilik);
        통신망.넣기32(avalu_nalunaiqsimavik, 26, 0x0a000202); 통신망.넣기32(avalu_nalunaiqsimavik, 30, 통신망.내주소);
        통신망.넣기16(avalu_nalunaiqsimavik, 34, 4321); 통신망.넣기16(avalu_nalunaiqsimavik, 36, 5000); 통신망.넣기16(avalu_nalunaiqsimavik, 38, takininga_atuutilik + 8);
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < takininga_atuutilik; nalunaiqsimavik++) avalu_nalunaiqsimavik[42 + nalunaiqsimavik] = nalunaiqsimavik & 255;
        검사합넣기(takininga_atuutilik);
    }
    static void 검사합넣기(int takininga_atuutilik) {
        int[] avalu_nalunaiqsimavik = 통신망.입력틀;
        통신망.넣기16(avalu_nalunaiqsimavik, 24, 0); 통신망.넣기16(avalu_nalunaiqsimavik, 40, 0);
        통신망.넣기16(avalu_nalunaiqsimavik, 24, 검사합(avalu_nalunaiqsimavik, 14, 20, 0));
        int 초기 = 통신망.가상머리합(통신망.naasaut_32(avalu_nalunaiqsimavik, 26), 통신망.내주소, takininga_atuutilik + 8);
        int 합 = 검사합(avalu_nalunaiqsimavik, 34, takininga_atuutilik + 8, 초기);
        통신망.넣기16(avalu_nalunaiqsimavik, 40, 합 == 0 ? 65535 : 합);
    }
    static void 거부(int takininga_atuutilik) { 통신망.Pivallianiq_avalu(takininga_atuutilik); nalunairli_1aacb54c(통신망.받은길이[0] == -1); }
    public static void main(String[] 인수) {
        for (int takininga_atuutilik : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Parnalli(takininga_atuutilik); 통신망.Pivallianiq_avalu(takininga_atuutilik + 42);
            nalunairli_1aacb54c(통신망.받은길이[0] == takininga_atuutilik);
            nalunairli_1aacb54c(통신망.받은주소[0] == 0x0a000202 && 통신망.받은접속번호[0] == 4321);
            for (int nalunaiqsimavik = 0; nalunaiqsimavik < takininga_atuutilik; nalunaiqsimavik++) nalunairli_1aacb54c(통신망.받은자료[nalunaiqsimavik] == (nalunaiqsimavik & 255));
        }
        for (int takininga_atuutilik = 0; takininga_atuutilik < 42; takininga_atuutilik++) { Parnalli(0); 거부(takininga_atuutilik); }
        Parnalli(1025); 거부(1067);
        Parnalli(2); 통신망.입력틀[24] ^= 1; 거부(44);
        Parnalli(2); 통신망.입력틀[42] ^= 1; 거부(44);
        Parnalli(2); 통신망.넣기16(통신망.입력틀, 38, 7); 거부(44);
        Parnalli(2); 통신망.넣기16(통신망.입력틀, 38, 65535); 거부(44);
        Parnalli(2); 통신망.입력틀[14] = 0x4f; 거부(44);
        Parnalli(2); 통신망.입력틀[14] = 0x44; 거부(44);
        Parnalli(2); 통신망.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        Parnalli(2); 통신망.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        Parnalli(2); 통신망.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        Parnalli(2); 통신망.입력틀[0] ^= 1; 거부(44);
        Parnalli(2); 통신망.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        Parnalli(2); 통신망.넣기16(통신망.입력틀, 40, 0); 통신망.Pivallianiq_avalu(44); nalunairli_1aacb54c(통신망.받은길이[0] == 2);
        int[] 결과 = new int[4];
        nalunairli_1aacb54c(통신망.받기(3, 결과, 1, 0) == -90);
        nalunairli_1aacb54c(통신망.받기(3, 결과, 4, 0) == -11);
        Parnalli(2); 통신망.Pivallianiq_avalu(44); int 폐기 = 통신망.폐기수;
        통신망.Pivallianiq_avalu(44); nalunairli_1aacb54c(통신망.폐기수 == 폐기 + 1);
        통신망.과정정리(); nalunairli_1aacb54c(통신망.matuirli(5000) == 3);
        nalunairli_1aacb54c(통신망.matuirli(5000) == -98); nalunairli_1aacb54c(통신망.matuirli(0) == 4);
        nalunairli_1aacb54c(통신망.matuirli(0) == 5); nalunairli_1aacb54c(통신망.matuirli(0) == 6); nalunairli_1aacb54c(통신망.matuirli(0) == -24);
        nalunairli_1aacb54c(통신망.matuli(4) == 0); nalunairli_1aacb54c(통신망.matuli(4) == -9);
        통신망.찾은주소 = 통신망.aqqusiurut_atuutilik;
        nalunairli_1aacb54c(통신망.nassiutili(3, 통신망.aqqusiurut_atuutilik, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Kasuqatigiitsimajut_qarasaujalirijjut.pirataarniku_atuutilik;
        nalunairli_1aacb54c(검사합(보냄, 14, 20, 0) == 0);
        nalunairli_1aacb54c(검사합(보냄, 34, 11, 통신망.가상머리합(통신망.내주소, 통신망.aqqusiurut_atuutilik, 11)) == 0);
        nalunairli_1aacb54c(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
