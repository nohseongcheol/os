// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 stilla_VALUE úthluta_geymsla, losa_geymsla, 병합을 담당한다. */
public final class Minni_stjórnandi {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Minni_stjórnandi(int samtala_breyta_stærð) {
        if (samtala_breyta_stærð < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[samtala_breyta_stærð];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(samtala_breyta_stærð - 4096));
    }

    public synchronized int úthluta_geymsla(int Stærð) {
        return 정렬할당(Stærð, 1);
    }

    public synchronized int 정렬할당(int Stærð, int stilla_VALUE) {
        if (Stærð <= 0 || stilla_VALUE <= 0 || (stilla_VALUE & (stilla_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> færsla_VALUE : 빈영역.entrySet()) {
            int Keyra_2 = færsla_VALUE.getKey().intValue();
            int 영역크기 = færsla_VALUE.getValue().intValue();
            int 정렬시작 = (Keyra_2 + stilla_VALUE - 1) & -stilla_VALUE;
            int myndavél_að_framan_VALUE_breyta_stærð = 정렬시작 - Keyra_2;
            int 끝크기 = 영역크기 - myndavél_að_framan_VALUE_breyta_stærð - Stærð;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Keyra_2));
            if (myndavél_að_framan_VALUE_breyta_stærð > 0) {
                빈영역.put(Integer.valueOf(Keyra_2), Integer.valueOf(myndavél_að_framan_VALUE_breyta_stærð));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Stærð), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Stærð));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Stærð, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void losa_geymsla(int slóð) {
        Integer breyta_stærð_hlutur = 사용영역.remove(Integer.valueOf(slóð));
        if (breyta_stærð_hlutur == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Keyra_2 = slóð;
        int Stærð = breyta_stærð_hlutur.intValue();
        Map.Entry<Integer, Integer> myndavél_að_framan_VALUE = 빈영역.lowerEntry(Integer.valueOf(Keyra_2));
        if (myndavél_að_framan_VALUE != null && myndavél_að_framan_VALUE.getKey().intValue() + myndavél_að_framan_VALUE.getValue().intValue() == Keyra_2) {
            Keyra_2 = myndavél_að_framan_VALUE.getKey().intValue();
            Stærð += myndavél_að_framan_VALUE.getValue().intValue();
            빈영역.remove(myndavél_að_framan_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> TIL_BAKA_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Keyra_2));
        if (TIL_BAKA_VALUE != null && Keyra_2 + Stærð == TIL_BAKA_VALUE.getKey().intValue()) {
            Stærð += TIL_BAKA_VALUE.getValue().intValue();
            빈영역.remove(TIL_BAKA_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Keyra_2), Integer.valueOf(Stærð));
    }

    public synchronized byte 바이트읽기(int slóð) {
        범위확인(slóð, 1);
        return 기억공간[slóð];
    }

    public synchronized void skrifa_bæti_VALUE(int slóð, byte VALUE) {
        범위확인(slóð, 1);
        기억공간[slóð] = VALUE;
    }

    public synchronized int samtala_breyta_stærð() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int samtala_VALUE = 0;
        for (Integer Stærð : 사용영역.values()) {
            samtala_VALUE += Stærð.intValue();
        }
        return samtala_VALUE;
    }

    private void 범위확인(int slóð, int Stærð) {
        if (slóð < 0 || Stærð < 0 || slóð > 기억공간.length - Stærð) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

