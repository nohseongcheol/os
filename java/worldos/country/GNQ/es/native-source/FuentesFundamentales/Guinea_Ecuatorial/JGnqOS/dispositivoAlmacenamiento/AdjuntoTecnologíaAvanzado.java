// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Guinea_Ecuatorial.JGnqOS.dispositivoAlmacenamiento;

import java.util.Arrays;

/** Dispositivo de sectores lógicos de 512 bytes equivalente a la capa de órdenes ATA de 28 bits. */
public final class AdjuntoTecnologíaAvanzado {
    public static final int tamañoSección = 512;
    private final byte[] Datos;
    private final boolean leerValorSolamente;

    public AdjuntoTecnologíaAvanzado(int númeroElementosSección, boolean leerValorSolamente) {
        if (númeroElementosSección <= 0) {
            throw new IllegalArgumentException("valorSección 수가 올바르지 않습니다.");
        }
        Datos = new byte[Math.multiplyExact(númeroElementosSección, tamañoSección)];
        this.leerValorSolamente = leerValorSolamente;
    }

    public int númeroElementosSección() {
        return Datos.length / tamañoSección;
    }

    public void leer(int índiceSección, byte[] recibirDestino) {
        comprobarRango(índiceSección, recibirDestino);
        System.arraycopy(Datos, índiceSección * tamañoSección, recibirDestino, 0, tamañoSección);
    }

    public void escribir(int índiceSección, byte[] escribirHaciaDatos) {
        if (leerValorSolamente) {
            throw new IllegalStateException("leer 전용 장치입니다.");
        }
        comprobarRango(índiceSección, escribirHaciaDatos);
        System.arraycopy(escribirHaciaDatos, 0, Datos, índiceSección * tamañoSección, tamañoSección);
    }

    public void borrarEntradaElemento() {
        if (leerValorSolamente) {
            throw new IllegalStateException("leer 전용 장치입니다.");
        }
        Arrays.fill(Datos, (byte) 0);
    }

    private void comprobarRango(int índiceSección, byte[] espacioTemporal) {
        if (índiceSección < 0 || índiceSección >= númeroElementosSección() || espacioTemporal.length < tamañoSección) {
            throw new IllegalArgumentException("ATA valorSección 범위가 올바르지 않습니다.");
        }
    }
}

