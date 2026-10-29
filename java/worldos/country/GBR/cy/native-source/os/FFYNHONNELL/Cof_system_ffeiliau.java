// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Ffeil. 원본 Golygu_VALUE/llunio_ffynhonnell methiant_VALUE 시 기존 파일을 보존한다. */
public final class Cof_system_ffeiliau {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] newid_maint_Rhestr = new int[8];
    static int[] agor_COUNT = new int[8], 허가들 = new int[8];
    static int[] Enw = new int[64];
    static int[] Golygu_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean gorlif_VALUE = false;
    static int Golygu_newid_maint = 0;

    static boolean gwirio_enw(int[] nod_VALUE, int hyd_VALUE) {
        if (hyd_VALUE < 1 || hyd_VALUE > 63) return false;
        for (int 수 = 0; 수 < hyd_VALUE; 수++) {
            int VALUE = nod_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return nod_VALUE[0] != '.';
    }

    static int FIND_cofnod(int[] nod_VALUE, int hyd_VALUE) {
        if (!gwirio_enw(nod_VALUE, hyd_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + hyd_VALUE] == 0;
            for (int slot_cofnod = 0; slot_cofnod < hyd_VALUE; slot_cofnod++) if (이름들[수 * 64 + slot_cofnod] != nod_VALUE[slot_cofnod]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] nod_VALUE, int hyd_VALUE, int[] data, int Maint) {
        if (!gwirio_enw(nod_VALUE, hyd_VALUE) || Maint < 0 || Maint > data.length) return -22;
        if (Maint > 최대크기) return -90;
        int INDEX = FIND_cofnod(nod_VALUE, hyd_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && agor_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int ADDRESS = dyfais_VALUE.ffeil_Cof() + INDEX * 최대크기;
        for (int 수 = 0; 수 < Maint; 수++) dyfais_VALUE.ysgrifennu_Cof(ADDRESS + 수, data[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < hyd_VALUE ? nod_VALUE[수] : 0;
        newid_maint_Rhestr[INDEX] = Maint;
        return Maint;
    }

    static void cofnod_Rhestr() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int slot_cofnod = 0; slot_cofnod < 64 && 이름들[수 * 64 + slot_cofnod] != 0; slot_cofnod++) SMS_Terfynell.문자(이름들[수 * 64 + slot_cofnod]);
            SMS_Terfynell.Ysgrifennu("  "); SMS_Terfynell.수쓰기(newid_maint_Rhestr[수]); SMS_Terfynell.Ysgrifennu("beit_VALUE\n");
        }
        SMS_Terfynell.Ysgrifennu(Storio_dyfais_cyswllt.technoleg_gwybodaeth_Ar_gael_9e72441a ? "Ffeil 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Ffeil 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Gorchymyn(int[] 입력, int Gweithredu_2, int hyd_VALUE, int Gweithrediad) {
        while (Gweithredu_2 < hyd_VALUE && 입력[Gweithredu_2] == ' ') Gweithredu_2++;
        int 끝 = hyd_VALUE;
        while (끝 > Gweithredu_2 && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Gweithredu_2;
        if (수 < 1 || 수 > 63) { SMS_Terfynell.Ysgrifennu("올바르지 않은 Ffeil Enw\n"); return; }
        for (int slot_cofnod = 0; slot_cofnod < 64; slot_cofnod++) Enw[slot_cofnod] = slot_cofnod < 수 ? 입력[Gweithredu_2 + slot_cofnod] : 0;
        int INDEX = FIND_cofnod(Enw, 수);
        if (INDEX == -22) { SMS_Terfynell.Ysgrifennu("올바르지 않은 Ffeil Enw\n"); return; }
        if (Gweithrediad == 0) {
            편집중 = true; Golygu_newid_maint = 0; gorlif_VALUE = false;
            SMS_Terfynell.Ysgrifennu("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terfynell.Ysgrifennu("파일을 찾을 수 없습니다\n");
        else if (Gweithrediad == 1) {
            int ADDRESS = dyfais_VALUE.ffeil_Cof() + INDEX * 최대크기;
            for (int slot_cofnod = 0; slot_cofnod < newid_maint_Rhestr[INDEX]; slot_cofnod++) SMS_Terfynell.문자(dyfais_VALUE.기억읽기(ADDRESS + slot_cofnod));
            SMS_Terfynell.문자(10);
        } else { 이름들[INDEX * 64] = 0; newid_maint_Rhestr[INDEX] = 0; SMS_Terfynell.Ysgrifennu("파일을 지웠습니다\n"); }
    }

    static boolean technoleg_gwybodaeth_EXACT(int[] 입력, int hyd_VALUE, String 문구) {
        if (hyd_VALUE != 문구.length()) return false;
        for (int slot_cofnod = 0; slot_cofnod < hyd_VALUE; slot_cofnod++) if (입력[slot_cofnod] != 문구.charAt(slot_cofnod)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int hyd_VALUE, boolean llinell_gorlif) {
        if (technoleg_gwybodaeth_EXACT(입력, hyd_VALUE, ".cancel")) {
            편집중 = false; SMS_Terfynell.Ysgrifennu("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (technoleg_gwybodaeth_EXACT(입력, hyd_VALUE, ".save")) {
            편집중 = false;
            if (gorlif_VALUE) { SMS_Terfynell.Ysgrifennu("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Enw[수] != 0) 수++;
            int mesur = Store_VALUE(Enw, 수, Golygu_VALUE, Golygu_newid_maint);
            SMS_Terfynell.Ysgrifennu(mesur >= 0 ? "보존한 beit_VALUE 수: " : "보존 methiant_VALUE: ");
            SMS_Terfynell.수쓰기(mesur); SMS_Terfynell.문자(10);
        } else if (llinell_gorlif || hyd_VALUE + 1 > 최대크기 - Golygu_newid_maint) gorlif_VALUE = true;
        else {
            for (int 수 = 0; 수 < hyd_VALUE; 수++) Golygu_VALUE[Golygu_newid_maint++] = 입력[수];
            Golygu_VALUE[Golygu_newid_maint++] = 10;
        }
    }

    static void 예제(String Ffeil, String Cynnwys_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Enw[수] = 수 < Ffeil.length() ? Ffeil.charAt(수) : 0;
        for (int 수 = 0; 수 < Cynnwys_VALUE.length(); 수++) Golygu_VALUE[수] = Cynnwys_VALUE.charAt(수);
        Store_VALUE(Enw, Ffeil.length(), Golygu_VALUE, Cynnwys_VALUE.length());
    }

    static void Paratoi() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Grŵp_VALUE = dyfais_VALUE.자바파일묶음(), Maint = dyfais_VALUE.자바파일묶음크기();
        if (Maint < 8 || 실행관리.수(Grŵp_VALUE) != 0x464a4b4a) { SMS_Terfynell.Ysgrifennu("올바르지 않은 Java Ffeil Grŵp_VALUE\n"); return; }
        int eitem_COUNT = 실행관리.수(Grŵp_VALUE + 4);
        if (eitem_COUNT < 0 || eitem_COUNT > 8 || eitem_COUNT > (Maint - 8) / 72) { SMS_Terfynell.Ysgrifennu("올바르지 않은 Java Ffeil cofnod_Rhestr\n"); return; }
        for (int 수 = 0; 수 < eitem_COUNT; 수++) {
            int cofnod_VALUE = Grŵp_VALUE + 8 + 수 * 72, hyd_VALUE = 0;
            for (int slot_cofnod = 0; slot_cofnod < 64; slot_cofnod++) Enw[slot_cofnod] = dyfais_VALUE.기억읽기(cofnod_VALUE + slot_cofnod);
            while (hyd_VALUE < 64 && Enw[hyd_VALUE] != 0) hyd_VALUE++;
            int safle = 실행관리.수(cofnod_VALUE + 64), ffeil_newid_maint = 실행관리.수(cofnod_VALUE + 68);
            if (!gwirio_enw(Enw, hyd_VALUE) || ffeil_newid_maint < 0 || ffeil_newid_maint > 최대크기 || safle < 8 + eitem_COUNT * 72 || safle > Maint - ffeil_newid_maint) {
                SMS_Terfynell.Ysgrifennu("올바르지 않은 Java Ffeil cofnod_VALUE\n"); return;
            }
            for (int slot_cofnod = 0; slot_cofnod < ffeil_newid_maint; slot_cofnod++) Golygu_VALUE[slot_cofnod] = dyfais_VALUE.기억읽기(Grŵp_VALUE + safle + slot_cofnod);
            if (Store_VALUE(Enw, hyd_VALUE, Golygu_VALUE, ffeil_newid_maint) < 0) { SMS_Terfynell.Ysgrifennu("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
