// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Idosiye. 원본 guhindura_agaciro/gusohora_inkomoko kudakora_agaciro 시 기존 파일을 보존한다. */
public final class ububiko_sisitemu_ya_dosiye {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] ingano_Urutonde = new int[8];
    static int[] 열림수 = new int[8], 허가들 = new int[8];
    static int[] Izina = new int[64];
    static int[] guhindura_agaciro = new int[최대크기];
    static boolean 편집중 = false;
    static boolean umusago_agaciro = false;
    static int guhindura_ingano = 0;

    static boolean sheki_izina(int[] inyuguti_agaciro, int uburebure_agaciro) {
        if (uburebure_agaciro < 1 || uburebure_agaciro > 63) return false;
        for (int 수 = 0; 수 < uburebure_agaciro; 수++) {
            int agaciro = inyuguti_agaciro[수];
            if (!(agaciro >= 'a' && agaciro <= 'z') && !(agaciro >= 'A' && agaciro <= 'Z')
                && !(agaciro >= '0' && agaciro <= '9') && agaciro != '_' && agaciro != '-' && agaciro != '.') return false;
        }
        return inyuguti_agaciro[0] != '.';
    }

    static int gushaka_icyinjizwa(int[] inyuguti_agaciro, int uburebure_agaciro) {
        if (!sheki_izina(inyuguti_agaciro, uburebure_agaciro)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + uburebure_agaciro] == 0;
            for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < uburebure_agaciro; umwanya_icyinjizwa++) if (이름들[수 * 64 + umwanya_icyinjizwa] != inyuguti_agaciro[umwanya_icyinjizwa]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_agaciro(int[] inyuguti_agaciro, int uburebure_agaciro, int[] amakurushingiro, int Ingano) {
        if (!sheki_izina(inyuguti_agaciro, uburebure_agaciro) || Ingano < 0 || Ingano > amakurushingiro.length) return -22;
        if (Ingano > 최대크기) return -90;
        int umugerekashakiro = gushaka_icyinjizwa(inyuguti_agaciro, uburebure_agaciro);
        if (umugerekashakiro == -2) {
            for (int 수 = 0; 수 < 8 && umugerekashakiro < 0; 수++) if (이름들[수 * 64] == 0 && 열림수[수] == 0) umugerekashakiro = 수;
            if (umugerekashakiro >= 0) 허가들[umugerekashakiro] = 438;
        }
        if (umugerekashakiro < 0) return -28;
        int aderesi = igendanwa_agaciro.dosiye_ububiko() + umugerekashakiro * 최대크기;
        for (int 수 = 0; 수 < Ingano; 수++) igendanwa_agaciro.kwandika_ububiko(aderesi + 수, amakurushingiro[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[umugerekashakiro * 64 + 수] = 수 < uburebure_agaciro ? inyuguti_agaciro[수] : 0;
        ingano_Urutonde[umugerekashakiro] = Ingano;
        return Ingano;
    }

    static void icyinjizwa_Urutonde() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 64 && 이름들[수 * 64 + umwanya_icyinjizwa] != 0; umwanya_icyinjizwa++) 문자단말.문자(이름들[수 * 64 + umwanya_icyinjizwa]);
            문자단말.kwandika("  "); 문자단말.수쓰기(ingano_Urutonde[수]); 문자단말.kwandika("bayiti_agaciro\n");
        }
        문자단말.kwandika(Ububiko_igendanwa_kwihuza.사용가능 ? "Idosiye 8칸, 파일당 16384바이트; sync로 Store_agaciro 장치에 보존\n"
            : "임시 Idosiye 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Icyo_wifuza(int[] 입력, int ihuriro, int uburebure_agaciro, int Igikorwa) {
        while (ihuriro < uburebure_agaciro && 입력[ihuriro] == ' ') ihuriro++;
        int 끝 = uburebure_agaciro;
        while (끝 > ihuriro && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - ihuriro;
        if (수 < 1 || 수 > 63) { 문자단말.kwandika("올바르지 않은 Idosiye Izina\n"); return; }
        for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 64; umwanya_icyinjizwa++) Izina[umwanya_icyinjizwa] = umwanya_icyinjizwa < 수 ? 입력[ihuriro + umwanya_icyinjizwa] : 0;
        int umugerekashakiro = gushaka_icyinjizwa(Izina, 수);
        if (umugerekashakiro == -22) { 문자단말.kwandika("올바르지 않은 Idosiye Izina\n"); return; }
        if (Igikorwa == 0) {
            편집중 = true; guhindura_ingano = 0; umusago_agaciro = false;
            문자단말.kwandika("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (umugerekashakiro < 0) 문자단말.kwandika("파일을 찾을 수 없습니다\n");
        else if (Igikorwa == 1) {
            int aderesi = igendanwa_agaciro.dosiye_ububiko() + umugerekashakiro * 최대크기;
            for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < ingano_Urutonde[umugerekashakiro]; umwanya_icyinjizwa++) 문자단말.문자(igendanwa_agaciro.기억읽기(aderesi + umwanya_icyinjizwa));
            문자단말.문자(10);
        } else { 이름들[umugerekashakiro * 64] = 0; ingano_Urutonde[umugerekashakiro] = 0; 문자단말.kwandika("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int uburebure_agaciro, String 문구) {
        if (uburebure_agaciro != 문구.length()) return false;
        for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < uburebure_agaciro; umwanya_icyinjizwa++) if (입력[umwanya_icyinjizwa] != 문구.charAt(umwanya_icyinjizwa)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int uburebure_agaciro, boolean umurongo_umusago) {
        if (정확(입력, uburebure_agaciro, ".cancel")) {
            편집중 = false; 문자단말.kwandika("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, uburebure_agaciro, ".save")) {
            편집중 = false;
            if (umusago_agaciro) { 문자단말.kwandika("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Izina[수] != 0) 수++;
            int 결과 = Store_agaciro(Izina, 수, guhindura_agaciro, guhindura_ingano);
            문자단말.kwandika(결과 >= 0 ? "보존한 bayiti_agaciro 수: " : "보존 kudakora_agaciro: ");
            문자단말.수쓰기(결과); 문자단말.문자(10);
        } else if (umurongo_umusago || uburebure_agaciro + 1 > 최대크기 - guhindura_ingano) umusago_agaciro = true;
        else {
            for (int 수 = 0; 수 < uburebure_agaciro; 수++) guhindura_agaciro[guhindura_ingano++] = 입력[수];
            guhindura_agaciro[guhindura_ingano++] = 10;
        }
    }

    static void 예제(String Idosiye, String Ibirimo_agaciro) {
        for (int 수 = 0; 수 < 64; 수++) Izina[수] = 수 < Idosiye.length() ? Idosiye.charAt(수) : 0;
        for (int 수 = 0; 수 < Ibirimo_agaciro.length(); 수++) guhindura_agaciro[수] = Ibirimo_agaciro.charAt(수);
        Store_agaciro(Izina, Idosiye.length(), guhindura_agaciro, Ibirimo_agaciro.length());
    }

    static void Gutegura() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int itsinda_agaciro = igendanwa_agaciro.자바파일묶음(), Ingano = igendanwa_agaciro.자바파일묶음크기();
        if (Ingano < 8 || 실행관리.수(itsinda_agaciro) != 0x464a4b4a) { 문자단말.kwandika("올바르지 않은 Java Idosiye itsinda_agaciro\n"); return; }
        int 개수 = 실행관리.수(itsinda_agaciro + 4);
        if (개수 < 0 || 개수 > 8 || 개수 > (Ingano - 8) / 72) { 문자단말.kwandika("올바르지 않은 Java Idosiye icyinjizwa_Urutonde\n"); return; }
        for (int 수 = 0; 수 < 개수; 수++) {
            int icyinjizwa_agaciro = itsinda_agaciro + 8 + 수 * 72, uburebure_agaciro = 0;
            for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 64; umwanya_icyinjizwa++) Izina[umwanya_icyinjizwa] = igendanwa_agaciro.기억읽기(icyinjizwa_agaciro + umwanya_icyinjizwa);
            while (uburebure_agaciro < 64 && Izina[uburebure_agaciro] != 0) uburebure_agaciro++;
            int 위치 = 실행관리.수(icyinjizwa_agaciro + 64), dosiye_ingano = 실행관리.수(icyinjizwa_agaciro + 68);
            if (!sheki_izina(Izina, uburebure_agaciro) || dosiye_ingano < 0 || dosiye_ingano > 최대크기 || 위치 < 8 + 개수 * 72 || 위치 > Ingano - dosiye_ingano) {
                문자단말.kwandika("올바르지 않은 Java Idosiye icyinjizwa_agaciro\n"); return;
            }
            for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < dosiye_ingano; umwanya_icyinjizwa++) guhindura_agaciro[umwanya_icyinjizwa] = igendanwa_agaciro.기억읽기(itsinda_agaciro + 위치 + umwanya_icyinjizwa);
            if (Store_agaciro(Izina, uburebure_agaciro, guhindura_agaciro, dosiye_ingano) < 0) { 문자단말.kwandika("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
