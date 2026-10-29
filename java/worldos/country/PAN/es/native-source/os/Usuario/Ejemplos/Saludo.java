// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class Saludo {
    public static int ponerEnMarcha() {
        Usuario.escribir("Hello from a separate Java ELF!\n");
        Usuario.escribir(Usuario.permisoEjecución() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int número = 0; número < Usuario.númeroElementosArgumentos(); número++) {
            Usuario.escribir("arg: "); Usuario.escribir(Usuario.argumentos(número)); Usuario.escribir("\n");
        }
        return Usuario.permisoEjecución() == 3 ? 0 : 1;
    }
}
