// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class ComandosAdministración {
    static String palabraCompletado() { return "configurar-ip dirección-ip probar-eco rutas conexiones procesos actividad memoria almacenamiento tiempo-activo apagar ayuda"; }
    static String textoPalabra(int número) {
        if (número==0) return "configurar-ip";
        if (número==1) return "dirección-ip";
        if (número==2) return "probar-eco";
        if (número==3) return "rutas";
        if (número==4) return "conexiones";
        if (número==5) return "procesos";
        if (número==6) return "actividad";
        if (número==7) return "memoria";
        if (número==8) return "almacenamiento";
        if (número==9) return "tiempo-activo";
        if (número==10) return "apagar";
        return "ayuda";
    }
    static String descripción(int número) {
        if (número==0) return "IPv4 settings: address, netmask, gateway";
        if (número==1) return "IPv4 interface and route tools";
        if (número==2) return "ICMP echo and round-trip time";
        if (número==3) return "Connected network and default route";
        if (número==4) return "TCP/UDP sockets and traffic";
        if (número==5) return "Kernel tasks and user processes";
        if (número==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (número==7) return "Actual kernel pools and user mappings";
        if (número==8) return "RAM filesystem capacity and file slots";
        if (número==9) return "Time since boot";
        if (número==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
