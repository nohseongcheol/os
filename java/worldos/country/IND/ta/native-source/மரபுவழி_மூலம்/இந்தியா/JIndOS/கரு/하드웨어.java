// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package இந்தியா.JIndOS.கரு;

/** Java 관리 커널과 CPU 고유 குறியீடு_மதிப்பு 사이의 유일한 경계다. */
public interface 하드웨어 {
    void 직렬출력(String உள்ளடக்கம்_மதிப்பு);

    int 포트바이트읽기(int 포트번호);

    void எழுது_முணையம்_பைட்(int 포트번호, int மதிப்பு);

    void 중앙처리장치멈춤();
}

