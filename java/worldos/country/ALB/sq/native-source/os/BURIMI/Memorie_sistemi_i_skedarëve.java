// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Kartelë. 원본 redaktim_VALUE/ndërtoj_burim dështim_VALUE 시 기존 파일을 보존한다. */
public final class Memorie_sistemi_i_skedarëve {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] ndryshoj_përmasat_Listë = new int[8];
    static int[] hap_COUNT = new int[8], 허가들 = new int[8];
    static int[] Emër = new int[64];
    static int[] redaktim_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean tejkalim_VALUE = false;
    static int redaktim_ndryshoj_përmasat = 0;

    static boolean çek_emër(int[] karakter_VALUE, int gjatësi_VALUE) {
        if (gjatësi_VALUE < 1 || gjatësi_VALUE > 63) return false;
        for (int 수 = 0; 수 < gjatësi_VALUE; 수++) {
            int VALUE = karakter_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return karakter_VALUE[0] != '.';
    }

    static int FIND_futje(int[] karakter_VALUE, int gjatësi_VALUE) {
        if (!çek_emër(karakter_VALUE, gjatësi_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + gjatësi_VALUE] == 0;
            for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < gjatësi_VALUE; hapësirë_për_tekst_futje++) if (이름들[수 * 64 + hapësirë_për_tekst_futje] != karakter_VALUE[hapësirë_për_tekst_futje]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] karakter_VALUE, int gjatësi_VALUE, int[] të_dhëna, int Madhësi) {
        if (!çek_emër(karakter_VALUE, gjatësi_VALUE) || Madhësi < 0 || Madhësi > të_dhëna.length) return -22;
        if (Madhësi > 최대크기) return -90;
        int INDEX = FIND_futje(karakter_VALUE, gjatësi_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && hap_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int email = pajisje_VALUE.skedar_Memorie() + INDEX * 최대크기;
        for (int 수 = 0; 수 < Madhësi; 수++) pajisje_VALUE.shkruaj_Memorie(email + 수, të_dhëna[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < gjatësi_VALUE ? karakter_VALUE[수] : 0;
        ndryshoj_përmasat_Listë[INDEX] = Madhësi;
        return Madhësi;
    }

    static void futje_Listë() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 64 && 이름들[수 * 64 + hapësirë_për_tekst_futje] != 0; hapësirë_për_tekst_futje++) SMS_Terminali.문자(이름들[수 * 64 + hapësirë_për_tekst_futje]);
            SMS_Terminali.Shkrimi("  "); SMS_Terminali.수쓰기(ndryshoj_përmasat_Listë[수]); SMS_Terminali.Shkrimi("bajt_VALUE\n");
        }
        SMS_Terminali.Shkrimi(hapësira_ruajtëse_pajisje_lidhje.teknologjia_e_informacionit_Aktiv_9e72441a ? "Kartelë 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Kartelë 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Komanda(int[] 입력, int Ekzekuto, int gjatësi_VALUE, int Veprim) {
        while (Ekzekuto < gjatësi_VALUE && 입력[Ekzekuto] == ' ') Ekzekuto++;
        int 끝 = gjatësi_VALUE;
        while (끝 > Ekzekuto && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Ekzekuto;
        if (수 < 1 || 수 > 63) { SMS_Terminali.Shkrimi("올바르지 않은 Kartelë Emër\n"); return; }
        for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 64; hapësirë_për_tekst_futje++) Emër[hapësirë_për_tekst_futje] = hapësirë_për_tekst_futje < 수 ? 입력[Ekzekuto + hapësirë_për_tekst_futje] : 0;
        int INDEX = FIND_futje(Emër, 수);
        if (INDEX == -22) { SMS_Terminali.Shkrimi("올바르지 않은 Kartelë Emër\n"); return; }
        if (Veprim == 0) {
            편집중 = true; redaktim_ndryshoj_përmasat = 0; tejkalim_VALUE = false;
            SMS_Terminali.Shkrimi("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminali.Shkrimi("파일을 찾을 수 없습니다\n");
        else if (Veprim == 1) {
            int email = pajisje_VALUE.skedar_Memorie() + INDEX * 최대크기;
            for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < ndryshoj_përmasat_Listë[INDEX]; hapësirë_për_tekst_futje++) SMS_Terminali.문자(pajisje_VALUE.기억읽기(email + hapësirë_për_tekst_futje));
            SMS_Terminali.문자(10);
        } else { 이름들[INDEX * 64] = 0; ndryshoj_përmasat_Listë[INDEX] = 0; SMS_Terminali.Shkrimi("파일을 지웠습니다\n"); }
    }

    static boolean teknologjia_e_informacionit_EXACT(int[] 입력, int gjatësi_VALUE, String 문구) {
        if (gjatësi_VALUE != 문구.length()) return false;
        for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < gjatësi_VALUE; hapësirë_për_tekst_futje++) if (입력[hapësirë_për_tekst_futje] != 문구.charAt(hapësirë_për_tekst_futje)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int gjatësi_VALUE, boolean linjë_tejkalim) {
        if (teknologjia_e_informacionit_EXACT(입력, gjatësi_VALUE, ".cancel")) {
            편집중 = false; SMS_Terminali.Shkrimi("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (teknologjia_e_informacionit_EXACT(입력, gjatësi_VALUE, ".save")) {
            편집중 = false;
            if (tejkalim_VALUE) { SMS_Terminali.Shkrimi("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Emër[수] != 0) 수++;
            int llogaritje = Store_VALUE(Emër, 수, redaktim_VALUE, redaktim_ndryshoj_përmasat);
            SMS_Terminali.Shkrimi(llogaritje >= 0 ? "보존한 bajt_VALUE 수: " : "보존 dështim_VALUE: ");
            SMS_Terminali.수쓰기(llogaritje); SMS_Terminali.문자(10);
        } else if (linjë_tejkalim || gjatësi_VALUE + 1 > 최대크기 - redaktim_ndryshoj_përmasat) tejkalim_VALUE = true;
        else {
            for (int 수 = 0; 수 < gjatësi_VALUE; 수++) redaktim_VALUE[redaktim_ndryshoj_përmasat++] = 입력[수];
            redaktim_VALUE[redaktim_ndryshoj_përmasat++] = 10;
        }
    }

    static void 예제(String Kartelë, String Përmbajtje_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Emër[수] = 수 < Kartelë.length() ? Kartelë.charAt(수) : 0;
        for (int 수 = 0; 수 < Përmbajtje_VALUE.length(); 수++) redaktim_VALUE[수] = Përmbajtje_VALUE.charAt(수);
        Store_VALUE(Emër, Kartelë.length(), redaktim_VALUE, Përmbajtje_VALUE.length());
    }

    static void Përgatit() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int grup_VALUE = pajisje_VALUE.자바파일묶음(), Madhësi = pajisje_VALUE.자바파일묶음크기();
        if (Madhësi < 8 || 실행관리.수(grup_VALUE) != 0x464a4b4a) { SMS_Terminali.Shkrimi("올바르지 않은 Java Kartelë grup_VALUE\n"); return; }
        int njësi_COUNT = 실행관리.수(grup_VALUE + 4);
        if (njësi_COUNT < 0 || njësi_COUNT > 8 || njësi_COUNT > (Madhësi - 8) / 72) { SMS_Terminali.Shkrimi("올바르지 않은 Java Kartelë futje_Listë\n"); return; }
        for (int 수 = 0; 수 < njësi_COUNT; 수++) {
            int futje_VALUE = grup_VALUE + 8 + 수 * 72, gjatësi_VALUE = 0;
            for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 64; hapësirë_për_tekst_futje++) Emër[hapësirë_për_tekst_futje] = pajisje_VALUE.기억읽기(futje_VALUE + hapësirë_për_tekst_futje);
            while (gjatësi_VALUE < 64 && Emër[gjatësi_VALUE] != 0) gjatësi_VALUE++;
            int Pozicioni = 실행관리.수(futje_VALUE + 64), skedar_ndryshoj_përmasat = 실행관리.수(futje_VALUE + 68);
            if (!çek_emër(Emër, gjatësi_VALUE) || skedar_ndryshoj_përmasat < 0 || skedar_ndryshoj_përmasat > 최대크기 || Pozicioni < 8 + njësi_COUNT * 72 || Pozicioni > Madhësi - skedar_ndryshoj_përmasat) {
                SMS_Terminali.Shkrimi("올바르지 않은 Java Kartelë futje_VALUE\n"); return;
            }
            for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < skedar_ndryshoj_përmasat; hapësirë_për_tekst_futje++) redaktim_VALUE[hapësirë_për_tekst_futje] = pajisje_VALUE.기억읽기(grup_VALUE + Pozicioni + hapësirë_për_tekst_futje);
            if (Store_VALUE(Emër, gjatësi_VALUE, redaktim_VALUE, skedar_ndryshoj_përmasat) < 0) { SMS_Terminali.Shkrimi("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
