// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Fayl. 원본 tahrirlamoq_VALUE/yig_moq_manba to_xtab_qolish_VALUE 시 기존 파일을 보존한다. */
public final class Xotira_fayllar_tizimi {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] o_lcham_Ro_yxat = new int[8];
    static int[] ochmoq_COUNT = new int[8], 허가들 = new int[8];
    static int[] Nomi = new int[64];
    static int[] tahrirlamoq_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean to_lib_ketish_VALUE = false;
    static int tahrirlamoq_o_lcham = 0;

    static boolean chek_nom(int[] belgi_VALUE, int uzunlik_VALUE) {
        if (uzunlik_VALUE < 1 || uzunlik_VALUE > 63) return false;
        for (int 수 = 0; 수 < uzunlik_VALUE; 수++) {
            int VALUE = belgi_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return belgi_VALUE[0] != '.';
    }

    static int FIND_kiritish(int[] belgi_VALUE, int uzunlik_VALUE) {
        if (!chek_nom(belgi_VALUE, uzunlik_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + uzunlik_VALUE] == 0;
            for (int in_kiritish = 0; in_kiritish < uzunlik_VALUE; in_kiritish++) if (이름들[수 * 64 + in_kiritish] != belgi_VALUE[in_kiritish]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] belgi_VALUE, int uzunlik_VALUE, int[] ma_lumotlar, int Hajmi) {
        if (!chek_nom(belgi_VALUE, uzunlik_VALUE) || Hajmi < 0 || Hajmi > ma_lumotlar.length) return -22;
        if (Hajmi > 최대크기) return -90;
        int INDEX = FIND_kiritish(belgi_VALUE, uzunlik_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && ochmoq_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int manzil = qurilma_VALUE.fayl_Xotira() + INDEX * 최대크기;
        for (int 수 = 0; 수 < Hajmi; 수++) qurilma_VALUE.yozmoq_Xotira(manzil + 수, ma_lumotlar[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < uzunlik_VALUE ? belgi_VALUE[수] : 0;
        o_lcham_Ro_yxat[INDEX] = Hajmi;
        return Hajmi;
    }

    static void kiritish_Ro_yxat() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int in_kiritish = 0; in_kiritish < 64 && 이름들[수 * 64 + in_kiritish] != 0; in_kiritish++) SMS_Terminal.문자(이름들[수 * 64 + in_kiritish]);
            SMS_Terminal.Yozish("  "); SMS_Terminal.수쓰기(o_lcham_Ro_yxat[수]); SMS_Terminal.Yozish("bayt_VALUE\n");
        }
        SMS_Terminal.Yozish(Xotira_qurilma_aloqa.사용가능 ? "Fayl 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Fayl 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Buyruq(int[] 입력, int Bajarish, int uzunlik_VALUE, int Amal) {
        while (Bajarish < uzunlik_VALUE && 입력[Bajarish] == ' ') Bajarish++;
        int 끝 = uzunlik_VALUE;
        while (끝 > Bajarish && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Bajarish;
        if (수 < 1 || 수 > 63) { SMS_Terminal.Yozish("올바르지 않은 Fayl Nomi\n"); return; }
        for (int in_kiritish = 0; in_kiritish < 64; in_kiritish++) Nomi[in_kiritish] = in_kiritish < 수 ? 입력[Bajarish + in_kiritish] : 0;
        int INDEX = FIND_kiritish(Nomi, 수);
        if (INDEX == -22) { SMS_Terminal.Yozish("올바르지 않은 Fayl Nomi\n"); return; }
        if (Amal == 0) {
            편집중 = true; tahrirlamoq_o_lcham = 0; to_lib_ketish_VALUE = false;
            SMS_Terminal.Yozish("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminal.Yozish("파일을 찾을 수 없습니다\n");
        else if (Amal == 1) {
            int manzil = qurilma_VALUE.fayl_Xotira() + INDEX * 최대크기;
            for (int in_kiritish = 0; in_kiritish < o_lcham_Ro_yxat[INDEX]; in_kiritish++) SMS_Terminal.문자(qurilma_VALUE.기억읽기(manzil + in_kiritish));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; o_lcham_Ro_yxat[INDEX] = 0; SMS_Terminal.Yozish("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int uzunlik_VALUE, String 문구) {
        if (uzunlik_VALUE != 문구.length()) return false;
        for (int in_kiritish = 0; in_kiritish < uzunlik_VALUE; in_kiritish++) if (입력[in_kiritish] != 문구.charAt(in_kiritish)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int uzunlik_VALUE, boolean satr_to_lib_ketish) {
        if (정확(입력, uzunlik_VALUE, ".cancel")) {
            편집중 = false; SMS_Terminal.Yozish("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, uzunlik_VALUE, ".save")) {
            편집중 = false;
            if (to_lib_ketish_VALUE) { SMS_Terminal.Yozish("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Nomi[수] != 0) 수++;
            int o_lchov = Store_VALUE(Nomi, 수, tahrirlamoq_VALUE, tahrirlamoq_o_lcham);
            SMS_Terminal.Yozish(o_lchov >= 0 ? "보존한 bayt_VALUE 수: " : "보존 to_xtab_qolish_VALUE: ");
            SMS_Terminal.수쓰기(o_lchov); SMS_Terminal.문자(10);
        } else if (satr_to_lib_ketish || uzunlik_VALUE + 1 > 최대크기 - tahrirlamoq_o_lcham) to_lib_ketish_VALUE = true;
        else {
            for (int 수 = 0; 수 < uzunlik_VALUE; 수++) tahrirlamoq_VALUE[tahrirlamoq_o_lcham++] = 입력[수];
            tahrirlamoq_VALUE[tahrirlamoq_o_lcham++] = 10;
        }
    }

    static void 예제(String Fayl, String tarkib_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Nomi[수] = 수 < Fayl.length() ? Fayl.charAt(수) : 0;
        for (int 수 = 0; 수 < tarkib_VALUE.length(); 수++) tahrirlamoq_VALUE[수] = tarkib_VALUE.charAt(수);
        Store_VALUE(Nomi, Fayl.length(), tahrirlamoq_VALUE, tarkib_VALUE.length());
    }

    static void Tayyorlamoq() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Guruh_VALUE = qurilma_VALUE.자바파일묶음(), Hajmi = qurilma_VALUE.자바파일묶음크기();
        if (Hajmi < 8 || 실행관리.수(Guruh_VALUE) != 0x464a4b4a) { SMS_Terminal.Yozish("올바르지 않은 Java Fayl Guruh_VALUE\n"); return; }
        int element_COUNT = 실행관리.수(Guruh_VALUE + 4);
        if (element_COUNT < 0 || element_COUNT > 8 || element_COUNT > (Hajmi - 8) / 72) { SMS_Terminal.Yozish("올바르지 않은 Java Fayl kiritish_Ro_yxat\n"); return; }
        for (int 수 = 0; 수 < element_COUNT; 수++) {
            int kiritish_VALUE = Guruh_VALUE + 8 + 수 * 72, uzunlik_VALUE = 0;
            for (int in_kiritish = 0; in_kiritish < 64; in_kiritish++) Nomi[in_kiritish] = qurilma_VALUE.기억읽기(kiritish_VALUE + in_kiritish);
            while (uzunlik_VALUE < 64 && Nomi[uzunlik_VALUE] != 0) uzunlik_VALUE++;
            int Holati = 실행관리.수(kiritish_VALUE + 64), fayl_o_lcham = 실행관리.수(kiritish_VALUE + 68);
            if (!chek_nom(Nomi, uzunlik_VALUE) || fayl_o_lcham < 0 || fayl_o_lcham > 최대크기 || Holati < 8 + element_COUNT * 72 || Holati > Hajmi - fayl_o_lcham) {
                SMS_Terminal.Yozish("올바르지 않은 Java Fayl kiritish_VALUE\n"); return;
            }
            for (int in_kiritish = 0; in_kiritish < fayl_o_lcham; in_kiritish++) tahrirlamoq_VALUE[in_kiritish] = qurilma_VALUE.기억읽기(Guruh_VALUE + Holati + in_kiritish);
            if (Store_VALUE(Nomi, uzunlik_VALUE, tahrirlamoq_VALUE, fayl_o_lcham) < 0) { SMS_Terminal.Yozish("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
