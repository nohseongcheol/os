#include "ContratoEjemplo.h"
int main(void) {
    const char Datos[]="C Archivo: Español 😀\n";
    int Archivo=abrirArchivo("c.txt",EscribirLeer|AusenteSiCrear|ContenidoTruncar,0600);
    if(Archivo<0)return 1;
    if(escribirDatosArchivo(Archivo,Datos,sizeof(Datos)-1)!=sizeof(Datos)-1)return 2;
    if(posicionarArchivo(Archivo,0,PrincipioDesde)!=0)return 3;
    char leerValorTexto[128]={0};int longitud=leerDatosArchivo(Archivo,leerValorTexto,sizeof(leerValorTexto)-1);
    cerrarArchivo(Archivo);
    if(longitud!=sizeof(Datos)-1)return 4;
    for(int númeroValor=0;númeroValor<longitud;númeroValor++)if(Datos[númeroValor]!=leerValorTexto[númeroValor])return 5;
    return Salida(leerValorTexto);
}
