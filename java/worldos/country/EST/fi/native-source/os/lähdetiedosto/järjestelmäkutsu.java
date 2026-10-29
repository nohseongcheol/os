// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 käyttäjätila osoitin/길이는 pääsy_merkintä_68aed533 전에 검사한다. */
public final class järjestelmäkutsu {
    static int[] 임시자료 = new int[1024];

    static int MATRIISI_kesto(int OSOITE) {
        if (!suoritus_Valvoja.leikata(OSOITE, 4)) return -14;
        int kesto_ARVO = suoritus_Valvoja.numero(OSOITE);
        if (kesto_ARVO < 0 || kesto_ARVO > (suoritus_Valvoja.käyttäjä_lopettaa_puhelu - OSOITE - 4) / 4) return -14;
        return kesto_ARVO;
    }

    public static int prosessi_ARVO_merkintä(int INDEKSI, int 가, int SEKUNNIT_operandi, int 다, int 라, int 마) {
        if (INDEKSI == 30) return 파일서술자관리.avata_Tiedosto(가, SEKUNNIT_operandi, 다);
        if (INDEKSI == 31) return 파일서술자관리.lukea_Tiedosto(가, SEKUNNIT_operandi, 다);
        if (INDEKSI == 32) return 파일서술자관리.kirjoitus_Tiedosto(가, SEKUNNIT_operandi, 다);
        if (INDEKSI == 33) return 파일서술자관리.Sulje_Tiedosto(가);
        if (INDEKSI == 34) return 파일서술자관리.hae_Tiedosto(가, SEKUNNIT_operandi, 다);
        if (INDEKSI == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEKSI == 36) return 파일서술자관리.서술자복제(가, SEKUNNIT_operandi, true, 0);
        if (INDEKSI == 37) return 파일서술자관리.lukea_Tiedosto_tila(가, SEKUNNIT_operandi);
        if (INDEKSI == 38) return 파일서술자관리.poistaa_Tiedosto_merkintä_nimi(가);
        if (INDEKSI == 39) return 파일서술자관리.ryhmä_Tiedosto_kesto(가, SEKUNNIT_operandi);
        if (INDEKSI == 40) return 파일서술자관리.서술자제어(가, SEKUNNIT_operandi, 다);
        if (INDEKSI == 41) return 파일서술자관리.Luo_päätepiste(가, SEKUNNIT_operandi, 다);
        if (INDEKSI == 42) return 파일서술자관리.BIND_OSOITE(가, SEKUNNIT_operandi, 다);
        if (INDEKSI == 43) return 파일서술자관리.lähettää_datagrammi_data(가, SEKUNNIT_operandi, 다, 라, 마);
        if (INDEKSI == 44) return 파일서술자관리.saada_datagrammi_data(가, SEKUNNIT_operandi, 다, 라, 마);
        if (INDEKSI == 45) return 파일서술자관리.lukea_vastake_OSOITE(가, SEKUNNIT_operandi, 다);
        if (INDEKSI == 46) return 파일서술자관리.ryhmä_saada_AIKAKATKAISU(가, SEKUNNIT_operandi);
        if (INDEKSI == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.synkronoi();
        }
        if (INDEKSI == 1) {
            int kesto_ARVO = MATRIISI_kesto(가);
            if (kesto_ARVO < 0) return kesto_ARVO;
            if (kesto_ARVO > 4096) return -90;
            for (int merkki_ARVO = 0; merkki_ARVO < kesto_ARVO; merkki_ARVO++) SMS_Pääte.문자(suoritus_Valvoja.numero(가 + 4 + merkki_ARVO * 4) & 65535);
            return kesto_ARVO;
        }
        if (INDEKSI == 2) return suoritus_Valvoja.argumentti_LASKE;
        if (INDEKSI == 3) return 가 >= 0 && 가 < suoritus_Valvoja.argumentti_LASKE ? suoritus_Valvoja.argumentti_OSOITE[가] : 0;
        if (INDEKSI == 10) return verkko_Pino.Avaa(가);
        if (INDEKSI == 11) {
            int kesto_ARVO = MATRIISI_kesto(라);
            if (kesto_ARVO < 0) return kesto_ARVO;
            if (마 < 0 || 마 > kesto_ARVO || 마 > 1024) return -90;
            for (int paikka = 0; paikka < 마; paikka++) 임시자료[paikka] = suoritus_Valvoja.numero(라 + 4 + paikka * 4) & 255;
            return verkko_Pino.lähettää(가, SEKUNNIT_operandi, 다, 임시자료, 마);
        }
        if (INDEKSI == 12) {
            int kesto_ARVO = MATRIISI_kesto(SEKUNNIT_operandi);
            if (kesto_ARVO < 0) return kesto_ARVO;
            if (다 < 0 || 다 > 2000) return -22;
            int TULOS = verkko_Pino.saada(가, 임시자료, kesto_ARVO < 1024 ? kesto_ARVO : 1024, 다);
            if (TULOS >= 0) for (int paikka = 0; paikka < TULOS; paikka++) suoritus_Valvoja.kirjoitus_numero(SEKUNNIT_operandi + 4 + paikka * 4, 임시자료[paikka]);
            return TULOS;
        }
        if (INDEKSI == 13) return verkko_Pino.Sulje(가);
        if (INDEKSI == 14) return verkko_Pino.내주소;
        if (INDEKSI == 15) return verkko_Pino.vertaissolmu_OSOITE(가);
        if (INDEKSI == 16) return verkko_Pino.vertaissolmu_portin_numero(가);
        if (INDEKSI == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Pääte.문자(가); return 1;
        }
        if (INDEKSI == 20 || INDEKSI == 21) {
            int nimi_muuttaa_kokoa = MATRIISI_kesto(가), data_muuttaa_kokoa = MATRIISI_kesto(SEKUNNIT_operandi);
            if (nimi_muuttaa_kokoa < 0 || data_muuttaa_kokoa < 0) return -14;
            if (nimi_muuttaa_kokoa < 1 || nimi_muuttaa_kokoa > 64) return -22;
            int kesto_ARVO = 0;
            while (kesto_ARVO < nimi_muuttaa_kokoa && suoritus_Valvoja.numero(가 + 4 + kesto_ARVO * 4) != 0) {
                Muisti_tiedostojärjestelmä.Nimi[kesto_ARVO] = suoritus_Valvoja.numero(가 + 4 + kesto_ARVO * 4);
                kesto_ARVO++;
            }
            if (!Muisti_tiedostojärjestelmä.sekki_nimi(Muisti_tiedostojärjestelmä.Nimi, kesto_ARVO)) return -22;
            if (INDEKSI == 20) {
                int tiedoston_nimi = Muisti_tiedostojärjestelmä.ETSI_merkintä(Muisti_tiedostojärjestelmä.Nimi, kesto_ARVO);
                if (tiedoston_nimi < 0) return tiedoston_nimi;
                int Koko = Muisti_tiedostojärjestelmä.muuttaa_kokoa_luettelo[tiedoston_nimi];
                if (Koko > data_muuttaa_kokoa) return -90;
                int OSOITE = laite_ARVO.Tiedosto_Muisti() + tiedoston_nimi * Muisti_tiedostojärjestelmä.최대크기;
                for (int numero = 0; numero < Koko; numero++) suoritus_Valvoja.kirjoitus_numero(SEKUNNIT_operandi + 4 + numero * 4, laite_ARVO.lukea_Muisti(OSOITE + numero));
                return Koko;
            }
            if (다 < 0 || 다 > data_muuttaa_kokoa) return -22;
            if (다 > Muisti_tiedostojärjestelmä.최대크기) return -90;
            for (int numero = 0; numero < 다; numero++) Muisti_tiedostojärjestelmä.muutos_ARVO[numero] = suoritus_Valvoja.numero(SEKUNNIT_operandi + 4 + numero * 4) & 255;
            return Muisti_tiedostojärjestelmä.Store_ARVO(Muisti_tiedostojärjestelmä.Nimi, kesto_ARVO, Muisti_tiedostojärjestelmä.muutos_ARVO, 다);
        }
        return -38;
    }
}
