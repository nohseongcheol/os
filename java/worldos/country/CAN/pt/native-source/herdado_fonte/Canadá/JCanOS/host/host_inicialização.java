// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canadá.JCanOS.host;

import Canadá.JCanOS.Núcleo.Núcleo;

public final class host_inicialização {
    private host_inicialização() {
    }

    public static void main(String[] parâmetro_argumento) {
        Núcleo kernel_VALOR = new Núcleo(new host_hardware());
        kernel_VALOR.iniciar();
        kernel_VALOR.Executar_etapa();
    }
}

