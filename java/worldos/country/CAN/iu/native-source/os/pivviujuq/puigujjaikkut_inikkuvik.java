// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 ini. 원본 aaqqigiarli_atuutilik/sanali_pivviujuq itigaqtuq_atuutilik 시 기존 파일을 보존한다. */
public final class puigujjaikkut_inikkuvik {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] anininga_Titiqpalliagaq = new int[8];
    static int[] 열림수 = new int[8], 허가들 = new int[8];
    static int[] atiq = new int[64];
    static int[] aaqqigiarli_atuutilik = new int[최대크기];
    static boolean 편집중 = false;
    static boolean tatattuq_atuutilik = false;
    static int aaqqigiarli_anininga = 0;

    static boolean qaujigiarli_atiq(int[] immikkuuqtuq_atuutilik, int takininga_atuutilik) {
        if (takininga_atuutilik < 1 || takininga_atuutilik > 63) return false;
        for (int 수 = 0; 수 < takininga_atuutilik; 수++) {
            int atuutilik = immikkuuqtuq_atuutilik[수];
            if (!(atuutilik >= 'a' && atuutilik <= 'z') && !(atuutilik >= 'A' && atuutilik <= 'Z')
                && !(atuutilik >= '0' && atuutilik <= '9') && atuutilik != '_' && atuutilik != '-' && atuutilik != '.') return false;
        }
        return immikkuuqtuq_atuutilik[0] != '.';
    }

    static int nanili_Iliniku(int[] immikkuuqtuq_atuutilik, int takininga_atuutilik) {
        if (!qaujigiarli_atiq(immikkuuqtuq_atuutilik, takininga_atuutilik)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + takininga_atuutilik] == 0;
            for (int 칸 = 0; 칸 < takininga_atuutilik; 칸++) if (이름들[수 * 64 + 칸] != immikkuuqtuq_atuutilik[칸]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int tuqqurli_atuutilik(int[] immikkuuqtuq_atuutilik, int takininga_atuutilik, int[] titiqqat, int anininga) {
        if (!qaujigiarli_atiq(immikkuuqtuq_atuutilik, takininga_atuutilik) || anininga < 0 || anininga > titiqqat.length) return -22;
        if (anininga > 최대크기) return -90;
        int nalunaiqsimavik = nanili_Iliniku(immikkuuqtuq_atuutilik, takininga_atuutilik);
        if (nalunaiqsimavik == -2) {
            for (int 수 = 0; 수 < 8 && nalunaiqsimavik < 0; 수++) if (이름들[수 * 64] == 0 && 열림수[수] == 0) nalunaiqsimavik = 수;
            if (nalunaiqsimavik >= 0) 허가들[nalunaiqsimavik] = 438;
        }
        if (nalunaiqsimavik < 0) return -28;
        int turaarut = sunakkutaaq_atuutilik.ini_puigujjaikkut() + nalunaiqsimavik * 최대크기;
        for (int 수 = 0; 수 < anininga; 수++) sunakkutaaq_atuutilik.titiraq_puigujjaikkut(turaarut + 수, titiqqat[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[nalunaiqsimavik * 64 + 수] = 수 < takininga_atuutilik ? immikkuuqtuq_atuutilik[수] : 0;
        anininga_Titiqpalliagaq[nalunaiqsimavik] = anininga;
        return anininga;
    }

    static void Iliniku_Titiqpalliagaq() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[수 * 64 + 칸] != 0; 칸++) 문자단말.문자(이름들[수 * 64 + 칸]);
            문자단말.titiraq("  "); 문자단말.수쓰기(anininga_Titiqpalliagaq[수]); 문자단말.titiraq("byte_atuutilik\n");
        }
        문자단말.titiraq(저장장치접속.사용가능 ? "ini 8칸, 파일당 16384바이트; sync로 tuqqurli_atuutilik 장치에 보존\n"
            : "임시 ini 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void piqujijjut(int[] 입력, int 시작, int takininga_atuutilik, int sugiarut) {
        while (시작 < takininga_atuutilik && 입력[시작] == ' ') 시작++;
        int 끝 = takininga_atuutilik;
        while (끝 > 시작 && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - 시작;
        if (수 < 1 || 수 > 63) { 문자단말.titiraq("올바르지 않은 ini atiq\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) atiq[칸] = 칸 < 수 ? 입력[시작 + 칸] : 0;
        int nalunaiqsimavik = nanili_Iliniku(atiq, 수);
        if (nalunaiqsimavik == -22) { 문자단말.titiraq("올바르지 않은 ini atiq\n"); return; }
        if (sugiarut == 0) {
            편집중 = true; aaqqigiarli_anininga = 0; tatattuq_atuutilik = false;
            문자단말.titiraq("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (nalunaiqsimavik < 0) 문자단말.titiraq("파일을 찾을 수 없습니다\n");
        else if (sugiarut == 1) {
            int turaarut = sunakkutaaq_atuutilik.ini_puigujjaikkut() + nalunaiqsimavik * 최대크기;
            for (int 칸 = 0; 칸 < anininga_Titiqpalliagaq[nalunaiqsimavik]; 칸++) 문자단말.문자(sunakkutaaq_atuutilik.기억읽기(turaarut + 칸));
            문자단말.문자(10);
        } else { 이름들[nalunaiqsimavik * 64] = 0; anininga_Titiqpalliagaq[nalunaiqsimavik] = 0; 문자단말.titiraq("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int takininga_atuutilik, String 문구) {
        if (takininga_atuutilik != 문구.length()) return false;
        for (int 칸 = 0; 칸 < takininga_atuutilik; 칸++) if (입력[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int takininga_atuutilik, boolean titikutaak_tatattuq) {
        if (정확(입력, takininga_atuutilik, ".cancel")) {
            편집중 = false; 문자단말.titiraq("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, takininga_atuutilik, ".save")) {
            편집중 = false;
            if (tatattuq_atuutilik) { 문자단말.titiraq("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && atiq[수] != 0) 수++;
            int 결과 = tuqqurli_atuutilik(atiq, 수, aaqqigiarli_atuutilik, aaqqigiarli_anininga);
            문자단말.titiraq(결과 >= 0 ? "보존한 byte_atuutilik 수: " : "보존 itigaqtuq_atuutilik: ");
            문자단말.수쓰기(결과); 문자단말.문자(10);
        } else if (titikutaak_tatattuq || takininga_atuutilik + 1 > 최대크기 - aaqqigiarli_anininga) tatattuq_atuutilik = true;
        else {
            for (int 수 = 0; 수 < takininga_atuutilik; 수++) aaqqigiarli_atuutilik[aaqqigiarli_anininga++] = 입력[수];
            aaqqigiarli_atuutilik[aaqqigiarli_anininga++] = 10;
        }
    }

    static void 예제(String ini, String Ilulingit_atuutilik) {
        for (int 수 = 0; 수 < 64; 수++) atiq[수] = 수 < ini.length() ? ini.charAt(수) : 0;
        for (int 수 = 0; 수 < Ilulingit_atuutilik.length(); 수++) aaqqigiarli_atuutilik[수] = Ilulingit_atuutilik.charAt(수);
        tuqqurli_atuutilik(atiq, ini.length(), aaqqigiarli_atuutilik, Ilulingit_atuutilik.length());
    }

    static void Parnalli() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int katinngajut_atuutilik = sunakkutaaq_atuutilik.자바파일묶음(), anininga = sunakkutaaq_atuutilik.자바파일묶음크기();
        if (anininga < 8 || 실행관리.수(katinngajut_atuutilik) != 0x464a4b4a) { 문자단말.titiraq("올바르지 않은 Java ini katinngajut_atuutilik\n"); return; }
        int 개수 = 실행관리.수(katinngajut_atuutilik + 4);
        if (개수 < 0 || 개수 > 8 || 개수 > (anininga - 8) / 72) { 문자단말.titiraq("올바르지 않은 Java ini Iliniku_Titiqpalliagaq\n"); return; }
        for (int 수 = 0; 수 < 개수; 수++) {
            int Iliniku_atuutilik = katinngajut_atuutilik + 8 + 수 * 72, takininga_atuutilik = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) atiq[칸] = sunakkutaaq_atuutilik.기억읽기(Iliniku_atuutilik + 칸);
            while (takininga_atuutilik < 64 && atiq[takininga_atuutilik] != 0) takininga_atuutilik++;
            int 위치 = 실행관리.수(Iliniku_atuutilik + 64), ini_anininga = 실행관리.수(Iliniku_atuutilik + 68);
            if (!qaujigiarli_atiq(atiq, takininga_atuutilik) || ini_anininga < 0 || ini_anininga > 최대크기 || 위치 < 8 + 개수 * 72 || 위치 > anininga - ini_anininga) {
                문자단말.titiraq("올바르지 않은 Java ini Iliniku_atuutilik\n"); return;
            }
            for (int 칸 = 0; 칸 < ini_anininga; 칸++) aaqqigiarli_atuutilik[칸] = sunakkutaaq_atuutilik.기억읽기(katinngajut_atuutilik + 위치 + 칸);
            if (tuqqurli_atuutilik(atiq, takininga_atuutilik, aaqqigiarli_atuutilik, ini_anininga) < 0) { 문자단말.titiraq("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
