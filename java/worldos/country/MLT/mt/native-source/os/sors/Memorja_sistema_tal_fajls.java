// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 fajl. 원본 editja_VALUE/bena_sors żball_VALUE 시 기존 파일을 보존한다. */
public final class Memorja_sistema_tal_fajls {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] daqqas_Lista = new int[8];
    static int[] fetaħ_COUNT = new int[8], 허가들 = new int[8];
    static int[] isem = new int[64];
    static int[] editja_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean overflow_VALUE = false;
    static int editja_daqqas = 0;

    static boolean ċekk_isem(int[] karattru_VALUE, int tul_VALUE) {
        if (tul_VALUE < 1 || tul_VALUE > 63) return false;
        for (int 수 = 0; 수 < tul_VALUE; 수++) {
            int VALUE = karattru_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return karattru_VALUE[0] != '.';
    }

    static int sab_entrata(int[] karattru_VALUE, int tul_VALUE) {
        if (!ċekk_isem(karattru_VALUE, tul_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + tul_VALUE] == 0;
            for (int slott_entrata = 0; slott_entrata < tul_VALUE; slott_entrata++) if (이름들[수 * 64 + slott_entrata] != karattru_VALUE[slott_entrata]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] karattru_VALUE, int tul_VALUE, int[] data, int daqqas) {
        if (!ċekk_isem(karattru_VALUE, tul_VALUE) || daqqas < 0 || daqqas > data.length) return -22;
        if (daqqas > 최대크기) return -90;
        int INDEX = sab_entrata(karattru_VALUE, tul_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && fetaħ_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int ADDRESS = mowbajl_VALUE.fajl_Memorja() + INDEX * 최대크기;
        for (int 수 = 0; 수 < daqqas; 수++) mowbajl_VALUE.kiteb_Memorja(ADDRESS + 수, data[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < tul_VALUE ? karattru_VALUE[수] : 0;
        daqqas_Lista[INDEX] = daqqas;
        return daqqas;
    }

    static void entrata_Lista() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int slott_entrata = 0; slott_entrata < 64 && 이름들[수 * 64 + slott_entrata] != 0; slott_entrata++) SMS_Terminal.문자(이름들[수 * 64 + slott_entrata]);
            SMS_Terminal.kiteb("  "); SMS_Terminal.수쓰기(daqqas_Lista[수]); SMS_Terminal.kiteb("byte_VALUE\n");
        }
        SMS_Terminal.kiteb(Ħażna_mowbajl_konnessjoni.사용가능 ? "fajl 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 fajl 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void kmand(int[] 입력, int serje, int tul_VALUE, int azzjoni) {
        while (serje < tul_VALUE && 입력[serje] == ' ') serje++;
        int 끝 = tul_VALUE;
        while (끝 > serje && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - serje;
        if (수 < 1 || 수 > 63) { SMS_Terminal.kiteb("올바르지 않은 fajl isem\n"); return; }
        for (int slott_entrata = 0; slott_entrata < 64; slott_entrata++) isem[slott_entrata] = slott_entrata < 수 ? 입력[serje + slott_entrata] : 0;
        int INDEX = sab_entrata(isem, 수);
        if (INDEX == -22) { SMS_Terminal.kiteb("올바르지 않은 fajl isem\n"); return; }
        if (azzjoni == 0) {
            편집중 = true; editja_daqqas = 0; overflow_VALUE = false;
            SMS_Terminal.kiteb("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminal.kiteb("파일을 찾을 수 없습니다\n");
        else if (azzjoni == 1) {
            int ADDRESS = mowbajl_VALUE.fajl_Memorja() + INDEX * 최대크기;
            for (int slott_entrata = 0; slott_entrata < daqqas_Lista[INDEX]; slott_entrata++) SMS_Terminal.문자(mowbajl_VALUE.기억읽기(ADDRESS + slott_entrata));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; daqqas_Lista[INDEX] = 0; SMS_Terminal.kiteb("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int tul_VALUE, String 문구) {
        if (tul_VALUE != 문구.length()) return false;
        for (int slott_entrata = 0; slott_entrata < tul_VALUE; slott_entrata++) if (입력[slott_entrata] != 문구.charAt(slott_entrata)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int tul_VALUE, boolean linja_overflow) {
        if (정확(입력, tul_VALUE, ".cancel")) {
            편집중 = false; SMS_Terminal.kiteb("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, tul_VALUE, ".save")) {
            편집중 = false;
            if (overflow_VALUE) { SMS_Terminal.kiteb("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && isem[수] != 0) 수++;
            int miżura = Store_VALUE(isem, 수, editja_VALUE, editja_daqqas);
            SMS_Terminal.kiteb(miżura >= 0 ? "보존한 byte_VALUE 수: " : "보존 żball_VALUE: ");
            SMS_Terminal.수쓰기(miżura); SMS_Terminal.문자(10);
        } else if (linja_overflow || tul_VALUE + 1 > 최대크기 - editja_daqqas) overflow_VALUE = true;
        else {
            for (int 수 = 0; 수 < tul_VALUE; 수++) editja_VALUE[editja_daqqas++] = 입력[수];
            editja_VALUE[editja_daqqas++] = 10;
        }
    }

    static void 예제(String fajl, String Kontenut_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) isem[수] = 수 < fajl.length() ? fajl.charAt(수) : 0;
        for (int 수 = 0; 수 < Kontenut_VALUE.length(); 수++) editja_VALUE[수] = Kontenut_VALUE.charAt(수);
        Store_VALUE(isem, fajl.length(), editja_VALUE, Kontenut_VALUE.length());
    }

    static void Ħejji() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int grupp_VALUE = mowbajl_VALUE.자바파일묶음(), daqqas = mowbajl_VALUE.자바파일묶음크기();
        if (daqqas < 8 || 실행관리.수(grupp_VALUE) != 0x464a4b4a) { SMS_Terminal.kiteb("올바르지 않은 Java fajl grupp_VALUE\n"); return; }
        int element_COUNT = 실행관리.수(grupp_VALUE + 4);
        if (element_COUNT < 0 || element_COUNT > 8 || element_COUNT > (daqqas - 8) / 72) { SMS_Terminal.kiteb("올바르지 않은 Java fajl entrata_Lista\n"); return; }
        for (int 수 = 0; 수 < element_COUNT; 수++) {
            int entrata_VALUE = grupp_VALUE + 8 + 수 * 72, tul_VALUE = 0;
            for (int slott_entrata = 0; slott_entrata < 64; slott_entrata++) isem[slott_entrata] = mowbajl_VALUE.기억읽기(entrata_VALUE + slott_entrata);
            while (tul_VALUE < 64 && isem[tul_VALUE] != 0) tul_VALUE++;
            int pożizzjoni = 실행관리.수(entrata_VALUE + 64), fajl_daqqas = 실행관리.수(entrata_VALUE + 68);
            if (!ċekk_isem(isem, tul_VALUE) || fajl_daqqas < 0 || fajl_daqqas > 최대크기 || pożizzjoni < 8 + element_COUNT * 72 || pożizzjoni > daqqas - fajl_daqqas) {
                SMS_Terminal.kiteb("올바르지 않은 Java fajl entrata_VALUE\n"); return;
            }
            for (int slott_entrata = 0; slott_entrata < fajl_daqqas; slott_entrata++) editja_VALUE[slott_entrata] = mowbajl_VALUE.기억읽기(grupp_VALUE + pożizzjoni + slott_entrata);
            if (Store_VALUE(isem, tul_VALUE, editja_VALUE, fajl_daqqas) < 0) { SMS_Terminal.kiteb("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
