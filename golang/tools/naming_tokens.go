// Token-only renaming: comments, literals and executable operations are preserved.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"go/parser"
	"go/scanner"
	"go/token"
	"io/ioutil"
	"os"
	"strconv"
)

type request struct {
	Files   []string
	Names   map[string]string
	Imports map[string]string
}
type result struct {
	Path         string
	Source       string
	Replacements int
	Counts       map[string]int
}

func transform(path string, names, imports map[string]string) result {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		panic(err)
	}
	fset := token.NewFileSet()
	f, err := parser.ParseFile(fset, path, data, parser.ParseComments)
	if err != nil {
		panic(err)
	}
	importOffsets := map[int]bool{}
	for _, imp := range f.Imports {
		importOffsets[fset.Position(imp.Path.Pos()).Offset] = true
	}
	var scan scanner.Scanner
	scan.Init(fset.AddFile(path, -1, len(data)), data, nil, scanner.ScanComments)
	var output bytes.Buffer
	last := 0
	r := result{Path: path, Counts: map[string]int{}}
	for {
		pos, kind, lit := scan.Scan()
		if kind == token.EOF {
			break
		}
		offset := fset.Position(pos).Offset
		replacement := ""
		if kind == token.IDENT {
			replacement = names[lit]
		}
		if kind == token.STRING && importOffsets[offset] {
			value, e := strconv.Unquote(lit)
			if e != nil {
				panic(e)
			}
			if target := imports[value]; target != "" && value != target {
				replacement = strconv.Quote(target)
			}
		}
		if replacement != "" && replacement != lit {
			output.Write(data[last:offset])
			output.WriteString(replacement)
			last = offset + len(lit)
			if kind == token.IDENT {
				r.Replacements++
				r.Counts[lit]++
			}
		}
	}
	output.Write(data[last:])
	if _, err := parser.ParseFile(token.NewFileSet(), path, output.Bytes(), parser.ParseComments); err != nil {
		panic(err)
	}
	r.Source = output.String()
	return r
}

func main() {
	var req request
	if err := json.NewDecoder(os.Stdin).Decode(&req); err != nil {
		panic(err)
	}
	enc := json.NewEncoder(os.Stdout)
	for _, path := range req.Files {
		if err := enc.Encode(transform(path, req.Names, req.Imports)); err != nil {
			panic(fmt.Sprint(err))
		}
	}
}
