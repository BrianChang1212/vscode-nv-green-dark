const manifest = require('../package.json');

function activate(context, vscodeApi = require('vscode')) {
  const command = vscodeApi.commands.registerCommand('nvGreenDark.applyAll', async () => {
    const settings = vscodeApi.workspace.getConfiguration('workbench');
    try {
      await settings.update('colorTheme', manifest.contributes.themes[0].label, vscodeApi.ConfigurationTarget.Global);
      await settings.update('iconTheme', manifest.contributes.iconThemes[0].id, vscodeApi.ConfigurationTarget.Global);
      await settings.update('productIconTheme', manifest.contributes.productIconThemes[0].id, vscodeApi.ConfigurationTarget.Global);
      await vscodeApi.window.showInformationMessage('NV Green Dark is active.');
    } catch (error) {
      await vscodeApi.window.showErrorMessage(`NV Green Dark could not apply every theme: ${error.message}`);
      throw error;
    }
  });
  context.subscriptions.push(command);
}

module.exports = { activate };
