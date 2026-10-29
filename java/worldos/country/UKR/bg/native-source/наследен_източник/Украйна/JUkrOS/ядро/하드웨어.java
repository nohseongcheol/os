// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Украйна.JUkrOS.ядро;

/** Java 관리 커널과 CPU 고유 код_стойност 사이의 유일한 경계다. */
public interface 하드웨어 {
    void 직렬출력(String Съдържание_стойност);

    int 포트바이트읽기(int 포트번호);

    void записване_порт_байт(int 포트번호, int стойност);

    void 중앙처리장치멈춤();
}

