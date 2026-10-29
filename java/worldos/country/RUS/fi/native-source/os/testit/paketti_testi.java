// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** todellinen_data Java sopimuksen_arvo 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class paketti_testi {
    static int toisto_LASKE = 0;
    static void tarkistaa(boolean ARVO) { if (!ARVO) throw new AssertionError("case " + toisto_LASKE); toisto_LASKE++; }
    static int tarkistussumma(int[] ARVO, int Suorita_2, int kesto_ARVO, int alkutila) {
        int SUM_ARVO = alkutila;
        for (int INDEKSI = 0; INDEKSI < kesto_ARVO; INDEKSI++) SUM_ARVO += ARVO[Suorita_2 + INDEKSI] << ((INDEKSI & 1) == 0 ? 8 : 0);
        SUM_ARVO = (SUM_ARVO & 65535) + (SUM_ARVO >>> 16);
        SUM_ARVO = (SUM_ARVO & 65535) + (SUM_ARVO >>> 16);
        return ~SUM_ARVO & 65535;
    }
    static void Valmistele(int kesto_ARVO) {
        verkko_Pino.SIIVOA_prosessi();
        tarkistaa(verkko_Pino.Avaa(5000) == 3);
        int[] kuva_INDEKSI = verkko_Pino.syöte_kuva;
        Arrays.fill(kuva_INDEKSI, 0);
        for (int INDEKSI = 0; INDEKSI < 6; INDEKSI++) kuva_INDEKSI[INDEKSI] = verkko_ohjain.laite_OSOITE[INDEKSI];
        verkko_Pino.넣기16(kuva_INDEKSI, 12, 0x0800);
        kuva_INDEKSI[14] = 0x45; kuva_INDEKSI[22] = 64; kuva_INDEKSI[23] = 17;
        verkko_Pino.넣기16(kuva_INDEKSI, 16, 28 + kesto_ARVO);
        verkko_Pino.넣기32(kuva_INDEKSI, 26, 0x0a000202); verkko_Pino.넣기32(kuva_INDEKSI, 30, verkko_Pino.내주소);
        verkko_Pino.넣기16(kuva_INDEKSI, 34, 4321); verkko_Pino.넣기16(kuva_INDEKSI, 36, 5000); verkko_Pino.넣기16(kuva_INDEKSI, 38, kesto_ARVO + 8);
        for (int INDEKSI = 0; INDEKSI < kesto_ARVO; INDEKSI++) kuva_INDEKSI[42 + INDEKSI] = INDEKSI & 255;
        ryhmä_tarkistussumma(kesto_ARVO);
    }
    static void ryhmä_tarkistussumma(int kesto_ARVO) {
        int[] kuva_INDEKSI = verkko_Pino.syöte_kuva;
        verkko_Pino.넣기16(kuva_INDEKSI, 24, 0); verkko_Pino.넣기16(kuva_INDEKSI, 40, 0);
        verkko_Pino.넣기16(kuva_INDEKSI, 24, tarkistussumma(kuva_INDEKSI, 14, 20, 0));
        int alkutila = verkko_Pino.가상머리합(verkko_Pino.kokonaisluku_32(kuva_INDEKSI, 26), verkko_Pino.내주소, kesto_ARVO + 8);
        int SUM_ARVO = tarkistussumma(kuva_INDEKSI, 34, kesto_ARVO + 8, alkutila);
        verkko_Pino.넣기16(kuva_INDEKSI, 40, SUM_ARVO == 0 ? 65535 : SUM_ARVO);
    }
    static void hylkää_ARVO_e3ecc00b(int kesto_ARVO) { verkko_Pino.prosessi_kuva(kesto_ARVO); tarkistaa(verkko_Pino.SAATU_HINTA_kesto[0] == -1); }
    public static void main(String[] argumentit) {
        for (int kesto_ARVO : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Valmistele(kesto_ARVO); verkko_Pino.prosessi_kuva(kesto_ARVO + 42);
            tarkistaa(verkko_Pino.SAATU_HINTA_kesto[0] == kesto_ARVO);
            tarkistaa(verkko_Pino.SAATU_HINTA_OSOITE[0] == 0x0a000202 && verkko_Pino.SAATU_HINTA_portin_numero[0] == 4321);
            for (int INDEKSI = 0; INDEKSI < kesto_ARVO; INDEKSI++) tarkistaa(verkko_Pino.SAATU_HINTA_data[INDEKSI] == (INDEKSI & 255));
        }
        for (int kesto_ARVO = 0; kesto_ARVO < 42; kesto_ARVO++) { Valmistele(0); hylkää_ARVO_e3ecc00b(kesto_ARVO); }
        Valmistele(1025); hylkää_ARVO_e3ecc00b(1067);
        Valmistele(2); verkko_Pino.syöte_kuva[24] ^= 1; hylkää_ARVO_e3ecc00b(44);
        Valmistele(2); verkko_Pino.syöte_kuva[42] ^= 1; hylkää_ARVO_e3ecc00b(44);
        Valmistele(2); verkko_Pino.넣기16(verkko_Pino.syöte_kuva, 38, 7); hylkää_ARVO_e3ecc00b(44);
        Valmistele(2); verkko_Pino.넣기16(verkko_Pino.syöte_kuva, 38, 65535); hylkää_ARVO_e3ecc00b(44);
        Valmistele(2); verkko_Pino.syöte_kuva[14] = 0x4f; hylkää_ARVO_e3ecc00b(44);
        Valmistele(2); verkko_Pino.syöte_kuva[14] = 0x44; hylkää_ARVO_e3ecc00b(44);
        Valmistele(2); verkko_Pino.syöte_kuva[20] = 0x20; ryhmä_tarkistussumma(2); hylkää_ARVO_e3ecc00b(44);
        Valmistele(2); verkko_Pino.syöte_kuva[21] = 1; ryhmä_tarkistussumma(2); hylkää_ARVO_e3ecc00b(44);
        Valmistele(2); verkko_Pino.syöte_kuva[33] = 99; ryhmä_tarkistussumma(2); hylkää_ARVO_e3ecc00b(44);
        Valmistele(2); verkko_Pino.syöte_kuva[0] ^= 1; hylkää_ARVO_e3ecc00b(44);
        Valmistele(2); verkko_Pino.syöte_kuva[23] = 6; ryhmä_tarkistussumma(2); hylkää_ARVO_e3ecc00b(44);
        Valmistele(2); verkko_Pino.넣기16(verkko_Pino.syöte_kuva, 40, 0); verkko_Pino.prosessi_kuva(44); tarkistaa(verkko_Pino.SAATU_HINTA_kesto[0] == 2);
        int[] TULOS = new int[4];
        tarkistaa(verkko_Pino.saada(3, TULOS, 1, 0) == -90);
        tarkistaa(verkko_Pino.saada(3, TULOS, 4, 0) == -11);
        Valmistele(2); verkko_Pino.prosessi_kuva(44); int hylkää_ARVO = verkko_Pino.폐기수;
        verkko_Pino.prosessi_kuva(44); tarkistaa(verkko_Pino.폐기수 == hylkää_ARVO + 1);
        verkko_Pino.SIIVOA_prosessi(); tarkistaa(verkko_Pino.Avaa(5000) == 3);
        tarkistaa(verkko_Pino.Avaa(5000) == -98); tarkistaa(verkko_Pino.Avaa(0) == 4);
        tarkistaa(verkko_Pino.Avaa(0) == 5); tarkistaa(verkko_Pino.Avaa(0) == 6); tarkistaa(verkko_Pino.Avaa(0) == -24);
        tarkistaa(verkko_Pino.Sulje(4) == 0); tarkistaa(verkko_Pino.Sulje(4) == -9);
        verkko_Pino.찾은주소 = verkko_Pino.yhdyskäytävä_ARVO;
        tarkistaa(verkko_Pino.lähettää(3, verkko_Pino.yhdyskäytävä_ARVO, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = verkko_ohjain.viimeisimmät_ARVO;
        tarkistaa(tarkistussumma(보냄, 14, 20, 0) == 0);
        tarkistaa(tarkistussumma(보냄, 34, 11, verkko_Pino.가상머리합(verkko_Pino.내주소, verkko_Pino.yhdyskäytävä_ARVO, 11)) == 0);
        tarkistaa(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + toisto_LASKE + " assertions");
    }
}
