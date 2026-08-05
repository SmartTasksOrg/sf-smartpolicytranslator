import Foundation
import SPTClient

let ds = CommandLine.arguments[1]
let out = CommandLine.arguments[2]
try? FileManager.default.createDirectory(atPath: out, withIntermediateDirectories: true)
let spt = SPTClient(baseURL: ProcessInfo.processInfo.environment["SPT_URL"] ?? "http://localhost:8000")
let files = (try? FileManager.default.contentsOfDirectory(atPath: ds)) ?? []
let sem = DispatchSemaphore(value: 0)
Task {
    for f in files.filter({ $0.hasSuffix(".txt") }).sorted() {
        let text = (try? String(contentsOfFile: "\(ds)/\(f)", encoding: .utf8)) ?? ""
        let res = try await spt.translate(uri: text)
        let name = (f as NSString).deletingPathExtension
        let data = try JSONSerialization.data(withJSONObject: res, options: .prettyPrinted)
        try? data.write(to: URL(fileURLWithPath: "\(out)/\(name).policy.json"))
        if let p = res["iaiso_policy"] as? [String: Any] { print("  \(name): \(p["enforcement_mode"] ?? "")") }
    }
    sem.signal()
}
sem.wait()
