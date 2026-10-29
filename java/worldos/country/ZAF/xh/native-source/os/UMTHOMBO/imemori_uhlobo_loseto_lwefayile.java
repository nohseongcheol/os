// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 iFayili. 원본 hlela_ixabiso/yakha_umthombo ukungaphumeleli_ixabiso 시 기존 파일을 보존한다. */
public final class imemori_uhlobo_loseto_lwefayile {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] isayizi_uludwe = new int[8];
    static int[] 열림수 = new int[8], 허가들 = new int[8];
    static int[] Igama = new int[64];
    static int[] hlela_ixabiso = new int[최대크기];
    static boolean 편집중 = false;
    static boolean ukuphuphuma_ixabiso = false;
    static int hlela_isayizi = 0;

    static boolean jonga_igama(int[] ikharakhtha_ixabiso, int ubude_ixabiso) {
        if (ubude_ixabiso < 1 || ubude_ixabiso > 63) return false;
        for (int 수 = 0; 수 < ubude_ixabiso; 수++) {
            int ixabiso = ikharakhtha_ixabiso[수];
            if (!(ixabiso >= 'a' && ixabiso <= 'z') && !(ixabiso >= 'A' && ixabiso <= 'Z')
                && !(ixabiso >= '0' && ixabiso <= '9') && ixabiso != '_' && ixabiso != '-' && ixabiso != '.') return false;
        }
        return ikharakhtha_ixabiso[0] != '.';
    }

    static int fumana_ufako_nkcukacha(int[] ikharakhtha_ixabiso, int ubude_ixabiso) {
        if (!jonga_igama(ikharakhtha_ixabiso, ubude_ixabiso)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + ubude_ixabiso] == 0;
            for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < ubude_ixabiso; isithuba_ufako_nkcukacha++) if (이름들[수 * 64 + isithuba_ufako_nkcukacha] != ikharakhtha_ixabiso[isithuba_ufako_nkcukacha]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_ixabiso(int[] ikharakhtha_ixabiso, int ubude_ixabiso, int[] iingcombolo, int Ubukhulu) {
        if (!jonga_igama(ikharakhtha_ixabiso, ubude_ixabiso) || Ubukhulu < 0 || Ubukhulu > iingcombolo.length) return -22;
        if (Ubukhulu > 최대크기) return -90;
        int indeksa = fumana_ufako_nkcukacha(ikharakhtha_ixabiso, ubude_ixabiso);
        if (indeksa == -2) {
            for (int 수 = 0; 수 < 8 && indeksa < 0; 수++) if (이름들[수 * 64] == 0 && 열림수[수] == 0) indeksa = 수;
            if (indeksa >= 0) 허가들[indeksa] = 438;
        }
        if (indeksa < 0) return -28;
        int idilesi = isixhobo_ixabiso.ifayile_imemori() + indeksa * 최대크기;
        for (int 수 = 0; 수 < Ubukhulu; 수++) isixhobo_ixabiso.bhala_imemori(idilesi + 수, iingcombolo[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[indeksa * 64 + 수] = 수 < ubude_ixabiso ? ikharakhtha_ixabiso[수] : 0;
        isayizi_uludwe[indeksa] = Ubukhulu;
        return Ubukhulu;
    }

    static void ufako_nkcukacha_uludwe() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 64 && 이름들[수 * 64 + isithuba_ufako_nkcukacha] != 0; isithuba_ufako_nkcukacha++) 문자단말.문자(이름들[수 * 64 + isithuba_ufako_nkcukacha]);
            문자단말.Bhala("  "); 문자단말.수쓰기(isayizi_uludwe[수]); 문자단말.Bhala("ibhayithi_ixabiso\n");
        }
        문자단말.Bhala(Ugcino_isixhobo_uqhagamshelo.사용가능 ? "iFayili 8칸, 파일당 16384바이트; sync로 Store_ixabiso 장치에 보존\n"
            : "임시 iFayili 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Umyalelo(int[] 입력, int Phumeza, int ubude_ixabiso, int Intshukumo) {
        while (Phumeza < ubude_ixabiso && 입력[Phumeza] == ' ') Phumeza++;
        int 끝 = ubude_ixabiso;
        while (끝 > Phumeza && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Phumeza;
        if (수 < 1 || 수 > 63) { 문자단말.Bhala("올바르지 않은 iFayili Igama\n"); return; }
        for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 64; isithuba_ufako_nkcukacha++) Igama[isithuba_ufako_nkcukacha] = isithuba_ufako_nkcukacha < 수 ? 입력[Phumeza + isithuba_ufako_nkcukacha] : 0;
        int indeksa = fumana_ufako_nkcukacha(Igama, 수);
        if (indeksa == -22) { 문자단말.Bhala("올바르지 않은 iFayili Igama\n"); return; }
        if (Intshukumo == 0) {
            편집중 = true; hlela_isayizi = 0; ukuphuphuma_ixabiso = false;
            문자단말.Bhala("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (indeksa < 0) 문자단말.Bhala("파일을 찾을 수 없습니다\n");
        else if (Intshukumo == 1) {
            int idilesi = isixhobo_ixabiso.ifayile_imemori() + indeksa * 최대크기;
            for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < isayizi_uludwe[indeksa]; isithuba_ufako_nkcukacha++) 문자단말.문자(isixhobo_ixabiso.기억읽기(idilesi + isithuba_ufako_nkcukacha));
            문자단말.문자(10);
        } else { 이름들[indeksa * 64] = 0; isayizi_uludwe[indeksa] = 0; 문자단말.Bhala("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int ubude_ixabiso, String 문구) {
        if (ubude_ixabiso != 문구.length()) return false;
        for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < ubude_ixabiso; isithuba_ufako_nkcukacha++) if (입력[isithuba_ufako_nkcukacha] != 문구.charAt(isithuba_ufako_nkcukacha)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int ubude_ixabiso, boolean umgca_ukuphuphuma) {
        if (정확(입력, ubude_ixabiso, ".cancel")) {
            편집중 = false; 문자단말.Bhala("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, ubude_ixabiso, ".save")) {
            편집중 = false;
            if (ukuphuphuma_ixabiso) { 문자단말.Bhala("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Igama[수] != 0) 수++;
            int 결과 = Store_ixabiso(Igama, 수, hlela_ixabiso, hlela_isayizi);
            문자단말.Bhala(결과 >= 0 ? "보존한 ibhayithi_ixabiso 수: " : "보존 ukungaphumeleli_ixabiso: ");
            문자단말.수쓰기(결과); 문자단말.문자(10);
        } else if (umgca_ukuphuphuma || ubude_ixabiso + 1 > 최대크기 - hlela_isayizi) ukuphuphuma_ixabiso = true;
        else {
            for (int 수 = 0; 수 < ubude_ixabiso; 수++) hlela_ixabiso[hlela_isayizi++] = 입력[수];
            hlela_ixabiso[hlela_isayizi++] = 10;
        }
    }

    static void 예제(String iFayili, String Isiqulatho_ixabiso) {
        for (int 수 = 0; 수 < 64; 수++) Igama[수] = 수 < iFayili.length() ? iFayili.charAt(수) : 0;
        for (int 수 = 0; 수 < Isiqulatho_ixabiso.length(); 수++) hlela_ixabiso[수] = Isiqulatho_ixabiso.charAt(수);
        Store_ixabiso(Igama, iFayili.length(), hlela_ixabiso, Isiqulatho_ixabiso.length());
    }

    static void lungisa() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int iqela_ixabiso = isixhobo_ixabiso.자바파일묶음(), Ubukhulu = isixhobo_ixabiso.자바파일묶음크기();
        if (Ubukhulu < 8 || 실행관리.수(iqela_ixabiso) != 0x464a4b4a) { 문자단말.Bhala("올바르지 않은 Java iFayili iqela_ixabiso\n"); return; }
        int 개수 = 실행관리.수(iqela_ixabiso + 4);
        if (개수 < 0 || 개수 > 8 || 개수 > (Ubukhulu - 8) / 72) { 문자단말.Bhala("올바르지 않은 Java iFayili ufako_nkcukacha_uludwe\n"); return; }
        for (int 수 = 0; 수 < 개수; 수++) {
            int ufako_nkcukacha_ixabiso = iqela_ixabiso + 8 + 수 * 72, ubude_ixabiso = 0;
            for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 64; isithuba_ufako_nkcukacha++) Igama[isithuba_ufako_nkcukacha] = isixhobo_ixabiso.기억읽기(ufako_nkcukacha_ixabiso + isithuba_ufako_nkcukacha);
            while (ubude_ixabiso < 64 && Igama[ubude_ixabiso] != 0) ubude_ixabiso++;
            int 위치 = 실행관리.수(ufako_nkcukacha_ixabiso + 64), ifayile_isayizi = 실행관리.수(ufako_nkcukacha_ixabiso + 68);
            if (!jonga_igama(Igama, ubude_ixabiso) || ifayile_isayizi < 0 || ifayile_isayizi > 최대크기 || 위치 < 8 + 개수 * 72 || 위치 > Ubukhulu - ifayile_isayizi) {
                문자단말.Bhala("올바르지 않은 Java iFayili ufako_nkcukacha_ixabiso\n"); return;
            }
            for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < ifayile_isayizi; isithuba_ufako_nkcukacha++) hlela_ixabiso[isithuba_ufako_nkcukacha] = isixhobo_ixabiso.기억읽기(iqela_ixabiso + 위치 + isithuba_ufako_nkcukacha);
            if (Store_ixabiso(Igama, ubude_ixabiso, hlela_ixabiso, ifayile_isayizi) < 0) { 문자단말.Bhala("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
