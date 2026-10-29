// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package إريتريا.JEriOS.ذاكرة_منطقة;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 يحاذي_قيمة يخصص_تخزين, إصدار_تخزين, 병합을 담당한다. */
public final class ذاكرة_مدير {
    private final byte[] ذاكرة_منطقة;
    private final TreeMap<Integer, Integer> فارغ_منطقة = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public ذاكرة_مدير(int إجمالي_يغير_الحجم) {
        if (إجمالي_يغير_الحجم < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        ذاكرة_منطقة = new byte[إجمالي_يغير_الحجم];
        فارغ_منطقة.put(Integer.valueOf(4096), Integer.valueOf(إجمالي_يغير_الحجم - 4096));
    }

    public synchronized int يخصص_تخزين(int حجم) {
        return 정렬할당(حجم, 1);
    }

    public synchronized int 정렬할당(int حجم, int يحاذي_قيمة) {
        if (حجم <= 0 || يحاذي_قيمة <= 0 || (يحاذي_قيمة & (يحاذي_قيمة - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> إدخال_قيمة_962f286b : فارغ_منطقة.entrySet()) {
            int تشغيل = إدخال_قيمة_962f286b.getKey().intValue();
            int منطقة_يغير_الحجم = إدخال_قيمة_962f286b.getValue().intValue();
            int 정렬시작 = (تشغيل + يحاذي_قيمة - 1) & -يحاذي_قيمة;
            int الكاميرا_الأمامية_قيمة_يغير_الحجم = 정렬시작 - تشغيل;
            int 끝크기 = منطقة_يغير_الحجم - الكاميرا_الأمامية_قيمة_يغير_الحجم - حجم;
            if (끝크기 < 0) {
                continue;
            }
            فارغ_منطقة.remove(Integer.valueOf(تشغيل));
            if (الكاميرا_الأمامية_قيمة_يغير_الحجم > 0) {
                فارغ_منطقة.put(Integer.valueOf(تشغيل), Integer.valueOf(الكاميرا_الأمامية_قيمة_يغير_الحجم));
            }
            if (끝크기 > 0) {
                فارغ_منطقة.put(Integer.valueOf(정렬시작 + حجم), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(حجم));
            Arrays.fill(ذاكرة_منطقة, 정렬시작, 정렬시작 + حجم, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void إصدار_تخزين(int عنوان) {
        Integer يغير_الحجم_عنصر = 사용영역.remove(Integer.valueOf(عنوان));
        if (يغير_الحجم_عنصر == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int تشغيل = عنوان;
        int حجم = يغير_الحجم_عنصر.intValue();
        Map.Entry<Integer, Integer> الكاميرا_الأمامية_قيمة = فارغ_منطقة.lowerEntry(Integer.valueOf(تشغيل));
        if (الكاميرا_الأمامية_قيمة != null && الكاميرا_الأمامية_قيمة.getKey().intValue() + الكاميرا_الأمامية_قيمة.getValue().intValue() == تشغيل) {
            تشغيل = الكاميرا_الأمامية_قيمة.getKey().intValue();
            حجم += الكاميرا_الأمامية_قيمة.getValue().intValue();
            فارغ_منطقة.remove(الكاميرا_الأمامية_قيمة.getKey());
        }
        Map.Entry<Integer, Integer> عودة_قيمة = فارغ_منطقة.ceilingEntry(Integer.valueOf(تشغيل));
        if (عودة_قيمة != null && تشغيل + حجم == عودة_قيمة.getKey().intValue()) {
            حجم += عودة_قيمة.getValue().intValue();
            فارغ_منطقة.remove(عودة_قيمة.getKey());
        }
        فارغ_منطقة.put(Integer.valueOf(تشغيل), Integer.valueOf(حجم));
    }

    public synchronized byte يقرأ_بايت_قيمة(int عنوان) {
        شيك_نطاق(عنوان, 1);
        return ذاكرة_منطقة[عنوان];
    }

    public synchronized void كتابة_بايت_قيمة(int عنوان, byte قيمة) {
        شيك_نطاق(عنوان, 1);
        ذاكرة_منطقة[عنوان] = قيمة;
    }

    public synchronized int إجمالي_يغير_الحجم() {
        return ذاكرة_منطقة.length;
    }

    public synchronized int 사용크기() {
        int إجمالي_قيمة = 0;
        for (Integer حجم : 사용영역.values()) {
            إجمالي_قيمة += حجم.intValue();
        }
        return إجمالي_قيمة;
    }

    private void شيك_نطاق(int عنوان, int حجم) {
        if (عنوان < 0 || حجم < 0 || عنوان > ذاكرة_منطقة.length - حجم) {
            throw new IndexOutOfBoundsException("ذاكرة_منطقة 범위를 벗어났습니다.");
        }
    }
}

