// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package افغانستان.JAfgOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 پرليکول_ارزښت 할당, 해제, 병합을 담당한다. */
public final class 기억공간관리자 {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public 기억공간관리자(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int 할당(int کچ) {
        return 정렬할당(کچ, 1);
    }

    public synchronized int 정렬할당(int کچ, int پرليکول_ارزښت) {
        if (کچ <= 0 || پرليکول_ارزښت <= 0 || (پرليکول_ارزښت & (پرليکول_ارزښت - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ننوت_ارزښت : 빈영역.entrySet()) {
            int ځغلول = ننوت_ارزښت.getKey().intValue();
            int 영역크기 = ننوت_ارزښت.getValue().intValue();
            int 정렬시작 = (ځغلول + پرليکول_ارزښت - 1) & -پرليکول_ارزښت;
            int 앞크기 = 정렬시작 - ځغلول;
            int 끝크기 = 영역크기 - 앞크기 - کچ;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(ځغلول));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(ځغلول), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + کچ), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(کچ));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + کچ, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void 해제(int پته) {
        Integer 크기객체 = 사용영역.remove(Integer.valueOf(پته));
        if (크기객체 == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ځغلول = پته;
        int کچ = 크기객체.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(ځغلول));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == ځغلول) {
            ځغلول = 앞.getKey().intValue();
            کچ += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> 뒤 = 빈영역.ceilingEntry(Integer.valueOf(ځغلول));
        if (뒤 != null && ځغلول + کچ == 뒤.getKey().intValue()) {
            کچ += 뒤.getValue().intValue();
            빈영역.remove(뒤.getKey());
        }
        빈영역.put(Integer.valueOf(ځغلول), Integer.valueOf(کچ));
    }

    public synchronized byte 바이트읽기(int پته) {
        범위확인(پته, 1);
        return 기억공간[پته];
    }

    public synchronized void ليکل_بايټ_ارزښت(int پته, byte ارزښت) {
        범위확인(پته, 1);
        기억공간[پته] = ارزښت;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer کچ : 사용영역.values()) {
            합계 += کچ.intValue();
        }
        return 합계;
    }

    private void 범위확인(int پته, int کچ) {
        if (پته < 0 || کچ < 0 || پته > 기억공간.length - کچ) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

