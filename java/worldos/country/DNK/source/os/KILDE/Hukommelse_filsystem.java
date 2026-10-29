// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Fil. 원본 Rediger_VÆRDI/kompilere_kilde fejl_VÆRDI 시 기존 파일을 보존한다. */
public final class Hukommelse_filsystem {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] tilpasse_størrelse_Liste = new int[8];
    static int[] åben_TÆL = new int[8], 허가들 = new int[8];
    static int[] Navn = new int[64];
    static int[] Rediger_VÆRDI = new int[최대크기];
    static boolean 편집중 = false;
    static boolean overløb_VÆRDI = false;
    static int Rediger_tilpasse_størrelse = 0;

    static boolean check_navn(int[] tegn_VÆRDI, int varighed_VÆRDI) {
        if (varighed_VÆRDI < 1 || varighed_VÆRDI > 63) return false;
        for (int tal = 0; tal < varighed_VÆRDI; tal++) {
            int VÆRDI = tegn_VÆRDI[tal];
            if (!(VÆRDI >= 'a' && VÆRDI <= 'z') && !(VÆRDI >= 'A' && VÆRDI <= 'Z')
                && !(VÆRDI >= '0' && VÆRDI <= '9') && VÆRDI != '_' && VÆRDI != '-' && VÆRDI != '.') return false;
        }
        return tegn_VÆRDI[0] != '.';
    }

    static int Søg_post(int[] tegn_VÆRDI, int varighed_VÆRDI) {
        if (!check_navn(tegn_VÆRDI, varighed_VÆRDI)) return -22;
        for (int tal = 0; tal < 8; tal++) {
            boolean 같음 = 이름들[tal * 64 + varighed_VÆRDI] == 0;
            for (int udvidelsesstik_post = 0; udvidelsesstik_post < varighed_VÆRDI; udvidelsesstik_post++) if (이름들[tal * 64 + udvidelsesstik_post] != tegn_VÆRDI[udvidelsesstik_post]) 같음 = false;
            if (같음) return tal;
        }
        return -2;
    }

    static int Store_VÆRDI(int[] tegn_VÆRDI, int varighed_VÆRDI, int[] data, int Størrelse) {
        if (!check_navn(tegn_VÆRDI, varighed_VÆRDI) || Størrelse < 0 || Størrelse > data.length) return -22;
        if (Størrelse > 최대크기) return -90;
        int INDEKS = Søg_post(tegn_VÆRDI, varighed_VÆRDI);
        if (INDEKS == -2) {
            for (int tal = 0; tal < 8 && INDEKS < 0; tal++) if (이름들[tal * 64] == 0 && åben_TÆL[tal] == 0) INDEKS = tal;
            if (INDEKS >= 0) 허가들[INDEKS] = 438;
        }
        if (INDEKS < 0) return -28;
        int mail = enhed_VÆRDI.fil_Hukommelse() + INDEKS * 최대크기;
        for (int tal = 0; tal < Størrelse; tal++) enhed_VÆRDI.skrive_Hukommelse(mail + tal, data[tal]);
        for (int tal = 0; tal < 64; tal++) 이름들[INDEKS * 64 + tal] = tal < varighed_VÆRDI ? tegn_VÆRDI[tal] : 0;
        tilpasse_størrelse_Liste[INDEKS] = Størrelse;
        return Størrelse;
    }

    static void post_Liste() {
        for (int tal = 0; tal < 8; tal++) if (이름들[tal * 64] != 0) {
            for (int udvidelsesstik_post = 0; udvidelsesstik_post < 64 && 이름들[tal * 64 + udvidelsesstik_post] != 0; udvidelsesstik_post++) sms_Terminal.문자(이름들[tal * 64 + udvidelsesstik_post]);
            sms_Terminal.Skrive("  "); sms_Terminal.skrive_tal(tilpasse_størrelse_Liste[tal]); sms_Terminal.Skrive("byte_VÆRDI\n");
        }
        sms_Terminal.Skrive(lagerenhed_forbindelse.it_Aktiv_9e72441a ? "Fil 8칸, 파일당 16384바이트; sync로 Store_VÆRDI 장치에 보존\n"
            : "임시 Fil 8칸, 파일당 16384바이트; prøve_igen_VÆRDI 시작하면 사라짐\n");
    }

    static void Kommando(int[] input_VÆRDI, int Kør_2, int varighed_VÆRDI, int Handling) {
        while (Kør_2 < varighed_VÆRDI && input_VÆRDI[Kør_2] == ' ') Kør_2++;
        int 끝 = varighed_VÆRDI;
        while (끝 > Kør_2 && input_VÆRDI[끝 - 1] == ' ') 끝--;
        int tal = 끝 - Kør_2;
        if (tal < 1 || tal > 63) { sms_Terminal.Skrive("올바르지 않은 Fil Navn\n"); return; }
        for (int udvidelsesstik_post = 0; udvidelsesstik_post < 64; udvidelsesstik_post++) Navn[udvidelsesstik_post] = udvidelsesstik_post < tal ? input_VÆRDI[Kør_2 + udvidelsesstik_post] : 0;
        int INDEKS = Søg_post(Navn, tal);
        if (INDEKS == -22) { sms_Terminal.Skrive("올바르지 않은 Fil Navn\n"); return; }
        if (Handling == 0) {
            편집중 = true; Rediger_tilpasse_størrelse = 0; overløb_VÆRDI = false;
            sms_Terminal.Skrive("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEKS < 0) sms_Terminal.Skrive("파일을 찾을 tal 없습니다\n");
        else if (Handling == 1) {
            int mail = enhed_VÆRDI.fil_Hukommelse() + INDEKS * 최대크기;
            for (int udvidelsesstik_post = 0; udvidelsesstik_post < tilpasse_størrelse_Liste[INDEKS]; udvidelsesstik_post++) sms_Terminal.문자(enhed_VÆRDI.기억읽기(mail + udvidelsesstik_post));
            sms_Terminal.문자(10);
        } else { 이름들[INDEKS * 64] = 0; tilpasse_størrelse_Liste[INDEKS] = 0; sms_Terminal.Skrive("파일을 지웠습니다\n"); }
    }

    static boolean it_EKSAKT(int[] input_VÆRDI, int varighed_VÆRDI, String 문구) {
        if (varighed_VÆRDI != 문구.length()) return false;
        for (int udvidelsesstik_post = 0; udvidelsesstik_post < varighed_VÆRDI; udvidelsesstik_post++) if (input_VÆRDI[udvidelsesstik_post] != 문구.charAt(udvidelsesstik_post)) return false;
        return true;
    }

    static void Redigeret_linje(int[] input_VÆRDI, int varighed_VÆRDI, boolean linje_overløb) {
        if (it_EKSAKT(input_VÆRDI, varighed_VÆRDI, ".cancel")) {
            편집중 = false; sms_Terminal.Skrive("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (it_EKSAKT(input_VÆRDI, varighed_VÆRDI, ".save")) {
            편집중 = false;
            if (overløb_VÆRDI) { sms_Terminal.Skrive("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int tal = 0;
            while (tal < 64 && Navn[tal] != 0) tal++;
            int KR = Store_VÆRDI(Navn, tal, Rediger_VÆRDI, Rediger_tilpasse_størrelse);
            sms_Terminal.Skrive(KR >= 0 ? "보존한 byte_VÆRDI tal: " : "보존 fejl_VÆRDI: ");
            sms_Terminal.skrive_tal(KR); sms_Terminal.문자(10);
        } else if (linje_overløb || varighed_VÆRDI + 1 > 최대크기 - Rediger_tilpasse_størrelse) overløb_VÆRDI = true;
        else {
            for (int tal = 0; tal < varighed_VÆRDI; tal++) Rediger_VÆRDI[Rediger_tilpasse_størrelse++] = input_VÆRDI[tal];
            Rediger_VÆRDI[Rediger_tilpasse_størrelse++] = 10;
        }
    }

    static void 예제(String Fil, String Indhold_VÆRDI) {
        for (int tal = 0; tal < 64; tal++) Navn[tal] = tal < Fil.length() ? Fil.charAt(tal) : 0;
        for (int tal = 0; tal < Indhold_VÆRDI.length(); tal++) Rediger_VÆRDI[tal] = Indhold_VÆRDI.charAt(tal);
        Store_VÆRDI(Navn, Fil.length(), Rediger_VÆRDI, Indhold_VÆRDI.length());
    }

    static void Tilrettelæg() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int gruppe_VÆRDI = enhed_VÆRDI.자바파일묶음(), Størrelse = enhed_VÆRDI.자바파일묶음크기();
        if (Størrelse < 8 || udførelse_Leder.tal(gruppe_VÆRDI) != 0x464a4b4a) { sms_Terminal.Skrive("올바르지 않은 Java Fil gruppe_VÆRDI\n"); return; }
        int vare_TÆL = udførelse_Leder.tal(gruppe_VÆRDI + 4);
        if (vare_TÆL < 0 || vare_TÆL > 8 || vare_TÆL > (Størrelse - 8) / 72) { sms_Terminal.Skrive("올바르지 않은 Java Fil post_Liste\n"); return; }
        for (int tal = 0; tal < vare_TÆL; tal++) {
            int post_VÆRDI_962f286b = gruppe_VÆRDI + 8 + tal * 72, varighed_VÆRDI = 0;
            for (int udvidelsesstik_post = 0; udvidelsesstik_post < 64; udvidelsesstik_post++) Navn[udvidelsesstik_post] = enhed_VÆRDI.기억읽기(post_VÆRDI_962f286b + udvidelsesstik_post);
            while (varighed_VÆRDI < 64 && Navn[varighed_VÆRDI] != 0) varighed_VÆRDI++;
            int Placering = udførelse_Leder.tal(post_VÆRDI_962f286b + 64), filstørrelse = udførelse_Leder.tal(post_VÆRDI_962f286b + 68);
            if (!check_navn(Navn, varighed_VÆRDI) || filstørrelse < 0 || filstørrelse > 최대크기 || Placering < 8 + vare_TÆL * 72 || Placering > Størrelse - filstørrelse) {
                sms_Terminal.Skrive("올바르지 않은 Java Fil post_VÆRDI_962f286b\n"); return;
            }
            for (int udvidelsesstik_post = 0; udvidelsesstik_post < filstørrelse; udvidelsesstik_post++) Rediger_VÆRDI[udvidelsesstik_post] = enhed_VÆRDI.기억읽기(gruppe_VÆRDI + Placering + udvidelsesstik_post);
            if (Store_VÆRDI(Navn, varighed_VÆRDI, Rediger_VÆRDI, filstørrelse) < 0) { sms_Terminal.Skrive("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
