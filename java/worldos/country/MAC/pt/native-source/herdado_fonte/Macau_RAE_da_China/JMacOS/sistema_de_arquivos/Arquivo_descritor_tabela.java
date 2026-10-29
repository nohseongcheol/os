// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Macau_RAE_da_China.JMacOS.sistema_de_arquivos;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ficheiro 설명을 유지한다. */
public final class Arquivo_descritor_tabela {
    private static final int 최대서술자 = 32;

    private static final class descritor_entrada {
        private final sistema_de_arquivos.열린파일 열린파일;
        private boolean 실행시닫기;

        descritor_entrada(sistema_de_arquivos.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final sistema_de_arquivos sistema_de_arquivos;
    private final Map<Integer, descritor_entrada> 서술자들 = new HashMap<Integer, descritor_entrada>();

    public Arquivo_descritor_tabela(sistema_de_arquivos sistema_de_arquivos) {
        this.sistema_de_arquivos = sistema_de_arquivos;
    }

    public int Abrir(String Nome) {
        sistema_de_arquivos.열린파일 열린파일 = sistema_de_arquivos.Abrir(Nome);
        if (열린파일 == null) {
            return -2;
        }
        int ÍNDICE = vazio_ÍNDICE(3);
        if (ÍNDICE < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(ÍNDICE), new descritor_entrada(열린파일));
        return ÍNDICE;
    }

    public int Leitura(int ÍNDICE, byte[] receber_destino, int Tamanho) {
        descritor_entrada entrada_VALOR_962f286b = 서술자들.get(Integer.valueOf(ÍNDICE));
        if (entrada_VALOR_962f286b == null) {
            return -9;
        }
        if (Tamanho < 0 || Tamanho > receber_destino.length) {
            return -22;
        }
        int 남음 = entrada_VALOR_962f286b.열린파일.dados.length - entrada_VALOR_962f286b.열린파일.posição;
        int leitura_dimensionar = Math.min(Tamanho, Math.max(남음, 0));
        System.arraycopy(entrada_VALOR_962f286b.열린파일.dados, entrada_VALOR_962f286b.열린파일.posição, receber_destino, 0, leitura_dimensionar);
        entrada_VALOR_962f286b.열린파일.posição += leitura_dimensionar;
        return leitura_dimensionar;
    }

    public int mover_cargo(int ÍNDICE, int 거리, int ação_raiz) {
        descritor_entrada entrada_VALOR_962f286b = 서술자들.get(Integer.valueOf(ÍNDICE));
        if (entrada_VALOR_962f286b == null) {
            return -9;
        }
        int Tela_de_fundo_VALOR;
        if (ação_raiz == 0) {
            Tela_de_fundo_VALOR = 0;
        } else if (ação_raiz == 1) {
            Tela_de_fundo_VALOR = entrada_VALOR_962f286b.열린파일.posição;
        } else if (ação_raiz == 2) {
            Tela_de_fundo_VALOR = entrada_VALOR_962f286b.열린파일.dados.length;
        } else {
            return -22;
        }
        int 새위치 = Tela_de_fundo_VALOR + 거리;
        if (새위치 < 0) {
            return -22;
        }
        entrada_VALOR_962f286b.열린파일.posição = 새위치;
        return 새위치;
    }

    public int Fechar(int ÍNDICE) {
        descritor_entrada entrada_VALOR_962f286b = 서술자들.remove(Integer.valueOf(ÍNDICE));
        if (entrada_VALOR_962f286b == null) {
            return -9;
        }
        entrada_VALOR_962f286b.열린파일.Referência_CONT_NÚM--;
        return 0;
    }

    public int 복제서술자(int ÍNDICE, int 최소번호) {
        descritor_entrada entrada_VALOR_962f286b = 서술자들.get(Integer.valueOf(ÍNDICE));
        if (entrada_VALOR_962f286b == null) {
            return -9;
        }
        int Novo_Número = vazio_ÍNDICE(최소번호);
        if (Novo_Número < 0) {
            return -24;
        }
        entrada_VALOR_962f286b.열린파일.Referência_CONT_NÚM++;
        서술자들.put(Integer.valueOf(Novo_Número), new descritor_entrada(entrada_VALOR_962f286b.열린파일));
        return Novo_Número;
    }

    public int 지정복제(int ÍNDICE, int Novo_Número) {
        if (ÍNDICE == Novo_Número) {
            return 서술자들.containsKey(Integer.valueOf(ÍNDICE)) ? ÍNDICE : -9;
        }
        if (Novo_Número < 0 || Novo_Número >= 최대서술자) {
            return -9;
        }
        descritor_entrada 원본 = 서술자들.get(Integer.valueOf(ÍNDICE));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Novo_Número))) {
            Fechar(Novo_Número);
        }
        원본.열린파일.Referência_CONT_NÚM++;
        서술자들.put(Integer.valueOf(Novo_Número), new descritor_entrada(원본.열린파일));
        return Novo_Número;
    }

    public int 실행시닫기설정(int ÍNDICE, boolean VALOR) {
        descritor_entrada entrada_VALOR_962f286b = 서술자들.get(Integer.valueOf(ÍNDICE));
        if (entrada_VALOR_962f286b == null) {
            return -9;
        }
        entrada_VALOR_962f286b.실행시닫기 = VALOR;
        return 0;
    }

    public int 실행시닫기값(int ÍNDICE) {
        descritor_entrada entrada_VALOR_962f286b = 서술자들.get(Integer.valueOf(ÍNDICE));
        if (entrada_VALOR_962f286b == null) {
            return -9;
        }
        return entrada_VALOR_962f286b.실행시닫기 ? 1 : 0;
    }

    public Arquivo_informações msinfo32_exe(int ÍNDICE) {
        if (ÍNDICE >= 0 && ÍNDICE <= 2) {
            return new Arquivo_informações(0, 0020666);
        }
        descritor_entrada entrada_VALOR_962f286b = 서술자들.get(Integer.valueOf(ÍNDICE));
        if (entrada_VALOR_962f286b == null) {
            return null;
        }
        return new Arquivo_informações(entrada_VALOR_962f286b.열린파일.dados.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] número_Lista = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer ÍNDICE : número_Lista) {
            descritor_entrada entrada_VALOR_962f286b = 서술자들.get(ÍNDICE);
            if (entrada_VALOR_962f286b != null && entrada_VALOR_962f286b.실행시닫기) {
                Fechar(ÍNDICE.intValue());
            }
        }
    }

    public boolean TI_abrir(int ÍNDICE) {
        return 서술자들.containsKey(Integer.valueOf(ÍNDICE));
    }

    public Arquivo_descritor_tabela clone_VALOR() {
        Arquivo_descritor_tabela resultado = new Arquivo_descritor_tabela(sistema_de_arquivos);
        for (Map.Entry<Integer, descritor_entrada> entrada_VALOR_962f286b : 서술자들.entrySet()) {
            entrada_VALOR_962f286b.getValue().열린파일.Referência_CONT_NÚM++;
            descritor_entrada 새서술자 = new descritor_entrada(entrada_VALOR_962f286b.getValue().열린파일);
            새서술자.실행시닫기 = entrada_VALOR_962f286b.getValue().실행시닫기;
            resultado.서술자들.put(entrada_VALOR_962f286b.getKey(), 새서술자);
        }
        return resultado;
    }

    private int vazio_ÍNDICE(int 최소번호) {
        for (int ÍNDICE = Math.max(0, 최소번호); ÍNDICE < 최대서술자; ÍNDICE++) {
            if (!서술자들.containsKey(Integer.valueOf(ÍNDICE))) {
                return ÍNDICE;
            }
        }
        return -1;
    }
}
