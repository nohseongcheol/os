// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** verklig_data Java kontraktsvärde 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class paket_test {
    static int repetition_ANTAL = 0;
    static void verifiera(boolean värde) { if (!värde) throw new AssertionError("case " + repetition_ANTAL); repetition_ANTAL++; }
    static int kontrollsumma(int[] värde, int Kör, int längd_värde, int starttillstånd) {
        int SUM_värde = starttillstånd;
        for (int INDEX = 0; INDEX < längd_värde; INDEX++) SUM_värde += värde[Kör + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_värde = (SUM_värde & 65535) + (SUM_värde >>> 16);
        SUM_värde = (SUM_värde & 65535) + (SUM_värde >>> 16);
        return ~SUM_värde & 65535;
    }
    static void Förbereda(int längd_värde) {
        nätverk_Stack.Rent_Process();
        verifiera(nätverk_Stack.Öppna(5000) == 3);
        int[] ram_INDEX = nätverk_Stack.indata_ram;
        Arrays.fill(ram_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) ram_INDEX[INDEX] = nätverk_drivrutin.enhet_ADRESS[INDEX];
        nätverk_Stack.넣기16(ram_INDEX, 12, 0x0800);
        ram_INDEX[14] = 0x45; ram_INDEX[22] = 64; ram_INDEX[23] = 17;
        nätverk_Stack.넣기16(ram_INDEX, 16, 28 + längd_värde);
        nätverk_Stack.넣기32(ram_INDEX, 26, 0x0a000202); nätverk_Stack.넣기32(ram_INDEX, 30, nätverk_Stack.내주소);
        nätverk_Stack.넣기16(ram_INDEX, 34, 4321); nätverk_Stack.넣기16(ram_INDEX, 36, 5000); nätverk_Stack.넣기16(ram_INDEX, 38, längd_värde + 8);
        for (int INDEX = 0; INDEX < längd_värde; INDEX++) ram_INDEX[42 + INDEX] = INDEX & 255;
        uppsättning_kontrollsumma(längd_värde);
    }
    static void uppsättning_kontrollsumma(int längd_värde) {
        int[] ram_INDEX = nätverk_Stack.indata_ram;
        nätverk_Stack.넣기16(ram_INDEX, 24, 0); nätverk_Stack.넣기16(ram_INDEX, 40, 0);
        nätverk_Stack.넣기16(ram_INDEX, 24, kontrollsumma(ram_INDEX, 14, 20, 0));
        int starttillstånd = nätverk_Stack.가상머리합(nätverk_Stack.heltal_32(ram_INDEX, 26), nätverk_Stack.내주소, längd_värde + 8);
        int SUM_värde = kontrollsumma(ram_INDEX, 34, längd_värde + 8, starttillstånd);
        nätverk_Stack.넣기16(ram_INDEX, 40, SUM_värde == 0 ? 65535 : SUM_värde);
    }
    static void avvisa_värde(int längd_värde) { nätverk_Stack.Process_ram(längd_värde); verifiera(nätverk_Stack.BELOPP_längd[0] == -1); }
    public static void main(String[] argument) {
        for (int längd_värde : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Förbereda(längd_värde); nätverk_Stack.Process_ram(längd_värde + 42);
            verifiera(nätverk_Stack.BELOPP_längd[0] == längd_värde);
            verifiera(nätverk_Stack.BELOPP_ADRESS[0] == 0x0a000202 && nätverk_Stack.BELOPP_portnummer[0] == 4321);
            for (int INDEX = 0; INDEX < längd_värde; INDEX++) verifiera(nätverk_Stack.BELOPP_data[INDEX] == (INDEX & 255));
        }
        for (int längd_värde = 0; längd_värde < 42; längd_värde++) { Förbereda(0); avvisa_värde(längd_värde); }
        Förbereda(1025); avvisa_värde(1067);
        Förbereda(2); nätverk_Stack.indata_ram[24] ^= 1; avvisa_värde(44);
        Förbereda(2); nätverk_Stack.indata_ram[42] ^= 1; avvisa_värde(44);
        Förbereda(2); nätverk_Stack.넣기16(nätverk_Stack.indata_ram, 38, 7); avvisa_värde(44);
        Förbereda(2); nätverk_Stack.넣기16(nätverk_Stack.indata_ram, 38, 65535); avvisa_värde(44);
        Förbereda(2); nätverk_Stack.indata_ram[14] = 0x4f; avvisa_värde(44);
        Förbereda(2); nätverk_Stack.indata_ram[14] = 0x44; avvisa_värde(44);
        Förbereda(2); nätverk_Stack.indata_ram[20] = 0x20; uppsättning_kontrollsumma(2); avvisa_värde(44);
        Förbereda(2); nätverk_Stack.indata_ram[21] = 1; uppsättning_kontrollsumma(2); avvisa_värde(44);
        Förbereda(2); nätverk_Stack.indata_ram[33] = 99; uppsättning_kontrollsumma(2); avvisa_värde(44);
        Förbereda(2); nätverk_Stack.indata_ram[0] ^= 1; avvisa_värde(44);
        Förbereda(2); nätverk_Stack.indata_ram[23] = 6; uppsättning_kontrollsumma(2); avvisa_värde(44);
        Förbereda(2); nätverk_Stack.넣기16(nätverk_Stack.indata_ram, 40, 0); nätverk_Stack.Process_ram(44); verifiera(nätverk_Stack.BELOPP_längd[0] == 2);
        int[] RESULTAT = new int[4];
        verifiera(nätverk_Stack.få(3, RESULTAT, 1, 0) == -90);
        verifiera(nätverk_Stack.få(3, RESULTAT, 4, 0) == -11);
        Förbereda(2); nätverk_Stack.Process_ram(44); int ta_bort_värde = nätverk_Stack.폐기수;
        nätverk_Stack.Process_ram(44); verifiera(nätverk_Stack.폐기수 == ta_bort_värde + 1);
        nätverk_Stack.Rent_Process(); verifiera(nätverk_Stack.Öppna(5000) == 3);
        verifiera(nätverk_Stack.Öppna(5000) == -98); verifiera(nätverk_Stack.Öppna(0) == 4);
        verifiera(nätverk_Stack.Öppna(0) == 5); verifiera(nätverk_Stack.Öppna(0) == 6); verifiera(nätverk_Stack.Öppna(0) == -24);
        verifiera(nätverk_Stack.Stäng(4) == 0); verifiera(nätverk_Stack.Stäng(4) == -9);
        nätverk_Stack.찾은주소 = nätverk_Stack.gateway_värde;
        verifiera(nätverk_Stack.skicka(3, nätverk_Stack.gateway_värde, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = nätverk_drivrutin.senaste_värde;
        verifiera(kontrollsumma(보냄, 14, 20, 0) == 0);
        verifiera(kontrollsumma(보냄, 34, 11, nätverk_Stack.가상머리합(nätverk_Stack.내주소, nätverk_Stack.gateway_värde, 11)) == 0);
        verifiera(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + repetition_ANTAL + " assertions");
    }
}
