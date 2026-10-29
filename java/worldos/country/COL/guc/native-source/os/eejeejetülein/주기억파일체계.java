// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 anaajaalaa. 원본 anaataa_ajutuu/akompiraajaa_eejeejetülein ajachitia_ajutuu 시 기존 파일을 보존한다. */
public final class 주기억파일체계 {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] 크기들 = new int[8];
    static int[] 열림수 = new int[8], 허가들 = new int[8];
    static int[] 이름 = new int[64];
    static int[] anaataa_ajutuu = new int[최대크기];
    static boolean 편집중 = false;
    static boolean 넘침 = false;
    static int 편집크기 = 0;

    static boolean 이름검사(int[] jeerü_ajutuu, int akaliaa_ajutuu) {
        if (akaliaa_ajutuu < 1 || akaliaa_ajutuu > 63) return false;
        for (int 수 = 0; 수 < akaliaa_ajutuu; 수++) {
            int ajutuu = jeerü_ajutuu[수];
            if (!(ajutuu >= 'a' && ajutuu <= 'z') && !(ajutuu >= 'A' && ajutuu <= 'Z')
                && !(ajutuu >= '0' && ajutuu <= '9') && ajutuu != '_' && ajutuu != '-' && ajutuu != '.') return false;
        }
        return jeerü_ajutuu[0] != '.';
    }

    static int 찾기(int[] jeerü_ajutuu, int akaliaa_ajutuu) {
        if (!이름검사(jeerü_ajutuu, akaliaa_ajutuu)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + akaliaa_ajutuu] == 0;
            for (int 칸 = 0; 칸 < akaliaa_ajutuu; 칸++) if (이름들[수 * 64 + 칸] != jeerü_ajutuu[칸]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int 저장(int[] jeerü_ajutuu, int akaliaa_ajutuu, int[] atijaaya, int 크기) {
        if (!이름검사(jeerü_ajutuu, akaliaa_ajutuu) || 크기 < 0 || 크기 > atijaaya.length) return -22;
        if (크기 > 최대크기) return -90;
        int ee_iyatialujuna = 찾기(jeerü_ajutuu, akaliaa_ajutuu);
        if (ee_iyatialujuna == -2) {
            for (int 수 = 0; 수 < 8 && ee_iyatialujuna < 0; 수++) if (이름들[수 * 64] == 0 && 열림수[수] == 0) ee_iyatialujuna = 수;
            if (ee_iyatialujuna >= 0) 허가들[ee_iyatialujuna] = 438;
        }
        if (ee_iyatialujuna < 0) return -28;
        int ejepüsee = serulaalü_ajutuu.파일기억() + ee_iyatialujuna * 최대크기;
        for (int 수 = 0; 수 < 크기; 수++) serulaalü_ajutuu.기억쓰기(ejepüsee + 수, atijaaya[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[ee_iyatialujuna * 64 + 수] = 수 < akaliaa_ajutuu ? jeerü_ajutuu[수] : 0;
        크기들[ee_iyatialujuna] = 크기;
        return 크기;
    }

    static void 목록() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[수 * 64 + 칸] != 0; 칸++) 문자단말.문자(이름들[수 * 64 + 칸]);
            문자단말.ashajaa("  "); 문자단말.수쓰기(크기들[수]); 문자단말.ashajaa("waai_ajutuu\n");
        }
        문자단말.ashajaa(저장장치접속.사용가능 ? "anaajaalaa 8칸, 파일당 16384바이트; sync로 저장 장치에 보존\n"
            : "임시 anaajaalaa 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void aluwataaya(int[] 입력, int 시작, int akaliaa_ajutuu, int aa_inra_awai) {
        while (시작 < akaliaa_ajutuu && 입력[시작] == ' ') 시작++;
        int 끝 = akaliaa_ajutuu;
        while (끝 > 시작 && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - 시작;
        if (수 < 1 || 수 > 63) { 문자단말.ashajaa("올바르지 않은 anaajaalaa 이름\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) 이름[칸] = 칸 < 수 ? 입력[시작 + 칸] : 0;
        int ee_iyatialujuna = 찾기(이름, 수);
        if (ee_iyatialujuna == -22) { 문자단말.ashajaa("올바르지 않은 anaajaalaa 이름\n"); return; }
        if (aa_inra_awai == 0) {
            편집중 = true; 편집크기 = 0; 넘침 = false;
            문자단말.ashajaa("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (ee_iyatialujuna < 0) 문자단말.ashajaa("파일을 찾을 수 없습니다\n");
        else if (aa_inra_awai == 1) {
            int ejepüsee = serulaalü_ajutuu.파일기억() + ee_iyatialujuna * 최대크기;
            for (int 칸 = 0; 칸 < 크기들[ee_iyatialujuna]; 칸++) 문자단말.문자(serulaalü_ajutuu.기억읽기(ejepüsee + 칸));
            문자단말.문자(10);
        } else { 이름들[ee_iyatialujuna * 64] = 0; 크기들[ee_iyatialujuna] = 0; 문자단말.ashajaa("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int akaliaa_ajutuu, String 문구) {
        if (akaliaa_ajutuu != 문구.length()) return false;
        for (int 칸 = 0; 칸 < akaliaa_ajutuu; 칸++) if (입력[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int akaliaa_ajutuu, boolean 줄넘침) {
        if (정확(입력, akaliaa_ajutuu, ".cancel")) {
            편집중 = false; 문자단말.ashajaa("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, akaliaa_ajutuu, ".save")) {
            편집중 = false;
            if (넘침) { 문자단말.ashajaa("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && 이름[수] != 0) 수++;
            int 결과 = 저장(이름, 수, anaataa_ajutuu, 편집크기);
            문자단말.ashajaa(결과 >= 0 ? "보존한 waai_ajutuu 수: " : "보존 ajachitia_ajutuu: ");
            문자단말.수쓰기(결과); 문자단말.문자(10);
        } else if (줄넘침 || akaliaa_ajutuu + 1 > 최대크기 - 편집크기) 넘침 = true;
        else {
            for (int 수 = 0; 수 < akaliaa_ajutuu; 수++) anaataa_ajutuu[편집크기++] = 입력[수];
            anaataa_ajutuu[편집크기++] = 10;
        }
    }

    static void 예제(String anaajaalaa, String alu_ujatüü_ajutuu) {
        for (int 수 = 0; 수 < 64; 수++) 이름[수] = 수 < anaajaalaa.length() ? anaajaalaa.charAt(수) : 0;
        for (int 수 = 0; 수 < alu_ujatüü_ajutuu.length(); 수++) anaataa_ajutuu[수] = alu_ujatüü_ajutuu.charAt(수);
        저장(이름, anaajaalaa.length(), anaataa_ajutuu, alu_ujatüü_ajutuu.length());
    }

    static void 준비() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int akotchijuushi_ajutuu = serulaalü_ajutuu.자바파일묶음(), 크기 = serulaalü_ajutuu.자바파일묶음크기();
        if (크기 < 8 || 실행관리.수(akotchijuushi_ajutuu) != 0x464a4b4a) { 문자단말.ashajaa("올바르지 않은 Java anaajaalaa akotchijuushi_ajutuu\n"); return; }
        int 개수 = 실행관리.수(akotchijuushi_ajutuu + 4);
        if (개수 < 0 || 개수 > 8 || 개수 > (크기 - 8) / 72) { 문자단말.ashajaa("올바르지 않은 Java anaajaalaa 목록\n"); return; }
        for (int 수 = 0; 수 < 개수; 수++) {
            int ekeroliaa_ajutuu = akotchijuushi_ajutuu + 8 + 수 * 72, akaliaa_ajutuu = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) 이름[칸] = serulaalü_ajutuu.기억읽기(ekeroliaa_ajutuu + 칸);
            while (akaliaa_ajutuu < 64 && 이름[akaliaa_ajutuu] != 0) akaliaa_ajutuu++;
            int 위치 = 실행관리.수(ekeroliaa_ajutuu + 64), 파일크기 = 실행관리.수(ekeroliaa_ajutuu + 68);
            if (!이름검사(이름, akaliaa_ajutuu) || 파일크기 < 0 || 파일크기 > 최대크기 || 위치 < 8 + 개수 * 72 || 위치 > 크기 - 파일크기) {
                문자단말.ashajaa("올바르지 않은 Java anaajaalaa ekeroliaa_ajutuu\n"); return;
            }
            for (int 칸 = 0; 칸 < 파일크기; 칸++) anaataa_ajutuu[칸] = serulaalü_ajutuu.기억읽기(akotchijuushi_ajutuu + 위치 + 칸);
            if (저장(이름, akaliaa_ajutuu, anaataa_ajutuu, 파일크기) < 0) { 문자단말.ashajaa("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
