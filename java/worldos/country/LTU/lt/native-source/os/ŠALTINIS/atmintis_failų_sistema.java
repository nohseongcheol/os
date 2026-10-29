// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Failas. 원본 redaguoti_VALUE/kompiliuoti_šaltinis triktis_VALUE 시 기존 파일을 보존한다. */
public final class atmintis_failų_sistema {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] dydis_Sąrašas = new int[8];
    static int[] kurti_COUNT = new int[8], 허가들 = new int[8];
    static int[] Pavadinimas_2 = new int[64];
    static int[] redaguoti_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean perpilda_VALUE = false;
    static int redaguoti_dydis = 0;

    static boolean čekis_pavadinimas(int[] simbolis_VALUE_068c2631, int 길이) {
        if (길이 < 1 || 길이 > 63) return false;
        for (int numeris = 0; numeris < 길이; numeris++) {
            int VALUE = simbolis_VALUE_068c2631[numeris];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return simbolis_VALUE_068c2631[0] != '.';
    }

    static int FIND_įrašas(int[] simbolis_VALUE_068c2631, int 길이) {
        if (!čekis_pavadinimas(simbolis_VALUE_068c2631, 길이)) return -22;
        for (int numeris = 0; numeris < 8; numeris++) {
            boolean 같음 = 이름들[numeris * 64 + 길이] == 0;
            for (int 칸 = 0; 칸 < 길이; 칸++) if (이름들[numeris * 64 + 칸] != simbolis_VALUE_068c2631[칸]) 같음 = false;
            if (같음) return numeris;
        }
        return -2;
    }

    static int Store_VALUE(int[] simbolis_VALUE_068c2631, int 길이, int[] duomenys, int Dydis) {
        if (!čekis_pavadinimas(simbolis_VALUE_068c2631, 길이) || Dydis < 0 || Dydis > duomenys.length) return -22;
        if (Dydis > 최대크기) return -90;
        int INDEX = FIND_įrašas(simbolis_VALUE_068c2631, 길이);
        if (INDEX == -2) {
            for (int numeris = 0; numeris < 8 && INDEX < 0; numeris++) if (이름들[numeris * 64] == 0 && kurti_COUNT[numeris] == 0) INDEX = numeris;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int ADDRESS = įrenginys_VALUE.Failas_atmintis() + INDEX * 최대크기;
        for (int numeris = 0; numeris < Dydis; numeris++) įrenginys_VALUE.rašymas_atmintis(ADDRESS + numeris, duomenys[numeris]);
        for (int numeris = 0; numeris < 64; numeris++) 이름들[INDEX * 64 + numeris] = numeris < 길이 ? simbolis_VALUE_068c2631[numeris] : 0;
        dydis_Sąrašas[INDEX] = Dydis;
        return Dydis;
    }

    static void įrašas_Sąrašas() {
        for (int numeris = 0; numeris < 8; numeris++) if (이름들[numeris * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[numeris * 64 + 칸] != 0; 칸++) SMS_Terminalas.문자(이름들[numeris * 64 + 칸]);
            SMS_Terminalas.Rašymas("  "); SMS_Terminalas.rašymas_numeris(dydis_Sąrašas[numeris]); SMS_Terminalas.Rašymas("baitas_VALUE\n");
        }
        SMS_Terminalas.Rašymas(saugojimo_įrenginys_ryšys.informacinės_technologijos_Aktyvus_9e72441a ? "Failas 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Failas 8칸, 파일당 16384바이트; kartoti_VALUE 시작하면 사라짐\n");
    }

    static void Komanda(int[] 입력, int Paleisti, int 길이, int Veiksmas) {
        while (Paleisti < 길이 && 입력[Paleisti] == ' ') Paleisti++;
        int 끝 = 길이;
        while (끝 > Paleisti && 입력[끝 - 1] == ' ') 끝--;
        int numeris = 끝 - Paleisti;
        if (numeris < 1 || numeris > 63) { SMS_Terminalas.Rašymas("올바르지 않은 Failas Pavadinimas_2\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) Pavadinimas_2[칸] = 칸 < numeris ? 입력[Paleisti + 칸] : 0;
        int INDEX = FIND_įrašas(Pavadinimas_2, numeris);
        if (INDEX == -22) { SMS_Terminalas.Rašymas("올바르지 않은 Failas Pavadinimas_2\n"); return; }
        if (Veiksmas == 0) {
            편집중 = true; redaguoti_dydis = 0; perpilda_VALUE = false;
            SMS_Terminalas.Rašymas("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminalas.Rašymas("파일을 찾을 numeris 없습니다\n");
        else if (Veiksmas == 1) {
            int ADDRESS = įrenginys_VALUE.Failas_atmintis() + INDEX * 최대크기;
            for (int 칸 = 0; 칸 < dydis_Sąrašas[INDEX]; 칸++) SMS_Terminalas.문자(įrenginys_VALUE.기억읽기(ADDRESS + 칸));
            SMS_Terminalas.문자(10);
        } else { 이름들[INDEX * 64] = 0; dydis_Sąrašas[INDEX] = 0; SMS_Terminalas.Rašymas("파일을 지웠습니다\n"); }
    }

    static boolean informacinės_technologijos_EXACT(int[] 입력, int 길이, String 문구) {
        if (길이 != 문구.length()) return false;
        for (int 칸 = 0; 칸 < 길이; 칸++) if (입력[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void Redaguotos_eilutė(int[] 입력, int 길이, boolean eilutė_perpilda) {
        if (informacinės_technologijos_EXACT(입력, 길이, ".cancel")) {
            편집중 = false; SMS_Terminalas.Rašymas("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (informacinės_technologijos_EXACT(입력, 길이, ".save")) {
            편집중 = false;
            if (perpilda_VALUE) { SMS_Terminalas.Rašymas("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int numeris = 0;
            while (numeris < 64 && Pavadinimas_2[numeris] != 0) numeris++;
            int REZULTATAS = Store_VALUE(Pavadinimas_2, numeris, redaguoti_VALUE, redaguoti_dydis);
            SMS_Terminalas.Rašymas(REZULTATAS >= 0 ? "보존한 baitas_VALUE numeris: " : "보존 triktis_VALUE: ");
            SMS_Terminalas.rašymas_numeris(REZULTATAS); SMS_Terminalas.문자(10);
        } else if (eilutė_perpilda || 길이 + 1 > 최대크기 - redaguoti_dydis) perpilda_VALUE = true;
        else {
            for (int numeris = 0; numeris < 길이; numeris++) redaguoti_VALUE[redaguoti_dydis++] = 입력[numeris];
            redaguoti_VALUE[redaguoti_dydis++] = 10;
        }
    }

    static void 예제(String Failas, String Turinys_VALUE) {
        for (int numeris = 0; numeris < 64; numeris++) Pavadinimas_2[numeris] = numeris < Failas.length() ? Failas.charAt(numeris) : 0;
        for (int numeris = 0; numeris < Turinys_VALUE.length(); numeris++) redaguoti_VALUE[numeris] = Turinys_VALUE.charAt(numeris);
        Store_VALUE(Pavadinimas_2, Failas.length(), redaguoti_VALUE, Turinys_VALUE.length());
    }

    static void Parengti() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Grupė_VALUE = įrenginys_VALUE.자바파일묶음(), Dydis = įrenginys_VALUE.자바파일묶음크기();
        if (Dydis < 8 || 실행관리.numeris(Grupė_VALUE) != 0x464a4b4a) { SMS_Terminalas.Rašymas("올바르지 않은 Java Failas Grupė_VALUE\n"); return; }
        int prekė_COUNT = 실행관리.numeris(Grupė_VALUE + 4);
        if (prekė_COUNT < 0 || prekė_COUNT > 8 || prekė_COUNT > (Dydis - 8) / 72) { SMS_Terminalas.Rašymas("올바르지 않은 Java Failas įrašas_Sąrašas\n"); return; }
        for (int numeris = 0; numeris < prekė_COUNT; numeris++) {
            int įrašas_VALUE = Grupė_VALUE + 8 + numeris * 72, 길이 = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Pavadinimas_2[칸] = įrenginys_VALUE.기억읽기(įrašas_VALUE + 칸);
            while (길이 < 64 && Pavadinimas_2[길이] != 0) 길이++;
            int Pozicija = 실행관리.numeris(įrašas_VALUE + 64), failo_dydis = 실행관리.numeris(įrašas_VALUE + 68);
            if (!čekis_pavadinimas(Pavadinimas_2, 길이) || failo_dydis < 0 || failo_dydis > 최대크기 || Pozicija < 8 + prekė_COUNT * 72 || Pozicija > Dydis - failo_dydis) {
                SMS_Terminalas.Rašymas("올바르지 않은 Java Failas įrašas_VALUE\n"); return;
            }
            for (int 칸 = 0; 칸 < failo_dydis; 칸++) redaguoti_VALUE[칸] = įrenginys_VALUE.기억읽기(Grupė_VALUE + Pozicija + 칸);
            if (Store_VALUE(Pavadinimas_2, 길이, redaguoti_VALUE, failo_dydis) < 0) { SMS_Terminalas.Rašymas("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
