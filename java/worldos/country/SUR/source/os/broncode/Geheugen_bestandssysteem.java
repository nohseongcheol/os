// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 bestand. 원본 Bewerk_WAARDE/compileren_bron fout_WAARDE 시 기존 파일을 보존한다. */
public final class Geheugen_bestandssysteem {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] formaat_wijzigen_Lijst = new int[8];
    static int[] open_AANTAL = new int[8], 허가들 = new int[8];
    static int[] Naam = new int[64];
    static int[] Bewerk_WAARDE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean overloop_WAARDE = false;
    static int Bewerk_formaat_wijzigen = 0;

    static boolean cheque_naam(int[] teken_WAARDE, int tijdsduur_WAARDE) {
        if (tijdsduur_WAARDE < 1 || tijdsduur_WAARDE > 63) return false;
        for (int nummer = 0; nummer < tijdsduur_WAARDE; nummer++) {
            int WAARDE = teken_WAARDE[nummer];
            if (!(WAARDE >= 'a' && WAARDE <= 'z') && !(WAARDE >= 'A' && WAARDE <= 'Z')
                && !(WAARDE >= '0' && WAARDE <= '9') && WAARDE != '_' && WAARDE != '-' && WAARDE != '.') return false;
        }
        return teken_WAARDE[0] != '.';
    }

    static int Zoeken_invoer(int[] teken_WAARDE, int tijdsduur_WAARDE) {
        if (!cheque_naam(teken_WAARDE, tijdsduur_WAARDE)) return -22;
        for (int nummer = 0; nummer < 8; nummer++) {
            boolean 같음 = 이름들[nummer * 64 + tijdsduur_WAARDE] == 0;
            for (int sleuf_invoer = 0; sleuf_invoer < tijdsduur_WAARDE; sleuf_invoer++) if (이름들[nummer * 64 + sleuf_invoer] != teken_WAARDE[sleuf_invoer]) 같음 = false;
            if (같음) return nummer;
        }
        return -2;
    }

    static int Store_WAARDE(int[] teken_WAARDE, int tijdsduur_WAARDE, int[] gegevens, int Grootte) {
        if (!cheque_naam(teken_WAARDE, tijdsduur_WAARDE) || Grootte < 0 || Grootte > gegevens.length) return -22;
        if (Grootte > 최대크기) return -90;
        int INDEX = Zoeken_invoer(teken_WAARDE, tijdsduur_WAARDE);
        if (INDEX == -2) {
            for (int nummer = 0; nummer < 8 && INDEX < 0; nummer++) if (이름들[nummer * 64] == 0 && open_AANTAL[nummer] == 0) INDEX = nummer;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int ADRES = mobiel_WAARDE.Bestand_Geheugen() + INDEX * 최대크기;
        for (int nummer = 0; nummer < Grootte; nummer++) mobiel_WAARDE.schrijven_Geheugen(ADRES + nummer, gegevens[nummer]);
        for (int nummer = 0; nummer < 64; nummer++) 이름들[INDEX * 64 + nummer] = nummer < tijdsduur_WAARDE ? teken_WAARDE[nummer] : 0;
        formaat_wijzigen_Lijst[INDEX] = Grootte;
        return Grootte;
    }

    static void invoer_Lijst_f07b3200() {
        for (int nummer = 0; nummer < 8; nummer++) if (이름들[nummer * 64] != 0) {
            for (int sleuf_invoer = 0; sleuf_invoer < 64 && 이름들[nummer * 64 + sleuf_invoer] != 0; sleuf_invoer++) sms_Terminal.문자(이름들[nummer * 64 + sleuf_invoer]);
            sms_Terminal.Schrijven("  "); sms_Terminal.schrijven_nummer(formaat_wijzigen_Lijst[nummer]); sms_Terminal.Schrijven("byte_WAARDE\n");
        }
        sms_Terminal.Schrijven(opslagapparaat_verbinding.informatie_Actief_9e72441a ? "bestand 8칸, 파일당 16384바이트; sync로 Store_WAARDE 장치에 보존\n"
            : "임시 bestand 8칸, 파일당 16384바이트; opnieuw_proberen_WAARDE 시작하면 사라짐\n");
    }

    static void opdracht(int[] invoer_WAARDE, int starten, int tijdsduur_WAARDE, int Actie) {
        while (starten < tijdsduur_WAARDE && invoer_WAARDE[starten] == ' ') starten++;
        int 끝 = tijdsduur_WAARDE;
        while (끝 > starten && invoer_WAARDE[끝 - 1] == ' ') 끝--;
        int nummer = 끝 - starten;
        if (nummer < 1 || nummer > 63) { sms_Terminal.Schrijven("올바르지 않은 bestand Naam\n"); return; }
        for (int sleuf_invoer = 0; sleuf_invoer < 64; sleuf_invoer++) Naam[sleuf_invoer] = sleuf_invoer < nummer ? invoer_WAARDE[starten + sleuf_invoer] : 0;
        int INDEX = Zoeken_invoer(Naam, nummer);
        if (INDEX == -22) { sms_Terminal.Schrijven("올바르지 않은 bestand Naam\n"); return; }
        if (Actie == 0) {
            편집중 = true; Bewerk_formaat_wijzigen = 0; overloop_WAARDE = false;
            sms_Terminal.Schrijven("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) sms_Terminal.Schrijven("파일을 찾을 nummer 없습니다\n");
        else if (Actie == 1) {
            int ADRES = mobiel_WAARDE.Bestand_Geheugen() + INDEX * 최대크기;
            for (int sleuf_invoer = 0; sleuf_invoer < formaat_wijzigen_Lijst[INDEX]; sleuf_invoer++) sms_Terminal.문자(mobiel_WAARDE.기억읽기(ADRES + sleuf_invoer));
            sms_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; formaat_wijzigen_Lijst[INDEX] = 0; sms_Terminal.Schrijven("파일을 지웠습니다\n"); }
    }

    static boolean informatie_GELIJK(int[] invoer_WAARDE, int tijdsduur_WAARDE, String 문구) {
        if (tijdsduur_WAARDE != 문구.length()) return false;
        for (int sleuf_invoer = 0; sleuf_invoer < tijdsduur_WAARDE; sleuf_invoer++) if (invoer_WAARDE[sleuf_invoer] != 문구.charAt(sleuf_invoer)) return false;
        return true;
    }

    static void Bewerkt_lijn(int[] invoer_WAARDE, int tijdsduur_WAARDE, boolean lijn_overloop) {
        if (informatie_GELIJK(invoer_WAARDE, tijdsduur_WAARDE, ".cancel")) {
            편집중 = false; sms_Terminal.Schrijven("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (informatie_GELIJK(invoer_WAARDE, tijdsduur_WAARDE, ".save")) {
            편집중 = false;
            if (overloop_WAARDE) { sms_Terminal.Schrijven("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int nummer = 0;
            while (nummer < 64 && Naam[nummer] != 0) nummer++;
            int resultaat = Store_WAARDE(Naam, nummer, Bewerk_WAARDE, Bewerk_formaat_wijzigen);
            sms_Terminal.Schrijven(resultaat >= 0 ? "보존한 byte_WAARDE nummer: " : "보존 fout_WAARDE: ");
            sms_Terminal.schrijven_nummer(resultaat); sms_Terminal.문자(10);
        } else if (lijn_overloop || tijdsduur_WAARDE + 1 > 최대크기 - Bewerk_formaat_wijzigen) overloop_WAARDE = true;
        else {
            for (int nummer = 0; nummer < tijdsduur_WAARDE; nummer++) Bewerk_WAARDE[Bewerk_formaat_wijzigen++] = invoer_WAARDE[nummer];
            Bewerk_WAARDE[Bewerk_formaat_wijzigen++] = 10;
        }
    }

    static void 예제(String bestand, String Inhoud_WAARDE) {
        for (int nummer = 0; nummer < 64; nummer++) Naam[nummer] = nummer < bestand.length() ? bestand.charAt(nummer) : 0;
        for (int nummer = 0; nummer < Inhoud_WAARDE.length(); nummer++) Bewerk_WAARDE[nummer] = Inhoud_WAARDE.charAt(nummer);
        Store_WAARDE(Naam, bestand.length(), Bewerk_WAARDE, Inhoud_WAARDE.length());
    }

    static void Bereid_voor() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Groep_WAARDE = mobiel_WAARDE.자바파일묶음(), Grootte = mobiel_WAARDE.자바파일묶음크기();
        if (Grootte < 8 || uitvoerbewerking_Manager.nummer(Groep_WAARDE) != 0x464a4b4a) { sms_Terminal.Schrijven("올바르지 않은 Java bestand Groep_WAARDE\n"); return; }
        int item_AANTAL = uitvoerbewerking_Manager.nummer(Groep_WAARDE + 4);
        if (item_AANTAL < 0 || item_AANTAL > 8 || item_AANTAL > (Grootte - 8) / 72) { sms_Terminal.Schrijven("올바르지 않은 Java bestand invoer_Lijst_f07b3200\n"); return; }
        for (int nummer = 0; nummer < item_AANTAL; nummer++) {
            int invoer_WAARDE_962f286b = Groep_WAARDE + 8 + nummer * 72, tijdsduur_WAARDE = 0;
            for (int sleuf_invoer = 0; sleuf_invoer < 64; sleuf_invoer++) Naam[sleuf_invoer] = mobiel_WAARDE.기억읽기(invoer_WAARDE_962f286b + sleuf_invoer);
            while (tijdsduur_WAARDE < 64 && Naam[tijdsduur_WAARDE] != 0) tijdsduur_WAARDE++;
            int positie = uitvoerbewerking_Manager.nummer(invoer_WAARDE_962f286b + 64), bestandsgrootte = uitvoerbewerking_Manager.nummer(invoer_WAARDE_962f286b + 68);
            if (!cheque_naam(Naam, tijdsduur_WAARDE) || bestandsgrootte < 0 || bestandsgrootte > 최대크기 || positie < 8 + item_AANTAL * 72 || positie > Grootte - bestandsgrootte) {
                sms_Terminal.Schrijven("올바르지 않은 Java bestand invoer_WAARDE_962f286b\n"); return;
            }
            for (int sleuf_invoer = 0; sleuf_invoer < bestandsgrootte; sleuf_invoer++) Bewerk_WAARDE[sleuf_invoer] = mobiel_WAARDE.기억읽기(Groep_WAARDE + positie + sleuf_invoer);
            if (Store_WAARDE(Naam, tijdsduur_WAARDE, Bewerk_WAARDE, bestandsgrootte) < 0) { sms_Terminal.Schrijven("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
