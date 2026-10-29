// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** skutečný_data Java hodnota_smlouvy 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class paket_test {
    static int opakování_POČET = 0;
    static void ověřit(boolean HODNOTA) { if (!HODNOTA) throw new AssertionError("case " + opakování_POČET); opakování_POČET++; }
    static int kontrolní_součet(int[] HODNOTA, int Spustit_2, int délka_HODNOTA, int počáteční_stav) {
        int SUMA_HODNOTA = počáteční_stav;
        for (int INDEX = 0; INDEX < délka_HODNOTA; INDEX++) SUMA_HODNOTA += HODNOTA[Spustit_2 + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUMA_HODNOTA = (SUMA_HODNOTA & 65535) + (SUMA_HODNOTA >>> 16);
        SUMA_HODNOTA = (SUMA_HODNOTA & 65535) + (SUMA_HODNOTA >>> 16);
        return ~SUMA_HODNOTA & 65535;
    }
    static void Připravit(int délka_HODNOTA) {
        síť_Štos.Čisté_Proces();
        ověřit(síť_Štos.Otevřít(5000) == 3);
        int[] rámec_INDEX = síť_Štos.vstup_rámec;
        Arrays.fill(rámec_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) rámec_INDEX[INDEX] = síť_ovladač.mobilní_ODKAZ[INDEX];
        síť_Štos.넣기16(rámec_INDEX, 12, 0x0800);
        rámec_INDEX[14] = 0x45; rámec_INDEX[22] = 64; rámec_INDEX[23] = 17;
        síť_Štos.넣기16(rámec_INDEX, 16, 28 + délka_HODNOTA);
        síť_Štos.넣기32(rámec_INDEX, 26, 0x0a000202); síť_Štos.넣기32(rámec_INDEX, 30, síť_Štos.내주소);
        síť_Štos.넣기16(rámec_INDEX, 34, 4321); síť_Štos.넣기16(rámec_INDEX, 36, 5000); síť_Štos.넣기16(rámec_INDEX, 38, délka_HODNOTA + 8);
        for (int INDEX = 0; INDEX < délka_HODNOTA; INDEX++) rámec_INDEX[42 + INDEX] = INDEX & 255;
        sada_kontrolní_součet(délka_HODNOTA);
    }
    static void sada_kontrolní_součet(int délka_HODNOTA) {
        int[] rámec_INDEX = síť_Štos.vstup_rámec;
        síť_Štos.넣기16(rámec_INDEX, 24, 0); síť_Štos.넣기16(rámec_INDEX, 40, 0);
        síť_Štos.넣기16(rámec_INDEX, 24, kontrolní_součet(rámec_INDEX, 14, 20, 0));
        int počáteční_stav = síť_Štos.가상머리합(síť_Štos.integer_32(rámec_INDEX, 26), síť_Štos.내주소, délka_HODNOTA + 8);
        int SUMA_HODNOTA = kontrolní_součet(rámec_INDEX, 34, délka_HODNOTA + 8, počáteční_stav);
        síť_Štos.넣기16(rámec_INDEX, 40, SUMA_HODNOTA == 0 ? 65535 : SUMA_HODNOTA);
    }
    static void odmítnout_HODNOTA(int délka_HODNOTA) { síť_Štos.Proces_rámec(délka_HODNOTA); ověřit(síť_Štos.RECEIVED_délka[0] == -1); }
    public static void main(String[] argumenty) {
        for (int délka_HODNOTA : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Připravit(délka_HODNOTA); síť_Štos.Proces_rámec(délka_HODNOTA + 42);
            ověřit(síť_Štos.RECEIVED_délka[0] == délka_HODNOTA);
            ověřit(síť_Štos.RECEIVED_ODKAZ[0] == 0x0a000202 && síť_Štos.RECEIVED_číslo_portu[0] == 4321);
            for (int INDEX = 0; INDEX < délka_HODNOTA; INDEX++) ověřit(síť_Štos.RECEIVED_data[INDEX] == (INDEX & 255));
        }
        for (int délka_HODNOTA = 0; délka_HODNOTA < 42; délka_HODNOTA++) { Připravit(0); odmítnout_HODNOTA(délka_HODNOTA); }
        Připravit(1025); odmítnout_HODNOTA(1067);
        Připravit(2); síť_Štos.vstup_rámec[24] ^= 1; odmítnout_HODNOTA(44);
        Připravit(2); síť_Štos.vstup_rámec[42] ^= 1; odmítnout_HODNOTA(44);
        Připravit(2); síť_Štos.넣기16(síť_Štos.vstup_rámec, 38, 7); odmítnout_HODNOTA(44);
        Připravit(2); síť_Štos.넣기16(síť_Štos.vstup_rámec, 38, 65535); odmítnout_HODNOTA(44);
        Připravit(2); síť_Štos.vstup_rámec[14] = 0x4f; odmítnout_HODNOTA(44);
        Připravit(2); síť_Štos.vstup_rámec[14] = 0x44; odmítnout_HODNOTA(44);
        Připravit(2); síť_Štos.vstup_rámec[20] = 0x20; sada_kontrolní_součet(2); odmítnout_HODNOTA(44);
        Připravit(2); síť_Štos.vstup_rámec[21] = 1; sada_kontrolní_součet(2); odmítnout_HODNOTA(44);
        Připravit(2); síť_Štos.vstup_rámec[33] = 99; sada_kontrolní_součet(2); odmítnout_HODNOTA(44);
        Připravit(2); síť_Štos.vstup_rámec[0] ^= 1; odmítnout_HODNOTA(44);
        Připravit(2); síť_Štos.vstup_rámec[23] = 6; sada_kontrolní_součet(2); odmítnout_HODNOTA(44);
        Připravit(2); síť_Štos.넣기16(síť_Štos.vstup_rámec, 40, 0); síť_Štos.Proces_rámec(44); ověřit(síť_Štos.RECEIVED_délka[0] == 2);
        int[] VÝSLEDEK = new int[4];
        ověřit(síť_Štos.dostat(3, VÝSLEDEK, 1, 0) == -90);
        ověřit(síť_Štos.dostat(3, VÝSLEDEK, 4, 0) == -11);
        Připravit(2); síť_Štos.Proces_rámec(44); int zahodit_HODNOTA = síť_Štos.폐기수;
        síť_Štos.Proces_rámec(44); ověřit(síť_Štos.폐기수 == zahodit_HODNOTA + 1);
        síť_Štos.Čisté_Proces(); ověřit(síť_Štos.Otevřít(5000) == 3);
        ověřit(síť_Štos.Otevřít(5000) == -98); ověřit(síť_Štos.Otevřít(0) == 4);
        ověřit(síť_Štos.Otevřít(0) == 5); ověřit(síť_Štos.Otevřít(0) == 6); ověřit(síť_Štos.Otevřít(0) == -24);
        ověřit(síť_Štos.Zavřené(4) == 0); ověřit(síť_Štos.Zavřené(4) == -9);
        síť_Štos.찾은주소 = síť_Štos.brána_HODNOTA;
        ověřit(síť_Štos.poslat(3, síť_Štos.brána_HODNOTA, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = síť_ovladač.nedávné_HODNOTA;
        ověřit(kontrolní_součet(보냄, 14, 20, 0) == 0);
        ověřit(kontrolní_součet(보냄, 34, 11, síť_Štos.가상머리합(síť_Štos.내주소, síť_Štos.brána_HODNOTA, 11)) == 0);
        ověřit(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + opakování_POČET + " assertions");
    }
}
