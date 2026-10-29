// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Portugal.JPrtOS.SistemaArchivo;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Valida cabeceras y segmentos de carga de ejecutables ELF32 de orden little-endian. */
public final class CargadorCódigoEjecutable {
    public static final class valorSección {
        private final int valorClaseTipo;
        private final int valorBandera;
        private final int dirección;
        private final int posiciónArchivo;
        private final int tamaño;

        valorSección(int valorClaseTipo, int valorBandera, int dirección, int posiciónArchivo, int tamaño) {
            this.valorClaseTipo = valorClaseTipo;
            this.valorBandera = valorBandera;
            this.dirección = dirección;
            this.posiciónArchivo = posiciónArchivo;
            this.tamaño = tamaño;
        }

        public int valorClaseTipo() {
            return valorClaseTipo;
        }

        public int valorBandera() {
            return valorBandera;
        }

        public int dirección() {
            return dirección;
        }

        public int posiciónArchivo() {
            return posiciónArchivo;
        }

        public int tamaño() {
            return tamaño;
        }
    }

    public static final class imagen {
        private final int iniciarDirección;
        private final List<valorSección> listaSecciones;

        imagen(int iniciarDirección, List<valorSección> listaSecciones) {
            this.iniciarDirección = iniciarDirección;
            this.listaSecciones = Collections.unmodifiableList(listaSecciones);
        }

        public int iniciarDirección() {
            return iniciarDirección;
        }

        public List<valorSección> listaSecciones() {
            return listaSecciones;
        }
    }

    public imagen Comprobaciones(byte[] Datos) {
        if (Datos == null || Datos.length < 52
                || Datos[0] != 0x7f || Datos[1] != 'E' || Datos[2] != 'L' || Datos[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (Datos[4] != 1 || Datos[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int iniciarDirección = analizarEnteroValor(Datos, 24);
        int posiciónTablaSección = analizarEnteroValor(Datos, 32);
        int tamañoEntradaElementoSección = leerEnteroValorCorto(Datos, 46);
        int númeroElementosSección = leerEnteroValorCorto(Datos, 48);
        if (tamañoEntradaElementoSección < 40 || posiciónTablaSección < 0
                || (long) posiciónTablaSección + (long) tamañoEntradaElementoSección * númeroElementosSección > Datos.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<valorSección> listaSecciones = new ArrayList<valorSección>();
        for (int número = 0; número < númeroElementosSección; número++) {
            int posición = posiciónTablaSección + número * tamañoEntradaElementoSección;
            int valorClaseTipo = analizarEnteroValor(Datos, posición + 4);
            int valorBandera = analizarEnteroValor(Datos, posición + 8);
            int dirección = analizarEnteroValor(Datos, posición + 12);
            int posiciónArchivo = analizarEnteroValor(Datos, posición + 16);
            int tamaño = analizarEnteroValor(Datos, posición + 20);
            if (tamaño < 0 || (valorClaseTipo != 8 && ((long) posiciónArchivo + tamaño > Datos.length || posiciónArchivo < 0))) {
                throw new IllegalArgumentException("ELF valorSección Datos 범위가 올바르지 않습니다.");
            }
            listaSecciones.add(new valorSección(valorClaseTipo, valorBandera, dirección, posiciónArchivo, tamaño));
        }
        return new imagen(iniciarDirección, listaSecciones);
    }

    private int analizarEnteroValor(byte[] Datos, int posición) {
        if (posición < 0 || posición > Datos.length - 4) {
            throw new IllegalArgumentException("ELF EnteroValor 범위를 벗어났습니다.");
        }
        return (Datos[posición] & 0xff)
                | ((Datos[posición + 1] & 0xff) << 8)
                | ((Datos[posición + 2] & 0xff) << 16)
                | ((Datos[posición + 3] & 0xff) << 24);
    }

    private int leerEnteroValorCorto(byte[] Datos, int posición) {
        if (posición < 0 || posición > Datos.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 EnteroValor 범위를 벗어났습니다.");
        }
        return (Datos[posición] & 0xff) | ((Datos[posición + 1] & 0xff) << 8);
    }
}
