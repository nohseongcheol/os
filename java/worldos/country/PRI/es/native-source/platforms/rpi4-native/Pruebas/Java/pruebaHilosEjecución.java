// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class valorContador {
    int númeroValor;
    synchronized void añadirValores() { int valorLadoDelantero = númeroValor; Thread.yield(); númeroValor = valorLadoDelantero + 1; }
}
class AcciónTarea implements Runnable {
    valorContador referenciaContador; AcciónTarea(valorContador referenciaContador) { this.referenciaContador = referenciaContador; }
    public void run() { for (int i = 0; i < 20; i++) referenciaContador.añadirValores(); }
}
class valorHiloEjecución extends Thread { public void run() { synchronized (pruebaHilosEjecución.valorCerrojo) { pruebaHilosEjecución.esTerminado = 1; } } }
public class pruebaHilosEjecución {
    static Object valorCerrojo = new Object(); static int esTerminado;
    public static void main(String[] a) throws Exception {
        valorContador referenciaContador = new valorContador(); Thread valorUno = new Thread(new AcciónTarea(referenciaContador)); Thread valorDos = new Thread(new AcciónTarea(referenciaContador));
        valorUno.start(); valorDos.start(); valorUno.join(); valorDos.join(); System.out.println(referenciaContador.númeroValor); System.out.println(valorUno.isAlive());
        valorHiloEjecución elementoListaTercero = new valorHiloEjecución(); elementoListaTercero.start(); elementoListaTercero.join(); System.out.println(esTerminado);
        try { valorUno.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 rechazarValor"); }
        System.out.println("valorHiloEjecución esTerminado");
    }
}
