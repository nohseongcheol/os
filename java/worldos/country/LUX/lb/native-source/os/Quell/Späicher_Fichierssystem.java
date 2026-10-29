// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Fichier. 원본 Editéieren_VALUE/erstellen_Quell Feeler_VALUE 시 기존 파일을 보존한다. */
public final class Späicher_Fichierssystem {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] d_Gréisst_veränneren_Lëscht = new int[8];
    static int[] ariichten_COUNT = new int[8], 허가들 = new int[8];
    static int[] Numm = new int[64];
    static int[] Editéieren_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean Iwwerlaf_VALUE = false;
    static int Editéieren_d_Gréisst_veränneren = 0;

    static boolean Scheck_Numm(int[] Zeechen_VALUE, int Längt_VALUE) {
        if (Längt_VALUE < 1 || Längt_VALUE > 63) return false;
        for (int 수 = 0; 수 < Längt_VALUE; 수++) {
            int VALUE = Zeechen_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return Zeechen_VALUE[0] != '.';
    }

    static int FIND_Agab(int[] Zeechen_VALUE, int Längt_VALUE) {
        if (!Scheck_Numm(Zeechen_VALUE, Längt_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + Längt_VALUE] == 0;
            for (int Slot_Agab = 0; Slot_Agab < Längt_VALUE; Slot_Agab++) if (이름들[수 * 64 + Slot_Agab] != Zeechen_VALUE[Slot_Agab]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] Zeechen_VALUE, int Längt_VALUE, int[] Daten, int d_Gréisst_veränneren) {
        if (!Scheck_Numm(Zeechen_VALUE, Längt_VALUE) || d_Gréisst_veränneren < 0 || d_Gréisst_veränneren > Daten.length) return -22;
        if (d_Gréisst_veränneren > 최대크기) return -90;
        int INDEX = FIND_Agab(Zeechen_VALUE, Längt_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && ariichten_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int Adress = Mobil_VALUE.Fichier_Späicher() + INDEX * 최대크기;
        for (int 수 = 0; 수 < d_Gréisst_veränneren; 수++) Mobil_VALUE.schreiwen_Späicher(Adress + 수, Daten[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < Längt_VALUE ? Zeechen_VALUE[수] : 0;
        d_Gréisst_veränneren_Lëscht[INDEX] = d_Gréisst_veränneren;
        return d_Gréisst_veränneren;
    }

    static void Agab_Lëscht() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int Slot_Agab = 0; Slot_Agab < 64 && 이름들[수 * 64 + Slot_Agab] != 0; Slot_Agab++) SMS_Terminal.문자(이름들[수 * 64 + Slot_Agab]);
            SMS_Terminal.schreiwen("  "); SMS_Terminal.수쓰기(d_Gréisst_veränneren_Lëscht[수]); SMS_Terminal.schreiwen("Byte_VALUE\n");
        }
        SMS_Terminal.schreiwen(Späicher_Mobil_Verbindung.사용가능 ? "Fichier 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Fichier 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Befeel(int[] 입력, int Laf, int Längt_VALUE, int Aktioun) {
        while (Laf < Längt_VALUE && 입력[Laf] == ' ') Laf++;
        int 끝 = Längt_VALUE;
        while (끝 > Laf && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Laf;
        if (수 < 1 || 수 > 63) { SMS_Terminal.schreiwen("올바르지 않은 Fichier Numm\n"); return; }
        for (int Slot_Agab = 0; Slot_Agab < 64; Slot_Agab++) Numm[Slot_Agab] = Slot_Agab < 수 ? 입력[Laf + Slot_Agab] : 0;
        int INDEX = FIND_Agab(Numm, 수);
        if (INDEX == -22) { SMS_Terminal.schreiwen("올바르지 않은 Fichier Numm\n"); return; }
        if (Aktioun == 0) {
            편집중 = true; Editéieren_d_Gréisst_veränneren = 0; Iwwerlaf_VALUE = false;
            SMS_Terminal.schreiwen("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminal.schreiwen("파일을 찾을 수 없습니다\n");
        else if (Aktioun == 1) {
            int Adress = Mobil_VALUE.Fichier_Späicher() + INDEX * 최대크기;
            for (int Slot_Agab = 0; Slot_Agab < d_Gréisst_veränneren_Lëscht[INDEX]; Slot_Agab++) SMS_Terminal.문자(Mobil_VALUE.기억읽기(Adress + Slot_Agab));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; d_Gréisst_veränneren_Lëscht[INDEX] = 0; SMS_Terminal.schreiwen("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int Längt_VALUE, String 문구) {
        if (Längt_VALUE != 문구.length()) return false;
        for (int Slot_Agab = 0; Slot_Agab < Längt_VALUE; Slot_Agab++) if (입력[Slot_Agab] != 문구.charAt(Slot_Agab)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int Längt_VALUE, boolean Zeil_Iwwerlaf) {
        if (정확(입력, Längt_VALUE, ".cancel")) {
            편집중 = false; SMS_Terminal.schreiwen("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, Längt_VALUE, ".save")) {
            편집중 = false;
            if (Iwwerlaf_VALUE) { SMS_Terminal.schreiwen("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Numm[수] != 0) 수++;
            int Mooss = Store_VALUE(Numm, 수, Editéieren_VALUE, Editéieren_d_Gréisst_veränneren);
            SMS_Terminal.schreiwen(Mooss >= 0 ? "보존한 Byte_VALUE 수: " : "보존 Feeler_VALUE: ");
            SMS_Terminal.수쓰기(Mooss); SMS_Terminal.문자(10);
        } else if (Zeil_Iwwerlaf || Längt_VALUE + 1 > 최대크기 - Editéieren_d_Gréisst_veränneren) Iwwerlaf_VALUE = true;
        else {
            for (int 수 = 0; 수 < Längt_VALUE; 수++) Editéieren_VALUE[Editéieren_d_Gréisst_veränneren++] = 입력[수];
            Editéieren_VALUE[Editéieren_d_Gréisst_veränneren++] = 10;
        }
    }

    static void 예제(String Fichier, String Inhalt_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Numm[수] = 수 < Fichier.length() ? Fichier.charAt(수) : 0;
        for (int 수 = 0; 수 < Inhalt_VALUE.length(); 수++) Editéieren_VALUE[수] = Inhalt_VALUE.charAt(수);
        Store_VALUE(Numm, Fichier.length(), Editéieren_VALUE, Inhalt_VALUE.length());
    }

    static void Préparéieren() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Grupp_VALUE = Mobil_VALUE.자바파일묶음(), d_Gréisst_veränneren = Mobil_VALUE.자바파일묶음크기();
        if (d_Gréisst_veränneren < 8 || 실행관리.수(Grupp_VALUE) != 0x464a4b4a) { SMS_Terminal.schreiwen("올바르지 않은 Java Fichier Grupp_VALUE\n"); return; }
        int Element_COUNT = 실행관리.수(Grupp_VALUE + 4);
        if (Element_COUNT < 0 || Element_COUNT > 8 || Element_COUNT > (d_Gréisst_veränneren - 8) / 72) { SMS_Terminal.schreiwen("올바르지 않은 Java Fichier Agab_Lëscht\n"); return; }
        for (int 수 = 0; 수 < Element_COUNT; 수++) {
            int Agab_VALUE = Grupp_VALUE + 8 + 수 * 72, Längt_VALUE = 0;
            for (int Slot_Agab = 0; Slot_Agab < 64; Slot_Agab++) Numm[Slot_Agab] = Mobil_VALUE.기억읽기(Agab_VALUE + Slot_Agab);
            while (Längt_VALUE < 64 && Numm[Längt_VALUE] != 0) Längt_VALUE++;
            int positionéieren = 실행관리.수(Agab_VALUE + 64), Fichier_d_Gréisst_veränneren = 실행관리.수(Agab_VALUE + 68);
            if (!Scheck_Numm(Numm, Längt_VALUE) || Fichier_d_Gréisst_veränneren < 0 || Fichier_d_Gréisst_veränneren > 최대크기 || positionéieren < 8 + Element_COUNT * 72 || positionéieren > d_Gréisst_veränneren - Fichier_d_Gréisst_veränneren) {
                SMS_Terminal.schreiwen("올바르지 않은 Java Fichier Agab_VALUE\n"); return;
            }
            for (int Slot_Agab = 0; Slot_Agab < Fichier_d_Gréisst_veränneren; Slot_Agab++) Editéieren_VALUE[Slot_Agab] = Mobil_VALUE.기억읽기(Grupp_VALUE + positionéieren + Slot_Agab);
            if (Store_VALUE(Numm, Längt_VALUE, Editéieren_VALUE, Fichier_d_Gréisst_veränneren) < 0) { SMS_Terminal.schreiwen("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
