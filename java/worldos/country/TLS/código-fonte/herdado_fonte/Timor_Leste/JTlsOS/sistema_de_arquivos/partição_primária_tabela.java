// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Timor_Leste.JTlsOS.sistema_de_arquivos;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 valor_padrão 분할 영역을 읽는다. */
public final class partição_primária_tabela {
    public static final class partição_VALOR {
        private final int Tipo_VALOR;
        private final long START_seção;
        private final long seção_CONT_NÚM;

        partição_VALOR(int Tipo_VALOR, long START_seção, long seção_CONT_NÚM) {
            this.Tipo_VALOR = Tipo_VALOR;
            this.START_seção = START_seção;
            this.seção_CONT_NÚM = seção_CONT_NÚM;
        }

        public int Tipo_VALOR() { return Tipo_VALOR; }
        public long START_seção() { return START_seção; }
        public long seção_CONT_NÚM() { return seção_CONT_NÚM; }
    }

    public List<partição_VALOR> Leitura(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partição_VALOR> resultado = new ArrayList<partição_VALOR>();
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) {
            int posição = 446 + ÍNDICE * 16;
            int Tipo_VALOR = 첫구역[posição + 4] & 0xff;
            long iniciar = little_endian_inteiro(첫구역, posição + 8);
            long Tamanho = little_endian_inteiro(첫구역, posição + 12);
            if (Tipo_VALOR != 0 && Tamanho != 0) {
                resultado.add(new partição_VALOR(Tipo_VALOR, iniciar, Tamanho));
            }
        }
        return Collections.unmodifiableList(resultado);
    }

    private long little_endian_inteiro(byte[] dados, int posição) {
        return (dados[posição] & 0xffL)
                | ((dados[posição + 1] & 0xffL) << 8)
                | ((dados[posição + 2] & 0xffL) << 16)
                | ((dados[posição + 3] & 0xffL) << 24);
    }
}

