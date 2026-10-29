// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Faịlụ. 원본 dezìmà_valuu/wue_ebensìbịa ọdịdà_valuu 시 기존 파일을 보존한다. */
public final class memọrị_sistèm_ọbọakwụkwo {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] ụha_ndepụta = new int[8];
    static int[] 열림수 = new int[8], 허가들 = new int[8];
    static int[] Aha = new int[64];
    static int[] dezìmà_valuu = new int[최대크기];
    static boolean 편집중 = false;
    static boolean njubigaoke_valuu = false;
    static int dezìmà_ụha = 0;

    static boolean cheèk_akara_ahà(int[] mkpụrụedemede_valuu, int ogologo_valuu) {
        if (ogologo_valuu < 1 || ogologo_valuu > 63) return false;
        for (int 수 = 0; 수 < ogologo_valuu; 수++) {
            int valuu = mkpụrụedemede_valuu[수];
            if (!(valuu >= 'a' && valuu <= 'z') && !(valuu >= 'A' && valuu <= 'Z')
                && !(valuu >= '0' && valuu <= '9') && valuu != '_' && valuu != '-' && valuu != '.') return false;
        }
        return mkpụrụedemede_valuu[0] != '.';
    }

    static int chọta_ndebà(int[] mkpụrụedemede_valuu, int ogologo_valuu) {
        if (!cheèk_akara_ahà(mkpụrụedemede_valuu, ogologo_valuu)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + ogologo_valuu] == 0;
            for (int oghere_ndebà = 0; oghere_ndebà < ogologo_valuu; oghere_ndebà++) if (이름들[수 * 64 + oghere_ndebà] != mkpụrụedemede_valuu[oghere_ndebà]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_valuu(int[] mkpụrụedemede_valuu, int ogologo_valuu, int[] datà, int Ụhara) {
        if (!cheèk_akara_ahà(mkpụrụedemede_valuu, ogologo_valuu) || Ụhara < 0 || Ụhara > datà.length) return -22;
        if (Ụhara > 최대크기) return -90;
        int indèks = chọta_ndebà(mkpụrụedemede_valuu, ogologo_valuu);
        if (indèks == -2) {
            for (int 수 = 0; 수 < 8 && indèks < 0; 수++) if (이름들[수 * 64] == 0 && 열림수[수] == 0) indèks = 수;
            if (indèks >= 0) 허가들[indèks] = 438;
        }
        if (indèks < 0) return -28;
        int àdreèsì = njìarụ_valuu.ọbọakwụkwọ_memọrị() + indèks * 최대크기;
        for (int 수 = 0; 수 < Ụhara; 수++) njìarụ_valuu.dee_memọrị(àdreèsì + 수, datà[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[indèks * 64 + 수] = 수 < ogologo_valuu ? mkpụrụedemede_valuu[수] : 0;
        ụha_ndepụta[indèks] = Ụhara;
        return Ụhara;
    }

    static void ndebà_ndepụta() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int oghere_ndebà = 0; oghere_ndebà < 64 && 이름들[수 * 64 + oghere_ndebà] != 0; oghere_ndebà++) 문자단말.문자(이름들[수 * 64 + oghere_ndebà]);
            문자단말.Chekwaa_ozi("  "); 문자단말.수쓰기(ụha_ndepụta[수]); 문자단말.Chekwaa_ozi("baịtị_valuu\n");
        }
        문자단말.Chekwaa_ozi(Nchekwa_njìarụ_njikọ.사용가능 ? "Faịlụ 8칸, 파일당 16384바이트; sync로 Store_valuu 장치에 보존\n"
            : "임시 Faịlụ 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Ntiiwu(int[] 입력, int Bido, int ogologo_valuu, int mmèm) {
        while (Bido < ogologo_valuu && 입력[Bido] == ' ') Bido++;
        int 끝 = ogologo_valuu;
        while (끝 > Bido && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Bido;
        if (수 < 1 || 수 > 63) { 문자단말.Chekwaa_ozi("올바르지 않은 Faịlụ Aha\n"); return; }
        for (int oghere_ndebà = 0; oghere_ndebà < 64; oghere_ndebà++) Aha[oghere_ndebà] = oghere_ndebà < 수 ? 입력[Bido + oghere_ndebà] : 0;
        int indèks = chọta_ndebà(Aha, 수);
        if (indèks == -22) { 문자단말.Chekwaa_ozi("올바르지 않은 Faịlụ Aha\n"); return; }
        if (mmèm == 0) {
            편집중 = true; dezìmà_ụha = 0; njubigaoke_valuu = false;
            문자단말.Chekwaa_ozi("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (indèks < 0) 문자단말.Chekwaa_ozi("파일을 찾을 수 없습니다\n");
        else if (mmèm == 1) {
            int àdreèsì = njìarụ_valuu.ọbọakwụkwọ_memọrị() + indèks * 최대크기;
            for (int oghere_ndebà = 0; oghere_ndebà < ụha_ndepụta[indèks]; oghere_ndebà++) 문자단말.문자(njìarụ_valuu.기억읽기(àdreèsì + oghere_ndebà));
            문자단말.문자(10);
        } else { 이름들[indèks * 64] = 0; ụha_ndepụta[indèks] = 0; 문자단말.Chekwaa_ozi("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int ogologo_valuu, String 문구) {
        if (ogologo_valuu != 문구.length()) return false;
        for (int oghere_ndebà = 0; oghere_ndebà < ogologo_valuu; oghere_ndebà++) if (입력[oghere_ndebà] != 문구.charAt(oghere_ndebà)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int ogologo_valuu, boolean ahịrī_njubigaoke) {
        if (정확(입력, ogologo_valuu, ".cancel")) {
            편집중 = false; 문자단말.Chekwaa_ozi("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, ogologo_valuu, ".save")) {
            편집중 = false;
            if (njubigaoke_valuu) { 문자단말.Chekwaa_ozi("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Aha[수] != 0) 수++;
            int 결과 = Store_valuu(Aha, 수, dezìmà_valuu, dezìmà_ụha);
            문자단말.Chekwaa_ozi(결과 >= 0 ? "보존한 baịtị_valuu 수: " : "보존 ọdịdà_valuu: ");
            문자단말.수쓰기(결과); 문자단말.문자(10);
        } else if (ahịrī_njubigaoke || ogologo_valuu + 1 > 최대크기 - dezìmà_ụha) njubigaoke_valuu = true;
        else {
            for (int 수 = 0; 수 < ogologo_valuu; 수++) dezìmà_valuu[dezìmà_ụha++] = 입력[수];
            dezìmà_valuu[dezìmà_ụha++] = 10;
        }
    }

    static void 예제(String Faịlụ, String ndịnà_valuu) {
        for (int 수 = 0; 수 < 64; 수++) Aha[수] = 수 < Faịlụ.length() ? Faịlụ.charAt(수) : 0;
        for (int 수 = 0; 수 < ndịnà_valuu.length(); 수++) dezìmà_valuu[수] = ndịnà_valuu.charAt(수);
        Store_valuu(Aha, Faịlụ.length(), dezìmà_valuu, ndịnà_valuu.length());
    }

    static void Kwado() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int otu_valuu = njìarụ_valuu.자바파일묶음(), Ụhara = njìarụ_valuu.자바파일묶음크기();
        if (Ụhara < 8 || 실행관리.수(otu_valuu) != 0x464a4b4a) { 문자단말.Chekwaa_ozi("올바르지 않은 Java Faịlụ otu_valuu\n"); return; }
        int 개수 = 실행관리.수(otu_valuu + 4);
        if (개수 < 0 || 개수 > 8 || 개수 > (Ụhara - 8) / 72) { 문자단말.Chekwaa_ozi("올바르지 않은 Java Faịlụ ndebà_ndepụta\n"); return; }
        for (int 수 = 0; 수 < 개수; 수++) {
            int ndebà_valuu = otu_valuu + 8 + 수 * 72, ogologo_valuu = 0;
            for (int oghere_ndebà = 0; oghere_ndebà < 64; oghere_ndebà++) Aha[oghere_ndebà] = njìarụ_valuu.기억읽기(ndebà_valuu + oghere_ndebà);
            while (ogologo_valuu < 64 && Aha[ogologo_valuu] != 0) ogologo_valuu++;
            int 위치 = 실행관리.수(ndebà_valuu + 64), ọbọakwụkwọ_ụha = 실행관리.수(ndebà_valuu + 68);
            if (!cheèk_akara_ahà(Aha, ogologo_valuu) || ọbọakwụkwọ_ụha < 0 || ọbọakwụkwọ_ụha > 최대크기 || 위치 < 8 + 개수 * 72 || 위치 > Ụhara - ọbọakwụkwọ_ụha) {
                문자단말.Chekwaa_ozi("올바르지 않은 Java Faịlụ ndebà_valuu\n"); return;
            }
            for (int oghere_ndebà = 0; oghere_ndebà < ọbọakwụkwọ_ụha; oghere_ndebà++) dezìmà_valuu[oghere_ndebà] = njìarụ_valuu.기억읽기(otu_valuu + 위치 + oghere_ndebà);
            if (Store_valuu(Aha, ogologo_valuu, dezìmà_valuu, ọbọakwụkwọ_ụha) < 0) { 문자단말.Chekwaa_ozi("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
