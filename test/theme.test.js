const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const root = path.join(__dirname, '..');
const readJson = (relativePath) => JSON.parse(fs.readFileSync(path.join(root, relativePath), 'utf8'));

test('extension contributes the three coordinated themes and apply command', () => {
  const manifest = readJson('package.json');
  assert.equal(manifest.displayName, 'NV Green Dark');
  assert.equal(manifest.publisher, 'brian-chang');
  assert.equal(manifest.contributes.themes.length, 1);
  assert.equal(manifest.contributes.iconThemes.length, 1);
  assert.equal(manifest.contributes.productIconThemes.length, 1);
  assert.equal(manifest.contributes.themes[0].uiTheme, 'vs-dark');
  for (const type of ['themes', 'iconThemes', 'productIconThemes']) {
    assert.ok(fs.existsSync(path.join(root, manifest.contributes[type][0].path)));
  }
  assert.ok(manifest.contributes.commands.some((command) => command.command === 'nvGreenDark.applyAll'));
});

test('extension icon appears in the package manifest and README', () => {
  const manifest = readJson('package.json');
  const readme = fs.readFileSync(path.join(root, 'README.md'), 'utf8');
  assert.equal(manifest.icon, 'assets/extension-icon.png');
  assert.ok(fs.existsSync(path.join(root, manifest.icon)));
  assert.match(readme, /!\[NV Green Dark icon\]\(assets\/extension-icon\.png\)/);
});

test('dark palette covers workbench, syntax, semantic tokens, and terminal', () => {
  const theme = readJson('themes/nv-green-dark-color-theme.json');
  const colors = theme.colors;
  for (const key of [
    'editor.background', 'editor.foreground', 'sideBar.background',
    'activityBar.background', 'statusBar.background', 'titleBar.activeBackground',
    'terminal.background', 'terminal.ansiGreen', 'panel.background',
    'tab.activeBackground', 'input.background', 'button.background',
    'editor.selectionBackground', 'focusBorder',
  ]) assert.match(colors[key], /^#[0-9a-fA-F]{6,8}$/);
  assert.ok(theme.tokenColors.some((rule) => String(rule.scope).includes('comment')));
  assert.ok(theme.tokenColors.some((rule) => String(rule.scope).includes('string')));
  assert.ok(theme.semanticHighlighting);
  assert.ok(theme.semanticTokenColors.variable);
  assert.ok(theme.semanticTokenColors.function);
});

test('file icons include common development formats and fallback images', () => {
  const icons = readJson('themes/nv-green-dark-icon-theme.json');
  for (const category of ['file', 'folder', 'folderExpanded']) {
    assert.ok(icons.iconDefinitions[icons[category]]);
  }
  for (const extension of ['js', 'ts', 'py', 'c', 'cpp', 'h', 'json', 'yaml', 'md', 'hex', 'bin', 'log']) {
    assert.ok(icons.iconDefinitions[icons.fileExtensions[extension]], extension);
  }
  for (const definition of Object.values(icons.iconDefinitions)) {
    assert.ok(fs.existsSync(path.join(root, 'themes', definition.iconPath)), definition.iconPath);
  }
});

test('product icon font provides coherent controls', () => {
  const icons = readJson('themes/nv-green-dark-product-icon-theme.json');
  assert.ok(fs.existsSync(path.join(root, 'themes', icons.fonts[0].src[0].path)));
  for (const id of ['add', 'close', 'search', 'settings-gear', 'refresh', 'chevron-right', 'chevron-down', 'files', 'extensions', 'terminal']) {
    assert.match(icons.iconDefinitions[id].fontCharacter, /^\\[0-9a-fA-F]{4}$/);
  }
});

test('apply command sets all themes at user scope', async () => {
  const manifest = readJson('package.json');
  let handler;
  const updates = [];
  const vscode = {
    ConfigurationTarget: { Global: 'global' },
    commands: { registerCommand: (_name, callback) => { handler = callback; return { dispose() {} }; } },
    workspace: { getConfiguration: (section) => ({ update: async (key, value, target) => { updates.push([section, key, value, target]); } }) },
    window: { showInformationMessage() {} },
  };
  const extension = require('../source/extension');
  extension.activate({ subscriptions: [] }, vscode);
  await handler();
  assert.deepEqual(updates, [
    ['workbench', 'colorTheme', manifest.contributes.themes[0].label, 'global'],
    ['workbench', 'iconTheme', manifest.contributes.iconThemes[0].id, 'global'],
    ['workbench', 'productIconTheme', manifest.contributes.productIconThemes[0].id, 'global'],
  ]);
});
