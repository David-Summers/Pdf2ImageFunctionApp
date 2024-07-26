@minLength(5)
param uniqueStr string

resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: '${uniqueStr}acr' // Replace with your ACR name
  location: resourceGroup().location
  sku: {
    name: 'Standard' // Choose between Basic, Standard, and Premium
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    adminUserEnabled: false
  }
}
