// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package São_Tomé_e_Príncipe.JStpOS.Memória_região;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 alinhar_VALOR alocar_Armazenamento, lançar_Armazenamento, 병합을 담당한다. */
public final class Memória_gerente {
    private final byte[] Memória_região;
    private final TreeMap<Integer, Integer> vazio_região = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Memória_gerente(int total_dimensionar) {
        if (total_dimensionar < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Memória_região = new byte[total_dimensionar];
        vazio_região.put(Integer.valueOf(4096), Integer.valueOf(total_dimensionar - 4096));
    }

    public synchronized int alocar_Armazenamento(int Tamanho) {
        return 정렬할당(Tamanho, 1);
    }

    public synchronized int 정렬할당(int Tamanho, int alinhar_VALOR) {
        if (Tamanho <= 0 || alinhar_VALOR <= 0 || (alinhar_VALOR & (alinhar_VALOR - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> entrada_VALOR_962f286b : vazio_região.entrySet()) {
            int iniciar = entrada_VALOR_962f286b.getKey().intValue();
            int região_dimensionar = entrada_VALOR_962f286b.getValue().intValue();
            int 정렬시작 = (iniciar + alinhar_VALOR - 1) & -alinhar_VALOR;
            int câmera_frontal_VALOR_dimensionar = 정렬시작 - iniciar;
            int 끝크기 = região_dimensionar - câmera_frontal_VALOR_dimensionar - Tamanho;
            if (끝크기 < 0) {
                continue;
            }
            vazio_região.remove(Integer.valueOf(iniciar));
            if (câmera_frontal_VALOR_dimensionar > 0) {
                vazio_região.put(Integer.valueOf(iniciar), Integer.valueOf(câmera_frontal_VALOR_dimensionar));
            }
            if (끝크기 > 0) {
                vazio_região.put(Integer.valueOf(정렬시작 + Tamanho), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Tamanho));
            Arrays.fill(Memória_região, 정렬시작, 정렬시작 + Tamanho, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void lançar_Armazenamento(int Endereço) {
        Integer dimensionar_objeto = 사용영역.remove(Integer.valueOf(Endereço));
        if (dimensionar_objeto == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int iniciar = Endereço;
        int Tamanho = dimensionar_objeto.intValue();
        Map.Entry<Integer, Integer> câmera_frontal_VALOR = vazio_região.lowerEntry(Integer.valueOf(iniciar));
        if (câmera_frontal_VALOR != null && câmera_frontal_VALOR.getKey().intValue() + câmera_frontal_VALOR.getValue().intValue() == iniciar) {
            iniciar = câmera_frontal_VALOR.getKey().intValue();
            Tamanho += câmera_frontal_VALOR.getValue().intValue();
            vazio_região.remove(câmera_frontal_VALOR.getKey());
        }
        Map.Entry<Integer, Integer> BACK_VALOR = vazio_região.ceilingEntry(Integer.valueOf(iniciar));
        if (BACK_VALOR != null && iniciar + Tamanho == BACK_VALOR.getKey().intValue()) {
            Tamanho += BACK_VALOR.getValue().intValue();
            vazio_região.remove(BACK_VALOR.getKey());
        }
        vazio_região.put(Integer.valueOf(iniciar), Integer.valueOf(Tamanho));
    }

    public synchronized byte leitura_byte_VALOR(int Endereço) {
        cheque_alcance(Endereço, 1);
        return Memória_região[Endereço];
    }

    public synchronized void gravar_byte_VALOR(int Endereço, byte VALOR) {
        cheque_alcance(Endereço, 1);
        Memória_região[Endereço] = VALOR;
    }

    public synchronized int total_dimensionar() {
        return Memória_região.length;
    }

    public synchronized int 사용크기() {
        int total_VALOR = 0;
        for (Integer Tamanho : 사용영역.values()) {
            total_VALOR += Tamanho.intValue();
        }
        return total_VALOR;
    }

    private void cheque_alcance(int Endereço, int Tamanho) {
        if (Endereço < 0 || Tamanho < 0 || Endereço > Memória_região.length - Tamanho) {
            throw new IndexOutOfBoundsException("Memória_região 범위를 벗어났습니다.");
        }
    }
}

