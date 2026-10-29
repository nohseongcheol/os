// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Colombia.JColOS.Anfitrión;

import java.util.HashMap;
import java.util.Map;
import Colombia.JColOS.Núcleo.valorEquipoFísico;

/** Sustituto del hardware para pruebas deterministas del núcleo gestionado en una JVM ordinaria. */
public final class EquipoFísicoAnfitrión implements valorEquipoFísico {
    private final Map<Integer, Integer> valorPuertoEquipoFísico = new HashMap<Integer, Integer>();
    private final StringBuilder diarioSerie = new StringBuilder();

    @Override
    public void salidaSerie(String valorContenidoValor) {
        diarioSerie.append(valorContenidoValor);
        System.out.print(valorContenidoValor);
    }

    @Override
    public int leerBytePuerto(int númeroPuertoEquipoFísico) {
        Integer valor = valorPuertoEquipoFísico.get(Integer.valueOf(númeroPuertoEquipoFísico));
        return valor == null ? 0 : valor.intValue();
    }

    @Override
    public void escribirBytePuerto(int númeroPuertoEquipoFísico, int valor) {
        valorPuertoEquipoFísico.put(Integer.valueOf(númeroPuertoEquipoFísico), Integer.valueOf(valor & 0xff));
    }

    @Override
    public void cPUDetenerMáquina() {
        // En las pruebas del anfitrión, volver inmediatamente sin esperar al siguiente evento.
    }

    public String diarioSerie() {
        return diarioSerie.toString();
    }
}

