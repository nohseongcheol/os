// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** tota_tshedimosetso Java konteraka_Boleng 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void netefatsa(boolean Boleng) { if (!Boleng) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] Boleng, int dirisa, int boleele_Boleng, int 초기) {
        int 합 = 초기;
        for (int tshupane = 0; tshupane < boleele_Boleng; tshupane++) 합 += Boleng[dirisa + tshupane] << ((tshupane & 1) == 0 ? 8 : 0);
        합 = (합 & 65535) + (합 >>> 16);
        합 = (합 & 65535) + (합 >>> 16);
        return ~합 & 65535;
    }
    static void Baakanya(int boleele_Boleng) {
        Neteweke_kokoanyodinepe.과정정리();
        netefatsa(Neteweke_kokoanyodinepe.bula(5000) == 3);
        int[] Foreimi_tshupane = Neteweke_kokoanyodinepe.입력틀;
        Arrays.fill(Foreimi_tshupane, 0);
        for (int tshupane = 0; tshupane < 6; tshupane++) Foreimi_tshupane[tshupane] = Neteweke_selaodi.mobaele_aterese[tshupane];
        Neteweke_kokoanyodinepe.넣기16(Foreimi_tshupane, 12, 0x0800);
        Foreimi_tshupane[14] = 0x45; Foreimi_tshupane[22] = 64; Foreimi_tshupane[23] = 17;
        Neteweke_kokoanyodinepe.넣기16(Foreimi_tshupane, 16, 28 + boleele_Boleng);
        Neteweke_kokoanyodinepe.넣기32(Foreimi_tshupane, 26, 0x0a000202); Neteweke_kokoanyodinepe.넣기32(Foreimi_tshupane, 30, Neteweke_kokoanyodinepe.내주소);
        Neteweke_kokoanyodinepe.넣기16(Foreimi_tshupane, 34, 4321); Neteweke_kokoanyodinepe.넣기16(Foreimi_tshupane, 36, 5000); Neteweke_kokoanyodinepe.넣기16(Foreimi_tshupane, 38, boleele_Boleng + 8);
        for (int tshupane = 0; tshupane < boleele_Boleng; tshupane++) Foreimi_tshupane[42 + tshupane] = tshupane & 255;
        검사합넣기(boleele_Boleng);
    }
    static void 검사합넣기(int boleele_Boleng) {
        int[] Foreimi_tshupane = Neteweke_kokoanyodinepe.입력틀;
        Neteweke_kokoanyodinepe.넣기16(Foreimi_tshupane, 24, 0); Neteweke_kokoanyodinepe.넣기16(Foreimi_tshupane, 40, 0);
        Neteweke_kokoanyodinepe.넣기16(Foreimi_tshupane, 24, 검사합(Foreimi_tshupane, 14, 20, 0));
        int 초기 = Neteweke_kokoanyodinepe.가상머리합(Neteweke_kokoanyodinepe.Palotlalo_32(Foreimi_tshupane, 26), Neteweke_kokoanyodinepe.내주소, boleele_Boleng + 8);
        int 합 = 검사합(Foreimi_tshupane, 34, boleele_Boleng + 8, 초기);
        Neteweke_kokoanyodinepe.넣기16(Foreimi_tshupane, 40, 합 == 0 ? 65535 : 합);
    }
    static void 거부(int boleele_Boleng) { Neteweke_kokoanyodinepe.Thulaganyo_Foreimi(boleele_Boleng); netefatsa(Neteweke_kokoanyodinepe.받은길이[0] == -1); }
    public static void main(String[] 인수) {
        for (int boleele_Boleng : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Baakanya(boleele_Boleng); Neteweke_kokoanyodinepe.Thulaganyo_Foreimi(boleele_Boleng + 42);
            netefatsa(Neteweke_kokoanyodinepe.받은길이[0] == boleele_Boleng);
            netefatsa(Neteweke_kokoanyodinepe.받은주소[0] == 0x0a000202 && Neteweke_kokoanyodinepe.받은접속번호[0] == 4321);
            for (int tshupane = 0; tshupane < boleele_Boleng; tshupane++) netefatsa(Neteweke_kokoanyodinepe.받은자료[tshupane] == (tshupane & 255));
        }
        for (int boleele_Boleng = 0; boleele_Boleng < 42; boleele_Boleng++) { Baakanya(0); 거부(boleele_Boleng); }
        Baakanya(1025); 거부(1067);
        Baakanya(2); Neteweke_kokoanyodinepe.입력틀[24] ^= 1; 거부(44);
        Baakanya(2); Neteweke_kokoanyodinepe.입력틀[42] ^= 1; 거부(44);
        Baakanya(2); Neteweke_kokoanyodinepe.넣기16(Neteweke_kokoanyodinepe.입력틀, 38, 7); 거부(44);
        Baakanya(2); Neteweke_kokoanyodinepe.넣기16(Neteweke_kokoanyodinepe.입력틀, 38, 65535); 거부(44);
        Baakanya(2); Neteweke_kokoanyodinepe.입력틀[14] = 0x4f; 거부(44);
        Baakanya(2); Neteweke_kokoanyodinepe.입력틀[14] = 0x44; 거부(44);
        Baakanya(2); Neteweke_kokoanyodinepe.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        Baakanya(2); Neteweke_kokoanyodinepe.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        Baakanya(2); Neteweke_kokoanyodinepe.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        Baakanya(2); Neteweke_kokoanyodinepe.입력틀[0] ^= 1; 거부(44);
        Baakanya(2); Neteweke_kokoanyodinepe.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        Baakanya(2); Neteweke_kokoanyodinepe.넣기16(Neteweke_kokoanyodinepe.입력틀, 40, 0); Neteweke_kokoanyodinepe.Thulaganyo_Foreimi(44); netefatsa(Neteweke_kokoanyodinepe.받은길이[0] == 2);
        int[] 결과 = new int[4];
        netefatsa(Neteweke_kokoanyodinepe.받기(3, 결과, 1, 0) == -90);
        netefatsa(Neteweke_kokoanyodinepe.받기(3, 결과, 4, 0) == -11);
        Baakanya(2); Neteweke_kokoanyodinepe.Thulaganyo_Foreimi(44); int latlha_Boleng = Neteweke_kokoanyodinepe.폐기수;
        Neteweke_kokoanyodinepe.Thulaganyo_Foreimi(44); netefatsa(Neteweke_kokoanyodinepe.폐기수 == latlha_Boleng + 1);
        Neteweke_kokoanyodinepe.과정정리(); netefatsa(Neteweke_kokoanyodinepe.bula(5000) == 3);
        netefatsa(Neteweke_kokoanyodinepe.bula(5000) == -98); netefatsa(Neteweke_kokoanyodinepe.bula(0) == 4);
        netefatsa(Neteweke_kokoanyodinepe.bula(0) == 5); netefatsa(Neteweke_kokoanyodinepe.bula(0) == 6); netefatsa(Neteweke_kokoanyodinepe.bula(0) == -24);
        netefatsa(Neteweke_kokoanyodinepe.tswala(4) == 0); netefatsa(Neteweke_kokoanyodinepe.tswala(4) == -9);
        Neteweke_kokoanyodinepe.찾은주소 = Neteweke_kokoanyodinepe.kgorotsamaiso_Boleng;
        netefatsa(Neteweke_kokoanyodinepe.romela(3, Neteweke_kokoanyodinepe.kgorotsamaiso_Boleng, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Neteweke_selaodi.bošhweng_Boleng;
        netefatsa(검사합(보냄, 14, 20, 0) == 0);
        netefatsa(검사합(보냄, 34, 11, Neteweke_kokoanyodinepe.가상머리합(Neteweke_kokoanyodinepe.내주소, Neteweke_kokoanyodinepe.kgorotsamaiso_Boleng, 11)) == 0);
        netefatsa(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
