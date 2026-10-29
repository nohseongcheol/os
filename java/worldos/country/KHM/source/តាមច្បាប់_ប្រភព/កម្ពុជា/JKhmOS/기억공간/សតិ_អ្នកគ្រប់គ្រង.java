// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 តំរឹម_តំលៃ លៃទុក_ការផ្ទុក, លែង_ការផ្ទុក, 병합을 담당한다. */
public final class សតិ_អ្នកគ្រប់គ្រង {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public សតិ_អ្នកគ្រប់គ្រង(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int លៃទុក_ការផ្ទុក(int ដាក់ទំហំ) {
        return 정렬할당(ដាក់ទំហំ, 1);
    }

    public synchronized int 정렬할당(int ដាក់ទំហំ, int តំរឹម_តំលៃ) {
        if (ដាក់ទំហំ <= 0 || តំរឹម_តំលៃ <= 0 || (តំរឹម_តំលៃ & (តំរឹម_តំលៃ - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ការបញ្ចូល_តំលៃ : 빈영역.entrySet()) {
            int រត់ = ការបញ្ចូល_តំលៃ.getKey().intValue();
            int 영역크기 = ការបញ្ចូល_តំលៃ.getValue().intValue();
            int 정렬시작 = (រត់ + តំរឹម_តំលៃ - 1) & -តំរឹម_តំលៃ;
            int ខាងមុខ_តំលៃ_ដាក់ទំហំ = 정렬시작 - រត់;
            int 끝크기 = 영역크기 - ខាងមុខ_តំលៃ_ដាក់ទំហំ - ដាក់ទំហំ;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(រត់));
            if (ខាងមុខ_តំលៃ_ដាក់ទំហំ > 0) {
                빈영역.put(Integer.valueOf(រត់), Integer.valueOf(ខាងមុខ_តំលៃ_ដាក់ទំហំ));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + ដាក់ទំហំ), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(ដាក់ទំហំ));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + ដាក់ទំហំ, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void លែង_ការផ្ទុក(int អ៊ីម៉ែល) {
        Integer ដាក់ទំហំ_វត្ថុ = 사용영역.remove(Integer.valueOf(អ៊ីម៉ែល));
        if (ដាក់ទំហំ_វត្ថុ == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int រត់ = អ៊ីម៉ែល;
        int ដាក់ទំហំ = ដាក់ទំហំ_វត្ថុ.intValue();
        Map.Entry<Integer, Integer> ខាងមុខ_តំលៃ = 빈영역.lowerEntry(Integer.valueOf(រត់));
        if (ខាងមុខ_តំលៃ != null && ខាងមុខ_តំលៃ.getKey().intValue() + ខាងមុខ_តំលៃ.getValue().intValue() == រត់) {
            រត់ = ខាងមុខ_តំលៃ.getKey().intValue();
            ដាក់ទំហំ += ខាងមុខ_តំលៃ.getValue().intValue();
            빈영역.remove(ខាងមុខ_តំលៃ.getKey());
        }
        Map.Entry<Integer, Integer> ការថយ_តំលៃ = 빈영역.ceilingEntry(Integer.valueOf(រត់));
        if (ការថយ_តំលៃ != null && រត់ + ដាក់ទំហំ == ការថយ_តំលៃ.getKey().intValue()) {
            ដាក់ទំហំ += ការថយ_តំលៃ.getValue().intValue();
            빈영역.remove(ការថយ_តំលៃ.getKey());
        }
        빈영역.put(Integer.valueOf(រត់), Integer.valueOf(ដាក់ទំហំ));
    }

    public synchronized byte 바이트읽기(int អ៊ីម៉ែល) {
        범위확인(អ៊ីម៉ែល, 1);
        return 기억공간[អ៊ីម៉ែល];
    }

    public synchronized void សរសេរ_បៃ_តំលៃ(int អ៊ីម៉ែល, byte តំលៃ) {
        범위확인(អ៊ីម៉ែល, 1);
        기억공간[អ៊ីម៉ែល] = តំលៃ;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer ដាក់ទំហំ : 사용영역.values()) {
            합계 += ដាក់ទំហំ.intValue();
        }
        return 합계;
    }

    private void 범위확인(int អ៊ីម៉ែល, int ដាក់ទំហំ) {
        if (អ៊ីម៉ែល < 0 || ដាក់ទំហំ < 0 || អ៊ីម៉ែល > 기억공간.length - ដាក់ទំហំ) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

