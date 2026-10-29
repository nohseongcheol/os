// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ecuador.JEcuOS.Tarea;

import Ecuador.JEcuOS.EspacioMemoria.GestorPágina;
import Ecuador.JEcuOS.SistemaArchivo.tablaDescriptorArchivo;

public final class valorProceso {
    private final int valorIdentificador;
    private final int identificadorPadre;
    private final GestorPágina.EspacioDirección EspacioDirección;
    private final tablaDescriptorArchivo descriptorArchivo;
    private estadoValorProceso valorEstadoValor = estadoValorProceso.preparar;
    private int códigoSalir;
    private int interrumpirBuclePrograma = 0x06000000;
    private int direcciónIniciarEjecución;
    private String[] argumentoEjecución = new String[0];
    private String[] valorEntorno = new String[0];

    valorProceso(int valorIdentificador, int identificadorPadre, GestorPágina.EspacioDirección EspacioDirección, tablaDescriptorArchivo descriptorArchivo) {
        this.valorIdentificador = valorIdentificador;
        this.identificadorPadre = identificadorPadre;
        this.EspacioDirección = EspacioDirección;
        this.descriptorArchivo = descriptorArchivo;
    }

    public int valorIdentificador() {
        return valorIdentificador;
    }

    public int identificadorPadre() {
        return identificadorPadre;
    }

    public GestorPágina.EspacioDirección EspacioDirección() {
        return EspacioDirección;
    }

    public tablaDescriptorArchivo descriptorArchivo() {
        return descriptorArchivo;
    }

    public estadoValorProceso valorEstadoValor() {
        return valorEstadoValor;
    }

    public void establecerEstadoValor(estadoValorProceso estadoValorNuevo) {
        valorEstadoValor = estadoValorNuevo;
    }

    public int códigoSalir() {
        return códigoSalir;
    }

    public void programaSalir(int valor) {
        códigoSalir = valor & 0xff;
        valorEstadoValor = estadoValorProceso.programaSalir;
    }

    public int interrumpirBuclePrograma() {
        return interrumpirBuclePrograma;
    }

    public void establecerInterrumpirBuclePrograma(int finNuevo) {
        if (finNuevo < 0x06000000 || finNuevo > 0x07000000) {
            throw new IllegalArgumentException("Programa terminación 범위를 벗어났습니다.");
        }
        interrumpirBuclePrograma = finNuevo;
    }

    public void establecerContextoEjecución(int iniciarDirección, String[] argumentoParámetro, String[] entorno) {
        direcciónIniciarEjecución = iniciarDirección;
        argumentoEjecución = argumentoParámetro.clone();
        valorEntorno = entorno.clone();
    }

    public int direcciónIniciarEjecución() { return direcciónIniciarEjecución; }
    public String[] argumentoEjecución() { return argumentoEjecución.clone(); }
    public String[] valorEntorno() { return valorEntorno.clone(); }
}
