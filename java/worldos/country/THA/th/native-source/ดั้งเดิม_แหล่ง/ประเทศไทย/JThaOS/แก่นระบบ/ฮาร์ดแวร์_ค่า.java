// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.แก่นระบบ;

/** Java 관리 커널과 CPU 고유 รหัส_ค่า 사이의 유일한 경계다. */
public interface ฮาร์ดแวร์_ค่า {
    void 직렬출력(String เนื้อหา_ค่า);

    int 포트바이트읽기(int ฮาร์ดแวร์_หมายเลขพอร์ต);

    void 포트바이트쓰기(int ฮาร์ดแวร์_หมายเลขพอร์ต, int ค่า);

    void 중앙처리장치멈춤();
}

