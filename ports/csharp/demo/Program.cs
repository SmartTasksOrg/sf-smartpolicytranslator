using System.Text.Json;
using SmartTasks.Spt;

var ds = args[0]; var outDir = args[1];
Directory.CreateDirectory(outDir);
var spt = new SptClient(Environment.GetEnvironmentVariable("SPT_URL") ?? "http://localhost:8000");
foreach (var f in Directory.GetFiles(ds, "*.txt").OrderBy(x => x))
{
    var res = await spt.TranslateAsync(File.ReadAllText(f));
    var name = Path.GetFileNameWithoutExtension(f);
    File.WriteAllText(Path.Combine(outDir, name + ".policy.json"),
        JsonSerializer.Serialize(res, new JsonSerializerOptions { WriteIndented = true }));
    Console.WriteLine($"  {name}: {res.GetProperty("iaiso_policy").GetProperty("enforcement_mode")}");
}
