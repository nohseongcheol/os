// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਭਾਰਤ.JIndOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 ਸੇਧਬੰਦ_ਕਰੋ_ਕੀਮਤ ਨਿਰਧਾਰਿਤ_ਕਰੋ_ਸਟੋਰੇਜ, ਰਿਲੀਜ_ਸਟੋਰੇਜ, 병합을 담당한다. */
public final class ਮੈਮਰੀ_ਪ੍ਰਬੰਧਕ {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public ਮੈਮਰੀ_ਪ੍ਰਬੰਧਕ(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int ਨਿਰਧਾਰਿਤ_ਕਰੋ_ਸਟੋਰੇਜ(int ਆਕਾਰ) {
        return 정렬할당(ਆਕਾਰ, 1);
    }

    public synchronized int 정렬할당(int ਆਕਾਰ, int ਸੇਧਬੰਦ_ਕਰੋ_ਕੀਮਤ) {
        if (ਆਕਾਰ <= 0 || ਸੇਧਬੰਦ_ਕਰੋ_ਕੀਮਤ <= 0 || (ਸੇਧਬੰਦ_ਕਰੋ_ਕੀਮਤ & (ਸੇਧਬੰਦ_ਕਰੋ_ਕੀਮਤ - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ਦਾਖਲਾ_ਕੀਮਤ : 빈영역.entrySet()) {
            int ਚਲਾਓ_2 = ਦਾਖਲਾ_ਕੀਮਤ.getKey().intValue();
            int 영역크기 = ਦਾਖਲਾ_ਕੀਮਤ.getValue().intValue();
            int 정렬시작 = (ਚਲਾਓ_2 + ਸੇਧਬੰਦ_ਕਰੋ_ਕੀਮਤ - 1) & -ਸੇਧਬੰਦ_ਕਰੋ_ਕੀਮਤ;
            int 앞크기 = 정렬시작 - ਚਲਾਓ_2;
            int 끝크기 = 영역크기 - 앞크기 - ਆਕਾਰ;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(ਚਲਾਓ_2));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(ਚਲਾਓ_2), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + ਆਕਾਰ), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(ਆਕਾਰ));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + ਆਕਾਰ, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void ਰਿਲੀਜ_ਸਟੋਰੇਜ(int ਪਤਾ) {
        Integer ਆਕਾਰ_ਔਬਜੈਕਟ = 사용영역.remove(Integer.valueOf(ਪਤਾ));
        if (ਆਕਾਰ_ਔਬਜੈਕਟ == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ਚਲਾਓ_2 = ਪਤਾ;
        int ਆਕਾਰ = ਆਕਾਰ_ਔਬਜੈਕਟ.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(ਚਲਾਓ_2));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == ਚਲਾਓ_2) {
            ਚਲਾਓ_2 = 앞.getKey().intValue();
            ਆਕਾਰ += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> ਪਿਛਲਾ_ਕੀਮਤ = 빈영역.ceilingEntry(Integer.valueOf(ਚਲਾਓ_2));
        if (ਪਿਛਲਾ_ਕੀਮਤ != null && ਚਲਾਓ_2 + ਆਕਾਰ == ਪਿਛਲਾ_ਕੀਮਤ.getKey().intValue()) {
            ਆਕਾਰ += ਪਿਛਲਾ_ਕੀਮਤ.getValue().intValue();
            빈영역.remove(ਪਿਛਲਾ_ਕੀਮਤ.getKey());
        }
        빈영역.put(Integer.valueOf(ਚਲਾਓ_2), Integer.valueOf(ਆਕਾਰ));
    }

    public synchronized byte 바이트읽기(int ਪਤਾ) {
        범위확인(ਪਤਾ, 1);
        return 기억공간[ਪਤਾ];
    }

    public synchronized void ਲਿੱਖੋ_ਬਾਈਟ_ਕੀਮਤ(int ਪਤਾ, byte ਕੀਮਤ) {
        범위확인(ਪਤਾ, 1);
        기억공간[ਪਤਾ] = ਕੀਮਤ;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer ਆਕਾਰ : 사용영역.values()) {
            합계 += ਆਕਾਰ.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ਪਤਾ, int ਆਕਾਰ) {
        if (ਪਤਾ < 0 || ਆਕਾਰ < 0 || ਪਤਾ > 기억공간.length - ਆਕਾਰ) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

