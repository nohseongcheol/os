// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Fil. 원본 Rediger_VERDI/kompilere_kilde feil_VERDI 시 기존 파일을 보존한다. */
public final class Minne_filsystem {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] skalere_Liste = new int[8];
    static int[] åpen_ANTALL = new int[8], 허가들 = new int[8];
    static int[] Navn = new int[64];
    static int[] Rediger_VERDI = new int[최대크기];
    static boolean 편집중 = false;
    static boolean overløp_VERDI = false;
    static int Rediger_skalere = 0;

    static boolean sjekk_navn(int[] tegn_VERDI, int lengde_VERDI) {
        if (lengde_VERDI < 1 || lengde_VERDI > 63) return false;
        for (int nummer = 0; nummer < lengde_VERDI; nummer++) {
            int VERDI = tegn_VERDI[nummer];
            if (!(VERDI >= 'a' && VERDI <= 'z') && !(VERDI >= 'A' && VERDI <= 'Z')
                && !(VERDI >= '0' && VERDI <= '9') && VERDI != '_' && VERDI != '-' && VERDI != '.') return false;
        }
        return tegn_VERDI[0] != '.';
    }

    static int Søk_oppføring(int[] tegn_VERDI, int lengde_VERDI) {
        if (!sjekk_navn(tegn_VERDI, lengde_VERDI)) return -22;
        for (int nummer = 0; nummer < 8; nummer++) {
            boolean 같음 = 이름들[nummer * 64 + lengde_VERDI] == 0;
            for (int åpning_oppføring = 0; åpning_oppføring < lengde_VERDI; åpning_oppføring++) if (이름들[nummer * 64 + åpning_oppføring] != tegn_VERDI[åpning_oppføring]) 같음 = false;
            if (같음) return nummer;
        }
        return -2;
    }

    static int Store_VERDI(int[] tegn_VERDI, int lengde_VERDI, int[] data, int Størrelse) {
        if (!sjekk_navn(tegn_VERDI, lengde_VERDI) || Størrelse < 0 || Størrelse > data.length) return -22;
        if (Størrelse > 최대크기) return -90;
        int INDEKS = Søk_oppføring(tegn_VERDI, lengde_VERDI);
        if (INDEKS == -2) {
            for (int nummer = 0; nummer < 8 && INDEKS < 0; nummer++) if (이름들[nummer * 64] == 0 && åpen_ANTALL[nummer] == 0) INDEKS = nummer;
            if (INDEKS >= 0) 허가들[INDEKS] = 438;
        }
        if (INDEKS < 0) return -28;
        int e_post = enhet_VERDI.Fil_Minne() + INDEKS * 최대크기;
        for (int nummer = 0; nummer < Størrelse; nummer++) enhet_VERDI.skrive_Minne(e_post + nummer, data[nummer]);
        for (int nummer = 0; nummer < 64; nummer++) 이름들[INDEKS * 64 + nummer] = nummer < lengde_VERDI ? tegn_VERDI[nummer] : 0;
        skalere_Liste[INDEKS] = Størrelse;
        return Størrelse;
    }

    static void oppføring_Liste() {
        for (int nummer = 0; nummer < 8; nummer++) if (이름들[nummer * 64] != 0) {
            for (int åpning_oppføring = 0; åpning_oppføring < 64 && 이름들[nummer * 64 + åpning_oppføring] != 0; åpning_oppføring++) SMS_Terminal.문자(이름들[nummer * 64 + åpning_oppføring]);
            SMS_Terminal.Skriv("  "); SMS_Terminal.skrive_nummer(skalere_Liste[nummer]); SMS_Terminal.Skriv("byte_VERDI\n");
        }
        SMS_Terminal.Skriv(lagringsenhet_kontakt.informasjonssystemer_Aktiv_9e72441a ? "Fil 8칸, 파일당 16384바이트; sync로 Store_VERDI 장치에 보존\n"
            : "임시 Fil 8칸, 파일당 16384바이트; prøve_på_nytt_VERDI 시작하면 사라짐\n");
    }

    static void Kommando(int[] inndata_VERDI, int Kjør_2, int lengde_VERDI, int Handling) {
        while (Kjør_2 < lengde_VERDI && inndata_VERDI[Kjør_2] == ' ') Kjør_2++;
        int 끝 = lengde_VERDI;
        while (끝 > Kjør_2 && inndata_VERDI[끝 - 1] == ' ') 끝--;
        int nummer = 끝 - Kjør_2;
        if (nummer < 1 || nummer > 63) { SMS_Terminal.Skriv("올바르지 않은 Fil Navn\n"); return; }
        for (int åpning_oppføring = 0; åpning_oppføring < 64; åpning_oppføring++) Navn[åpning_oppføring] = åpning_oppføring < nummer ? inndata_VERDI[Kjør_2 + åpning_oppføring] : 0;
        int INDEKS = Søk_oppføring(Navn, nummer);
        if (INDEKS == -22) { SMS_Terminal.Skriv("올바르지 않은 Fil Navn\n"); return; }
        if (Handling == 0) {
            편집중 = true; Rediger_skalere = 0; overløp_VERDI = false;
            SMS_Terminal.Skriv("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEKS < 0) SMS_Terminal.Skriv("파일을 찾을 nummer 없습니다\n");
        else if (Handling == 1) {
            int e_post = enhet_VERDI.Fil_Minne() + INDEKS * 최대크기;
            for (int åpning_oppføring = 0; åpning_oppføring < skalere_Liste[INDEKS]; åpning_oppføring++) SMS_Terminal.문자(enhet_VERDI.기억읽기(e_post + åpning_oppføring));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEKS * 64] = 0; skalere_Liste[INDEKS] = 0; SMS_Terminal.Skriv("파일을 지웠습니다\n"); }
    }

    static boolean informasjonssystemer_EKSAKT(int[] inndata_VERDI, int lengde_VERDI, String 문구) {
        if (lengde_VERDI != 문구.length()) return false;
        for (int åpning_oppføring = 0; åpning_oppføring < lengde_VERDI; åpning_oppføring++) if (inndata_VERDI[åpning_oppføring] != 문구.charAt(åpning_oppføring)) return false;
        return true;
    }

    static void Redigert_linje(int[] inndata_VERDI, int lengde_VERDI, boolean linje_overløp) {
        if (informasjonssystemer_EKSAKT(inndata_VERDI, lengde_VERDI, ".cancel")) {
            편집중 = false; SMS_Terminal.Skriv("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (informasjonssystemer_EKSAKT(inndata_VERDI, lengde_VERDI, ".save")) {
            편집중 = false;
            if (overløp_VERDI) { SMS_Terminal.Skriv("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int nummer = 0;
            while (nummer < 64 && Navn[nummer] != 0) nummer++;
            int KR = Store_VERDI(Navn, nummer, Rediger_VERDI, Rediger_skalere);
            SMS_Terminal.Skriv(KR >= 0 ? "보존한 byte_VERDI nummer: " : "보존 feil_VERDI: ");
            SMS_Terminal.skrive_nummer(KR); SMS_Terminal.문자(10);
        } else if (linje_overløp || lengde_VERDI + 1 > 최대크기 - Rediger_skalere) overløp_VERDI = true;
        else {
            for (int nummer = 0; nummer < lengde_VERDI; nummer++) Rediger_VERDI[Rediger_skalere++] = inndata_VERDI[nummer];
            Rediger_VERDI[Rediger_skalere++] = 10;
        }
    }

    static void 예제(String Fil, String Innhold_VERDI) {
        for (int nummer = 0; nummer < 64; nummer++) Navn[nummer] = nummer < Fil.length() ? Fil.charAt(nummer) : 0;
        for (int nummer = 0; nummer < Innhold_VERDI.length(); nummer++) Rediger_VERDI[nummer] = Innhold_VERDI.charAt(nummer);
        Store_VERDI(Navn, Fil.length(), Rediger_VERDI, Innhold_VERDI.length());
    }

    static void Forbered() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int gruppe_VERDI = enhet_VERDI.자바파일묶음(), Størrelse = enhet_VERDI.자바파일묶음크기();
        if (Størrelse < 8 || kjøring_overordnet.nummer(gruppe_VERDI) != 0x464a4b4a) { SMS_Terminal.Skriv("올바르지 않은 Java Fil gruppe_VERDI\n"); return; }
        int vare_ANTALL = kjøring_overordnet.nummer(gruppe_VERDI + 4);
        if (vare_ANTALL < 0 || vare_ANTALL > 8 || vare_ANTALL > (Størrelse - 8) / 72) { SMS_Terminal.Skriv("올바르지 않은 Java Fil oppføring_Liste\n"); return; }
        for (int nummer = 0; nummer < vare_ANTALL; nummer++) {
            int oppføring_VERDI = gruppe_VERDI + 8 + nummer * 72, lengde_VERDI = 0;
            for (int åpning_oppføring = 0; åpning_oppføring < 64; åpning_oppføring++) Navn[åpning_oppføring] = enhet_VERDI.기억읽기(oppføring_VERDI + åpning_oppføring);
            while (lengde_VERDI < 64 && Navn[lengde_VERDI] != 0) lengde_VERDI++;
            int Posisjon = kjøring_overordnet.nummer(oppføring_VERDI + 64), filstørrelse = kjøring_overordnet.nummer(oppføring_VERDI + 68);
            if (!sjekk_navn(Navn, lengde_VERDI) || filstørrelse < 0 || filstørrelse > 최대크기 || Posisjon < 8 + vare_ANTALL * 72 || Posisjon > Størrelse - filstørrelse) {
                SMS_Terminal.Skriv("올바르지 않은 Java Fil oppføring_VERDI\n"); return;
            }
            for (int åpning_oppføring = 0; åpning_oppføring < filstørrelse; åpning_oppføring++) Rediger_VERDI[åpning_oppføring] = enhet_VERDI.기억읽기(gruppe_VERDI + Posisjon + åpning_oppføring);
            if (Store_VERDI(Navn, lengde_VERDI, Rediger_VERDI, filstørrelse) < 0) { SMS_Terminal.Skriv("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
