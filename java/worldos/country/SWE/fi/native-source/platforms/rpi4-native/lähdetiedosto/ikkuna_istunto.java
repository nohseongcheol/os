// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 liittymä Tila_ARVO. tiedoston_nimi 저장소는 공유하고 polku_2/muuttuja_ARVO/LOG_TIETUE/입력은 분리한다. */
public final class ikkuna_istunto {
    static int[] 보관 = new int[4 * 30000], Valmistele = new int[4];
    static int nykyinen_kohde, paikka;
    static boolean 이어읽기;
    static void MATRIISI_ARVO(int[] data, boolean Store_ARVO) {
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < data.length; Loop_INDEKSI++) { if (Store_ARVO) 보관[paikka++] = data[Loop_INDEKSI]; else data[Loop_INDEKSI] = 보관[paikka++]; }
    }
    static int ARVO(int data_ARVO, boolean 저장여부) { if (저장여부) { 보관[paikka++] = data_ARVO; return data_ARVO; } return 보관[paikka++]; }
    static void hae_toimi(int 보관칸, boolean 저장여부) {
        paikka = 보관칸 * 30000;
        MATRIISI_ARVO(Muisti_Files.nykyinen_kohde, 저장여부); Muisti_Files.nykyinen_kesto = ARVO(Muisti_Files.nykyinen_kesto, 저장여부);
        MATRIISI_ARVO(liittymä_syntaksi.muuttuja_nimi, 저장여부); MATRIISI_ARVO(liittymä_syntaksi.muuttuja_data, 저장여부); MATRIISI_ARVO(liittymä_syntaksi.이름길이, 저장여부); MATRIISI_ARVO(liittymä_syntaksi.ARVO_kesto, 저장여부);
        liittymä_syntaksi.Tila_ARVO = ARVO(liittymä_syntaksi.Tila_ARVO, 저장여부);
        MATRIISI_ARVO(rivi_editori.LOG_TIETUE, 저장여부); MATRIISI_ARVO(rivi_editori.LOG_kesto, 저장여부); MATRIISI_ARVO(rivi_editori.Store_ARVO, 저장여부); MATRIISI_ARVO(명령해석기.syöterivi, 저장여부);
        rivi_editori.LOG_LASKE = ARVO(rivi_editori.LOG_LASKE, 저장여부); rivi_editori.LOG_TIETUE_lopettaa_puhelu = ARVO(rivi_editori.LOG_TIETUE_lopettaa_puhelu, 저장여부);
        rivi_editori.Hae_ARVO = ARVO(rivi_editori.Hae_ARVO, 저장여부); rivi_editori.저장길이 = ARVO(rivi_editori.저장길이, 저장여부);
        rivi_editori.Koko = ARVO(rivi_editori.Koko, 저장여부); rivi_editori.kohdistin_ARVO = ARVO(rivi_editori.kohdistin_ARVO, 저장여부); rivi_editori.alku_ikkuna = ARVO(rivi_editori.alku_ikkuna, 저장여부);
        Valmistele[보관칸] = 1;
    }
    static void prosessi_ARVO_merkintä() {
        int tapahtuma_numero = Taulu.komentotulkki(12); if (tapahtuma_numero == 0) return;
        hae_toimi(nykyinen_kohde, true);
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < 4; Loop_INDEKSI++) {
            if ((tapahtuma_numero & (1 << (8 + Loop_INDEKSI))) != 0) { Taulu.ohjain_käyttäjä_ohjelma(32 + Loop_INDEKSI); Valmistele[Loop_INDEKSI] = 0; }
            if ((tapahtuma_numero & (1 << (4 + Loop_INDEKSI))) != 0 && Loop_INDEKSI != nykyinen_kohde) Valmistele[Loop_INDEKSI] = 0;
        }
        int Seuraava_toimi = (tapahtuma_numero & 15) - 1; if (Seuraava_toimi < 0) Seuraava_toimi = 0;
        if (Valmistele[Seuraava_toimi] == 0) for (int Loop_INDEKSI = 0; Loop_INDEKSI < 30000; Loop_INDEKSI++) 보관[Seuraava_toimi * 30000 + Loop_INDEKSI] = 0;
        nykyinen_kohde = Seuraava_toimi; hae_toimi(nykyinen_kohde, false); Taulu.komentotulkki(100 + nykyinen_kohde); 이어읽기 = true;
        단말.Kirjoitus("\nTERMINAL FOCUS "); 단말.numero(nykyinen_kohde + 1); 단말.문자(10);
    }
    static boolean jatka_suoritus() {
        if (Taulu.ohjain_käyttäjä_ohjelma(16 + nykyinen_kohde) == 0) return false;
        셸입출력.Salli_vuorovaikutteinen = true; 셸입출력.Suorita_2(false, false); Taulu.입출력전환(1);
        int 처리값 = Taulu.ohjain_käyttäjä_ohjelma(nykyinen_kohde); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; liittymä_syntaksi.Tila_ARVO = 처리값 < 0 ? 126 : 처리값; 단말.Kirjoitus("exit "); 단말.numero(처리값); 단말.문자(10); Taulu.komentotulkki(3); }
        return true;
    }
}
