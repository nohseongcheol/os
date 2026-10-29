// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 e_mailen_WAARDE 버퍼와 8KiB ontvangen_WAARDE lus_WAARDE. 인터럽트 대신 폴링한다. */
public final class net_stuurprogramma {
    static int 입출력기준주소 = 0;
    static int ontvangen_functie = 0, 송신칸 = 0;
    static int[] mobiel_ADRES = new int[6];
    static int 송신수 = 0, ontvangen_AANTAL = 0, fout_AANTAL = 0;

    static int 설정읽기(int mobiel_nummer, int positie) {
        mobiel_WAARDE.입출력정수쓰기(0xcf8, 0x80000000 | (mobiel_nummer << 11) | positie);
        return mobiel_WAARDE.입출력정수읽기(0xcfc);
    }

    static boolean Bereid_voor() {
        int mobiel_nummer = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { mobiel_nummer = INDEX; break; }
        }
        if (mobiel_nummer < 0) return false;
        int standaardwaarde = 설정읽기(mobiel_nummer, 0x10);
        if ((standaardwaarde & 1) == 0 || (standaardwaarde & 0xfffffffc) < 0x100 || (standaardwaarde & 0xfffffffc) > 65535) return false;
        입출력기준주소 = standaardwaarde & 0xfffc;
        int opdracht = 설정읽기(mobiel_nummer, 4);
        mobiel_WAARDE.입출력정수쓰기(0xcf8, 0x80000004 | (mobiel_nummer << 11));
        mobiel_WAARDE.입출력짧은수쓰기(0xcfc, opdracht | 5); // I/O 및 bus master Toestaan_WAARDE, PCI Status_WAARDE 비트는 건드리지 않음
        mobiel_WAARDE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!opnieuw_instellen_WAARDE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) mobiel_ADRES[INDEX] = mobiel_WAARDE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean opnieuw_instellen_WAARDE() {
        mobiel_WAARDE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int starten = mobiel_WAARDE.밀리초();
        while ((mobiel_WAARDE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (mobiel_WAARDE.밀리초() - starten > 100) return false;
        ontvangen_functie = 0; 송신칸 = 0;
        mobiel_WAARDE.입출력정수쓰기(입출력기준주소 + 0x30, mobiel_WAARDE.net_Geheugen());
        for (int INDEX = 0; INDEX < 4; INDEX++) mobiel_WAARDE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, mobiel_WAARDE.net_Geheugen() + 12288);
        mobiel_WAARDE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        mobiel_WAARDE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        mobiel_WAARDE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        mobiel_WAARDE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/broadcast_WAARDE, wrap 연속 Store_WAARDE, 8KiB
        mobiel_WAARDE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int e_mailen(int[] gegevens, int tijdsduur_WAARDE) {
        if (입출력기준주소 == 0) return -19;
        if (tijdsduur_WAARDE < 14 || tijdsduur_WAARDE > 1514) return -90;
        int status_poort = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int starten = mobiel_WAARDE.밀리초();
        while ((mobiel_WAARDE.입출력정수읽기(status_poort) & 0x2000) == 0)
            if (mobiel_WAARDE.밀리초() - starten > 100) return -110;
        int Grootte = tijdsduur_WAARDE < 60 ? 60 : tijdsduur_WAARDE;
        for (int INDEX = 0; INDEX < Grootte; INDEX++)
            mobiel_WAARDE.schrijven_Geheugen(mobiel_WAARDE.net_Geheugen() + 12288 + INDEX, INDEX < tijdsduur_WAARDE ? gegevens[INDEX] : 0);
        mobiel_WAARDE.입출력정수쓰기(status_poort, Grootte | 0x00080000);
        starten = mobiel_WAARDE.밀리초();
        while ((mobiel_WAARDE.입출력정수읽기(status_poort) & 0xe0008000) == 0)
            if (mobiel_WAARDE.밀리초() - starten > 100) return -110;
        if ((mobiel_WAARDE.입출력정수읽기(status_poort) & 0x8000) == 0) { fout_AANTAL++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return tijdsduur_WAARDE;
    }

    static int ontvangen(int[] gegevens) {
        if (입출력기준주소 == 0) return 0;
        if ((mobiel_WAARDE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            fout_AANTAL++;
            if (!opnieuw_instellen_WAARDE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((mobiel_WAARDE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int kop_WAARDE = mobiel_WAARDE.net_Geheugen() + ontvangen_functie;
        int Status_WAARDE = uitvoerbewerking_Manager.짧은수(kop_WAARDE), Grootte = uitvoerbewerking_Manager.짧은수(kop_WAARDE + 2);
        if (Grootte == 0xfff0) return 0; // DMA 진행 중
        if (Grootte < 4 || Grootte > 1518) {
            fout_AANTAL++;
            if (!opnieuw_instellen_WAARDE()) 입출력기준주소 = 0;
            return 0;
        }
        int tijdsduur_WAARDE = Grootte - 4;
        if ((Status_WAARDE & 1) != 0) {
            for (int INDEX = 0; INDEX < tijdsduur_WAARDE; INDEX++) gegevens[INDEX] = mobiel_WAARDE.기억읽기(kop_WAARDE + 4 + INDEX);
            ontvangen_AANTAL++;
        } else { tijdsduur_WAARDE = 0; fout_AANTAL++; }
        ontvangen_functie = (ontvangen_functie + Grootte + 4 + 3) & ~3;
        ontvangen_functie &= 8191;
        mobiel_WAARDE.입출력짧은수쓰기(입출력기준주소 + 0x38, (ontvangen_functie - 16) & 65535);
        mobiel_WAARDE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return tijdsduur_WAARDE;
    }
}
