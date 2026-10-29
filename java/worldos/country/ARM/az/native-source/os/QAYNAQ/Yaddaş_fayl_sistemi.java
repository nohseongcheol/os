// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 FAYL. 원본 redaktə_VALUE/qurmaq_mənbə xəta_VALUE 시 기존 파일을 보존한다. */
public final class Yaddaş_fayl_sistemi {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] ölçünü_dəyişmək_Siyahı = new int[8];
    static int[] açmaq_COUNT = new int[8], 허가들 = new int[8];
    static int[] Ad = new int[64];
    static int[] redaktə_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean dolub_daşma_VALUE = false;
    static int redaktə_ölçünü_dəyişmək = 0;

    static boolean çek_ad(int[] simvol_VALUE_068c2631, int uzunluq_VALUE) {
        if (uzunluq_VALUE < 1 || uzunluq_VALUE > 63) return false;
        for (int 수 = 0; 수 < uzunluq_VALUE; 수++) {
            int VALUE = simvol_VALUE_068c2631[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return simvol_VALUE_068c2631[0] != '.';
    }

    static int FIND_daxiletmə(int[] simvol_VALUE_068c2631, int uzunluq_VALUE) {
        if (!çek_ad(simvol_VALUE_068c2631, uzunluq_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + uzunluq_VALUE] == 0;
            for (int slot_daxiletmə = 0; slot_daxiletmə < uzunluq_VALUE; slot_daxiletmə++) if (이름들[수 * 64 + slot_daxiletmə] != simvol_VALUE_068c2631[slot_daxiletmə]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] simvol_VALUE_068c2631, int uzunluq_VALUE, int[] verilənlər, int Böyüklük) {
        if (!çek_ad(simvol_VALUE_068c2631, uzunluq_VALUE) || Böyüklük < 0 || Böyüklük > verilənlər.length) return -22;
        if (Böyüklük > 최대크기) return -90;
        int INDEX = FIND_daxiletmə(simvol_VALUE_068c2631, uzunluq_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && açmaq_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int ünvan = cihaz_VALUE.fayl_Yaddaş() + INDEX * 최대크기;
        for (int 수 = 0; 수 < Böyüklük; 수++) cihaz_VALUE.yazmaq_Yaddaş(ünvan + 수, verilənlər[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < uzunluq_VALUE ? simvol_VALUE_068c2631[수] : 0;
        ölçünü_dəyişmək_Siyahı[INDEX] = Böyüklük;
        return Böyüklük;
    }

    static void daxiletmə_Siyahı() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int slot_daxiletmə = 0; slot_daxiletmə < 64 && 이름들[수 * 64 + slot_daxiletmə] != 0; slot_daxiletmə++) SMS_Terminal.문자(이름들[수 * 64 + slot_daxiletmə]);
            SMS_Terminal.Yazma("  "); SMS_Terminal.수쓰기(ölçünü_dəyişmək_Siyahı[수]); SMS_Terminal.Yazma("bayt_VALUE\n");
        }
        SMS_Terminal.Yazma(Yaddaş_cihaz_qoşulma.사용가능 ? "FAYL 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 FAYL 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Əmr(int[] 입력, int İcra_Et, int uzunluq_VALUE, int Gedişat) {
        while (İcra_Et < uzunluq_VALUE && 입력[İcra_Et] == ' ') İcra_Et++;
        int 끝 = uzunluq_VALUE;
        while (끝 > İcra_Et && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - İcra_Et;
        if (수 < 1 || 수 > 63) { SMS_Terminal.Yazma("올바르지 않은 FAYL Ad\n"); return; }
        for (int slot_daxiletmə = 0; slot_daxiletmə < 64; slot_daxiletmə++) Ad[slot_daxiletmə] = slot_daxiletmə < 수 ? 입력[İcra_Et + slot_daxiletmə] : 0;
        int INDEX = FIND_daxiletmə(Ad, 수);
        if (INDEX == -22) { SMS_Terminal.Yazma("올바르지 않은 FAYL Ad\n"); return; }
        if (Gedişat == 0) {
            편집중 = true; redaktə_ölçünü_dəyişmək = 0; dolub_daşma_VALUE = false;
            SMS_Terminal.Yazma("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminal.Yazma("파일을 찾을 수 없습니다\n");
        else if (Gedişat == 1) {
            int ünvan = cihaz_VALUE.fayl_Yaddaş() + INDEX * 최대크기;
            for (int slot_daxiletmə = 0; slot_daxiletmə < ölçünü_dəyişmək_Siyahı[INDEX]; slot_daxiletmə++) SMS_Terminal.문자(cihaz_VALUE.기억읽기(ünvan + slot_daxiletmə));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; ölçünü_dəyişmək_Siyahı[INDEX] = 0; SMS_Terminal.Yazma("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int uzunluq_VALUE, String 문구) {
        if (uzunluq_VALUE != 문구.length()) return false;
        for (int slot_daxiletmə = 0; slot_daxiletmə < uzunluq_VALUE; slot_daxiletmə++) if (입력[slot_daxiletmə] != 문구.charAt(slot_daxiletmə)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int uzunluq_VALUE, boolean xətt_dolub_daşma) {
        if (정확(입력, uzunluq_VALUE, ".cancel")) {
            편집중 = false; SMS_Terminal.Yazma("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, uzunluq_VALUE, ".save")) {
            편집중 = false;
            if (dolub_daşma_VALUE) { SMS_Terminal.Yazma("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Ad[수] != 0) 수++;
            int ölçü = Store_VALUE(Ad, 수, redaktə_VALUE, redaktə_ölçünü_dəyişmək);
            SMS_Terminal.Yazma(ölçü >= 0 ? "보존한 bayt_VALUE 수: " : "보존 xəta_VALUE: ");
            SMS_Terminal.수쓰기(ölçü); SMS_Terminal.문자(10);
        } else if (xətt_dolub_daşma || uzunluq_VALUE + 1 > 최대크기 - redaktə_ölçünü_dəyişmək) dolub_daşma_VALUE = true;
        else {
            for (int 수 = 0; 수 < uzunluq_VALUE; 수++) redaktə_VALUE[redaktə_ölçünü_dəyişmək++] = 입력[수];
            redaktə_VALUE[redaktə_ölçünü_dəyişmək++] = 10;
        }
    }

    static void 예제(String FAYL, String Məzmun_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Ad[수] = 수 < FAYL.length() ? FAYL.charAt(수) : 0;
        for (int 수 = 0; 수 < Məzmun_VALUE.length(); 수++) redaktə_VALUE[수] = Məzmun_VALUE.charAt(수);
        Store_VALUE(Ad, FAYL.length(), redaktə_VALUE, Məzmun_VALUE.length());
    }

    static void Hazırla() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Qrup_VALUE = cihaz_VALUE.자바파일묶음(), Böyüklük = cihaz_VALUE.자바파일묶음크기();
        if (Böyüklük < 8 || 실행관리.수(Qrup_VALUE) != 0x464a4b4a) { SMS_Terminal.Yazma("올바르지 않은 Java FAYL Qrup_VALUE\n"); return; }
        int element_COUNT = 실행관리.수(Qrup_VALUE + 4);
        if (element_COUNT < 0 || element_COUNT > 8 || element_COUNT > (Böyüklük - 8) / 72) { SMS_Terminal.Yazma("올바르지 않은 Java FAYL daxiletmə_Siyahı\n"); return; }
        for (int 수 = 0; 수 < element_COUNT; 수++) {
            int daxiletmə_VALUE = Qrup_VALUE + 8 + 수 * 72, uzunluq_VALUE = 0;
            for (int slot_daxiletmə = 0; slot_daxiletmə < 64; slot_daxiletmə++) Ad[slot_daxiletmə] = cihaz_VALUE.기억읽기(daxiletmə_VALUE + slot_daxiletmə);
            while (uzunluq_VALUE < 64 && Ad[uzunluq_VALUE] != 0) uzunluq_VALUE++;
            int yerinə_qoymaq = 실행관리.수(daxiletmə_VALUE + 64), fayl_ölçünü_dəyişmək = 실행관리.수(daxiletmə_VALUE + 68);
            if (!çek_ad(Ad, uzunluq_VALUE) || fayl_ölçünü_dəyişmək < 0 || fayl_ölçünü_dəyişmək > 최대크기 || yerinə_qoymaq < 8 + element_COUNT * 72 || yerinə_qoymaq > Böyüklük - fayl_ölçünü_dəyişmək) {
                SMS_Terminal.Yazma("올바르지 않은 Java FAYL daxiletmə_VALUE\n"); return;
            }
            for (int slot_daxiletmə = 0; slot_daxiletmə < fayl_ölçünü_dəyişmək; slot_daxiletmə++) redaktə_VALUE[slot_daxiletmə] = cihaz_VALUE.기억읽기(Qrup_VALUE + yerinə_qoymaq + slot_daxiletmə);
            if (Store_VALUE(Ad, uzunluq_VALUE, redaktə_VALUE, fayl_ölçünü_dəyişmək) < 0) { SMS_Terminal.Yazma("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
