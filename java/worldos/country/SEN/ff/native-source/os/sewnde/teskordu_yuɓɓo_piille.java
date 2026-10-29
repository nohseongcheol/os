// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 fiilde. 원본 feewnditde_njaru/tafde_sewnde ella_njaru 시 기존 파일을 보존한다. */
public final class teskordu_yuɓɓo_piille {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] waylude_etannde_Doggol = new int[8];
    static int[] 열림수 = new int[8], 허가들 = new int[8];
    static int[] innde = new int[64];
    static int[] feewnditde_njaru = new int[최대크기];
    static boolean 편집중 = false;
    static boolean binndi_ɓurtuɗi_njaru = false;
    static int feewnditde_waylude_etannde = 0;

    static boolean sek_innde(int[] alkulal_njaru, int njuuteendi_njaru) {
        if (njuuteendi_njaru < 1 || njuuteendi_njaru > 63) return false;
        for (int 수 = 0; 수 < njuuteendi_njaru; 수++) {
            int njaru = alkulal_njaru[수];
            if (!(njaru >= 'a' && njaru <= 'z') && !(njaru >= 'A' && njaru <= 'Z')
                && !(njaru >= '0' && njaru <= '9') && njaru != '_' && njaru != '-' && njaru != '.') return false;
        }
        return alkulal_njaru[0] != '.';
    }

    static int yiylaade_naatnugol(int[] alkulal_njaru, int njuuteendi_njaru) {
        if (!sek_innde(alkulal_njaru, njuuteendi_njaru)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + njuuteendi_njaru] == 0;
            for (int 칸 = 0; 칸 < njuuteendi_njaru; 칸++) if (이름들[수 * 64 + 칸] != alkulal_njaru[칸]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int resde_njaru(int[] alkulal_njaru, int njuuteendi_njaru, int[] keɓe, int waylude_etannde) {
        if (!sek_innde(alkulal_njaru, njuuteendi_njaru) || waylude_etannde < 0 || waylude_etannde > keɓe.length) return -22;
        if (waylude_etannde > 최대크기) return -90;
        int joopirdu = yiylaade_naatnugol(alkulal_njaru, njuuteendi_njaru);
        if (joopirdu == -2) {
            for (int 수 = 0; 수 < 8 && joopirdu < 0; 수++) if (이름들[수 * 64] == 0 && 열림수[수] == 0) joopirdu = 수;
            if (joopirdu >= 0) 허가들[joopirdu] = 438;
        }
        if (joopirdu < 0) return -28;
        int ñiiɓirde = kaɓirgal_njaru.fiilde_teskordu() + joopirdu * 최대크기;
        for (int 수 = 0; 수 < waylude_etannde; 수++) kaɓirgal_njaru.winndude_teskordu(ñiiɓirde + 수, keɓe[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[joopirdu * 64 + 수] = 수 < njuuteendi_njaru ? alkulal_njaru[수] : 0;
        waylude_etannde_Doggol[joopirdu] = waylude_etannde;
        return waylude_etannde;
    }

    static void naatnugol_Doggol() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[수 * 64 + 칸] != 0; 칸++) 문자단말.문자(이름들[수 * 64 + 칸]);
            문자단말.winndude("  "); 문자단말.수쓰기(waylude_etannde_Doggol[수]); 문자단말.winndude("oktee_njaru\n");
        }
        문자단말.winndude(저장장치접속.사용가능 ? "fiilde 8칸, 파일당 16384바이트; sync로 resde_njaru 장치에 보존\n"
            : "임시 fiilde 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void ginol(int[] 입력, int huutoraade, int njuuteendi_njaru, int gollal) {
        while (huutoraade < njuuteendi_njaru && 입력[huutoraade] == ' ') huutoraade++;
        int 끝 = njuuteendi_njaru;
        while (끝 > huutoraade && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - huutoraade;
        if (수 < 1 || 수 > 63) { 문자단말.winndude("올바르지 않은 fiilde innde\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) innde[칸] = 칸 < 수 ? 입력[huutoraade + 칸] : 0;
        int joopirdu = yiylaade_naatnugol(innde, 수);
        if (joopirdu == -22) { 문자단말.winndude("올바르지 않은 fiilde innde\n"); return; }
        if (gollal == 0) {
            편집중 = true; feewnditde_waylude_etannde = 0; binndi_ɓurtuɗi_njaru = false;
            문자단말.winndude("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (joopirdu < 0) 문자단말.winndude("파일을 찾을 수 없습니다\n");
        else if (gollal == 1) {
            int ñiiɓirde = kaɓirgal_njaru.fiilde_teskordu() + joopirdu * 최대크기;
            for (int 칸 = 0; 칸 < waylude_etannde_Doggol[joopirdu]; 칸++) 문자단말.문자(kaɓirgal_njaru.기억읽기(ñiiɓirde + 칸));
            문자단말.문자(10);
        } else { 이름들[joopirdu * 64] = 0; waylude_etannde_Doggol[joopirdu] = 0; 문자단말.winndude("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int njuuteendi_njaru, String 문구) {
        if (njuuteendi_njaru != 문구.length()) return false;
        for (int 칸 = 0; 칸 < njuuteendi_njaru; 칸++) if (입력[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int njuuteendi_njaru, boolean diidol_binndi_ɓurtuɗi) {
        if (정확(입력, njuuteendi_njaru, ".cancel")) {
            편집중 = false; 문자단말.winndude("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, njuuteendi_njaru, ".save")) {
            편집중 = false;
            if (binndi_ɓurtuɗi_njaru) { 문자단말.winndude("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && innde[수] != 0) 수++;
            int 결과 = resde_njaru(innde, 수, feewnditde_njaru, feewnditde_waylude_etannde);
            문자단말.winndude(결과 >= 0 ? "보존한 oktee_njaru 수: " : "보존 ella_njaru: ");
            문자단말.수쓰기(결과); 문자단말.문자(10);
        } else if (diidol_binndi_ɓurtuɗi || njuuteendi_njaru + 1 > 최대크기 - feewnditde_waylude_etannde) binndi_ɓurtuɗi_njaru = true;
        else {
            for (int 수 = 0; 수 < njuuteendi_njaru; 수++) feewnditde_njaru[feewnditde_waylude_etannde++] = 입력[수];
            feewnditde_njaru[feewnditde_waylude_etannde++] = 10;
        }
    }

    static void 예제(String fiilde, String loowdi_njaru) {
        for (int 수 = 0; 수 < 64; 수++) innde[수] = 수 < fiilde.length() ? fiilde.charAt(수) : 0;
        for (int 수 = 0; 수 < loowdi_njaru.length(); 수++) feewnditde_njaru[수] = loowdi_njaru.charAt(수);
        resde_njaru(innde, fiilde.length(), feewnditde_njaru, loowdi_njaru.length());
    }

    static void Heblu() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int seto_njaru = kaɓirgal_njaru.자바파일묶음(), waylude_etannde = kaɓirgal_njaru.자바파일묶음크기();
        if (waylude_etannde < 8 || 실행관리.수(seto_njaru) != 0x464a4b4a) { 문자단말.winndude("올바르지 않은 Java fiilde seto_njaru\n"); return; }
        int 개수 = 실행관리.수(seto_njaru + 4);
        if (개수 < 0 || 개수 > 8 || 개수 > (waylude_etannde - 8) / 72) { 문자단말.winndude("올바르지 않은 Java fiilde naatnugol_Doggol\n"); return; }
        for (int 수 = 0; 수 < 개수; 수++) {
            int naatnugol_njaru = seto_njaru + 8 + 수 * 72, njuuteendi_njaru = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) innde[칸] = kaɓirgal_njaru.기억읽기(naatnugol_njaru + 칸);
            while (njuuteendi_njaru < 64 && innde[njuuteendi_njaru] != 0) njuuteendi_njaru++;
            int 위치 = 실행관리.수(naatnugol_njaru + 64), fiilde_waylude_etannde = 실행관리.수(naatnugol_njaru + 68);
            if (!sek_innde(innde, njuuteendi_njaru) || fiilde_waylude_etannde < 0 || fiilde_waylude_etannde > 최대크기 || 위치 < 8 + 개수 * 72 || 위치 > waylude_etannde - fiilde_waylude_etannde) {
                문자단말.winndude("올바르지 않은 Java fiilde naatnugol_njaru\n"); return;
            }
            for (int 칸 = 0; 칸 < fiilde_waylude_etannde; 칸++) feewnditde_njaru[칸] = kaɓirgal_njaru.기억읽기(seto_njaru + 위치 + 칸);
            if (resde_njaru(innde, njuuteendi_njaru, feewnditde_njaru, fiilde_waylude_etannde) < 0) { 문자단말.winndude("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
