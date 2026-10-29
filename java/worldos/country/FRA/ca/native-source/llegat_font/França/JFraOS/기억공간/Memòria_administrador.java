// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package França.JFraOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 alinear_VALOR assignar_Emmagatzematge, versió_Emmagatzematge, 병합을 담당한다. */
public final class Memòria_administrador {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Memòria_administrador(int total_canviar_la_mida) {
        if (total_canviar_la_mida < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[total_canviar_la_mida];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(total_canviar_la_mida - 4096));
    }

    public synchronized int assignar_Emmagatzematge(int Mida) {
        return 정렬할당(Mida, 1);
    }

    public synchronized int 정렬할당(int Mida, int alinear_VALOR) {
        if (Mida <= 0 || alinear_VALOR <= 0 || (alinear_VALOR & (alinear_VALOR - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> introducció_VALOR : 빈영역.entrySet()) {
            int Executa_2 = introducció_VALOR.getKey().intValue();
            int 영역크기 = introducció_VALOR.getValue().intValue();
            int 정렬시작 = (Executa_2 + alinear_VALOR - 1) & -alinear_VALOR;
            int frontal_VALOR_canviar_la_mida = 정렬시작 - Executa_2;
            int 끝크기 = 영역크기 - frontal_VALOR_canviar_la_mida - Mida;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Executa_2));
            if (frontal_VALOR_canviar_la_mida > 0) {
                빈영역.put(Integer.valueOf(Executa_2), Integer.valueOf(frontal_VALOR_canviar_la_mida));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Mida), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Mida));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Mida, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void versió_Emmagatzematge(int Adreça) {
        Integer canviar_la_mida_objecte = 사용영역.remove(Integer.valueOf(Adreça));
        if (canviar_la_mida_objecte == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Executa_2 = Adreça;
        int Mida = canviar_la_mida_objecte.intValue();
        Map.Entry<Integer, Integer> frontal_VALOR = 빈영역.lowerEntry(Integer.valueOf(Executa_2));
        if (frontal_VALOR != null && frontal_VALOR.getKey().intValue() + frontal_VALOR.getValue().intValue() == Executa_2) {
            Executa_2 = frontal_VALOR.getKey().intValue();
            Mida += frontal_VALOR.getValue().intValue();
            빈영역.remove(frontal_VALOR.getKey());
        }
        Map.Entry<Integer, Integer> ENRERE_VALOR = 빈영역.ceilingEntry(Integer.valueOf(Executa_2));
        if (ENRERE_VALOR != null && Executa_2 + Mida == ENRERE_VALOR.getKey().intValue()) {
            Mida += ENRERE_VALOR.getValue().intValue();
            빈영역.remove(ENRERE_VALOR.getKey());
        }
        빈영역.put(Integer.valueOf(Executa_2), Integer.valueOf(Mida));
    }

    public synchronized byte tancar_byte_VALOR(int Adreça) {
        xec_interval(Adreça, 1);
        return 기억공간[Adreça];
    }

    public synchronized void escriure_byte_VALOR(int Adreça, byte VALOR) {
        xec_interval(Adreça, 1);
        기억공간[Adreça] = VALOR;
    }

    public synchronized int total_canviar_la_mida() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int total_VALOR = 0;
        for (Integer Mida : 사용영역.values()) {
            total_VALOR += Mida.intValue();
        }
        return total_VALOR;
    }

    private void xec_interval(int Adreça, int Mida) {
        if (Adreça < 0 || Mida < 0 || Adreça > 기억공간.length - Mida) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

