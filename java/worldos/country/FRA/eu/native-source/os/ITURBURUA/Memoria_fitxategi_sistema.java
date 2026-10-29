// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Fitxategia. 원본 edizio_balio/eraiki_iturburu hutsegite_balio 시 기존 파일을 보존한다. */
public final class Memoria_fitxategi_sistema {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] 크기들 = new int[8];
    static int[] ireki_ZENBATU = new int[8], 허가들 = new int[8];
    static int[] Izena = new int[64];
    static int[] edizio_balio = new int[최대크기];
    static boolean 편집중 = false;
    static boolean 넘침 = false;
    static int 편집크기 = 0;

    static boolean txeke_izen(int[] karaktere_balio, int luzera_balio) {
        if (luzera_balio < 1 || luzera_balio > 63) return false;
        for (int 수 = 0; 수 < luzera_balio; 수++) {
            int balio = karaktere_balio[수];
            if (!(balio >= 'a' && balio <= 'z') && !(balio >= 'A' && balio <= 'Z')
                && !(balio >= '0' && balio <= '9') && balio != '_' && balio != '-' && balio != '.') return false;
        }
        return karaktere_balio[0] != '.';
    }

    static int Bilatu_sarrera(int[] karaktere_balio, int luzera_balio) {
        if (!txeke_izen(karaktere_balio, luzera_balio)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + luzera_balio] == 0;
            for (int 칸 = 0; 칸 < luzera_balio; 칸++) if (이름들[수 * 64 + 칸] != karaktere_balio[칸]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_balio(int[] karaktere_balio, int luzera_balio, int[] datuak, int Tamaina) {
        if (!txeke_izen(karaktere_balio, luzera_balio) || Tamaina < 0 || Tamaina > datuak.length) return -22;
        if (Tamaina > 최대크기) return -90;
        int INDIZE = Bilatu_sarrera(karaktere_balio, luzera_balio);
        if (INDIZE == -2) {
            for (int 수 = 0; 수 < 8 && INDIZE < 0; 수++) if (이름들[수 * 64] == 0 && ireki_ZENBATU[수] == 0) INDIZE = 수;
            if (INDIZE >= 0) 허가들[INDIZE] = 438;
        }
        if (INDIZE < 0) return -28;
        int helbide = gailu_balio.fitxategi_Memoria() + INDIZE * 최대크기;
        for (int 수 = 0; 수 < Tamaina; 수++) gailu_balio.idatzi_Memoria(helbide + 수, datuak[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDIZE * 64 + 수] = 수 < luzera_balio ? karaktere_balio[수] : 0;
        크기들[INDIZE] = Tamaina;
        return Tamaina;
    }

    static void sarrera_Zerrenda() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[수 * 64 + 칸] != 0; 칸++) SMS_Terminal.문자(이름들[수 * 64 + 칸]);
            SMS_Terminal.Idatzi("  "); SMS_Terminal.수쓰기(크기들[수]); SMS_Terminal.Idatzi("byte_balio\n");
        }
        SMS_Terminal.Idatzi(biltegi_gailu_konexio.informatika_libre ? "Fitxategia 8칸, 파일당 16384바이트; sync로 Store_balio 장치에 보존\n"
            : "임시 Fitxategia 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Komandoa(int[] 입력, int Exekutatu_2, int luzera_balio, int Ekintza) {
        while (Exekutatu_2 < luzera_balio && 입력[Exekutatu_2] == ' ') Exekutatu_2++;
        int 끝 = luzera_balio;
        while (끝 > Exekutatu_2 && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Exekutatu_2;
        if (수 < 1 || 수 > 63) { SMS_Terminal.Idatzi("올바르지 않은 Fitxategia Izena\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) Izena[칸] = 칸 < 수 ? 입력[Exekutatu_2 + 칸] : 0;
        int INDIZE = Bilatu_sarrera(Izena, 수);
        if (INDIZE == -22) { SMS_Terminal.Idatzi("올바르지 않은 Fitxategia Izena\n"); return; }
        if (Ekintza == 0) {
            편집중 = true; 편집크기 = 0; 넘침 = false;
            SMS_Terminal.Idatzi("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDIZE < 0) SMS_Terminal.Idatzi("파일을 찾을 수 없습니다\n");
        else if (Ekintza == 1) {
            int helbide = gailu_balio.fitxategi_Memoria() + INDIZE * 최대크기;
            for (int 칸 = 0; 칸 < 크기들[INDIZE]; 칸++) SMS_Terminal.문자(gailu_balio.기억읽기(helbide + 칸));
            SMS_Terminal.문자(10);
        } else { 이름들[INDIZE * 64] = 0; 크기들[INDIZE] = 0; SMS_Terminal.Idatzi("파일을 지웠습니다\n"); }
    }

    static boolean informatika_BERDIN(int[] 입력, int luzera_balio, String 문구) {
        if (luzera_balio != 문구.length()) return false;
        for (int 칸 = 0; 칸 < luzera_balio; 칸++) if (입력[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void Editatutakoak_lerro(int[] 입력, int luzera_balio, boolean 줄넘침) {
        if (informatika_BERDIN(입력, luzera_balio, ".cancel")) {
            편집중 = false; SMS_Terminal.Idatzi("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (informatika_BERDIN(입력, luzera_balio, ".save")) {
            편집중 = false;
            if (넘침) { SMS_Terminal.Idatzi("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Izena[수] != 0) 수++;
            int EMAITZA = Store_balio(Izena, 수, edizio_balio, 편집크기);
            SMS_Terminal.Idatzi(EMAITZA >= 0 ? "보존한 byte_balio 수: " : "보존 hutsegite_balio: ");
            SMS_Terminal.수쓰기(EMAITZA); SMS_Terminal.문자(10);
        } else if (줄넘침 || luzera_balio + 1 > 최대크기 - 편집크기) 넘침 = true;
        else {
            for (int 수 = 0; 수 < luzera_balio; 수++) edizio_balio[편집크기++] = 입력[수];
            edizio_balio[편집크기++] = 10;
        }
    }

    static void 예제(String Fitxategia, String eduki_balio) {
        for (int 수 = 0; 수 < 64; 수++) Izena[수] = 수 < Fitxategia.length() ? Fitxategia.charAt(수) : 0;
        for (int 수 = 0; 수 < eduki_balio.length(); 수++) edizio_balio[수] = eduki_balio.charAt(수);
        Store_balio(Izena, Fitxategia.length(), edizio_balio, eduki_balio.length());
    }

    static void 준비() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int talde_balio = gailu_balio.자바파일묶음(), Tamaina = gailu_balio.자바파일묶음크기();
        if (Tamaina < 8 || 실행관리.수(talde_balio) != 0x464a4b4a) { SMS_Terminal.Idatzi("올바르지 않은 Java Fitxategia talde_balio\n"); return; }
        int elementu_ZENBATU = 실행관리.수(talde_balio + 4);
        if (elementu_ZENBATU < 0 || elementu_ZENBATU > 8 || elementu_ZENBATU > (Tamaina - 8) / 72) { SMS_Terminal.Idatzi("올바르지 않은 Java Fitxategia sarrera_Zerrenda\n"); return; }
        for (int 수 = 0; 수 < elementu_ZENBATU; 수++) {
            int sarrera_balio = talde_balio + 8 + 수 * 72, luzera_balio = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Izena[칸] = gailu_balio.기억읽기(sarrera_balio + 칸);
            while (luzera_balio < 64 && Izena[luzera_balio] != 0) luzera_balio++;
            int Posizioa = 실행관리.수(sarrera_balio + 64), 파일크기 = 실행관리.수(sarrera_balio + 68);
            if (!txeke_izen(Izena, luzera_balio) || 파일크기 < 0 || 파일크기 > 최대크기 || Posizioa < 8 + elementu_ZENBATU * 72 || Posizioa > Tamaina - 파일크기) {
                SMS_Terminal.Idatzi("올바르지 않은 Java Fitxategia sarrera_balio\n"); return;
            }
            for (int 칸 = 0; 칸 < 파일크기; 칸++) edizio_balio[칸] = gailu_balio.기억읽기(talde_balio + Posizioa + 칸);
            if (Store_balio(Izena, luzera_balio, edizio_balio, 파일크기) < 0) { SMS_Terminal.Idatzi("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
