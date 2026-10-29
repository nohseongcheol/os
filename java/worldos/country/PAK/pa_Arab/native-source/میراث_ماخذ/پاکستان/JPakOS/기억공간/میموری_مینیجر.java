// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 سیدھا_قدر مختص_کرو_ذخیرہ, اجراء_ذخیرہ, 병합을 담당한다. */
public final class میموری_مینیجر {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public میموری_مینیجر(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int مختص_کرو_ذخیرہ(int سائز) {
        return 정렬할당(سائز, 1);
    }

    public synchronized int 정렬할당(int سائز, int سیدھا_قدر) {
        if (سائز <= 0 || سیدھا_قدر <= 0 || (سیدھا_قدر & (سیدھا_قدر - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> داخلہ_قدر : 빈영역.entrySet()) {
            int چلاؤ = داخلہ_قدر.getKey().intValue();
            int 영역크기 = داخلہ_قدر.getValue().intValue();
            int 정렬시작 = (چلاؤ + سیدھا_قدر - 1) & -سیدھا_قدر;
            int 앞크기 = 정렬시작 - چلاؤ;
            int 끝크기 = 영역크기 - 앞크기 - سائز;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(چلاؤ));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(چلاؤ), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + سائز), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(سائز));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + سائز, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void اجراء_ذخیرہ(int پتا) {
        Integer سائز_آبجیکٹ = 사용영역.remove(Integer.valueOf(پتا));
        if (سائز_آبجیکٹ == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int چلاؤ = پتا;
        int سائز = سائز_آبجیکٹ.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(چلاؤ));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == چلاؤ) {
            چلاؤ = 앞.getKey().intValue();
            سائز += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> پیچھے_قدر = 빈영역.ceilingEntry(Integer.valueOf(چلاؤ));
        if (پیچھے_قدر != null && چلاؤ + سائز == پیچھے_قدر.getKey().intValue()) {
            سائز += پیچھے_قدر.getValue().intValue();
            빈영역.remove(پیچھے_قدر.getKey());
        }
        빈영역.put(Integer.valueOf(چلاؤ), Integer.valueOf(سائز));
    }

    public synchronized byte 바이트읽기(int پتا) {
        범위확인(پتا, 1);
        return 기억공간[پتا];
    }

    public synchronized void لکھو_بائٹ_قدر(int پتا, byte قدر) {
        범위확인(پتا, 1);
        기억공간[پتا] = قدر;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer سائز : 사용영역.values()) {
            합계 += سائز.intValue();
        }
        return 합계;
    }

    private void 범위확인(int پتا, int سائز) {
        if (پتا < 0 || سائز < 0 || پتا > 기억공간.length - سائز) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

