// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Argentina.JArgOS.EspacioMemoria;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** Proporciona mapeo de páginas de 4 KiB y copia al escribir. */
public final class GestorPágina {
    public static final int tamañoPágina = 4096;

    private static final class valorPágina {
        private byte[] Datos = new byte[tamañoPágina];
        private int númeroElementosReferencia = 1;
        private boolean puedeEscribir = true;
        private boolean copiarEscribirActivado;
    }

    public static final class EspacioDirección {
        private final Map<Integer, valorPágina> tablaPágina = new HashMap<Integer, valorPágina>();
    }

    public EspacioDirección espacioDirecciónNuevo() {
        return new EspacioDirección();
    }

    public void páginaTablaCorrespondencia(EspacioDirección regiónDirección, int direcciónVirtual, boolean puedeEscribir) {
        int número = númeroPágina(direcciónVirtual);
        valorPágina páginaNuevo = new valorPágina();
        páginaNuevo.puedeEscribir = puedeEscribir;
        regiónDirección.tablaPágina.put(Integer.valueOf(número), páginaNuevo);
    }

    public EspacioDirección escribirActivadoCopiarClonar(EspacioDirección original) {
        EspacioDirección valorClonado = new EspacioDirección();
        for (Map.Entry<Integer, valorPágina> valorEntradaElemento : original.tablaPágina.entrySet()) {
            valorPágina páginaCompartido = valorEntradaElemento.getValue();
            páginaCompartido.númeroElementosReferencia++;
            if (páginaCompartido.puedeEscribir) {
                páginaCompartido.puedeEscribir = false;
                páginaCompartido.copiarEscribirActivado = true;
            }
            valorClonado.tablaPágina.put(valorEntradaElemento.getKey(), páginaCompartido);
        }
        return valorClonado;
    }

    public byte leerValorByte(EspacioDirección regiónDirección, int direcciónVirtual) {
        valorPágina valorObjetivo = encontrarPágina(regiónDirección, direcciónVirtual);
        return valorObjetivo.Datos[Math.floorMod(direcciónVirtual, tamañoPágina)];
    }

    public void escribirValorByte(EspacioDirección regiónDirección, int direcciónVirtual, byte valor) {
        int número = númeroPágina(direcciónVirtual);
        valorPágina valorObjetivo = encontrarPágina(regiónDirección, direcciónVirtual);
        if (!valorObjetivo.puedeEscribir) {
            if (!valorObjetivo.copiarEscribirActivado) {
                throw new IllegalStateException("leer 전용 쪽입니다.");
            }
            valorObjetivo = crearPáginaPrivado(regiónDirección, número, valorObjetivo);
        }
        valorObjetivo.Datos[Math.floorMod(direcciónVirtual, tamañoPágina)] = valor;
    }

    public void escribirRangoPrivado(EspacioDirección regiónDirección, int iniciarDirección, int tamaño) {
        if (tamaño < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int direcciónFin = Math.addExact(iniciarDirección, tamaño);
        for (int dirección = iniciarDirección; dirección < direcciónFin; dirección = (númeroPágina(dirección) + 1) * tamañoPágina) {
            int número = númeroPágina(dirección);
            valorPágina valorObjetivo = encontrarPágina(regiónDirección, dirección);
            if (valorObjetivo.copiarEscribirActivado) {
                crearPáginaPrivado(regiónDirección, número, valorObjetivo);
            } else {
                valorObjetivo.puedeEscribir = true;
            }
        }
    }

    public void escribirRango(EspacioDirección regiónDirección, int iniciarDirección, byte[] Datos) {
        for (int número = 0; número < Datos.length; número++) {
            escribirValorByte(regiónDirección, iniciarDirección + número, Datos[número]);
        }
    }

    private valorPágina crearPáginaPrivado(EspacioDirección regiónDirección, int número, valorPágina páginaCompartido) {
        valorPágina páginaPrivado = new valorPágina();
        páginaPrivado.Datos = Arrays.copyOf(páginaCompartido.Datos, páginaCompartido.Datos.length);
        páginaPrivado.puedeEscribir = true;
        páginaPrivado.copiarEscribirActivado = false;
        páginaCompartido.númeroElementosReferencia--;
        regiónDirección.tablaPágina.put(Integer.valueOf(número), páginaPrivado);
        return páginaPrivado;
    }

    private valorPágina encontrarPágina(EspacioDirección regiónDirección, int dirección) {
        valorPágina valorObjetivo = regiónDirección.tablaPágina.get(Integer.valueOf(númeroPágina(dirección)));
        if (valorObjetivo == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return valorObjetivo;
    }

    private int númeroPágina(int dirección) {
        if (dirección < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return dirección / tamañoPágina;
    }
}

