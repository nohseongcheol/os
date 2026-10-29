// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.ระบบแฟ้ม;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT อ่าน 계층과 같은 อ่าน 전용 แฟ้ม 저장소의 관리 모델이다. */
public final class ระบบแฟ้ม {
    static final class 열린파일 {
        final byte[] ข้อมูล;
        int ตําแหน่ง;
        int 참조수 = 1;

        열린파일(byte[] ข้อมูล) {
            this.ข้อมูล = ข้อมูล;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void ผนวก_แฟ้ม(String ชื่อ, byte[] ข้อมูล) {
        파일들.put(ชื่อมาตรฐาน(ชื่อ), Arrays.copyOf(ข้อมูล, ข้อมูล.length));
    }

    열린파일 เปิด(String ชื่อ) {
        byte[] ข้อมูล = 파일들.get(ชื่อมาตรฐาน(ชื่อ));
        if (ข้อมูล == null) {
            return null;
        }
        return new 열린파일(ข้อมูล);
    }

    public boolean 존재함(String ชื่อ) {
        return 파일들.containsKey(ชื่อมาตรฐาน(ชื่อ));
    }

    public แฟ้ม_ข้อมูล ข้อมูลระบบ(String ชื่อ) {
        byte[] ข้อมูล = 파일들.get(ชื่อมาตรฐาน(ชื่อ));
        if (ข้อมูล == null) {
            return null;
        }
        return new แฟ้ม_ข้อมูล(ข้อมูล.length, 0100444);
    }

    private String ชื่อมาตรฐาน(String ชื่อ) {
        if (ชื่อ == null) {
            throw new NullPointerException("แฟ้ม 이름이 없습니다.");
        }
        String ผลลัพธ์ = ชื่อ.startsWith("/") ? ชื่อ.substring(1) : ชื่อ;
        return ผลลัพธ์.toUpperCase(Locale.ROOT);
    }
}
