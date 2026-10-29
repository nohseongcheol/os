// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] bevitel_adat = new int[16384], kimenet_adat = new int[16384];
    static int bevitel_hossz, bevitel_pozíció, kimenet_hossz, bemeneti_fájl = -1, kimeneti_fájl = -1;
    static boolean átad_bevitel, átad_kimenet;
    static int hiba_ÉRTÉK;
    static boolean engedélyez_interaktív = true;
    public static int informatikai_részleg_interaktív() { return engedélyez_interaktív && bemeneti_fájl < 3 && kimeneti_fájl < 3 && !átad_bevitel && !átad_kimenet ? 1 : 0; }
    public static int Kimenet(int Csatorna_ÉRTÉK, int ÉRTÉK) {
        if (Csatorna_ÉRTÉK != 1) return 0;
        if (kimeneti_fájl >= 3) { int 처리값 = Memória_Files.Írás(kimeneti_fájl, ÉRTÉK); if (처리값 < 0) hiba_ÉRTÉK = 처리값; return 1; }
        if (!átad_kimenet) return 0;
        if (kimenet_hossz == kimenet_adat.length) hiba_ÉRTÉK = -28;
        else kimenet_adat[kimenet_hossz++] = ÉRTÉK;
        return 1;
    }
    public static int bevitel_ÉRTÉK() {
        if (bemeneti_fájl >= 3) { int 처리값 = Memória_Files.Olvasás(bemeneti_fájl); return 처리값 == 256 ? -2 : 처리값; }
        if (átad_bevitel) return bevitel_pozíció < bevitel_hossz ? bevitel_adat[bevitel_pozíció++] : -2;
        return -3; // UART로 Előre_ÉRTÉK
    }
    static void Futtatás(boolean sorköz_átad, boolean 뒤파이프) {
        átad_bevitel = sorköz_átad; átad_kimenet = 뒤파이프;
        bevitel_pozíció = 0; kimenet_hossz = 0; bemeneti_fájl = -1; kimeneti_fájl = -1; hiba_ÉRTÉK = 0;
    }
    static void 끝() {
        fal.입출력전환(0);
        if (bemeneti_fájl >= 3) Memória_Files.Bezárás(bemeneti_fájl);
        if (kimeneti_fájl >= 3) Memória_Files.Bezárás(kimeneti_fájl);
        if (átad_kimenet) { bevitel_hossz = kimenet_hossz; for (int Loop_INDEX = 0; Loop_INDEX < kimenet_hossz; Loop_INDEX++) bevitel_adat[Loop_INDEX] = kimenet_adat[Loop_INDEX]; }
        bemeneti_fájl = -1; kimeneti_fájl = -1; átad_bevitel = false; átad_kimenet = false;
    }
}
