// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canadá.JCanOS.Anfitrión;

import Canadá.JCanOS.Núcleo.Núcleo;

public final class inicioSistemaAnfitrión {
    private inicioSistemaAnfitrión() {
    }

    public static void main(String[] argumentoParámetro) {
        Núcleo valorNúcleo = new Núcleo(new EquipoFísicoAnfitrión());
        valorNúcleo.ponerEnMarcha();
        valorNúcleo.ejecutarPasoUnidad();
    }
}

