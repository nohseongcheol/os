// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 faidhle. 원본 deasaich_VALUE/tog_tùs fàilligeadh_VALUE 시 기존 파일을 보존한다. */
public final class cuimhne_siostam_fhaidhlichean {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] atharraich_am_meud_Liosta = new int[8];
    static int[] fosgail_COUNT = new int[8], 허가들 = new int[8];
    static int[] Ainm = new int[64];
    static int[] deasaich_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean taomadh_VALUE = false;
    static int deasaich_atharraich_am_meud = 0;

    static boolean seic_ainm(int[] caractar_VALUE, int faid_VALUE) {
        if (faid_VALUE < 1 || faid_VALUE > 63) return false;
        for (int 수 = 0; 수 < faid_VALUE; 수++) {
            int VALUE = caractar_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return caractar_VALUE[0] != '.';
    }

    static int FIND_cur_a_steach(int[] caractar_VALUE, int faid_VALUE) {
        if (!seic_ainm(caractar_VALUE, faid_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + faid_VALUE] == 0;
            for (int slot_cur_a_steach = 0; slot_cur_a_steach < faid_VALUE; slot_cur_a_steach++) if (이름들[수 * 64 + slot_cur_a_steach] != caractar_VALUE[slot_cur_a_steach]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] caractar_VALUE, int faid_VALUE, int[] dàta, int atharraich_am_meud) {
        if (!seic_ainm(caractar_VALUE, faid_VALUE) || atharraich_am_meud < 0 || atharraich_am_meud > dàta.length) return -22;
        if (atharraich_am_meud > 최대크기) return -90;
        int INDEX = FIND_cur_a_steach(caractar_VALUE, faid_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && fosgail_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int ADDRESS = uidheam_VALUE.faidhle_cuimhne() + INDEX * 최대크기;
        for (int 수 = 0; 수 < atharraich_am_meud; 수++) uidheam_VALUE.sgrìobh_cuimhne(ADDRESS + 수, dàta[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < faid_VALUE ? caractar_VALUE[수] : 0;
        atharraich_am_meud_Liosta[INDEX] = atharraich_am_meud;
        return atharraich_am_meud;
    }

    static void cur_a_steach_Liosta() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int slot_cur_a_steach = 0; slot_cur_a_steach < 64 && 이름들[수 * 64 + slot_cur_a_steach] != 0; slot_cur_a_steach++) SMS_tèirmineal.문자(이름들[수 * 64 + slot_cur_a_steach]);
            SMS_tèirmineal.sgrìobh("  "); SMS_tèirmineal.수쓰기(atharraich_am_meud_Liosta[수]); SMS_tèirmineal.sgrìobh("baidht_VALUE\n");
        }
        SMS_tèirmineal.sgrìobh(stòras_uidheam_ceangal.사용가능 ? "faidhle 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 faidhle 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void àithne(int[] 입력, int ruith, int faid_VALUE, int Gnìomh) {
        while (ruith < faid_VALUE && 입력[ruith] == ' ') ruith++;
        int 끝 = faid_VALUE;
        while (끝 > ruith && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - ruith;
        if (수 < 1 || 수 > 63) { SMS_tèirmineal.sgrìobh("올바르지 않은 faidhle Ainm\n"); return; }
        for (int slot_cur_a_steach = 0; slot_cur_a_steach < 64; slot_cur_a_steach++) Ainm[slot_cur_a_steach] = slot_cur_a_steach < 수 ? 입력[ruith + slot_cur_a_steach] : 0;
        int INDEX = FIND_cur_a_steach(Ainm, 수);
        if (INDEX == -22) { SMS_tèirmineal.sgrìobh("올바르지 않은 faidhle Ainm\n"); return; }
        if (Gnìomh == 0) {
            편집중 = true; deasaich_atharraich_am_meud = 0; taomadh_VALUE = false;
            SMS_tèirmineal.sgrìobh("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_tèirmineal.sgrìobh("파일을 찾을 수 없습니다\n");
        else if (Gnìomh == 1) {
            int ADDRESS = uidheam_VALUE.faidhle_cuimhne() + INDEX * 최대크기;
            for (int slot_cur_a_steach = 0; slot_cur_a_steach < atharraich_am_meud_Liosta[INDEX]; slot_cur_a_steach++) SMS_tèirmineal.문자(uidheam_VALUE.기억읽기(ADDRESS + slot_cur_a_steach));
            SMS_tèirmineal.문자(10);
        } else { 이름들[INDEX * 64] = 0; atharraich_am_meud_Liosta[INDEX] = 0; SMS_tèirmineal.sgrìobh("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int faid_VALUE, String 문구) {
        if (faid_VALUE != 문구.length()) return false;
        for (int slot_cur_a_steach = 0; slot_cur_a_steach < faid_VALUE; slot_cur_a_steach++) if (입력[slot_cur_a_steach] != 문구.charAt(slot_cur_a_steach)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int faid_VALUE, boolean loidhne_taomadh) {
        if (정확(입력, faid_VALUE, ".cancel")) {
            편집중 = false; SMS_tèirmineal.sgrìobh("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, faid_VALUE, ".save")) {
            편집중 = false;
            if (taomadh_VALUE) { SMS_tèirmineal.sgrìobh("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Ainm[수] != 0) 수++;
            int tomhas = Store_VALUE(Ainm, 수, deasaich_VALUE, deasaich_atharraich_am_meud);
            SMS_tèirmineal.sgrìobh(tomhas >= 0 ? "보존한 baidht_VALUE 수: " : "보존 fàilligeadh_VALUE: ");
            SMS_tèirmineal.수쓰기(tomhas); SMS_tèirmineal.문자(10);
        } else if (loidhne_taomadh || faid_VALUE + 1 > 최대크기 - deasaich_atharraich_am_meud) taomadh_VALUE = true;
        else {
            for (int 수 = 0; 수 < faid_VALUE; 수++) deasaich_VALUE[deasaich_atharraich_am_meud++] = 입력[수];
            deasaich_VALUE[deasaich_atharraich_am_meud++] = 10;
        }
    }

    static void 예제(String faidhle, String susbaint_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Ainm[수] = 수 < faidhle.length() ? faidhle.charAt(수) : 0;
        for (int 수 = 0; 수 < susbaint_VALUE.length(); 수++) deasaich_VALUE[수] = susbaint_VALUE.charAt(수);
        Store_VALUE(Ainm, faidhle.length(), deasaich_VALUE, susbaint_VALUE.length());
    }

    static void Ullaich() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int buidheann_VALUE = uidheam_VALUE.자바파일묶음(), atharraich_am_meud = uidheam_VALUE.자바파일묶음크기();
        if (atharraich_am_meud < 8 || 실행관리.수(buidheann_VALUE) != 0x464a4b4a) { SMS_tèirmineal.sgrìobh("올바르지 않은 Java faidhle buidheann_VALUE\n"); return; }
        int nì_COUNT = 실행관리.수(buidheann_VALUE + 4);
        if (nì_COUNT < 0 || nì_COUNT > 8 || nì_COUNT > (atharraich_am_meud - 8) / 72) { SMS_tèirmineal.sgrìobh("올바르지 않은 Java faidhle cur_a_steach_Liosta\n"); return; }
        for (int 수 = 0; 수 < nì_COUNT; 수++) {
            int cur_a_steach_VALUE = buidheann_VALUE + 8 + 수 * 72, faid_VALUE = 0;
            for (int slot_cur_a_steach = 0; slot_cur_a_steach < 64; slot_cur_a_steach++) Ainm[slot_cur_a_steach] = uidheam_VALUE.기억읽기(cur_a_steach_VALUE + slot_cur_a_steach);
            while (faid_VALUE < 64 && Ainm[faid_VALUE] != 0) faid_VALUE++;
            int suidhich = 실행관리.수(cur_a_steach_VALUE + 64), faidhle_atharraich_am_meud = 실행관리.수(cur_a_steach_VALUE + 68);
            if (!seic_ainm(Ainm, faid_VALUE) || faidhle_atharraich_am_meud < 0 || faidhle_atharraich_am_meud > 최대크기 || suidhich < 8 + nì_COUNT * 72 || suidhich > atharraich_am_meud - faidhle_atharraich_am_meud) {
                SMS_tèirmineal.sgrìobh("올바르지 않은 Java faidhle cur_a_steach_VALUE\n"); return;
            }
            for (int slot_cur_a_steach = 0; slot_cur_a_steach < faidhle_atharraich_am_meud; slot_cur_a_steach++) deasaich_VALUE[slot_cur_a_steach] = uidheam_VALUE.기억읽기(buidheann_VALUE + suidhich + slot_cur_a_steach);
            if (Store_VALUE(Ainm, faid_VALUE, deasaich_VALUE, faidhle_atharraich_am_meud) < 0) { SMS_tèirmineal.sgrìobh("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
