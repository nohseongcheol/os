// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Վրաստան.JGeoOS.միջուկ;

/** Java 관리 커널과 CPU 고유 կոդ_արժեք 사이의 유일한 경계다. */
public interface 하드웨어 {
    void 직렬출력(String Բովանդակություն_արժեք);

    int 포트바이트읽기(int 포트번호);

    void գրել_միացք_բայթ(int 포트번호, int արժեք);

    void 중앙처리장치멈춤();
}

