// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** Na_hakika_Tarin_bayani Java Kes_Daraja 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void Tabbatar_da(boolean Daraja) { if (!Daraja) throw new AssertionError("case " + 횟수); 횟수++; }
    static int checksum(int[] Daraja, int Tafiyar_da, int Tsawo_Daraja, int 초기) {
        int 합 = 초기;
        for (int Indes = 0; Indes < Tsawo_Daraja; Indes++) 합 += Daraja[Tafiyar_da + Indes] << ((Indes & 1) == 0 ? 8 : 0);
        합 = (합 & 65535) + (합 >>> 16);
        합 = (합 & 65535) + (합 >>> 16);
        return ~합 & 65535;
    }
    static void Shirya(int Tsawo_Daraja) {
        Hanyar_sadarwa_tara.과정정리();
        Tabbatar_da(Hanyar_sadarwa_tara.Buɗe(5000) == 3);
        int[] allo_Indes = Hanyar_sadarwa_tara.입력틀;
        Arrays.fill(allo_Indes, 0);
        for (int Indes = 0; Indes < 6; Indes++) allo_Indes[Indes] = Hanyar_sadarwa_diraiba.na_ura_imel[Indes];
        Hanyar_sadarwa_tara.넣기16(allo_Indes, 12, 0x0800);
        allo_Indes[14] = 0x45; allo_Indes[22] = 64; allo_Indes[23] = 17;
        Hanyar_sadarwa_tara.넣기16(allo_Indes, 16, 28 + Tsawo_Daraja);
        Hanyar_sadarwa_tara.넣기32(allo_Indes, 26, 0x0a000202); Hanyar_sadarwa_tara.넣기32(allo_Indes, 30, Hanyar_sadarwa_tara.내주소);
        Hanyar_sadarwa_tara.넣기16(allo_Indes, 34, 4321); Hanyar_sadarwa_tara.넣기16(allo_Indes, 36, 5000); Hanyar_sadarwa_tara.넣기16(allo_Indes, 38, Tsawo_Daraja + 8);
        for (int Indes = 0; Indes < Tsawo_Daraja; Indes++) allo_Indes[42 + Indes] = Indes & 255;
        zubi_checksum(Tsawo_Daraja);
    }
    static void zubi_checksum(int Tsawo_Daraja) {
        int[] allo_Indes = Hanyar_sadarwa_tara.입력틀;
        Hanyar_sadarwa_tara.넣기16(allo_Indes, 24, 0); Hanyar_sadarwa_tara.넣기16(allo_Indes, 40, 0);
        Hanyar_sadarwa_tara.넣기16(allo_Indes, 24, checksum(allo_Indes, 14, 20, 0));
        int 초기 = Hanyar_sadarwa_tara.가상머리합(Hanyar_sadarwa_tara.Lamba_mara_32(allo_Indes, 26), Hanyar_sadarwa_tara.내주소, Tsawo_Daraja + 8);
        int 합 = checksum(allo_Indes, 34, Tsawo_Daraja + 8, 초기);
        Hanyar_sadarwa_tara.넣기16(allo_Indes, 40, 합 == 0 ? 65535 : 합);
    }
    static void kore_Daraja(int Tsawo_Daraja) { Hanyar_sadarwa_tara.haryar_aikin_na_ura_allo(Tsawo_Daraja); Tabbatar_da(Hanyar_sadarwa_tara.받은길이[0] == -1); }
    public static void main(String[] 인수) {
        for (int Tsawo_Daraja : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Shirya(Tsawo_Daraja); Hanyar_sadarwa_tara.haryar_aikin_na_ura_allo(Tsawo_Daraja + 42);
            Tabbatar_da(Hanyar_sadarwa_tara.받은길이[0] == Tsawo_Daraja);
            Tabbatar_da(Hanyar_sadarwa_tara.받은주소[0] == 0x0a000202 && Hanyar_sadarwa_tara.받은접속번호[0] == 4321);
            for (int Indes = 0; Indes < Tsawo_Daraja; Indes++) Tabbatar_da(Hanyar_sadarwa_tara.받은자료[Indes] == (Indes & 255));
        }
        for (int Tsawo_Daraja = 0; Tsawo_Daraja < 42; Tsawo_Daraja++) { Shirya(0); kore_Daraja(Tsawo_Daraja); }
        Shirya(1025); kore_Daraja(1067);
        Shirya(2); Hanyar_sadarwa_tara.입력틀[24] ^= 1; kore_Daraja(44);
        Shirya(2); Hanyar_sadarwa_tara.입력틀[42] ^= 1; kore_Daraja(44);
        Shirya(2); Hanyar_sadarwa_tara.넣기16(Hanyar_sadarwa_tara.입력틀, 38, 7); kore_Daraja(44);
        Shirya(2); Hanyar_sadarwa_tara.넣기16(Hanyar_sadarwa_tara.입력틀, 38, 65535); kore_Daraja(44);
        Shirya(2); Hanyar_sadarwa_tara.입력틀[14] = 0x4f; kore_Daraja(44);
        Shirya(2); Hanyar_sadarwa_tara.입력틀[14] = 0x44; kore_Daraja(44);
        Shirya(2); Hanyar_sadarwa_tara.입력틀[20] = 0x20; zubi_checksum(2); kore_Daraja(44);
        Shirya(2); Hanyar_sadarwa_tara.입력틀[21] = 1; zubi_checksum(2); kore_Daraja(44);
        Shirya(2); Hanyar_sadarwa_tara.입력틀[33] = 99; zubi_checksum(2); kore_Daraja(44);
        Shirya(2); Hanyar_sadarwa_tara.입력틀[0] ^= 1; kore_Daraja(44);
        Shirya(2); Hanyar_sadarwa_tara.입력틀[23] = 6; zubi_checksum(2); kore_Daraja(44);
        Shirya(2); Hanyar_sadarwa_tara.넣기16(Hanyar_sadarwa_tara.입력틀, 40, 0); Hanyar_sadarwa_tara.haryar_aikin_na_ura_allo(44); Tabbatar_da(Hanyar_sadarwa_tara.받은길이[0] == 2);
        int[] 결과 = new int[4];
        Tabbatar_da(Hanyar_sadarwa_tara.받기(3, 결과, 1, 0) == -90);
        Tabbatar_da(Hanyar_sadarwa_tara.받기(3, 결과, 4, 0) == -11);
        Shirya(2); Hanyar_sadarwa_tara.haryar_aikin_na_ura_allo(44); int watsar_Daraja = Hanyar_sadarwa_tara.폐기수;
        Hanyar_sadarwa_tara.haryar_aikin_na_ura_allo(44); Tabbatar_da(Hanyar_sadarwa_tara.폐기수 == watsar_Daraja + 1);
        Hanyar_sadarwa_tara.과정정리(); Tabbatar_da(Hanyar_sadarwa_tara.Buɗe(5000) == 3);
        Tabbatar_da(Hanyar_sadarwa_tara.Buɗe(5000) == -98); Tabbatar_da(Hanyar_sadarwa_tara.Buɗe(0) == 4);
        Tabbatar_da(Hanyar_sadarwa_tara.Buɗe(0) == 5); Tabbatar_da(Hanyar_sadarwa_tara.Buɗe(0) == 6); Tabbatar_da(Hanyar_sadarwa_tara.Buɗe(0) == -24);
        Tabbatar_da(Hanyar_sadarwa_tara.Rufe(4) == 0); Tabbatar_da(Hanyar_sadarwa_tara.Rufe(4) == -9);
        Hanyar_sadarwa_tara.찾은주소 = Hanyar_sadarwa_tara.Mashiga_Daraja;
        Tabbatar_da(Hanyar_sadarwa_tara.Aika(3, Hanyar_sadarwa_tara.Mashiga_Daraja, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Hanyar_sadarwa_diraiba.na_kwanan_nan_Daraja;
        Tabbatar_da(checksum(보냄, 14, 20, 0) == 0);
        Tabbatar_da(checksum(보냄, 34, 11, Hanyar_sadarwa_tara.가상머리합(Hanyar_sadarwa_tara.내주소, Hanyar_sadarwa_tara.Mashiga_Daraja, 11)) == 0);
        Tabbatar_da(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
