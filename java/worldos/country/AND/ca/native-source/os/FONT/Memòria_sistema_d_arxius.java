// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Fitxer. 원본 Editar_VALOR/generar_font error_VALOR 시 기존 파일을 보존한다. */
public final class Memòria_sistema_d_arxius {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] canviar_la_mida_Llista = new int[8];
    static int[] crear_COMPT = new int[8], 허가들 = new int[8];
    static int[] Nom = new int[64];
    static int[] Editar_VALOR = new int[최대크기];
    static boolean 편집중 = false;
    static boolean sobreeiximent_VALOR = false;
    static int Editar_canviar_la_mida = 0;

    static boolean xec_nom(int[] caràcter_VALOR, int durada_VALOR) {
        if (durada_VALOR < 1 || durada_VALOR > 63) return false;
        for (int 수 = 0; 수 < durada_VALOR; 수++) {
            int VALOR = caràcter_VALOR[수];
            if (!(VALOR >= 'a' && VALOR <= 'z') && !(VALOR >= 'A' && VALOR <= 'Z')
                && !(VALOR >= '0' && VALOR <= '9') && VALOR != '_' && VALOR != '-' && VALOR != '.') return false;
        }
        return caràcter_VALOR[0] != '.';
    }

    static int BUSCA_introducció(int[] caràcter_VALOR, int durada_VALOR) {
        if (!xec_nom(caràcter_VALOR, durada_VALOR)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + durada_VALOR] == 0;
            for (int 칸 = 0; 칸 < durada_VALOR; 칸++) if (이름들[수 * 64 + 칸] != caràcter_VALOR[칸]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALOR(int[] caràcter_VALOR, int durada_VALOR, int[] dades, int Mida) {
        if (!xec_nom(caràcter_VALOR, durada_VALOR) || Mida < 0 || Mida > dades.length) return -22;
        if (Mida > 최대크기) return -90;
        int INDEX = BUSCA_introducció(caràcter_VALOR, durada_VALOR);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && crear_COMPT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int Adreça = dispositiu_VALOR.arxiu_Memòria() + INDEX * 최대크기;
        for (int 수 = 0; 수 < Mida; 수++) dispositiu_VALOR.escriure_Memòria(Adreça + 수, dades[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < durada_VALOR ? caràcter_VALOR[수] : 0;
        canviar_la_mida_Llista[INDEX] = Mida;
        return Mida;
    }

    static void introducció_Llista() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[수 * 64 + 칸] != 0; 칸++) SMS_Terminal.문자(이름들[수 * 64 + 칸]);
            SMS_Terminal.Escriptura("  "); SMS_Terminal.수쓰기(canviar_la_mida_Llista[수]); SMS_Terminal.Escriptura("byte_VALOR\n");
        }
        SMS_Terminal.Escriptura(Emmagatzematge_dispositiu_connexió.tecnologies_de_la_informació_Actiu_9e72441a ? "Fitxer 8칸, 파일당 16384바이트; sync로 Store_VALOR 장치에 보존\n"
            : "임시 Fitxer 8칸, 파일당 16384바이트; tornar_ho_a_provar_VALOR 시작하면 사라짐\n");
    }

    static void Ordre(int[] 입력, int Executa_2, int durada_VALOR, int Acció) {
        while (Executa_2 < durada_VALOR && 입력[Executa_2] == ' ') Executa_2++;
        int 끝 = durada_VALOR;
        while (끝 > Executa_2 && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Executa_2;
        if (수 < 1 || 수 > 63) { SMS_Terminal.Escriptura("올바르지 않은 Fitxer Nom\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) Nom[칸] = 칸 < 수 ? 입력[Executa_2 + 칸] : 0;
        int INDEX = BUSCA_introducció(Nom, 수);
        if (INDEX == -22) { SMS_Terminal.Escriptura("올바르지 않은 Fitxer Nom\n"); return; }
        if (Acció == 0) {
            편집중 = true; Editar_canviar_la_mida = 0; sobreeiximent_VALOR = false;
            SMS_Terminal.Escriptura("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminal.Escriptura("파일을 찾을 수 없습니다\n");
        else if (Acció == 1) {
            int Adreça = dispositiu_VALOR.arxiu_Memòria() + INDEX * 최대크기;
            for (int 칸 = 0; 칸 < canviar_la_mida_Llista[INDEX]; 칸++) SMS_Terminal.문자(dispositiu_VALOR.tancar_Memòria(Adreça + 칸));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; canviar_la_mida_Llista[INDEX] = 0; SMS_Terminal.Escriptura("파일을 지웠습니다\n"); }
    }

    static boolean tecnologies_de_la_informació_IGUAL(int[] 입력, int durada_VALOR, String 문구) {
        if (durada_VALOR != 문구.length()) return false;
        for (int 칸 = 0; 칸 < durada_VALOR; 칸++) if (입력[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void Editats_línia(int[] 입력, int durada_VALOR, boolean línia_sobreeiximent) {
        if (tecnologies_de_la_informació_IGUAL(입력, durada_VALOR, ".cancel")) {
            편집중 = false; SMS_Terminal.Escriptura("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (tecnologies_de_la_informació_IGUAL(입력, durada_VALOR, ".save")) {
            편집중 = false;
            if (sobreeiximent_VALOR) { SMS_Terminal.Escriptura("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Nom[수] != 0) 수++;
            int RESULTAT = Store_VALOR(Nom, 수, Editar_VALOR, Editar_canviar_la_mida);
            SMS_Terminal.Escriptura(RESULTAT >= 0 ? "보존한 byte_VALOR 수: " : "보존 error_VALOR: ");
            SMS_Terminal.수쓰기(RESULTAT); SMS_Terminal.문자(10);
        } else if (línia_sobreeiximent || durada_VALOR + 1 > 최대크기 - Editar_canviar_la_mida) sobreeiximent_VALOR = true;
        else {
            for (int 수 = 0; 수 < durada_VALOR; 수++) Editar_VALOR[Editar_canviar_la_mida++] = 입력[수];
            Editar_VALOR[Editar_canviar_la_mida++] = 10;
        }
    }

    static void 예제(String Fitxer, String contingut_VALOR) {
        for (int 수 = 0; 수 < 64; 수++) Nom[수] = 수 < Fitxer.length() ? Fitxer.charAt(수) : 0;
        for (int 수 = 0; 수 < contingut_VALOR.length(); 수++) Editar_VALOR[수] = contingut_VALOR.charAt(수);
        Store_VALOR(Nom, Fitxer.length(), Editar_VALOR, contingut_VALOR.length());
    }

    static void Prepara() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Grup_VALOR = dispositiu_VALOR.자바파일묶음(), Mida = dispositiu_VALOR.자바파일묶음크기();
        if (Mida < 8 || 실행관리.수(Grup_VALOR) != 0x464a4b4a) { SMS_Terminal.Escriptura("올바르지 않은 Java Fitxer Grup_VALOR\n"); return; }
        int element_COMPT = 실행관리.수(Grup_VALOR + 4);
        if (element_COMPT < 0 || element_COMPT > 8 || element_COMPT > (Mida - 8) / 72) { SMS_Terminal.Escriptura("올바르지 않은 Java Fitxer introducció_Llista\n"); return; }
        for (int 수 = 0; 수 < element_COMPT; 수++) {
            int introducció_VALOR = Grup_VALOR + 8 + 수 * 72, durada_VALOR = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Nom[칸] = dispositiu_VALOR.tancar_Memòria(introducció_VALOR + 칸);
            while (durada_VALOR < 64 && Nom[durada_VALOR] != 0) durada_VALOR++;
            int Posició = 실행관리.수(introducció_VALOR + 64), arxiu_canviar_la_mida = 실행관리.수(introducció_VALOR + 68);
            if (!xec_nom(Nom, durada_VALOR) || arxiu_canviar_la_mida < 0 || arxiu_canviar_la_mida > 최대크기 || Posició < 8 + element_COMPT * 72 || Posició > Mida - arxiu_canviar_la_mida) {
                SMS_Terminal.Escriptura("올바르지 않은 Java Fitxer introducció_VALOR\n"); return;
            }
            for (int 칸 = 0; 칸 < arxiu_canviar_la_mida; 칸++) Editar_VALOR[칸] = dispositiu_VALOR.tancar_Memòria(Grup_VALOR + Posició + 칸);
            if (Store_VALOR(Nom, durada_VALOR, Editar_VALOR, arxiu_canviar_la_mida) < 0) { SMS_Terminal.Escriptura("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
