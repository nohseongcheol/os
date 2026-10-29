// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 file. 원본 edit_VALUE/bumuo_pinagmulan pagpalya_VALUE 시 기존 파일을 보존한다. */
public final class Memory_sistema_ng_file {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] sukat_list = new int[8];
    static int[] buksan_COUNT = new int[8], 허가들 = new int[8];
    static int[] pangalan = new int[64];
    static int[] edit_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean sobrang_teksto_VALUE = false;
    static int edit_sukat = 0;

    static boolean tseke_pangalan(int[] karakter_VALUE, int haba_VALUE) {
        if (haba_VALUE < 1 || haba_VALUE > 63) return false;
        for (int 수 = 0; 수 < haba_VALUE; 수++) {
            int VALUE = karakter_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return karakter_VALUE[0] != '.';
    }

    static int FIND_pagpasok(int[] karakter_VALUE, int haba_VALUE) {
        if (!tseke_pangalan(karakter_VALUE, haba_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + haba_VALUE] == 0;
            for (int espasyo_pagpasok = 0; espasyo_pagpasok < haba_VALUE; espasyo_pagpasok++) if (이름들[수 * 64 + espasyo_pagpasok] != karakter_VALUE[espasyo_pagpasok]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] karakter_VALUE, int haba_VALUE, int[] data, int sukat_82232621) {
        if (!tseke_pangalan(karakter_VALUE, haba_VALUE) || sukat_82232621 < 0 || sukat_82232621 > data.length) return -22;
        if (sukat_82232621 > 최대크기) return -90;
        int INDEX = FIND_pagpasok(karakter_VALUE, haba_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && buksan_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int email = device_VALUE.file_Memory() + INDEX * 최대크기;
        for (int 수 = 0; 수 < sukat_82232621; 수++) device_VALUE.sumulat_Memory(email + 수, data[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < haba_VALUE ? karakter_VALUE[수] : 0;
        sukat_list[INDEX] = sukat_82232621;
        return sukat_82232621;
    }

    static void pagpasok_list() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int espasyo_pagpasok = 0; espasyo_pagpasok < 64 && 이름들[수 * 64 + espasyo_pagpasok] != 0; espasyo_pagpasok++) SMS_Terminal.문자(이름들[수 * 64 + espasyo_pagpasok]);
            SMS_Terminal.sumulat("  "); SMS_Terminal.수쓰기(sukat_list[수]); SMS_Terminal.sumulat("byte_VALUE\n");
        }
        SMS_Terminal.sumulat(Storage_device_koneksyon.information_technology_Aktibo_9e72441a ? "file 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 file 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void utos(int[] 입력, int run, int haba_VALUE, int aksyon) {
        while (run < haba_VALUE && 입력[run] == ' ') run++;
        int 끝 = haba_VALUE;
        while (끝 > run && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - run;
        if (수 < 1 || 수 > 63) { SMS_Terminal.sumulat("올바르지 않은 file pangalan\n"); return; }
        for (int espasyo_pagpasok = 0; espasyo_pagpasok < 64; espasyo_pagpasok++) pangalan[espasyo_pagpasok] = espasyo_pagpasok < 수 ? 입력[run + espasyo_pagpasok] : 0;
        int INDEX = FIND_pagpasok(pangalan, 수);
        if (INDEX == -22) { SMS_Terminal.sumulat("올바르지 않은 file pangalan\n"); return; }
        if (aksyon == 0) {
            편집중 = true; edit_sukat = 0; sobrang_teksto_VALUE = false;
            SMS_Terminal.sumulat("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminal.sumulat("파일을 찾을 수 없습니다\n");
        else if (aksyon == 1) {
            int email = device_VALUE.file_Memory() + INDEX * 최대크기;
            for (int espasyo_pagpasok = 0; espasyo_pagpasok < sukat_list[INDEX]; espasyo_pagpasok++) SMS_Terminal.문자(device_VALUE.기억읽기(email + espasyo_pagpasok));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; sukat_list[INDEX] = 0; SMS_Terminal.sumulat("파일을 지웠습니다\n"); }
    }

    static boolean information_technology_EXACT(int[] 입력, int haba_VALUE, String 문구) {
        if (haba_VALUE != 문구.length()) return false;
        for (int espasyo_pagpasok = 0; espasyo_pagpasok < haba_VALUE; espasyo_pagpasok++) if (입력[espasyo_pagpasok] != 문구.charAt(espasyo_pagpasok)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int haba_VALUE, boolean linya_sobrang_teksto) {
        if (information_technology_EXACT(입력, haba_VALUE, ".cancel")) {
            편집중 = false; SMS_Terminal.sumulat("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (information_technology_EXACT(입력, haba_VALUE, ".save")) {
            편집중 = false;
            if (sobrang_teksto_VALUE) { SMS_Terminal.sumulat("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && pangalan[수] != 0) 수++;
            int sukat = Store_VALUE(pangalan, 수, edit_VALUE, edit_sukat);
            SMS_Terminal.sumulat(sukat >= 0 ? "보존한 byte_VALUE 수: " : "보존 pagpalya_VALUE: ");
            SMS_Terminal.수쓰기(sukat); SMS_Terminal.문자(10);
        } else if (linya_sobrang_teksto || haba_VALUE + 1 > 최대크기 - edit_sukat) sobrang_teksto_VALUE = true;
        else {
            for (int 수 = 0; 수 < haba_VALUE; 수++) edit_VALUE[edit_sukat++] = 입력[수];
            edit_VALUE[edit_sukat++] = 10;
        }
    }

    static void 예제(String file, String Nilalaman_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) pangalan[수] = 수 < file.length() ? file.charAt(수) : 0;
        for (int 수 = 0; 수 < Nilalaman_VALUE.length(); 수++) edit_VALUE[수] = Nilalaman_VALUE.charAt(수);
        Store_VALUE(pangalan, file.length(), edit_VALUE, Nilalaman_VALUE.length());
    }

    static void Ihanda() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Grupo_VALUE = device_VALUE.자바파일묶음(), sukat_82232621 = device_VALUE.자바파일묶음크기();
        if (sukat_82232621 < 8 || 실행관리.수(Grupo_VALUE) != 0x464a4b4a) { SMS_Terminal.sumulat("올바르지 않은 Java file Grupo_VALUE\n"); return; }
        int item_COUNT = 실행관리.수(Grupo_VALUE + 4);
        if (item_COUNT < 0 || item_COUNT > 8 || item_COUNT > (sukat_82232621 - 8) / 72) { SMS_Terminal.sumulat("올바르지 않은 Java file pagpasok_list\n"); return; }
        for (int 수 = 0; 수 < item_COUNT; 수++) {
            int pagpasok_VALUE = Grupo_VALUE + 8 + 수 * 72, haba_VALUE = 0;
            for (int espasyo_pagpasok = 0; espasyo_pagpasok < 64; espasyo_pagpasok++) pangalan[espasyo_pagpasok] = device_VALUE.기억읽기(pagpasok_VALUE + espasyo_pagpasok);
            while (haba_VALUE < 64 && pangalan[haba_VALUE] != 0) haba_VALUE++;
            int posisyon = 실행관리.수(pagpasok_VALUE + 64), file_sukat = 실행관리.수(pagpasok_VALUE + 68);
            if (!tseke_pangalan(pangalan, haba_VALUE) || file_sukat < 0 || file_sukat > 최대크기 || posisyon < 8 + item_COUNT * 72 || posisyon > sukat_82232621 - file_sukat) {
                SMS_Terminal.sumulat("올바르지 않은 Java file pagpasok_VALUE\n"); return;
            }
            for (int espasyo_pagpasok = 0; espasyo_pagpasok < file_sukat; espasyo_pagpasok++) edit_VALUE[espasyo_pagpasok] = device_VALUE.기억읽기(Grupo_VALUE + posisyon + espasyo_pagpasok);
            if (Store_VALUE(pangalan, haba_VALUE, edit_VALUE, file_sukat) < 0) { SMS_Terminal.sumulat("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
