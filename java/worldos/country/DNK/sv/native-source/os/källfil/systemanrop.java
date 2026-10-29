// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 användarutrymme markör/길이는 ansluta_post 전에 검사한다. */
public final class systemanrop {
    static int[] 임시자료 = new int[1024];

    static int MATRIS_längd(int Adress) {
        if (!körning_Ansvarig.klipp(Adress, 4)) return -14;
        int längd_värde = körning_Ansvarig.nummer(Adress);
        if (längd_värde < 0 || längd_värde > (körning_Ansvarig.användare_avsluta - Adress - 4) / 4) return -14;
        return längd_värde;
    }

    public static int Process_värde_post(int INDEX, int 가, int SEKUND_operand, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.skapa_fil(가, SEKUND_operand, 다);
        if (INDEX == 31) return 파일서술자관리.läsa_fil(가, SEKUND_operand, 다);
        if (INDEX == 32) return 파일서술자관리.skriva_fil(가, SEKUND_operand, 다);
        if (INDEX == 33) return 파일서술자관리.Stäng_fil(가);
        if (INDEX == 34) return 파일서술자관리.söka_fil(가, SEKUND_operand, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, SEKUND_operand, true, 0);
        if (INDEX == 37) return 파일서술자관리.läsa_fil_status(가, SEKUND_operand);
        if (INDEX == 38) return 파일서술자관리.ta_bort_fil_post_namn(가);
        if (INDEX == 39) return 파일서술자관리.uppsättning_fil_längd(가, SEKUND_operand);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, SEKUND_operand, 다);
        if (INDEX == 41) return 파일서술자관리.Skapa_deltagare(가, SEKUND_operand, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_ADRESS(가, SEKUND_operand, 다);
        if (INDEX == 43) return 파일서술자관리.skicka_datagram_data(가, SEKUND_operand, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.få_datagram_data(가, SEKUND_operand, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.läsa_socket_ADRESS(가, SEKUND_operand, 다);
        if (INDEX == 46) return 파일서술자관리.uppsättning_få_TIMEOUT(가, SEKUND_operand);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.variant_värde[기술] != 2) return -22;
            return 파일보존.synka();
        }
        if (INDEX == 1) {
            int längd_värde = MATRIS_längd(가);
            if (längd_värde < 0) return längd_värde;
            if (längd_värde > 4096) return -90;
            for (int tecken_värde = 0; tecken_värde < längd_värde; tecken_värde++) SMS_Terminal.문자(körning_Ansvarig.nummer(가 + 4 + tecken_värde * 4) & 65535);
            return längd_värde;
        }
        if (INDEX == 2) return körning_Ansvarig.argument_ANTAL;
        if (INDEX == 3) return 가 >= 0 && 가 < körning_Ansvarig.argument_ANTAL ? körning_Ansvarig.argument_ADRESS[가] : 0;
        if (INDEX == 10) return nätverk_Stack.Öppna(가);
        if (INDEX == 11) {
            int längd_värde = MATRIS_längd(라);
            if (längd_värde < 0) return längd_värde;
            if (마 < 0 || 마 > längd_värde || 마 > 1024) return -90;
            for (int position = 0; position < 마; position++) 임시자료[position] = körning_Ansvarig.nummer(라 + 4 + position * 4) & 255;
            return nätverk_Stack.skicka(가, SEKUND_operand, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int längd_värde = MATRIS_längd(SEKUND_operand);
            if (längd_värde < 0) return längd_värde;
            if (다 < 0 || 다 > 2000) return -22;
            int RESULTAT = nätverk_Stack.få(가, 임시자료, längd_värde < 1024 ? längd_värde : 1024, 다);
            if (RESULTAT >= 0) for (int position = 0; position < RESULTAT; position++) körning_Ansvarig.skriva_nummer(SEKUND_operand + 4 + position * 4, 임시자료[position]);
            return RESULTAT;
        }
        if (INDEX == 13) return nätverk_Stack.Stäng(가);
        if (INDEX == 14) return nätverk_Stack.내주소;
        if (INDEX == 15) return nätverk_Stack.peer_ADRESS(가);
        if (INDEX == 16) return nätverk_Stack.peer_portnummer(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int namn_storlek = MATRIS_längd(가), data_storlek = MATRIS_längd(SEKUND_operand);
            if (namn_storlek < 0 || data_storlek < 0) return -14;
            if (namn_storlek < 1 || namn_storlek > 64) return -22;
            int längd_värde = 0;
            while (längd_värde < namn_storlek && körning_Ansvarig.nummer(가 + 4 + längd_värde * 4) != 0) {
                Minne_filsystem.Namn[längd_värde] = körning_Ansvarig.nummer(가 + 4 + längd_värde * 4);
                längd_värde++;
            }
            if (!Minne_filsystem.check_namn(Minne_filsystem.Namn, längd_värde)) return -22;
            if (INDEX == 20) {
                int filnamn = Minne_filsystem.Sök_post(Minne_filsystem.Namn, längd_värde);
                if (filnamn < 0) return filnamn;
                int Storlek = Minne_filsystem.storlek_ange[filnamn];
                if (Storlek > data_storlek) return -90;
                int Adress = enhet_värde.fil_Minne() + filnamn * Minne_filsystem.최대크기;
                for (int nummer = 0; nummer < Storlek; nummer++) körning_Ansvarig.skriva_nummer(SEKUND_operand + 4 + nummer * 4, enhet_värde.läsa_Minne(Adress + nummer));
                return Storlek;
            }
            if (다 < 0 || 다 > data_storlek) return -22;
            if (다 > Minne_filsystem.최대크기) return -90;
            for (int nummer = 0; nummer < 다; nummer++) Minne_filsystem.ändring_värde[nummer] = körning_Ansvarig.nummer(SEKUND_operand + 4 + nummer * 4) & 255;
            return Minne_filsystem.Store_värde(Minne_filsystem.Namn, längd_värde, Minne_filsystem.ändring_värde, 다);
        }
        return -38;
    }
}
