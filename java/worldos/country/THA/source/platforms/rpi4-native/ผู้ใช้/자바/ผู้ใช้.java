// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 เครื่องมือ 전용 SVC เชื่อมต่อ. 기존 x86 เครื่องมือ 원문을 함께 빌드한다. */
public final class ผู้ใช้ {
    public static native int 파일서술자열기(int[] ชื่อ, int ตั้งค่า);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int ค่า);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] ชื่อ, int[] ข้อมูล);
    public static native int 파일쓰기(int[] ชื่อ, int[] ข้อมูล, int 길이);
    public static native int เขียน(String ข้อความ);
    public static native int 문자쓰기(int ค่า);
    public static native int 인수개수();
    public static native String อาร์กิวเมนต์(int ดัชนี);
    public static native int เครื่องมือ_หมายเลข();
    public static native int 화면연결(int การกระทํา, int ดัชนี, int 가, int 나, int 다, int 라);
    public static native int 화면글(int ดัชนี, int[] ข้อความ, int 길이);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int สตรีม_ควบคุม(int การกระทํา, int 서술자, int ค่า);
    public static native int เชื่อมต่อ_สตรีม(int 서술자, int อีเมล, int แปลง_ค่า);
    public static native int เปิด_เครือข่าย(int แปลง_ค่า);
    public static native int ส่ง_เครือข่าย(int 서술자, int อีเมล, int แปลง_ค่า, int[] ข้อมูล, int 길이);
    public static native int รับ_เครือข่าย(int 서술자, int[] ข้อมูล, int 길이);
    public static native int เครือข่าย_แปลง(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int สี่เหลี่ยมผืนผ้า(int 가로, int แนวตั้ง_ตําแหน่ง, int 폭, int 높이, int 색);
}
