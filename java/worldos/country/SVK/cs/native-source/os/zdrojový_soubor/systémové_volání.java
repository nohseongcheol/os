// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 uživatelský_prostor ukazatel/길이는 přístup_položka 전에 검사한다. */
public final class systémové_volání {
    static int[] 임시자료 = new int[1024];

    static int pole_délka(int Adresa) {
        if (!spuštění_Správce.oříznout(Adresa, 4)) return -14;
        int délka_HODNOTA = spuštění_Správce.číslo(Adresa);
        if (délka_HODNOTA < 0 || délka_HODNOTA > (spuštění_Správce.uživatel_konec - Adresa - 4) / 4) return -14;
        return délka_HODNOTA;
    }

    public static int Proces_HODNOTA_položka(int INDEX, int 가, int SEKUNDA_operand, int 다, int 라, int 마) {
        if (INDEX == 30) return Soubor_popisovač_Správce.otevřít_Soubor(가, SEKUNDA_operand, 다);
        if (INDEX == 31) return Soubor_popisovač_Správce.파일읽기(가, SEKUNDA_operand, 다);
        if (INDEX == 32) return Soubor_popisovač_Správce.zápis_Soubor(가, SEKUNDA_operand, 다);
        if (INDEX == 33) return Soubor_popisovač_Správce.Zavřít_Soubor(가);
        if (INDEX == 34) return Soubor_popisovač_Správce.hledat_Soubor(가, SEKUNDA_operand, 다);
        if (INDEX == 35) return Soubor_popisovač_Správce.duplikát_popisovač(가, 0, false, 0);
        if (INDEX == 36) return Soubor_popisovač_Správce.duplikát_popisovač(가, SEKUNDA_operand, true, 0);
        if (INDEX == 37) return Soubor_popisovač_Správce.파일상태읽기(가, SEKUNDA_operand);
        if (INDEX == 38) return Soubor_popisovač_Správce.odebrat_Soubor_položka_název(가);
        if (INDEX == 39) return Soubor_popisovač_Správce.sada_Soubor_délka(가, SEKUNDA_operand);
        if (INDEX == 40) return Soubor_popisovač_Správce.řízení_popisovač(가, SEKUNDA_operand, 다);
        if (INDEX == 41) return Soubor_popisovač_Správce.Create_účastník(가, SEKUNDA_operand, 다);
        if (INDEX == 42) return Soubor_popisovač_Správce.vázat_ODKAZ(가, SEKUNDA_operand, 다);
        if (INDEX == 43) return Soubor_popisovač_Správce.poslat_datagram_data(가, SEKUNDA_operand, 다, 라, 마);
        if (INDEX == 44) return Soubor_popisovač_Správce.dostat_datagram_data(가, SEKUNDA_operand, 다, 라, 마);
        if (INDEX == 45) return Soubor_popisovač_Správce.통신주소읽기(가, SEKUNDA_operand, 다);
        if (INDEX == 46) return Soubor_popisovač_Správce.sada_dostat_TIMEOUT(가, SEKUNDA_operand);
        if (INDEX == 47) {
            int popisovač_HODNOTA = Soubor_popisovač_Správce.NAJÍT_popisovač(가);
            if (popisovač_HODNOTA < 0) return -9;
            if (Soubor_popisovač_Správce.Druh_HODNOTA[popisovač_HODNOTA] != 2) return -22;
            return 파일보존.synchronizovat();
        }
        if (INDEX == 1) {
            int délka_HODNOTA = pole_délka(가);
            if (délka_HODNOTA < 0) return délka_HODNOTA;
            if (délka_HODNOTA > 4096) return -90;
            for (int znak_HODNOTA = 0; znak_HODNOTA < délka_HODNOTA; znak_HODNOTA++) SMS_Terminál.문자(spuštění_Správce.číslo(가 + 4 + znak_HODNOTA * 4) & 65535);
            return délka_HODNOTA;
        }
        if (INDEX == 2) return spuštění_Správce.argument_POČET;
        if (INDEX == 3) return 가 >= 0 && 가 < spuštění_Správce.argument_POČET ? spuštění_Správce.argument_ODKAZ[가] : 0;
        if (INDEX == 10) return síť_Štos.Otevřít(가);
        if (INDEX == 11) {
            int délka_HODNOTA = pole_délka(라);
            if (délka_HODNOTA < 0) return délka_HODNOTA;
            if (마 < 0 || 마 > délka_HODNOTA || 마 > 1024) return -90;
            for (int pozice = 0; pozice < 마; pozice++) 임시자료[pozice] = spuštění_Správce.číslo(라 + 4 + pozice * 4) & 255;
            return síť_Štos.poslat(가, SEKUNDA_operand, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int délka_HODNOTA = pole_délka(SEKUNDA_operand);
            if (délka_HODNOTA < 0) return délka_HODNOTA;
            if (다 < 0 || 다 > 2000) return -22;
            int VÝSLEDEK = síť_Štos.dostat(가, 임시자료, délka_HODNOTA < 1024 ? délka_HODNOTA : 1024, 다);
            if (VÝSLEDEK >= 0) for (int pozice = 0; pozice < VÝSLEDEK; pozice++) spuštění_Správce.zápis_číslo(SEKUNDA_operand + 4 + pozice * 4, 임시자료[pozice]);
            return VÝSLEDEK;
        }
        if (INDEX == 13) return síť_Štos.Zavřené(가);
        if (INDEX == 14) return síť_Štos.내주소;
        if (INDEX == 15) return síť_Štos.partner_ODKAZ(가);
        if (INDEX == 16) return síť_Štos.partner_číslo_portu(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminál.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int název_změnit_velikost = pole_délka(가), data_změnit_velikost = pole_délka(SEKUNDA_operand);
            if (název_změnit_velikost < 0 || data_změnit_velikost < 0) return -14;
            if (název_změnit_velikost < 1 || název_změnit_velikost > 64) return -22;
            int délka_HODNOTA = 0;
            while (délka_HODNOTA < název_změnit_velikost && spuštění_Správce.číslo(가 + 4 + délka_HODNOTA * 4) != 0) {
                Paměť_systém_souborů.Název[délka_HODNOTA] = spuštění_Správce.číslo(가 + 4 + délka_HODNOTA * 4);
                délka_HODNOTA++;
            }
            if (!Paměť_systém_souborů.šek_název(Paměť_systém_souborů.Název, délka_HODNOTA)) return -22;
            if (INDEX == 20) {
                int název_souboru = Paměť_systém_souborů.NAJÍT_položka(Paměť_systém_souborů.Název, délka_HODNOTA);
                if (název_souboru < 0) return název_souboru;
                int Velikost = Paměť_systém_souborů.změnit_velikost_Seznam[název_souboru];
                if (Velikost > data_změnit_velikost) return -90;
                int Adresa = mobilní_HODNOTA.Soubor_Paměť() + název_souboru * Paměť_systém_souborů.최대크기;
                for (int číslo = 0; číslo < Velikost; číslo++) spuštění_Správce.zápis_číslo(SEKUNDA_operand + 4 + číslo * 4, mobilní_HODNOTA.기억읽기(Adresa + číslo));
                return Velikost;
            }
            if (다 < 0 || 다 > data_změnit_velikost) return -22;
            if (다 > Paměť_systém_souborů.최대크기) return -90;
            for (int číslo = 0; číslo < 다; číslo++) Paměť_systém_souborů.úprava_HODNOTA[číslo] = spuštění_Správce.číslo(SEKUNDA_operand + 4 + číslo * 4) & 255;
            return Paměť_systém_souborů.Store_HODNOTA(Paměť_systém_souborů.Název, délka_HODNOTA, Paměť_systém_souborů.úprava_HODNOTA, 다);
        }
        return -38;
    }
}
