// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Uruguay.JUryOS.Anfitrión;

import Uruguay.JUryOS.Núcleo.Núcleo;

public final class inicioSistemaAnfitrión {
    private inicioSistemaAnfitrión() {
    }

    public static void main(String[] argumentoParámetro) {
        Núcleo valorNúcleo = new Núcleo(new EquipoFísicoAnfitrión());
        valorNúcleo.ponerEnMarcha();
        valorNúcleo.ejecutarPasoUnidad();
    }
}

