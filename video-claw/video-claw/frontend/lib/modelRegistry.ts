import type { ProviderGroup } from '@/config/models';
import { fetchApiModels } from '@/lib/workflowApi';

const PROVIDER_LABELS: Record<string, string> = {
  dashscope: 'DashScope',
  ark: 'ARK (Volcengine)',
  deepseek: 'DeepSeek',
  openai: 'OpenAI',
  atlascloud: 'Atlas Cloud',
  gemini: 'Gemini',
  kling: 'Kling',
};

export function groupModelOptions(
  models: Array<{ id: string; label?: string; provider?: string }>,
): ProviderGroup[] {
  const groups = new Map<string, ProviderGroup>();
  for (const model of models) {
    const provider = model.provider || 'unknown';
    if (!groups.has(provider)) {
      groups.set(provider, {
        provider,
        label: PROVIDER_LABELS[provider] || provider,
        models: [],
      });
    }
    groups.get(provider)!.models.push({
      id: model.id,
      label: model.label || model.id,
    });
  }
  return Array.from(groups.values());
}

export async function fetchModelGroupsByType(
  modelType: 'llm' | 'vlm' | 't2i' | 'i2i' | 'video',
): Promise<ProviderGroup[]> {
  const models = await fetchApiModels({ modelType });
  return groupModelOptions(models);
}

export async function fetchVideoModelGroupsByAbility(ability: string): Promise<ProviderGroup[]> {
  const models = await fetchApiModels({ mediaType: 'video', ability, verifiedOnly: true });
  return groupModelOptions(models);
}
