// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "SPTClient",
    products: [.library(name: "SPTClient", targets: ["SPTClient"])],
    targets: [
        .target(name: "SPTClient", path: "Sources/SPTClient"),
        .executableTarget(name: "demo", dependencies: ["SPTClient"], path: "Sources/demo"),
    ]
)
