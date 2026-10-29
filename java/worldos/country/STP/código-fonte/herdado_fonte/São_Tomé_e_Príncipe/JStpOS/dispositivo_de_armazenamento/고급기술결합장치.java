// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package São_Tomé_e_Príncipe.JStpOS.dispositivo_de_armazenamento;

import java.util.Arrays;

/** ATA 28비트 comando 계층과 같은 512바이트 논리 seção_VALOR 장치다. */
public final class 고급기술결합장치 {
    public static final int seção_dimensionar = 512;
    private final byte[] dados;
    private final boolean somente_leitura_VALOR;

    public 고급기술결합장치(int seção_CONT_NÚM, boolean somente_leitura_VALOR) {
        if (seção_CONT_NÚM <= 0) {
            throw new IllegalArgumentException("seção_VALOR 수가 올바르지 않습니다.");
        }
        dados = new byte[Math.multiplyExact(seção_CONT_NÚM, seção_dimensionar)];
        this.somente_leitura_VALOR = somente_leitura_VALOR;
    }

    public int seção_CONT_NÚM() {
        return dados.length / seção_dimensionar;
    }

    public void Leitura(int seção_ÍNDICE, byte[] receber_destino) {
        cheque_alcance(seção_ÍNDICE, receber_destino);
        System.arraycopy(dados, seção_ÍNDICE * seção_dimensionar, receber_destino, 0, seção_dimensionar);
    }

    public void Escrita(int seção_ÍNDICE, byte[] 쓸자료) {
        if (somente_leitura_VALOR) {
            throw new IllegalStateException("Leitura 전용 장치입니다.");
        }
        cheque_alcance(seção_ÍNDICE, 쓸자료);
        System.arraycopy(쓸자료, 0, dados, seção_ÍNDICE * seção_dimensionar, seção_dimensionar);
    }

    public void apagar_entrada() {
        if (somente_leitura_VALOR) {
            throw new IllegalStateException("Leitura 전용 장치입니다.");
        }
        Arrays.fill(dados, (byte) 0);
    }

    private void cheque_alcance(int seção_ÍNDICE, byte[] 임시공간) {
        if (seção_ÍNDICE < 0 || seção_ÍNDICE >= seção_CONT_NÚM() || 임시공간.length < seção_dimensionar) {
            throw new IllegalArgumentException("ATA seção_VALOR 범위가 올바르지 않습니다.");
        }
    }
}

