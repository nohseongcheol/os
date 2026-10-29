// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** faktinis_duomenys Java sutarties_vertė 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void patvirtinti(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int kontrolinė_suma(int[] VALUE, int Paleisti, int 길이, int pradinė_būsena) {
        int SUM_VALUE = pradinė_būsena;
        for (int INDEX = 0; INDEX < 길이; INDEX++) SUM_VALUE += VALUE[Paleisti + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Parengti(int 길이) {
        tinklas_eilė.CLEAN_Procesas();
        patvirtinti(tinklas_eilė.Atverti(5000) == 3);
        int[] kadras_INDEX = tinklas_eilė.입력틀;
        Arrays.fill(kadras_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) kadras_INDEX[INDEX] = tinklas_tvarkyklė.įrenginys_ADDRESS[INDEX];
        tinklas_eilė.넣기16(kadras_INDEX, 12, 0x0800);
        kadras_INDEX[14] = 0x45; kadras_INDEX[22] = 64; kadras_INDEX[23] = 17;
        tinklas_eilė.넣기16(kadras_INDEX, 16, 28 + 길이);
        tinklas_eilė.넣기32(kadras_INDEX, 26, 0x0a000202); tinklas_eilė.넣기32(kadras_INDEX, 30, tinklas_eilė.내주소);
        tinklas_eilė.넣기16(kadras_INDEX, 34, 4321); tinklas_eilė.넣기16(kadras_INDEX, 36, 5000); tinklas_eilė.넣기16(kadras_INDEX, 38, 길이 + 8);
        for (int INDEX = 0; INDEX < 길이; INDEX++) kadras_INDEX[42 + INDEX] = INDEX & 255;
        rinkinys_kontrolinė_suma(길이);
    }
    static void rinkinys_kontrolinė_suma(int 길이) {
        int[] kadras_INDEX = tinklas_eilė.입력틀;
        tinklas_eilė.넣기16(kadras_INDEX, 24, 0); tinklas_eilė.넣기16(kadras_INDEX, 40, 0);
        tinklas_eilė.넣기16(kadras_INDEX, 24, kontrolinė_suma(kadras_INDEX, 14, 20, 0));
        int pradinė_būsena = tinklas_eilė.가상머리합(tinklas_eilė.sveikasis_skaičius_32(kadras_INDEX, 26), tinklas_eilė.내주소, 길이 + 8);
        int SUM_VALUE = kontrolinė_suma(kadras_INDEX, 34, 길이 + 8, pradinė_būsena);
        tinklas_eilė.넣기16(kadras_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void atmesti_VALUE(int 길이) { tinklas_eilė.Procesas_kadras(길이); patvirtinti(tinklas_eilė.받은길이[0] == -1); }
    public static void main(String[] Argumentai) {
        for (int 길이 : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Parengti(길이); tinklas_eilė.Procesas_kadras(길이 + 42);
            patvirtinti(tinklas_eilė.받은길이[0] == 길이);
            patvirtinti(tinklas_eilė.RECEIVED_ADDRESS[0] == 0x0a000202 && tinklas_eilė.RECEIVED_prievado_numeris[0] == 4321);
            for (int INDEX = 0; INDEX < 길이; INDEX++) patvirtinti(tinklas_eilė.RECEIVED_duomenys[INDEX] == (INDEX & 255));
        }
        for (int 길이 = 0; 길이 < 42; 길이++) { Parengti(0); atmesti_VALUE(길이); }
        Parengti(1025); atmesti_VALUE(1067);
        Parengti(2); tinklas_eilė.입력틀[24] ^= 1; atmesti_VALUE(44);
        Parengti(2); tinklas_eilė.입력틀[42] ^= 1; atmesti_VALUE(44);
        Parengti(2); tinklas_eilė.넣기16(tinklas_eilė.입력틀, 38, 7); atmesti_VALUE(44);
        Parengti(2); tinklas_eilė.넣기16(tinklas_eilė.입력틀, 38, 65535); atmesti_VALUE(44);
        Parengti(2); tinklas_eilė.입력틀[14] = 0x4f; atmesti_VALUE(44);
        Parengti(2); tinklas_eilė.입력틀[14] = 0x44; atmesti_VALUE(44);
        Parengti(2); tinklas_eilė.입력틀[20] = 0x20; rinkinys_kontrolinė_suma(2); atmesti_VALUE(44);
        Parengti(2); tinklas_eilė.입력틀[21] = 1; rinkinys_kontrolinė_suma(2); atmesti_VALUE(44);
        Parengti(2); tinklas_eilė.입력틀[33] = 99; rinkinys_kontrolinė_suma(2); atmesti_VALUE(44);
        Parengti(2); tinklas_eilė.입력틀[0] ^= 1; atmesti_VALUE(44);
        Parengti(2); tinklas_eilė.입력틀[23] = 6; rinkinys_kontrolinė_suma(2); atmesti_VALUE(44);
        Parengti(2); tinklas_eilė.넣기16(tinklas_eilė.입력틀, 40, 0); tinklas_eilė.Procesas_kadras(44); patvirtinti(tinklas_eilė.받은길이[0] == 2);
        int[] REZULTATAS = new int[4];
        patvirtinti(tinklas_eilė.gauti(3, REZULTATAS, 1, 0) == -90);
        patvirtinti(tinklas_eilė.gauti(3, REZULTATAS, 4, 0) == -11);
        Parengti(2); tinklas_eilė.Procesas_kadras(44); int atsisakyti_VALUE = tinklas_eilė.폐기수;
        tinklas_eilė.Procesas_kadras(44); patvirtinti(tinklas_eilė.폐기수 == atsisakyti_VALUE + 1);
        tinklas_eilė.CLEAN_Procesas(); patvirtinti(tinklas_eilė.Atverti(5000) == 3);
        patvirtinti(tinklas_eilė.Atverti(5000) == -98); patvirtinti(tinklas_eilė.Atverti(0) == 4);
        patvirtinti(tinklas_eilė.Atverti(0) == 5); patvirtinti(tinklas_eilė.Atverti(0) == 6); patvirtinti(tinklas_eilė.Atverti(0) == -24);
        patvirtinti(tinklas_eilė.Užverti(4) == 0); patvirtinti(tinklas_eilė.Užverti(4) == -9);
        tinklas_eilė.찾은주소 = tinklas_eilė.šliuzas_VALUE;
        patvirtinti(tinklas_eilė.siųsti(3, tinklas_eilė.šliuzas_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = tinklas_tvarkyklė.naujausia_VALUE;
        patvirtinti(kontrolinė_suma(보냄, 14, 20, 0) == 0);
        patvirtinti(kontrolinė_suma(보냄, 34, 11, tinklas_eilė.가상머리합(tinklas_eilė.내주소, tinklas_eilė.šliuzas_VALUE, 11)) == 0);
        patvirtinti(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
