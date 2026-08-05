import { IExecuteFunctions, INodeExecutionData, INodeType, INodeTypeDescription,
  NodeConnectionType } from 'n8n-workflow';

/** n8n node: regulation text -> IAIso policy via a running SmartPolicyTranslator. */
export class SmartPolicyTranslator implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'SmartPolicyTranslator', name: 'smartPolicyTranslator',
    group: ['transform'], version: 1,
    description: 'Translate regulation into a REAL IAIso policy file',
    defaults: { name: 'SmartPolicyTranslator' },
    inputs: ['main' as NodeConnectionType], outputs: ['main' as NodeConnectionType],
    properties: [
      { displayName: 'Base URL', name: 'baseUrl', type: 'string', default: 'http://localhost:8000', required: true },
      { displayName: 'Source (text/path/URL)', name: 'uri', type: 'string', default: '', required: true, typeOptions: { rows: 4 } },
      { displayName: 'Use LLM', name: 'useLlm', type: 'boolean', default: false },
      { displayName: 'Provider', name: 'provider', type: 'options', default: 'lmstudio',
        options: [ { name: 'LM Studio', value: 'lmstudio' }, { name: 'Ollama', value: 'ollama' }, { name: 'llama.cpp', value: 'llamacpp' } ] },
    ],
  };
  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData(); const out: INodeExecutionData[] = [];
    for (let i = 0; i < items.length; i++) {
      const baseUrl = this.getNodeParameter('baseUrl', i) as string;
      const res = await this.helpers.httpRequest({ method: 'POST', url: `${baseUrl}/translate`,
        body: { uri: this.getNodeParameter('uri', i), use_llm: this.getNodeParameter('useLlm', i),
                provider: this.getNodeParameter('provider', i) }, json: true });
      out.push({ json: res });
    }
    return [out];
  }
}
