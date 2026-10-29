// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 ಒಗ್ಗೂಡಿಸಿ_ಮೌಲ್ಯ ವಿತರಿಸು_ಸಂಗ್ರಹ, ಬಿಡುಗಡೆ_ಸಂಗ್ರಹ, 병합을 담당한다. */
public final class ಮೆಮೊರಿ_ವ್ಯವಸ್ಥಾಪಕ {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public ಮೆಮೊರಿ_ವ್ಯವಸ್ಥಾಪಕ(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int ವಿತರಿಸು_ಸಂಗ್ರಹ(int ಗಾತ್ರ) {
        return 정렬할당(ಗಾತ್ರ, 1);
    }

    public synchronized int 정렬할당(int ಗಾತ್ರ, int ಒಗ್ಗೂಡಿಸಿ_ಮೌಲ್ಯ) {
        if (ಗಾತ್ರ <= 0 || ಒಗ್ಗೂಡಿಸಿ_ಮೌಲ್ಯ <= 0 || (ಒಗ್ಗೂಡಿಸಿ_ಮೌಲ್ಯ & (ಒಗ್ಗೂಡಿಸಿ_ಮೌಲ್ಯ - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ನಮೂದು_ಮೌಲ್ಯ : 빈영역.entrySet()) {
            int ಚಲಾಯಿಸು_2 = ನಮೂದು_ಮೌಲ್ಯ.getKey().intValue();
            int 영역크기 = ನಮೂದು_ಮೌಲ್ಯ.getValue().intValue();
            int 정렬시작 = (ಚಲಾಯಿಸು_2 + ಒಗ್ಗೂಡಿಸಿ_ಮೌಲ್ಯ - 1) & -ಒಗ್ಗೂಡಿಸಿ_ಮೌಲ್ಯ;
            int ಮುಂದೆ_ಮೌಲ್ಯ_ಗಾತ್ರಿಸು = 정렬시작 - ಚಲಾಯಿಸು_2;
            int 끝크기 = 영역크기 - ಮುಂದೆ_ಮೌಲ್ಯ_ಗಾತ್ರಿಸು - ಗಾತ್ರ;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(ಚಲಾಯಿಸು_2));
            if (ಮುಂದೆ_ಮೌಲ್ಯ_ಗಾತ್ರಿಸು > 0) {
                빈영역.put(Integer.valueOf(ಚಲಾಯಿಸು_2), Integer.valueOf(ಮುಂದೆ_ಮೌಲ್ಯ_ಗಾತ್ರಿಸು));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + ಗಾತ್ರ), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(ಗಾತ್ರ));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + ಗಾತ್ರ, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void ಬಿಡುಗಡೆ_ಸಂಗ್ರಹ(int ಇಮೇಲ್) {
        Integer ಗಾತ್ರಿಸು_ಆಬ್ಜೆಕ್ಟ್ = 사용영역.remove(Integer.valueOf(ಇಮೇಲ್));
        if (ಗಾತ್ರಿಸು_ಆಬ್ಜೆಕ್ಟ್ == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ಚಲಾಯಿಸು_2 = ಇಮೇಲ್;
        int ಗಾತ್ರ = ಗಾತ್ರಿಸು_ಆಬ್ಜೆಕ್ಟ್.intValue();
        Map.Entry<Integer, Integer> ಮುಂದೆ_ಮೌಲ್ಯ = 빈영역.lowerEntry(Integer.valueOf(ಚಲಾಯಿಸು_2));
        if (ಮುಂದೆ_ಮೌಲ್ಯ != null && ಮುಂದೆ_ಮೌಲ್ಯ.getKey().intValue() + ಮುಂದೆ_ಮೌಲ್ಯ.getValue().intValue() == ಚಲಾಯಿಸು_2) {
            ಚಲಾಯಿಸು_2 = ಮುಂದೆ_ಮೌಲ್ಯ.getKey().intValue();
            ಗಾತ್ರ += ಮುಂದೆ_ಮೌಲ್ಯ.getValue().intValue();
            빈영역.remove(ಮುಂದೆ_ಮೌಲ್ಯ.getKey());
        }
        Map.Entry<Integer, Integer> ಹಿಂದೆ_ಮೌಲ್ಯ = 빈영역.ceilingEntry(Integer.valueOf(ಚಲಾಯಿಸು_2));
        if (ಹಿಂದೆ_ಮೌಲ್ಯ != null && ಚಲಾಯಿಸು_2 + ಗಾತ್ರ == ಹಿಂದೆ_ಮೌಲ್ಯ.getKey().intValue()) {
            ಗಾತ್ರ += ಹಿಂದೆ_ಮೌಲ್ಯ.getValue().intValue();
            빈영역.remove(ಹಿಂದೆ_ಮೌಲ್ಯ.getKey());
        }
        빈영역.put(Integer.valueOf(ಚಲಾಯಿಸು_2), Integer.valueOf(ಗಾತ್ರ));
    }

    public synchronized byte 바이트읽기(int ಇಮೇಲ್) {
        범위확인(ಇಮೇಲ್, 1);
        return 기억공간[ಇಮೇಲ್];
    }

    public synchronized void ಬರೆ_ಬೈಟ್_ಮೌಲ್ಯ(int ಇಮೇಲ್, byte ಮೌಲ್ಯ) {
        범위확인(ಇಮೇಲ್, 1);
        기억공간[ಇಮೇಲ್] = ಮೌಲ್ಯ;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer ಗಾತ್ರ : 사용영역.values()) {
            합계 += ಗಾತ್ರ.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ಇಮೇಲ್, int ಗಾತ್ರ) {
        if (ಇಮೇಲ್ < 0 || ಗಾತ್ರ < 0 || ಇಮೇಲ್ > 기억공간.length - ಗಾತ್ರ) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

