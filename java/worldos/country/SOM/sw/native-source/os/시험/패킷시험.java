// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** halisi_data Java Kazi_thamani 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void thibitisha(boolean thamani) { if (!thamani) throw new AssertionError("case " + 횟수); 횟수++; }
    static int jumla(int[] thamani, int endesha, int urefu_thamani, int 초기) {
        int 합 = 초기;
        for (int kielezo = 0; kielezo < urefu_thamani; kielezo++) 합 += thamani[endesha + kielezo] << ((kielezo & 1) == 0 ? 8 : 0);
        합 = (합 & 65535) + (합 >>> 16);
        합 = (합 & 65535) + (합 >>> 16);
        return ~합 & 65535;
    }
    static void Andaa(int urefu_thamani) {
        Mtandao_Mpororo.Safi_Mchakato();
        thibitisha(Mtandao_Mpororo.unda(5000) == 3);
        int[] fremu_kielezo = Mtandao_Mpororo.입력틀;
        Arrays.fill(fremu_kielezo, 0);
        for (int kielezo = 0; kielezo < 6; kielezo++) fremu_kielezo[kielezo] = Mtandao_kiendeshaji.kifaa_anwani[kielezo];
        Mtandao_Mpororo.넣기16(fremu_kielezo, 12, 0x0800);
        fremu_kielezo[14] = 0x45; fremu_kielezo[22] = 64; fremu_kielezo[23] = 17;
        Mtandao_Mpororo.넣기16(fremu_kielezo, 16, 28 + urefu_thamani);
        Mtandao_Mpororo.넣기32(fremu_kielezo, 26, 0x0a000202); Mtandao_Mpororo.넣기32(fremu_kielezo, 30, Mtandao_Mpororo.내주소);
        Mtandao_Mpororo.넣기16(fremu_kielezo, 34, 4321); Mtandao_Mpororo.넣기16(fremu_kielezo, 36, 5000); Mtandao_Mpororo.넣기16(fremu_kielezo, 38, urefu_thamani + 8);
        for (int kielezo = 0; kielezo < urefu_thamani; kielezo++) fremu_kielezo[42 + kielezo] = kielezo & 255;
        seti_jumla(urefu_thamani);
    }
    static void seti_jumla(int urefu_thamani) {
        int[] fremu_kielezo = Mtandao_Mpororo.입력틀;
        Mtandao_Mpororo.넣기16(fremu_kielezo, 24, 0); Mtandao_Mpororo.넣기16(fremu_kielezo, 40, 0);
        Mtandao_Mpororo.넣기16(fremu_kielezo, 24, jumla(fremu_kielezo, 14, 20, 0));
        int 초기 = Mtandao_Mpororo.가상머리합(Mtandao_Mpororo.namba_kamili_32(fremu_kielezo, 26), Mtandao_Mpororo.내주소, urefu_thamani + 8);
        int 합 = jumla(fremu_kielezo, 34, urefu_thamani + 8, 초기);
        Mtandao_Mpororo.넣기16(fremu_kielezo, 40, 합 == 0 ? 65535 : 합);
    }
    static void kataa_thamani(int urefu_thamani) { Mtandao_Mpororo.Mchakato_fremu(urefu_thamani); thibitisha(Mtandao_Mpororo.받은길이[0] == -1); }
    public static void main(String[] 인수) {
        for (int urefu_thamani : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Andaa(urefu_thamani); Mtandao_Mpororo.Mchakato_fremu(urefu_thamani + 42);
            thibitisha(Mtandao_Mpororo.받은길이[0] == urefu_thamani);
            thibitisha(Mtandao_Mpororo.받은주소[0] == 0x0a000202 && Mtandao_Mpororo.받은접속번호[0] == 4321);
            for (int kielezo = 0; kielezo < urefu_thamani; kielezo++) thibitisha(Mtandao_Mpororo.받은자료[kielezo] == (kielezo & 255));
        }
        for (int urefu_thamani = 0; urefu_thamani < 42; urefu_thamani++) { Andaa(0); kataa_thamani(urefu_thamani); }
        Andaa(1025); kataa_thamani(1067);
        Andaa(2); Mtandao_Mpororo.입력틀[24] ^= 1; kataa_thamani(44);
        Andaa(2); Mtandao_Mpororo.입력틀[42] ^= 1; kataa_thamani(44);
        Andaa(2); Mtandao_Mpororo.넣기16(Mtandao_Mpororo.입력틀, 38, 7); kataa_thamani(44);
        Andaa(2); Mtandao_Mpororo.넣기16(Mtandao_Mpororo.입력틀, 38, 65535); kataa_thamani(44);
        Andaa(2); Mtandao_Mpororo.입력틀[14] = 0x4f; kataa_thamani(44);
        Andaa(2); Mtandao_Mpororo.입력틀[14] = 0x44; kataa_thamani(44);
        Andaa(2); Mtandao_Mpororo.입력틀[20] = 0x20; seti_jumla(2); kataa_thamani(44);
        Andaa(2); Mtandao_Mpororo.입력틀[21] = 1; seti_jumla(2); kataa_thamani(44);
        Andaa(2); Mtandao_Mpororo.입력틀[33] = 99; seti_jumla(2); kataa_thamani(44);
        Andaa(2); Mtandao_Mpororo.입력틀[0] ^= 1; kataa_thamani(44);
        Andaa(2); Mtandao_Mpororo.입력틀[23] = 6; seti_jumla(2); kataa_thamani(44);
        Andaa(2); Mtandao_Mpororo.넣기16(Mtandao_Mpororo.입력틀, 40, 0); Mtandao_Mpororo.Mchakato_fremu(44); thibitisha(Mtandao_Mpororo.받은길이[0] == 2);
        int[] 결과 = new int[4];
        thibitisha(Mtandao_Mpororo.받기(3, 결과, 1, 0) == -90);
        thibitisha(Mtandao_Mpororo.받기(3, 결과, 4, 0) == -11);
        Andaa(2); Mtandao_Mpororo.Mchakato_fremu(44); int puuza_thamani = Mtandao_Mpororo.폐기수;
        Mtandao_Mpororo.Mchakato_fremu(44); thibitisha(Mtandao_Mpororo.폐기수 == puuza_thamani + 1);
        Mtandao_Mpororo.Safi_Mchakato(); thibitisha(Mtandao_Mpororo.unda(5000) == 3);
        thibitisha(Mtandao_Mpororo.unda(5000) == -98); thibitisha(Mtandao_Mpororo.unda(0) == 4);
        thibitisha(Mtandao_Mpororo.unda(0) == 5); thibitisha(Mtandao_Mpororo.unda(0) == 6); thibitisha(Mtandao_Mpororo.unda(0) == -24);
        thibitisha(Mtandao_Mpororo.funga(4) == 0); thibitisha(Mtandao_Mpororo.funga(4) == -9);
        Mtandao_Mpororo.찾은주소 = Mtandao_Mpororo.kichanganishi_mtandao_thamani;
        thibitisha(Mtandao_Mpororo.tuma(3, Mtandao_Mpororo.kichanganishi_mtandao_thamani, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Mtandao_kiendeshaji.hivi_karibuni_thamani;
        thibitisha(jumla(보냄, 14, 20, 0) == 0);
        thibitisha(jumla(보냄, 34, 11, Mtandao_Mpororo.가상머리합(Mtandao_Mpororo.내주소, Mtandao_Mpororo.kichanganishi_mtandao_thamani, 11)) == 0);
        thibitisha(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
