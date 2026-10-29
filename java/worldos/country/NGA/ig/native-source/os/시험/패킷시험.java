// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** ǹdịnezie_datà Java ngō_valuu 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void nkwàdo_eziokwū(boolean valuu) { if (!valuu) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] valuu, int Bido, int ogologo_valuu, int 초기) {
        int 합 = 초기;
        for (int indèks = 0; indèks < ogologo_valuu; indèks++) 합 += valuu[Bido + indèks] << ((indèks & 1) == 0 ? 8 : 0);
        합 = (합 & 65535) + (합 >>> 16);
        합 = (합 & 65535) + (합 >>> 16);
        return ~합 & 65535;
    }
    static void Kwado(int ogologo_valuu) {
        Netwọọkụ_ikpo.과정정리();
        nkwàdo_eziokwū(Netwọọkụ_ikpo.Mepee(5000) == 3);
        int[] okpokoro_indèks = Netwọọkụ_ikpo.입력틀;
        Arrays.fill(okpokoro_indèks, 0);
        for (int indèks = 0; indèks < 6; indèks++) okpokoro_indèks[indèks] = Netwọọkụ_ǹnyà.njìarụ_àdreèsì[indèks];
        Netwọọkụ_ikpo.넣기16(okpokoro_indèks, 12, 0x0800);
        okpokoro_indèks[14] = 0x45; okpokoro_indèks[22] = 64; okpokoro_indèks[23] = 17;
        Netwọọkụ_ikpo.넣기16(okpokoro_indèks, 16, 28 + ogologo_valuu);
        Netwọọkụ_ikpo.넣기32(okpokoro_indèks, 26, 0x0a000202); Netwọọkụ_ikpo.넣기32(okpokoro_indèks, 30, Netwọọkụ_ikpo.내주소);
        Netwọọkụ_ikpo.넣기16(okpokoro_indèks, 34, 4321); Netwọọkụ_ikpo.넣기16(okpokoro_indèks, 36, 5000); Netwọọkụ_ikpo.넣기16(okpokoro_indèks, 38, ogologo_valuu + 8);
        for (int indèks = 0; indèks < ogologo_valuu; indèks++) okpokoro_indèks[42 + indèks] = indèks & 255;
        검사합넣기(ogologo_valuu);
    }
    static void 검사합넣기(int ogologo_valuu) {
        int[] okpokoro_indèks = Netwọọkụ_ikpo.입력틀;
        Netwọọkụ_ikpo.넣기16(okpokoro_indèks, 24, 0); Netwọọkụ_ikpo.넣기16(okpokoro_indèks, 40, 0);
        Netwọọkụ_ikpo.넣기16(okpokoro_indèks, 24, 검사합(okpokoro_indèks, 14, 20, 0));
        int 초기 = Netwọọkụ_ikpo.가상머리합(Netwọọkụ_ikpo.ọnụọgụ_nzùrùòkè_32(okpokoro_indèks, 26), Netwọọkụ_ikpo.내주소, ogologo_valuu + 8);
        int 합 = 검사합(okpokoro_indèks, 34, ogologo_valuu + 8, 초기);
        Netwọọkụ_ikpo.넣기16(okpokoro_indèks, 40, 합 == 0 ? 65535 : 합);
    }
    static void 거부(int ogologo_valuu) { Netwọọkụ_ikpo.ùsòrò_okpokoro(ogologo_valuu); nkwàdo_eziokwū(Netwọọkụ_ikpo.받은길이[0] == -1); }
    public static void main(String[] 인수) {
        for (int ogologo_valuu : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Kwado(ogologo_valuu); Netwọọkụ_ikpo.ùsòrò_okpokoro(ogologo_valuu + 42);
            nkwàdo_eziokwū(Netwọọkụ_ikpo.받은길이[0] == ogologo_valuu);
            nkwàdo_eziokwū(Netwọọkụ_ikpo.받은주소[0] == 0x0a000202 && Netwọọkụ_ikpo.받은접속번호[0] == 4321);
            for (int indèks = 0; indèks < ogologo_valuu; indèks++) nkwàdo_eziokwū(Netwọọkụ_ikpo.받은자료[indèks] == (indèks & 255));
        }
        for (int ogologo_valuu = 0; ogologo_valuu < 42; ogologo_valuu++) { Kwado(0); 거부(ogologo_valuu); }
        Kwado(1025); 거부(1067);
        Kwado(2); Netwọọkụ_ikpo.입력틀[24] ^= 1; 거부(44);
        Kwado(2); Netwọọkụ_ikpo.입력틀[42] ^= 1; 거부(44);
        Kwado(2); Netwọọkụ_ikpo.넣기16(Netwọọkụ_ikpo.입력틀, 38, 7); 거부(44);
        Kwado(2); Netwọọkụ_ikpo.넣기16(Netwọọkụ_ikpo.입력틀, 38, 65535); 거부(44);
        Kwado(2); Netwọọkụ_ikpo.입력틀[14] = 0x4f; 거부(44);
        Kwado(2); Netwọọkụ_ikpo.입력틀[14] = 0x44; 거부(44);
        Kwado(2); Netwọọkụ_ikpo.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        Kwado(2); Netwọọkụ_ikpo.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        Kwado(2); Netwọọkụ_ikpo.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        Kwado(2); Netwọọkụ_ikpo.입력틀[0] ^= 1; 거부(44);
        Kwado(2); Netwọọkụ_ikpo.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        Kwado(2); Netwọọkụ_ikpo.넣기16(Netwọọkụ_ikpo.입력틀, 40, 0); Netwọọkụ_ikpo.ùsòrò_okpokoro(44); nkwàdo_eziokwū(Netwọọkụ_ikpo.받은길이[0] == 2);
        int[] 결과 = new int[4];
        nkwàdo_eziokwū(Netwọọkụ_ikpo.받기(3, 결과, 1, 0) == -90);
        nkwàdo_eziokwū(Netwọọkụ_ikpo.받기(3, 결과, 4, 0) == -11);
        Kwado(2); Netwọọkụ_ikpo.ùsòrò_okpokoro(44); int tufuo_valuu = Netwọọkụ_ikpo.폐기수;
        Netwọọkụ_ikpo.ùsòrò_okpokoro(44); nkwàdo_eziokwū(Netwọọkụ_ikpo.폐기수 == tufuo_valuu + 1);
        Netwọọkụ_ikpo.과정정리(); nkwàdo_eziokwū(Netwọọkụ_ikpo.Mepee(5000) == 3);
        nkwàdo_eziokwū(Netwọọkụ_ikpo.Mepee(5000) == -98); nkwàdo_eziokwū(Netwọọkụ_ikpo.Mepee(0) == 4);
        nkwàdo_eziokwū(Netwọọkụ_ikpo.Mepee(0) == 5); nkwàdo_eziokwū(Netwọọkụ_ikpo.Mepee(0) == 6); nkwàdo_eziokwū(Netwọọkụ_ikpo.Mepee(0) == -24);
        nkwàdo_eziokwū(Netwọọkụ_ikpo.Mechie(4) == 0); nkwàdo_eziokwū(Netwọọkụ_ikpo.Mechie(4) == -9);
        Netwọọkụ_ikpo.찾은주소 = Netwọọkụ_ikpo.ụzọmbànye_valuu;
        nkwàdo_eziokwū(Netwọọkụ_ikpo.zìga(3, Netwọọkụ_ikpo.ụzọmbànye_valuu, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Netwọọkụ_ǹnyà.dị_nsonso_valuu;
        nkwàdo_eziokwū(검사합(보냄, 14, 20, 0) == 0);
        nkwàdo_eziokwū(검사합(보냄, 34, 11, Netwọọkụ_ikpo.가상머리합(Netwọọkụ_ikpo.내주소, Netwọọkụ_ikpo.ụzọmbànye_valuu, 11)) == 0);
        nkwàdo_eziokwū(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
