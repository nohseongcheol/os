// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Comhad. 원본 cuir_in_eagar_VALUE/tóg_foinse teip_VALUE 시 기존 파일을 보존한다. */
public final class Cuimhne_córas_comhad {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] socraigh_méid_Liosta = new int[8];
    static int[] oscail_COUNT = new int[8], 허가들 = new int[8];
    static int[] Ainm = new int[64];
    static int[] cuir_in_eagar_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean róshreabhadh_VALUE = false;
    static int cuir_in_eagar_socraigh_méid = 0;

    static boolean seic_ainm(int[] carachtar_VALUE, int fad_VALUE) {
        if (fad_VALUE < 1 || fad_VALUE > 63) return false;
        for (int 수 = 0; 수 < fad_VALUE; 수++) {
            int VALUE = carachtar_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return carachtar_VALUE[0] != '.';
    }

    static int FIND_iontráil(int[] carachtar_VALUE, int fad_VALUE) {
        if (!seic_ainm(carachtar_VALUE, fad_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + fad_VALUE] == 0;
            for (int spás_iontráil = 0; spás_iontráil < fad_VALUE; spás_iontráil++) if (이름들[수 * 64 + spás_iontráil] != carachtar_VALUE[spás_iontráil]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] carachtar_VALUE, int fad_VALUE, int[] sonraí, int Méid) {
        if (!seic_ainm(carachtar_VALUE, fad_VALUE) || Méid < 0 || Méid > sonraí.length) return -22;
        if (Méid > 최대크기) return -90;
        int INDEX = FIND_iontráil(carachtar_VALUE, fad_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && oscail_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int ADDRESS = gléas_VALUE.comhad_Cuimhne() + INDEX * 최대크기;
        for (int 수 = 0; 수 < Méid; 수++) gléas_VALUE.scríobh_Cuimhne(ADDRESS + 수, sonraí[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < fad_VALUE ? carachtar_VALUE[수] : 0;
        socraigh_méid_Liosta[INDEX] = Méid;
        return Méid;
    }

    static void iontráil_Liosta() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int spás_iontráil = 0; spás_iontráil < 64 && 이름들[수 * 64 + spás_iontráil] != 0; spás_iontráil++) SMS_Teirminéal.문자(이름들[수 * 64 + spás_iontráil]);
            SMS_Teirminéal.Scríobh("  "); SMS_Teirminéal.수쓰기(socraigh_méid_Liosta[수]); SMS_Teirminéal.Scríobh("beart_VALUE\n");
        }
        SMS_Teirminéal.Scríobh(Stóras_gléas_nasc.teicneolaíocht_faisnéise_ar_fáil ? "Comhad 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Comhad 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Ordú(int[] 입력, int Rith_2, int fad_VALUE, int Gníomh) {
        while (Rith_2 < fad_VALUE && 입력[Rith_2] == ' ') Rith_2++;
        int 끝 = fad_VALUE;
        while (끝 > Rith_2 && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Rith_2;
        if (수 < 1 || 수 > 63) { SMS_Teirminéal.Scríobh("올바르지 않은 Comhad Ainm\n"); return; }
        for (int spás_iontráil = 0; spás_iontráil < 64; spás_iontráil++) Ainm[spás_iontráil] = spás_iontráil < 수 ? 입력[Rith_2 + spás_iontráil] : 0;
        int INDEX = FIND_iontráil(Ainm, 수);
        if (INDEX == -22) { SMS_Teirminéal.Scríobh("올바르지 않은 Comhad Ainm\n"); return; }
        if (Gníomh == 0) {
            편집중 = true; cuir_in_eagar_socraigh_méid = 0; róshreabhadh_VALUE = false;
            SMS_Teirminéal.Scríobh("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Teirminéal.Scríobh("파일을 찾을 수 없습니다\n");
        else if (Gníomh == 1) {
            int ADDRESS = gléas_VALUE.comhad_Cuimhne() + INDEX * 최대크기;
            for (int spás_iontráil = 0; spás_iontráil < socraigh_méid_Liosta[INDEX]; spás_iontráil++) SMS_Teirminéal.문자(gléas_VALUE.기억읽기(ADDRESS + spás_iontráil));
            SMS_Teirminéal.문자(10);
        } else { 이름들[INDEX * 64] = 0; socraigh_méid_Liosta[INDEX] = 0; SMS_Teirminéal.Scríobh("파일을 지웠습니다\n"); }
    }

    static boolean teicneolaíocht_faisnéise_EXACT(int[] 입력, int fad_VALUE, String 문구) {
        if (fad_VALUE != 문구.length()) return false;
        for (int spás_iontráil = 0; spás_iontráil < fad_VALUE; spás_iontráil++) if (입력[spás_iontráil] != 문구.charAt(spás_iontráil)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int fad_VALUE, boolean líne_róshreabhadh) {
        if (teicneolaíocht_faisnéise_EXACT(입력, fad_VALUE, ".cancel")) {
            편집중 = false; SMS_Teirminéal.Scríobh("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (teicneolaíocht_faisnéise_EXACT(입력, fad_VALUE, ".save")) {
            편집중 = false;
            if (róshreabhadh_VALUE) { SMS_Teirminéal.Scríobh("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Ainm[수] != 0) 수++;
            int tomhas = Store_VALUE(Ainm, 수, cuir_in_eagar_VALUE, cuir_in_eagar_socraigh_méid);
            SMS_Teirminéal.Scríobh(tomhas >= 0 ? "보존한 beart_VALUE 수: " : "보존 teip_VALUE: ");
            SMS_Teirminéal.수쓰기(tomhas); SMS_Teirminéal.문자(10);
        } else if (líne_róshreabhadh || fad_VALUE + 1 > 최대크기 - cuir_in_eagar_socraigh_méid) róshreabhadh_VALUE = true;
        else {
            for (int 수 = 0; 수 < fad_VALUE; 수++) cuir_in_eagar_VALUE[cuir_in_eagar_socraigh_méid++] = 입력[수];
            cuir_in_eagar_VALUE[cuir_in_eagar_socraigh_méid++] = 10;
        }
    }

    static void 예제(String Comhad, String Inneachar_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Ainm[수] = 수 < Comhad.length() ? Comhad.charAt(수) : 0;
        for (int 수 = 0; 수 < Inneachar_VALUE.length(); 수++) cuir_in_eagar_VALUE[수] = Inneachar_VALUE.charAt(수);
        Store_VALUE(Ainm, Comhad.length(), cuir_in_eagar_VALUE, Inneachar_VALUE.length());
    }

    static void Ullmhaigh() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Grúpa_VALUE = gléas_VALUE.자바파일묶음(), Méid = gléas_VALUE.자바파일묶음크기();
        if (Méid < 8 || 실행관리.수(Grúpa_VALUE) != 0x464a4b4a) { SMS_Teirminéal.Scríobh("올바르지 않은 Java Comhad Grúpa_VALUE\n"); return; }
        int mír_COUNT = 실행관리.수(Grúpa_VALUE + 4);
        if (mír_COUNT < 0 || mír_COUNT > 8 || mír_COUNT > (Méid - 8) / 72) { SMS_Teirminéal.Scríobh("올바르지 않은 Java Comhad iontráil_Liosta\n"); return; }
        for (int 수 = 0; 수 < mír_COUNT; 수++) {
            int iontráil_VALUE = Grúpa_VALUE + 8 + 수 * 72, fad_VALUE = 0;
            for (int spás_iontráil = 0; spás_iontráil < 64; spás_iontráil++) Ainm[spás_iontráil] = gléas_VALUE.기억읽기(iontráil_VALUE + spás_iontráil);
            while (fad_VALUE < 64 && Ainm[fad_VALUE] != 0) fad_VALUE++;
            int suíomh = 실행관리.수(iontráil_VALUE + 64), comhad_socraigh_méid = 실행관리.수(iontráil_VALUE + 68);
            if (!seic_ainm(Ainm, fad_VALUE) || comhad_socraigh_méid < 0 || comhad_socraigh_méid > 최대크기 || suíomh < 8 + mír_COUNT * 72 || suíomh > Méid - comhad_socraigh_méid) {
                SMS_Teirminéal.Scríobh("올바르지 않은 Java Comhad iontráil_VALUE\n"); return;
            }
            for (int spás_iontráil = 0; spás_iontráil < comhad_socraigh_méid; spás_iontráil++) cuir_in_eagar_VALUE[spás_iontráil] = gléas_VALUE.기억읽기(Grúpa_VALUE + suíomh + spás_iontráil);
            if (Store_VALUE(Ainm, fad_VALUE, cuir_in_eagar_VALUE, comhad_socraigh_méid) < 0) { SMS_Teirminéal.Scríobh("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
