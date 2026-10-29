// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Szlovákia.JSvkOS.kernel;

/** Java 관리 커널과 CPU EGYEDI_ÉRTÉK KÓD_ÉRTÉK 사이의 유일한 경계다. */
public interface hardver_ÉRTÉK {
    void 직렬출력(String Tartalom_ÉRTÉK);

    int 포트바이트읽기(int hardver_portszám);

    void ír_port_bájt(int hardver_portszám, int ÉRTÉK);

    void 중앙처리장치멈춤();
}

