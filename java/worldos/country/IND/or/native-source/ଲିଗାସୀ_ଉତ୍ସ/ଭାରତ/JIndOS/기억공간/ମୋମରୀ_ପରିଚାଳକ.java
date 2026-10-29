// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 ଶ୍ରେଣୀବଦ୍ଧ_ମୂଲ୍ୟ ବଣ୍ଟନ_ଷ୍ଟୋରେଜ୍, ରିଲିଜ୍_ଷ୍ଟୋରେଜ୍, 병합을 담당한다. */
public final class ମୋମରୀ_ପରିଚାଳକ {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public ମୋମରୀ_ପରିଚାଳକ(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int ବଣ୍ଟନ_ଷ୍ଟୋରେଜ୍(int ଆକାର) {
        return 정렬할당(ଆକାର, 1);
    }

    public synchronized int 정렬할당(int ଆକାର, int ଶ୍ରେଣୀବଦ୍ଧ_ମୂଲ୍ୟ) {
        if (ଆକାର <= 0 || ଶ୍ରେଣୀବଦ୍ଧ_ମୂଲ୍ୟ <= 0 || (ଶ୍ରେଣୀବଦ୍ଧ_ମୂଲ୍ୟ & (ଶ୍ରେଣୀବଦ୍ଧ_ମୂଲ୍ୟ - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ : 빈영역.entrySet()) {
            int ଚଳାନ୍ତୁ = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.getKey().intValue();
            int 영역크기 = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.getValue().intValue();
            int 정렬시작 = (ଚଳାନ୍ତୁ + ଶ୍ରେଣୀବଦ୍ଧ_ମୂଲ୍ୟ - 1) & -ଶ୍ରେଣୀବଦ୍ଧ_ମୂଲ୍ୟ;
            int 앞크기 = 정렬시작 - ଚଳାନ୍ତୁ;
            int 끝크기 = 영역크기 - 앞크기 - ଆକାର;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(ଚଳାନ୍ତୁ));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(ଚଳାନ୍ତୁ), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + ଆକାର), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(ଆକାର));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + ଆକାର, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void ରିଲିଜ୍_ଷ୍ଟୋରେଜ୍(int ଠିକଣା) {
        Integer ଅକାର_ଅବଜେକ୍ଟ = 사용영역.remove(Integer.valueOf(ଠିକଣା));
        if (ଅକାର_ଅବଜେକ୍ଟ == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ଚଳାନ୍ତୁ = ଠିକଣା;
        int ଆକାର = ଅକାର_ଅବଜେକ୍ଟ.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(ଚଳାନ୍ତୁ));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == ଚଳାନ୍ତୁ) {
            ଚଳାନ୍ତୁ = 앞.getKey().intValue();
            ଆକାର += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> ପଛ_ମୂଲ୍ୟ = 빈영역.ceilingEntry(Integer.valueOf(ଚଳାନ୍ତୁ));
        if (ପଛ_ମୂଲ୍ୟ != null && ଚଳାନ୍ତୁ + ଆକାର == ପଛ_ମୂଲ୍ୟ.getKey().intValue()) {
            ଆକାର += ପଛ_ମୂଲ୍ୟ.getValue().intValue();
            빈영역.remove(ପଛ_ମୂଲ୍ୟ.getKey());
        }
        빈영역.put(Integer.valueOf(ଚଳାନ୍ତୁ), Integer.valueOf(ଆକାର));
    }

    public synchronized byte 바이트읽기(int ଠିକଣା) {
        범위확인(ଠିକଣା, 1);
        return 기억공간[ଠିକଣା];
    }

    public synchronized void ଲିଖନ_ବାଇଟ୍_ମୂଲ୍ୟ(int ଠିକଣା, byte ମୂଲ୍ୟ) {
        범위확인(ଠିକଣା, 1);
        기억공간[ଠିକଣା] = ମୂଲ୍ୟ;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer ଆକାର : 사용영역.values()) {
            합계 += ଆକାର.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ଠିକଣା, int ଆକାର) {
        if (ଠିକଣା < 0 || ଆକାର < 0 || ଠିକଣା > 기억공간.length - ଆକାର) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

