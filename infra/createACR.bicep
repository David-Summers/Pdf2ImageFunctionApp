param containerRegistryName string

resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: containerRegistryName
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

