require_relative "spt_client"
require "json"
require "fileutils"
ds, out = ARGV
FileUtils.mkdir_p(out)
c = SmartTasks::SptClient.new(ENV["SPT_URL"] || "http://localhost:8000")
Dir.glob("#{ds}/*.txt").sort.each do |f|
  res = c.translate(File.read(f))
  name = File.basename(f, ".txt")
  File.write("#{out}/#{name}.policy.json", JSON.pretty_generate(res))
  puts "  #{name}: #{res["iaiso_policy"]["enforcement_mode"]}"
end
