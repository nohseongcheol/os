// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** skutočný_údaje Java prípad_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class paket_test {
    static int 횟수 = 0;
    static void overiť(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int kontrolný_súčet(int[] VALUE, int Spustiť_2, int dĺžka_VALUE, int počiatočný_stav) {
        int SUM_VALUE = počiatočný_stav;
        for (int INDEX = 0; INDEX < dĺžka_VALUE; INDEX++) SUM_VALUE += VALUE[Spustiť_2 + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Pripraviť(int dĺžka_VALUE) {
        sieť_Vrstvy.CLEAN_Proces();
        overiť(sieť_Vrstvy.Otvoriť(5000) == 3);
        int[] rám_INDEX = sieť_Vrstvy.vstup_rám;
        Arrays.fill(rám_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) rám_INDEX[INDEX] = sieť_ovládač.telefón_adresa[INDEX];
        sieť_Vrstvy.넣기16(rám_INDEX, 12, 0x0800);
        rám_INDEX[14] = 0x45; rám_INDEX[22] = 64; rám_INDEX[23] = 17;
        sieť_Vrstvy.넣기16(rám_INDEX, 16, 28 + dĺžka_VALUE);
        sieť_Vrstvy.넣기32(rám_INDEX, 26, 0x0a000202); sieť_Vrstvy.넣기32(rám_INDEX, 30, sieť_Vrstvy.내주소);
        sieť_Vrstvy.넣기16(rám_INDEX, 34, 4321); sieť_Vrstvy.넣기16(rám_INDEX, 36, 5000); sieť_Vrstvy.넣기16(rám_INDEX, 38, dĺžka_VALUE + 8);
        for (int INDEX = 0; INDEX < dĺžka_VALUE; INDEX++) rám_INDEX[42 + INDEX] = INDEX & 255;
        množina_kontrolný_súčet(dĺžka_VALUE);
    }
    static void množina_kontrolný_súčet(int dĺžka_VALUE) {
        int[] rám_INDEX = sieť_Vrstvy.vstup_rám;
        sieť_Vrstvy.넣기16(rám_INDEX, 24, 0); sieť_Vrstvy.넣기16(rám_INDEX, 40, 0);
        sieť_Vrstvy.넣기16(rám_INDEX, 24, kontrolný_súčet(rám_INDEX, 14, 20, 0));
        int počiatočný_stav = sieť_Vrstvy.가상머리합(sieť_Vrstvy.celé_číslo_32(rám_INDEX, 26), sieť_Vrstvy.내주소, dĺžka_VALUE + 8);
        int SUM_VALUE = kontrolný_súčet(rám_INDEX, 34, dĺžka_VALUE + 8, počiatočný_stav);
        sieť_Vrstvy.넣기16(rám_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void odmietnuť_VALUE(int dĺžka_VALUE) { sieť_Vrstvy.Proces_rám(dĺžka_VALUE); overiť(sieť_Vrstvy.RECEIVED_dĺžka[0] == -1); }
    public static void main(String[] Argumenty) {
        for (int dĺžka_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Pripraviť(dĺžka_VALUE); sieť_Vrstvy.Proces_rám(dĺžka_VALUE + 42);
            overiť(sieť_Vrstvy.RECEIVED_dĺžka[0] == dĺžka_VALUE);
            overiť(sieť_Vrstvy.RECEIVED_adresa[0] == 0x0a000202 && sieť_Vrstvy.RECEIVED_číslo_portu[0] == 4321);
            for (int INDEX = 0; INDEX < dĺžka_VALUE; INDEX++) overiť(sieť_Vrstvy.RECEIVED_údaje[INDEX] == (INDEX & 255));
        }
        for (int dĺžka_VALUE = 0; dĺžka_VALUE < 42; dĺžka_VALUE++) { Pripraviť(0); odmietnuť_VALUE(dĺžka_VALUE); }
        Pripraviť(1025); odmietnuť_VALUE(1067);
        Pripraviť(2); sieť_Vrstvy.vstup_rám[24] ^= 1; odmietnuť_VALUE(44);
        Pripraviť(2); sieť_Vrstvy.vstup_rám[42] ^= 1; odmietnuť_VALUE(44);
        Pripraviť(2); sieť_Vrstvy.넣기16(sieť_Vrstvy.vstup_rám, 38, 7); odmietnuť_VALUE(44);
        Pripraviť(2); sieť_Vrstvy.넣기16(sieť_Vrstvy.vstup_rám, 38, 65535); odmietnuť_VALUE(44);
        Pripraviť(2); sieť_Vrstvy.vstup_rám[14] = 0x4f; odmietnuť_VALUE(44);
        Pripraviť(2); sieť_Vrstvy.vstup_rám[14] = 0x44; odmietnuť_VALUE(44);
        Pripraviť(2); sieť_Vrstvy.vstup_rám[20] = 0x20; množina_kontrolný_súčet(2); odmietnuť_VALUE(44);
        Pripraviť(2); sieť_Vrstvy.vstup_rám[21] = 1; množina_kontrolný_súčet(2); odmietnuť_VALUE(44);
        Pripraviť(2); sieť_Vrstvy.vstup_rám[33] = 99; množina_kontrolný_súčet(2); odmietnuť_VALUE(44);
        Pripraviť(2); sieť_Vrstvy.vstup_rám[0] ^= 1; odmietnuť_VALUE(44);
        Pripraviť(2); sieť_Vrstvy.vstup_rám[23] = 6; množina_kontrolný_súčet(2); odmietnuť_VALUE(44);
        Pripraviť(2); sieť_Vrstvy.넣기16(sieť_Vrstvy.vstup_rám, 40, 0); sieť_Vrstvy.Proces_rám(44); overiť(sieť_Vrstvy.RECEIVED_dĺžka[0] == 2);
        int[] KR = new int[4];
        overiť(sieť_Vrstvy.dostať(3, KR, 1, 0) == -90);
        overiť(sieť_Vrstvy.dostať(3, KR, 4, 0) == -11);
        Pripraviť(2); sieť_Vrstvy.Proces_rám(44); int zahodiť_VALUE = sieť_Vrstvy.폐기수;
        sieť_Vrstvy.Proces_rám(44); overiť(sieť_Vrstvy.폐기수 == zahodiť_VALUE + 1);
        sieť_Vrstvy.CLEAN_Proces(); overiť(sieť_Vrstvy.Otvoriť(5000) == 3);
        overiť(sieť_Vrstvy.Otvoriť(5000) == -98); overiť(sieť_Vrstvy.Otvoriť(0) == 4);
        overiť(sieť_Vrstvy.Otvoriť(0) == 5); overiť(sieť_Vrstvy.Otvoriť(0) == 6); overiť(sieť_Vrstvy.Otvoriť(0) == -24);
        overiť(sieť_Vrstvy.Zatvoriť(4) == 0); overiť(sieť_Vrstvy.Zatvoriť(4) == -9);
        sieť_Vrstvy.찾은주소 = sieť_Vrstvy.brána_VALUE;
        overiť(sieť_Vrstvy.odoslať(3, sieť_Vrstvy.brána_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = sieť_ovládač.Nedávne_VALUE;
        overiť(kontrolný_súčet(보냄, 14, 20, 0) == 0);
        overiť(kontrolný_súčet(보냄, 34, 11, sieť_Vrstvy.가상머리합(sieť_Vrstvy.내주소, sieť_Vrstvy.brána_VALUE, 11)) == 0);
        overiť(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
