// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Perú.JPerOS.SistemaArchivo;

import java.util.HashMap;
import java.util.Map;

/** Mantiene descriptores independientes por proceso y descripciones compartibles de archivos abiertos. */
public final class tablaDescriptorArchivo {
    private static final int descriptorMáximo = 32;

    private static final class entradaElementoDescriptor {
        private final SistemaArchivo.archivoAbierto archivoAbierto;
        private boolean cerrarOperaciónEjecuciónActivado;

        entradaElementoDescriptor(SistemaArchivo.archivoAbierto archivoAbierto) {
            this.archivoAbierto = archivoAbierto;
        }
    }

    private final SistemaArchivo SistemaArchivo;
    private final Map<Integer, entradaElementoDescriptor> entradasDescriptor = new HashMap<Integer, entradaElementoDescriptor>();

    public tablaDescriptorArchivo(SistemaArchivo SistemaArchivo) {
        this.SistemaArchivo = SistemaArchivo;
    }

    public int abrir(String nombre) {
        SistemaArchivo.archivoAbierto archivoAbierto = SistemaArchivo.abrir(nombre);
        if (archivoAbierto == null) {
            return -2;
        }
        int número = índiceVacíoEstado(3);
        if (número < 0) {
            return -24;
        }
        entradasDescriptor.put(Integer.valueOf(número), new entradaElementoDescriptor(archivoAbierto));
        return número;
    }

    public int leer(int número, byte[] recibirDestino, int tamaño) {
        entradaElementoDescriptor valorEntradaElemento = entradasDescriptor.get(Integer.valueOf(número));
        if (valorEntradaElemento == null) {
            return -9;
        }
        if (tamaño < 0 || tamaño > recibirDestino.length) {
            return -22;
        }
        int datosRestoDivisión = valorEntradaElemento.archivoAbierto.Datos.length - valorEntradaElemento.archivoAbierto.posición;
        int leerTamaño = Math.min(tamaño, Math.max(datosRestoDivisión, 0));
        System.arraycopy(valorEntradaElemento.archivoAbierto.Datos, valorEntradaElemento.archivoAbierto.posición, recibirDestino, 0, leerTamaño);
        valorEntradaElemento.archivoAbierto.posición += leerTamaño;
        return leerTamaño;
    }

    public int posiciónMover(int número, int valorDistancia, int raízProyecto) {
        entradaElementoDescriptor valorEntradaElemento = entradasDescriptor.get(Integer.valueOf(número));
        if (valorEntradaElemento == null) {
            return -9;
        }
        int valorFondo;
        if (raízProyecto == 0) {
            valorFondo = 0;
        } else if (raízProyecto == 1) {
            valorFondo = valorEntradaElemento.archivoAbierto.posición;
        } else if (raízProyecto == 2) {
            valorFondo = valorEntradaElemento.archivoAbierto.Datos.length;
        } else {
            return -22;
        }
        int posiciónNuevo = valorFondo + valorDistancia;
        if (posiciónNuevo < 0) {
            return -22;
        }
        valorEntradaElemento.archivoAbierto.posición = posiciónNuevo;
        return posiciónNuevo;
    }

    public int cerrar(int número) {
        entradaElementoDescriptor valorEntradaElemento = entradasDescriptor.remove(Integer.valueOf(número));
        if (valorEntradaElemento == null) {
            return -9;
        }
        valorEntradaElemento.archivoAbierto.númeroElementosReferencia--;
        return 0;
    }

    public int descriptorClonado(int número, int númeroMínimo) {
        entradaElementoDescriptor valorEntradaElemento = entradasDescriptor.get(Integer.valueOf(número));
        if (valorEntradaElemento == null) {
            return -9;
        }
        int númeroNuevo = índiceVacíoEstado(númeroMínimo);
        if (númeroNuevo < 0) {
            return -24;
        }
        valorEntradaElemento.archivoAbierto.númeroElementosReferencia++;
        entradasDescriptor.put(Integer.valueOf(númeroNuevo), new entradaElementoDescriptor(valorEntradaElemento.archivoAbierto));
        return númeroNuevo;
    }

    public int enPosiciónDuplicado(int número, int númeroNuevo) {
        if (número == númeroNuevo) {
            return entradasDescriptor.containsKey(Integer.valueOf(número)) ? número : -9;
        }
        if (númeroNuevo < 0 || númeroNuevo >= descriptorMáximo) {
            return -9;
        }
        entradaElementoDescriptor original = entradasDescriptor.get(Integer.valueOf(número));
        if (original == null) {
            return -9;
        }
        if (entradasDescriptor.containsKey(Integer.valueOf(númeroNuevo))) {
            cerrar(númeroNuevo);
        }
        original.archivoAbierto.númeroElementosReferencia++;
        entradasDescriptor.put(Integer.valueOf(númeroNuevo), new entradaElementoDescriptor(original.archivoAbierto));
        return númeroNuevo;
    }

    public int establecerOperaciónEjecuciónActivadoCerrar(int número, boolean valor) {
        entradaElementoDescriptor valorEntradaElemento = entradasDescriptor.get(Integer.valueOf(número));
        if (valorEntradaElemento == null) {
            return -9;
        }
        valorEntradaElemento.cerrarOperaciónEjecuciónActivado = valor;
        return 0;
    }

    public int cerrarValorOperaciónEjecuciónActivado(int número) {
        entradaElementoDescriptor valorEntradaElemento = entradasDescriptor.get(Integer.valueOf(número));
        if (valorEntradaElemento == null) {
            return -9;
        }
        return valorEntradaElemento.cerrarOperaciónEjecuciónActivado ? 1 : 0;
    }

    public informaciónArchivo informaciónSistema(int número) {
        if (número >= 0 && número <= 2) {
            return new informaciónArchivo(0, 0020666);
        }
        entradaElementoDescriptor valorEntradaElemento = entradasDescriptor.get(Integer.valueOf(número));
        if (valorEntradaElemento == null) {
            return null;
        }
        return new informaciónArchivo(valorEntradaElemento.archivoAbierto.Datos.length, 0100444);
    }

    public void cerrarOperaciónEjecuciónActivado() {
        Integer[] listaNúmero = entradasDescriptor.keySet().toArray(new Integer[0]);
        for (Integer número : listaNúmero) {
            entradaElementoDescriptor valorEntradaElemento = entradasDescriptor.get(número);
            if (valorEntradaElemento != null && valorEntradaElemento.cerrarOperaciónEjecuciónActivado) {
                cerrar(número.intValue());
            }
        }
    }

    public boolean esAbrir(int número) {
        return entradasDescriptor.containsKey(Integer.valueOf(número));
    }

    public tablaDescriptorArchivo valorClonar() {
        tablaDescriptorArchivo resultado = new tablaDescriptorArchivo(SistemaArchivo);
        for (Map.Entry<Integer, entradaElementoDescriptor> valorEntradaElemento : entradasDescriptor.entrySet()) {
            valorEntradaElemento.getValue().archivoAbierto.númeroElementosReferencia++;
            entradaElementoDescriptor descriptorNuevo = new entradaElementoDescriptor(valorEntradaElemento.getValue().archivoAbierto);
            descriptorNuevo.cerrarOperaciónEjecuciónActivado = valorEntradaElemento.getValue().cerrarOperaciónEjecuciónActivado;
            resultado.entradasDescriptor.put(valorEntradaElemento.getKey(), descriptorNuevo);
        }
        return resultado;
    }

    private int índiceVacíoEstado(int númeroMínimo) {
        for (int número = Math.max(0, númeroMínimo); número < descriptorMáximo; número++) {
            if (!entradasDescriptor.containsKey(Integer.valueOf(número))) {
                return número;
            }
        }
        return -1;
    }
}
