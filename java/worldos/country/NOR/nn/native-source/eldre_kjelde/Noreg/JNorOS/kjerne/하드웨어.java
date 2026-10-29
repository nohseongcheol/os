// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.kjerne;

/** Java 관리 커널과 CPU UNIQUE_VALUE CODE_VALUE 사이의 유일한 경계다. */
public interface 하드웨어 {
    void 직렬출력(String Innhald_VALUE);

    int 포트바이트읽기(int 포트번호);

    void skrive_port_byte(int 포트번호, int VALUE);

    void 중앙처리장치멈춤();
}

