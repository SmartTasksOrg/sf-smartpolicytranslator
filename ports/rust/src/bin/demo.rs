use smartpolicytranslator_client::SptClient;
use std::{env, fs};

fn main() -> Result<(), String> {
    let a: Vec<String> = env::args().collect();
    let (ds, out) = (&a[1], &a[2]);
    fs::create_dir_all(out).ok();
    let c = SptClient::new(&env::var("SPT_URL").unwrap_or_default());
    for e in fs::read_dir(ds).map_err(|e| e.to_string())? {
        let p = e.map_err(|e| e.to_string())?.path();
        if p.extension().map_or(false, |x| x == "txt") {
            let text = fs::read_to_string(&p).map_err(|e| e.to_string())?;
            let v = c.translate(&text, false, "lmstudio")?;
            let name = p.file_stem().unwrap().to_string_lossy();
            fs::write(format!("{}/{}.policy.json", out, name),
                      serde_json::to_string_pretty(&v).unwrap()).ok();
            println!("  {}: {}", name, v["iaiso_policy"]["enforcement_mode"]);
        }
    }
    Ok(())
}
