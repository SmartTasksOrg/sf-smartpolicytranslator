package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	spt "github.com/SmartTasksOrg/sf-smartpolicytranslator/ports/go"
)

func main() {
	ds, out := os.Args[1], os.Args[2]
	os.MkdirAll(out, 0o755)
	c := spt.New(os.Getenv("SPT_URL"))
	files, _ := filepath.Glob(filepath.Join(ds, "*.txt"))
	for _, f := range files {
		b, _ := os.ReadFile(f)
		res, err := c.Translate(string(b), false, "lmstudio")
		if err != nil {
			panic(err)
		}
		name := strings.TrimSuffix(filepath.Base(f), ".txt")
		j, _ := json.MarshalIndent(res, "", "  ")
		os.WriteFile(filepath.Join(out, name+".policy.json"), j, 0o644)
		pol := res["iaiso_policy"].(map[string]any)
		fmt.Printf("  %s: %v\n", name, pol["enforcement_mode"])
	}
}
