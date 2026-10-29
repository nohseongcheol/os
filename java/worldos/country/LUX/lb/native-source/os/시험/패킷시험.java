// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** aktuell_Daten Java Job_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void verifizéieren(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] VALUE, int Laf, int Längt_VALUE, int 초기) {
        int SUM_VALUE = 초기;
        for (int INDEX = 0; INDEX < Längt_VALUE; INDEX++) SUM_VALUE += VALUE[Laf + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Préparéieren(int Längt_VALUE) {
        Reseau_Stapel.CLEAN_Prozess();
        verifizéieren(Reseau_Stapel.ariichten(5000) == 3);
        int[] Rumm_INDEX = Reseau_Stapel.입력틀;
        Arrays.fill(Rumm_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) Rumm_INDEX[INDEX] = Reseau_Driver.Mobil_Adress[INDEX];
        Reseau_Stapel.넣기16(Rumm_INDEX, 12, 0x0800);
        Rumm_INDEX[14] = 0x45; Rumm_INDEX[22] = 64; Rumm_INDEX[23] = 17;
        Reseau_Stapel.넣기16(Rumm_INDEX, 16, 28 + Längt_VALUE);
        Reseau_Stapel.넣기32(Rumm_INDEX, 26, 0x0a000202); Reseau_Stapel.넣기32(Rumm_INDEX, 30, Reseau_Stapel.내주소);
        Reseau_Stapel.넣기16(Rumm_INDEX, 34, 4321); Reseau_Stapel.넣기16(Rumm_INDEX, 36, 5000); Reseau_Stapel.넣기16(Rumm_INDEX, 38, Längt_VALUE + 8);
        for (int INDEX = 0; INDEX < Längt_VALUE; INDEX++) Rumm_INDEX[42 + INDEX] = INDEX & 255;
        검사합넣기(Längt_VALUE);
    }
    static void 검사합넣기(int Längt_VALUE) {
        int[] Rumm_INDEX = Reseau_Stapel.입력틀;
        Reseau_Stapel.넣기16(Rumm_INDEX, 24, 0); Reseau_Stapel.넣기16(Rumm_INDEX, 40, 0);
        Reseau_Stapel.넣기16(Rumm_INDEX, 24, 검사합(Rumm_INDEX, 14, 20, 0));
        int 초기 = Reseau_Stapel.가상머리합(Reseau_Stapel.Ganzzuel_32(Rumm_INDEX, 26), Reseau_Stapel.내주소, Längt_VALUE + 8);
        int SUM_VALUE = 검사합(Rumm_INDEX, 34, Längt_VALUE + 8, 초기);
        Reseau_Stapel.넣기16(Rumm_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void 거부(int Längt_VALUE) { Reseau_Stapel.Prozess_Rumm(Längt_VALUE); verifizéieren(Reseau_Stapel.RECEIVED_Längt[0] == -1); }
    public static void main(String[] 인수) {
        for (int Längt_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Préparéieren(Längt_VALUE); Reseau_Stapel.Prozess_Rumm(Längt_VALUE + 42);
            verifizéieren(Reseau_Stapel.RECEIVED_Längt[0] == Längt_VALUE);
            verifizéieren(Reseau_Stapel.RECEIVED_Adress[0] == 0x0a000202 && Reseau_Stapel.받은접속번호[0] == 4321);
            for (int INDEX = 0; INDEX < Längt_VALUE; INDEX++) verifizéieren(Reseau_Stapel.RECEIVED_Daten[INDEX] == (INDEX & 255));
        }
        for (int Längt_VALUE = 0; Längt_VALUE < 42; Längt_VALUE++) { Préparéieren(0); 거부(Längt_VALUE); }
        Préparéieren(1025); 거부(1067);
        Préparéieren(2); Reseau_Stapel.입력틀[24] ^= 1; 거부(44);
        Préparéieren(2); Reseau_Stapel.입력틀[42] ^= 1; 거부(44);
        Préparéieren(2); Reseau_Stapel.넣기16(Reseau_Stapel.입력틀, 38, 7); 거부(44);
        Préparéieren(2); Reseau_Stapel.넣기16(Reseau_Stapel.입력틀, 38, 65535); 거부(44);
        Préparéieren(2); Reseau_Stapel.입력틀[14] = 0x4f; 거부(44);
        Préparéieren(2); Reseau_Stapel.입력틀[14] = 0x44; 거부(44);
        Préparéieren(2); Reseau_Stapel.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        Préparéieren(2); Reseau_Stapel.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        Préparéieren(2); Reseau_Stapel.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        Préparéieren(2); Reseau_Stapel.입력틀[0] ^= 1; 거부(44);
        Préparéieren(2); Reseau_Stapel.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        Préparéieren(2); Reseau_Stapel.넣기16(Reseau_Stapel.입력틀, 40, 0); Reseau_Stapel.Prozess_Rumm(44); verifizéieren(Reseau_Stapel.RECEIVED_Längt[0] == 2);
        int[] Mooss = new int[4];
        verifizéieren(Reseau_Stapel.받기(3, Mooss, 1, 0) == -90);
        verifizéieren(Reseau_Stapel.받기(3, Mooss, 4, 0) == -11);
        Préparéieren(2); Reseau_Stapel.Prozess_Rumm(44); int verwerfen_VALUE = Reseau_Stapel.폐기수;
        Reseau_Stapel.Prozess_Rumm(44); verifizéieren(Reseau_Stapel.폐기수 == verwerfen_VALUE + 1);
        Reseau_Stapel.CLEAN_Prozess(); verifizéieren(Reseau_Stapel.ariichten(5000) == 3);
        verifizéieren(Reseau_Stapel.ariichten(5000) == -98); verifizéieren(Reseau_Stapel.ariichten(0) == 4);
        verifizéieren(Reseau_Stapel.ariichten(0) == 5); verifizéieren(Reseau_Stapel.ariichten(0) == 6); verifizéieren(Reseau_Stapel.ariichten(0) == -24);
        verifizéieren(Reseau_Stapel.Clôture(4) == 0); verifizéieren(Reseau_Stapel.Clôture(4) == -9);
        Reseau_Stapel.찾은주소 = Reseau_Stapel.Gateway_VALUE;
        verifizéieren(Reseau_Stapel.mailen(3, Reseau_Stapel.Gateway_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Reseau_Driver.rezent_VALUE;
        verifizéieren(검사합(보냄, 14, 20, 0) == 0);
        verifizéieren(검사합(보냄, 34, 11, Reseau_Stapel.가상머리합(Reseau_Stapel.내주소, Reseau_Stapel.Gateway_VALUE, 11)) == 0);
        verifizéieren(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
