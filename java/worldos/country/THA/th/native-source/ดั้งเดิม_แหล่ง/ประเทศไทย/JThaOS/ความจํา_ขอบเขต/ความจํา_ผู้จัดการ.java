// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.ความจํา_ขอบเขต;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 จัดแนว_ค่า จัดสรร_ที่เก็บ, ปล่อย_ที่เก็บ, 병합을 담당한다. */
public final class ความจํา_ผู้จัดการ {
    private final byte[] ความจํา_ขอบเขต;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public ความจํา_ผู้จัดการ(int รวม_ขนาด) {
        if (รวม_ขนาด < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        ความจํา_ขอบเขต = new byte[รวม_ขนาด];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(รวม_ขนาด - 4096));
    }

    public synchronized int จัดสรร_ที่เก็บ(int ขนาด) {
        return 정렬할당(ขนาด, 1);
    }

    public synchronized int 정렬할당(int ขนาด, int จัดแนว_ค่า) {
        if (ขนาด <= 0 || จัดแนว_ค่า <= 0 || (จัดแนว_ค่า & (จัดแนว_ค่า - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> รายการ_ค่า : 빈영역.entrySet()) {
            int เรียกใช้งาน = รายการ_ค่า.getKey().intValue();
            int ขอบเขต_ขนาด = รายการ_ค่า.getValue().intValue();
            int 정렬시작 = (เรียกใช้งาน + จัดแนว_ค่า - 1) & -จัดแนว_ค่า;
            int กล้องหน้า_ค่า_ขนาด = 정렬시작 - เรียกใช้งาน;
            int 끝크기 = ขอบเขต_ขนาด - กล้องหน้า_ค่า_ขนาด - ขนาด;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(เรียกใช้งาน));
            if (กล้องหน้า_ค่า_ขนาด > 0) {
                빈영역.put(Integer.valueOf(เรียกใช้งาน), Integer.valueOf(กล้องหน้า_ค่า_ขนาด));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + ขนาด), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(ขนาด));
            Arrays.fill(ความจํา_ขอบเขต, 정렬시작, 정렬시작 + ขนาด, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void ปล่อย_ที่เก็บ(int อีเมล) {
        Integer ขนาด_วัตถุ = 사용영역.remove(Integer.valueOf(อีเมล));
        if (ขนาด_วัตถุ == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int เรียกใช้งาน = อีเมล;
        int ขนาด = ขนาด_วัตถุ.intValue();
        Map.Entry<Integer, Integer> กล้องหน้า_ค่า = 빈영역.lowerEntry(Integer.valueOf(เรียกใช้งาน));
        if (กล้องหน้า_ค่า != null && กล้องหน้า_ค่า.getKey().intValue() + กล้องหน้า_ค่า.getValue().intValue() == เรียกใช้งาน) {
            เรียกใช้งาน = กล้องหน้า_ค่า.getKey().intValue();
            ขนาด += กล้องหน้า_ค่า.getValue().intValue();
            빈영역.remove(กล้องหน้า_ค่า.getKey());
        }
        Map.Entry<Integer, Integer> ย้อนกลับ_ค่า = 빈영역.ceilingEntry(Integer.valueOf(เรียกใช้งาน));
        if (ย้อนกลับ_ค่า != null && เรียกใช้งาน + ขนาด == ย้อนกลับ_ค่า.getKey().intValue()) {
            ขนาด += ย้อนกลับ_ค่า.getValue().intValue();
            빈영역.remove(ย้อนกลับ_ค่า.getKey());
        }
        빈영역.put(Integer.valueOf(เรียกใช้งาน), Integer.valueOf(ขนาด));
    }

    public synchronized byte 바이트읽기(int อีเมล) {
        เช็ค_ช่วง(อีเมล, 1);
        return ความจํา_ขอบเขต[อีเมล];
    }

    public synchronized void 바이트쓰기(int อีเมล, byte ค่า) {
        เช็ค_ช่วง(อีเมล, 1);
        ความจํา_ขอบเขต[อีเมล] = ค่า;
    }

    public synchronized int รวม_ขนาด() {
        return ความจํา_ขอบเขต.length;
    }

    public synchronized int 사용크기() {
        int รวม_ค่า = 0;
        for (Integer ขนาด : 사용영역.values()) {
            รวม_ค่า += ขนาด.intValue();
        }
        return รวม_ค่า;
    }

    private void เช็ค_ช่วง(int อีเมล, int ขนาด) {
        if (อีเมล < 0 || ขนาด < 0 || อีเมล > ความจํา_ขอบเขต.length - ขนาด) {
            throw new IndexOutOfBoundsException("ความจํา_ขอบเขต 범위를 벗어났습니다.");
        }
    }
}

