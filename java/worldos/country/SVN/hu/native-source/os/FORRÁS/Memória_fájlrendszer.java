// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Fájl. 원본 szerkeszt_ÉRTÉK/épít_forrás hiba_ÉRTÉK 시 기존 파일을 보존한다. */
public final class Memória_fájlrendszer {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] méretez_Lista = new int[8];
    static int[] készít_DARAB = new int[8], 허가들 = new int[8];
    static int[] Név = new int[64];
    static int[] szerkeszt_ÉRTÉK = new int[최대크기];
    static boolean 편집중 = false;
    static boolean túlfolyás_ÉRTÉK = false;
    static int szerkeszt_méretez = 0;

    static boolean csekk_név(int[] karakter_ÉRTÉK, int hossz_ÉRTÉK) {
        if (hossz_ÉRTÉK < 1 || hossz_ÉRTÉK > 63) return false;
        for (int szám = 0; szám < hossz_ÉRTÉK; szám++) {
            int ÉRTÉK = karakter_ÉRTÉK[szám];
            if (!(ÉRTÉK >= 'a' && ÉRTÉK <= 'z') && !(ÉRTÉK >= 'A' && ÉRTÉK <= 'Z')
                && !(ÉRTÉK >= '0' && ÉRTÉK <= '9') && ÉRTÉK != '_' && ÉRTÉK != '-' && ÉRTÉK != '.') return false;
        }
        return karakter_ÉRTÉK[0] != '.';
    }

    static int keres_bejegyzés(int[] karakter_ÉRTÉK, int hossz_ÉRTÉK) {
        if (!csekk_név(karakter_ÉRTÉK, hossz_ÉRTÉK)) return -22;
        for (int szám = 0; szám < 8; szám++) {
            boolean 같음 = 이름들[szám * 64 + hossz_ÉRTÉK] == 0;
            for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < hossz_ÉRTÉK; tárolóhely_bejegyzés++) if (이름들[szám * 64 + tárolóhely_bejegyzés] != karakter_ÉRTÉK[tárolóhely_bejegyzés]) 같음 = false;
            if (같음) return szám;
        }
        return -2;
    }

    static int tár_ÉRTÉK(int[] karakter_ÉRTÉK, int hossz_ÉRTÉK, int[] adat, int Méret) {
        if (!csekk_név(karakter_ÉRTÉK, hossz_ÉRTÉK) || Méret < 0 || Méret > adat.length) return -22;
        if (Méret > 최대크기) return -90;
        int INDEX = keres_bejegyzés(karakter_ÉRTÉK, hossz_ÉRTÉK);
        if (INDEX == -2) {
            for (int szám = 0; szám < 8 && INDEX < 0; szám++) if (이름들[szám * 64] == 0 && készít_DARAB[szám] == 0) INDEX = szám;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int CÍM = mobil_ÉRTÉK.Fájl_Memória() + INDEX * 최대크기;
        for (int szám = 0; szám < Méret; szám++) mobil_ÉRTÉK.ír_Memória(CÍM + szám, adat[szám]);
        for (int szám = 0; szám < 64; szám++) 이름들[INDEX * 64 + szám] = szám < hossz_ÉRTÉK ? karakter_ÉRTÉK[szám] : 0;
        méretez_Lista[INDEX] = Méret;
        return Méret;
    }

    static void bejegyzés_Lista() {
        for (int szám = 0; szám < 8; szám++) if (이름들[szám * 64] != 0) {
            for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 64 && 이름들[szám * 64 + tárolóhely_bejegyzés] != 0; tárolóhely_bejegyzés++) SMS_Terminál.문자(이름들[szám * 64 + tárolóhely_bejegyzés]);
            SMS_Terminál.Írás("  "); SMS_Terminál.ír_szám(méretez_Lista[szám]); SMS_Terminál.Írás("bájt_ÉRTÉK\n");
        }
        SMS_Terminál.Írás(tárolóeszköz_ismerős.informatikai_részleg_Aktív_9e72441a ? "Fájl 8칸, 파일당 16384바이트; sync로 tár_ÉRTÉK 장치에 보존\n"
            : "임시 Fájl 8칸, 파일당 16384바이트; újrapróbál_ÉRTÉK 시작하면 사라짐\n");
    }

    static void Parancs(int[] bevitel_ÉRTÉK, int Futtatás, int hossz_ÉRTÉK, int Művelet) {
        while (Futtatás < hossz_ÉRTÉK && bevitel_ÉRTÉK[Futtatás] == ' ') Futtatás++;
        int 끝 = hossz_ÉRTÉK;
        while (끝 > Futtatás && bevitel_ÉRTÉK[끝 - 1] == ' ') 끝--;
        int szám = 끝 - Futtatás;
        if (szám < 1 || szám > 63) { SMS_Terminál.Írás("올바르지 않은 Fájl Név\n"); return; }
        for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 64; tárolóhely_bejegyzés++) Név[tárolóhely_bejegyzés] = tárolóhely_bejegyzés < szám ? bevitel_ÉRTÉK[Futtatás + tárolóhely_bejegyzés] : 0;
        int INDEX = keres_bejegyzés(Név, szám);
        if (INDEX == -22) { SMS_Terminál.Írás("올바르지 않은 Fájl Név\n"); return; }
        if (Művelet == 0) {
            편집중 = true; szerkeszt_méretez = 0; túlfolyás_ÉRTÉK = false;
            SMS_Terminál.Írás("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminál.Írás("파일을 찾을 szám 없습니다\n");
        else if (Művelet == 1) {
            int CÍM = mobil_ÉRTÉK.Fájl_Memória() + INDEX * 최대크기;
            for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < méretez_Lista[INDEX]; tárolóhely_bejegyzés++) SMS_Terminál.문자(mobil_ÉRTÉK.기억읽기(CÍM + tárolóhely_bejegyzés));
            SMS_Terminál.문자(10);
        } else { 이름들[INDEX * 64] = 0; méretez_Lista[INDEX] = 0; SMS_Terminál.Írás("파일을 지웠습니다\n"); }
    }

    static boolean informatikai_részleg_AZONOS(int[] bevitel_ÉRTÉK, int hossz_ÉRTÉK, String 문구) {
        if (hossz_ÉRTÉK != 문구.length()) return false;
        for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < hossz_ÉRTÉK; tárolóhely_bejegyzés++) if (bevitel_ÉRTÉK[tárolóhely_bejegyzés] != 문구.charAt(tárolóhely_bejegyzés)) return false;
        return true;
    }

    static void Szerkesztett_sor(int[] bevitel_ÉRTÉK, int hossz_ÉRTÉK, boolean sor_túlfolyás) {
        if (informatikai_részleg_AZONOS(bevitel_ÉRTÉK, hossz_ÉRTÉK, ".cancel")) {
            편집중 = false; SMS_Terminál.Írás("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (informatikai_részleg_AZONOS(bevitel_ÉRTÉK, hossz_ÉRTÉK, ".save")) {
            편집중 = false;
            if (túlfolyás_ÉRTÉK) { SMS_Terminál.Írás("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int szám = 0;
            while (szám < 64 && Név[szám] != 0) szám++;
            int KR = tár_ÉRTÉK(Név, szám, szerkeszt_ÉRTÉK, szerkeszt_méretez);
            SMS_Terminál.Írás(KR >= 0 ? "보존한 bájt_ÉRTÉK szám: " : "보존 hiba_ÉRTÉK: ");
            SMS_Terminál.ír_szám(KR); SMS_Terminál.문자(10);
        } else if (sor_túlfolyás || hossz_ÉRTÉK + 1 > 최대크기 - szerkeszt_méretez) túlfolyás_ÉRTÉK = true;
        else {
            for (int szám = 0; szám < hossz_ÉRTÉK; szám++) szerkeszt_ÉRTÉK[szerkeszt_méretez++] = bevitel_ÉRTÉK[szám];
            szerkeszt_ÉRTÉK[szerkeszt_méretez++] = 10;
        }
    }

    static void 예제(String Fájl, String Tartalom_ÉRTÉK) {
        for (int szám = 0; szám < 64; szám++) Név[szám] = szám < Fájl.length() ? Fájl.charAt(szám) : 0;
        for (int szám = 0; szám < Tartalom_ÉRTÉK.length(); szám++) szerkeszt_ÉRTÉK[szám] = Tartalom_ÉRTÉK.charAt(szám);
        tár_ÉRTÉK(Név, Fájl.length(), szerkeszt_ÉRTÉK, Tartalom_ÉRTÉK.length());
    }

    static void Előkészítés() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Csoport_ÉRTÉK = mobil_ÉRTÉK.자바파일묶음(), Méret = mobil_ÉRTÉK.자바파일묶음크기();
        if (Méret < 8 || végrehajtás_kezelő.szám(Csoport_ÉRTÉK) != 0x464a4b4a) { SMS_Terminál.Írás("올바르지 않은 Java Fájl Csoport_ÉRTÉK\n"); return; }
        int cikk_DARAB = végrehajtás_kezelő.szám(Csoport_ÉRTÉK + 4);
        if (cikk_DARAB < 0 || cikk_DARAB > 8 || cikk_DARAB > (Méret - 8) / 72) { SMS_Terminál.Írás("올바르지 않은 Java Fájl bejegyzés_Lista\n"); return; }
        for (int szám = 0; szám < cikk_DARAB; szám++) {
            int bejegyzés_ÉRTÉK = Csoport_ÉRTÉK + 8 + szám * 72, hossz_ÉRTÉK = 0;
            for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 64; tárolóhely_bejegyzés++) Név[tárolóhely_bejegyzés] = mobil_ÉRTÉK.기억읽기(bejegyzés_ÉRTÉK + tárolóhely_bejegyzés);
            while (hossz_ÉRTÉK < 64 && Név[hossz_ÉRTÉK] != 0) hossz_ÉRTÉK++;
            int Pozíció = végrehajtás_kezelő.szám(bejegyzés_ÉRTÉK + 64), fájlméret = végrehajtás_kezelő.szám(bejegyzés_ÉRTÉK + 68);
            if (!csekk_név(Név, hossz_ÉRTÉK) || fájlméret < 0 || fájlméret > 최대크기 || Pozíció < 8 + cikk_DARAB * 72 || Pozíció > Méret - fájlméret) {
                SMS_Terminál.Írás("올바르지 않은 Java Fájl bejegyzés_ÉRTÉK\n"); return;
            }
            for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < fájlméret; tárolóhely_bejegyzés++) szerkeszt_ÉRTÉK[tárolóhely_bejegyzés] = mobil_ÉRTÉK.기억읽기(Csoport_ÉRTÉK + Pozíció + tárolóhely_bejegyzés);
            if (tár_ÉRTÉK(Név, hossz_ÉRTÉK, szerkeszt_ÉRTÉK, fájlméret) < 0) { SMS_Terminál.Írás("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
