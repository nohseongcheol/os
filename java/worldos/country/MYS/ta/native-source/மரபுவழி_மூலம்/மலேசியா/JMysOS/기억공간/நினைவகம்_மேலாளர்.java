// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package மலேசியா.JMysOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 சீரமை_மதிப்பு ஒதுக்கிடு_சேமிப்பகம், அனுப்பு_சேமிப்பகம், 병합을 담당한다. */
public final class நினைவகம்_மேலாளர் {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public நினைவகம்_மேலாளர்(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int ஒதுக்கிடு_சேமிப்பகம்(int அளவு) {
        return 정렬할당(அளவு, 1);
    }

    public synchronized int 정렬할당(int அளவு, int சீரமை_மதிப்பு) {
        if (அளவு <= 0 || சீரமை_மதிப்பு <= 0 || (சீரமை_மதிப்பு & (சீரமை_மதிப்பு - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> உள்ளீடு_மதிப்பு : 빈영역.entrySet()) {
            int செயல்படுத்துக = உள்ளீடு_மதிப்பு.getKey().intValue();
            int 영역크기 = உள்ளீடு_மதிப்பு.getValue().intValue();
            int 정렬시작 = (செயல்படுத்துக + சீரமை_மதிப்பு - 1) & -சீரமை_மதிப்பு;
            int முன்_மதிப்பு_அளவு = 정렬시작 - செயல்படுத்துக;
            int 끝크기 = 영역크기 - முன்_மதிப்பு_அளவு - அளவு;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(செயல்படுத்துக));
            if (முன்_மதிப்பு_அளவு > 0) {
                빈영역.put(Integer.valueOf(செயல்படுத்துக), Integer.valueOf(முன்_மதிப்பு_அளவு));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + அளவு), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(அளவு));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + அளவு, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void அனுப்பு_சேமிப்பகம்(int முகவரி) {
        Integer அளவு_பொருள் = 사용영역.remove(Integer.valueOf(முகவரி));
        if (அளவு_பொருள் == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int செயல்படுத்துக = முகவரி;
        int அளவு = அளவு_பொருள்.intValue();
        Map.Entry<Integer, Integer> முன்_மதிப்பு = 빈영역.lowerEntry(Integer.valueOf(செயல்படுத்துக));
        if (முன்_மதிப்பு != null && முன்_மதிப்பு.getKey().intValue() + முன்_மதிப்பு.getValue().intValue() == செயல்படுத்துக) {
            செயல்படுத்துக = முன்_மதிப்பு.getKey().intValue();
            அளவு += முன்_மதிப்பு.getValue().intValue();
            빈영역.remove(முன்_மதிப்பு.getKey());
        }
        Map.Entry<Integer, Integer> பின்_மதிப்பு = 빈영역.ceilingEntry(Integer.valueOf(செயல்படுத்துக));
        if (பின்_மதிப்பு != null && செயல்படுத்துக + அளவு == பின்_மதிப்பு.getKey().intValue()) {
            அளவு += பின்_மதிப்பு.getValue().intValue();
            빈영역.remove(பின்_மதிப்பு.getKey());
        }
        빈영역.put(Integer.valueOf(செயல்படுத்துக), Integer.valueOf(அளவு));
    }

    public synchronized byte 바이트읽기(int முகவரி) {
        범위확인(முகவரி, 1);
        return 기억공간[முகவரி];
    }

    public synchronized void எழுது_பைட்_மதிப்பு(int முகவரி, byte மதிப்பு) {
        범위확인(முகவரி, 1);
        기억공간[முகவரி] = மதிப்பு;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer அளவு : 사용영역.values()) {
            합계 += அளவு.intValue();
        }
        return 합계;
    }

    private void 범위확인(int முகவரி, int அளவு) {
        if (முகவரி < 0 || அளவு < 0 || முகவரி > 기억공간.length - அளவு) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

