// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Faele. 원본 rulaganya_boleng/aga_mohlodi go_palelwa_boleng 시 기존 파일을 보존한다. */
public final class memori_tshepedišo_ya_difaele {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] bogolo_Lenaneo = new int[8];
    static int[] 열림수 = new int[8], 허가들 = new int[8];
    static int[] Leina = new int[64];
    static int[] rulaganya_boleng = new int[최대크기];
    static boolean 편집중 = false;
    static boolean mongwaloutama_boleng = false;
    static int rulaganya_bogolo = 0;

    static boolean lekola_leina(int[] tlhaka_boleng, int botelele_boleng) {
        if (botelele_boleng < 1 || botelele_boleng > 63) return false;
        for (int 수 = 0; 수 < botelele_boleng; 수++) {
            int boleng = tlhaka_boleng[수];
            if (!(boleng >= 'a' && boleng <= 'z') && !(boleng >= 'A' && boleng <= 'Z')
                && !(boleng >= '0' && boleng <= '9') && boleng != '_' && boleng != '-' && boleng != '.') return false;
        }
        return tlhaka_boleng[0] != '.';
    }

    static int hwetša_go_tsenya_tshedimošo(int[] tlhaka_boleng, int botelele_boleng) {
        if (!lekola_leina(tlhaka_boleng, botelele_boleng)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + botelele_boleng] == 0;
            for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < botelele_boleng; sekgobana_go_tsenya_tshedimošo++) if (이름들[수 * 64 + sekgobana_go_tsenya_tshedimošo] != tlhaka_boleng[sekgobana_go_tsenya_tshedimošo]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int lota_boleng(int[] tlhaka_boleng, int botelele_boleng, int[] data, int Bogolo) {
        if (!lekola_leina(tlhaka_boleng, botelele_boleng) || Bogolo < 0 || Bogolo > data.length) return -22;
        if (Bogolo > 최대크기) return -90;
        int lokela = hwetša_go_tsenya_tshedimošo(tlhaka_boleng, botelele_boleng);
        if (lokela == -2) {
            for (int 수 = 0; 수 < 8 && lokela < 0; 수++) if (이름들[수 * 64] == 0 && 열림수[수] == 0) lokela = 수;
            if (lokela >= 0) 허가들[lokela] = 438;
        }
        if (lokela < 0) return -28;
        int atrese = sedirišwa_boleng.faele_memori() + lokela * 최대크기;
        for (int 수 = 0; 수 < Bogolo; 수++) sedirišwa_boleng.ngwala_memori(atrese + 수, data[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[lokela * 64 + 수] = 수 < botelele_boleng ? tlhaka_boleng[수] : 0;
        bogolo_Lenaneo[lokela] = Bogolo;
        return Bogolo;
    }

    static void go_tsenya_tshedimošo_Lenaneo() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 64 && 이름들[수 * 64 + sekgobana_go_tsenya_tshedimošo] != 0; sekgobana_go_tsenya_tshedimošo++) 문자단말.문자(이름들[수 * 64 + sekgobana_go_tsenya_tshedimošo]);
            문자단말.Ngwala("  "); 문자단말.수쓰기(bogolo_Lenaneo[수]); 문자단말.Ngwala("paete_boleng\n");
        }
        문자단말.Ngwala(Bobolokelo_sedirišwa_kgokaganya.사용가능 ? "Faele 8칸, 파일당 16384바이트; sync로 lota_boleng 장치에 보존\n"
            : "임시 Faele 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Taelo(int[] 입력, int Diriša, int botelele_boleng, int Mogato) {
        while (Diriša < botelele_boleng && 입력[Diriša] == ' ') Diriša++;
        int 끝 = botelele_boleng;
        while (끝 > Diriša && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Diriša;
        if (수 < 1 || 수 > 63) { 문자단말.Ngwala("올바르지 않은 Faele Leina\n"); return; }
        for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 64; sekgobana_go_tsenya_tshedimošo++) Leina[sekgobana_go_tsenya_tshedimošo] = sekgobana_go_tsenya_tshedimošo < 수 ? 입력[Diriša + sekgobana_go_tsenya_tshedimošo] : 0;
        int lokela = hwetša_go_tsenya_tshedimošo(Leina, 수);
        if (lokela == -22) { 문자단말.Ngwala("올바르지 않은 Faele Leina\n"); return; }
        if (Mogato == 0) {
            편집중 = true; rulaganya_bogolo = 0; mongwaloutama_boleng = false;
            문자단말.Ngwala("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (lokela < 0) 문자단말.Ngwala("파일을 찾을 수 없습니다\n");
        else if (Mogato == 1) {
            int atrese = sedirišwa_boleng.faele_memori() + lokela * 최대크기;
            for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < bogolo_Lenaneo[lokela]; sekgobana_go_tsenya_tshedimošo++) 문자단말.문자(sedirišwa_boleng.기억읽기(atrese + sekgobana_go_tsenya_tshedimošo));
            문자단말.문자(10);
        } else { 이름들[lokela * 64] = 0; bogolo_Lenaneo[lokela] = 0; 문자단말.Ngwala("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int botelele_boleng, String 문구) {
        if (botelele_boleng != 문구.length()) return false;
        for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < botelele_boleng; sekgobana_go_tsenya_tshedimošo++) if (입력[sekgobana_go_tsenya_tshedimošo] != 문구.charAt(sekgobana_go_tsenya_tshedimošo)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int botelele_boleng, boolean mothaladi_mongwaloutama) {
        if (정확(입력, botelele_boleng, ".cancel")) {
            편집중 = false; 문자단말.Ngwala("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, botelele_boleng, ".save")) {
            편집중 = false;
            if (mongwaloutama_boleng) { 문자단말.Ngwala("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Leina[수] != 0) 수++;
            int 결과 = lota_boleng(Leina, 수, rulaganya_boleng, rulaganya_bogolo);
            문자단말.Ngwala(결과 >= 0 ? "보존한 paete_boleng 수: " : "보존 go_palelwa_boleng: ");
            문자단말.수쓰기(결과); 문자단말.문자(10);
        } else if (mothaladi_mongwaloutama || botelele_boleng + 1 > 최대크기 - rulaganya_bogolo) mongwaloutama_boleng = true;
        else {
            for (int 수 = 0; 수 < botelele_boleng; 수++) rulaganya_boleng[rulaganya_bogolo++] = 입력[수];
            rulaganya_boleng[rulaganya_bogolo++] = 10;
        }
    }

    static void 예제(String Faele, String Diteng_boleng) {
        for (int 수 = 0; 수 < 64; 수++) Leina[수] = 수 < Faele.length() ? Faele.charAt(수) : 0;
        for (int 수 = 0; 수 < Diteng_boleng.length(); 수++) rulaganya_boleng[수] = Diteng_boleng.charAt(수);
        lota_boleng(Leina, Faele.length(), rulaganya_boleng, Diteng_boleng.length());
    }

    static void Lokišetša() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int sehlopha_boleng = sedirišwa_boleng.자바파일묶음(), Bogolo = sedirišwa_boleng.자바파일묶음크기();
        if (Bogolo < 8 || 실행관리.수(sehlopha_boleng) != 0x464a4b4a) { 문자단말.Ngwala("올바르지 않은 Java Faele sehlopha_boleng\n"); return; }
        int 개수 = 실행관리.수(sehlopha_boleng + 4);
        if (개수 < 0 || 개수 > 8 || 개수 > (Bogolo - 8) / 72) { 문자단말.Ngwala("올바르지 않은 Java Faele go_tsenya_tshedimošo_Lenaneo\n"); return; }
        for (int 수 = 0; 수 < 개수; 수++) {
            int go_tsenya_tshedimošo_boleng = sehlopha_boleng + 8 + 수 * 72, botelele_boleng = 0;
            for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 64; sekgobana_go_tsenya_tshedimošo++) Leina[sekgobana_go_tsenya_tshedimošo] = sedirišwa_boleng.기억읽기(go_tsenya_tshedimošo_boleng + sekgobana_go_tsenya_tshedimošo);
            while (botelele_boleng < 64 && Leina[botelele_boleng] != 0) botelele_boleng++;
            int 위치 = 실행관리.수(go_tsenya_tshedimošo_boleng + 64), faele_bogolo = 실행관리.수(go_tsenya_tshedimošo_boleng + 68);
            if (!lekola_leina(Leina, botelele_boleng) || faele_bogolo < 0 || faele_bogolo > 최대크기 || 위치 < 8 + 개수 * 72 || 위치 > Bogolo - faele_bogolo) {
                문자단말.Ngwala("올바르지 않은 Java Faele go_tsenya_tshedimošo_boleng\n"); return;
            }
            for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < faele_bogolo; sekgobana_go_tsenya_tshedimošo++) rulaganya_boleng[sekgobana_go_tsenya_tshedimošo] = sedirišwa_boleng.기억읽기(sehlopha_boleng + 위치 + sekgobana_go_tsenya_tshedimošo);
            if (lota_boleng(Leina, botelele_boleng, rulaganya_boleng, faele_bogolo) < 0) { 문자단말.Ngwala("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
