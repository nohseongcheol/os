// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ผู้ใช้ ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ผู้ใช้ {
    public static native int 파일서술자열기(int[] แฟ้ม_รายการ_ชื่อ, int เปิด_การตั้งค่า);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int ไบต์_ค่า);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] ชื่อ, int[] ข้อมูล);
    public static native int 문자쓰기(int 문자);
    public static native int 파일쓰기(int[] ชื่อ, int[] ข้อมูล, int 길이);
    public static native int เขียน(String เนื้อหา_ค่า);
    public static native int 인수개수();
    public static native String อาร์กิวเมนต์(int ดัชนี);
    public static native int 실행권한();
    public static native int เปิด_เครือข่าย(int ท้องถิ่น_แปลง);
    public static native int ส่ง_ข้อมูล(int จุดจับ_ค่า, int อีเมล, int ปลายทาง_แปลง, int[] ข้อมูล, int 길이);
    public static native int รับ_ข้อมูล(int จุดจับ_ค่า, int[] ข้อมูล, int 제한밀리초);
    public static native int ปิด_เครือข่าย(int จุดจับ_ค่า);
    public static native int 내주소();
    public static native int 보낸주소(int จุดจับ_ค่า);
    public static native int 보낸창구(int จุดจับ_ค่า);
}
