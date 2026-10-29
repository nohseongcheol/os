// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package España.JEspOS.SistemaArchivo;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** Modelo gestionado de almacenamiento de archivos de solo lectura correspondiente a la capa de lectura FAT de engos. */
public final class SistemaArchivo {
    static final class archivoAbierto {
        final byte[] Datos;
        int posición;
        int númeroElementosReferencia = 1;

        archivoAbierto(byte[] Datos) {
            this.Datos = Datos;
        }
    }

    private final Map<String, byte[]> entradasArchivo = new LinkedHashMap<String, byte[]>();

    public void añadirFinalArchivo(String nombre, byte[] Datos) {
        entradasArchivo.put(nombreCanónico(nombre), Arrays.copyOf(Datos, Datos.length));
    }

    archivoAbierto abrir(String nombre) {
        byte[] Datos = entradasArchivo.get(nombreCanónico(nombre));
        if (Datos == null) {
            return null;
        }
        return new archivoAbierto(Datos);
    }

    public boolean valorExiste(String nombre) {
        return entradasArchivo.containsKey(nombreCanónico(nombre));
    }

    public informaciónArchivo informaciónSistema(String nombre) {
        byte[] Datos = entradasArchivo.get(nombreCanónico(nombre));
        if (Datos == null) {
            return null;
        }
        return new informaciónArchivo(Datos.length, 0100444);
    }

    private String nombreCanónico(String nombre) {
        if (nombre == null) {
            throw new NullPointerException("Archivo 이름이 없습니다.");
        }
        String resultado = nombre.startsWith("/") ? nombre.substring(1) : nombre;
        return resultado.toUpperCase(Locale.ROOT);
    }
}
