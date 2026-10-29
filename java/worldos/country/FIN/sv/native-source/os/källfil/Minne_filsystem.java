// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 filnamn. 원본 ändring_värde/kompilera_källa fel_värde 시 기존 파일을 보존한다. */
public final class Minne_filsystem {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] storlek_ange = new int[8];
    static int[] skapa_ANTAL = new int[8], 허가들 = new int[8];
    static int[] Namn = new int[64];
    static int[] ändring_värde = new int[최대크기];
    static boolean 편집중 = false;
    static boolean spill_värde = false;
    static int ändring_storlek = 0;

    static boolean check_namn(int[] tecken_värde, int längd_värde) {
        if (längd_värde < 1 || längd_värde > 63) return false;
        for (int nummer = 0; nummer < längd_värde; nummer++) {
            int värde = tecken_värde[nummer];
            if (!(värde >= 'a' && värde <= 'z') && !(värde >= 'A' && värde <= 'Z')
                && !(värde >= '0' && värde <= '9') && värde != '_' && värde != '-' && värde != '.') return false;
        }
        return tecken_värde[0] != '.';
    }

    static int Sök_post(int[] tecken_värde, int längd_värde) {
        if (!check_namn(tecken_värde, längd_värde)) return -22;
        for (int nummer = 0; nummer < 8; nummer++) {
            boolean 같음 = 이름들[nummer * 64 + längd_värde] == 0;
            for (int fack_post = 0; fack_post < längd_värde; fack_post++) if (이름들[nummer * 64 + fack_post] != tecken_värde[fack_post]) 같음 = false;
            if (같음) return nummer;
        }
        return -2;
    }

    static int Store_värde(int[] tecken_värde, int längd_värde, int[] data, int Storlek) {
        if (!check_namn(tecken_värde, längd_värde) || Storlek < 0 || Storlek > data.length) return -22;
        if (Storlek > 최대크기) return -90;
        int INDEX = Sök_post(tecken_värde, längd_värde);
        if (INDEX == -2) {
            for (int nummer = 0; nummer < 8 && INDEX < 0; nummer++) if (이름들[nummer * 64] == 0 && skapa_ANTAL[nummer] == 0) INDEX = nummer;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int Adress = enhet_värde.fil_Minne() + INDEX * 최대크기;
        for (int nummer = 0; nummer < Storlek; nummer++) enhet_värde.skriva_Minne(Adress + nummer, data[nummer]);
        for (int nummer = 0; nummer < 64; nummer++) 이름들[INDEX * 64 + nummer] = nummer < längd_värde ? tecken_värde[nummer] : 0;
        storlek_ange[INDEX] = Storlek;
        return Storlek;
    }

    static void post_ange() {
        for (int nummer = 0; nummer < 8; nummer++) if (이름들[nummer * 64] != 0) {
            for (int fack_post = 0; fack_post < 64 && 이름들[nummer * 64 + fack_post] != 0; fack_post++) SMS_Terminal.문자(이름들[nummer * 64 + fack_post]);
            SMS_Terminal.Skriv("  "); SMS_Terminal.skriva_nummer(storlek_ange[nummer]); SMS_Terminal.Skriv("byte_värde\n");
        }
        SMS_Terminal.Skriv(lagringsenhet_kontakt.informationsteknik_Aktiv_9e72441a ? "filnamn 8칸, 파일당 16384바이트; sync로 Store_värde 장치에 보존\n"
            : "임시 filnamn 8칸, 파일당 16384바이트; försöka_igen_värde 시작하면 사라짐\n");
    }

    static void kommando(int[] indata_värde, int Kör, int längd_värde, int Åtgärd) {
        while (Kör < längd_värde && indata_värde[Kör] == ' ') Kör++;
        int 끝 = längd_värde;
        while (끝 > Kör && indata_värde[끝 - 1] == ' ') 끝--;
        int nummer = 끝 - Kör;
        if (nummer < 1 || nummer > 63) { SMS_Terminal.Skriv("올바르지 않은 filnamn Namn\n"); return; }
        for (int fack_post = 0; fack_post < 64; fack_post++) Namn[fack_post] = fack_post < nummer ? indata_värde[Kör + fack_post] : 0;
        int INDEX = Sök_post(Namn, nummer);
        if (INDEX == -22) { SMS_Terminal.Skriv("올바르지 않은 filnamn Namn\n"); return; }
        if (Åtgärd == 0) {
            편집중 = true; ändring_storlek = 0; spill_värde = false;
            SMS_Terminal.Skriv("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminal.Skriv("파일을 찾을 nummer 없습니다\n");
        else if (Åtgärd == 1) {
            int Adress = enhet_värde.fil_Minne() + INDEX * 최대크기;
            for (int fack_post = 0; fack_post < storlek_ange[INDEX]; fack_post++) SMS_Terminal.문자(enhet_värde.läsa_Minne(Adress + fack_post));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; storlek_ange[INDEX] = 0; SMS_Terminal.Skriv("파일을 지웠습니다\n"); }
    }

    static boolean informationsteknik_EXAKT(int[] indata_värde, int längd_värde, String 문구) {
        if (längd_värde != 문구.length()) return false;
        for (int fack_post = 0; fack_post < längd_värde; fack_post++) if (indata_värde[fack_post] != 문구.charAt(fack_post)) return false;
        return true;
    }

    static void Redigerat_rad(int[] indata_värde, int längd_värde, boolean rad_spill) {
        if (informationsteknik_EXAKT(indata_värde, längd_värde, ".cancel")) {
            편집중 = false; SMS_Terminal.Skriv("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (informationsteknik_EXAKT(indata_värde, längd_värde, ".save")) {
            편집중 = false;
            if (spill_värde) { SMS_Terminal.Skriv("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int nummer = 0;
            while (nummer < 64 && Namn[nummer] != 0) nummer++;
            int RESULTAT = Store_värde(Namn, nummer, ändring_värde, ändring_storlek);
            SMS_Terminal.Skriv(RESULTAT >= 0 ? "보존한 byte_värde nummer: " : "보존 fel_värde: ");
            SMS_Terminal.skriva_nummer(RESULTAT); SMS_Terminal.문자(10);
        } else if (rad_spill || längd_värde + 1 > 최대크기 - ändring_storlek) spill_värde = true;
        else {
            for (int nummer = 0; nummer < längd_värde; nummer++) ändring_värde[ändring_storlek++] = indata_värde[nummer];
            ändring_värde[ändring_storlek++] = 10;
        }
    }

    static void 예제(String filnamn, String Innehåll_värde) {
        for (int nummer = 0; nummer < 64; nummer++) Namn[nummer] = nummer < filnamn.length() ? filnamn.charAt(nummer) : 0;
        for (int nummer = 0; nummer < Innehåll_värde.length(); nummer++) ändring_värde[nummer] = Innehåll_värde.charAt(nummer);
        Store_värde(Namn, filnamn.length(), ändring_värde, Innehåll_värde.length());
    }

    static void Förbereda() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int grupp_värde = enhet_värde.자바파일묶음(), Storlek = enhet_värde.자바파일묶음크기();
        if (Storlek < 8 || körning_Ansvarig.nummer(grupp_värde) != 0x464a4b4a) { SMS_Terminal.Skriv("올바르지 않은 Java filnamn grupp_värde\n"); return; }
        int objekt_ANTAL = körning_Ansvarig.nummer(grupp_värde + 4);
        if (objekt_ANTAL < 0 || objekt_ANTAL > 8 || objekt_ANTAL > (Storlek - 8) / 72) { SMS_Terminal.Skriv("올바르지 않은 Java filnamn post_ange\n"); return; }
        for (int nummer = 0; nummer < objekt_ANTAL; nummer++) {
            int post_värde = grupp_värde + 8 + nummer * 72, längd_värde = 0;
            for (int fack_post = 0; fack_post < 64; fack_post++) Namn[fack_post] = enhet_värde.läsa_Minne(post_värde + fack_post);
            while (längd_värde < 64 && Namn[längd_värde] != 0) längd_värde++;
            int position = körning_Ansvarig.nummer(post_värde + 64), filstorlek = körning_Ansvarig.nummer(post_värde + 68);
            if (!check_namn(Namn, längd_värde) || filstorlek < 0 || filstorlek > 최대크기 || position < 8 + objekt_ANTAL * 72 || position > Storlek - filstorlek) {
                SMS_Terminal.Skriv("올바르지 않은 Java filnamn post_värde\n"); return;
            }
            for (int fack_post = 0; fack_post < filstorlek; fack_post++) ändring_värde[fack_post] = enhet_värde.läsa_Minne(grupp_värde + position + fack_post);
            if (Store_värde(Namn, längd_värde, ändring_värde, filstorlek) < 0) { SMS_Terminal.Skriv("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
