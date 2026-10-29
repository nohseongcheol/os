#include "ContratoEjemplo.h"
#include <ABIRed.h>
int main(int númeroElementosArgumento,char **argumentos) {
    if(númeroElementosArgumento!=2)return Salida("사용법: ./네트워크 UDP창구번호\n");
    unsigned valorPuerto=0;for(int númeroValor=0;argumentos[1][númeroValor];númeroValor++) {
        if(argumentos[1][númeroValor]<'0'||argumentos[1][númeroValor]>'9')return 2;
        valorPuerto=valorPuerto*10+argumentos[1][númeroValor]-'0';if(valorPuerto>65535)return 2;
    }
    if(!valorPuerto)return 2;
    int extremo=crearExtremo(FamiliaInternet,ConectorRedDatagrama,ProtocoloDatagrama);if(extremo<0)return 3;
    struct DirecciónConectorRedInternet dirección={0};dirección.familiaDirección=FamiliaInternet;
    if(asociarDirección(extremo,(struct DirecciónConectorRed *)&dirección,sizeof(dirección))<0)return 4;
    dirección.númeroPuerto=cortoRed(valorPuerto);dirección.DirecciónInternet.valorDirección=enteroValorRed(0x0a000202);
    const char datagrama[]="C UDP Español";
    if(enviarDatosDatagrama(extremo,datagrama,sizeof(datagrama)-1,0,(struct DirecciónConectorRed *)&dirección,sizeof(dirección))!=sizeof(datagrama)-1)return 5;
    char respuesta[512];unsigned ponerEnMarcha=milisegundos();int númeroElementosRecibido;
    do {
        númeroElementosRecibido=recibirDatosDatagrama(extremo,respuesta,sizeof(respuesta),0,0,0);
        if(númeroElementosRecibido<0&&númeroError!=ErrorOtraVezIntentar)return 6;
    } while(númeroElementosRecibido<0&&(unsigned)(milisegundos()-ponerEnMarcha)<700);
    cerrarArchivo(extremo);if(númeroElementosRecibido!=sizeof(datagrama)-1)return 7;
    for(int númeroValor=0;númeroValor<númeroElementosRecibido;númeroValor++)if(datagrama[númeroValor]!=respuesta[númeroValor])return 8;
    return Salida("C 네트워크 verificar: UDP Español\n");
}
