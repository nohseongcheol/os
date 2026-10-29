// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.ಕರ್ನಲ್;

/** Java 관리 커널과 CPU 고유 ಕೋಡ್_ಮೌಲ್ಯ 사이의 유일한 경계다. */
public interface 하드웨어 {
    void 직렬출력(String ವಿಷಯ_ಮೌಲ್ಯ);

    int 포트바이트읽기(int 포트번호);

    void ಬರೆ_ಪೋರ್ಟ್_ಬೈಟ್(int 포트번호, int ಮೌಲ್ಯ);

    void 중앙처리장치멈춤();
}

