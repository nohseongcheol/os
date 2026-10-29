// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Тоҷикистон.JTjkOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 мос_кардан_қимат татбиқ_кардан_Захирагоҳ, нашр_Захирагоҳ, 병합을 담당한다. */
public final class ҳофиза_мудир {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public ҳофиза_мудир(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int татбиқ_кардан_Захирагоҳ(int андоза_кардан) {
        return 정렬할당(андоза_кардан, 1);
    }

    public synchronized int 정렬할당(int андоза_кардан, int мос_кардан_қимат) {
        if (андоза_кардан <= 0 || мос_кардан_қимат <= 0 || (мос_кардан_қимат & (мос_кардан_қимат - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ворида_қимат : 빈영역.entrySet()) {
            int порча = ворида_қимат.getKey().intValue();
            int 영역크기 = ворида_қимат.getValue().intValue();
            int 정렬시작 = (порча + мос_кардан_қимат - 1) & -мос_кардан_қимат;
            int 앞크기 = 정렬시작 - порча;
            int 끝크기 = 영역크기 - 앞크기 - андоза_кардан;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(порча));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(порча), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + андоза_кардан), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(андоза_кардан));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + андоза_кардан, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void нашр_Захирагоҳ(int суроға) {
        Integer андоза_кардан_объект = 사용영역.remove(Integer.valueOf(суроға));
        if (андоза_кардан_объект == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int порча = суроға;
        int андоза_кардан = андоза_кардан_объект.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(порча));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == порча) {
            порча = 앞.getKey().intValue();
            андоза_кардан += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Бозгашт_қимат = 빈영역.ceilingEntry(Integer.valueOf(порча));
        if (Бозгашт_қимат != null && порча + андоза_кардан == Бозгашт_қимат.getKey().intValue()) {
            андоза_кардан += Бозгашт_қимат.getValue().intValue();
            빈영역.remove(Бозгашт_қимат.getKey());
        }
        빈영역.put(Integer.valueOf(порча), Integer.valueOf(андоза_кардан));
    }

    public synchronized byte 바이트읽기(int суроға) {
        범위확인(суроға, 1);
        return 기억공간[суроға];
    }

    public synchronized void навиштан_байт_қимат(int суроға, byte қимат) {
        범위확인(суроға, 1);
        기억공간[суроға] = қимат;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer андоза_кардан : 사용영역.values()) {
            합계 += андоза_кардан.intValue();
        }
        return 합계;
    }

    private void 범위확인(int суроға, int андоза_кардан) {
        if (суроға < 0 || андоза_кардан < 0 || суроға > 기억공간.length - андоза_кардан) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

