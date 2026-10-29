"""Class-file reader and instruction decoder shared by AOT and dependency audit.

This validates file structure and instruction boundaries, not JVM type safety.
"""
import struct
import zipfile
from pathlib import Path
from fordítóprogram import fordítási_hiba, 자료읽기, 수정유티에프해독


NAMES = '''nop aconst_null iconst_m1 iconst_0 iconst_1 iconst_2 iconst_3 iconst_4 iconst_5
lconst_0 lconst_1 fconst_0 fconst_1 fconst_2 dconst_0 dconst_1 bipush sipush ldc ldc_w ldc2_w
iload lload fload dload aload iload_0 iload_1 iload_2 iload_3 lload_0 lload_1 lload_2 lload_3
fload_0 fload_1 fload_2 fload_3 dload_0 dload_1 dload_2 dload_3 aload_0 aload_1 aload_2 aload_3
iaload laload faload daload aaload baload caload saload istore lstore fstore dstore astore
istore_0 istore_1 istore_2 istore_3 lstore_0 lstore_1 lstore_2 lstore_3
fstore_0 fstore_1 fstore_2 fstore_3 dstore_0 dstore_1 dstore_2 dstore_3 astore_0 astore_1 astore_2 astore_3
iastore lastore fastore dastore aastore bastore castore sastore pop pop2 dup dup_x1 dup_x2 dup2 dup2_x1 dup2_x2 swap
iadd ladd fadd dadd isub lsub fsub dsub imul lmul fmul dmul idiv ldiv fdiv ddiv irem lrem frem drem
ineg lneg fneg dneg ishl lshl ishr lshr iushr lushr iand land ior lor ixor lxor iinc
i2l i2f i2d l2i l2f l2d f2i f2l f2d d2i d2l d2f i2b i2c i2s lcmp fcmpl fcmpg dcmpl dcmpg
ifeq ifne iflt ifge ifgt ifle if_icmpeq if_icmpne if_icmplt if_icmpge if_icmpgt if_icmple if_acmpeq if_acmpne
goto jsr ret tableswitch lookupswitch ireturn lreturn freturn dreturn areturn return
getstatic putstatic getfield putfield invokevirtual invokespecial invokestatic invokeinterface invokedynamic
new newarray anewarray arraylength athrow checkcast instanceof monitorenter monitorexit wide multianewarray
ifnull ifnonnull goto_w jsr_w'''.split()
assert len(NAMES) == 202


def descriptor(text, method=False):
    def one(at, void=False):
        start = at
        while at < len(text) and text[at] == '[': at += 1
        if at - start > 255 or at >= len(text): raise fordítási_hiba('Invalid descriptor: ' + text)
        if text[at] == 'L':
            end = text.find(';', at)
            if end <= at + 1: raise fordítási_hiba('Invalid descriptor: ' + text)
            at = end + 1
        elif text[at] in 'ZBCSIJFD' or (void and at == start and text[at] == 'V'): at += 1
        else: raise fordítási_hiba('Invalid descriptor: ' + text)
        return text[start:at], at
    if not method:
        result, end = one(0)
        if end != len(text): raise fordítási_hiba('Invalid descriptor: ' + text)
        return result
    if not text.startswith('('): raise fordítási_hiba('Invalid method descriptor: ' + text)
    args, at = [], 1
    while at < len(text) and text[at] != ')':
        value, at = one(at); args.append(value)
    if at >= len(text): raise fordítási_hiba('Invalid method descriptor: ' + text)
    result, at = one(at + 1, True)
    if at != len(text) or sum(width(a) for a in args) > 255: raise fordítási_hiba('Invalid method descriptor: ' + text)
    return args, result


def width(desc): return 2 if desc in ('J', 'D') else (0 if desc == 'V' else 1)


def instructions(data):
    r, out, branches = 자료읽기(data), [], []
    while r.Pozíció < len(data):
        pc, op = r.Pozíció, r.szám('B')
        if op >= len(NAMES): raise fordítási_hiba('Reserved/invalid opcode 0x{:02x} at {}'.format(op, pc))
        args = []
        if op in (16, 17): args = [r.szám('b' if op == 16 else 'h')]
        elif op in (18, 188) or 21 <= op <= 25 or 54 <= op <= 58 or op == 169: args = [r.szám('B')]
        elif op in (19, 20) or 178 <= op <= 184 or op in (187, 189, 192, 193): args = [r.szám('H')]
        elif op == 132: args = [r.szám('B'), r.szám('b')]
        elif 153 <= op <= 168 or op in (198, 199, 200, 201):
            args = [pc + r.szám('i' if op >= 200 else 'h')]; branches += args
        elif op in (170, 171):
            while r.Pozíció % 4:
                if r.szám('B'): raise fordítási_hiba('Nonzero switch padding')
            default = pc + r.szám('i')
            if op == 170:
                low, high = r.szám('i'), r.szám('i')
                count = high - low + 1
                if count < 1 or count > (len(data) - r.Pozíció) // 4: raise fordítási_hiba('Invalid tableswitch size')
                pairs = [(v, pc + r.szám('i')) for v in range(low, high + 1)]
            else:
                count = r.szám('i')
                if count < 0 or count > (len(data) - r.Pozíció) // 8: raise fordítási_hiba('Invalid lookupswitch size')
                pairs = [(r.szám('i'), pc + r.szám('i')) for _ in range(count)]
                if any(pairs[i][0] >= pairs[i + 1][0] for i in range(count - 1)):
                    raise fordítási_hiba('Unsorted lookupswitch')
            args = [default, pairs]; branches += [default] + [v for _, v in pairs]
        elif op in (185, 186):
            index, a, b = r.szám('H'), r.szám('B'), r.szám('B')
            if b or (op == 186 and a) or (op == 185 and not a): raise fordítási_hiba('Invalid invoke operands')
            args = [index, a]
        elif op == 196:
            sub, index = r.szám('B'), r.szám('H')
            if sub not in tuple(range(21, 26)) + tuple(range(54, 59)) + (132, 169):
                raise fordítási_hiba('Invalid wide opcode')
            args = [sub, index]
            if sub == 132: args.append(r.szám('h'))
        elif op == 197:
            args = [r.szám('H'), r.szám('B')]
            if not args[1]: raise fordítási_hiba('Zero multianewarray dimensions')
        if op == 188 and args[0] not in range(4, 12): raise fordítási_hiba('Invalid newarray type')
        out.append((pc, op, args))
    boundaries = {pc for pc, _, _ in out}
    if any(pc not in boundaries for pc in branches): raise fordítási_hiba('Branch is not an instruction boundary')
    return out


class ClassFile:
    def __init__(self, data, origin='class'):
        self.origin = origin
        r = 자료읽기(data)
        if r.szám('I') != 0xcafebabe: raise fordítási_hiba('Invalid class magic: ' + origin)
        self.minor, self.major = r.szám('H'), r.szám('H')
        self.cp = [None] * r.szám('H')
        if not self.cp: raise fordítási_hiba('Empty constant pool')
        i = 1
        while i < len(self.cp):
            tag = r.szám('B')
            if tag == 1: value = 수정유티에프해독(r.Olvasás(r.szám('H')))
            elif tag in (3, 4): value = r.szám('I')
            elif tag in (5, 6): value = r.szám('Q')
            elif tag in (7, 8, 16, 19, 20): value = r.szám('H')
            elif tag in (9, 10, 11, 12, 17, 18): value = (r.szám('H'), r.szám('H'))
            elif tag == 15: value = (r.szám('B'), r.szám('H'))
            else: raise fordítási_hiba('Unknown constant tag {}: {}'.format(tag, origin))
            self.cp[i] = (tag, value)
            i += 2 if tag in (5, 6) else 1
            if i > len(self.cp): raise fordítási_hiba('Truncated category-2 constant')
        self.access, name, parent = r.szám('H'), r.szám('H'), r.szám('H')
        self.name, self.parent = self.classname(name), self.classname(parent) if parent else None
        self.interfaces = [self.classname(r.szám('H')) for _ in range(r.szám('H'))]
        self.fields, self.methods = self.members(r, False), self.members(r, True)
        self.attrs = self.attributes(r)
        if r.Pozíció != len(data): raise fordítási_hiba('Trailing bytes: ' + origin)

    def constant(self, index, tags):
        if index < 1 or index >= len(self.cp) or self.cp[index] is None or self.cp[index][0] not in tags:
            raise fordítási_hiba('Invalid constant #{} in {}'.format(index, self.origin))
        return self.cp[index][1]

    def utf(self, index): return self.constant(index, (1,))
    def classname(self, index): return self.utf(self.constant(index, (7,)))
    def reference(self, index, tags=(9, 10, 11)):
        owner, nt = self.constant(index, tags)
        name, desc = self.constant(nt, (12,))
        return self.classname(owner), self.utf(name), self.utf(desc)

    def attributes(self, r):
        attrs = {}
        for _ in range(r.szám('H')):
            name = self.utf(r.szám('H'))
            value = r.Olvasás(r.szám('I'))
            if name in attrs and name in ('Code', 'ConstantValue', 'BootstrapMethods'):
                raise fordítási_hiba('Duplicate attribute: ' + name)
            attrs[name] = value
        return attrs

    def members(self, r, method):
        result, seen = [], set()
        for _ in range(r.szám('H')):
            access, name, desc = r.szám('H'), self.utf(r.szám('H')), self.utf(r.szám('H'))
            descriptor(desc, method)
            if (name, desc) in seen: raise fordítási_hiba('Duplicate member: ' + name)
            seen.add((name, desc))
            result.append((access, name, desc, self.attributes(r)))
        return result

    def code(self, attrs):
        if 'Code' not in attrs: return None
        r = 자료읽기(attrs['Code'])
        stack, locals_, size = r.szám('H'), r.szám('H'), r.szám('I')
        if size < 1 or size > 65535: raise fordítási_hiba('Invalid Code length')
        code = instructions(r.Olvasás(size))
        handlers = [tuple(r.szám('H') for _ in range(4)) for _ in range(r.szám('H'))]
        boundaries = {pc for pc, _, _ in code}
        for start, end, target, catch in handlers:
            if start not in boundaries or end not in boundaries | {size} or start >= end or target not in boundaries:
                raise fordítási_hiba('Invalid exception table')
            if catch: self.classname(catch)
        self.attributes(r)
        if r.Pozíció != len(r.adat): raise fordítási_hiba('Trailing Code attribute bytes')
        return stack, locals_, code, handlers


def read_classes(paths):
    for path in map(Path, paths):
        if path.is_dir():
            for child in sorted(path.rglob('*.class')):
                yield ClassFile(child.read_bytes(), str(child))
        elif path.suffix in ('.jar', '.jmod', '.zip'):
            with zipfile.ZipFile(str(path)) as archive:
                for name in sorted(archive.namelist()):
                    if name.endswith('.class') and not name.startswith('META-INF/versions/'):
                        yield ClassFile(archive.read(name), str(path) + ':' + name)
        else: yield ClassFile(path.read_bytes(), str(path))
