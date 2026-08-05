# Ruby client for SmartPolicyTranslator: regulation -> IAIso policy.
# Pair with the iaiso-ruby port (github.com/SmartTasksOrg/IAISO core/iaiso-ruby).
require "net/http"
require "json"
require "uri"

module SmartTasks
  class SptClient
    def initialize(base_url = "http://localhost:8000")
      @base_url = base_url.chomp("/")
    end

    # Returns the decoded translate result (contains "iaiso_policy").
    def translate(uri, use_llm: false, provider: "lmstudio")
      u = URI("#{@base_url}/translate")
      req = Net::HTTP::Post.new(u, "Content-Type" => "application/json")
      req.body = { uri: uri, use_llm: use_llm, provider: provider }.to_json
      res = Net::HTTP.start(u.hostname, u.port, read_timeout: 120) { |h| h.request(req) }
      raise "SPT #{res.code}: #{res.body}" if res.code.to_i >= 300
      JSON.parse(res.body)
    end
  end
end
