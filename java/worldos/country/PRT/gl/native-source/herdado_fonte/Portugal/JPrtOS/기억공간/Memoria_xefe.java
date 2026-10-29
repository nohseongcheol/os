// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Portugal.JPrtOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 aliñar_VALOR atribuír_Almacenamento, liberar_Almacenamento, 병합을 담당한다. */
public final class Memoria_xefe {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Memoria_xefe(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int atribuír_Almacenamento(int Tamaño) {
        return 정렬할당(Tamaño, 1);
    }

    public synchronized int 정렬할당(int Tamaño, int aliñar_VALOR) {
        if (Tamaño <= 0 || aliñar_VALOR <= 0 || (aliñar_VALOR & (aliñar_VALOR - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> introdución_VALOR : 빈영역.entrySet()) {
            int Executar_2 = introdución_VALOR.getKey().intValue();
            int 영역크기 = introdución_VALOR.getValue().intValue();
            int 정렬시작 = (Executar_2 + aliñar_VALOR - 1) & -aliñar_VALOR;
            int 앞크기 = 정렬시작 - Executar_2;
            int 끝크기 = 영역크기 - 앞크기 - Tamaño;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Executar_2));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(Executar_2), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Tamaño), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Tamaño));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Tamaño, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void liberar_Almacenamento(int ENDEREZO) {
        Integer 크기객체 = 사용영역.remove(Integer.valueOf(ENDEREZO));
        if (크기객체 == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Executar_2 = ENDEREZO;
        int Tamaño = 크기객체.intValue();
        Map.Entry<Integer, Integer> frontal_VALOR = 빈영역.lowerEntry(Integer.valueOf(Executar_2));
        if (frontal_VALOR != null && frontal_VALOR.getKey().intValue() + frontal_VALOR.getValue().intValue() == Executar_2) {
            Executar_2 = frontal_VALOR.getKey().intValue();
            Tamaño += frontal_VALOR.getValue().intValue();
            빈영역.remove(frontal_VALOR.getKey());
        }
        Map.Entry<Integer, Integer> ATRÁS_VALOR = 빈영역.ceilingEntry(Integer.valueOf(Executar_2));
        if (ATRÁS_VALOR != null && Executar_2 + Tamaño == ATRÁS_VALOR.getKey().intValue()) {
            Tamaño += ATRÁS_VALOR.getValue().intValue();
            빈영역.remove(ATRÁS_VALOR.getKey());
        }
        빈영역.put(Integer.valueOf(Executar_2), Integer.valueOf(Tamaño));
    }

    public synchronized byte 바이트읽기(int ENDEREZO) {
        cheque_intervalo(ENDEREZO, 1);
        return 기억공간[ENDEREZO];
    }

    public synchronized void escribir_byte_VALOR(int ENDEREZO, byte VALOR) {
        cheque_intervalo(ENDEREZO, 1);
        기억공간[ENDEREZO] = VALOR;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Tamaño : 사용영역.values()) {
            합계 += Tamaño.intValue();
        }
        return 합계;
    }

    private void cheque_intervalo(int ENDEREZO, int Tamaño) {
        if (ENDEREZO < 0 || Tamaño < 0 || ENDEREZO > 기억공간.length - Tamaño) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

