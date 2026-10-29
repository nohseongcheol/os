// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 เครื่อง 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class บอร์ด {
    public static native int 표시화소읽기(int 가로, int แนวตั้ง_ตําแหน่ง);
    public static native void 표시화소쓰기(int 가로, int แนวตั้ง_ตําแหน่ง, int 색);
    public static native int การควบคุมระยะไกล(int 종류, int การกระทํา);
    public static native void สิ้นสุดการโทร_ระยะไกล_คําสั่ง(int สถานะ_ค่า);
    public static native void ระยะไกล_รอเดี๋ยว(int สถานะ_ค่า);
    public static native void 직렬쓰기(int ค่า);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int หน่วยประมวลผลกลาง_สิทธิ์_ระดับ();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int แนวตั้ง_ตําแหน่ง, int 색);
    public static native void หยุดชั่วคราว_ผู้ประมวลผล();
    public static native int เปิด_งาน(int ดัชนี);
    public static native int งาน_สถานะ(int ดัชนี);
    public static native void หยุด(int สถานะ_ค่า);
    public static native int 씨플러스시험();
    public static native int ใช้งาน_ผู้ใช้_แอป(int ดัชนี);
    public static native int เช็ค_ผู้ใช้_แอป();
    public static native int 인수준비(int 개수);
    public static native int ดําเนินการ_ผู้ใช้_แฟ้ม();
    public static native int 리눅스파일실행();
    public static native int อาร์กิวเมนต์_ไบต์(int ดัชนี, int ตําแหน่ง, int ค่า);
    public static native int เทอร์มินัล(int การกระทํา);
    public static native int ควบคุม_ผู้ใช้_แอป(int การกระทํา);
    public static native void 입출력전환(int การกระทํา);
    public static native int การถ่ายโอนแฟ้ม_บริการ(int การกระทํา);
    public static native int เครือข่าย_สถานะ(int รายการ_ค่า, int ดัชนี);
    public static native int เครือข่าย_การตั้งค่า(int การกระทํา, int อีเมล, int มาสก์_ค่า, int เกตเวย์_ค่า);
    public static native int ส่ง_การตอบ(int อีเมล, int ลําดับ_ค่า);
    public static native int 응답읽기(int รายการ_ค่า);
    public static native int คิวรี_ระบบ(int รายการ_ค่า, int ดัชนี);
    public static native void 전원끄기();
}
