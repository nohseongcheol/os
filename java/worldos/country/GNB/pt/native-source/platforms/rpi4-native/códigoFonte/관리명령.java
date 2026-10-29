// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String concluído_Word() { return "configurar-ip endereço-ip testar-eco rotas ligações processos atividade memória armazenamento tempo-ativo desligar ajuda"; }
    static String Word_SMS(int ÍNDICE) {
        if (ÍNDICE==0) return "configurar-ip";
        if (ÍNDICE==1) return "endereço-ip";
        if (ÍNDICE==2) return "testar-eco";
        if (ÍNDICE==3) return "rotas";
        if (ÍNDICE==4) return "ligações";
        if (ÍNDICE==5) return "processos";
        if (ÍNDICE==6) return "atividade";
        if (ÍNDICE==7) return "memória";
        if (ÍNDICE==8) return "armazenamento";
        if (ÍNDICE==9) return "tempo-ativo";
        if (ÍNDICE==10) return "desligar";
        return "ajuda";
    }
    static String 설명(int ÍNDICE) {
        if (ÍNDICE==0) return "IPv4 settings: address, netmask, gateway";
        if (ÍNDICE==1) return "IPv4 interface and route tools";
        if (ÍNDICE==2) return "ICMP echo and round-trip time";
        if (ÍNDICE==3) return "Connected network and default route";
        if (ÍNDICE==4) return "TCP/UDP sockets and traffic";
        if (ÍNDICE==5) return "Kernel tasks and user processes";
        if (ÍNDICE==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (ÍNDICE==7) return "Actual kernel pools and user mappings";
        if (ÍNDICE==8) return "RAM filesystem capacity and file slots";
        if (ÍNDICE==9) return "Time since boot";
        if (ÍNDICE==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
