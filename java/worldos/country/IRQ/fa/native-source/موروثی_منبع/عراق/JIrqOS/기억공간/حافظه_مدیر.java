// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عراق.JIrqOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 تراز_کردن_مقدار اختصاص_دادن_حافظه_تلفن, انتشار_حافظه_تلفن, 병합을 담당한다. */
public final class حافظه_مدیر {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public حافظه_مدیر(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int اختصاص_دادن_حافظه_تلفن(int اندازه) {
        return 정렬할당(اندازه, 1);
    }

    public synchronized int 정렬할당(int اندازه, int تراز_کردن_مقدار) {
        if (اندازه <= 0 || تراز_کردن_مقدار <= 0 || (تراز_کردن_مقدار & (تراز_کردن_مقدار - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ورودی_مقدار : 빈영역.entrySet()) {
            int اجرا_2 = ورودی_مقدار.getKey().intValue();
            int 영역크기 = ورودی_مقدار.getValue().intValue();
            int 정렬시작 = (اجرا_2 + تراز_کردن_مقدار - 1) & -تراز_کردن_مقدار;
            int جلو_مقدار_اندازه_کردن = 정렬시작 - اجرا_2;
            int 끝크기 = 영역크기 - جلو_مقدار_اندازه_کردن - اندازه;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(اجرا_2));
            if (جلو_مقدار_اندازه_کردن > 0) {
                빈영역.put(Integer.valueOf(اجرا_2), Integer.valueOf(جلو_مقدار_اندازه_کردن));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + اندازه), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(اندازه));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + اندازه, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void انتشار_حافظه_تلفن(int آدرس) {
        Integer اندازه_کردن_شئ = 사용영역.remove(Integer.valueOf(آدرس));
        if (اندازه_کردن_شئ == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int اجرا_2 = آدرس;
        int اندازه = اندازه_کردن_شئ.intValue();
        Map.Entry<Integer, Integer> جلو_مقدار = 빈영역.lowerEntry(Integer.valueOf(اجرا_2));
        if (جلو_مقدار != null && جلو_مقدار.getKey().intValue() + جلو_مقدار.getValue().intValue() == اجرا_2) {
            اجرا_2 = جلو_مقدار.getKey().intValue();
            اندازه += جلو_مقدار.getValue().intValue();
            빈영역.remove(جلو_مقدار.getKey());
        }
        Map.Entry<Integer, Integer> برگشت_مقدار = 빈영역.ceilingEntry(Integer.valueOf(اجرا_2));
        if (برگشت_مقدار != null && اجرا_2 + اندازه == برگشت_مقدار.getKey().intValue()) {
            اندازه += برگشت_مقدار.getValue().intValue();
            빈영역.remove(برگشت_مقدار.getKey());
        }
        빈영역.put(Integer.valueOf(اجرا_2), Integer.valueOf(اندازه));
    }

    public synchronized byte 바이트읽기(int آدرس) {
        범위확인(آدرس, 1);
        return 기억공간[آدرس];
    }

    public synchronized void نوشتن_بایت_مقدار(int آدرس, byte مقدار) {
        범위확인(آدرس, 1);
        기억공간[آدرس] = مقدار;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer اندازه : 사용영역.values()) {
            합계 += اندازه.intValue();
        }
        return 합계;
    }

    private void 범위확인(int آدرس, int اندازه) {
        if (آدرس < 0 || اندازه < 0 || آدرس > 기억공간.length - اندازه) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

