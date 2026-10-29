// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 ficheiro. 원본 Editar_VALOR/compilar_fonte falha_VALOR 시 기존 파일을 보존한다. */
public final class Memória_sistema_de_arquivos {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] dimensionar_Lista = new int[8];
    static int[] abrir_CONT_NÚM = new int[8], 허가들 = new int[8];
    static int[] Nome = new int[64];
    static int[] Editar_VALOR = new int[최대크기];
    static boolean 편집중 = false;
    static boolean estouro_VALOR = false;
    static int Editar_dimensionar = 0;

    static boolean cheque_nome(int[] caractere_VALOR, int duração_VALOR) {
        if (duração_VALOR < 1 || duração_VALOR > 63) return false;
        for (int número = 0; número < duração_VALOR; número++) {
            int VALOR = caractere_VALOR[número];
            if (!(VALOR >= 'a' && VALOR <= 'z') && !(VALOR >= 'A' && VALOR <= 'Z')
                && !(VALOR >= '0' && VALOR <= '9') && VALOR != '_' && VALOR != '-' && VALOR != '.') return false;
        }
        return caractere_VALOR[0] != '.';
    }

    static int PROCURAR_entrada(int[] caractere_VALOR, int duração_VALOR) {
        if (!cheque_nome(caractere_VALOR, duração_VALOR)) return -22;
        for (int número = 0; número < 8; número++) {
            boolean 같음 = 이름들[número * 64 + duração_VALOR] == 0;
            for (int slot_entrada = 0; slot_entrada < duração_VALOR; slot_entrada++) if (이름들[número * 64 + slot_entrada] != caractere_VALOR[slot_entrada]) 같음 = false;
            if (같음) return número;
        }
        return -2;
    }

    static int Store_VALOR(int[] caractere_VALOR, int duração_VALOR, int[] dados, int Tamanho) {
        if (!cheque_nome(caractere_VALOR, duração_VALOR) || Tamanho < 0 || Tamanho > dados.length) return -22;
        if (Tamanho > 최대크기) return -90;
        int ÍNDICE = PROCURAR_entrada(caractere_VALOR, duração_VALOR);
        if (ÍNDICE == -2) {
            for (int número = 0; número < 8 && ÍNDICE < 0; número++) if (이름들[número * 64] == 0 && abrir_CONT_NÚM[número] == 0) ÍNDICE = número;
            if (ÍNDICE >= 0) 허가들[ÍNDICE] = 438;
        }
        if (ÍNDICE < 0) return -28;
        int Endereço = celular_VALOR.Arquivo_Memória() + ÍNDICE * 최대크기;
        for (int número = 0; número < Tamanho; número++) celular_VALOR.gravar_Memória(Endereço + número, dados[número]);
        for (int número = 0; número < 64; número++) 이름들[ÍNDICE * 64 + número] = número < duração_VALOR ? caractere_VALOR[número] : 0;
        dimensionar_Lista[ÍNDICE] = Tamanho;
        return Tamanho;
    }

    static void entrada_Lista_f07b3200() {
        for (int número = 0; número < 8; número++) if (이름들[número * 64] != 0) {
            for (int slot_entrada = 0; slot_entrada < 64 && 이름들[número * 64 + slot_entrada] != 0; slot_entrada++) SMS_Terminal.문자(이름들[número * 64 + slot_entrada]);
            SMS_Terminal.Escrita("  "); SMS_Terminal.gravar_número(dimensionar_Lista[número]); SMS_Terminal.Escrita("byte_VALOR\n");
        }
        SMS_Terminal.Escrita(dispositivo_de_armazenamento_conexão.TI_Ativo_9e72441a ? "ficheiro 8칸, 파일당 16384바이트; sync로 Store_VALOR 장치에 보존\n"
            : "임시 ficheiro 8칸, 파일당 16384바이트; repetir_VALOR 시작하면 사라짐\n");
    }

    static void comando(int[] entrada_VALOR, int iniciar, int duração_VALOR, int Acção) {
        while (iniciar < duração_VALOR && entrada_VALOR[iniciar] == ' ') iniciar++;
        int 끝 = duração_VALOR;
        while (끝 > iniciar && entrada_VALOR[끝 - 1] == ' ') 끝--;
        int número = 끝 - iniciar;
        if (número < 1 || número > 63) { SMS_Terminal.Escrita("올바르지 않은 ficheiro Nome\n"); return; }
        for (int slot_entrada = 0; slot_entrada < 64; slot_entrada++) Nome[slot_entrada] = slot_entrada < número ? entrada_VALOR[iniciar + slot_entrada] : 0;
        int ÍNDICE = PROCURAR_entrada(Nome, número);
        if (ÍNDICE == -22) { SMS_Terminal.Escrita("올바르지 않은 ficheiro Nome\n"); return; }
        if (Acção == 0) {
            편집중 = true; Editar_dimensionar = 0; estouro_VALOR = false;
            SMS_Terminal.Escrita("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (ÍNDICE < 0) SMS_Terminal.Escrita("파일을 찾을 número 없습니다\n");
        else if (Acção == 1) {
            int Endereço = celular_VALOR.Arquivo_Memória() + ÍNDICE * 최대크기;
            for (int slot_entrada = 0; slot_entrada < dimensionar_Lista[ÍNDICE]; slot_entrada++) SMS_Terminal.문자(celular_VALOR.leitura_Memória(Endereço + slot_entrada));
            SMS_Terminal.문자(10);
        } else { 이름들[ÍNDICE * 64] = 0; dimensionar_Lista[ÍNDICE] = 0; SMS_Terminal.Escrita("파일을 지웠습니다\n"); }
    }

    static boolean TI_EXATO(int[] entrada_VALOR, int duração_VALOR, String 문구) {
        if (duração_VALOR != 문구.length()) return false;
        for (int slot_entrada = 0; slot_entrada < duração_VALOR; slot_entrada++) if (entrada_VALOR[slot_entrada] != 문구.charAt(slot_entrada)) return false;
        return true;
    }

    static void Editado_linha(int[] entrada_VALOR, int duração_VALOR, boolean linha_estouro) {
        if (TI_EXATO(entrada_VALOR, duração_VALOR, ".cancel")) {
            편집중 = false; SMS_Terminal.Escrita("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (TI_EXATO(entrada_VALOR, duração_VALOR, ".save")) {
            편집중 = false;
            if (estouro_VALOR) { SMS_Terminal.Escrita("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int número = 0;
            while (número < 64 && Nome[número] != 0) número++;
            int resultado = Store_VALOR(Nome, número, Editar_VALOR, Editar_dimensionar);
            SMS_Terminal.Escrita(resultado >= 0 ? "보존한 byte_VALOR número: " : "보존 falha_VALOR: ");
            SMS_Terminal.gravar_número(resultado); SMS_Terminal.문자(10);
        } else if (linha_estouro || duração_VALOR + 1 > 최대크기 - Editar_dimensionar) estouro_VALOR = true;
        else {
            for (int número = 0; número < duração_VALOR; número++) Editar_VALOR[Editar_dimensionar++] = entrada_VALOR[número];
            Editar_VALOR[Editar_dimensionar++] = 10;
        }
    }

    static void 예제(String ficheiro, String Conteúdo_VALOR) {
        for (int número = 0; número < 64; número++) Nome[número] = número < ficheiro.length() ? ficheiro.charAt(número) : 0;
        for (int número = 0; número < Conteúdo_VALOR.length(); número++) Editar_VALOR[número] = Conteúdo_VALOR.charAt(número);
        Store_VALOR(Nome, ficheiro.length(), Editar_VALOR, Conteúdo_VALOR.length());
    }

    static void Preparar() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Grupo_VALOR = celular_VALOR.자바파일묶음(), Tamanho = celular_VALOR.자바파일묶음크기();
        if (Tamanho < 8 || execução_gerente.número(Grupo_VALOR) != 0x464a4b4a) { SMS_Terminal.Escrita("올바르지 않은 Java ficheiro Grupo_VALOR\n"); return; }
        int item_CONT_NÚM = execução_gerente.número(Grupo_VALOR + 4);
        if (item_CONT_NÚM < 0 || item_CONT_NÚM > 8 || item_CONT_NÚM > (Tamanho - 8) / 72) { SMS_Terminal.Escrita("올바르지 않은 Java ficheiro entrada_Lista_f07b3200\n"); return; }
        for (int número = 0; número < item_CONT_NÚM; número++) {
            int entrada_VALOR_962f286b = Grupo_VALOR + 8 + número * 72, duração_VALOR = 0;
            for (int slot_entrada = 0; slot_entrada < 64; slot_entrada++) Nome[slot_entrada] = celular_VALOR.leitura_Memória(entrada_VALOR_962f286b + slot_entrada);
            while (duração_VALOR < 64 && Nome[duração_VALOR] != 0) duração_VALOR++;
            int posição = execução_gerente.número(entrada_VALOR_962f286b + 64), tamanho_do_arquivo = execução_gerente.número(entrada_VALOR_962f286b + 68);
            if (!cheque_nome(Nome, duração_VALOR) || tamanho_do_arquivo < 0 || tamanho_do_arquivo > 최대크기 || posição < 8 + item_CONT_NÚM * 72 || posição > Tamanho - tamanho_do_arquivo) {
                SMS_Terminal.Escrita("올바르지 않은 Java ficheiro entrada_VALOR_962f286b\n"); return;
            }
            for (int slot_entrada = 0; slot_entrada < tamanho_do_arquivo; slot_entrada++) Editar_VALOR[slot_entrada] = celular_VALOR.leitura_Memória(Grupo_VALOR + posição + slot_entrada);
            if (Store_VALOR(Nome, duração_VALOR, Editar_VALOR, tamanho_do_arquivo) < 0) { SMS_Terminal.Escrita("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
