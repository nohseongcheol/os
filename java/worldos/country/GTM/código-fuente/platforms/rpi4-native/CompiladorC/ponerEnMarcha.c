#include "../denominación/nombresEnlazarMáquina.h"
#include "invocar.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *salidaC(size_t *);
extern const char *fuenteCompilaciónJavaAnticipada(const char *);
typedef struct { unsigned char valorIdentificador[16];uint16_t categoríaTipo,tipoMáquina;uint32_t númeroVersión;uint64_t puntoEntradaElemento,desfaseEncabezadoPrograma,desfaseEncabezadoSección;uint32_t bitsConfiguración;uint16_t tamaño,tamañoEncabezadoPrograma,númeroElementosEncabezadoPrograma,tamañoEncabezadoSección,númeroElementosEncabezadoSección,tablaNombreSección; } valorEncabezado;
typedef struct {uint32_t categoríaTipo,bitsConfiguración;uint64_t valorDesfase,dirección,direcciónFísico,tamañoZonaArchivo,tamañoZonaMemoria,fronteraAlinear;} valorSegmento;
static unsigned char imagen[16384];
static int entradaElementoPublicar(const char *nombre){
    size_t númeroElementosElementoLista;const unsigned char*datosOriginal=salidaC(&númeroElementosElementoLista);if(númeroElementosElementoLista<sizeof(valorEncabezado))return -1;
    valorEncabezado encabezadoCódigoEjecutable;memcpy(&encabezadoCódigoEjecutable,datosOriginal,sizeof(encabezadoCódigoEjecutable));
    if(encabezadoCódigoEjecutable.categoríaTipo!=2||encabezadoCódigoEjecutable.tipoMáquina!=183||encabezadoCódigoEjecutable.tamañoEncabezadoPrograma!=sizeof(valorSegmento)||!encabezadoCódigoEjecutable.númeroElementosEncabezadoPrograma||encabezadoCódigoEjecutable.númeroElementosEncabezadoPrograma>16||encabezadoCódigoEjecutable.desfaseEncabezadoPrograma>númeroElementosElementoLista||encabezadoCódigoEjecutable.númeroElementosEncabezadoPrograma*sizeof(valorSegmento)>númeroElementosElementoLista-encabezadoCódigoEjecutable.desfaseEncabezadoPrograma)return -1;
    encabezadoCódigoEjecutable.desfaseEncabezadoPrograma=sizeof(encabezadoCódigoEjecutable);encabezadoCódigoEjecutable.desfaseEncabezadoSección=encabezadoCódigoEjecutable.númeroElementosEncabezadoSección=encabezadoCódigoEjecutable.tamañoEncabezadoSección=encabezadoCódigoEjecutable.tablaNombreSección=0;memcpy(imagen,&encabezadoCódigoEjecutable,sizeof(encabezadoCódigoEjecutable));
    size_t informaciónAuxiliar=sizeof(encabezadoCódigoEjecutable)+encabezadoCódigoEjecutable.númeroElementosEncabezadoPrograma*sizeof(valorSegmento),elementoListaSiguiente=4096;unsigned char listaPágina[3072]={0};int puntoEntradaElementoVálido=0;
    for(unsigned índiceOrdinal=0;índiceOrdinal<encabezadoCódigoEjecutable.númeroElementosEncabezadoPrograma;índiceOrdinal++){
        valorSegmento posiciónDatos;valorEncabezado original;memcpy(&original,datosOriginal,sizeof(original));memcpy(&posiciónDatos,datosOriginal+original.desfaseEncabezadoPrograma+índiceOrdinal*sizeof(posiciónDatos),sizeof(posiciónDatos));
        if(posiciónDatos.valorDesfase>númeroElementosElementoLista||posiciónDatos.tamañoZonaArchivo>númeroElementosElementoLista-posiciónDatos.valorDesfase||posiciónDatos.tamañoZonaArchivo>posiciónDatos.tamañoZonaMemoria)return -1;
        if(posiciónDatos.categoríaTipo==1){
            if((posiciónDatos.bitsConfiguración&~7u)||!(posiciónDatos.bitsConfiguración&4)||(posiciónDatos.bitsConfiguración&3)==3||posiciónDatos.dirección<0x02000000||posiciónDatos.dirección>0x02c00000||posiciónDatos.tamañoZonaMemoria>0x02c00000-posiciónDatos.dirección)return -1;
            if((posiciónDatos.bitsConfiguración&1)&&encabezadoCódigoEjecutable.puntoEntradaElemento>=posiciónDatos.dirección&&encabezadoCódigoEjecutable.puntoEntradaElemento-posiciónDatos.dirección<posiciónDatos.tamañoZonaArchivo&&!(encabezadoCódigoEjecutable.puntoEntradaElemento&3))puntoEntradaElementoVálido=1;
            size_t valorPrecedente=posiciónDatos.dirección&4095,valoresByte=posiciónDatos.tamañoZonaArchivo?valorPrecedente+posiciónDatos.tamañoZonaArchivo:0;
            if(elementoListaSiguiente>sizeof(imagen)||valoresByte>sizeof(imagen)-elementoListaSiguiente){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(elementoListaSiguiente+valoresByte),(unsigned)sizeof(imagen));return -1;}
            if(valoresByte)memcpy(imagen+elementoListaSiguiente+valorPrecedente,datosOriginal+posiciónDatos.valorDesfase,posiciónDatos.tamañoZonaArchivo);
            posiciónDatos.dirección-=valorPrecedente;posiciónDatos.direcciónFísico=posiciónDatos.dirección;posiciónDatos.tamañoZonaMemoria+=valorPrecedente;posiciónDatos.tamañoZonaArchivo=valoresByte;posiciónDatos.valorDesfase=elementoListaSiguiente;posiciónDatos.fronteraAlinear=4096;
            for(uint64_t valorPágina=posiciónDatos.dirección;valorPágina<posiciónDatos.dirección+posiciónDatos.tamañoZonaMemoria;valorPágina+=4096){unsigned índiceBuscar=(valorPágina-0x02000000)/4096;if(índiceBuscar>=sizeof(listaPágina)||listaPágina[índiceBuscar]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}listaPágina[índiceBuscar]=1;}
            elementoListaSiguiente+=(valoresByte+4095)&~(size_t)4095;
        }else if(posiciónDatos.categoríaTipo==4){if(posiciónDatos.tamañoZonaArchivo>4096-informaciónAuxiliar)return -1;memcpy(imagen+informaciónAuxiliar,datosOriginal+posiciónDatos.valorDesfase,posiciónDatos.tamañoZonaArchivo);posiciónDatos.valorDesfase=informaciónAuxiliar;informaciónAuxiliar+=posiciónDatos.tamañoZonaArchivo;}
        else if(posiciónDatos.categoríaTipo!=0&&posiciónDatos.categoríaTipo!=6&&posiciónDatos.categoríaTipo!=0x6474e551)return -1;
        memcpy(imagen+encabezadoCódigoEjecutable.desfaseEncabezadoPrograma+índiceOrdinal*sizeof(posiciónDatos),&posiciónDatos,sizeof(posiciónDatos));
    }
    if(!puntoEntradaElementoVálido)return -1;
    intptr_t manejadorArchivo=invocarUsuario(3,(uintptr_t)nombre,577,0600,0,0,0);if(manejadorArchivo<0){printf("cc: cannot create output file, error %d\n",(int)manejadorArchivo);return -1;}
    intptr_t escrito=invocarUsuario(1,manejadorArchivo,(uintptr_t)imagen,elementoListaSiguiente,0,0,0);invocarUsuario(4,manejadorArchivo,0,0,0,0,0);return escrito==(intptr_t)elementoListaSiguiente?0:-1;
}
int iniciarProgramaUsuario(int modoMétodo){
    char entrada[256],entradaElementoSeleccionado[256],salida[256]="a.elf";
    int númeroElementosArgumentos=invocarUsuario(15,UINTPTR_MAX,0,0,0,0,0);
    if(númeroElementosArgumentos!=1&&númeroElementosArgumentos!=3){printf(modoMétodo?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(invocarUsuario(15,0,(uintptr_t)entrada,sizeof(entrada),0,0,0)<0)return 2;
    if(númeroElementosArgumentos==1&&(!strcmp(entrada,"--version")||!strcmp(entrada,"-version"))){printf(modoMétodo?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(númeroElementosArgumentos==3){invocarUsuario(15,1,(uintptr_t)entradaElementoSeleccionado,sizeof(entradaElementoSeleccionado),0,0,0);if(strcmp(entradaElementoSeleccionado,"-o")||invocarUsuario(15,2,(uintptr_t)salida,sizeof(salida),0,0,0)<0)return 2;}
    if(!strcmp(entrada,salida)){printf("cc: input and output must differ\n");return 2;}
    TCCState*datosCadena=tcc_new();if(!datosCadena)return 1;
    tcc_undefine_symbol(datosCadena,"__linux__");tcc_undefine_symbol(datosCadena,"__linux");tcc_undefine_symbol(datosCadena,"linux");
    tcc_undefine_symbol(datosCadena,"__unix__");tcc_undefine_symbol(datosCadena,"__unix");tcc_undefine_symbol(datosCadena,"unix");
    tcc_undefine_symbol(datosCadena,"__STDC_HOSTED__");tcc_define_symbol(datosCadena,"__STDC_HOSTED__","0");tcc_define_symbol(datosCadena,"__JKOROS__","1");
    tcc_set_options(datosCadena,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(datosCadena,"/sdk/include");
    int valorDevuelto=tcc_set_output_type(datosCadena,TCC_OUTPUT_EXE);
    if(!valorDevuelto){if(modoMétodo){const char*datosOriginal=fuenteCompilaciónJavaAnticipada(entrada);valorDevuelto=datosOriginal?tcc_compile_string(datosCadena,datosOriginal):-1;}else valorDevuelto=tcc_add_file(datosCadena,entrada);}
    if(!valorDevuelto)valorDevuelto=tcc_add_file(datosCadena,"/sdk/lib/start.o");
    if(!valorDevuelto)valorDevuelto=tcc_add_file(datosCadena,"/sdk/lib/crt.o");
    if(!valorDevuelto&&modoMétodo)valorDevuelto=tcc_add_file(datosCadena,"/sdk/lib/aot-runtime.o");
    if(!valorDevuelto)valorDevuelto=tcc_add_file(datosCadena,"/sdk/lib/libposix-kor-user.a");
    if(!valorDevuelto)valorDevuelto=tcc_output_file(datosCadena,"/@cc-output");
    if(!valorDevuelto)valorDevuelto=entradaElementoPublicar(salida);
    tcc_delete(datosCadena);
    if(valorDevuelto){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(modoMétodo?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",salida);return 0;
}
