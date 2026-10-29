// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canadá.JCanOS.Núcleo;

/** Única frontera entre el núcleo gestionado en Java y el código específico de CPU. */
public interface valorEquipoFísico {
    void salidaSerie(String valorContenidoValor);

    int leerBytePuerto(int númeroPuertoEquipoFísico);

    void escribirBytePuerto(int númeroPuertoEquipoFísico, int valor);

    void cPUDetenerMáquina();
}

