"""SmartPolicyTranslator — translate natural-language regulation into REAL,
schema-conformant IAIso policy files and wire them into your architecture.

Emits IAIso v1 policy documents (see spec/iaiso/policy.schema.json), validates
them against the vendored IAIso specification and its official test vectors, and
ships integrations (LangChain via the IAIso SDK, n8n, Flowise) plus language
ports (Node, Java, React) that mirror IAIso's own multi-language ports.
"""
__version__ = "1.0.0"
FRAMEWORK = "IAIso"
