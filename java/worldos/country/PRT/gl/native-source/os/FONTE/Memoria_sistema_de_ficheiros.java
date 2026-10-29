// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Ficheiro. 원본 editar_VALOR/compilar_fonte erro_VALOR 시 기존 파일을 보존한다. */
public final class Memoria_sistema_de_ficheiros {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] 크기들 = new int[8];
    static int[] abrir_CONTAR = new int[8], 허가들 = new int[8];
    static int[] Nome = new int[64];
    static int[] editar_VALOR = new int[최대크기];
    static boolean 편집중 = false;
    static boolean 넘침 = false;
    static int 편집크기 = 0;

    static boolean cheque_nome(int[] carácter_VALOR, int duración_VALOR) {
        if (duración_VALOR < 1 || duración_VALOR > 63) return false;
        for (int 수 = 0; 수 < duración_VALOR; 수++) {
            int VALOR = carácter_VALOR[수];
            if (!(VALOR >= 'a' && VALOR <= 'z') && !(VALOR >= 'A' && VALOR <= 'Z')
                && !(VALOR >= '0' && VALOR <= '9') && VALOR != '_' && VALOR != '-' && VALOR != '.') return false;
        }
        return carácter_VALOR[0] != '.';
    }

    static int Busca_introdución(int[] carácter_VALOR, int duración_VALOR) {
        if (!cheque_nome(carácter_VALOR, duración_VALOR)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + duración_VALOR] == 0;
            for (int 칸 = 0; 칸 < duración_VALOR; 칸++) if (이름들[수 * 64 + 칸] != carácter_VALOR[칸]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALOR(int[] carácter_VALOR, int duración_VALOR, int[] datos, int Tamaño) {
        if (!cheque_nome(carácter_VALOR, duración_VALOR) || Tamaño < 0 || Tamaño > datos.length) return -22;
        if (Tamaño > 최대크기) return -90;
        int ÍNDICE = Busca_introdución(carácter_VALOR, duración_VALOR);
        if (ÍNDICE == -2) {
            for (int 수 = 0; 수 < 8 && ÍNDICE < 0; 수++) if (이름들[수 * 64] == 0 && abrir_CONTAR[수] == 0) ÍNDICE = 수;
            if (ÍNDICE >= 0) 허가들[ÍNDICE] = 438;
        }
        if (ÍNDICE < 0) return -28;
        int ENDEREZO = dispositivo_VALOR.Ficheiro_Memoria() + ÍNDICE * 최대크기;
        for (int 수 = 0; 수 < Tamaño; 수++) dispositivo_VALOR.escribir_Memoria(ENDEREZO + 수, datos[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[ÍNDICE * 64 + 수] = 수 < duración_VALOR ? carácter_VALOR[수] : 0;
        크기들[ÍNDICE] = Tamaño;
        return Tamaño;
    }

    static void introdución_Lista() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[수 * 64 + 칸] != 0; 칸++) SMS_Terminal.문자(이름들[수 * 64 + 칸]);
            SMS_Terminal.Escritura("  "); SMS_Terminal.수쓰기(크기들[수]); SMS_Terminal.Escritura("byte_VALOR\n");
        }
        SMS_Terminal.Escritura(Almacenamento_dispositivo_conexión.Tecnoloxía_da_información_TI_Activo_9e72441a ? "Ficheiro 8칸, 파일당 16384바이트; sync로 Store_VALOR 장치에 보존\n"
            : "임시 Ficheiro 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Orde(int[] 입력, int Executar_2, int duración_VALOR, int Acción) {
        while (Executar_2 < duración_VALOR && 입력[Executar_2] == ' ') Executar_2++;
        int 끝 = duración_VALOR;
        while (끝 > Executar_2 && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Executar_2;
        if (수 < 1 || 수 > 63) { SMS_Terminal.Escritura("올바르지 않은 Ficheiro Nome\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) Nome[칸] = 칸 < 수 ? 입력[Executar_2 + 칸] : 0;
        int ÍNDICE = Busca_introdución(Nome, 수);
        if (ÍNDICE == -22) { SMS_Terminal.Escritura("올바르지 않은 Ficheiro Nome\n"); return; }
        if (Acción == 0) {
            편집중 = true; 편집크기 = 0; 넘침 = false;
            SMS_Terminal.Escritura("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (ÍNDICE < 0) SMS_Terminal.Escritura("파일을 찾을 수 없습니다\n");
        else if (Acción == 1) {
            int ENDEREZO = dispositivo_VALOR.Ficheiro_Memoria() + ÍNDICE * 최대크기;
            for (int 칸 = 0; 칸 < 크기들[ÍNDICE]; 칸++) SMS_Terminal.문자(dispositivo_VALOR.기억읽기(ENDEREZO + 칸));
            SMS_Terminal.문자(10);
        } else { 이름들[ÍNDICE * 64] = 0; 크기들[ÍNDICE] = 0; SMS_Terminal.Escritura("파일을 지웠습니다\n"); }
    }

    static boolean Tecnoloxía_da_información_TI_EXACTO(int[] 입력, int duración_VALOR, String 문구) {
        if (duración_VALOR != 문구.length()) return false;
        for (int 칸 = 0; 칸 < duración_VALOR; 칸++) if (입력[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void Edición_liña(int[] 입력, int duración_VALOR, boolean 줄넘침) {
        if (Tecnoloxía_da_información_TI_EXACTO(입력, duración_VALOR, ".cancel")) {
            편집중 = false; SMS_Terminal.Escritura("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (Tecnoloxía_da_información_TI_EXACTO(입력, duración_VALOR, ".save")) {
            편집중 = false;
            if (넘침) { SMS_Terminal.Escritura("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Nome[수] != 0) 수++;
            int RESULTANTE = Store_VALOR(Nome, 수, editar_VALOR, 편집크기);
            SMS_Terminal.Escritura(RESULTANTE >= 0 ? "보존한 byte_VALOR 수: " : "보존 erro_VALOR: ");
            SMS_Terminal.수쓰기(RESULTANTE); SMS_Terminal.문자(10);
        } else if (줄넘침 || duración_VALOR + 1 > 최대크기 - 편집크기) 넘침 = true;
        else {
            for (int 수 = 0; 수 < duración_VALOR; 수++) editar_VALOR[편집크기++] = 입력[수];
            editar_VALOR[편집크기++] = 10;
        }
    }

    static void 예제(String Ficheiro, String Contido_VALOR) {
        for (int 수 = 0; 수 < 64; 수++) Nome[수] = 수 < Ficheiro.length() ? Ficheiro.charAt(수) : 0;
        for (int 수 = 0; 수 < Contido_VALOR.length(); 수++) editar_VALOR[수] = Contido_VALOR.charAt(수);
        Store_VALOR(Nome, Ficheiro.length(), editar_VALOR, Contido_VALOR.length());
    }

    static void 준비() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Grupo_VALOR = dispositivo_VALOR.자바파일묶음(), Tamaño = dispositivo_VALOR.자바파일묶음크기();
        if (Tamaño < 8 || 실행관리.수(Grupo_VALOR) != 0x464a4b4a) { SMS_Terminal.Escritura("올바르지 않은 Java Ficheiro Grupo_VALOR\n"); return; }
        int elemento_CONTAR = 실행관리.수(Grupo_VALOR + 4);
        if (elemento_CONTAR < 0 || elemento_CONTAR > 8 || elemento_CONTAR > (Tamaño - 8) / 72) { SMS_Terminal.Escritura("올바르지 않은 Java Ficheiro introdución_Lista\n"); return; }
        for (int 수 = 0; 수 < elemento_CONTAR; 수++) {
            int introdución_VALOR = Grupo_VALOR + 8 + 수 * 72, duración_VALOR = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Nome[칸] = dispositivo_VALOR.기억읽기(introdución_VALOR + 칸);
            while (duración_VALOR < 64 && Nome[duración_VALOR] != 0) duración_VALOR++;
            int Posición = 실행관리.수(introdución_VALOR + 64), 파일크기 = 실행관리.수(introdución_VALOR + 68);
            if (!cheque_nome(Nome, duración_VALOR) || 파일크기 < 0 || 파일크기 > 최대크기 || Posición < 8 + elemento_CONTAR * 72 || Posición > Tamaño - 파일크기) {
                SMS_Terminal.Escritura("올바르지 않은 Java Ficheiro introdución_VALOR\n"); return;
            }
            for (int 칸 = 0; 칸 < 파일크기; 칸++) editar_VALOR[칸] = dispositivo_VALOR.기억읽기(Grupo_VALOR + Posición + 칸);
            if (Store_VALOR(Nome, duración_VALOR, editar_VALOR, 파일크기) < 0) { SMS_Terminal.Escritura("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
