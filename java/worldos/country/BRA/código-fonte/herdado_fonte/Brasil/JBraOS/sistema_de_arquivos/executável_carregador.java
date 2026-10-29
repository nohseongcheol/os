// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Brasil.JBraOS.sistema_de_arquivos;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Executar_comando 파일의 머리부와 적재 구역을 검증한다. */
public final class executável_carregador {
    public static final class seção_VALOR {
        private final int Tipo_VALOR;
        private final int sinalizar_VALOR;
        private final int Endereço;
        private final int Arquivo_cargo_2aa21a9a;
        private final int Tamanho;

        seção_VALOR(int Tipo_VALOR, int sinalizar_VALOR, int Endereço, int Arquivo_cargo_2aa21a9a, int Tamanho) {
            this.Tipo_VALOR = Tipo_VALOR;
            this.sinalizar_VALOR = sinalizar_VALOR;
            this.Endereço = Endereço;
            this.Arquivo_cargo_2aa21a9a = Arquivo_cargo_2aa21a9a;
            this.Tamanho = Tamanho;
        }

        public int Tipo_VALOR() {
            return Tipo_VALOR;
        }

        public int sinalizar_VALOR() {
            return sinalizar_VALOR;
        }

        public int Endereço() {
            return Endereço;
        }

        public int Arquivo_cargo_2aa21a9a() {
            return Arquivo_cargo_2aa21a9a;
        }

        public int Tamanho() {
            return Tamanho;
        }
    }

    public static final class foto {
        private final int START_email;
        private final List<seção_VALOR> 구역들;

        foto(int START_email, List<seção_VALOR> 구역들) {
            this.START_email = START_email;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int START_email() {
            return START_email;
        }

        public List<seção_VALOR> 구역들() {
            return 구역들;
        }
    }

    public foto 검사(byte[] dados) {
        if (dados == null || dados.length < 52
                || dados[0] != 0x7f || dados[1] != 'E' || dados[2] != 'L' || dados[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (dados[4] != 1 || dados[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int START_email = analisar_inteiro(dados, 24);
        int seção_tabela_cargo = analisar_inteiro(dados, 32);
        int seção_entrada_dimensionar = 짧은정수읽기(dados, 46);
        int seção_CONT_NÚM = 짧은정수읽기(dados, 48);
        if (seção_entrada_dimensionar < 40 || seção_tabela_cargo < 0
                || (long) seção_tabela_cargo + (long) seção_entrada_dimensionar * seção_CONT_NÚM > dados.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<seção_VALOR> 구역들 = new ArrayList<seção_VALOR>();
        for (int ÍNDICE = 0; ÍNDICE < seção_CONT_NÚM; ÍNDICE++) {
            int posição = seção_tabela_cargo + ÍNDICE * seção_entrada_dimensionar;
            int Tipo_VALOR = analisar_inteiro(dados, posição + 4);
            int sinalizar_VALOR = analisar_inteiro(dados, posição + 8);
            int Endereço = analisar_inteiro(dados, posição + 12);
            int Arquivo_cargo_2aa21a9a = analisar_inteiro(dados, posição + 16);
            int Tamanho = analisar_inteiro(dados, posição + 20);
            if (Tamanho < 0 || (Tipo_VALOR != 8 && ((long) Arquivo_cargo_2aa21a9a + Tamanho > dados.length || Arquivo_cargo_2aa21a9a < 0))) {
                throw new IllegalArgumentException("ELF seção_VALOR dados 범위가 올바르지 않습니다.");
            }
            구역들.add(new seção_VALOR(Tipo_VALOR, sinalizar_VALOR, Endereço, Arquivo_cargo_2aa21a9a, Tamanho));
        }
        return new foto(START_email, 구역들);
    }

    private int analisar_inteiro(byte[] dados, int posição) {
        if (posição < 0 || posição > dados.length - 4) {
            throw new IllegalArgumentException("ELF inteiro 범위를 벗어났습니다.");
        }
        return (dados[posição] & 0xff)
                | ((dados[posição + 1] & 0xff) << 8)
                | ((dados[posição + 2] & 0xff) << 16)
                | ((dados[posição + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] dados, int posição) {
        if (posição < 0 || posição > dados.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 inteiro 범위를 벗어났습니다.");
        }
        return (dados[posição] & 0xff) | ((dados[posição + 1] & 0xff) << 8);
    }
}
