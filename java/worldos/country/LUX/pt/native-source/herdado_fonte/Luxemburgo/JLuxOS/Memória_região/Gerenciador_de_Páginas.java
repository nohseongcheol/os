// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Luxemburgo.JLuxOS.Memória_região;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB página_VALOR 연결과 Escrita 시 복사를 제공한다. */
public final class Gerenciador_de_Páginas {
    public static final int tamanho_da_página = 4096;

    private static final class página_VALOR {
        private byte[] dados = new byte[tamanho_da_página];
        private int Referência_CONT_NÚM = 1;
        private boolean 쓰기가능 = true;
        private boolean COW;
    }

    public static final class espaço_de_endereço {
        private final Map<Integer, página_VALOR> página_tabela = new HashMap<Integer, página_VALOR>();
    }

    public espaço_de_endereço 새주소공간() {
        return new espaço_de_endereço();
    }

    public void MAP_página(espaço_de_endereço email_região, int endereço_virtual, boolean 쓰기가능) {
        int ÍNDICE = página_número(endereço_virtual);
        página_VALOR 새쪽 = new página_VALOR();
        새쪽.쓰기가능 = 쓰기가능;
        email_região.página_tabela.put(Integer.valueOf(ÍNDICE), 새쪽);
    }

    public espaço_de_endereço clone_COW(espaço_de_endereço 원본) {
        espaço_de_endereço 복제본 = new espaço_de_endereço();
        for (Map.Entry<Integer, página_VALOR> entrada_VALOR_962f286b : 원본.página_tabela.entrySet()) {
            página_VALOR Compartilhado_página = entrada_VALOR_962f286b.getValue();
            Compartilhado_página.Referência_CONT_NÚM++;
            if (Compartilhado_página.쓰기가능) {
                Compartilhado_página.쓰기가능 = false;
                Compartilhado_página.COW = true;
            }
            복제본.página_tabela.put(entrada_VALOR_962f286b.getKey(), Compartilhado_página);
        }
        return 복제본;
    }

    public byte leitura_byte_VALOR(espaço_de_endereço email_região, int endereço_virtual) {
        página_VALOR meta = PROCURAR_página(email_região, endereço_virtual);
        return meta.dados[Math.floorMod(endereço_virtual, tamanho_da_página)];
    }

    public void gravar_byte_VALOR(espaço_de_endereço email_região, int endereço_virtual, byte VALOR) {
        int ÍNDICE = página_número(endereço_virtual);
        página_VALOR meta = PROCURAR_página(email_região, endereço_virtual);
        if (!meta.쓰기가능) {
            if (!meta.COW) {
                throw new IllegalStateException("Leitura 전용 쪽입니다.");
            }
            meta = Criar_Bloqueado_página(email_região, ÍNDICE, meta);
        }
        meta.dados[Math.floorMod(endereço_virtual, tamanho_da_página)] = VALOR;
    }

    public void Bloqueado_alcance_gravar(espaço_de_endereço email_região, int START_email, int Tamanho) {
        if (Tamanho < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int endereço_final = Math.addExact(START_email, Tamanho);
        for (int Endereço = START_email; Endereço < endereço_final; Endereço = (página_número(Endereço) + 1) * tamanho_da_página) {
            int ÍNDICE = página_número(Endereço);
            página_VALOR meta = PROCURAR_página(email_região, Endereço);
            if (meta.COW) {
                Criar_Bloqueado_página(email_região, ÍNDICE, meta);
            } else {
                meta.쓰기가능 = true;
            }
        }
    }

    public void alcance_gravar(espaço_de_endereço email_região, int START_email, byte[] dados) {
        for (int ÍNDICE = 0; ÍNDICE < dados.length; ÍNDICE++) {
            gravar_byte_VALOR(email_região, START_email + ÍNDICE, dados[ÍNDICE]);
        }
    }

    private página_VALOR Criar_Bloqueado_página(espaço_de_endereço email_região, int ÍNDICE, página_VALOR Compartilhado_página) {
        página_VALOR Bloqueado_página = new página_VALOR();
        Bloqueado_página.dados = Arrays.copyOf(Compartilhado_página.dados, Compartilhado_página.dados.length);
        Bloqueado_página.쓰기가능 = true;
        Bloqueado_página.COW = false;
        Compartilhado_página.Referência_CONT_NÚM--;
        email_região.página_tabela.put(Integer.valueOf(ÍNDICE), Bloqueado_página);
        return Bloqueado_página;
    }

    private página_VALOR PROCURAR_página(espaço_de_endereço email_região, int Endereço) {
        página_VALOR meta = email_região.página_tabela.get(Integer.valueOf(página_número(Endereço)));
        if (meta == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return meta;
    }

    private int página_número(int Endereço) {
        if (Endereço < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return Endereço / tamanho_da_página;
    }
}

