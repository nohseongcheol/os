// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Fail. 원본 muudatus_VALUE/kompileerima_lähe tõrge_VALUE 시 기존 파일을 보존한다. */
public final class Mälu_failisüsteem {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] suurust_muutma_Loend = new int[8];
    static int[] avama_COUNT = new int[8], 허가들 = new int[8];
    static int[] Nimi_2 = new int[64];
    static int[] muudatus_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean ületäide_VALUE = false;
    static int muudatus_suurust_muutma = 0;

    static boolean tšekk_nimetus(int[] märk_VALUE, int 길이) {
        if (길이 < 1 || 길이 > 63) return false;
        for (int number = 0; number < 길이; number++) {
            int VALUE = märk_VALUE[number];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return märk_VALUE[0] != '.';
    }

    static int FIND_kirje(int[] märk_VALUE, int 길이) {
        if (!tšekk_nimetus(märk_VALUE, 길이)) return -22;
        for (int number = 0; number < 8; number++) {
            boolean 같음 = 이름들[number * 64 + 길이] == 0;
            for (int 칸 = 0; 칸 < 길이; 칸++) if (이름들[number * 64 + 칸] != märk_VALUE[칸]) 같음 = false;
            if (같음) return number;
        }
        return -2;
    }

    static int salv_VALUE(int[] märk_VALUE, int 길이, int[] andmed, int Suurus) {
        if (!tšekk_nimetus(märk_VALUE, 길이) || Suurus < 0 || Suurus > andmed.length) return -22;
        if (Suurus > 최대크기) return -90;
        int INDEX = FIND_kirje(märk_VALUE, 길이);
        if (INDEX == -2) {
            for (int number = 0; number < 8 && INDEX < 0; number++) if (이름들[number * 64] == 0 && avama_COUNT[number] == 0) INDEX = number;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int ADDRESS = seade_VALUE.Fail_Mälu() + INDEX * 최대크기;
        for (int number = 0; number < Suurus; number++) seade_VALUE.kirjutamine_Mälu(ADDRESS + number, andmed[number]);
        for (int number = 0; number < 64; number++) 이름들[INDEX * 64 + number] = number < 길이 ? märk_VALUE[number] : 0;
        suurust_muutma_Loend[INDEX] = Suurus;
        return Suurus;
    }

    static void kirje_Loend() {
        for (int number = 0; number < 8; number++) if (이름들[number * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[number * 64 + 칸] != 0; 칸++) SMS_terminal.문자(이름들[number * 64 + 칸]);
            SMS_terminal.Kirjutamine("  "); SMS_terminal.kirjutamine_number(suurust_muutma_Loend[number]); SMS_terminal.Kirjutamine("bait_VALUE\n");
        }
        SMS_terminal.Kirjutamine(salvesti_ühendus.infotehnoloogia_Aktiivne_9e72441a ? "Fail 8칸, 파일당 16384바이트; sync로 salv_VALUE 장치에 보존\n"
            : "임시 Fail 8칸, 파일당 16384바이트; uuesti_proovima_VALUE 시작하면 사라짐\n");
    }

    static void Käsk(int[] 입력, int Käivita_2, int 길이, int Nimi) {
        while (Käivita_2 < 길이 && 입력[Käivita_2] == ' ') Käivita_2++;
        int 끝 = 길이;
        while (끝 > Käivita_2 && 입력[끝 - 1] == ' ') 끝--;
        int number = 끝 - Käivita_2;
        if (number < 1 || number > 63) { SMS_terminal.Kirjutamine("올바르지 않은 Fail Nimi_2\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) Nimi_2[칸] = 칸 < number ? 입력[Käivita_2 + 칸] : 0;
        int INDEX = FIND_kirje(Nimi_2, number);
        if (INDEX == -22) { SMS_terminal.Kirjutamine("올바르지 않은 Fail Nimi_2\n"); return; }
        if (Nimi == 0) {
            편집중 = true; muudatus_suurust_muutma = 0; ületäide_VALUE = false;
            SMS_terminal.Kirjutamine("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_terminal.Kirjutamine("파일을 찾을 number 없습니다\n");
        else if (Nimi == 1) {
            int ADDRESS = seade_VALUE.Fail_Mälu() + INDEX * 최대크기;
            for (int 칸 = 0; 칸 < suurust_muutma_Loend[INDEX]; 칸++) SMS_terminal.문자(seade_VALUE.기억읽기(ADDRESS + 칸));
            SMS_terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; suurust_muutma_Loend[INDEX] = 0; SMS_terminal.Kirjutamine("파일을 지웠습니다\n"); }
    }

    static boolean infotehnoloogia_EXACT(int[] 입력, int 길이, String 문구) {
        if (길이 != 문구.length()) return false;
        for (int 칸 = 0; 칸 < 길이; 칸++) if (입력[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void Redigeeritud_liin(int[] 입력, int 길이, boolean liin_ületäide) {
        if (infotehnoloogia_EXACT(입력, 길이, ".cancel")) {
            편집중 = false; SMS_terminal.Kirjutamine("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (infotehnoloogia_EXACT(입력, 길이, ".save")) {
            편집중 = false;
            if (ületäide_VALUE) { SMS_terminal.Kirjutamine("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int number = 0;
            while (number < 64 && Nimi_2[number] != 0) number++;
            int TULEMUS = salv_VALUE(Nimi_2, number, muudatus_VALUE, muudatus_suurust_muutma);
            SMS_terminal.Kirjutamine(TULEMUS >= 0 ? "보존한 bait_VALUE number: " : "보존 tõrge_VALUE: ");
            SMS_terminal.kirjutamine_number(TULEMUS); SMS_terminal.문자(10);
        } else if (liin_ületäide || 길이 + 1 > 최대크기 - muudatus_suurust_muutma) ületäide_VALUE = true;
        else {
            for (int number = 0; number < 길이; number++) muudatus_VALUE[muudatus_suurust_muutma++] = 입력[number];
            muudatus_VALUE[muudatus_suurust_muutma++] = 10;
        }
    }

    static void 예제(String Fail, String Sisu_VALUE) {
        for (int number = 0; number < 64; number++) Nimi_2[number] = number < Fail.length() ? Fail.charAt(number) : 0;
        for (int number = 0; number < Sisu_VALUE.length(); number++) muudatus_VALUE[number] = Sisu_VALUE.charAt(number);
        salv_VALUE(Nimi_2, Fail.length(), muudatus_VALUE, Sisu_VALUE.length());
    }

    static void Ettevalmistamine() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Rühm_VALUE = seade_VALUE.자바파일묶음(), Suurus = seade_VALUE.자바파일묶음크기();
        if (Suurus < 8 || 실행관리.number(Rühm_VALUE) != 0x464a4b4a) { SMS_terminal.Kirjutamine("올바르지 않은 Java Fail Rühm_VALUE\n"); return; }
        int kaup_COUNT = 실행관리.number(Rühm_VALUE + 4);
        if (kaup_COUNT < 0 || kaup_COUNT > 8 || kaup_COUNT > (Suurus - 8) / 72) { SMS_terminal.Kirjutamine("올바르지 않은 Java Fail kirje_Loend\n"); return; }
        for (int number = 0; number < kaup_COUNT; number++) {
            int kirje_VALUE = Rühm_VALUE + 8 + number * 72, 길이 = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Nimi_2[칸] = seade_VALUE.기억읽기(kirje_VALUE + 칸);
            while (길이 < 64 && Nimi_2[길이] != 0) 길이++;
            int Asukoht = 실행관리.number(kirje_VALUE + 64), faili_maht = 실행관리.number(kirje_VALUE + 68);
            if (!tšekk_nimetus(Nimi_2, 길이) || faili_maht < 0 || faili_maht > 최대크기 || Asukoht < 8 + kaup_COUNT * 72 || Asukoht > Suurus - faili_maht) {
                SMS_terminal.Kirjutamine("올바르지 않은 Java Fail kirje_VALUE\n"); return;
            }
            for (int 칸 = 0; 칸 < faili_maht; 칸++) muudatus_VALUE[칸] = seade_VALUE.기억읽기(Rühm_VALUE + Asukoht + 칸);
            if (salv_VALUE(Nimi_2, 길이, muudatus_VALUE, faili_maht) < 0) { SMS_terminal.Kirjutamine("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
