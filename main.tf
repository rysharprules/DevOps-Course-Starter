terraform {
    backend "azurerm" {
      resource_group_name   = "AmericanExpress1_RyanSharp_ProjectExercise"
      storage_account_name  = "rysharpstorage"
      container_name        = "tododb"
      key                   = "https://ryvault.vault.azure.net/secrets/ARM-ACCESS-KEY/edbab94b287442cc89ec22a21a1c3e6a"
    }
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = ">= 2.49"
        }
    }
}
provider "azurerm" {
    features {}
}
data "azurerm_resource_group" "main" {
    name = "AmericanExpress1_RyanSharp_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
    name = "terraformed-asp"
    location = var.LOCATION
    resource_group_name = data.azurerm_resource_group.main.name
    kind = "Linux"
    reserved = true
    sku {
        tier = "Basic"
        size = "B1"
    }
}

resource "azurerm_app_service" "main" {
    name = "rysharp-terraform-todoapp"
    location = var.LOCATION
    resource_group_name = data.azurerm_resource_group.main.name
    app_service_plan_id = azurerm_app_service_plan.main.id
    site_config {
        app_command_line = ""
        linux_fx_version = "DOCKER|rysharp/todo-app:latest"
    }
    app_settings = {
        "MONGODB_CONNECTION_STRING" = "mongodb://${azurerm_cosmosdb_account.maindbaccount.name}:${azurerm_cosmosdb_account.maindbaccount.primary_key}@${azurerm_cosmosdb_account.maindbaccount.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
        "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
        "CLIENT_ID" = var.CLIENT_ID
        "CLIENT_SECRET" = var.CLIENT_SECRET
        "DOCKER_ENABLE_CI" = "true"
        "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io/v1"
        "FLASK_APP" = "todo_app.app"
        "FLASK_ENV" = "production"
        "SECRET_KEY" = var.SECRET_KEY
        "OAUTHLIB_INSECURE_TRANSPORT"="1"
    }
}

resource "azurerm_cosmosdb_account" "maindbaccount" {
  name                = "rysharp"
  resource_group_name = data.azurerm_resource_group.main.name
  location            = var.LOCATION
  offer_type          = "Standard"
  kind                = "MongoDB"

  capabilities {
    name = "EnableMongo"
  }
  capabilities {
    name = "EnableServerless"
  }
  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 10
    max_staleness_prefix    = 200
  }
  geo_location {
    location          = var.LOCATION
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "maindb" {
  name                = "rysharp-terraform"
  resource_group_name = azurerm_cosmosdb_account.maindbaccount.resource_group_name
  account_name        = azurerm_cosmosdb_account.maindbaccount.name
}