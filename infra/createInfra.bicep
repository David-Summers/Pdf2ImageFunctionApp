@minLength(5)
param uniqueStr string

// Reference to the existing ACR
resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' existing = {
  name: '${uniqueStr}acr' 
}


resource functionApp 'Microsoft.Web/sites@2022-03-01' = {
  name: '${uniqueStr}app' // 
  location: resourceGroup().location
  kind: 'functionapp'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'false'
        }
        // {
        //   name: 'DOCKER_REGISTRY_SERVER_URL'
        //   value: 'https://${acr.name}.azurecr.io'
        // }
        // {
        //   name: 'DOCKER_REGISTRY_SERVER_USERNAME'
        //   value: acr.listCredentials().username
        // }
        // {
        //   name: 'DOCKER_ENABLE_CI'
        //   value: 'true'
        // }
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${listKeys(storageAccount.id,'2019-06-01').keys[0].value};EndpointSuffix=core.windows.net'
        }
      ]
      alwaysOn: true
      linuxFxVersion: 'DOCKER|${acr.name}.azurecr.io/pythonfunc:latest'
    }
    clientAffinityEnabled: false
    virtualNetworkSubnetId: null
    publicNetworkAccess: 'Enabled'
    httpsOnly: true
  }
}

resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: '${uniqueStr}asp' // Replace with your App Service Plan name
  location: resourceGroup().location
  sku: {
    name: 'S1'
  }
  kind: 'linux'
  properties: {
    reserved: true // This is required for Linux plans.
  }
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2022-05-01' = {
  name: '${uniqueStr}appsa'
  location: resourceGroup().location
  tags: {}
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    defaultToOAuthAuthentication: true
  }
  kind: 'StorageV2'
}

resource acrPullRoleAssignment 'Microsoft.Authorization/roleAssignments@2021-04-01-preview' = {
  name: guid(acr.id, functionApp.id, 'acrpull')
  scope: acr
  properties: {
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d') // Role definition ID for AcrPull
    principalId: functionApp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

