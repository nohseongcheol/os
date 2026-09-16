/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <sistema/stat.h>
#include <sistema/identidade_do_sistema.h>
#include <sistema/syscall.h>

enum { SYS_estado_do_ficheiro = 106, SYS_obter_estado_da_ligação_em_si = 107, SYS_obter_estado_do_ficheiro_aberto = 108, SYS_obter_informações_do_sistema = 122 };

int estado_do_ficheiro(const char *caminho, struct estado_do_ficheiro *memória_intermédia_de_transferência)
{
    return (int)__syscall_result(
        __syscall6(SYS_estado_do_ficheiro, (long)caminho, (long)memória_intermédia_de_transferência, 0, 0, 0, 0));
}

int obter_estado_da_ligação_em_si(const char *caminho, struct estado_do_ficheiro *memória_intermédia_de_transferência)
{
    return (int)__syscall_result(
        __syscall6(SYS_obter_estado_da_ligação_em_si, (long)caminho, (long)memória_intermédia_de_transferência, 0, 0, 0, 0));
}

int obter_estado_do_ficheiro_aberto(int descritor_do_ficheiro, struct estado_do_ficheiro *memória_intermédia_de_transferência)
{
    return (int)__syscall_result(
        __syscall6(SYS_obter_estado_do_ficheiro_aberto, descritor_do_ficheiro, (long)memória_intermédia_de_transferência, 0, 0, 0, 0));
}

int obter_informações_do_sistema(struct utsname *identidade_do_sistema)
{
    return (int)__syscall_result(
        __syscall6(SYS_obter_informações_do_sistema, (long)identidade_do_sistema, 0, 0, 0, 0, 0));
}
