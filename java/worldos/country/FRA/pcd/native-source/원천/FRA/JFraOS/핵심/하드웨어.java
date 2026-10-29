// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package FRA.JFraOS.핵심;

/** Java 관리 커널과 CPU 고유 코드 사이의 유일한 경계다. */
public interface 하드웨어 {
    void 직렬출력(String 내용);

    int 포트바이트읽기(int 포트번호);

    void 포트바이트쓰기(int 포트번호, int 값);

    void 중앙처리장치멈춤();
}

