// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Avstrija.JAutOS.jedro;

/** Java 관리 커널과 CPU UNIQUE_VALUE CODE_VALUE 사이의 유일한 경계다. */
public interface strojna_oprema_VALUE {
    void 직렬출력(String vsebina_VALUE);

    int 포트바이트읽기(int strojna_oprema_številka_vrat);

    void pisati_vrata_bajt(int strojna_oprema_številka_vrat, int VALUE);

    void 중앙처리장치멈춤();
}

