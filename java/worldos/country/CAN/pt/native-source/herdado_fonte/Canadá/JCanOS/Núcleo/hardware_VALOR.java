// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canadá.JCanOS.Núcleo;

/** Java 관리 커널과 CPU ÚNICO_VALOR valor_do_código 사이의 유일한 경계다. */
public interface hardware_VALOR {
    void 직렬출력(String Conteúdo_VALOR);

    int leitura_porta_byte(int hardware_número_da_porta);

    void gravar_porta_byte(int hardware_número_da_porta, int VALOR);

    void 중앙처리장치멈춤();
}

