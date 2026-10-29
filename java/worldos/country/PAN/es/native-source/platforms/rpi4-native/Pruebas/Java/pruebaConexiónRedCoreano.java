// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import español.propio.*;

/** Prueba del contrato de comunicación ejecutando el mismo código de bytes en OpenJDK y en la JVM propia. */
public class pruebaConexiónRedCoreano {
    public static void main(String[] argumentos) throws ExcepciónSalidaEntrada {
        recibirPuerto valorPuerto = transporteConexión.abrirReceptor(0);
        Conexión valorInvitado = transporteConexión.abrir("127.0.0.1", valorPuerto.númeroPuerto());
        Conexión identificadorPropietario = valorPuerto.recibir();
        valorInvitado.tiempoEspera(200); identificadorPropietario.tiempoEspera(200);
        Comprobaciones.exigir(valorInvitado.conectado() && !valorInvitado.esCerrado(), "conectar valorEstadoValor");
        Comprobaciones.exigir(identificadorPropietario.númeroPuerto() == valorInvitado.númeroPuertoLocal(), "valorParRed númeroPuerto");
        Comprobaciones.exigir(valorInvitado.númeroPuerto() == identificadorPropietario.númeroPuertoLocal(), "ámbitoLocal númeroPuerto");
        FlujoEntrada valorEntrada = identificadorPropietario.valorEntrada(); FlujoSalida páginaSalida = valorInvitado.Salida();
        byte[] mensaje = Caracteres.codificar("한글 valorFlujo");
        páginaSalida.escribir(mensaje, 0, mensaje.length); páginaSalida.emitirValor();
        byte[] textoRecibido = new byte[mensaje.length];
        int leerNúmeroElementos = 0;
        while (leerNúmeroElementos < textoRecibido.length) {
            int leerAdicional = valorEntrada.leer(textoRecibido, leerNúmeroElementos, textoRecibido.length - leerNúmeroElementos);
            Comprobaciones.exigir(leerAdicional > 0, "예상하지 않은 Archivo terminación"); leerNúmeroElementos += leerAdicional;
        }
        Comprobaciones.exigir(Caracteres.textoIgual(Caracteres.descifrarDatos(textoRecibido), "한글 valorFlujo"), "valorSubparte 읽기와 escribir");
        páginaSalida.escribir(new byte[] {17, 18});
        byte[] leerCorto = new byte[2];
        int leerPrimero = valorEntrada.leer(leerCorto);
        Comprobaciones.exigir(leerPrimero > 0 && leerCorto[0] == 17, "valorArreglo leer");
        if (leerPrimero == 1) leerCorto[1] = (byte)valorEntrada.leer();
        Comprobaciones.exigir(leerCorto[1] == 18, "valorRestoDivisión leer");
        identificadorPropietario.Salida().escribir(255);
        Comprobaciones.exigir(valorInvitado.valorEntrada().leer() == 255, "valorCodificaciónEstado 없는 한 valorByte");
        páginaSalida.cerrar();
        Comprobaciones.exigir(valorInvitado.esCerrado() && valorEntrada.leer() == -1, "닫기와 Archivo terminación");
        valorEntrada.cerrar(); Comprobaciones.exigir(identificadorPropietario.esCerrado(), "valorEntrada valorFlujo cerrar");
        valorInvitado.cerrar(); identificadorPropietario.cerrar();
        valorPuerto.tiempoEspera(15);
        boolean tiempoEsperaEjecución = false;
        try { valorPuerto.recibir(); } catch (ExcepciónTiempoEsperaEsperar errorEsperado) { tiempoEsperaEjecución = true; }
        Comprobaciones.exigir(tiempoEsperaEjecución, "recibirValor tiempoEspera");
        valorPuerto.cerrar(); Comprobaciones.exigir(valorPuerto.esCerrado(), "recibirPuerto cerrar");
        CanalDatagrama extremoReceptor = CanalDatagrama.abrir(0), extremoEnvíoEnCurso = CanalDatagrama.abrir(0);
        extremoReceptor.tiempoEspera(200);
        extremoEnvíoEnCurso.enviar("127.0.0.1", extremoReceptor.númeroPuerto(), "datagrama 한글");
        Comprobaciones.exigir(Caracteres.textoIgual(extremoReceptor.recibir(), "datagrama 한글"), "datagrama 송수신");
        extremoEnvíoEnCurso.cerrar(); extremoReceptor.cerrar();
        Comprobaciones.exigir(extremoEnvíoEnCurso.esCerrado() && extremoReceptor.esCerrado(), "datagrama cerrar");
        Salida.escribirLínea("español Comunicación verificar: conectar datagrama valorFlujo tiempoEsperaEjecución cerrar");
    }
}
