// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package યુનાઇટેડ_કિંગડમ.JGbrOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 સંરેખિત_કરો_મૂલ્ય ફાળવો_સંગ્રહ, રિલીઝ_સંગ્રહ, 병합을 담당한다. */
public final class મેમરી_પ્રબંધક {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public મેમરી_પ્રબંધક(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int ફાળવો_સંગ્રહ(int માપ) {
        return 정렬할당(માપ, 1);
    }

    public synchronized int 정렬할당(int માપ, int સંરેખિત_કરો_મૂલ્ય) {
        if (માપ <= 0 || સંરેખિત_કરો_મૂલ્ય <= 0 || (સંરેખિત_કરો_મૂલ્ય & (સંરેખિત_કરો_મૂલ્ય - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> પ્રવેશ_મૂલ્ય : 빈영역.entrySet()) {
            int ચલાવો_2 = પ્રવેશ_મૂલ્ય.getKey().intValue();
            int 영역크기 = પ્રવેશ_મૂલ્ય.getValue().intValue();
            int 정렬시작 = (ચલાવો_2 + સંરેખિત_કરો_મૂલ્ય - 1) & -સંરેખિત_કરો_મૂલ્ય;
            int 앞크기 = 정렬시작 - ચલાવો_2;
            int 끝크기 = 영역크기 - 앞크기 - માપ;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(ચલાવો_2));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(ચલાવો_2), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + માપ), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(માપ));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + માપ, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void રિલીઝ_સંગ્રહ(int સરનામું) {
        Integer આકાર_ઑબ્જેક્ટ = 사용영역.remove(Integer.valueOf(સરનામું));
        if (આકાર_ઑબ્જેક્ટ == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ચલાવો_2 = સરનામું;
        int માપ = આકાર_ઑબ્જેક્ટ.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(ચલાવો_2));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == ચલાવો_2) {
            ચલાવો_2 = 앞.getKey().intValue();
            માપ += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> બેક_મૂલ્ય = 빈영역.ceilingEntry(Integer.valueOf(ચલાવો_2));
        if (બેક_મૂલ્ય != null && ચલાવો_2 + માપ == બેક_મૂલ્ય.getKey().intValue()) {
            માપ += બેક_મૂલ્ય.getValue().intValue();
            빈영역.remove(બેક_મૂલ્ય.getKey());
        }
        빈영역.put(Integer.valueOf(ચલાવો_2), Integer.valueOf(માપ));
    }

    public synchronized byte 바이트읽기(int સરનામું) {
        범위확인(સરનામું, 1);
        return 기억공간[સરનામું];
    }

    public synchronized void લખો_બાઇટ_મૂલ્ય(int સરનામું, byte મૂલ્ય) {
        범위확인(સરનામું, 1);
        기억공간[સરનામું] = મૂલ્ય;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer માપ : 사용영역.values()) {
            합계 += માપ.intValue();
        }
        return 합계;
    }

    private void 범위확인(int સરનામું, int માપ) {
        if (સરનામું < 0 || માપ < 0 || સરનામું > 기억공간.length - માપ) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

