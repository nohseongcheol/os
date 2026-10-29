// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Norge.JNorOS.kjerne;

/** Java 관리 커널과 CPU UNIK_VERDI KODE_VERDI 사이의 유일한 경계다. */
public interface maskinvare_VERDI {
    void 직렬출력(String Innhold_VERDI);

    int 포트바이트읽기(int maskinvare_portnummer);

    void skrive_port_byte(int maskinvare_portnummer, int VERDI);

    void 중앙처리장치멈춤();
}

