resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: 'pythonfunc' // Replace with your ACR name
  location: resourceGroup().location
  sku: {
    name: 'Standard' // Choose between Basic, Standard, and Premium
  }
  properties: {
    adminUserEnabled: true
  }
}

resource functionApp 'Microsoft.Web/sites@2023-12-01' = {
  name: 'pdfpythonfuncapp' // Replace with your Azure Function name
  location: resourceGroup().location
  kind: 'functionapp'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python' // Or your desired runtime
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_URL'
          value: 'https://${acr.name}.azurecr.io'
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_USERNAME'
          value: acr.listCredentials().username 
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_PASSWORD'
          value: acr.listCredentials().passwords[0].value
        }
      ]
    }
  }
}

resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: 'pdfpythonfuncasp' // Replace with your App Service Plan name
  location: resourceGroup().location
  sku: {
    name: 'S1' // This is the consumption plan. Adjust as necessary for your needs.
  }
  kind: 'linux'
  properties: {
    reserved: true // This is required for Linux plans.
  }
}
