// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Kọ 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int gígùn_iye = 0;
    static boolean 앞줄복귀 = false;
    static boolean ìlà_rékọjá = false;

    static boolean Àṣẹ(String Orúkọ) {
        if (gígùn_iye < Orúkọ.length()) return false;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < Orúkọ.length(); wá_atọ̀ka_àkóónú++)
            if (입력[wá_atọ̀ka_àkóónú] != Orúkọ.charAt(wá_atọ̀ka_àkóónú)) return false;
        return gígùn_iye == Orúkọ.length() || 입력[Orúkọ.length()] == ' ';
    }

    static void ṣàfihàn_ìrànwọ́() {
        문자단말.Kọ("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        문자단말.Kọ("apps | run NAME [ARGS] | net\n");
        문자단말.Kọ("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        문자단말.Kọ("sync (연결된 JKSTORE1 Store_iye 장치에 Fáìlì 보존)\n");
    }

    static void Ìlànà_iye_ìgbéwọlé() {
        if (gígùn_iye == 0) return;
        if (Àṣẹ("help")) ṣàfihàn_ìrànwọ́();
        else if (Àṣẹ("sync")) {
            int 결과 = 파일보존.múdọ́gba();
            문자단말.Kọ("Sync: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Àṣẹ("ls")) ibi_ìpamọ́_ìlànà_ètò_fáìlì.ìgbéwọlé_Àtòkọ();
        else if (Àṣẹ("edit")) ibi_ìpamọ́_ìlànà_ètò_fáìlì.Àṣẹ(입력, 4, gígùn_iye, 0);
        else if (Àṣẹ("cat")) ibi_ìpamọ́_ìlànà_ètò_fáìlì.Àṣẹ(입력, 3, gígùn_iye, 1);
        else if (Àṣẹ("rm")) ibi_ìpamọ́_ìlànà_ètò_fáìlì.Àṣẹ(입력, 2, gígùn_iye, 2);
        else if (Àṣẹ("java") || Àṣẹ("javac")) {
            int 결과 = 실행관리.ṣiṣẹ́_àṣẹ(입력, 0, gígùn_iye);
            문자단말.Kọ("Exit: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Àṣẹ("apps")) 실행관리.ìgbéwọlé_Àtòkọ();
        else if (Àṣẹ("net")) Alásopọ̀_kójọ.ipò_iye();
        else if (Àṣẹ("run")) {
            int 결과 = 실행관리.ṣiṣẹ́_àṣẹ(입력, 3, gígùn_iye);
            문자단말.Kọ("Exit: "); 문자단말.수쓰기(결과); 문자단말.Kọ("\n");
        } else if (Àṣẹ("info")) {
            문자단말.Kọ("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Àṣẹ("mem")) {
            문자단말.Kọ("위쪽 ibi_ìpamọ́_iye 공간(KiB): "); 문자단말.수쓰기(기억공간.위쪽기억크기());
            문자단말.Kọ("\n배열 동적 ibi_ìpamọ́_iye 공간(báìtì_iye): "); 문자단말.수쓰기(ohun_èlò_iye.ÀRÉÈ_ìlò());
            문자단말.Kọ(" / 262144\n작업 공간 abala_iye: "); 문자단말.수쓰기(기억공간.사용개수());
            문자단말.Kọ(" / 8 (각 4096바이트)\n");
        } else if (Àṣẹ("alloc")) {
            int wá_atọ̀ka_àkóónú = 기억공간.pín_Ibi_ìpamọ́();
            문자단말.Kọ("abala_iye wá_atọ̀ka_àkóónú: "); 문자단말.수쓰기(wá_atọ̀ka_àkóónú); 문자단말.Kọ("\n");
        } else if (Àṣẹ("free")) {
            if (gígùn_iye == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                문자단말.Kọ(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 abala_iye\n");
            } else 문자단말.Kọ("사용법: free 0..7\n");
        } else if (Àṣẹ("echo")) {
            for (int wá_atọ̀ka_àkóónú = 5; wá_atọ̀ka_àkóónú < gígùn_iye; wá_atọ̀ka_àkóónú++) 문자단말.문자(입력[wá_atọ̀ka_àkóónú]);
            문자단말.문자(10);
        } else if (Àṣẹ("clear")) 문자단말.지우기();
        else if (Àṣẹ("test")) kánẹ́ẹ̀lì.시험();
        else if (Àṣẹ("halt")) {
            문자단말.Kọ("HALTED\n");
            ohun_èlò_iye.정지();
        } else 문자단말.Kọ("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int iye) {
        if (iye == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = iye == 13;
        if (iye == 10 || iye == 13) {
            문자단말.문자(10);
            if (ibi_ìpamọ́_ìlànà_ètò_fáìlì.편집중) ibi_ìpamọ́_ìlànà_ètò_fáìlì.편집줄(입력, gígùn_iye, ìlà_rékọjá);
            else Ìlànà_iye_ìgbéwọlé();
            gígùn_iye = 0;
            ìlà_rékọjá = false;
            문자단말.Kọ(ibi_ìpamọ́_ìlànà_ètò_fáìlì.편집중 ? "...> " : "jkoros> ");
        } else if (iye == 8 || iye == 127) {
            if (gígùn_iye > 0) {
                gígùn_iye--;
                문자단말.직렬바이트(8); 문자단말.직렬바이트(32); 문자단말.직렬바이트(8);
                문자단말.화면문자(8);
            }
        } else if (iye >= 32 && iye < 127 && gígùn_iye < 입력.length) {
            입력[gígùn_iye++] = iye;
            문자단말.문자(iye);
        } else if (iye >= 32 && iye < 127) ìlà_rékọjá = true;
    }

    static void Rọ́ọ̀nù() {
        ṣàfihàn_ìrànwọ́();
        문자단말.Kọ("READY\njkoros> ");
        while (true) {
            int iye = 문자단말.직렬읽기();
            if (iye < 0) iye = àtẹ_ìtẹ̀wé.Kàá();
            if (iye >= 0) 받아쓰기(iye);
            else { Alásopọ̀_kójọ.ridájú(); ohun_èlò_iye.잠시양보(); }
        }
    }
}
