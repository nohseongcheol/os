// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Läs 전용 köra_kommando 묶음의 ELF32 validera, argument Framåt_värde, 한 번에 한 användarutrymme Process_värde köra_kommando. */
public final class körning_Ansvarig {
    static final int START_användare_app = 0x04000000;
    static final int användare_avsluta = 0x04400000;
    static final int BILD_avsluta_ADRESS = 0x04200000;
    static final int argument_START = 0x04300000;
    static int argument_ANTAL = 0;
    static int[] argument_ADRESS = new int[16];

    static boolean klipp(int Adress, int längd_värde) {
        return Adress >= START_användare_app && Adress < användare_avsluta && längd_värde >= 0 && längd_värde <= användare_avsluta - Adress;
    }

    static int nummer(int Adress) { return Minne_område.parsa_heltal(Adress); }
    static int 짧은수(int Adress) { return enhet_värde.läsa_Minne(Adress) | enhet_värde.läsa_Minne(Adress + 1) << 8; }
    static void skriva_nummer(int Adress, int värde) {
        for (int INDEX = 0; INDEX < 4; INDEX++) enhet_värde.skriva_Minne(Adress + INDEX, värde >>> (INDEX * 8));
    }

    static int grupp_ANTAL() {
        int Adress = enhet_värde.körbar_fil_bunt();
        int Storlek = enhet_värde.körbar_fil_bunt_storlek();
        if (Storlek < 8 || nummer(Adress) != 0x50414b4a) return 0;
        int objekt_ANTAL = nummer(Adress + 4);
        return objekt_ANTAL >= 0 && objekt_ANTAL <= 32 && objekt_ANTAL <= (Storlek - 8) / 24 ? objekt_ANTAL : 0;
    }

    static void post_ange() {
        for (int INDEX = 0; INDEX < grupp_ANTAL(); INDEX++) {
            int post_värde = enhet_värde.körbar_fil_bunt() + 8 + INDEX * 24;
            for (int tecken_värde = 0; tecken_värde < 16 && enhet_värde.läsa_Minne(post_värde + tecken_värde) != 0; tecken_värde++)
                SMS_Terminal.문자(enhet_värde.läsa_Minne(post_värde + tecken_värde));
            SMS_Terminal.Skriv("\n");
        }
    }

    static int Sök_post(int[] indata_värde, int Kör, int längd_värde) {
        if (längd_värde <= 0 || längd_värde >= 16) return 0;
        for (int INDEX = 0; INDEX < grupp_ANTAL(); INDEX++) {
            int post_värde = enhet_värde.körbar_fil_bunt() + 8 + INDEX * 24;
            boolean 같음 = enhet_värde.läsa_Minne(post_värde + längd_värde) == 0;
            for (int tecken_värde = 0; tecken_värde < längd_värde; tecken_värde++)
                if (indata_värde[Kör + tecken_värde] != enhet_värde.läsa_Minne(post_värde + tecken_värde)) 같음 = false;
            if (같음) return post_värde;
        }
        return 0;
    }

    static int validera(int filnamn, int längd_värde) {
        if (längd_värde < 52 || nummer(filnamn) != 0x464c457f || enhet_värde.läsa_Minne(filnamn + 4) != 1
            || enhet_värde.läsa_Minne(filnamn + 5) != 1 || enhet_värde.läsa_Minne(filnamn + 6) != 1
            || 짧은수(filnamn + 16) != 2 || 짧은수(filnamn + 18) != 3 || nummer(filnamn + 20) != 1
            || 짧은수(filnamn + 40) != 52 || 짧은수(filnamn + 42) != 32) return -8;
        int startpunkt_värde = nummer(filnamn + 24);
        int tabell_placera = nummer(filnamn + 28);
        int objekt_ANTAL = 짧은수(filnamn + 44);
        if (objekt_ANTAL == 0 || objekt_ANTAL > 16 || tabell_placera < 52 || tabell_placera > längd_värde - objekt_ANTAL * 32) return -8;
        boolean informationsteknik_körbar_fil = false;
        for (int INDEX = 0; INDEX < objekt_ANTAL; INDEX++) {
            int LETAUPP_tabell = filnamn + tabell_placera + INDEX * 32;
            int variant_värde = nummer(LETAUPP_tabell);
            if (variant_värde == 2 || variant_värde == 3) return -8; // 동적 Anslut/parser_48ee4b1b 미지원
            if (variant_värde != 1) continue;
            int position = nummer(LETAUPP_tabell + 4), Adress = nummer(LETAUPP_tabell + 8), filstorlek = nummer(LETAUPP_tabell + 16), Minne_storlek = nummer(LETAUPP_tabell + 20);
            int justera_värde = nummer(LETAUPP_tabell + 28);
            if (Adress < START_användare_app || Adress >= BILD_avsluta_ADRESS || Minne_storlek < 0 || Minne_storlek > BILD_avsluta_ADRESS - Adress
                || filstorlek < 0 || filstorlek > Minne_storlek || position < 0 || (filstorlek > 0 && position > längd_värde - filstorlek)
                || (justera_värde != 0 && (justera_värde < 0 || (justera_värde & (justera_värde - 1)) != 0
                    || ((Adress - position) & (justera_värde - 1)) != 0))) return -8;
            for (int framåtvänd_värde = 0; framåtvänd_värde < INDEX; framåtvänd_värde++) {
                int Föregående_objekt = filnamn + tabell_placera + framåtvänd_värde * 32;
                if (nummer(Föregående_objekt) == 1 && Minne_storlek > 0 && nummer(Föregående_objekt + 20) > 0
                    && Adress < nummer(Föregående_objekt + 8) + nummer(Föregående_objekt + 20) && nummer(Föregående_objekt + 8) < Adress + Minne_storlek) return -8;
            }
            if ((nummer(LETAUPP_tabell + 24) & 1) != 0 && startpunkt_värde >= Adress && startpunkt_värde - Adress < filstorlek) informationsteknik_körbar_fil = true;
        }
        return informationsteknik_körbar_fil ? startpunkt_värde : -8;
    }

    static int köra_kommando(int[] indata_värde, int Kör, int längd_värde) {
        while (Kör < längd_värde && indata_värde[Kör] == ' ') Kör++;
        int 끝 = Kör;
        while (끝 < längd_värde && indata_värde[끝] != ' ') 끝++;
        int post_värde = Sök_post(indata_värde, Kör, 끝 - Kör);
        if (post_värde == 0) return -2;
        int position = nummer(post_värde + 16), Storlek = nummer(post_värde + 20);
        if (position < 8 + grupp_ANTAL() * 24 || Storlek < 52 || position > enhet_värde.körbar_fil_bunt_storlek() - Storlek) return -8;
        int filnamn = enhet_värde.körbar_fil_bunt() + position;
        int startpunkt_värde = validera(filnamn, Storlek);
        if (startpunkt_värde < 0) return startpunkt_värde;
        enhet_värde.användare_rensa_Innehåll();
        int tabell_placera = nummer(filnamn + 28), objekt_ANTAL = 짧은수(filnamn + 44);
        for (int INDEX = 0; INDEX < objekt_ANTAL; INDEX++) {
            int LETAUPP_tabell = filnamn + tabell_placera + INDEX * 32;
            if (nummer(LETAUPP_tabell) != 1) continue;
            int 원본 = filnamn + nummer(LETAUPP_tabell + 4), mål_värde = nummer(LETAUPP_tabell + 8), filstorlek = nummer(LETAUPP_tabell + 16);
            for (int byte_värde = 0; byte_värde < filstorlek; byte_värde++) enhet_värde.skriva_Minne(mål_värde + byte_värde, enhet_värde.läsa_Minne(원본 + byte_värde));
        }
        argument_ANTAL = 0;
        int Store_värde = argument_START;
        while (끝 < längd_värde) {
            while (끝 < längd_värde && indata_värde[끝] == ' ') 끝++;
            if (끝 == längd_värde) break;
            if (argument_ANTAL == argument_ADRESS.length) return -22;
            Kör = 끝;
            while (끝 < längd_värde && indata_värde[끝] != ' ') 끝++;
            argument_ADRESS[argument_ANTAL++] = Store_värde;
            skriva_nummer(Store_värde, 끝 - Kör);
            for (int tecken_värde = Kör; tecken_värde < 끝; tecken_värde++) skriva_nummer(Store_värde + 4 + (tecken_värde - Kör) * 4, indata_värde[tecken_värde]);
            Store_värde += 4 + (끝 - Kör) * 4;
        }
        nätverk_Stack.Rent_Process();
        파일서술자관리.START_Process();
        int RESULTAT = enhet_värde.köra_användare_app(startpunkt_värde, användare_avsluta - 16);
        파일서술자관리.Rent_Process();
        nätverk_Stack.Rent_Process();
        return RESULTAT;
    }
}
