import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const dir = new URL('../n8n/workflows/', import.meta.url);
const files = readdirSync(dir).filter((file) => file.endsWith('.json'));
const errors = [];

for (const file of files) {
  const path = join(dir.pathname, file);
  try {
    const workflow = JSON.parse(readFileSync(path, 'utf8'));
    if (!workflow.name) errors.push(`${file}: missing name`);
    if (!Array.isArray(workflow.nodes) || workflow.nodes.length === 0) errors.push(`${file}: missing nodes`);
    if (!workflow.connections || typeof workflow.connections !== 'object') errors.push(`${file}: missing connections`);
    for (const node of workflow.nodes || []) {
      if (!node.id || !node.name || !node.type || !node.typeVersion) errors.push(`${file}: invalid node ${node.name || node.id || 'unknown'}`);
    }
  } catch (error) {
    errors.push(`${file}: ${error.message}`);
  }
}

if (errors.length) {
  console.error(errors.join('\n'));
  process.exit(1);
}

console.log(`Validated ${files.length} n8n workflow JSON files.`);
