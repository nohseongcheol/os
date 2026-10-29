// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Fișier. 원본 edita_VALUE/compilare_sursă eroare_VALUE 시 기존 파일을 보존한다. */
public final class Memorie_sistem_de_fișiere {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] dimensiona_Listă = new int[8];
    static int[] crea_COUNT = new int[8], 허가들 = new int[8];
    static int[] Nume = new int[64];
    static int[] edita_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean depășire_VALUE = false;
    static int edita_dimensiona = 0;

    static boolean verifica_nume(int[] caracter_VALUE, int lungime_VALUE) {
        if (lungime_VALUE < 1 || lungime_VALUE > 63) return false;
        for (int 수 = 0; 수 < lungime_VALUE; 수++) {
            int VALUE = caracter_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return caracter_VALUE[0] != '.';
    }

    static int FIND_intrare(int[] caracter_VALUE, int lungime_VALUE) {
        if (!verifica_nume(caracter_VALUE, lungime_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + lungime_VALUE] == 0;
            for (int 칸 = 0; 칸 < lungime_VALUE; 칸++) if (이름들[수 * 64 + 칸] != caracter_VALUE[칸]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] caracter_VALUE, int lungime_VALUE, int[] date, int Mărime) {
        if (!verifica_nume(caracter_VALUE, lungime_VALUE) || Mărime < 0 || Mărime > date.length) return -22;
        if (Mărime > 최대크기) return -90;
        int INDEX = FIND_intrare(caracter_VALUE, lungime_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && crea_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int adresa = mobil_VALUE.Fișier_Memorie() + INDEX * 최대크기;
        for (int 수 = 0; 수 < Mărime; 수++) mobil_VALUE.scriere_Memorie(adresa + 수, date[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < lungime_VALUE ? caracter_VALUE[수] : 0;
        dimensiona_Listă[INDEX] = Mărime;
        return Mărime;
    }

    static void intrare_Listă() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[수 * 64 + 칸] != 0; 칸++) SMS_Terminal.문자(이름들[수 * 64 + 칸]);
            SMS_Terminal.Scriere("  "); SMS_Terminal.수쓰기(dimensiona_Listă[수]); SMS_Terminal.Scriere("byte_VALUE\n");
        }
        SMS_Terminal.Scriere(dispozitiv_de_stocare_conexiune.sisteme_de_informații_Activ_9e72441a ? "Fișier 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Fișier 8칸, 파일당 16384바이트; reîncerca_VALUE 시작하면 사라짐\n");
    }

    static void Comandă(int[] 입력, int Pornește, int lungime_VALUE, int Acțiuni) {
        while (Pornește < lungime_VALUE && 입력[Pornește] == ' ') Pornește++;
        int 끝 = lungime_VALUE;
        while (끝 > Pornește && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Pornește;
        if (수 < 1 || 수 > 63) { SMS_Terminal.Scriere("올바르지 않은 Fișier Nume\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) Nume[칸] = 칸 < 수 ? 입력[Pornește + 칸] : 0;
        int INDEX = FIND_intrare(Nume, 수);
        if (INDEX == -22) { SMS_Terminal.Scriere("올바르지 않은 Fișier Nume\n"); return; }
        if (Acțiuni == 0) {
            편집중 = true; edita_dimensiona = 0; depășire_VALUE = false;
            SMS_Terminal.Scriere("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminal.Scriere("파일을 찾을 수 없습니다\n");
        else if (Acțiuni == 1) {
            int adresa = mobil_VALUE.Fișier_Memorie() + INDEX * 최대크기;
            for (int 칸 = 0; 칸 < dimensiona_Listă[INDEX]; 칸++) SMS_Terminal.문자(mobil_VALUE.기억읽기(adresa + 칸));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; dimensiona_Listă[INDEX] = 0; SMS_Terminal.Scriere("파일을 지웠습니다\n"); }
    }

    static boolean sisteme_de_informații_EXACT(int[] 입력, int lungime_VALUE, String 문구) {
        if (lungime_VALUE != 문구.length()) return false;
        for (int 칸 = 0; 칸 < lungime_VALUE; 칸++) if (입력[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void Editate_linie(int[] 입력, int lungime_VALUE, boolean linie_depășire) {
        if (sisteme_de_informații_EXACT(입력, lungime_VALUE, ".cancel")) {
            편집중 = false; SMS_Terminal.Scriere("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (sisteme_de_informații_EXACT(입력, lungime_VALUE, ".save")) {
            편집중 = false;
            if (depășire_VALUE) { SMS_Terminal.Scriere("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Nume[수] != 0) 수++;
            int KR = Store_VALUE(Nume, 수, edita_VALUE, edita_dimensiona);
            SMS_Terminal.Scriere(KR >= 0 ? "보존한 byte_VALUE 수: " : "보존 eroare_VALUE: ");
            SMS_Terminal.수쓰기(KR); SMS_Terminal.문자(10);
        } else if (linie_depășire || lungime_VALUE + 1 > 최대크기 - edita_dimensiona) depășire_VALUE = true;
        else {
            for (int 수 = 0; 수 < lungime_VALUE; 수++) edita_VALUE[edita_dimensiona++] = 입력[수];
            edita_VALUE[edita_dimensiona++] = 10;
        }
    }

    static void 예제(String Fișier, String Conținut_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Nume[수] = 수 < Fișier.length() ? Fișier.charAt(수) : 0;
        for (int 수 = 0; 수 < Conținut_VALUE.length(); 수++) edita_VALUE[수] = Conținut_VALUE.charAt(수);
        Store_VALUE(Nume, Fișier.length(), edita_VALUE, Conținut_VALUE.length());
    }

    static void Pregătiți() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int grup_VALUE = mobil_VALUE.자바파일묶음(), Mărime = mobil_VALUE.자바파일묶음크기();
        if (Mărime < 8 || 실행관리.수(grup_VALUE) != 0x464a4b4a) { SMS_Terminal.Scriere("올바르지 않은 Java Fișier grup_VALUE\n"); return; }
        int element_COUNT = 실행관리.수(grup_VALUE + 4);
        if (element_COUNT < 0 || element_COUNT > 8 || element_COUNT > (Mărime - 8) / 72) { SMS_Terminal.Scriere("올바르지 않은 Java Fișier intrare_Listă\n"); return; }
        for (int 수 = 0; 수 < element_COUNT; 수++) {
            int intrare_VALUE = grup_VALUE + 8 + 수 * 72, lungime_VALUE = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Nume[칸] = mobil_VALUE.기억읽기(intrare_VALUE + 칸);
            while (lungime_VALUE < 64 && Nume[lungime_VALUE] != 0) lungime_VALUE++;
            int Poziție = 실행관리.수(intrare_VALUE + 64), dimensiune_fișier = 실행관리.수(intrare_VALUE + 68);
            if (!verifica_nume(Nume, lungime_VALUE) || dimensiune_fișier < 0 || dimensiune_fișier > 최대크기 || Poziție < 8 + element_COUNT * 72 || Poziție > Mărime - dimensiune_fișier) {
                SMS_Terminal.Scriere("올바르지 않은 Java Fișier intrare_VALUE\n"); return;
            }
            for (int 칸 = 0; 칸 < dimensiune_fișier; 칸++) edita_VALUE[칸] = mobil_VALUE.기억읽기(grup_VALUE + Poziție + 칸);
            if (Store_VALUE(Nume, lungime_VALUE, edita_VALUE, dimensiune_fișier) < 0) { SMS_Terminal.Scriere("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
