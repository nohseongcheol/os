// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 felület Állapot_ÉRTÉK. Fájl 저장소는 공유하고 ÚTVONAL/változó_ÉRTÉK/LOG_REKORD/입력은 분리한다. */
public final class ablak_munkamenet {
    static int[] 보관 = new int[4 * 30000], Előkészítés = new int[4];
    static int aktuális_cikk, Pozíció;
    static boolean 이어읽기;
    static void TÖMB_ÉRTÉK(int[] adat, boolean tár_ÉRTÉK) {
        for (int Loop_INDEX = 0; Loop_INDEX < adat.length; Loop_INDEX++) { if (tár_ÉRTÉK) 보관[Pozíció++] = adat[Loop_INDEX]; else adat[Loop_INDEX] = 보관[Pozíció++]; }
    }
    static int ÉRTÉK(int adat_ÉRTÉK, boolean 저장여부) { if (저장여부) { 보관[Pozíció++] = adat_ÉRTÉK; return adat_ÉRTÉK; } return 보관[Pozíció++]; }
    static void keres_pozíció(int 보관칸, boolean 저장여부) {
        Pozíció = 보관칸 * 30000;
        TÖMB_ÉRTÉK(Memória_Files.aktuális_cikk, 저장여부); Memória_Files.aktuális_hossz = ÉRTÉK(Memória_Files.aktuális_hossz, 저장여부);
        TÖMB_ÉRTÉK(felület_szintaxis.változó_név, 저장여부); TÖMB_ÉRTÉK(felület_szintaxis.változó_adat, 저장여부); TÖMB_ÉRTÉK(felület_szintaxis.이름길이, 저장여부); TÖMB_ÉRTÉK(felület_szintaxis.ÉRTÉK_hossz, 저장여부);
        felület_szintaxis.Állapot_ÉRTÉK = ÉRTÉK(felület_szintaxis.Állapot_ÉRTÉK, 저장여부);
        TÖMB_ÉRTÉK(sorszerkesztő.LOG_REKORD, 저장여부); TÖMB_ÉRTÉK(sorszerkesztő.LOG_hossz, 저장여부); TÖMB_ÉRTÉK(sorszerkesztő.tár_ÉRTÉK, 저장여부); TÖMB_ÉRTÉK(명령해석기.Vonal, 저장여부);
        sorszerkesztő.LOG_DARAB = ÉRTÉK(sorszerkesztő.LOG_DARAB, 저장여부); sorszerkesztő.LOG_REKORD_megszüntet = ÉRTÉK(sorszerkesztő.LOG_REKORD_megszüntet, 저장여부);
        sorszerkesztő.keres_ÉRTÉK = ÉRTÉK(sorszerkesztő.keres_ÉRTÉK, 저장여부); sorszerkesztő.저장길이 = ÉRTÉK(sorszerkesztő.저장길이, 저장여부);
        sorszerkesztő.Méret = ÉRTÉK(sorszerkesztő.Méret, 저장여부); sorszerkesztő.kurzor_ÉRTÉK = ÉRTÉK(sorszerkesztő.kurzor_ÉRTÉK, 저장여부); sorszerkesztő.START_ablak = ÉRTÉK(sorszerkesztő.START_ablak, 저장여부);
        Előkészítés[보관칸] = 1;
    }
    static void folyamat_ÉRTÉK_bejegyzés() {
        int esemény_szám = fal.Terminál(12); if (esemény_szám == 0) return;
        keres_pozíció(aktuális_cikk, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((esemény_szám & (1 << (8 + Loop_INDEX))) != 0) { fal.vezérlő_felhasználó_app(32 + Loop_INDEX); Előkészítés[Loop_INDEX] = 0; }
            if ((esemény_szám & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != aktuális_cikk) Előkészítés[Loop_INDEX] = 0;
        }
        int Tovább_pozíció = (esemény_szám & 15) - 1; if (Tovább_pozíció < 0) Tovább_pozíció = 0;
        if (Előkészítés[Tovább_pozíció] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Tovább_pozíció * 30000 + Loop_INDEX] = 0;
        aktuális_cikk = Tovább_pozíció; keres_pozíció(aktuális_cikk, false); fal.Terminál(100 + aktuális_cikk); 이어읽기 = true;
        단말.Írás("\nTERMINAL FOCUS "); 단말.szám(aktuális_cikk + 1); 단말.문자(10);
    }
    static boolean CV_végrehajtás() {
        if (fal.vezérlő_felhasználó_app(16 + aktuális_cikk) == 0) return false;
        셸입출력.engedélyez_interaktív = true; 셸입출력.Futtatás(false, false); fal.입출력전환(1);
        int 처리값 = fal.vezérlő_felhasználó_app(aktuális_cikk); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; felület_szintaxis.Állapot_ÉRTÉK = 처리값 < 0 ? 126 : 처리값; 단말.Írás("exit "); 단말.szám(처리값); 단말.문자(10); fal.Terminál(3); }
        return true;
    }
}
