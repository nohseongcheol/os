// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package U_Rwanda.JRwaOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 gutondeka_agaciro kugenera_Ububiko, kurekura_Ububiko, 병합을 담당한다. */
public final class ububiko_Umugenzuzi {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public ububiko_Umugenzuzi(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int kugenera_Ububiko(int Ingano) {
        return 정렬할당(Ingano, 1);
    }

    public synchronized int 정렬할당(int Ingano, int gutondeka_agaciro) {
        if (Ingano <= 0 || gutondeka_agaciro <= 0 || (gutondeka_agaciro & (gutondeka_agaciro - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> icyinjizwa_agaciro : 빈영역.entrySet()) {
            int ihuriro = icyinjizwa_agaciro.getKey().intValue();
            int 영역크기 = icyinjizwa_agaciro.getValue().intValue();
            int 정렬시작 = (ihuriro + gutondeka_agaciro - 1) & -gutondeka_agaciro;
            int 앞크기 = 정렬시작 - ihuriro;
            int 끝크기 = 영역크기 - 앞크기 - Ingano;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(ihuriro));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(ihuriro), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Ingano), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Ingano));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Ingano, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void kurekura_Ububiko(int aderesi) {
        Integer ingano_ikintu = 사용영역.remove(Integer.valueOf(aderesi));
        if (ingano_ikintu == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ihuriro = aderesi;
        int Ingano = ingano_ikintu.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(ihuriro));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == ihuriro) {
            ihuriro = 앞.getKey().intValue();
            Ingano += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Ikibanza_agaciro = 빈영역.ceilingEntry(Integer.valueOf(ihuriro));
        if (Ikibanza_agaciro != null && ihuriro + Ingano == Ikibanza_agaciro.getKey().intValue()) {
            Ingano += Ikibanza_agaciro.getValue().intValue();
            빈영역.remove(Ikibanza_agaciro.getKey());
        }
        빈영역.put(Integer.valueOf(ihuriro), Integer.valueOf(Ingano));
    }

    public synchronized byte 바이트읽기(int aderesi) {
        범위확인(aderesi, 1);
        return 기억공간[aderesi];
    }

    public synchronized void kwandika_bayiti_agaciro(int aderesi, byte agaciro) {
        범위확인(aderesi, 1);
        기억공간[aderesi] = agaciro;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Ingano : 사용영역.values()) {
            합계 += Ingano.intValue();
        }
        return 합계;
    }

    private void 범위확인(int aderesi, int Ingano) {
        if (aderesi < 0 || Ingano < 0 || aderesi > 기억공간.length - Ingano) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

