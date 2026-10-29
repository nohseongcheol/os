// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Yazma 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int uzunluq_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean xətt_dolub_daşma = false;

    static boolean Əmr(String Ad) {
        if (uzunluq_VALUE < Ad.length()) return false;
        for (int INDEX = 0; INDEX < Ad.length(); INDEX++)
            if (입력[INDEX] != Ad.charAt(INDEX)) return false;
        return uzunluq_VALUE == Ad.length() || 입력[Ad.length()] == ' ';
    }

    static void göstərmək_kömək() {
        SMS_Terminal.Yazma("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Yazma("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Yazma("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Yazma("sync (연결된 JKSTORE1 Store_VALUE 장치에 FAYL 보존)\n");
    }

    static void Proses_VALUE_daxiletmə() {
        if (uzunluq_VALUE == 0) return;
        if (Əmr("help")) göstərmək_kömək();
        else if (Əmr("sync")) {
            int ölçü = 파일보존.sinxronlaşdırmaq();
            SMS_Terminal.Yazma("Sync: "); SMS_Terminal.수쓰기(ölçü); SMS_Terminal.문자(10);
        }
        else if (Əmr("ls")) Yaddaş_fayl_sistemi.daxiletmə_Siyahı();
        else if (Əmr("edit")) Yaddaş_fayl_sistemi.Əmr(입력, 4, uzunluq_VALUE, 0);
        else if (Əmr("cat")) Yaddaş_fayl_sistemi.Əmr(입력, 3, uzunluq_VALUE, 1);
        else if (Əmr("rm")) Yaddaş_fayl_sistemi.Əmr(입력, 2, uzunluq_VALUE, 2);
        else if (Əmr("java") || Əmr("javac")) {
            int ölçü = 실행관리.icra_etmək_əmr(입력, 0, uzunluq_VALUE);
            SMS_Terminal.Yazma("Exit: "); SMS_Terminal.수쓰기(ölçü); SMS_Terminal.문자(10);
        }
        else if (Əmr("apps")) 실행관리.daxiletmə_Siyahı();
        else if (Əmr("net")) Şəbəkə_Yığın.vəziyyət_VALUE();
        else if (Əmr("run")) {
            int ölçü = 실행관리.icra_etmək_əmr(입력, 3, uzunluq_VALUE);
            SMS_Terminal.Yazma("Exit: "); SMS_Terminal.수쓰기(ölçü); SMS_Terminal.Yazma("\n");
        } else if (Əmr("info")) {
            SMS_Terminal.Yazma("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Əmr("mem")) {
            SMS_Terminal.Yazma("위쪽 Yaddaş_VALUE 공간(KiB): "); SMS_Terminal.수쓰기(기억공간.UPPER_Yaddaş_ölçünü_dəyişmək());
            SMS_Terminal.Yazma("\n배열 동적 Yaddaş_VALUE 공간(bayt_VALUE): "); SMS_Terminal.수쓰기(cihaz_VALUE.ARRAY_istifadə());
            SMS_Terminal.Yazma(" / 262144\n작업 공간 bölmə_VALUE_366e0bfa: "); SMS_Terminal.수쓰기(기억공간.사용개수());
            SMS_Terminal.Yazma(" / 8 (각 4096바이트)\n");
        } else if (Əmr("alloc")) {
            int INDEX = 기억공간.ayırmaq_Yaddaş();
            SMS_Terminal.Yazma("bölmə_VALUE_366e0bfa INDEX: "); SMS_Terminal.수쓰기(INDEX); SMS_Terminal.Yazma("\n");
        } else if (Əmr("free")) {
            if (uzunluq_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminal.Yazma(기억공간.geri_qaytarmaq_ölçü(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 bölmə_VALUE_366e0bfa\n");
            } else SMS_Terminal.Yazma("사용법: free 0..7\n");
        } else if (Əmr("echo")) {
            for (int INDEX = 5; INDEX < uzunluq_VALUE; INDEX++) SMS_Terminal.문자(입력[INDEX]);
            SMS_Terminal.문자(10);
        } else if (Əmr("clear")) SMS_Terminal.silmək_daxiletmə_c8dbc399();
        else if (Əmr("test")) nüvə.시험();
        else if (Əmr("halt")) {
            SMS_Terminal.Yazma("HALTED\n");
            cihaz_VALUE.정지();
        } else SMS_Terminal.Yazma("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void qəbul_et_AND_yazmaq(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminal.문자(10);
            if (Yaddaş_fayl_sistemi.편집중) Yaddaş_fayl_sistemi.편집줄(입력, uzunluq_VALUE, xətt_dolub_daşma);
            else Proses_VALUE_daxiletmə();
            uzunluq_VALUE = 0;
            xətt_dolub_daşma = false;
            SMS_Terminal.Yazma(Yaddaş_fayl_sistemi.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (uzunluq_VALUE > 0) {
                uzunluq_VALUE--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && uzunluq_VALUE < 입력.length) {
            입력[uzunluq_VALUE++] = VALUE;
            SMS_Terminal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) xətt_dolub_daşma = true;
    }

    static void İcra_Et() {
        göstərmək_kömək();
        SMS_Terminal.Yazma("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminal.직렬읽기();
            if (VALUE < 0) VALUE = klaviatura.Oxuma();
            if (VALUE >= 0) qəbul_et_AND_yazmaq(VALUE);
            else { Şəbəkə_Yığın.yoxlamaq(); cihaz_VALUE.잠시양보(); }
        }
    }
}
