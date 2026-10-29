// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package España.JEspOS.EspacioMemoria;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** Gestiona la asignación alineada, liberación y unión de memoria física. */
public final class GestorMemoria {
    private final byte[] EspacioMemoria;
    private final TreeMap<Integer, Integer> regiónVacíoEstado = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> regiónUsado = new TreeMap<Integer, Integer>();

    public GestorMemoria(int tamañoTotal) {
        if (tamañoTotal < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        EspacioMemoria = new byte[tamañoTotal];
        regiónVacíoEstado.put(Integer.valueOf(4096), Integer.valueOf(tamañoTotal - 4096));
    }

    public synchronized int asignarMemoriaAlmacenamiento(int tamaño) {
        return asignarMemoriaAlineado(tamaño, 1);
    }

    public synchronized int asignarMemoriaAlineado(int tamaño, int valorAlinear) {
        if (tamaño <= 0 || valorAlinear <= 0 || (valorAlinear & (valorAlinear - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> valorEntradaElemento : regiónVacíoEstado.entrySet()) {
            int ponerEnMarcha = valorEntradaElemento.getKey().intValue();
            int tamañoRegión = valorEntradaElemento.getValue().intValue();
            int iniciarAlineado = (ponerEnMarcha + valorAlinear - 1) & -valorAlinear;
            int tamañoValorLadoDelantero = iniciarAlineado - ponerEnMarcha;
            int tamañoFinal = tamañoRegión - tamañoValorLadoDelantero - tamaño;
            if (tamañoFinal < 0) {
                continue;
            }
            regiónVacíoEstado.remove(Integer.valueOf(ponerEnMarcha));
            if (tamañoValorLadoDelantero > 0) {
                regiónVacíoEstado.put(Integer.valueOf(ponerEnMarcha), Integer.valueOf(tamañoValorLadoDelantero));
            }
            if (tamañoFinal > 0) {
                regiónVacíoEstado.put(Integer.valueOf(iniciarAlineado + tamaño), Integer.valueOf(tamañoFinal));
            }
            regiónUsado.put(Integer.valueOf(iniciarAlineado), Integer.valueOf(tamaño));
            Arrays.fill(EspacioMemoria, iniciarAlineado, iniciarAlineado + tamaño, (byte) 0);
            return iniciarAlineado;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void liberarAlmacenamiento(int dirección) {
        Integer objetoTamaño = regiónUsado.remove(Integer.valueOf(dirección));
        if (objetoTamaño == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ponerEnMarcha = dirección;
        int tamaño = objetoTamaño.intValue();
        Map.Entry<Integer, Integer> valorLadoDelantero = regiónVacíoEstado.lowerEntry(Integer.valueOf(ponerEnMarcha));
        if (valorLadoDelantero != null && valorLadoDelantero.getKey().intValue() + valorLadoDelantero.getValue().intValue() == ponerEnMarcha) {
            ponerEnMarcha = valorLadoDelantero.getKey().intValue();
            tamaño += valorLadoDelantero.getValue().intValue();
            regiónVacíoEstado.remove(valorLadoDelantero.getKey());
        }
        Map.Entry<Integer, Integer> valorLadoPosterior = regiónVacíoEstado.ceilingEntry(Integer.valueOf(ponerEnMarcha));
        if (valorLadoPosterior != null && ponerEnMarcha + tamaño == valorLadoPosterior.getKey().intValue()) {
            tamaño += valorLadoPosterior.getValue().intValue();
            regiónVacíoEstado.remove(valorLadoPosterior.getKey());
        }
        regiónVacíoEstado.put(Integer.valueOf(ponerEnMarcha), Integer.valueOf(tamaño));
    }

    public synchronized byte leerValorByte(int dirección) {
        comprobarRango(dirección, 1);
        return EspacioMemoria[dirección];
    }

    public synchronized void escribirValorByte(int dirección, byte valor) {
        comprobarRango(dirección, 1);
        EspacioMemoria[dirección] = valor;
    }

    public synchronized int tamañoTotal() {
        return EspacioMemoria.length;
    }

    public synchronized int tamañoUsado() {
        int valorTotal = 0;
        for (Integer tamaño : regiónUsado.values()) {
            valorTotal += tamaño.intValue();
        }
        return valorTotal;
    }

    private void comprobarRango(int dirección, int tamaño) {
        if (dirección < 0 || tamaño < 0 || dirección > EspacioMemoria.length - tamaño) {
            throw new IndexOutOfBoundsException("EspacioMemoria 범위를 벗어났습니다.");
        }
    }
}

