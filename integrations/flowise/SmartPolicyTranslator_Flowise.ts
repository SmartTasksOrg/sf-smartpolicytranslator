import { INode, INodeData, INodeParams } from 'flowise-components';
/** Flowise tool: regulation -> IAIso policy via SmartPolicyTranslator. */
class SmartPolicyTranslator_Tools implements INode {
  label = 'SmartPolicyTranslator'; name = 'smartPolicyTranslator'; version = 1.0;
  type = 'SPT'; category = 'Tools'; baseClasses = ['Tool'];
  description = 'Translate regulation into a REAL IAIso policy file';
  inputs: INodeParams[] = [
    { label: 'Base URL', name: 'baseUrl', type: 'string', default: 'http://localhost:8000' } ];
  async init(nodeData: INodeData): Promise<any> {
    const baseUrl = (nodeData.inputs?.baseUrl as string) || 'http://localhost:8000';
    return { name: 'smart_policy_translator',
      description: 'Input: regulation text/path/URL. Output: IAIso policy JSON.',
      func: async (input: string): Promise<string> => {
        const res = await fetch(`${baseUrl}/translate`, { method: 'POST',
          headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ uri: input }) });
        return await res.text();
      } };
  }
}
module.exports = { nodeClass: SmartPolicyTranslator_Tools };
