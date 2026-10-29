// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 faili. 원본 hariri_thamani/jenga_chanzo kushindwa_thamani 시 기존 파일을 보존한다. */
public final class kumbukumbu_mfumo_ya_mafaili {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] panga_ukubwa_Orodha = new int[8];
    static int[] 열림수 = new int[8], 허가들 = new int[8];
    static int[] Jina = new int[64];
    static int[] hariri_thamani = new int[최대크기];
    static boolean 편집중 = false;
    static boolean ziada_thamani = false;
    static int hariri_panga_ukubwa = 0;

    static boolean hundi_jina(int[] kibambo_thamani, int urefu_thamani) {
        if (urefu_thamani < 1 || urefu_thamani > 63) return false;
        for (int 수 = 0; 수 < urefu_thamani; 수++) {
            int thamani = kibambo_thamani[수];
            if (!(thamani >= 'a' && thamani <= 'z') && !(thamani >= 'A' && thamani <= 'Z')
                && !(thamani >= '0' && thamani <= '9') && thamani != '_' && thamani != '-' && thamani != '.') return false;
        }
        return kibambo_thamani[0] != '.';
    }

    static int gundua_ingizo(int[] kibambo_thamani, int urefu_thamani) {
        if (!hundi_jina(kibambo_thamani, urefu_thamani)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + urefu_thamani] == 0;
            for (int Sloti_ingizo = 0; Sloti_ingizo < urefu_thamani; Sloti_ingizo++) if (이름들[수 * 64 + Sloti_ingizo] != kibambo_thamani[Sloti_ingizo]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_thamani(int[] kibambo_thamani, int urefu_thamani, int[] data, int panga_ukubwa) {
        if (!hundi_jina(kibambo_thamani, urefu_thamani) || panga_ukubwa < 0 || panga_ukubwa > data.length) return -22;
        if (panga_ukubwa > 최대크기) return -90;
        int kielezo = gundua_ingizo(kibambo_thamani, urefu_thamani);
        if (kielezo == -2) {
            for (int 수 = 0; 수 < 8 && kielezo < 0; 수++) if (이름들[수 * 64] == 0 && 열림수[수] == 0) kielezo = 수;
            if (kielezo >= 0) 허가들[kielezo] = 438;
        }
        if (kielezo < 0) return -28;
        int anwani = kifaa_thamani.faili_kumbukumbu() + kielezo * 최대크기;
        for (int 수 = 0; 수 < panga_ukubwa; 수++) kifaa_thamani.andika_kumbukumbu(anwani + 수, data[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[kielezo * 64 + 수] = 수 < urefu_thamani ? kibambo_thamani[수] : 0;
        panga_ukubwa_Orodha[kielezo] = panga_ukubwa;
        return panga_ukubwa;
    }

    static void ingizo_Orodha() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int Sloti_ingizo = 0; Sloti_ingizo < 64 && 이름들[수 * 64 + Sloti_ingizo] != 0; Sloti_ingizo++) 문자단말.문자(이름들[수 * 64 + Sloti_ingizo]);
            문자단말.andika("  "); 문자단말.수쓰기(panga_ukubwa_Orodha[수]); 문자단말.andika("baiti_thamani\n");
        }
        문자단말.andika(Hifadhi_kifaa_muunganisho.teknolojia_ya_maelezo_Amilifu_9e72441a ? "faili 8칸, 파일당 16384바이트; sync로 Store_thamani 장치에 보존\n"
            : "임시 faili 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void amri(int[] 입력, int endesha, int urefu_thamani, int Kitendo) {
        while (endesha < urefu_thamani && 입력[endesha] == ' ') endesha++;
        int 끝 = urefu_thamani;
        while (끝 > endesha && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - endesha;
        if (수 < 1 || 수 > 63) { 문자단말.andika("올바르지 않은 faili Jina\n"); return; }
        for (int Sloti_ingizo = 0; Sloti_ingizo < 64; Sloti_ingizo++) Jina[Sloti_ingizo] = Sloti_ingizo < 수 ? 입력[endesha + Sloti_ingizo] : 0;
        int kielezo = gundua_ingizo(Jina, 수);
        if (kielezo == -22) { 문자단말.andika("올바르지 않은 faili Jina\n"); return; }
        if (Kitendo == 0) {
            편집중 = true; hariri_panga_ukubwa = 0; ziada_thamani = false;
            문자단말.andika("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (kielezo < 0) 문자단말.andika("파일을 찾을 수 없습니다\n");
        else if (Kitendo == 1) {
            int anwani = kifaa_thamani.faili_kumbukumbu() + kielezo * 최대크기;
            for (int Sloti_ingizo = 0; Sloti_ingizo < panga_ukubwa_Orodha[kielezo]; Sloti_ingizo++) 문자단말.문자(kifaa_thamani.기억읽기(anwani + Sloti_ingizo));
            문자단말.문자(10);
        } else { 이름들[kielezo * 64] = 0; panga_ukubwa_Orodha[kielezo] = 0; 문자단말.andika("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int urefu_thamani, String 문구) {
        if (urefu_thamani != 문구.length()) return false;
        for (int Sloti_ingizo = 0; Sloti_ingizo < urefu_thamani; Sloti_ingizo++) if (입력[Sloti_ingizo] != 문구.charAt(Sloti_ingizo)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int urefu_thamani, boolean laini_ziada) {
        if (정확(입력, urefu_thamani, ".cancel")) {
            편집중 = false; 문자단말.andika("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, urefu_thamani, ".save")) {
            편집중 = false;
            if (ziada_thamani) { 문자단말.andika("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Jina[수] != 0) 수++;
            int 결과 = Store_thamani(Jina, 수, hariri_thamani, hariri_panga_ukubwa);
            문자단말.andika(결과 >= 0 ? "보존한 baiti_thamani 수: " : "보존 kushindwa_thamani: ");
            문자단말.수쓰기(결과); 문자단말.문자(10);
        } else if (laini_ziada || urefu_thamani + 1 > 최대크기 - hariri_panga_ukubwa) ziada_thamani = true;
        else {
            for (int 수 = 0; 수 < urefu_thamani; 수++) hariri_thamani[hariri_panga_ukubwa++] = 입력[수];
            hariri_thamani[hariri_panga_ukubwa++] = 10;
        }
    }

    static void 예제(String faili, String maudhui_thamani) {
        for (int 수 = 0; 수 < 64; 수++) Jina[수] = 수 < faili.length() ? faili.charAt(수) : 0;
        for (int 수 = 0; 수 < maudhui_thamani.length(); 수++) hariri_thamani[수] = maudhui_thamani.charAt(수);
        Store_thamani(Jina, faili.length(), hariri_thamani, maudhui_thamani.length());
    }

    static void Andaa() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Kikundi_thamani = kifaa_thamani.자바파일묶음(), panga_ukubwa = kifaa_thamani.자바파일묶음크기();
        if (panga_ukubwa < 8 || 실행관리.수(Kikundi_thamani) != 0x464a4b4a) { 문자단말.andika("올바르지 않은 Java faili Kikundi_thamani\n"); return; }
        int 개수 = 실행관리.수(Kikundi_thamani + 4);
        if (개수 < 0 || 개수 > 8 || 개수 > (panga_ukubwa - 8) / 72) { 문자단말.andika("올바르지 않은 Java faili ingizo_Orodha\n"); return; }
        for (int 수 = 0; 수 < 개수; 수++) {
            int ingizo_thamani = Kikundi_thamani + 8 + 수 * 72, urefu_thamani = 0;
            for (int Sloti_ingizo = 0; Sloti_ingizo < 64; Sloti_ingizo++) Jina[Sloti_ingizo] = kifaa_thamani.기억읽기(ingizo_thamani + Sloti_ingizo);
            while (urefu_thamani < 64 && Jina[urefu_thamani] != 0) urefu_thamani++;
            int 위치 = 실행관리.수(ingizo_thamani + 64), faili_panga_ukubwa = 실행관리.수(ingizo_thamani + 68);
            if (!hundi_jina(Jina, urefu_thamani) || faili_panga_ukubwa < 0 || faili_panga_ukubwa > 최대크기 || 위치 < 8 + 개수 * 72 || 위치 > panga_ukubwa - faili_panga_ukubwa) {
                문자단말.andika("올바르지 않은 Java faili ingizo_thamani\n"); return;
            }
            for (int Sloti_ingizo = 0; Sloti_ingizo < faili_panga_ukubwa; Sloti_ingizo++) hariri_thamani[Sloti_ingizo] = kifaa_thamani.기억읽기(Kikundi_thamani + 위치 + Sloti_ingizo);
            if (Store_thamani(Jina, urefu_thamani, hariri_thamani, faili_panga_ukubwa) < 0) { 문자단말.andika("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
