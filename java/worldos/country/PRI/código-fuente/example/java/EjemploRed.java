// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import español.propio.Conexión;
import español.propio.Argumentos;
import español.propio.CanalDatagrama;
import español.propio.Caracteres;
import español.propio.Salida;
import español.propio.Comprobaciones;
import español.propio.FlujoEntrada;
import español.propio.ExcepciónSalidaEntrada;

public class EjemploRed {
    public static void ponerEnMarcha() throws ExcepciónSalidaEntrada {
        // Anfitrión: python3 Herramientas/repetirEntradaEjemplo.py --tcp-port 9000 --udp-port 9001
        Conexión conectar = Conexión.abrir("10.0.2.2", Caracteres.analizarEnteroValor(Argumentos.texto(0)));
        try {
            conectar.tiempoEspera(700);
            byte[] mensaje = Caracteres.codificar("JAVA TCP Español\n");
            conectar.Salida().escribir(mensaje);
            FlujoEntrada valorEntrada = conectar.valorEntrada();
            for (int númeroValor = 0; númeroValor < Caracteres.númeroElementosByte(mensaje); númeroValor++) {
                Comprobaciones.exigir(valorEntrada.leer() == (mensaje[númeroValor] & 255), "TCP respuesta 불일치");
            }
        } finally { conectar.cerrar(); }
        CanalDatagrama extremo = CanalDatagrama.abrir(0);
        try {
            extremo.tiempoEspera(700);
            extremo.enviar("10.0.2.2", Caracteres.analizarEnteroValor(Argumentos.texto(1)), "JAVA UDP Español");
            Comprobaciones.exigir(Caracteres.textoIgual(extremo.recibir(), "JAVA UDP Español"), "UDP respuesta 불일치");
        } finally { extremo.cerrar(); }
        Salida.escribirLínea("JAVA 네트워크 verificar: TCP UDP Español");
    }
}
