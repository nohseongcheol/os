// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عێراق.JIrqOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 لاچن_کردن_نرخ تەرخانکردن_هەمارگە, وەشان_هەمارگە, 병합을 담당한다. */
public final class بیرگە_بەڕێوەبەر {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public بیرگە_بەڕێوەبەر(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int تەرخانکردن_هەمارگە(int گۆڕینی_ئەندازە) {
        return 정렬할당(گۆڕینی_ئەندازە, 1);
    }

    public synchronized int 정렬할당(int گۆڕینی_ئەندازە, int لاچن_کردن_نرخ) {
        if (گۆڕینی_ئەندازە <= 0 || لاچن_کردن_نرخ <= 0 || (لاچن_کردن_نرخ & (لاچن_کردن_نرخ - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> تێنووسین_نرخ : 빈영역.entrySet()) {
            int ڕادان = تێنووسین_نرخ.getKey().intValue();
            int 영역크기 = تێنووسین_نرخ.getValue().intValue();
            int 정렬시작 = (ڕادان + لاچن_کردن_نرخ - 1) & -لاچن_کردن_نرخ;
            int 앞크기 = 정렬시작 - ڕادان;
            int 끝크기 = 영역크기 - 앞크기 - گۆڕینی_ئەندازە;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(ڕادان));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(ڕادان), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + گۆڕینی_ئەندازە), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(گۆڕینی_ئەندازە));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + گۆڕینی_ئەندازە, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void وەشان_هەمارگە(int ناونیشان) {
        Integer گۆڕینی_ئەندازە_شت = 사용영역.remove(Integer.valueOf(ناونیشان));
        if (گۆڕینی_ئەندازە_شت == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ڕادان = ناونیشان;
        int گۆڕینی_ئەندازە = گۆڕینی_ئەندازە_شت.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(ڕادان));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == ڕادان) {
            ڕادان = 앞.getKey().intValue();
            گۆڕینی_ئەندازە += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> دواوە_نرخ = 빈영역.ceilingEntry(Integer.valueOf(ڕادان));
        if (دواوە_نرخ != null && ڕادان + گۆڕینی_ئەندازە == دواوە_نرخ.getKey().intValue()) {
            گۆڕینی_ئەندازە += دواوە_نرخ.getValue().intValue();
            빈영역.remove(دواوە_نرخ.getKey());
        }
        빈영역.put(Integer.valueOf(ڕادان), Integer.valueOf(گۆڕینی_ئەندازە));
    }

    public synchronized byte 바이트읽기(int ناونیشان) {
        범위확인(ناونیشان, 1);
        return 기억공간[ناونیشان];
    }

    public synchronized void ڕایت_کردن_بایت_نرخ(int ناونیشان, byte نرخ) {
        범위확인(ناونیشان, 1);
        기억공간[ناونیشان] = نرخ;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer گۆڕینی_ئەندازە : 사용영역.values()) {
            합계 += گۆڕینی_ئەندازە.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ناونیشان, int گۆڕینی_ئەندازە) {
        if (ناونیشان < 0 || گۆڕینی_ئەندازە < 0 || ناونیشان > 기억공간.length - گۆڕینی_ئەندازە) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

