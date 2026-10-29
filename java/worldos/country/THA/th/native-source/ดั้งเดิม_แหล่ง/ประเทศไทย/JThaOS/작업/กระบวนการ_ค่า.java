// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.작업;

import ประเทศไทย.JThaOS.ความจํา_ขอบเขต.เพจ_ผู้จัดการ;
import ประเทศไทย.JThaOS.ระบบแฟ้ม.파일서술자표;

public final class กระบวนการ_ค่า {
    private final int ตัวระบุ_ค่า;
    private final int แม่_ตัวระบุ;
    private final เพจ_ผู้จัดการ.อีเมล_สเปซ อีเมล_สเปซ;
    private final 파일서술자표 파일서술자;
    private กระบวนการ_สถานะ สถานะ_ค่า = กระบวนการ_สถานะ.จัดเตรียม;
    private int ออก_รหัส;
    private int แอป_เวลาพัก = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] สภาพแวดล้อม_ค่า = new String[0];

    กระบวนการ_ค่า(int ตัวระบุ_ค่า, int แม่_ตัวระบุ, เพจ_ผู้จัดการ.อีเมล_สเปซ อีเมล_สเปซ, 파일서술자표 파일서술자) {
        this.ตัวระบุ_ค่า = ตัวระบุ_ค่า;
        this.แม่_ตัวระบุ = แม่_ตัวระบุ;
        this.อีเมล_สเปซ = อีเมล_สเปซ;
        this.파일서술자 = 파일서술자;
    }

    public int ตัวระบุ_ค่า() {
        return ตัวระบุ_ค่า;
    }

    public int แม่_ตัวระบุ() {
        return แม่_ตัวระบุ;
    }

    public เพจ_ผู้จัดการ.อีเมล_สเปซ อีเมล_สเปซ() {
        return อีเมล_สเปซ;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public กระบวนการ_สถานะ สถานะ_ค่า() {
        return สถานะ_ค่า;
    }

    public void ชุด_สถานะ(กระบวนการ_สถานะ 새상태) {
        สถานะ_ค่า = 새상태;
    }

    public int ออก_รหัส() {
        return ออก_รหัส;
    }

    public void ออก_แอป(int ค่า) {
        ออก_รหัส = ค่า & 0xff;
        สถานะ_ค่า = กระบวนการ_สถานะ.ออก_แอป;
    }

    public int แอป_เวลาพัก() {
        return แอป_เวลาพัก;
    }

    public void ชุด_แอป_เวลาพัก(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("แอป_f5044b9b 끝 범위를 벗어났습니다.");
        }
        แอป_เวลาพัก = 새끝;
    }

    public void 실행문맥설정(int เริ่ม_อีเมล, String[] พารามิเตอร์_อาร์กิวเมนต์, String[] สภาพแวดล้อม) {
        실행시작주소 = เริ่ม_อีเมล;
        실행인자 = พารามิเตอร์_อาร์กิวเมนต์.clone();
        สภาพแวดล้อม_ค่า = สภาพแวดล้อม.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] สภาพแวดล้อม_ค่า() { return สภาพแวดล้อม_ค่า.clone(); }
}
