// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Itàlia.JItaOS.nucli;

/** Java 관리 커널과 CPU ÚNICS_VALOR CODI_VALOR 사이의 유일한 경계다. */
public interface 하드웨어 {
    void 직렬출력(String contingut_VALOR);

    int tancar_port_byte(int 포트번호);

    void escriure_port_byte(int 포트번호, int VALOR);

    void 중앙처리장치멈춤();
}

