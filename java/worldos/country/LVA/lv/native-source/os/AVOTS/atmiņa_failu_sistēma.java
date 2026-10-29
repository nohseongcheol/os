// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Fails. 원본 Rediģēt_VALUE/kompilēt_avots kļūme_VALUE 시 기존 파일을 보존한다. */
public final class atmiņa_failu_sistēma {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] mainīt_izmērus_Saraksts = new int[8];
    static int[] atvērt_COUNT = new int[8], 허가들 = new int[8];
    static int[] Nosaukums = new int[64];
    static int[] Rediģēt_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean pārpilde_VALUE = false;
    static int Rediģēt_mainīt_izmērus = 0;

    static boolean čeks_nosaukums(int[] rakstzīme_VALUE, int 길이) {
        if (길이 < 1 || 길이 > 63) return false;
        for (int numurs = 0; numurs < 길이; numurs++) {
            int VALUE = rakstzīme_VALUE[numurs];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return rakstzīme_VALUE[0] != '.';
    }

    static int FIND_ievade(int[] rakstzīme_VALUE, int 길이) {
        if (!čeks_nosaukums(rakstzīme_VALUE, 길이)) return -22;
        for (int numurs = 0; numurs < 8; numurs++) {
            boolean 같음 = 이름들[numurs * 64 + 길이] == 0;
            for (int 칸 = 0; 칸 < 길이; 칸++) if (이름들[numurs * 64 + 칸] != rakstzīme_VALUE[칸]) 같음 = false;
            if (같음) return numurs;
        }
        return -2;
    }

    static int Store_VALUE(int[] rakstzīme_VALUE, int 길이, int[] dati, int Izmērs) {
        if (!čeks_nosaukums(rakstzīme_VALUE, 길이) || Izmērs < 0 || Izmērs > dati.length) return -22;
        if (Izmērs > 최대크기) return -90;
        int INDEX = FIND_ievade(rakstzīme_VALUE, 길이);
        if (INDEX == -2) {
            for (int numurs = 0; numurs < 8 && INDEX < 0; numurs++) if (이름들[numurs * 64] == 0 && atvērt_COUNT[numurs] == 0) INDEX = numurs;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int adrese = ierīce_VALUE.Fails_atmiņa() + INDEX * 최대크기;
        for (int numurs = 0; numurs < Izmērs; numurs++) ierīce_VALUE.rakstīšana_atmiņa(adrese + numurs, dati[numurs]);
        for (int numurs = 0; numurs < 64; numurs++) 이름들[INDEX * 64 + numurs] = numurs < 길이 ? rakstzīme_VALUE[numurs] : 0;
        mainīt_izmērus_Saraksts[INDEX] = Izmērs;
        return Izmērs;
    }

    static void ievade_Saraksts() {
        for (int numurs = 0; numurs < 8; numurs++) if (이름들[numurs * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[numurs * 64 + 칸] != 0; 칸++) SMS_Terminālis.문자(이름들[numurs * 64 + 칸]);
            SMS_Terminālis.Rakstīt("  "); SMS_Terminālis.rakstīšana_numurs(mainīt_izmērus_Saraksts[numurs]); SMS_Terminālis.Rakstīt("byte_VALUE\n");
        }
        SMS_Terminālis.Rakstīt(atmiņas_ierīce_paziņa.informācijas_tehnoloģija_Aktīvs_9e72441a ? "Fails 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Fails 8칸, 파일당 16384바이트; mēģināt_vēlreiz_VALUE 시작하면 사라짐\n");
    }

    static void Komanda(int[] 입력, int Palaist, int 길이, int Darbība) {
        while (Palaist < 길이 && 입력[Palaist] == ' ') Palaist++;
        int 끝 = 길이;
        while (끝 > Palaist && 입력[끝 - 1] == ' ') 끝--;
        int numurs = 끝 - Palaist;
        if (numurs < 1 || numurs > 63) { SMS_Terminālis.Rakstīt("올바르지 않은 Fails Nosaukums\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) Nosaukums[칸] = 칸 < numurs ? 입력[Palaist + 칸] : 0;
        int INDEX = FIND_ievade(Nosaukums, numurs);
        if (INDEX == -22) { SMS_Terminālis.Rakstīt("올바르지 않은 Fails Nosaukums\n"); return; }
        if (Darbība == 0) {
            편집중 = true; Rediģēt_mainīt_izmērus = 0; pārpilde_VALUE = false;
            SMS_Terminālis.Rakstīt("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminālis.Rakstīt("파일을 찾을 numurs 없습니다\n");
        else if (Darbība == 1) {
            int adrese = ierīce_VALUE.Fails_atmiņa() + INDEX * 최대크기;
            for (int 칸 = 0; 칸 < mainīt_izmērus_Saraksts[INDEX]; 칸++) SMS_Terminālis.문자(ierīce_VALUE.기억읽기(adrese + 칸));
            SMS_Terminālis.문자(10);
        } else { 이름들[INDEX * 64] = 0; mainīt_izmērus_Saraksts[INDEX] = 0; SMS_Terminālis.Rakstīt("파일을 지웠습니다\n"); }
    }

    static boolean informācijas_tehnoloģija_EXACT(int[] 입력, int 길이, String 문구) {
        if (길이 != 문구.length()) return false;
        for (int 칸 = 0; 칸 < 길이; 칸++) if (입력[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void Rediģētie_līnija(int[] 입력, int 길이, boolean līnija_pārpilde) {
        if (informācijas_tehnoloģija_EXACT(입력, 길이, ".cancel")) {
            편집중 = false; SMS_Terminālis.Rakstīt("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (informācijas_tehnoloģija_EXACT(입력, 길이, ".save")) {
            편집중 = false;
            if (pārpilde_VALUE) { SMS_Terminālis.Rakstīt("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int numurs = 0;
            while (numurs < 64 && Nosaukums[numurs] != 0) numurs++;
            int mērs = Store_VALUE(Nosaukums, numurs, Rediģēt_VALUE, Rediģēt_mainīt_izmērus);
            SMS_Terminālis.Rakstīt(mērs >= 0 ? "보존한 byte_VALUE numurs: " : "보존 kļūme_VALUE: ");
            SMS_Terminālis.rakstīšana_numurs(mērs); SMS_Terminālis.문자(10);
        } else if (līnija_pārpilde || 길이 + 1 > 최대크기 - Rediģēt_mainīt_izmērus) pārpilde_VALUE = true;
        else {
            for (int numurs = 0; numurs < 길이; numurs++) Rediģēt_VALUE[Rediģēt_mainīt_izmērus++] = 입력[numurs];
            Rediģēt_VALUE[Rediģēt_mainīt_izmērus++] = 10;
        }
    }

    static void 예제(String Fails, String Saturs_VALUE) {
        for (int numurs = 0; numurs < 64; numurs++) Nosaukums[numurs] = numurs < Fails.length() ? Fails.charAt(numurs) : 0;
        for (int numurs = 0; numurs < Saturs_VALUE.length(); numurs++) Rediģēt_VALUE[numurs] = Saturs_VALUE.charAt(numurs);
        Store_VALUE(Nosaukums, Fails.length(), Rediģēt_VALUE, Saturs_VALUE.length());
    }

    static void Sagatavot() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Grupa_VALUE = ierīce_VALUE.자바파일묶음(), Izmērs = ierīce_VALUE.자바파일묶음크기();
        if (Izmērs < 8 || 실행관리.numurs(Grupa_VALUE) != 0x464a4b4a) { SMS_Terminālis.Rakstīt("올바르지 않은 Java Fails Grupa_VALUE\n"); return; }
        int krājums_COUNT = 실행관리.numurs(Grupa_VALUE + 4);
        if (krājums_COUNT < 0 || krājums_COUNT > 8 || krājums_COUNT > (Izmērs - 8) / 72) { SMS_Terminālis.Rakstīt("올바르지 않은 Java Fails ievade_Saraksts\n"); return; }
        for (int numurs = 0; numurs < krājums_COUNT; numurs++) {
            int ievade_VALUE = Grupa_VALUE + 8 + numurs * 72, 길이 = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Nosaukums[칸] = ierīce_VALUE.기억읽기(ievade_VALUE + 칸);
            while (길이 < 64 && Nosaukums[길이] != 0) 길이++;
            int Novietojums = 실행관리.numurs(ievade_VALUE + 64), faila_lielums = 실행관리.numurs(ievade_VALUE + 68);
            if (!čeks_nosaukums(Nosaukums, 길이) || faila_lielums < 0 || faila_lielums > 최대크기 || Novietojums < 8 + krājums_COUNT * 72 || Novietojums > Izmērs - faila_lielums) {
                SMS_Terminālis.Rakstīt("올바르지 않은 Java Fails ievade_VALUE\n"); return;
            }
            for (int 칸 = 0; 칸 < faila_lielums; 칸++) Rediģēt_VALUE[칸] = ierīce_VALUE.기억읽기(Grupa_VALUE + Novietojums + 칸);
            if (Store_VALUE(Nosaukums, 길이, Rediģēt_VALUE, faila_lielums) < 0) { SMS_Terminālis.Rakstīt("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
