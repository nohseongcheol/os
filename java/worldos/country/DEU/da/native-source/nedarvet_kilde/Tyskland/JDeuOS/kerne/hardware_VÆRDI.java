// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Tyskland.JDeuOS.kerne;

/** Java 관리 커널과 CPU ENTYDIGE_VÆRDI KODE_VÆRDI 사이의 유일한 경계다. */
public interface hardware_VÆRDI {
    void 직렬출력(String Indhold_VÆRDI);

    int 포트바이트읽기(int hardware_portnummer);

    void skrive_port_byte(int hardware_portnummer, int VÆRDI);

    void 중앙처리장치멈춤();
}

