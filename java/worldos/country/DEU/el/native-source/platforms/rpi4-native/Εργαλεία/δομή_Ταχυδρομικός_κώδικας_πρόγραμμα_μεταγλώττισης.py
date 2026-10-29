"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def ανοίγω_Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης(ρίζα_διαδρομή, αποθετήριο_διαδρομή, Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, πρόγραμμα_σύνδεσης_εργαλείο, ρυθμίσεις_Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο, εκτελώ_εντολή):
    μέτρηση_δεδομένα = ρίζα_διαδρομή / 'build/ccompiler'; μέτρηση_δεδομένα.mkdir(exist_ok=True)
    원본자료 = ρίζα_διαδρομή / 'Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης'
    ανοδικός = ρίζα_διαδρομή / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    κιτ_ανάπτυξης_λογισμικού = ρίζα_διαδρομή / 'vendor/sdk'
    if not (κιτ_ανάπτυξης_λογισμικού/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((κιτ_ανάπτυξης_λογισμικού/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    ρυθμίσεις_Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο = [Ρυθμίσεις_τιμή for Ρυθμίσεις_τιμή in ρυθμίσεις_Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο if Ρυθμίσεις_τιμή != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', ανοδικός, '-I', ρίζα_διαδρομή/'χρήστης', '-I', μέτρηση_δεδομένα, '-isystem', κιτ_ανάπτυξης_λογισμικού/'usr/include']
    εκτελώ_εντολή([Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης]+ρυθμίσεις_Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'시작지원.c','-o',μέτρηση_δεδομένα/'crt.o'])
    εκτελώ_εντολή([Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης]+ρυθμίσεις_Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο+['-I',αποθετήριο_διαδρομή/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',μέτρηση_δεδομένα/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+δεδομένα_θέση.name,δεδομένα_θέση) for δεδομένα_θέση in sorted((αποθετήριο_διαδρομή/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+δεδομένα_θέση.name,δεδομένα_θέση) for δεδομένα_θέση in sorted((ανοδικός/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+δεδομένα_θέση.name,δεδομένα_θέση) for δεδομένα_θέση in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',ρίζα_διαδρομή/'build/user/start.o'),('/sdk/lib/crt.o',μέτρηση_δεδομένα/'crt.o'),('/sdk/lib/aot-runtime.o',μέτρηση_δεδομένα/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',ρίζα_διαδρομή/'build/libposix-kor-user.a')]
    κεφαλίδα_τιμή=['typedef struct { const char *Όνομα; const unsigned char *δεδομένα; unsigned Μέγεθος; } πρόγραμμα_μεταγλώττισης_πόρος;']
    for 순번,(_,ΔΙΑΔΡΟΜΗ) in enumerate(탑재자료):
        κεφαλίδα_τιμή.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in ΔΙΑΔΡΟΜΗ.read_bytes())))
    κεφαλίδα_τιμή.append('static const πρόγραμμα_μεταγλώττισης_πόρος πρόγραμμα_μεταγλώττισης_Πόροι[] = {')
    for 순번,(Όνομα,ΔΙΑΔΡΟΜΗ) in enumerate(탑재자료): κεφαλίδα_τιμή.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Όνομα,ensure_ascii=False),순번,ΔΙΑΔΡΟΜΗ.stat().st_size))
    κεφαλίδα_τιμή.append('};');(μέτρηση_δεδομένα/'resources.h').write_text('\n'.join(κεφαλίδα_τιμή)+'\n',encoding='utf-8')
    προορισμός_Αρχεία=[]
    for Όνομα in ('πρόγραμμα_μεταγλώττισης_εργαλείο.c','περιβάλλον_εκτέλεσης_στήριγμα.c','Εκτέλεση_2.c','미리번역.c','επιστρέφω_γέφυρα.S'):
        αρχείο_προορισμού=μέτρηση_δεδομένα/(Path(Όνομα).stem+'.o');προορισμός_Αρχεία.append(αρχείο_προορισμού)
        εκτελώ_εντολή([Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης]+ρυθμίσεις_Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Όνομα,'-o',αρχείο_προορισμού])
    εκτελέσιμο=ρίζα_διαδρομή/'build/user/cc.elf'
    εκτελώ_εντολή([πρόγραμμα_σύνδεσης_εργαλείο,'--gc-sections','-T',ρίζα_διαδρομή/'χρήστης/συνδέω_Διάταξη.ld','-z','max-page-size=4096','-o',εκτελέσιμο,
         ρίζα_διαδρομή/'build/user/start.o',ρίζα_διαδρομή/'build/user/runtime.o']+προορισμός_Αρχεία+
         [ρίζα_διαδρομή/'build/user'/Όνομα for Όνομα in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
