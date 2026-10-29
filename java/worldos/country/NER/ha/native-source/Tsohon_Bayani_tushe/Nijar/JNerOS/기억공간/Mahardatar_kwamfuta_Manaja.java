// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijar.JNerOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 Daidaita_Daraja kasafta_Wurin_adana, saka_Wurin_adana, 병합을 담당한다. */
public final class Mahardatar_kwamfuta_Manaja {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Mahardatar_kwamfuta_Manaja(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int kasafta_Wurin_adana(int Girma) {
        return 정렬할당(Girma, 1);
    }

    public synchronized int 정렬할당(int Girma, int Daidaita_Daraja) {
        if (Girma <= 0 || Daidaita_Daraja <= 0 || (Daidaita_Daraja & (Daidaita_Daraja - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> Mashigar_bayanai_Daraja : 빈영역.entrySet()) {
            int Tafiyar_da = Mashigar_bayanai_Daraja.getKey().intValue();
            int 영역크기 = Mashigar_bayanai_Daraja.getValue().intValue();
            int 정렬시작 = (Tafiyar_da + Daidaita_Daraja - 1) & -Daidaita_Daraja;
            int kyamarar_gaba_Daraja_girma = 정렬시작 - Tafiyar_da;
            int 끝크기 = 영역크기 - kyamarar_gaba_Daraja_girma - Girma;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Tafiyar_da));
            if (kyamarar_gaba_Daraja_girma > 0) {
                빈영역.put(Integer.valueOf(Tafiyar_da), Integer.valueOf(kyamarar_gaba_Daraja_girma));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Girma), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Girma));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Girma, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void saka_Wurin_adana(int imel) {
        Integer girma_abu = 사용영역.remove(Integer.valueOf(imel));
        if (girma_abu == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Tafiyar_da = imel;
        int Girma = girma_abu.intValue();
        Map.Entry<Integer, Integer> kyamarar_gaba_Daraja = 빈영역.lowerEntry(Integer.valueOf(Tafiyar_da));
        if (kyamarar_gaba_Daraja != null && kyamarar_gaba_Daraja.getKey().intValue() + kyamarar_gaba_Daraja.getValue().intValue() == Tafiyar_da) {
            Tafiyar_da = kyamarar_gaba_Daraja.getKey().intValue();
            Girma += kyamarar_gaba_Daraja.getValue().intValue();
            빈영역.remove(kyamarar_gaba_Daraja.getKey());
        }
        Map.Entry<Integer, Integer> Baya_Daraja = 빈영역.ceilingEntry(Integer.valueOf(Tafiyar_da));
        if (Baya_Daraja != null && Tafiyar_da + Girma == Baya_Daraja.getKey().intValue()) {
            Girma += Baya_Daraja.getValue().intValue();
            빈영역.remove(Baya_Daraja.getKey());
        }
        빈영역.put(Integer.valueOf(Tafiyar_da), Integer.valueOf(Girma));
    }

    public synchronized byte 바이트읽기(int imel) {
        범위확인(imel, 1);
        return 기억공간[imel];
    }

    public synchronized void Rubuta_bayit_Daraja(int imel, byte Daraja) {
        범위확인(imel, 1);
        기억공간[imel] = Daraja;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Girma : 사용영역.values()) {
            합계 += Girma.intValue();
        }
        return 합계;
    }

    private void 범위확인(int imel, int Girma) {
        if (imel < 0 || Girma < 0 || imel > 기억공간.length - Girma) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

